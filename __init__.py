import math, Options, entrance_rando, settings
import worlds.LauncherComponents as LauncherComponents
from itertools import chain
from collections import Counter
from typing import TYPE_CHECKING, Any, Iterable, TextIO, cast, get_type_hints
from worlds.AutoWorld import World, WebWorld
from BaseClasses import CollectionState, EntranceType, MultiWorld, Tutorial, ItemClassification, Item, Location, Region

from . import options, locations, items, data
from .options import BanjoTooieOptions, BanjoTooieOptionsList
from .regions import BanjoTooieEntrance, BanjoTooieRegion, BanjoTooieRegions
from .locations import BanjoTooieLocation
from .items import BanjoTooieItem, BanjoTooieItemInfo
from .rules import BanjoTooieRules
from .ids import slot_data_names, option_name_to_id, exit_name_to_id

if TYPE_CHECKING:
	from .rules import BanjoTooieState

def launch_client():
	from . import client
	LauncherComponents.launch_subprocess(client.run, name="Banjo-Tooie Client") # type: ignore

LauncherComponents.components.append(
	LauncherComponents.Component(
		"Banjo-Tooie Client",
		"BTClient",
		func=launch_client
	)
)

class BanjoTooieSettings(settings.Group):

	class RomPath(settings.OptionalUserFilePath):
		"""File path of the Banjo-Tooie (USA) ROM."""

	class PatchPath(settings.OptionalUserFolderPath):
		"""Folder path of where to save the patched ROM."""

	class ProgramPath(settings.OptionalUserFilePath):
		"""
			File path of the program to automatically run.
			Leave blank to disable.
		"""

	class ProgramArgs(str):
		"""
			Arguments to pass to the automatically run program.
			Leave blank to disable.
			Set to "--lua=" to automatically use the correct path for the lua connector.
		"""

	class EnableTracker(settings.Bool):
		"""
			Whether to enable the built in logic Tracker.
			If enabled, the 'Tracker' tab will show all unchecked locations in logic.
		"""

	rom_path: RomPath | str = ""
	patch_path: PatchPath | str = ""
	program_path: ProgramPath | str = ""
	program_args: ProgramArgs | str = "--lua="
	enable_tracker: EnableTracker | bool = True

class BanjoTooieWebWorld(WebWorld):
	rich_text_options_doc = True
	tutorials = [
		Tutorial(
			"Setup Banjo-Tooie",
			"A guide to setting up Archipelago Banjo-Tooie on your computer.",
			"English",
			"setup_en.md",
			"setup/en",
			["Beebaleen"]
		),
		Tutorial(
			"Setup Banjo-Tooie",
			"A guide to setting up Archipelago Banjo-Tooie on your computer.",
			"French",
			"setup_fr.md",
			"setup/fr",
			["g0goTBC"]
		),
	]
	option_groups = options.groups

