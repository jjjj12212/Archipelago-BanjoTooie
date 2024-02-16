import asyncio
import json
import os
import multiprocessing
import copy
import subprocess
import zipfile
from asyncio import StreamReader, StreamWriter

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
import Utils
from Utils import async_start
from worlds import network_data_package

SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart banjoTooie_connector.lua"
CONNECTION_REFUSED_STATUS = "Connection refused. Please start your emulator and make sure banjoTooie_connector.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart banjoTooie_connector.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

"""
Payload: lua -> client
{
    playerName: string,
    locations: dict,
    deathlinkActive: bool,
    isDead: bool,
    gameComplete: bool
}

Payload: client -> lua
{
    items: list,
    playerNames: list,
    triggerDeath: bool,
    messages: string
}

Deathlink logic:
"Dead" is true <-> Link is at 0 hp.

deathlink_pending: we need to kill the player
deathlink_sent_this_death: we interacted with the multiworld on this death, waiting to reset with living link

"""

bt_loc_name_to_id = network_data_package["games"]["Banjo Tooie"]["location_name_to_id"]

script_version: int = 3

def get_item_value(ap_id):
    return ap_id


class BanjoTooieCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx): 
        super().__init__(ctx)

    def _cmd_n64(self):
        """Check N64 Connection State"""
        if isinstance(self.ctx, BanjoTooieContext):
            logger.info(f"N64 Status: {self.ctx.n64_status}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, BanjoTooieContext):
            self.ctx.deathlink_client_override = True
            self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
            async_start(self.ctx.update_death_link(self.ctx.deathlink_enabled), name="Update Deathlink")


class BanjoTooieContext(CommonContext):
    command_processor = BanjoTooieCommandProcessor
    items_handling = 0b001 #full

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = 'Banjo Tooie'
        self.n64_streams: (StreamReader, StreamWriter) = None
        self.n64_sync_task = None
        self.n64_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.location_table = {}
        self.deathlink_enabled = False
        self.deathlink_pending = False
        self.deathlink_sent_this_death = False
        self.deathlink_client_override = False
        self.version_warning = False
        self.messages = ""
        self.slot_data = {}
        self.sendSlot = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(BanjoTooieContext, self).server_auth(password_requested)
        if not self.auth:
            await self.get_username()
            await self.send_connect()
            self.awaiting_rom = True
            # logger.info('Awaiting connection to EmuHawk to get player information')
            return
        return

    def _set_message(self, msg: str, msg_id: int):
        self.messages = msg

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        super().on_deathlink(data)

    def run_gui(self):
        from kvui import GameManager

        class BanjoTooieManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Banjo Tooie Client"

        self.ui = BanjoTooieManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd, args):
        if cmd == 'Connected':
            self.slot_data = args.get('slot_data', None)
            self.deathlink_enabled = self.slot_data["deathlink"]
            logger.info("Please open Banjo Tooie and load banjoTooie_connector.lua")
            self.n64_sync_task = asyncio.create_task(n64_sync_task(self), name="N64 Sync")
        elif cmd == 'Print':
            msg = args['text']
            if ': !' not in msg:
                self._set_message(msg, SYSTEM_MESSAGE_ID)

    def on_print_json(self, args: dict):
        if self.ui:
            self.ui.print_json(copy.deepcopy(args["data"]))
        else:
            text = self.jsontotextparser(copy.deepcopy(args["data"]))
            logger.info(text)
        relevant = args.get("type", None) in {"Hint", "ItemSend"}
        if relevant:
            getitem = False
            item = args["item"]
            # found in this world
            if self.slot_concerns_self(args["receiving"]):
                relevant = True      
                getitem = True
            # goes in this world
            elif self.slot_concerns_self(item.player):
                relevant = True
            # not related
            else:
                relevant = False
            if relevant:
                item = args["item"]
                if getitem:
                    self.items_received.append(item)
                msg = self.raw_text_parser(copy.deepcopy(args["data"]))
                self._set_message(msg, item.item)


def get_payload(ctx: BanjoTooieContext):
    if ctx.deathlink_enabled and ctx.deathlink_pending:
        trigger_death = True
        ctx.deathlink_sent_this_death = True
    else:
        trigger_death = False

    if(len(ctx.items_received) > 0):
        print("Recieving Item")

    payload = json.dumps({
            "items": [get_item_value(item.item) for item in ctx.items_received],
            "playerNames": [name for (i, name) in ctx.player_names.items() if i != 0],
            "triggerDeath": trigger_death,
            "messages": ctx.messages,
        })
    if len(ctx.messages) > 0:
        ctx.messages = ""
    if len(ctx.items_received) > 0:
        ctx.items_received = []
    return payload

