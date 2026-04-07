import ast
from collections import deque
from types import CodeType
from typing import Callable, Any, Counter, Generator, cast, TYPE_CHECKING, get_type_hints

from Options import Choice, OptionDict
from BaseClasses import CollectionState, Region, Entrance, MultiWorld
from worlds.AutoWorld import LogicMixin
from .regions import BanjoTooieEntrance, BanjoTooieRegion
from .options import BanjoTooieOptionsList
from . import data

if TYPE_CHECKING:
	from . import BanjoTooieWorld

Rule = Callable[[CollectionState | None], bool]
true: Rule = lambda _state: True
false: Rule = lambda _state: False

class BanjoTooiePathFinder:

	def __init__(self, state: "BanjoTooieState", dest: Region):
		self.locked = False
		self.state = state
		self.dest = dest
		self.reachable_regions: set[Region] = {dest}
		self.blocked_entrances: set[Entrance] = set(dest.entrances)

	def copy(self, state: "BanjoTooieState"):
		ret = BanjoTooiePathFinder(state, self.dest)
		ret.reachable_regions = self.reachable_regions.copy()
		ret.blocked_entrances = self.blocked_entrances.copy()
		return ret

	def process_queue(self):
		while self.queue:
			entrance = self.queue.popleft()
			if not entrance.access_rule(self.state): continue
			self.blocked_entrances.remove(entrance)
			parent_region = entrance.parent_region
			if (
				parent_region is not None
				and parent_region not in self.reachable_regions
			):
				self.reachable_regions.add(parent_region)
				self.blocked_entrances.update(parent_region.entrances)
				self.queue.extend(parent_region.entrances)
				for new_entrance in self.state.multiworld.indirect_connections.get(parent_region, set()):
					if new_entrance in self.blocked_entrances and new_entrance not in self.queue:
						self.queue.append(new_entrance)
				yield parent_region

	def refresh_queue(self):
		self.queue = deque(self.blocked_entrances)

	def find_all(self, regions: set[Region]):
		for region in regions:
			if region in self.reachable_regions: yield region
		if self.locked: return
		regions -= self.reachable_regions
		if not regions: return
		try:
			self.locked = True
			self.refresh_queue()
			for region in self.process_queue():
				if region in regions:
					yield region
					regions.remove(region)
					if not regions: return
		finally:
			self.locked = False

	def can_reach_all(self, starts: set[Region]) -> bool:
		starts -= self.reachable_regions
		if not starts: return True
		if self.locked: return False
		try:
			self.locked = True
			self.refresh_queue()
			for region in self.process_queue():
				starts.discard(region)
				if not starts: return True
			return False
		finally:
			self.locked = False

	def can_reach_any(self, starts: set[Region]) -> bool:
		if starts & self.reachable_regions: return True
		if self.locked: return False
		try:
			self.locked = True
			self.refresh_queue()
			for region in self.process_queue():
				if region in starts: return True
			return False
		finally:
			self.locked = False

class BanjoTooiePathFinders(dict[Region, BanjoTooiePathFinder]):

	def __init__(self, state: "BanjoTooieState", *args: Any, **kwargs: Any):
		super().__init__(*args, **kwargs)
		self.state = state

	def __missing__(self, start: Region):
		path_finder = BanjoTooiePathFinder(self.state, start)
		self[start] = path_finder
		return path_finder

	def super_copy(self, state: "BanjoTooieState"):
		return BanjoTooiePathFinders(
			state,
			{region: path_finder.copy(state) for region, path_finder in self.items()}
		)

	def copy(self) -> dict[Region, BanjoTooiePathFinder]:
		return self.super_copy(self.state)

