import ast
from collections import deque
from typing import Callable, Any, Counter, Generator, cast, TYPE_CHECKING, get_type_hints

from Options import Choice, OptionDict
from BaseClasses import CollectionState, Region, Entrance, MultiWorld
from worlds.AutoWorld import LogicMixin
from .regions import BanjoTooieEntrance, BanjoTooieRegion
from . import data
from .data.parser import Parser

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

def air(region_name: str, form: data.Form, exit_name: str | None, state: "BanjoTooieState", player: int):
	world: "BanjoTooieWorld" = state.multiworld.worlds[player] # pyright: ignore[reportAssignmentType]
	region = world.region_links[region_name][form]
	if not state.allow_partial_entrances and region in state.banjo_tooie_air[player]:
		return state.banjo_tooie_air[player][region]
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

class BanjoTooieRules(ast.NodeTransformer):
	player = Parser.player

	def __init__(self, world: "BanjoTooieWorld"):
		super().__init__()
		self.world = world
		self.item_name_only = 0
		self.cache: dict[str, Rule] = {}
		option_names: dict[str, str] = {}
		self.options: dict[str, str] = {}
		self.options_choice: dict[str, str] = {}
		self.options_dict: dict[str, tuple[str, str]] = {}
		for option_name, option_class in get_type_hints(type(world.options)).items():
			option_names[option_class.display_name] = option_name
			name = option_class.__name__
			if issubclass(option_class, OptionDict):
				for key in cast(dict[str, int], option_class.valid_keys): # pyright: ignore[reportUnknownMemberType]
					self.options_dict[data.item_name(f"{name} {key}")] = (option_name, key)
			if issubclass(option_class, Choice):
				self.options_choice[name] = option_name
			else: self.options[name] = option_name
		self.tricks = {data.item_name(trick):trick for tricks in data.tricks.values() for trick in tricks}
		self.progressives: dict[str, tuple[str, int]] = {}
		for progressive, item_list in data.progressives.items():
			option_name = option_names[progressive]
			if getattr(world.options, option_name).value:
				i = 1
				for item_name in item_list:
					if hasattr(world.options, f"{option_name}_list"):
						if item_name not in {data.item_name(value) for value in getattr(world.options, f"{option_name}_list").value}:
							continue
					if item_name not in self.progressives:
						self.progressives[item_name] = (progressive, i)
					else:
						raise Exception(
							f"{world.game}: Item '{item_name}' part of multiple Progressive items. This should never happen."
						)
					i += 1
		self.ctx: dict[str, Any] = {
			"Player": world.player,
			"option": self.option,
			"option_dict": self.option_dict,
			"option_choice": self.option_choice,
			"trick": self.trick,
			"can_form_from_region_reach": can_form_from_region_reach,
			"forms_reach": forms_reach,
			"forms_reach_regions": forms_reach_regions,
			"can_form_reach": can_form_reach,
			"air": air,
		}

	def option(self, option: str):
		return getattr(self.world.options, self.options[option]).value

	def option_dict(self, option: str):
		value = self.options_dict[option]
		return getattr(self.world.options, value[0])[value[1]]

	def option_choice(self, option: str):
		return getattr(self.world.options, self.options_choice[option]).current_key

	def trick(self, trick: str):
		return trick in self.world.options.logic_tricks.value

	def state_has(self, args: list[ast.expr]):
		return ast.Call(Parser.expr("state.has"), args)

	def item_event(self, node: ast.Attribute, count: ast.expr = ast.Constant(1)):
		assert type(node.value) is ast.Name, f"{self.file}: Invalid attribute access `{ast.unparse(node)}`"
		if node.attr == "item":
			if node.value.id in self.progressives:
				progressive = self.progressives[node.value.id]
				name = progressive[0]
				count = ast.Constant(progressive[1])
			else: name = data.parser.items[node.value.id]
		else: name = data.parser.locations[node.value.id]
		item = ast.Constant(name)
		if self.item_name_only: return item
		args: list[ast.expr] = [item, self.player, count]
		return self.state_has(args)

	def parse(self, logic: str, file: str):
		self.regen_later = False
		match logic:
			case "": return true
			case "False": return false
			case _: pass
		if logic in self.cache: return self.cache[logic]
		self.file = file
		node = self.visit(ast.parse(f"lambda state: ({logic})", self.file, mode="eval"))
		node = ast.fix_missing_locations(node)
		if type(node.body.body) is ast.Constant:
			self.cache[logic] = true if node.body.body.value else false
			return self.cache[logic]
		if self.regen_later:
			self.logic = ast.unparse(node)
		func: Rule = eval(compile(node, self.file, "eval"), self.ctx)
		self.cache[logic] = func
		return func

	def visit_Name(self, node: ast.Name):
		if node.id in (
			"frozenset",
			"state",
			"forms_reach",
			"forms_reach_regions",
			"can_form_from_region_reach",
			"can_form_reach",
			"air",
		): return node
		match node.id:
			case "Player": return self.player
			case "TransformBlock": return Parser.expr("state.banjo_tooie_transform_block")
			case _: raise Exception(f"{self.file}: Not defined `{ast.unparse(node)}`")

	def visit_Attribute(self, node: ast.Attribute):
		assert type(node.value) is ast.Name, f"{self.file}: Invalid attribute access `{ast.unparse(node)}`"
		if node.value.id == "state": return self.generic_visit(node)
		match node.attr:
			case "option":
				self.regen_later = True
				if node.value.id in self.options_dict: func = "option_dict"
				elif node.value.id in self.options_choice: func = "option_choice"
				else: func = "option"
				return ast.Call(ast.Name(func), [ast.Constant(node.value.id)])
			case "trick":
				self.regen_later = True
				return ast.Call(ast.Name("trick"), [ast.Constant(self.tricks[node.value.id])])
			case "item" | "event": return self.item_event(node)
			case _: pass
		raise Exception(f"{self.file}: Unknown attribute access `{ast.unparse(node)}`")

	def visit_Tuple(self, node: ast.Tuple):
		item, count = node.elts
		assert (
			type(item) is ast.Attribute
			and type(item.value) is ast.Name
		), f"{self.file}: Invalid tuple `{ast.unparse(node)}`"
		return self.item_event(item, self.visit(count))

	def visit_BoolOp(self, node: ast.BoolOp):
		self.generic_visit(node)
		is_and = type(node.op) is ast.And
		items: dict[str, tuple[ast.Call, int]] = {}
		values: list[ast.expr] = []
		for child in node.values:
			if type(child) is ast.Call and ast.unparse(child.func) == "state.has":
				item = child.args[0]
				count = child.args[2]
				if (
					type(item) is ast.Constant and type(item.value) is str
					and type(count) is ast.Constant and type(count.value) is int
				):
					name: str = item.value
					amount: int = count.value
					update = False
					if name not in items: items[name] = (child, amount)
					else:
						if is_and:
							if amount > items[name][1]: update = True
						elif amount < items[name][1]: update = True
						if update:
							child = items[name][0]
							child.args[2] = count
							items[name] = (child, amount)
						continue
			values.append(child)
		node.values = values
		match len(values):
			case 0: return None
			case 1: return values[0]
			case _: return node

	def visit_Call(self, node: ast.Call):
		match ast.unparse(node.func):
			case "state.count":
				self.item_name_only += 1
				self.generic_visit(node)
				self.item_name_only -= 1
			case _: self.generic_visit(node)
		return node

