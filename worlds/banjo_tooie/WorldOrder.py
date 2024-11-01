import random
from .Names import itemName, regionName
from typing import TYPE_CHECKING, List

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import BanjoTooieWorld
else:
    BanjoTooieWorld = object

# Shamelessly Stolen from KH2 :D


def WorldRandomize(world: BanjoTooieWorld) -> None:
    # Universal Tracker Magic
    if hasattr(world.multiworld, "re_gen_passthrough"): 
        if "Banjo-Tooie" in world.multiworld.re_gen_passthrough:
            passthrough = world.multiworld.re_gen_passthrough["Banjo-Tooie"]
            world.randomize_worlds = passthrough['world_order']
            world.randomize_order = passthrough['world_keys']
            world.worlds_randomized = bool(passthrough['worlds'] == 'true') 
            world.starting_egg = passthrough['starting_egg']
            world.starting_attack = passthrough['starting_attack']
            world.single_silo = passthrough['first_silo']
            world.loading_zones = passthrough['loading_zones']
    else:
        randomize_level_order(world)
        set_level_costs(world)
        randomize_entrance_loading_zones(world)
        choose_unlocked_silos(world)
        handle_early_moves(world)

def randomize_level_order(world: BanjoTooieWorld) -> None:
    world.worlds_randomized = world.options.randomize_worlds.value
    if not world.worlds_randomized:
        world.randomize_order = {
            regionName.MT:  1230944, #These ids stay in the same order, but the keys may switch order when randomized.
            regionName.GM:  1230945,
            regionName.WW:  1230946,
            regionName.JR:  1230947,
            regionName.TL:  1230948,
            regionName.GIO: 1230949,
            regionName.HP:  1230950,
            regionName.CC:  1230951,
            regionName.CK:  1230952 
        }
    else:
        if world.options.randomize_world_loading_zone:
            randomizable_levels = [regionName.MT,regionName.GM,regionName.WW,regionName.JR,regionName.TL,regionName.GIO,regionName.HP,regionName.CC,regionName.CK]
            world_order = generate_world_order(world, randomizable_levels)

            world.randomize_order = {world_order[i]: i+1230944 for i in range(len(world_order))}
        else:
            randomizable_levels = [regionName.MT,regionName.GM,regionName.WW,regionName.JR,regionName.TL,regionName.GIO,regionName.HP,regionName.CC]
            world_order = generate_world_order(world, randomizable_levels)
            world.randomize_order = {world_order[i]: i+1230944 for i in range(len(world_order))}
            world.randomize_order.update({regionName.CK: 1230952})

def generate_world_order(world: BanjoTooieWorld, worlds: List[str]) -> List[str]:
    good_order = False
    while not good_order:
        good_order = True
        random.shuffle(worlds)

        # Fewer than 4 collectibles to get progressive Claw Clambers.
        if world.options.progressive_shoes.value and worlds[0] == regionName.CK:
            good_order = False

        # Not enough collectibles in the overworld to get to Quag
        if world.options.randomize_bk_moves.value != 2 and world.options.open_silos.value == 0 and worlds[0] in [regionName.GIO, regionName.CK]:
            good_order = False

        # The 2nd world needs to be not too hard to access from the first world.
        easy_2nd_worlds = {
            regionName.MT: [regionName.GM],
            regionName.GM: [regionName.MT, regionName.WW, regionName.JR, regionName.HP],
            regionName.WW: [regionName.MT, regionName.GM, regionName.TL, regionName.CC],
            regionName.JR: [regionName.MT, regionName.GM, regionName.HP],
            # GI is not easy when you need 3 progressive shoes.
            regionName.TL: [regionName.MT, regionName.GM, regionName.WW, regionName.CC] if world.options.progressive_shoes.value else [regionName.MT, regionName.GM, regionName.WW, regionName.GIO, regionName.CC],
            # Reaching CK is not easy when you need 4 progressive shoes.
            regionName.GIO: [regionName.MT, regionName.GM, regionName.GIO, regionName.TL, regionName.CC] if world.options.progressive_shoes.value else [regionName.MT, regionName.GM, regionName.GIO, regionName.TL, regionName.CC, regionName.CK],
            regionName.HP:  [regionName.MT, regionName.GM, regionName.JR],
            # Same thing with GI here.
            regionName.CC: [regionName.MT, regionName.GM, regionName.WW, regionName.TL] if world.options.progressive_shoes.value else [regionName.MT, regionName.GM, regionName.WW, regionName.GIO, regionName.TL],
            regionName.CK:  [regionName.MT, regionName.GM, regionName.GIO, regionName.TL, regionName.CC] 
        }
        if worlds[1] not in easy_2nd_worlds[worlds[0]]:
            good_order = False
    return worlds

def set_level_costs(world: BanjoTooieWorld) -> None:
    normal_costs = [1,4,8,14,20,28,36,45,55]
    quick_costs = [1,3,6,10,15,21,28,35,44]
    long_costs = [1,8,16,25,34,43,52,60,70]
    custom_costs = [
        world.options.world_1.value,
        world.options.world_2.value,
        world.options.world_3.value,
        world.options.world_4.value,
        world.options.world_5.value,
        world.options.world_6.value,
        world.options.world_7.value,
        world.options.world_8.value,
        world.options.world_9.value
    ]

    chosen_costs = []
    if world.options.game_length.value == 0:
        chosen_costs = quick_costs
    elif world.options.game_length.value == 1:
        chosen_costs = normal_costs
    elif world.options.game_length.value == 2:
        chosen_costs = long_costs
    elif world.options.game_length.value == 3:
        chosen_costs = custom_costs
    
    world.randomize_worlds = {list(world.randomize_order.keys())[i]: chosen_costs[i] for i in range(len(list(world.randomize_order.keys())))}