class BanjoTooieMixin(LogicMixin):
	banjo_tooie_path_finders: dict[int, BanjoTooiePathFinders]
	banjo_tooie_transform_block: Counter[int]
	banjo_tooie_forms_reach: dict[int, set[tuple[frozenset[data.Form], str]]] = {}
	banjo_tooie_forms_reach_regions: dict[int, set[frozenset[tuple[data.Form, str]]]] = {}
	banjo_tooie_air: dict[int, dict[BanjoTooieRegion, float]]

	def init_mixin(self, multiworld: MultiWorld) -> None:
		players = multiworld.get_game_players("Banjo-Tooie")
		self.banjo_tooie_path_finders = {}
		self.banjo_tooie_transform_block = Counter()
		self.banjo_tooie_forms_reach = {}
		self.banjo_tooie_forms_reach_regions = {}
		self.banjo_tooie_air = {}
		for player in players:
			self.banjo_tooie_path_finders[player] = BanjoTooiePathFinders(self) # pyright: ignore[reportArgumentType]
			self.banjo_tooie_forms_reach[player] = set()
			self.banjo_tooie_forms_reach_regions[player] = set()
			self.banjo_tooie_air[player] = {}

	def copy_mixin(self, new_state: "BanjoTooieMixin"):
		new_state.banjo_tooie_transform_block = self.banjo_tooie_transform_block.copy()
		new_state.banjo_tooie_path_finders = {
			key: value.super_copy(self) # pyright: ignore[reportArgumentType]
			for key, value in self.banjo_tooie_path_finders.items()
		}
		new_state.banjo_tooie_forms_reach = {
			key: value.copy()
			for key, value in self.banjo_tooie_forms_reach.items()
		}
		new_state.banjo_tooie_forms_reach_regions = {
			key: value.copy()
			for key, value in self.banjo_tooie_forms_reach_regions.items()
		}
		new_state.banjo_tooie_air = self.banjo_tooie_air.copy()
		return new_state

if TYPE_CHECKING:
	class BanjoTooieState(CollectionState, BanjoTooieMixin): pass

def can_form_from_region_reach(
	form: data.Form,
	from_name: str,
	to_names: str | list[str],
	state: "BanjoTooieState",
	player: int
) -> bool:
	world: "BanjoTooieWorld" = state.multiworld.worlds[player] # pyright: ignore[reportAssignmentType]
	start = world.region_links[from_name][form]
	if not start.can_reach(state): return False
	if isinstance(to_names, str): to_names = [to_names]
	regions = {world.region_links[to_name][form] for to_name in to_names}
	try:
		state.banjo_tooie_transform_block[player] += 1
		for region in regions:
			if not state.banjo_tooie_path_finders[player][region].can_reach_any({start}): return False
		return True
	finally:
		state.banjo_tooie_transform_block[player] -= 1

def start_regions_links(world: "BanjoTooieWorld", state: CollectionState, forms: set[data.Form] | frozenset[data.Form]):
	start_links: list[dict[data.Form, BanjoTooieRegion]] = []
	for start in data.form_start_regions:
		links = world.region_links[start]
		if forms - set(links): continue
		for form in forms:
			if not links[form].can_reach(state): break
		else: start_links.append(links)
	return start_links

def forms_reach(forms: frozenset[data.Form], region_name: str, state: "BanjoTooieState", player: int) -> bool:
	hashed = (forms, region_name)
	if hashed in state.banjo_tooie_forms_reach[player]: return True
	world: "BanjoTooieWorld" = state.multiworld.worlds[player] # pyright: ignore[reportAssignmentType]
	start_links = start_regions_links(world, state, forms)
	if not start_links: return False
	queues: list[Generator[BanjoTooieRegion, Any, None]] = []
	dest_links = world.region_links[region_name]
	for form in forms:
		region = dest_links[form]
		if not region.can_reach(state): return False
		path_finder = state.banjo_tooie_path_finders[player][region]
		queues.append(path_finder.find_all({start[form] for start in start_links})) # pyright: ignore[reportArgumentType]
	can_access: Counter[str] = Counter()
	target = len(forms)
	last = ""
	try:
		state.banjo_tooie_transform_block[player] += 1
		while True:
			for queue in queues:
				try:
					region = next(queue)
					last = region.formless_name
					can_access[last] += 1
				except StopIteration:
					return False
			if can_access[last] == target:
				state.banjo_tooie_forms_reach[player].add(hashed)
				return True
	finally:
		state.banjo_tooie_transform_block[player] -= 1

