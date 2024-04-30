import random
from multiprocessing import Process
import settings
import typing
from jinja2 import Environment, FileSystemLoader
from .Items import BanjoTooieItem, all_item_table, all_group_table
from .Locations import BanjoTooieLocation, all_location_table
from .Regions import BANJOTOOIEREGIONS, create_regions, connect_regions
from .Options import BanjoTooieOptions
from .Rules import BanjoTooieRules
from .Names import itemName, locationName, regionName

#from Utils import get_options
from BaseClasses import ItemClassification, Tutorial, Item, Region, MultiWorld
#from Fill import fill_restrictive
from ..AutoWorld import World, WebWorld
from ..LauncherComponents import Component, components, Type


def run_client():
    from worlds.banjo_tooie.BTClient import main  # lazy import
    p = Process(target=main)
    p.start()

components.append(Component("Banjo-Tooie Client", func=run_client, component_type=Type.CLIENT))

class BanjoTooieWeb(WebWorld):
    setup = Tutorial("Setup Banjo-Tooie",
        """A guide to setting up Archipelago Banjo-Tooie on your computer.""",
        "English",
        "setup_en.md",
        "setup/en",
        ["Beebaleen"])
    
    tutorials = [setup]
    

class BanjoTooieWorld(World):
    """
    Banjo-Tooie is a single-player platform game in which the protagonists are controlled from a third-person perspective.
    Carrying over most of the mechanics and concepts established in its predecessor,
    the game features three-dimensional worlds consisting of various platforming challenges and puzzles, with a notable
    increased focus on puzzle-solving over the worlds of Banjo-Kazooie.
    """
    
    game: str = "Banjo-Tooie"
    web = BanjoTooieWeb()
    topology_preset = True
    # item_name_to_id = {name: data.btid for name, data in all_item_table.items()}
    item_name_to_id = {}

    for name, data in all_item_table.items():
        if data.btid is None:  # Skip Victory Item
            continue
        item_name_to_id[name] = data.btid

    location_name_to_id = {name: data.btid for name, data in all_location_table.items()}

    item_name_groups = {
        # "Jiggy": all_group_table["jiggy"],
        "Jinjo": all_group_table["jinjo"],
        "Moves": all_group_table["moves"],
        "Magic": all_group_table["magic"],
        "Stations": all_group_table["stations"],
        "Access": all_group_table["levelaccess"],
    }
        
    options_dataclass =  BanjoTooieOptions
    options: BanjoTooieOptions

    def __init__(self, world, player):

        self.kingjingalingjiggy = False
        self.jiggy_counter: int = 0
        self.doubloon_counter: int = 0
        self.slot_data = []
        self.use_cheato_filler = False
        self.randomize_worlds = {}
        self.world_sphere_1 = [
            regionName.MT,
            regionName.GM,
            regionName.WW,
            regionName.JR,
            regionName.HP,
            regionName.TL,
            regionName.CC,
            regionName.GIO
        ]
        self.world_sphere_2 = [
        ]
        self.worlds_randomized = False
        super(BanjoTooieWorld, self).__init__(world, player)

        
    

    def create_item(self, itemname: str) -> Item:
        banjoItem = all_item_table.get(itemname)
        if banjoItem.type == 'progress':
            if banjoItem.btid == 1230515:
                if self.jiggy_counter <= 70:
                    item_classification = ItemClassification.progression
                else:
                    item_classification = ItemClassification.filler
                self.jiggy_counter += 1
            else:
                item_classification = ItemClassification.progression
        if banjoItem.type == 'useful':
            if banjoItem.btid == 1230513 and self.use_cheato_filler == False:
                item_classification = ItemClassification.useful
            elif banjoItem.btid == 1230513 and self.use_cheato_filler == True:
                item_classification = ItemClassification.filler
            else:
                item_classification = ItemClassification.useful

        if banjoItem.type == 'filler':
            item_classification = ItemClassification.filler

        if banjoItem.type == 'trap':
            item_classification = ItemClassification.trap

        if banjoItem.type == "victory":
            victory_item = BanjoTooieItem("Kick Around", ItemClassification.filler, None, self.player)
            return victory_item

        created_item = BanjoTooieItem(self.item_id_to_name[banjoItem.btid], item_classification, banjoItem.btid, self.player)
        return created_item

    def create_event_item(self, name: str) -> Item:
        item_classification = ItemClassification.progression
        created_item = BanjoTooieItem(name, item_classification, None, self.player)
        return created_item
    
    def create_items(self) -> None:
        itempool = []
        if self.options.cheato_as_filler == True:
            self.use_cheato_filler = True
        for name,id in all_item_table.items():
            item = self.create_item(name)
            if self.item_filter(item):
                if item.code == 1230515 and self.kingjingalingjiggy == True:
                    for i in range(id.qty - 1): #note the -1 in the count here. King Took one already.
                        if self.options.randomize_jinjos == False and self.jiggy_counter > 81:
                            break
                        else:
                            itempool += [self.create_item(name)]
                else:
                    for i in range(id.qty):
                        if self.options.randomize_jinjos == False and self.jiggy_counter > 81 and item.code == 1230515:
                            break
                        else:
                            itempool += [self.create_item(name)]
        
        for item in itempool:
            self.multiworld.itempool.append(item)

    def item_filter(self, item: Item) -> Item:
        if(item.code == 1230515 and self.kingjingalingjiggy == False and self.options.jingaling_jiggy == True):
            #Below give the king a guarentee Jiggy if option is set
            self.multiworld.get_location(self.location_id_to_name[1230685], self.player).place_locked_item(item)
            self.kingjingalingjiggy = True
            return True #doesn't need to be in the Pool.
        
        if item.code == 0: #Events
            return False
        
        if(item.code == 1230514 and self.options.randomize_doubloons == False) :
            return False
        
        if(item.code == 1230513 and self.options.randomize_cheato == False) : # Added later in Prefill
            return False
        
        if(item.code == 1230512 and self.options.randomize_honeycombs == False) : # Added later in Prefill
            return False
        
        if(item.code in range(1230753, 1230778) and self.options.randomize_moves == False) : #range you need to add +1 to the end. 
            return False
        
        if(item.code in range(1230174, 1230183) and self.options.randomize_glowbos == False) : #range you need to add +1 to the end.
            return False
        
        if(item.code in range(1230855, 1230864) and self.options.randomize_glowbos == False) : #range you need to add +1 to the end.
            return False

        if(item.code in range(1230501, 1230510) and self.options.randomize_jinjos == False) :#range you need to add +1 to the end.
            return False
        
        if(item.code == 1230778 and self.options.randomize_treble == False):
            return False
        
        if item.code == 1230796 and self.options.randomize_chuffy == False:
            return False
        
        if item.code in range(1230790, 1230796) and self.options.randomize_stations == False:
            return False
        
        if item.code == 1230797 and self.options.randomize_notes == False: #Notes
            return False
        
        if item.code == 1230798: #mumbo tokens for Mini Game and Boss Hunt
            return False
        
        # if item.code == 1230799 and self.options.warp_traps == 0: 
        #     return False
        
        if item.code in range(1230944, 1230952):
            return False

        return True

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)

    def generate_early(self) -> None:
        # Universal Tracker Magic
        if hasattr(self.multiworld, "re_gen_passthrough"): 
            if "Banjo-Tooie" in self.multiworld.re_gen_passthrough:
                passthrough = self.multiworld.re_gen_passthrough["Banjo-Tooie"]
                self.randomize_worlds = passthrough['world_order']
                self.worlds_randomized = passthrough['worlds']
        else:
            if self.options.randomize_worlds and self.options.randomize_moves == True and \
            self.options.skip_puzzles == True:
                random.shuffle(self.world_sphere_1)
                first_level = self.world_sphere_1[0]
                # #temp
                # while first_level != regionName.TL:
                #     random.shuffle(self.world_sphere_1)
                #     first_level = self.world_sphere_1[0]
                # #temp
                all_good = False
                while(all_good == False):
                    if first_level == regionName.GIO and (self.options.randomize_cheato == False or self.options.randomize_jinjos == False or \
                    self.options.randomize_notes == False):
                        random.shuffle(self.world_sphere_1)
                        first_level = self.world_sphere_1[0]
                        continue
                    elif first_level == regionName.TL and (self.options.randomize_cheato == False or self.options.randomize_jinjos == False) and \
                    self.options.randomize_notes == False:
                        random.shuffle(self.world_sphere_1)
                        first_level = self.world_sphere_1[0]
                        continue
                    elif first_level == regionName.CC and (self.options.randomize_cheato == False or self.options.randomize_jinjos == False) and \
                    self.options.randomize_notes == False:
                        random.shuffle(self.world_sphere_1)
                        first_level = self.world_sphere_1[0]
                        continue
                    elif first_level == regionName.WW and (self.options.randomize_cheato == False or self.options.randomize_jinjos == False) and \
                    self.options.randomize_notes == False:
                        random.shuffle(self.world_sphere_1)
                        first_level = self.world_sphere_1[0]
                        continue
                    else:
                        all_good = True
                i = 1
                for world in self.world_sphere_1:
                    if i == 1:
                        self.randomize_worlds.update({world: 1})
                        i = i+1
                    else:
                        self.world_sphere_2.append(world)

                random.shuffle(self.world_sphere_2)
                for world in self.world_sphere_2:
                    if i == 2:
                        self.randomize_worlds.update({world: 4})
                    elif i == 3:
                        self.randomize_worlds.update({world: 8})
                    elif i == 4:
                        self.randomize_worlds.update({world: 14})
                    elif i == 5:
                        self.randomize_worlds.update({world: 20})
                    elif i == 6:
                        self.randomize_worlds.update({world: 28})
                    elif i == 7:
                        self.randomize_worlds.update({world: 36})
                    elif i == 8:
                        self.randomize_worlds.update({world: 45})
                    i = i+1
                first_level = list(self.randomize_worlds.keys())[0]

                if  first_level != regionName.MT and self.options.logic_type != 2:
                    self.multiworld.early_items[self.player][itemName.GGRAB] = 1
                if  first_level == regionName.WW:
                    self.multiworld.early_items[self.player][itemName.FEGGS] = 1
                if  first_level == regionName.JR or first_level == regionName.HP:
                    self.multiworld.early_items[self.player][itemName.SPLITUP] = 1
                if first_level == regionName.TL or first_level == regionName.CC:
                    self.multiworld.early_items[self.player][itemName.FEGGS] = 1
                    self.multiworld.early_items[self.player][itemName.TTORP] = 1
                if first_level == regionName.GIO:
                    self.multiworld.early_items[self.player][itemName.FEGGS] = 1
                    self.multiworld.early_items[self.player][itemName.TTORP] = 1
                    # self.multiworld.early_items[self.player][itemName.SPRINGB] = 1
                    # self.multiworld.early_items[self.player][itemName.CLAWBTS] = 1
                self.worlds_randomized = True
            else:
                self.randomize_worlds = {
                    regionName.MT: 1,
                    regionName.GM: 4,
                    regionName.WW: 8,
                    regionName.JR: 14,
                    regionName.TL: 20,
                    regionName.GIO: 28,
                    regionName.HP:  36,
                    regionName.CC:  45, 
                }
                self.worlds_randomized = False

    def set_rules(self) -> None:
        rules = Rules.BanjoTooieRules(self)
        return rules.set_rules()
    
    def pre_fill(self) -> None:
        if self.options.randomize_honeycombs == False:
            self.banjo_pre_fills(itemName.HONEY, "Honeycomb", False)
                    
        if self.options.randomize_cheato == False:
            self.banjo_pre_fills(itemName.PAGES, "Page", False)

        if self.options.randomize_doubloons == False:
            self.banjo_pre_fills(itemName.DOUBLOON, "Doubloon", False)

        if self.options.randomize_moves == False:
            self.banjo_pre_fills("Moves", None, True)

        if self.options.randomize_glowbos == False:
            self.banjo_pre_fills("Magic", None, True)

        if self.options.randomize_treble == False:
            self.banjo_pre_fills(itemName.TREBLE, "Treble Clef", False)
        
        if self.options.randomize_stations == False:
            self.banjo_pre_fills("Stations", None, True)

        if self.options.randomize_chuffy == False:
            self.banjo_pre_fills(itemName.CHUFFY, "Chuffy", False)

        if self.options.randomize_notes == False:
         self.banjo_pre_fills(itemName.NOTE, "Note", False)

        if self.worlds_randomized == False and self.options.skip_puzzles == True:
            self.banjo_pre_fills("Access", None, True)
        elif self.worlds_randomized == True:
            world_num = 1
            for world, amt in self.randomize_worlds.items():
                if world == regionName.GIO:
                    item = self.create_item(itemName.GIA)
                else:
                    item = self.create_item(world)
                if world_num == 10:
                    self.multiworld.get_location("Boss Unlocked").place_locked_item(item)
                else:
                    self.multiworld.get_location("World "+ str(world_num) +" Unlocked", self.player).place_locked_item(item)
                    world_num = world_num + 1
        else:
            world_num = 1
            for world, amt in self.randomize_worlds.items():
                item = self.create_item(itemName.NONE)
                if world_num == 10:
                    self.multiworld.get_location("Boss Unlocked").place_locked_item(item)
                else:
                    self.multiworld.get_location("World "+ str(world_num) +" Unlocked", self.player).place_locked_item(item)
                    world_num = world_num + 1
        
        if self.options.victory_condition == 1:
            item = self.create_item(itemName.MUMBOTOKEN)
            self.multiworld.get_location(locationName.JIGGYMT3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYGM5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYWW1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYWW2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYWW4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYWW5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYJR1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYTD6, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYGI3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYGI9, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYHP8, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYCC3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYCC5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYCC8, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.CHEATOCC1, self.player).place_locked_item(item)
        
        if self.options.victory_condition == 2:
            item = self.create_item(itemName.MUMBOTOKEN)
            self.multiworld.get_location(locationName.JIGGYMT1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYGM1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYWW3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYJR7, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYTD4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.CHEATOGI3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYHP1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYCC1, self.player).place_locked_item(item)

        if self.options.victory_condition == 3:
            item = self.create_item(itemName.MUMBOTOKEN)
            self.multiworld.get_location(locationName.JIGGYIH1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH6, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH7, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH8, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH9, self.player).place_locked_item(item)
        
        elif self.options.randomize_jinjos == False:
            item = self.create_item(itemName.JIGGY)
            self.multiworld.get_location(locationName.JIGGYIH1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH6, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH7, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH8, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH9, self.player).place_locked_item(item)

        if self.options.randomize_jinjos == False:
            item = self.create_item(itemName.WJINJO)
            self.multiworld.get_location(locationName.JINJOJR5, self.player).place_locked_item(item)

            item = self.create_item(itemName.OJINJO)
            self.multiworld.get_location(locationName.JINJOWW4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOHP2, self.player).place_locked_item(item)

            item = self.create_item(itemName.YJINJO)
            self.multiworld.get_location(locationName.JINJOWW3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOHP4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOHP3, self.player).place_locked_item(item)

            item = self.create_item(itemName.BRJINJO)
            self.multiworld.get_location(locationName.JINJOGM1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOJR2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOTL2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOTL5, self.player).place_locked_item(item)

            item = self.create_item(itemName.GJINJO)
            self.multiworld.get_location(locationName.JINJOWW5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOJR1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOTL4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGI2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOHP1, self.player).place_locked_item(item)

            item = self.create_item(itemName.RJINJO)
            self.multiworld.get_location(locationName.JINJOMT2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOMT3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOMT5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOJR3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOJR4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOWW2, self.player).place_locked_item(item)

            item = self.create_item(itemName.BLJINJO)
            self.multiworld.get_location(locationName.JINJOGM3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOTL1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOHP5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOCC2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOIH1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOIH4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOIH5, self.player).place_locked_item(item)

            item = self.create_item(itemName.PJINJO)
            self.multiworld.get_location(locationName.JINJOMT1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGM5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGI3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOCC1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOCC3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOCC5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOIH2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOIH3, self.player).place_locked_item(item)

            item = self.create_item(itemName.BKJINJO)
            self.multiworld.get_location(locationName.JINJOMT4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGM2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGM4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOWW1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOTL3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGI1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGI5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOCC4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGI4, self.player).place_locked_item(item)


    def banjo_pre_fills(self, itemNameOrGroup: str, locationFindCriteria: str|None, useGroup: bool ) -> None:
        if useGroup:
            for group_name, item_info in self.item_name_groups.items():
                if group_name == itemNameOrGroup:
                    for name in item_info:
                        item = self.create_item(name)
                        banjoItem = all_item_table.get(name)
                        self.multiworld.get_location(banjoItem.defualt_location, self.player).place_locked_item(item)
        else:
            for name, id in self.location_name_to_id.items():
                item = self.create_item(itemNameOrGroup)
                if name.find(locationFindCriteria) != -1:
                    self.multiworld.get_location(name, self.player).place_locked_item(item)


    def fill_slot_data(self) -> dict[str, any]:
        btoptions = dict[str, any]()
        btoptions["player_name"] = self.multiworld.player_name[self.player]
        btoptions["seed"] = random.randint(12212, 69996)
        btoptions["deathlink"] = "true" if self.options.death_link.value == 1 else "false"
        if self.options.skip_tower_of_tragedy == 1:
            btoptions["skip_tot"] = "true"
        elif self.options.skip_tower_of_tragedy == 2:
            btoptions["skip_tot"] = "round 3"
        else:
            btoptions["skip_tot"] = "false"
        btoptions['honeycomb'] = "true" if self.options.randomize_honeycombs == 1 else "false"
        btoptions['pages'] = "true" if self.options.randomize_cheato == 1 else "false"
        btoptions['moves'] = "true" if self.options.randomize_moves == 1 else "false"
        btoptions['doubloons'] = "true" if self.options.randomize_doubloons == 1 else "false"
        btoptions['minigames'] = 'skip' if self.options.speed_up_minigames == 1 else "full"
        btoptions['trebleclef'] = "true" if self.options.randomize_treble == 1 else "false"
        btoptions['skip_puzzles'] = "true" if self.options.skip_puzzles == 1 else "false"
        btoptions['open_hag1'] = "true" if self.options.open_hag1 == 1 else "false"
        btoptions['stations']= "true" if self.options.randomize_stations == 1 else "false"
        btoptions['chuffy']= "true" if self.options.randomize_chuffy == 1 else "false"
        btoptions['jinjo']= "true" if self.options.randomize_jinjos == 1 else "false"
        btoptions['notes']= "true" if self.options.randomize_notes == 1 else "false"
        btoptions['worlds']= "true" if self.worlds_randomized else "false"
        btoptions['world_order'] = self.randomize_worlds
        btoptions['goal_type'] = int(self.options.victory_condition.value)
        btoptions['minigame_hunt_length'] = int(self.options.minigame_hunt_length.value)
        btoptions['boss_hunt_length'] = int(self.options.boss_hunt_length.value)
        btoptions['jinjo_family_rescue_length'] = int(self.options.jinjo_family_rescue_length.value)
        # btoptions['warp_traps'] = int(self.options.warp_traps.value)
        return btoptions

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data

    