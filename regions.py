from BaseClasses import CollectionState, Entrance, EntranceType, Region
from typing import TYPE_CHECKING, Callable
from . import data

if TYPE_CHECKING:
	from . import BanjoTooieWorld

class BanjoTooieEntrance(Entrance):
	exit_links: dict[data.Form, "BanjoTooieEntrance"] | None
	exit_data: data.types.FinalExit | None

	def __init__(
		self,
		player: int,
		name: str = "",
		parent: Region | None = None,
		randomization_group: int = 0,
		randomization_type: EntranceType = EntranceType.ONE_WAY,
	) -> None:
		super().__init__(player, name, parent, randomization_group, randomization_type)
		self.exit_links = None
		self.exit_data = None

	def super_connect(self, region: Region) -> None:
		super().connect(region)

	def connect(self, region: Region) -> None:
		if (
			region.multiworld is not None
			and self.exit_links is not None
			and isinstance(region, BanjoTooieRegion)
		):
			for form, entrance in self.exit_links.items():
				if self is entrance: continue
				if entrance.connected_region:
					entrance.connected_region.entrances.remove(entrance)
					entrance.connected_region = None
				entrance.super_connect(region.region_links[form])
		self.super_connect(region)

class BanjoTooieRegion(Region):
	entrance_type = BanjoTooieEntrance
	region_links: dict[data.Form, "BanjoTooieRegion"]
	form: data.Form
	region_data: data.FinalRegion
	formless_name: str

	def connect(
		self,
		connecting_region: Region,
		name: str | None = None,
		rule: Callable[[CollectionState], bool] | None = None
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