def forms_reach_regions(region_names: dict[data.Form, str], state: "BanjoTooieState", player: int) -> bool:
	hashed = frozenset(region_names.items())
	if hashed in state.banjo_tooie_forms_reach_regions[player]: return True
	world: "BanjoTooieWorld" = state.multiworld.worlds[player] # pyright: ignore[reportAssignmentType]
	start_links = start_regions_links(world, state, set(region_names))
	if not start_links: return False
	queues: list[Generator[BanjoTooieRegion, Any, None]] = []
	for form, region_name in region_names.items():
		region = world.region_links[region_name][form]
		if not region.can_reach(state): return False
		path_finder = state.banjo_tooie_path_finders[player][region]
		queues.append(path_finder.find_all({start[form] for start in start_links})) # pyright: ignore[reportArgumentType]
	can_access: Counter[str] = Counter()
	target = len(region_names)
	last = ""
	try:
		state.banjo_tooie_transform_block[player] += 1
		while True:
			for queue in queues:
				try:
					region = next(queue)
					last = region.formless_name
					can_access[last] += 1
				except StopIteration:
					return False
			if can_access[last] == target:
				state.banjo_tooie_forms_reach_regions[player].add(hashed)
				return True
	finally:
		state.banjo_tooie_transform_block[player] -= 1

def can_form_reach(form: data.Form, region_name: str, state: CollectionState, player: int):
	world: "BanjoTooieWorld" = state.multiworld.worlds[player] # pyright: ignore[reportAssignmentType]
	return world.region_links[region_name][form].can_reach(state)

def calc_air(
		region: BanjoTooieRegion,
		form: data.Form,
		exit_name: str | None,
		world: "BanjoTooieWorld",
		state: "BanjoTooieState",
		player: int
	):
	air = 0
	max_air = 10.0 if state.has("Double Air", player) else 6.0
	if state.has("Fast Swimming", player): air_index = 1
	elif form == "Banjo-Kazooie" and world.rhythmic_swimming(state): air_index = 2
	else: air_index = 0
	if exit_name is not None:
		max_air -= region.region_data.exits[exit_name].air[region.form][air_index]
	checked_regions: set[BanjoTooieRegion] = set()
	queue: deque[tuple[BanjoTooieEntrance, float]] = deque([(entrance, max_air) for entrance in region.entrances]) # pyright: ignore[reportAssignmentType]
	while queue:
		entrance, region_air = queue.popleft()
		parent_region: BanjoTooieRegion | None = entrance.parent_region # pyright: ignore[reportAssignmentType]
		if (
			entrance.exit_data is not None
			and parent_region is not None
			and parent_region not in checked_regions
			and parent_region.can_reach(state)
			and entrance.access_rule(state)
		):
			if parent_region.form == "Sub":
				air = max_air
				break
			checked_regions.add(parent_region)
			air_cost = 0
			if parent_region.form in entrance.exit_data.air:
				air_cost = entrance.exit_data.air[parent_region.form][air_index]
				region_air -= air_cost
			if parent_region in state.banjo_tooie_air[player]:
				region_air = state.banjo_tooie_air[player][parent_region] - air_cost
				if region_air > air: air = region_air
			elif region_air > air:
				if parent_region.region_data.underwater:
					queue.extend([(new_entrance, region_air) for new_entrance in parent_region.entrances]) # pyright: ignore[reportArgumentType]
				else: air = region_air
	if not state.allow_partial_entrances: state.banjo_tooie_air[player][region] = air
	return air

