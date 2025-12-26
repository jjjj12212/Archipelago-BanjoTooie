from dataclasses import dataclass
from BaseClasses import CollectionState, Entrance, Region
from typing import TYPE_CHECKING, Callable, Optional
from . import data

if TYPE_CHECKING:
	from . import BanjoTooieWorld

@dataclass
class BanjoTooieBaseExitData:
	on_map: int
	og_map: int
	og_exit: int

@dataclass
class BanjoTooieExitData(BanjoTooieBaseExitData):
	from_exit: int

@dataclass
class BanjoTooieExitMap(BanjoTooieBaseExitData):
	to_map: int
	to_exit: int

class BanjoTooieEntrance(Entrance):
	exit_links: dict[data.Form, "BanjoTooieEntrance"]
	exit_data: BanjoTooieExitData

	def super_connect(self, region: Region) -> None:
		super().connect(region)

	def connect(self, region: Region) -> None:
		if region.multiworld and hasattr(self, "exit_links"):
			to_region = data.regions[data.form_to_region_name[region.name]]
			for form, entrance in self.exit_links.items():
				if self is entrance: continue
				if entrance.connected_region:
					entrance.connected_region.entrances.remove(entrance)
					entrance.connected_region = None
				entrance.super_connect(region.multiworld.get_region(to_region["names"][form], region.player))
		self.super_connect(region)

class BanjoTooieRegion(Region):
	entrance_type = BanjoTooieEntrance

	def connect(
		self,
		connecting_region: Region,
		name: Optional[str] = None,
		rule: Optional[Callable[[CollectionState], bool]] = None
	) -> BanjoTooieEntrance:
		exit_ = self.create_exit(name if name else f"{self.name} -> {connecting_region.name}")
		if rule:
			exit_.access_rule = rule
		exit_.super_connect(connecting_region)
		return exit_

	def create_exit(self, name: str) -> BanjoTooieEntrance:
		exit_ = BanjoTooieEntrance(self.player, name, self)
		self.exits.append(exit_)
		return exit_

class BanjoTooieRegions(dict[str, BanjoTooieRegion]):
	world: "BanjoTooieWorld"

	def __init__(self, world: "BanjoTooieWorld"):
		self.world = world

	def __missing__(self, region_name: str):
		region = BanjoTooieRegion(region_name, self.world.player, self.world.multiworld)
		self[region_name] = region
		return region
