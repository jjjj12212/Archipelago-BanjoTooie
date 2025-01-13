from .Items import moves_table, bk_moves_table, progressive_ability_table
from .Names import locationName

TOTAL_HINTS = 62

# TODO: will be converted to go mode items
def generate_hints(world):
    generate_move_hints(world)
    generate_slow_locations_hints(world)
    world.random.shuffle(world.hints)

def generate_slow_locations_hints(world):
    worst_locations_names = [location_name for location_name in get_worst_location_names(world) if location_name not in world.hinted_location_names]
    world.hinted_location_names.extend(worst_locations_names)
    newHints = [generate_hint_from_location(world, get_location_by_name(world, location_name)) for location_name in worst_locations_names]

    if len(newHints) + len(world.hints) >= TOTAL_HINTS:
        world.random.shuffle(newHints)
        while len(world.hints) < TOTAL_HINTS:
            world.hints.append(newHints.pop())
        return
    world.hints.extend(newHints)

    bad_locations_names = [location_name for location_name in get_worst_location_names(world) if location_name not in world.hinted_location_names]
    world.hinted_location_names.extend(bad_locations_names)
    newHints = [generate_hint_from_location(world, get_location_by_name(world, location_name)) for location_name in bad_locations_names]
    if len(newHints) + len(world.hints) >= TOTAL_HINTS:
        world.random.shuffle(newHints)
        while len(world.hints) < TOTAL_HINTS:
            world.hints.append(newHints.pop())
        return
    world.hints.extend(newHints)

    # At this point, we went through all the bad locations, and we still don't have enough hints.
    # So we just hint random locations that have not been picked.
    remaining_locations = [location for location in get_player_locations(world) if location.name not in world.hinted_location_names]
    world.random.shuffle(remaining_locations)

    while len(world.hints) < TOTAL_HINTS:
        world.hints.append(generate_hint_from_location(world, remaining_locations.pop()))


def get_worst_location_names(world):
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


def get_bad_location_names(world):
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

def generate_move_hints(world):
    move_locations = get_move_locations(world)
    hinted_location_names = []
    for location in move_locations:
        world.hints.append(generate_hint_from_location(world, location))
        if location.player == world.player:
            world.hinted_location_names.append(location.name)
    return hinted_location_names


# TODO: have some fun with Grunty's rhymes here
def generate_hint_from_location(world, location):
    return "{}'s {} has {}'s {}.".format(player_id_to_name(world, location.player), location.name, player_id_to_name(world, location.item.player), location.item.name)

def get_move_locations(world):
    all_moves_names = []
    all_moves_names.extend(moves_table.keys())
    all_moves_names.extend(bk_moves_table.keys())
    all_moves_names.extend(progressive_ability_table.keys())

    locations = []
    for location in get_all_locations(world):
        if location.item.name in all_moves_names and location.item.player == world.player:
            locations.append(location)
    return locations

def get_location_by_name(world, name):
    return list(filter(lambda location: location.name == name, get_player_locations(world)))[0]

def get_all_locations(world):
    return world.multiworld.get_locations()

def get_player_locations(world):
    return world.multiworld.get_locations(world.player)

def player_id_to_name(world, id):
    return world.multiworld.player_name[id]