def calc_time(
		region: BanjoTooieRegion,
		exit_name: str | None,
		state: "BanjoTooieState",
		player: int
	):
	air = 0
	max_air = 20
	air_index = 0
	if exit_name is not None:
		max_air -= region.region_data.exits[exit_name].air[region.form][air_index]
	checked_regions: set[BanjoTooieRegion] = set()
	queue: deque[tuple[BanjoTooieEntrance, float]] = deque([(entrance, max_air) for entrance in region.entrances]) # pyright: ignore[reportAssignmentType]
	while queue:
		entrance, region_air = queue.popleft()
		parent_region: BanjoTooieRegion | None = entrance.parent_region # pyright: ignore[reportAssignmentType]
		if (
			entrance.exit_data is not None
			and parent_region is not None
			and parent_region.region_data.underwater
			and parent_region not in checked_regions
			and parent_region.can_reach(state)
			and entrance.access_rule(state)
		):
			checked_regions.add(parent_region)
			air_cost = 0
			if parent_region.form in entrance.exit_data.air:
				air_cost = entrance.exit_data.air[parent_region.form][air_index]
				region_air -= air_cost
			if parent_region in state.banjo_tooie_air[player]:
				region_air = state.banjo_tooie_air[player][parent_region] - air_cost
				if region_air > air: air = region_air
			elif region_air > air:
				if parent_region.form == "Banjo-Kazooie": air = region_air
				else:
					queue.extend([(new_entrance, region_air) for new_entrance in parent_region.entrances]) # pyright: ignore[reportArgumentType]
	if not state.allow_partial_entrances: state.banjo_tooie_air[player][region] = air
	print(region.name, air)
	return air

def air(region_name: str, form: data.Form, exit_name: str | None, state: "BanjoTooieState", player: int):
	world: "BanjoTooieWorld" = state.multiworld.worlds[player] # pyright: ignore[reportAssignmentType]
	region = world.region_links[region_name][form]
	if not state.allow_partial_entrances and region in state.banjo_tooie_air[player]:
		return state.banjo_tooie_air[player][region]
	if form == "Talon Torpedo": return calc_time(region, exit_name, state, player)
	else: return calc_air(region, form, exit_name, world, state, player)

class BanjoTooieRules(ast.NodeTransformer):

	def __init__(self, world: "BanjoTooieWorld"):
		super().__init__()
		self.world = world
		self.cache: dict[str, Rule] = {}

		self.options: dict[str, Any] = {}
		option_names: dict[str, str] = {}
		for name, cls in get_type_hints(BanjoTooieOptionsList).items():
			option_names[cls.display_name] = name
			self.options[cls.__name__] = getattr(world.options, name)
			if issubclass(cls, OptionDict):
				for key in cast(dict[str, int], cls.valid_keys): # pyright: ignore[reportUnknownMemberType]
					self.options[data.item_name(f"{cls.__name__} {key}")] = (getattr(world.options, name), key)

		self.items: dict[str, tuple[str, int, int]] = {}
		for progressive, item_list in data.progressives.items():
			option_name = option_names[progressive]
			if getattr(world.options, option_name).value:
				i = 1
				for item_name in item_list:
					item_name = data.parser.items[item_name]
					if hasattr(world.options, f"{option_name}_list"):
						if item_name not in getattr(world.options, f"{option_name}_list").value:
							self.items[item_name] = (item_name, world.player, 1)
							continue
					self.items[item_name] = (progressive, world.player, i)
					i += 1
			else:
				for item_name in item_list:
					item_name = data.parser.items[item_name]
					self.items[item_name] = (item_name, world.player, 1)

		self.ctx: dict[str, Any] = {
			"Player": world.player,
			"option": self.option,
			"trick": self.trick,
			"items": self.items,
			"can_form_from_region_reach": can_form_from_region_reach,
			"forms_reach": forms_reach,
			"forms_reach_regions": forms_reach_regions,
			"can_form_reach": can_form_reach,
			"air": air,
		}

	def option(self, option: str) -> Any:
		opt = self.options[option]
		cls = type(opt) # pyright: ignore[reportUnknownVariableType]
		if cls is tuple:
			return opt[0].value[opt[1]] # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
		if issubclass(cls, Choice):
			return opt.current_key
		return opt.value

	def trick(self, trick: str):
		return trick in self.world.options.logic_tricks.value

	def parse(self, logic: CodeType) -> Rule:
		if logic is data.parser.true: return true
		if logic is data.parser.false: return false
		return eval(logic, self.ctx)
