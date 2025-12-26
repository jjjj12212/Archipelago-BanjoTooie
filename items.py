from typing import NamedTuple
from BaseClasses import Item, ItemClassification
from . import data
from .ids import item_name_to_id
from .data import item_name

name_to_id: dict[str, int] = {}
names: dict[str, str] = {}
for item, value in item_name_to_id.items():
	if value > 0:
		name_to_id[item] = value
		names[item_name(item)] = item
groups = {
	group:{names[item] for item in items}
	for group, items in data.item_groups.items()
	if not group.startswith("_")
}

class BanjoTooieItem(Item):
	pass

class BanjoTooieItemInfo(NamedTuple):
	shuffled: bool
	classification: ItemClassification
