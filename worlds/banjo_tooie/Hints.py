from .Items import moves_table, bk_moves_table, progressive_ability_table

def generate_hints(world):
    return generate_move_hints(world)

def generate_move_hints(world):
    move_locations = get_move_locations(world)
    selected_locations = world.random.choices(move_locations, k = 62)

    hints = []
    for l in selected_locations:
        hints.append("{}'s {} has {}".format(world.player_name[l.player], l.name, l.item.name))
    return hints

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

def get_all_locations(world):
    return world.multiworld.get_locations()