def get_slot_payload(ctx: BanjoTooieContext):
    payload = json.dumps({
            "slot_player": ctx.slot_data["player_name"],
            "slot_seed": ctx.slot_data["seed"],
            "slot_deathlink": ctx.deathlink_enabled
        })
    ctx.sendSlot = False
    return payload


async def parse_payload(payload: dict, ctx: BanjoTooieContext, force: bool):

    # Refuse to do anything if ROM is detected as changed
    if ctx.auth and payload['playerName'] != ctx.auth:
        logger.warning("ROM change detected. Disconnecting and reconnecting...")
        ctx.deathlink_enabled = False
        ctx.deathlink_client_override = False
        ctx.finished_game = False
        ctx.location_table = {}
        ctx.deathlink_pending = False
        ctx.deathlink_sent_this_death = False
        ctx.auth = payload['playerName']
        await ctx.send_connect()
        return

    # Turn on deathlink if it is on, and if the client hasn't overriden it
    if payload['deathlinkActive'] and not ctx.deathlink_enabled and not ctx.deathlink_client_override:
        await ctx.update_death_link(True)
        ctx.deathlink_enabled = True

    # Game completion handling
    if payload['gameComplete'] and not ctx.finished_game:
        await ctx.send_msgs([{
            "cmd": "StatusUpdate",
            "status": 30
        }])
        ctx.finished_game = True

    # Locations handling
    locations = payload['locations']

    # The Lua JSON library serializes an empty table into a list instead of a dict. Verify types for safety:
    if isinstance(locations, list):
        locations = {}


    if ctx.location_table != locations:
        ctx.location_table = locations

        locs1 = [bt_loc_name_to_id[loc] for loc, b in ctx.location_table.items() if b]

        await ctx.send_msgs([{
            "cmd": "LocationChecks",
            "locations": locs1
        }])

    # Deathlink handling
    if ctx.deathlink_enabled:
        if payload['isDead']: #Banjo died
            ctx.deathlink_pending = False
            if not ctx.deathlink_sent_this_death:
                ctx.deathlink_sent_this_death = True
                await ctx.send_death()
        else: # Banjo is somehow still alive
            ctx.deathlink_sent_this_death = False


async def n64_sync_task(ctx: BanjoTooieContext): 
    logger.info("Starting n64 connector. Use /n64 for status information.")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.n64_streams:
            (reader, writer) = ctx.n64_streams
            if ctx.sendSlot == True:
                msg = get_slot_payload(ctx).encode()
            else:
                msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    data = await asyncio.wait_for(reader.readline(), timeout=10)
                    data_decoded = json.loads(data.decode())
                    reported_version = data_decoded.get('scriptVersion', 0)
                    getSlotData = data_decoded.get('getSlot', 0)
                    if getSlotData == True:
                        ctx.sendSlot = True
                    elif reported_version >= script_version:
                        if ctx.game is not None and 'locations' in data_decoded:
                            # Not just a keep alive ping, parse
                            async_start(parse_payload(data_decoded, ctx, False))
                        if not ctx.auth:
                            ctx.auth = data_decoded['playerName']
                            if ctx.awaiting_rom:
                                await ctx.server_auth(False)
                    else:
                        if not ctx.version_warning:
                            logger.warning(f"Your Lua script is version {reported_version}, expected {script_version}. "
                                "Please update to the latest version. "
                                "Your connection to the Archipelago server will not be accepted.")
                            ctx.version_warning = True
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.n64_streams = None
                except ConnectionResetError as e:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.n64_streams = None
            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.n64_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.n64_streams = None
            if ctx.n64_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to N64")
                    ctx.n64_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.n64_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.n64_status = error_status
                logger.info("Lost connection to N64 and attempting to reconnect. Use /n64 for status updates")
        else:
            try:
                logger.debug("Attempting to connect to N64")
                ctx.n64_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 21221), timeout=10)
                ctx.n64_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.n64_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.n64_status = CONNECTION_REFUSED_STATUS
                continue


if __name__ == '__main__':

    Utils.init_logging("Banjo Tooie Client")

    async def main():
        multiprocessing.freeze_support()
        parser = get_base_parser()
        args = parser.parse_args()

        ctx = BanjoTooieContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.n64_sync_task:
            await ctx.n64_sync_task

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()
