from BaseClasses import Location
from . import data
from .ids import location_name_to_id

name_to_id = {name:value for name, value in location_name_to_id.items() if value > 0}
groups = {name:items for name, items in data.location_groups.items() if not name.startswith("_")}

class BanjoTooieLocation(Location):
	pass