class BanjoTooieWorld(World):
	"""
		Banjo-Tooie is a single-player platform game in which the protagonists are controlled from a third-person perspective.
		Carrying over most of the mechanics and concepts established in its predecessor,
		the game features three-dimensional worlds consisting of various platforming challenges and puzzles, with a notable
		increased focus on puzzle-solving over the worlds of Banjo-Kazooie.
	"""
	game = "Banjo-Tooie"
	options_dataclass = BanjoTooieOptions
	options: BanjoTooieOptions # type: ignore
	settings: BanjoTooieSettings # type: ignore
	settings_key = "banjo_tooie_options"
	item_name_to_id = items.name_to_id
	location_name_to_id = locations.name_to_id
	item_name_groups = items.groups
	location_name_groups = locations.groups
	topology_present = True
	web = BanjoTooieWebWorld()

	parser: BanjoTooieRules
	item_info: dict[str, BanjoTooieItemInfo]
	item_pools: dict[str|int, list[BanjoTooieItem]]
	starting_worlds: list[str]
	region_links: dict[str, dict[data.Form, BanjoTooieRegion]]
	entrance_groups: dict[str, list[BanjoTooieEntrance]]
	exit_map: dict[int, int]
	spoiler_info: dict[str, list[str]]
	slot_data: dict[str, Any]
	is_fake_gen: bool
	ut_can_gen_without_yaml = True
	found_entrances_datastorage_key = "UsedEntrances"

	@classmethod
	def version_as_u32(cls) -> int:
		return (cls.world_version.major << 16) | (cls.world_version.minor << 8) | cls.world_version.build

	@classmethod
	def verify_version(cls, version: int | None):
		assert cls.version_as_u32() == version, (
			"Version Mismatch",
			"The client version does not match the generated version."
		)

	@staticmethod
	def fix_slot_data(slot_data: dict[str, Any]):
		slot_data["options"] = {int(key):value for key, value in slot_data["options"].items()}
		slot_data["exit_map"] = {int(key):value for key, value in slot_data["exit_map"].items()}

	def __init__(self, multiworld: "MultiWorld", player: int):
		super().__init__(multiworld, player)
		self.item_info = {}
		self.item_pools = {
			ItemClassification.progression: [],
			ItemClassification.progression_skip_balancing: [],
			ItemClassification.useful: [],
			ItemClassification.trap: [],
			ItemClassification.filler: [],
			"Jiggy": [],
			"Note Nest": [],
			"Nothing": [],
			"Extra Items": [],
			"Starting Inventory From Pool": [],
		}
		self.region_links = {}
		self.entrance_groups = {}
		self.exit_map = {}
		self.spoiler_info = {}

	def log_format(self, msg: str) -> str:
		return f"{self.game} player {self.player} ({self.player_name}): {msg}"

	def check_options(self) -> None:
		match self.options.preset_victory_goals.current_key:
			case "minigame_hunt":
				self.options.victory_goals.value |= {
					"MT Kickball",
					"Ordnance Storage",
					"Hoop Hurry",
					"Dodgem Dome",
					"Saucer of Peril",
					"Balloon Burst",
					"Mini-Sub Challenge",
					"Chompas Belly",
					"Clinker's Cavern",
					"Twinkly Packing",
					"HFP Kickball",
					"Pot O' Gold",
					"Zubbas",
				}
			case "boss_hunt":
				self.options.victory_goals.value |= {
					"Targitzan",
					"Old King Coal",
					"Mr. Patch",
					"Lord Woo Fak Fak",
					"Terry",
					"Weldar",
					"Chilly Willy",
					"Chilli Billi",
					"Mingy Jongo",
				}
			case "jinjo_family_rescue":
				self.options.victory_goals.value |= {
					"White Jinjo Family",
					"Orange Jinjo Family",
					"Yellow Jinjo Family",
					"Brown Jinjo Family",
					"Green Jinjo Family",
					"Red Jinjo Family",
					"Blue Jinjo Family",
					"Purple Jinjo Family",
					"Black Jinjo Family",
				}
			case "wonderwing_challenge": self.options.victory_goals.value = set(options.VictoryGoals.valid_keys)
			case "boss_hunt_and_hag1":
				self.options.victory_goals.value |= {
					"HAG-1",
					"Targitzan",
					"Old King Coal",
					"Mr. Patch",
					"Lord Woo Fak Fak",
					"Terry",
					"Weldar",
					"Chilly Willy",
					"Chilli Billi",
					"Mingy Jongo",
				}
			case "hag1":
				self.options.victory_goals.value |= {"HAG-1"}
			case _: pass
		if self.options.extra_mumbo_tokens.value == 0 and len(self.options.victory_goals.value) == 0:
			self.options.victory_goals.value = {"HAG-1"}
		max_mumbo_tokens = self.options.extra_mumbo_tokens.value + len(self.options.victory_goals.value - {"HAG-1"})
		if self.options.max_mumbo_tokens.value == 0 or self.options.max_mumbo_tokens.value > max_mumbo_tokens:
			self.options.max_mumbo_tokens.value = max_mumbo_tokens
		if self.options.replace_excess_mumbo_tokens.value:
			chosen_goals: set[str] = set()
			selected_goals = list(self.options.victory_goals.value - {"HAG-1"})
			self.random.shuffle(selected_goals)
			extra_mumbo_tokens = self.options.extra_mumbo_tokens.value
			for i in range(self.options.max_mumbo_tokens.value):
				if extra_mumbo_tokens: extra_mumbo_tokens -= 1
				else: chosen_goals.add(selected_goals.pop())
			self.options.extra_mumbo_tokens.value -= extra_mumbo_tokens
			if "HAG-1" in self.options.victory_goals.value: chosen_goals.add("HAG-1")
			self.options.chosen_goals.value = chosen_goals
		else: self.options.chosen_goals.value = self.options.victory_goals.value
		for preset_tricks, tricks in data.tricks.items():
			if preset_tricks in self.options.preset_logic_tricks.value:
				self.options.logic_tricks.value |= set(tricks)
		if self.options.jiggywiggys_challenges not in ["vanilla", "auto"]:
			self.options.shuffle_world_order.value = False
		if self.options.progressive_eggs.value:
			self.options.starting_eggs.value = {"Blue Eggs"}
		if not self.options.shuffle_bk_moves.value:
			self.options.progressive_beak_buster.value = False
			self.options.progressive_bash_attack.value = False
			self.options.progressive_aiming_list.value -= {"Third Person Egg Shooting"}
			self.options.progressive_flight_list.value -= {"Flight Pad", "Beak Bomb"}
			self.options.progressive_water_training_list.value -= {"Dive"}
			self.options.progressive_shoes_list.value -= {"Stilt Stride", "Turbo Trainers"}
		if not self.options.shuffle_bt_moves.value:
			self.options.progressive_eggs.value = False
			self.options.progressive_beak_buster.value = False
			self.options.progressive_aiming_list.value -= {"Amaze-O-Gaze", "Egg Aim", "Breegull Blaster"}
			self.options.progressive_flight_list.value -= {"Airborne Egg Aim"}
			self.options.progressive_water_training_list.value -= {
				"Sub Aqua Aiming",
				"Talon Torpedo",
				"Double Air",
				"Fast Swimming"
			}
			self.options.progressive_shoes_list.value -= {"Springy Step Shoes", "Claw Clamber Boots"}
			self.options.starting_eggs.value = {"Blue Eggs"}
			self.options.move_silo_costs.value = options.MoveSiloCosts.option_vanilla
		if not self.options.shuffle_note_nests.value:
			self.options.replace_excess_note_nests.value = False
		if not self.options.shuffle_stop_n_swop.value:
			self.options.progressive_bash_attack.value = False
		if len(self.options.progressive_aiming_list.value) < 2: self.options.progressive_aiming.value = False
		if len(self.options.progressive_flight_list.value) < 2: self.options.progressive_flight.value = False
		if len(self.options.progressive_water_training_list.value) < 2:
			self.options.progressive_water_training.value = False
		if len(self.options.progressive_shoes_list.value) < 2: self.options.progressive_shoes.value = False
		jiggywiggys_challenge_costs: list[int] = []
		jiggywiggys_challenge_costs_max = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 90]
		match self.options.preset_jiggywiggys_challenge_costs.current_key:
			case "cheap": jiggywiggys_challenge_costs = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66]
			case "expensive": jiggywiggys_challenge_costs = [1, 8, 16, 25, 34, 43, 52, 61, 70, 80, 90]
			case "custom": jiggywiggys_challenge_costs = list(self.options.jiggywiggys_challenge_costs.value.values())
			case "randomize":
				for limit in jiggywiggys_challenge_costs_max:
					jiggywiggys_challenge_costs.append(self.random.randint(1, limit))
			case _: # "default"
				jiggywiggys_challenge_costs = [1, 4, 8, 14, 20, 28, 36, 45, 55, 70, 70]
		self.options.jiggywiggys_challenge_costs.value = {}
		for i, value in enumerate(sorted(jiggywiggys_challenge_costs)):
			self.options.jiggywiggys_challenge_costs.value[f"Challenge {i+1}"] = min(value, jiggywiggys_challenge_costs_max[i])
		if not self.options.starting_eggs.value: self.options.starting_eggs.value = {"Blue Eggs"}
		match self.random.choice(list(self.options.starting_eggs.value)):
			case "Fire Eggs": self.options.chosen_eggs.value = options.ChosenEggs.option_fire_eggs
			case "Grenade Eggs": self.options.chosen_eggs.value = options.ChosenEggs.option_grenade_eggs
			case "Ice Eggs": self.options.chosen_eggs.value = options.ChosenEggs.option_ice_eggs
			case "Clockwork Kazooie Eggs": self.options.chosen_eggs.value = options.ChosenEggs.option_clockwork_kazooie_eggs
			case _: self.options.chosen_eggs.value = options.ChosenEggs.option_blue_eggs
		self.options.chosen_move_silo_costs.value = options.ChosenMoveSiloCosts.default.copy()
		if "ALL" in self.options.dialog_character.value:
			self.options.dialog_character.value = set(options.DialogCharacter.valid_keys)
		self.options.chosen_groggy_location.value = self.random.choice(list(options.ChosenGroggyLocation.options.values()))
		self.options.chosen_soggy_location.value = self.random.choice(list(options.ChosenSoggyLocation.options.values()))
		self.options.chosen_moggy_location.value = self.random.choice(list(options.ChosenMoggyLocation.options.values()))

	def create_item(self, name: str) -> BanjoTooieItem:
		if name in self.item_info: classification = self.item_info[name].classification
		else: classification = ItemClassification.progression
		return BanjoTooieItem(name, classification, items.name_to_id.get(name, None), self.player)

	def interpret_slot_data(self, slot_data: dict[str, Any]):
		return slot_data

	def set_options(self):
		self.verify_version(self.slot_data.get("version"))
		self.fix_slot_data(self.slot_data)
		slot_options = self.slot_data["options"]
		for key, cls in get_type_hints(BanjoTooieOptionsList).items():
			value: Any
			if issubclass(cls, Options.OptionSet):
				value = cast(set[Any], set())
				for sub_key in cast(Iterable[str], cls.valid_keys): # pyright: ignore[reportUnknownMemberType]
					if slot_options[option_name_to_id[data.option_name(f"{key} {sub_key}")]]:
						value.add(sub_key)
			elif issubclass(cls, Options.OptionCounter):
				value = {}
				for sub_key in cast(Iterable[str], cls.valid_keys): # pyright: ignore[reportUnknownMemberType]
					value[sub_key] = slot_options[option_name_to_id[data.option_name(f"{key} {sub_key}")]]
			else:
				assert key in option_name_to_id, ("Unrecognized Option Type", f"Report this to the devs: {key}")
				value = slot_options[option_name_to_id[key]]
			getattr(self.options, key).value = value
		for key, value in self.slot_data["extra_options"].items():
			opt = getattr(self.options, key, None)
			if opt is not None: setattr(self.options, key, opt.from_any(value))

	def generate_early(self) -> None:
		self.is_fake_gen = getattr(self.multiworld, "generation_is_fake", False)
		re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
		if re_gen_passthrough and self.game in re_gen_passthrough:
			self.slot_data = re_gen_passthrough[self.game]
			self.set_options()
		else: self.check_options()
		self.parser = BanjoTooieRules(self)
		self.rhythmic_swimming = self.parser.parse(data.ast_tricks["Rhythmic Swimming"])
		for item_name, (logic, classes) in data.ast_items.items():
			shuffled = self.parser.parse(logic)(None)
			for cls, logic in classes.items():
				if self.parser.parse(logic)(None): break
			else: cls = "filler"
			match cls:
				case "progression":
					classification = ItemClassification.progression
				case "progression_skip_balancing":
					classification = ItemClassification.progression_skip_balancing
				case "progression_deprioritized_skip_balancing":
					classification = ItemClassification.progression_deprioritized_skip_balancing
				case "progression_deprioritized":
					classification = ItemClassification.progression_deprioritized
				case "useful":
					classification = ItemClassification.useful
				case "trap":
					classification = ItemClassification.trap
				case "filler":
					classification = ItemClassification.filler
			self.item_info[item_name] = BanjoTooieItemInfo(shuffled, classification)

	def create_regions(self) -> None:
		region_cache = BanjoTooieRegions(self)

		for region_name, region in data.regions.items():
			ap_regions: dict[data.Form, BanjoTooieRegion] = {}
			for form, form_region_name in region.names.items():
				ap_region = region_cache[form_region_name]
				ap_region.region_links = ap_regions
				ap_region.form = form
				ap_region.region_data = region
				ap_region.formless_name = region_name
				ap_regions[form] = ap_region
			self.region_links[region_name] = ap_regions
			for location_name, location in region.locations.items():
				if not self.parser.parse(location.ast_enabled)(None):
					continue
				item_name = location.ast_item
				if item_name:
					for new_item_name, item_logic in item_name.items():
						if self.parser.parse(item_logic)(None):
							item_name = new_item_name
							break
				else: item_name = None
				assert not isinstance(item_name, dict), self.log_format(f"Unable to choose valid item: {location.file}")
				if item_name:
					item_name = data.parser.item_names[item_name]
					if item_name in self.parser.items: item_name = self.parser.items[item_name][0]
				else: item_name = location_name
				item = self.create_item(item_name)
				if item_name in self.item_info:
					if item.code and not self.item_info[item_name].shuffled: item.code = None
				else: item.classification = ItemClassification.progression
				if item.code and self.parser.parse(location.ast_force_event)(None):
					item.code = None
				if not item.code and ItemClassification.progression not in item.classification:
					continue
				form, logic_ast = next(iter(location.ast_logic.items()), ("Any", data.parser.true))
				logic = self.parser.parse(logic_ast)
				if region.major_region == "Menu":
					skip = True
					match region_name:
						case "Menu":
							if location_name == "Completion Condition":
								self.multiworld.completion_condition[self.player] = logic
						case "Starting Inventory":
							if item_name != "Nothing" and logic(None): self.push_precollected(item)
						case "Starting Inventory From Pool":
							if item_name != "Nothing" and logic(None): self.item_pools[region_name].append(item)
						case "Extra Items":
							if item.code and logic(None): self.item_pools[region_name].append(item)
							else: self.push_precollected(item)
						case _: skip = False
					if skip: continue
				ap_location = BanjoTooieLocation(self.player, location_name, None, ap_regions[form])
				if logic != rules.true: ap_location.access_rule = logic
				if item.code:
					ap_location.address = locations.name_to_id[location_name]
					if self.parser.parse(location.ast_locked)(None):
						ap_location.place_locked_item(item)
					else:
						if item_name in ("Nothing", "Jiggy", "Note Nest"): self.item_pools[item_name].append(item)
						else: self.item_pools[item.classification].append(item)
				else:
					ap_location.place_locked_item(item)
				if item.name == "Nothing":
					item.name = "Big-O Pants"
					item.code = items.name_to_id[item.name]
				ap_regions[form].locations.append(ap_location)
			for exit_name, exit_ in region.exits.items():
				exit_region = data.regions[exit_name]
				links: dict[data.Form, BanjoTooieEntrance] = {}
				for from_form, to_forms in exit_.ast_logic.items():
					for to_form, logic_ast in to_forms.items():
						if exit_region.event: form_exit_name = exit_name
						else: form_exit_name = exit_region.names[to_form]
						ap_exit = region_cache[form_exit_name]
						entrance = ap_regions[from_form].connect(ap_exit)
						for indirect_form, indirect_region in exit_.indirect_extras:
							self.multiworld.register_indirect_condition(
								region_cache[data.regions[indirect_region].names[indirect_form]],
								entrance
							)
						for indirect_form in exit_.indirect_starts:
							for indirect_region in data.form_start_regions:
								self.multiworld.register_indirect_condition(
									region_cache[data.regions[indirect_region].names[indirect_form]],
									entrance
								)
						links[to_form] = entrance
						entrance.exit_links = links
						entrance.exit_data = exit_
						logic = self.parser.parse(logic_ast)
						if logic != rules.true: entrance.access_rule = logic
						if exit_.id is None: continue
						if exit_.two_way: entrance.randomization_type = EntranceType.TWO_WAY
						else: entrance.randomization_type = EntranceType.ONE_WAY
						if from_form == to_form and to_form == data.normal_forms[0]:
							for group in exit_.groups:
								self.entrance_groups.setdefault(group, []).append(entrance)
			for ap_region in ap_regions.values():
				self.multiworld.regions.append(ap_region)

	def plan_early_game(self, starting_inventory: list[BanjoTooieItem]):

		state = CollectionState(self.multiworld, True)
		def placeable_locations_count():
			return len(self.multiworld.get_placeable_locations(state, self.player)) # type: ignore

		# Make sure we can access the Warp Silos.
		for item in self.item_name_groups["Warp Silos"]:
			state.add_item(item, self.player)
		state.update_reachable_regions(self.player)
		if not state.can_reach_region("IoH: Warp Silos", self.player):
			# Cycle progression items in an attempt to gain access to Warp Silos.
			current_checks = placeable_locations_count()
			item = None
			for item in self.item_pools[ItemClassification.progression]:
				state.add_item(item.name, self.player)
				state.update_reachable_regions(self.player)
				if state.can_reach_region("IoH: Warp Silos", self.player):
					break
				state.remove(item)
				item = None
			if item:
				# Make sure the item that gave us access to Warp Silos shows up early
				# if we have a free local location for it, otherwise start with it.
				if current_checks >= 1:
						self.multiworld.early_items[self.player].setdefault(item.name, 0)
						self.multiworld.early_items[self.player][item.name] += 1
				else:
					starting_inventory.append(item)
			else:
				# If we couldn't find a single item to give us access, give up.
				raise Exception(self.log_format("Unable to plan early game. This shouldn't happen..."))
		# Assume we have Warp Silos access now.
		self.world_order = [
			"Mayahem Temple",
			"Glitter Gulch Mine",
			"Witchyworld",
			"Jolly Roger's Lagoon",
			"Terrydactyland",
			"Grunty Industries",
			"Hailfire Peaks",
			"Cloud Cuckooland",
			"Cauldron Keep",
		]
		self.starting_worlds = self.world_order[:2]
		if self.options.shuffle_world_order.value or self.options.shuffle_world_entrances.value:
			check_worlds = self.world_order.copy()
			self.random.shuffle(check_worlds)
		else:
			check_worlds = [self.world_order[0]]
			self.starting_worlds = [self.world_order[0]]
		# Find worlds with early checks to be used as the starting worlds.
		found_worlds = 0
		current_checks = placeable_locations_count()
		for world in check_worlds:
			state.add_item(world, self.player)
			state.update_reachable_regions(self.player)
			count = placeable_locations_count()-current_checks
			if count > 0:
				self.starting_worlds[found_worlds] = world
				found_worlds += 1
			state.remove(self.create_item(world))
			if found_worlds == len(self.starting_worlds): break
		if found_worlds < len(self.starting_worlds):
			# Not enough worlds have early checks with these settings... Find an advancement item.
			for world in check_worlds:
				state.add_item(world, self.player)
			state.update_reachable_regions(self.player)
			current_checks = placeable_locations_count()
			item = None
			for item in self.item_pools[ItemClassification.progression]:
				state.add_item(item.name, self.player)
				state.update_reachable_regions(self.player)
				count = placeable_locations_count()-current_checks
				if count > 0:
					current_checks = count
					break
				state.remove(item)
				item = None
			if item:
				# Make sure the item that unlocked more checks shows up early
				# if we have a free local location for it, otherwise start with it.
				if current_checks >= 2:
					self.multiworld.early_items[self.player].setdefault(item.name, 0)
					self.multiworld.early_items[self.player][item.name] += 1
				else:
					starting_inventory.append(item)
			else:
				# If we couldn't find a single item to give us access, give up.
				raise Exception(self.log_format("Unable to plan early game. This shouldn't happen..."))
			for world in check_worlds: state.remove(self.create_item(world))
			for world in check_worlds:
				state.add_item(world, self.player)
				state.update_reachable_regions(self.player)
				count = placeable_locations_count()-current_checks
				if count > 0:
					self.starting_worlds[found_worlds] = world
					found_worlds += 1
				state.remove(self.create_item(world))
				if found_worlds == len(self.starting_worlds): break
		for world in reversed(self.starting_worlds):
			if world:
				check_worlds.remove(world)
				check_worlds.insert(0, world)
		open_warp_silos = self.options.open_warp_silos.value
		warp_silos = [
			"Jinjo Village Warp Silo",
			"Wooded Hollow Warp Silo",
			"Plateau Warp Silo",
			"Pine Grove Warp Silo",
			"Cliff Top Warp Silo",
			"Wasteland Warp Silo",
			"Quagmire Warp Silo",
		]
		self.random.shuffle(warp_silos)
		if self.options.shuffle_world_order.value:
			world_order = check_worlds
			region = data.regions["Jiggywiggy Challenges"]
			worlds = list(reversed(world_order))
			for location_name in region.locations:
				item = self.create_item(worlds.pop())
				ap_location = self.multiworld.get_location(location_name, self.player)
				if ap_location.item:
					ap_location.item.location = None
					ap_location.item = None
				ap_location.place_locked_item(item)
				if len(worlds) == 0: break
			if open_warp_silos >= 1:
				match world_order[0]:
					case "Glitter Gulch Mine": item = self.create_item("Plateau Warp Silo")
					case "Witchyworld": item = self.create_item("Pine Grove Warp Silo")
					case "Jolly Roger's Lagoon": item = self.create_item("Cliff Top Warp Silo")
					case "Terrydactyland": item = self.create_item("Wasteland Warp Silo")
					case "Grunty Industries": item = self.create_item("Quagmire Warp Silo")
					case "Hailfire Peaks": item = self.create_item("Cliff Top Warp Silo")
					case "Cloud Cuckooland": item = self.create_item("Wasteland Warp Silo")
					case "Cauldron Keep": item = self.create_item("Quagmire Warp Silo")
					case _: item = self.create_item("Wooded Hollow Warp Silo")
				open_warp_silos -= 1
				warp_silos.remove(item.name)
				starting_inventory.append(item)
				if open_warp_silos >= 1:
					if world_order[0] == "Mayahem Temple":
						item = self.create_item("Jinjo Village Warp Silo")
					else:
						item = self.create_item(self.random.choice(["Jinjo Village Warp Silo", "Wooded Hollow Warp Silo"]))
					open_warp_silos -= 1
					warp_silos.remove(item.name)
					starting_inventory.append(item)

		for _i in range(open_warp_silos):
			item = self.create_item(warp_silos.pop())
			starting_inventory.append(item)

		match self.options.move_silo_costs.current_key:
			case "randomize":
				for silo in self.options.chosen_move_silo_costs.value:
					self.options.chosen_move_silo_costs.value[silo] = self.random.randint(0, 160)*5
			case "progressive":
				world_moves = {
					"Mayahem Temple": [
						"Egg Aim",
						"Breegull Blaster",
						"Grip Grab",
					],
					"Glitter Gulch Mine": [
						"Bill Drill",
						"Beak Bayonet",
					],
					"Witchyworld": [
						"Split Up",
						"Pack Whack",
						"Airborne Egg Aiming",
					],
					"Jolly Roger's Lagoon": [
						"Wing Whack",
						"Sub Aqua Egg Aiming",
						"Talon Torpedo",
					],
					"Terrydactyland": [
						"Springy Step Shoes",
						"Taxi Pack",
						"Hatch",
					],
					"Grunty Industries": [
						"Claw Clamber Boots",
						"Snooze Pack",
						"Leg Spring",
					],
					"Hailfire Peaks": [
						"Shack Pack",
						"Glide",
					],
					"Cloud Cuckooland": [
						"Sack Pack",
					]
				}
				for moves in world_moves.values():
					self.random.shuffle(moves)
				move_costs = [765, 660, 640, 545, 525, 505, 420, 405, 390, 290, 275, 265, 180, 170, 160, 95, 85, 35, 30, 25]
				for world in self.world_order:
					for silo in world_moves.get(world, []):
						self.options.chosen_move_silo_costs.value[silo] = move_costs.pop()
			case _: pass # "vanilla"

	def create_items(self) -> None:
		filler = ("Nothing", ItemClassification.filler)
		replaceable = filler + (ItemClassification.useful, )
		pools = replaceable + (
			ItemClassification.trap,
			ItemClassification.progression_skip_balancing,
			ItemClassification.progression
		)
		for pool in pools: self.random.shuffle(self.item_pools[pool])
		pools += ("Jiggy", "Note Nest")
		extra_nothing = 0

		starting_inventory = self.item_pools["Starting Inventory From Pool"]
		def starting_inventory_from_pool():
			nonlocal extra_nothing
			if not starting_inventory: return
			self.random.shuffle(starting_inventory)
			for item in starting_inventory:
				self.push_precollected(item)
				replaced = False
				for pool in ("Extra Items",) + pools:
					if item in self.item_pools[pool]:
						replaced = True
						self.item_pools[pool].remove(item)
						break
				if replaced: extra_nothing += 1
			starting_inventory.clear()

		### Starting items ###

		starting_inventory_from_pool()
		self.random.shuffle(self.item_pools["Extra Items"])
		for item in self.item_pools["Extra Items"]:
			replaced = False
			for cls in replaceable:
				if len(self.item_pools[cls]):
					replaced = True
					self.multiworld.itempool.append(item)
					self.item_pools[cls].pop()
					break
			if not replaced: self.push_precollected(item)
		for _i in range(self.options.extra_mumbo_tokens.value):
			item = self.create_item("Mumbo Token")
			replaced = False
			for cls in replaceable:
				if len(self.item_pools[cls]):
					replaced = True
					self.multiworld.itempool.append(item)
					self.item_pools[cls].pop()
					break
			if not replaced: self.push_precollected(item)

		if not self.is_fake_gen: self.plan_early_game(starting_inventory)

		### Item pool manipulation ###

		starting_inventory_from_pool()

		if self.options.replace_excess_jiggies.value:
			if self.options.shuffle_jiggywiggys_super_special_challenge.value:
				needed = self.options.jiggywiggys_challenge_costs.value[f"Challenge 11"]
			elif not self.options.open_hag1.value or self.item_info["HAG-1"].shuffled:
				needed = self.options.jiggywiggys_challenge_costs.value[f"Challenge 10"]
			else:
				needed = self.options.jiggywiggys_challenge_costs.value[f"Challenge 9"]
			pool = self.item_pools["Jiggy"]
			replace: int = math.ceil((len(pool)-needed)/2)
			extra_nothing += replace
			del pool[:replace]

		extra_bass_treble_clefs = ["Bass Clef"]*self.options.extra_bass_clefs.value
		extra_bass_treble_clefs += ["Treble Clef"]*self.options.extra_treble_clefs.value
		if self.options.replace_excess_note_nests.value:
			pool = self.item_pools["Note Nest"]
			needed = max(self.options.chosen_move_silo_costs.value.values())
			needed -= 180 # Vanilla Treble Clefs
			needed = math.ceil(needed/5) # Note Nest items
			if needed > 0: replace = math.ceil((len(pool)-needed))
			else: replace = len(pool)
			extra_nothing += replace
			del pool[-replace:]
			self.random.shuffle(extra_bass_treble_clefs)
			while pool and extra_bass_treble_clefs:
				item = extra_bass_treble_clefs.pop()
				match item:
					case "Bass Clef": remove = 2
					case "Treble Clef": remove = 4
					case _: continue
				extra_nothing += len(pool[-remove:])-1
				del pool[-remove:]
				item = self.create_item(item)
				self.item_pools[item.classification].append(item)

		if extra_nothing: self.item_pools["Nothing"] += [self.create_item("Big-O Pants") for _i in range(extra_nothing)]

		extra_items = {
			ItemClassification.useful:
				extra_bass_treble_clefs
				+["Jiggy"]*self.options.extra_jiggies.value
				+["Note Nest"]*self.options.extra_note_nests.value
				+["Doubloon"]*self.options.extra_doubloons.value
				+["Empty Honeycomb"]*self.options.extra_empty_honeycombs.value
				+["Cheato Page"]*self.options.extra_cheato_pages.value,
			ItemClassification.filler:
				["Egg Nest"]*self.options.extra_egg_nests.value
				+["Feather Nest"]*self.options.extra_feather_nests.value,
			ItemClassification.trap:
				["Trip Trap"]*self.options.trip_traps.value
				+["Slip Trap"]*self.options.slip_traps.value
				+["Tip Trap"]*self.options.tip_traps.value
				+["Transform Trap"]*self.options.transform_traps.value
				+["Golden Egg Nest"]*self.options.golden_egg_nests.value
				+["Squish Trap"]*self.options.squish_traps.value,
		}
		for item_class, item_list in extra_items.items():
			self.random.shuffle(item_list)
			for item_name in item_list:
				item = self.create_item(item_name)
				item.classification = item_class
				replaced = False
				for cls in filler:
					if len(self.item_pools[cls]):
						replaced = True
						self.multiworld.itempool.append(item)
						self.item_pools[cls].pop()
						break
				if not replaced: break

		for pool in pools:
			self.multiworld.itempool += self.item_pools[pool]

		# Remove all regions that are completely inaccessible or useless with these settings.
		state = CollectionState(self.multiworld, True)
		for item in self.multiworld.itempool:
			if item.player == self.player: self.collect(state, item)
		for item in self.get_pre_fill_items(): self.collect(state, item)
		state.sweep_for_advancements()
		inaccessible_regions: list[str] = []
		remove_regions: set[Region] = set()
		remove_entrances: set[BanjoTooieEntrance] = set()
		for region in self.get_regions():
			if not region.can_reach(state) or len(region.locations) == 0 and len(region.exits) == 0:
				if len(region.locations): inaccessible_regions.append(region.name)
				for entrance in cast(Iterable[BanjoTooieEntrance], chain(region.entrances, region.exits)):
					remove_entrances.add(entrance)
				remove_regions.add(region)
		assert len(inaccessible_regions) == 0, self.log_format(
			"The following region(s) are inaccessible, but have location(s):\n" +
			"\n".join(inaccessible_regions)
		)
		ap_regions = self.multiworld.regions.region_cache[self.player]
		ap_entrances = self.multiworld.regions.entrance_cache[self.player]
		for entrance in remove_entrances:
			if entrance.exit_links is not None:
				for form, other_entrance in entrance.exit_links.items():
					if entrance is other_entrance:
						del entrance.exit_links[form]
						break
			del ap_entrances[entrance.name]
		for region in remove_regions:
			del ap_regions[region.name]

	def ap_connect_entrances(self) -> None:
		ids: dict[str, int] = {group:i+1 for i, group in enumerate(self.entrance_groups)}
		lookup: dict[int, list[int]] = {-2:[-1], -1:[-2], 0:[0]}
		shuffled_entrances: list[str] = []
		def add_group(group: str, restricted: bool) -> None: # type: ignore | planned future use
			shuffled_entrances.append(group)
			if restricted: lookup[ids[group]] = [ids[group]]
			else: ids[group] = 0
		def add_parent_child(parent: str, child: str, restricted: bool) -> None:
			shuffled_entrances.extend([parent, child])
			if restricted:
				lookup[ids[parent]] = [ids[child]]
				lookup[ids[child]] = [ids[parent]]
			else:
				ids[parent] = 0
				ids[child] = 0
		if self.options.shuffle_world_entrances.value:
			groups = ("World Entrances", "World Exits")
			add_parent_child(*groups, True)
			if self.options.shuffle_world_order.value:
				starting_worlds = [
					[self.starting_worlds[0], self.starting_worlds[1]],
					[self.starting_worlds[1], self.starting_worlds[0]]
				]
			else:
				starting_worlds = [
					[self.world_order[0], self.world_order[1]],
					[self.starting_worlds[0], self.starting_worlds[1]]
				]
			for i in range(len(groups)):
				for entrance in self.entrance_groups[groups[i]]:
					if (
						entrance.parent_region and entrance.parent_region.name in starting_worlds[i]
						or entrance.connected_region and entrance.connected_region.name in starting_worlds[i]
					):
						entrance.randomization_group = -(i+1)
						entrance_rando.disconnect_entrance_for_randomization(entrance)
		if self.options.shuffle_boss_entrances.value:
			add_parent_child("Boss Entrances", "Boss Exits", True)
		for group in shuffled_entrances:
			for entrance in self.entrance_groups[group]:
				if not entrance.parent_region or not entrance.connected_region: continue
				entrance.randomization_group = ids[group]
				entrance_rando.disconnect_entrance_for_randomization(
					entrance,
					one_way_target_name=f"{entrance.connected_region.name} -> {entrance.parent_region.name}"
				)
		er_state = entrance_rando.randomize_entrances(self, True, lookup)
		spoiler_info: list[str] = []
		for entrance_name, exit_name in er_state.pairings:
			spoiler_info.append(f"{entrance_name:50} = {exit_name.replace(" -> ", " <- ")}")
			to_region, from_region = exit_name.split(" -> ")
			exit_name = f"{from_region} -> {to_region}"
			self.exit_map[exit_name_to_id[entrance_name]] = exit_name_to_id[exit_name]
		self.spoiler_info["Entrances"] = spoiler_info

	def ut_connect_entrances(self):
		self.seen_entrances: set[int] = set()
		exit_map = self.slot_data["exit_map"]
		deferred_enabled = getattr(self.multiworld, "enforce_deferred_connections", "off") != "off"
		self.id_to_vanilla: dict[int, tuple[BanjoTooieEntrance, Region]] = {}
		for name, value in exit_name_to_id.items():
			entrance = cast(BanjoTooieEntrance, self.get_entrance(name))
			assert entrance.connected_region is not None
			self.id_to_vanilla[value] = (entrance, entrance.connected_region)
		for from_id, to_id in exit_map.items():
			exit_ = self.id_to_vanilla[from_id][0]
			entrance, entrance_connected = self.id_to_vanilla[to_id]
			if deferred_enabled and exit_.exit_links is not None:
				for linked_entrance in exit_.exit_links.values():
					if linked_entrance.connected_region:
						linked_entrance.connected_region.entrances.remove(linked_entrance)
						linked_entrance.connected_region = None
			else:
				exit_.connect(entrance_connected)

	def connect_entrances(self):
		if self.is_fake_gen: self.ut_connect_entrances()
		else: self.ap_connect_entrances()

	def reconnect_found_entrances(self, found_key: str, value: Any):
		if found_key != "UsedEntrances" or not isinstance(value, list): return
		exit_map = self.slot_data["exit_map"]
		new_entrances = set(cast(list[int], value)) - self.seen_entrances
		self.seen_entrances |= new_entrances
		for entrance_id in new_entrances:
			exit_ = self.id_to_vanilla[entrance_id][0]
			entrance_connected = self.id_to_vanilla[exit_map[entrance_id]][1]
			exit_.connect(entrance_connected)

	def get_filler_item_name(self) -> str:
		return "Big-O Pants"

	def collect(self, state: CollectionState, item: Item) -> bool:
		mixin: "BanjoTooieState" = state # pyright: ignore[reportAssignmentType]
		mixin.banjo_tooie_air[self.player].clear()
		return super().collect(state, item)

	def remove(self, state: CollectionState, item: Item):
		mixin: "BanjoTooieState" = state # pyright: ignore[reportAssignmentType]
		mixin.banjo_tooie_path_finders[self.player].clear()
		mixin.banjo_tooie_forms_reach[self.player].clear()
		mixin.banjo_tooie_forms_reach_regions[self.player].clear()
		mixin.banjo_tooie_air[self.player].clear()
		return super().remove(state, item)

	def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
		if self.options.chosen_move_silo_costs.value != options.ChosenMoveSiloCosts.default:
			spoiler_handle.write("Move Silo Costs:\n")
			for name, cost in sorted(self.options.chosen_move_silo_costs.value.items(), key=lambda e: e[1]):
				name = f"{name}:"
				spoiler_handle.write(f"  {name:25} {cost}\n")
		if len(self.spoiler_info.get("Entrances", [])):
			spoiler_handle.write("Entrances:\n")
			for line in self.spoiler_info["Entrances"]:
				spoiler_handle.write(f"  {line}\n")

	def fill_slot_data(self) -> dict[str, Any]:
		options: dict[int, int] = {option:0 for option in ids.option_name_to_id.values()}
		def add_option(name: str, value: int) -> None:
			name = data.option_name(name)
			options[ids.option_name_to_id[name]] = value
		for name, value in self.options.as_dict(*slot_data_names).items():
			if isinstance(value, list):
				for element in cast(list[str], value):
					add_option(f"{name} {element}", 1)
				continue
			if isinstance(value, dict):
				for key, val in cast(dict[str, int], value).items():
					add_option(f"{name} {key}", val)
				continue
			if isinstance(value, bool):
				value = 1 if value else 0
			add_option(name, value)
		return {
			"options": options,
			"extra_options": self.options.as_dict("exclude_locations", "priority_locations"),
			"exit_map": self.exit_map,
			"hints": {},
			"version": self.version_as_u32(),
		}

	@classmethod
	def stage_fill_hook(
		cls,
		multiworld: MultiWorld,
		progitempool: list[Item],
		usefulitempool: list[Item],
		filleritempool: list[Item],
		fill_locations: list[Location]
	):
		# If there are a lot of items to fit in few locations, help out the generator by sorting the items into a more
		# easy to fill order. This reduces the chance of the fill algorithm getting stuck and having to swap items.
		# 0.75 is a heuristic threshold; default BT settings is about 82% of the pool being progression.
		if len(progitempool) / len(fill_locations) < 0.75:
			return

		bt_players = {world.player for world in multiworld.get_game_worlds(cls.game)}

		# Count how many copies of each item exist for each BT player.
		# Items with more copies are placed first, which helps AP's fill algorithm.
		item_counts: dict[int, Counter[str]] = {player: Counter() for player in bt_players}
		for item in progitempool:
			if item.player in bt_players:
				item_counts[item.player][item.name] += 1

		def sort_pool(item: Item) -> int:
			if item.player in item_counts:
				return item_counts[item.player][item.name]
			else:
				# If it's not an item belonging to a Banjo-Tooie player, keep its order the same.
				return 0

		progitempool.sort(key=sort_pool)
