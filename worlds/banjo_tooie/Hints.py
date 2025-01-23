import typing
from BaseClasses import ItemClassification, Location
from worlds.AutoWorld import World
from worlds.banjo_tooie.Options import HintClarity
from .Items import moves_table, bk_moves_table, progressive_ability_table
from .Locations import all_location_table
from .Names import locationName

TOTAL_HINTS = 61

class HintData(typing.NamedTuple):
    text: str # The displayed text in the game.
    location_id: int
    location_player_id: int

def generate_hints(world: World):
    hintDatas = []

    generate_move_hints(world, hintDatas)
    generate_slow_locations_hints(world, hintDatas)

    world.random.shuffle(hintDatas)
    
    hint_location_ids = get_signpost_location_ids()
    for i in range(TOTAL_HINTS):
        world.hints.update({hint_location_ids[i]: hintDatas[i]})

def generate_slow_locations_hints(world: World, hint_datas: typing.List[HintData]):
    hinted_location_names_in_own_world = [location_id_to_name(world, hint_data.location_id)\
                                        for hint_data in hint_datas if hint_data.location_player_id == world.player]

    worst_locations_names = [location_name for location_name in get_worst_location_names(world)\
                             if location_name not in hinted_location_names_in_own_world]

    hinted_location_names_in_own_world.extend(worst_locations_names)

    newHints = [generate_hint_from_location(world, get_location_by_name(world, location_name)) for location_name in worst_locations_names]

    if len(newHints) + len(hint_datas) >= TOTAL_HINTS:
        world.random.shuffle(newHints)
        while len(hint_datas) < TOTAL_HINTS:
            hint_datas.append(newHints.pop())
        return
    hint_datas.extend(newHints)

    bad_locations_names = [location_name for location_name in get_bad_location_names(world) if location_name not in hinted_location_names_in_own_world]
    hinted_location_names_in_own_world.extend(bad_locations_names)
    newHints = [generate_hint_from_location(world, get_location_by_name(world, location_name)) for location_name in bad_locations_names]
    if len(newHints) + len(hint_datas) >= TOTAL_HINTS:
        world.random.shuffle(newHints)
        while len(hint_datas) < TOTAL_HINTS:
            hint_datas.append(newHints.pop())
        return
    hint_datas.extend(newHints)

    # At this point, we went through all the bad locations, and we still don't have enough hints.
    # So we just hint random locations in our own world that have not been picked.
    remaining_locations = [location for location in get_player_locations(world) if location.name not in hinted_location_names_in_own_world]
    world.random.shuffle(remaining_locations)

    while len(hint_datas) < TOTAL_HINTS:
        hint_datas.append(generate_hint_from_location(world, remaining_locations.pop()))

def location_id_to_name(world: World, location_id: int):
    return world.location_id_to_name[location_id]

def get_location_by_id(world: World, location_id: int):
    return list(filter(lambda location: location.address == location_id, get_player_locations(world)))[0]

def get_worst_location_names(world: World):
    slow_location_names = []

    slow_location_names.extend([
        locationName.JIGGYMT5,

        locationName.JIGGYGM5,

        locationName.JIGGYWW2,
        locationName.JIGGYWW3,
        locationName.JIGGYWW4,
        locationName.JIGGYWW7,

        locationName.JIGGYJR7,
        locationName.JIGGYJR9,

        locationName.JIGGYTD3,
        locationName.JIGGYTD7,

        locationName.JIGGYGI1,
        locationName.JIGGYGI2,
        locationName.JIGGYGI3,
        locationName.JIGGYGI4,

        locationName.JIGGYHP1,
        locationName.JIGGYHP5,
        locationName.JIGGYHP9,

        locationName.JIGGYCC1,
        locationName.JIGGYCC7,

        locationName.SCRAT,
    ])

    if world.options.randomize_jinjos.value == 1:
        slow_location_names.extend([
            locationName.JIGGYIH6,
            locationName.JIGGYIH7,
            locationName.JIGGYIH8,
            locationName.JIGGYIH9,

            locationName.JINJOGI3,
            locationName.JINJOGI5,
        ])
    
    if world.options.randomize_glowbos.value == 1:
        slow_location_names.extend([
            locationName.GLOWBOMEG,
        ])

    if world.options.randomize_cheato.value == 1:
        slow_location_names.extend([
            locationName.CHEATOWW3,
            locationName.CHEATOJR1,
            locationName.CHEATOGI3,
            locationName.CHEATOCC1,
        ])
    
    # The 5 most expensive silos
    if world.options.randomize_moves != 0:
        sorted_silos = [k for k, v in sorted(world.jamjars_siloname_costs.items(), key=lambda item: item[1])]
        for i in range(5):
            slow_location_names.append(sorted_silos.pop())
    
    if world.options.cheato_rewards.value == 1:
        slow_location_names.extend([
            locationName.CHEATOR4,
            locationName.CHEATOR5,
        ])
    
    if world.options.honeyb_rewards.value == 1:
        slow_location_names.extend([
            locationName.HONEYBR5,
        ])

    return slow_location_names