class BanjoTooieFinalRules(ast.NodeTransformer):

	def __init__(self, world: "BanjoTooieWorld"):
		super().__init__()
		self.world = world
		self.player = ast.Constant(world.player)
		self.cache: dict[str, Rule] = {}
		self.ctx: dict[str, Any] = {
			"can_form_from_region_reach": can_form_from_region_reach,
			"forms_reach": forms_reach,
			"forms_reach_regions": forms_reach_regions,
			"can_form_reach": can_form_reach,
			"air": air,
		}

	def option(self, option: str):
		return getattr(self.world.options, self.world.parser.options[option]).value

	def option_dict(self, option: str):
		value = self.world.parser.options_dict[option]
		return getattr(self.world.options, value[0])[value[1]]

	def option_choice(self, option: str):
		return getattr(self.world.options, self.world.parser.options_choice[option]).current_key

	def func_value(self, node: ast.Call):
		if not node.args: return None
		arg = node.args[0]
		if type(arg) is ast.Constant and type(arg.value) is str:
			match ast.unparse(node.func):
				case "trick": return arg.value in self.world.options.logic_tricks.value
				case "option": return self.option(arg.value)
				case "option_dict": return self.option_dict(arg.value)
				case "option_choice": return self.option_choice(arg.value)
				case _: pass
		return None

	def parse(self, logic: str, file: str):
		if logic in self.cache: return self.cache[logic]
		self.file = file
		self.start = True
		node = self.visit(ast.parse(logic, self.file, mode="eval"))
		node = ast.fix_missing_locations(node)
		if type(node.body.body) is ast.Constant:
			self.cache[logic] = true if node.body.body.value else false
			return self.cache[logic]
		func: Rule = eval(compile(node, self.file, "eval"), self.ctx)
		self.cache[logic] = func
		return func

	def visit_UnaryOp(self, node: ast.UnaryOp):
		self.generic_visit(node)
		return Parser.simplify_UnaryOp(node)

	def visit_Name(self, node: ast.Name):
		match node.id:
			case "Player": return self.player
			case _: return self.generic_visit(node)

	def visit_BoolOp(self, node: ast.BoolOp):
		start = self.start
		self.start = False
		self.generic_visit(node)
		ret = Parser.simplify_BoolOp(node)
		if start and ret is None:
			return ast.Constant(type(node.op) is ast.And)
		return ret

	def visit_Subscript(self, node: ast.Subscript):
		if type(node.value) is ast.Call and type(node.slice) is ast.Constant:
			value = self.func_value(node.value)
			assert type(value) is dict, f"{self.file}: Invalid subscript `{ast.unparse(node)}`"
			return Parser.expr(value[node.slice.value]) # pyright: ignore[reportUnknownArgumentType]
		return self.generic_visit(node)

	def visit_Compare(self, node: ast.Compare):
		if type(node.left) is ast.Call:
			value = self.func_value(node.left)
			if value is not None:
				node.left = ast.Constant(value) if type(value) is str else Parser.expr(str(value))
		comps: list[ast.expr] = []
		for comp in node.comparators:
			if type(comp) is ast.Call:
				value = self.func_value(comp)
				if value is not None:
					comps.append(ast.Constant(value) if type(value) is str else Parser.expr(str(value)))
					continue
			comps.append(comp)
		node.comparators = comps
		self.generic_visit(node)
		return Parser.simplify_Compare(node)

	def visit_Call(self, node: ast.Call):
		value = self.func_value(node)
		if value is not None: return ast.Constant(value)
		return self.generic_visit(node)