def randomize_entrance_loading_zones(world: BanjoTooieWorld) -> None:
    randomizable_levels = list(world.randomize_worlds.keys()) # Gives the levels in the order that they open.
    if not world.options.randomize_world_loading_zone:
        world.loading_zones = {level: level for level in randomizable_levels}
    else:
        randomized_levels = randomizable_levels[::]
        random.shuffle(randomized_levels)
        while randomized_levels[0] in [regionName.CK, regionName.GIO]:
            random.shuffle(randomized_levels)
        world.loading_zones = {randomizable_levels[i]: randomized_levels[i] for i in range(len(randomizable_levels))}


def choose_unlocked_silos(world: BanjoTooieWorld) -> None:
    if not world.options.randomize_bk_moves.value == 2 and world.options.open_silos.value == 0:
        world.single_silo = "NONE"

    elif world.options.open_silos.value == 2:
        world.single_silo = "ALL"

    elif world.options.randomize_bk_moves.value == 2 and world.options.randomize_worlds.value == 1:
        # One silo is necessary to make decent progress in the overworld, so we pick the one that's the closest to the first world.

        if list(world.randomize_order.keys())[0] == regionName.GIO:
            # GI is special. If loading zones are not randomized, the only way to make progress in the level is by riding the train into the level from Cliff Top.
            world.single_silo = regionName.IOHQM if world.options.randomize_world_loading_zone else regionName.IOHCT
        else:
            overworld_lookup = {
                regionName.MT: random.choice([regionName.IOHPL, regionName.IOHPG, regionName.IOHCT, regionName.IOHQM]), # You can already get there, so you get a bonus silo! (Nobody likes Mayahell anyway.)
                regionName.GM: regionName.IOHPL,
                regionName.WW: regionName.IOHPG,
                regionName.JR: regionName.IOHCT,
                regionName.TL: regionName.IOHWL,
                regionName.HP: regionName.IOHCT,
                regionName.CC: regionName.IOHWL,
                regionName.CK: regionName.IOHQM,
            }
            world.single_silo = overworld_lookup[list(world.randomize_order.keys())[0]]

    elif not (world.options.randomize_worlds.value == 1 and world.options.randomize_bk_moves.value == 2) and world.options.open_silos.value == 1:
        # No requirement for a specific silo, and the player wants one, so we pick one at random.
        world.single_silo = random.choice([regionName.IOHPL, regionName.IOHPG, regionName.IOHCT, regionName.IOHQM])

    else:
        raise ValueError("What are your settings? g0goTBC did not think of such a combination when randomizing the loading zones!")

def handle_early_moves(world: BanjoTooieWorld) -> None:
    first_level = list(world.randomize_worlds.keys())[0]
    actual_first_level = world.loading_zones[first_level]

    # A silo to the first world is not guaranteed.
    if world.options.randomize_bk_moves != 2 and world.single_silo != "ALL":
        if  first_level != regionName.MT and world.options.logic_type != 2:
            world.multiworld.early_items[world.player][itemName.GGRAB] = 1
        if  first_level == regionName.WW:
            early_fire_eggs(world)
        if  first_level == regionName.JR or first_level == regionName.HP:
            world.multiworld.early_items[world.player][itemName.SPLITUP] = 1
        if first_level == regionName.TL or first_level == regionName.CC:
            early_fire_eggs(world)
            early_torpedo(world)
        if first_level == regionName.CK: # CK can't be first if progressive shoes.
            world.multiworld.early_items[world.player][itemName.CLAWBTS] = 1

    if world.options.randomize_bk_moves == 2: # Guaranteed silo to first level, but getting enough stuff in levels is still hard sometimes.
        # MT, GGM, WW Easy

        if actual_first_level == regionName.JR and world.options.randomize_doubloons.value == False:
            move_lst = [itemName.TJUMP, itemName.FFLIP, itemName.TTROT]
            move = random.choice(move_lst)
            world.multiworld.early_items[world.player][move] = 1

        # TDL Easy

        if first_level == regionName.GIO and world.options.randomize_world_loading_zone.value == False: # Moves to enter the train.
            world.multiworld.early_items[world.player][itemName.CHUFFY] = 1
            world.multiworld.early_items[world.player][itemName.TRAINSWGI] = 1
            world.multiworld.early_items[world.player][itemName.CLIMB] = 1
            world.multiworld.early_items[world.player][itemName.TRAINSWIH] = 1
            world.multiworld.early_items[world.player][random.choice([itemName.FFLIP, itemName.TTROT, itemName.TJUMP])] = 1

        if actual_first_level == regionName.HP:
            move_lst = [itemName.TJUMP, itemName.FFLIP, itemName.TTROT]
            move = random.choice(move_lst)
            world.multiworld.early_items[world.player][move] = 1

        if actual_first_level == regionName.CC:
            move_lst = [itemName.SPLITUP, itemName.FPAD]
            move = random.choice(move_lst)
            world.multiworld.early_items[world.player][move] = 1

def early_fire_eggs(world: BanjoTooieWorld) -> None:
    world.multiworld.early_items[world.player][itemName.PBEGGS if world.options.egg_behaviour.value == 2 else itemName.FEGGS] = 1
    if world.options.randomize_bk_moves != 0:
        world.multiworld.early_items[world.player][random.choice([itemName.EGGAIM, itemName.EGGSHOOT])] = 1

def early_torpedo(world: BanjoTooieWorld) -> None:
    if world.options.randomize_bk_moves != 0:
        world.multiworld.early_items[world.player][itemName.DIVE] = 1
    world.multiworld.early_items[world.player][itemName.TTORP] = 1