def get_bad_location_names(world: World):
    slow_location_names = []

    slow_location_names.extend([
        locationName.JIGGYMT1,
        locationName.JIGGYMT3,

        locationName.JIGGYGM5,

        locationName.JIGGYWW1,
        locationName.JIGGYWW5,

        locationName.JIGGYJR1,
        locationName.JIGGYJR3,

        locationName.JIGGYTD2,
        locationName.JIGGYTD9,

        locationName.JIGGYGI6,
        locationName.JIGGYGI9,

        locationName.JIGGYHP3,
        locationName.JIGGYHP6,
        locationName.JIGGYHP10,

        locationName.JIGGYCC4,

        locationName.SCRUT,
    ])
    # TODO: continue here
    if world.options.randomize_jinjos.value == 1:
        slow_location_names.extend([
        ])
    
    if world.options.randomize_glowbos.value == 1:
        slow_location_names.extend([
        ])

    if world.options.randomize_cheato.value == 1:
        slow_location_names.extend([
        ])
    
    # The 10 most expensive silos
    if world.options.randomize_moves != 0:
        sorted_silos = [k for k, v in sorted(world.jamjars_siloname_costs.items(), key=lambda item: item[1])]
        for i in range(10):
            slow_location_names.append(sorted_silos.pop())
    
    if world.options.cheato_rewards.value == 1:
        slow_location_names.extend([
            locationName.CHEATOR3,
        ])
    
    if world.options.honeyb_rewards.value == 1:
        slow_location_names.extend([
            locationName.HONEYBR4,
        ])
    return slow_location_names

def generate_move_hints(world: World, hint_datas: typing.List[HintData]):
    move_locations = get_move_locations(world)
    for location in move_locations:
        hint_datas.append(generate_hint_from_location(world, location))

# TODO: have some fun with Grunty's rhymes here
def generate_hint_from_location(world: World, location: Location):
    text = ""
    if world.options.hint_clarity == HintClarity.option_clear:
        text = "{}'s {} has {}'s {}.".format(player_id_to_name(world, location.player),\
            location.name, player_id_to_name(world, location.item.player), location.item.name)
    else:
        text = generate_cryptic_hint_text(world, location)
    
    return HintData(text, location.address, location.player)

def generate_cryptic_hint_text(world: World, location: Location):
    if location.item.classification in [ItemClassification.progression, ItemClassification.progression_skip_balancing]:
        return "{}'s {} has a wonderful item.".format(player_id_to_name(world, location.player), location.name)
    if location.item.classification == ItemClassification.useful:
        return "{}'s {} has a good item.".format(player_id_to_name(world, location.player), location.name)
    if location.item.classification == ItemClassification.filler:
        return "{}'s {} has an okay item.".format(player_id_to_name(world, location.player), location.name)
    if location.item.classification == ItemClassification.trap:
        return "{}'s {} has a bad item.".format(player_id_to_name(world, location.player), location.name)

    # Not sure what actually fits in a multi-flag classification
    return "{}'s {} has a devilishly good item.".format(player_id_to_name(world, location.player), location.name)

def get_move_locations(world: World):
    all_moves_names = []
    if world.options.randomize_moves:
        all_moves_names.extend(moves_table.keys()) # We don't want BT moves to be hinted when they're in the vanilla location.
    all_moves_names.extend(bk_moves_table.keys())
    all_moves_names.extend(progressive_ability_table.keys())

    # The locations needs to have an id so that we can reveal them during gameplay in the Archipelago hint list.
    all_move_locations = [location for location in get_all_locations(world)\
            if location.item.name in all_moves_names and location.item.player == world.player and location.address]
    world.random.shuffle(all_move_locations)
    selected_move_locations = []

    for location in all_move_locations:
        if len(selected_move_locations) >= world.options.signpost_hint_distribution.value:
            return selected_move_locations
        selected_move_locations.append(location)
    return selected_move_locations

def get_location_by_name(world: World, name: str):
    return list(filter(lambda location: location.name == name, get_player_locations(world)))[0]

def get_all_locations(world: World):
    return world.multiworld.get_locations()

def get_player_locations(world: World):
    return world.multiworld.get_locations(world.player)

def player_id_to_name(world: World, id: int):
    return world.multiworld.player_name[id]

def get_signpost_location_ids():
    location_datas = list(filter(lambda location_data: location_data.group == "Signpost", all_location_table.values()))
    return [location_data.btid for location_data in location_datas]