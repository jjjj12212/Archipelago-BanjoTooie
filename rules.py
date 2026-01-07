import ast
from collections import deque
from typing import Callable, Any, Counter, Generator, cast, TYPE_CHECKING, get_type_hints
from Options import Choice
from BaseClasses import CollectionState, Region, Entrance, MultiWorld
from worlds.AutoWorld import LogicMixin
from .regions import BanjoTooieEntrance, BanjoTooieRegion
from . import locations, items, data

if TYPE_CHECKING:
	from . import BanjoTooieWorld

true: Callable[[CollectionState], bool] = lambda _state: True
false: Callable[[CollectionState], bool] = lambda _state: False

dynamic_options = (
	"chosen_move_silo_costs",
)

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

class BanjoTooieRules(ast.NodeTransformer):
	debug = False

	def can_form_from_region_reach(
		self,
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

	def start_links(self, world: "BanjoTooieWorld", state: CollectionState, forms: set[data.Form] | frozenset[data.Form]):
		start_links: list[dict[data.Form, BanjoTooieRegion]] = []
		for start in data.form_start_regions:
			links = world.region_links[start]
			if forms - set(links): continue
			for form in forms:
				if not links[form].can_reach(state): break
			else: start_links.append(links)
		return start_links

	def forms_reach(self, forms: frozenset[data.Form], region_name: str, state: "BanjoTooieState", player: int) -> bool:
		hashed = (forms, region_name)
		if hashed in state.banjo_tooie_forms_reach[player]: return True
		world: "BanjoTooieWorld" = state.multiworld.worlds[player] # pyright: ignore[reportAssignmentType]
		start_links = self.start_links(world, state, forms)
		if not start_links: return False
		queues: list[Generator[BanjoTooieRegion, Any, None]] = []
		dest_links = world.region_links[region_name]
		for form in forms:
			path_finder = state.banjo_tooie_path_finders[player][dest_links[form]]
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

	def forms_reach_regions(self, region_names: dict[data.Form, str], state: "BanjoTooieState", player: int) -> bool:
		hashed = frozenset(region_names.items())
		if hashed in state.banjo_tooie_forms_reach_regions[player]: return True
		world: "BanjoTooieWorld" = state.multiworld.worlds[player] # pyright: ignore[reportAssignmentType]
		start_links = self.start_links(world, state, set(region_names))
		if not start_links: return False
		queues: list[Generator[BanjoTooieRegion, Any, None]] = []
		for form, region_name in region_names.items():
			region = world.region_links[region_name][form]
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

	def air(self, region_name: str, form: data.Form, exit_name: str | None, state: "BanjoTooieState", player: int):
		region: BanjoTooieRegion = state.multiworld.get_region(data.regions[region_name]["names"][form], player) # pyright: ignore[reportAssignmentType]
		if not state.allow_partial_entrances and region in state.banjo_tooie_air[player]:
			return state.banjo_tooie_air[player][region]
		air = 0
		max_air = 10.0 if state.has("Double Air", player) else 6.0
		if state.has("Fast Swimming", player): air_index = 1
		elif form == "Banjo-Kazooie" and self.cache[self.tricks["RhythmicSwimming"]](state): air_index = 2
		else: air_index = 0
		if (
			exit_name is not None
			and "exits" in region.region_data
		):
			exit_data = region.region_data["exits"][exit_name]
			if "air" in exit_data:
				max_air -= exit_data["air"][region.form][air_index]
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
				if "air" in entrance.exit_data and parent_region.form in entrance.exit_data["air"]:
					air_cost = entrance.exit_data["air"][parent_region.form][air_index]
					region_air -= air_cost
				if parent_region in state.banjo_tooie_air[player]:
					region_air = state.banjo_tooie_air[player][parent_region] - air_cost
					if region_air > air: air = region_air
				elif region_air > air:
					if parent_region.region_data.get("underwater", False):
						queue.extend([(new_entrance, region_air) for new_entrance in parent_region.entrances]) # pyright: ignore[reportArgumentType]
					else: air = region_air
		if not state.allow_partial_entrances: state.banjo_tooie_air[player][region] = air
		return air

	@staticmethod
	def option_value(value: Any) -> ast.AST:
		if isinstance(value, set):
			return ast.Tuple(elts=[ast.Constant(value=elt) for elt in cast(set[str | int], value)], ctx=ast.Load())
		return ast.Constant(value=value)

	def __init__(self, world: "BanjoTooieWorld"):
		self.world = world
		self.entrance: BanjoTooieEntrance | None = None
		self.cache: dict[str, Callable[[CollectionState], bool]] = {}
		self.player = ast.Constant(value=world.player)
		self.alias: set[str] = set()
		self.options_static: dict[str, ast.AST] = {}
		self.options_dynamic: dict[str, str] = {}
		option_names: dict[str, str] = {}
		for option_name, option_class in get_type_hints(type(world.options)).items():
			option_names[option_class.display_name] = option_name
			if option_name in dynamic_options: self.options_dynamic[option_class.__name__] = option_name
			option = getattr(world.options, option_name)
			value = option.value
			if isinstance(option, Choice):
				value = option.current_key
			if isinstance(value, dict):
				for key, val in cast(dict[str, int], value).items():
					self.options_static[data.item_name(f"{option_class.__name__} {key}")] = self.option_value(val)
			else: self.options_static[option_class.__name__] = self.option_value(value)
		self.items = {data.item_name(location_name):location_name for location_name in locations.name_to_id}
		self.items |= items.names
		self.item_groups: dict[str, set[str]] = {}
		for group_name, group_items in data.item_groups.items():
			self.item_groups[group_name] = {self.items[item_name] for item_name in group_items}
		self.progressives: dict[str, tuple[str, int]] = {}
		for progressive, item_list in data.progressives.items():
			option_name = option_names[progressive]
			if getattr(world.options, option_name).value:
				i = 1
				for item_name in item_list:
					if hasattr(world.options, f"{option_name}_list"):
						if item_name not in {data.item_name(value) for value in getattr(world.options, f"{option_name}_list").value}:
							continue
					if item_name not in self.progressives: self.progressives[item_name] = (data.item_name(progressive), i)
					else:
						raise Exception(
							f"{world.game}: Item '{item_name}' part of multiple Progressive items. This should never happen."
						)
					i += 1
		self.tricks: dict[str, str] = {}
		for tricks in data.tricks.values():
			for name, logic in tricks.items():
				item_name = data.item_name(name)
				if name in world.options.logic_tricks.value:
					self.tricks[item_name] = f"({logic})"
				else: self.tricks[item_name] = "False"
		self.parse(self.tricks["RhythmicSwimming"], "data/tricks.py")
		self.ctx: dict[str, Any] = {
			"ItemGroups": self.item_groups,
			"options": self.world.options,
			"forms_reach": self.forms_reach,
			"forms_reach_regions": self.forms_reach_regions,
			"can_form_from_region_reach": self.can_form_from_region_reach,
			"air": self.air,
		}

	def parse(self, logic: str, file: str, arg: str="state", indirect_regions: set[str] | None = None) -> Callable[[Any], bool]:
		match logic:
			case "True" | "true" | "": return true
			case "False" | "false": return false
			case _: pass
		if not self.debug and logic in self.cache: return self.cache[logic]
		self.indirect_regions = indirect_regions
		self.file = file
		self.arg = arg
		if self.debug:
			print(self.file)
			print(f"   logic: {logic}")
		node = self.visit(ast.parse(f"lambda {arg}: ({logic})", self.file, mode="eval"))
		if isinstance(node.body.body, ast.Constant):
			self.cache[logic] = true if node.body.body.value else false
			self.indirect_regions = None
			return self.cache[logic]
		node = ast.fix_missing_locations(node)
		if self.debug:
			print(f"  parsed: {ast.unparse(node)}")
		func = eval(compile(node, self.file, "eval"), self.ctx)
		self.cache[logic] = func
		self.indirect_regions = None
		return func

	def make_attr(self, value: str, attr: str) -> ast.Attribute:
		return ast.Attribute(
			value=ast.Name(id=value, ctx=ast.Load()),
			attr=attr,
			ctx=ast.Load()
		)

	def make_call(self, func: str, args: list[Any]) -> ast.Call:
		args.insert(1, self.player)
		return ast.Call(
			func=self.make_attr("state", func),
			args=args,
			keywords=[]
		)

	def get_option(self, option_name: str) -> ast.Attribute:
		option_name = self.options_dynamic[option_name]
		option = getattr(self.world.options, option_name)
		attr = "value"
		if isinstance(option, Choice):
			attr = "current_key"
		return ast.Attribute(
			value=self.make_attr("options", option_name),
			attr=attr,
			ctx=ast.Load()
		)

	def get_item(self, item: str) -> ast.Constant:
		return ast.Constant(value=self.items[item])

	def get_alias(self, alias: str) -> ast.Expression:
		return ast.parse(f"({data.alias[alias]})", mode="eval")

	def visit_List(self, node: ast.List) -> ast.List:
		if not isinstance(node.ctx, ast.Load):
			raise Exception(f"Logic is read only\nFile: {self.file}")
		self.generic_visit(node)
		return node

	def visit_Starred(self, node: ast.Starred) -> ast.Starred:
		if not isinstance(node.ctx, ast.Load):
			raise Exception(f"Logic is read only\nFile: {self.file}")
		raise NotImplementedError(f"{self.file}")

	def visit_Subscript(self, node: ast.Subscript) -> ast.Subscript:
		if not isinstance(node.ctx, ast.Load):
			raise Exception(f"Logic is read only\nFile: {self.file}")
		if isinstance(node.value, ast.Name) and isinstance(node.slice, ast.Constant):
			if node.value.id in self.options_dynamic: node.value = self.visit(node.value)
			return node
		raise TypeError(f"object is not subscriptable\nFile: {self.file}")

	def visit_UnaryOp(self, node: ast.UnaryOp) -> ast.UnaryOp | ast.Constant:
		self.generic_visit(node)
		if isinstance(node.op, ast.Not) and isinstance(node.operand, ast.Constant):
			return ast.Constant(value=eval(compile(ast.fix_missing_locations(ast.Expression(body=node)), "<string>", "eval")))
		return node

	def visit_Compare(self, node: ast.Compare) -> ast.Compare | ast.Constant:
		self.generic_visit(node)
		if isinstance(node.left, ast.Constant):
			for child_node in node.comparators:
				if isinstance(child_node, ast.Tuple) or isinstance(child_node, ast.List):
					for elt in child_node.elts:
						if not isinstance(elt, ast.Constant):
							return node
				elif not isinstance(child_node, ast.Constant):
					return node
			return ast.Constant(value=eval(compile(ast.fix_missing_locations(ast.Expression(body=node)), "<string>", "eval")))
		return node

	def visit_Name(self, node: ast.Name) -> ast.AST:
		if not isinstance(node.ctx, ast.Load):
			raise Exception(f"Logic is read only\nFile: {self.file}")
		match node.id:
			case "true": return ast.Constant(value=True)
			case "false": return ast.Constant(value=False)
			case "Player": return self.player
			case "TransformBlock": return ast.Subscript(self.make_attr("state", "banjo_tooie_transform_block"), self.player)
			case _: pass
		if node.id in data.alias and node.id not in self.alias:
			self.alias.add(node.id)
			new_node = self.visit(self.get_alias(node.id)).body
			self.alias.remove(node.id)
			return new_node
		if node.id in self.tricks: return self.visit(ast.parse(f"({self.tricks[node.id]})", mode="eval")).body
		if self.arg == "item":
			if node.id in self.items: return self.get_item(node.id)
		else:
			if node.id in self.progressives:
				return self.reduce_BoolOp(
					ast.BoolOp(
						op=ast.Or(),
						values=[
							self.make_call("has", [self.get_item(progressive), ast.Constant(value=level)])
							for progressive, level in [self.progressives[node.id], (node.id, 1)]
						]
					)
				)
			if node.id in self.items: return self.make_call("has", [self.get_item(node.id)])
		if node.id in self.options_static: return self.options_static[node.id]
		if node.id in self.options_dynamic: return self.get_option(node.id)
		raise NameError(f"name '{node.id}' is not defined\nFile: {self.file}")

	def visit_Attribute(self, node: ast.Attribute) -> ast.Attribute:
		if not isinstance(node.ctx, ast.Load):
			raise Exception(f"Logic is read only\nFile: {self.file}")
		if isinstance(node.value, ast.Name):
			if self.arg == "item" and node.value.id == "item":
				if node.attr in ["name", "player"]: return node
			raise AttributeError(f"name '{node.value.id}' has no attribute '{node.attr}'\nFile: {self.file}")
		raise AttributeError(f"object has no attribute '{node.attr}'\nFile: {self.file}")

	def visit_Tuple(self, node: ast.Tuple):
		if not isinstance(node.ctx, ast.Load):
			raise Exception(f"Logic is read only\nFile: {self.file}")
		assert len(node.elts) == 2, f"{self.file}: Tuples must have exactly 2 elements."
		item, count = node.elts
		count = self.visit(count)
		assert isinstance(item, ast.Name), f"{self.file}: The first element of a Tuple must be an ast.Name."
		assert item.id in self.items, f"{self.file}: The first element of a Tuple must be an item."
		return self.make_call("has", [self.get_item(item.id), count])

	def reduce_BoolOp(self, node: ast.BoolOp) -> ast.AST:
		opIsAnd = isinstance(node.op, ast.And)
		values: list[ast.AST] = []
		grouped: dict[str, int] = {}
		for child_node in node.values:
			if isinstance(child_node, ast.Constant) and not isinstance(child_node.value, str):
				if opIsAnd:
					if child_node.value: continue
					else: return child_node
				else:
					if child_node.value: return child_node
					else: continue
			elif (
				isinstance(child_node, ast.Call) and isinstance(child_node.func, ast.Attribute)
				and isinstance(child_node.func.value, ast.Name) and child_node.func.value.id == "state"
				and len(child_node.args) and (
					(child_node.func.attr == "has" and isinstance(child_node.args[0], ast.Constant))
					or (not opIsAnd and child_node.func.attr == "has_any" and isinstance(child_node.args[0], ast.Tuple))
					or (not opIsAnd and child_node.func.attr == "has_any_count" and isinstance(child_node.args[0], ast.Dict))
					or (opIsAnd and child_node.func.attr == "has_all" and isinstance(child_node.args[0], ast.Tuple))
					or (opIsAnd and child_node.func.attr == "has_all_counts" and isinstance(child_node.args[0], ast.Dict))
				)
			):
				items: dict[str, int] = {}
				match child_node.func.attr:
					case "has":
						arg = child_node.args[0]
						if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
							item = arg.value
							items[item] = 1
							if len(child_node.args) == 3:
								arg = child_node.args[2]
								if isinstance(arg, ast.Constant) and isinstance(arg.value, int):
									items[item] = arg.value
					case "has_any" | "has_all":
						arg = child_node.args[0]
						if isinstance(arg, ast.Tuple):
							for elt in arg.elts:
								if not isinstance(elt, ast.Constant):
									values.append(child_node)
									continue
								if isinstance(elt.value, str):
									if elt.value not in items: items[elt.value] = 0
									items[elt.value] += 1
					case "has_any_count" | "has_all_counts":
						arg = child_node.args[0]
						if isinstance(arg, ast.Dict):
							contents = arg
							for i, item in enumerate(contents.keys):
								count = contents.values[i]
								if not isinstance(item, ast.Constant) or not isinstance(count, ast.Constant):
									values.append(child_node)
									continue
								if isinstance(item.value, str) and isinstance(count.value, int):
									items[item.value] = count.value
				for item, count in items.items():
					if item not in grouped: grouped[item] = count
					else:
						if child_node.func.attr == "has_any_count":
							if grouped[item] > count: grouped[item] = count
						elif grouped[item] < count: grouped[item] = count
			else: values.append(child_node)

		if len(grouped):
			has_func = "has"
			grouped_keys: list[ast.Constant] = []
			grouped_values: list[ast.Constant] = []
			for item, count in grouped.items():
				if count > 1:
					if opIsAnd: has_func = "has_all_counts"
					else: has_func = "has_any_count"
				grouped_keys.append(ast.Constant(value=item))
				grouped_values.append(ast.Constant(value=count))
			if has_func == "has":
				if len(grouped_keys) == 1:
					values.append(self.make_call("has", [grouped_keys[0]]))
				else:
					values.append(
						self.make_call(
							"has_all" if opIsAnd else "has_any",
							[ast.Tuple(elts=cast(list[ast.expr], grouped_keys), ctx=ast.Load())]
						)
					)
			else:
				values.append(
					self.make_call(
						has_func,
						[ast.Dict(keys=cast(list[ast.expr | None], grouped_keys), values=cast(list[ast.expr], grouped_values))]
					)
				)

		node.values = cast(list[ast.expr], values)
		match len(node.values):
			case 0:
				return ast.Constant(value=opIsAnd)
			case 1:
				return node.values[0]
			case _: pass
		return node

	def visit_BoolOp(self, node: ast.BoolOp) -> ast.AST:
		self.generic_visit(node)
		return self.reduce_BoolOp(node)

	def visit_Call(self, node: ast.Call) -> ast.AST:
		if isinstance(node.func, ast.Name) and isinstance(node.func.ctx, ast.Load):
			match node.func.id:
				case "exclude":
					node.keywords = []
					assert len(node.args) >= 2, f"{self.file}: exclude requires at least 2 arguments."
					except_list: list[str] = []
					items = node.args[0]
					if isinstance(items, ast.Name) and items.id in data.alias:
						items = self.get_alias(items.id).body
					assert isinstance(items, ast.BoolOp), f"{self.file}: exclude requires arg 1 to be a single list of items."
					for idx, arg in enumerate(node.args):
						if idx > 0:
							assert isinstance(arg, ast.Name), f"{self.file}: exclude invalid arg: {idx}"
							except_list.append(arg.id)
					new_items: list[ast.expr] = []
					for elt in items.values:
						assert isinstance(elt, ast.Name), f"{self.file}: exclude requires arg 1 to be a single list of items."
						if elt.id not in except_list: new_items.append(elt)
					items.values = new_items
					return self.visit_BoolOp(items)
				case "count":
					node.keywords = []
					assert len(node.args) == 1, f"{self.file}: count requires exactly 1 argument."
					item = self.visit(node.args[0])
					assert isinstance(item, ast.Call), f"{self.file}: count invalid arg."
					node.func = self.make_attr("state", "count")
					node.args = [item.args[0], self.player]
					return node
				case "forms_reach":
					node.keywords = []
					assert len(node.args) == 2, f"{self.file}: forms_reach requires exactly 2 arguments."
					assert isinstance(node.args[0], ast.Set), f"{self.file}: forms_reach requires arg 1 to be a set."
					forms: set[data.Form] = set()
					for arg in node.args[0].elts:
						assert (
							isinstance(arg, ast.Constant)
							and isinstance(arg.value, str)
						), f"{self.file}: forms_reach requires set to contain only str."
						forms.add(cast(data.Form, arg.value))
					node.args[0] = ast.Call(ast.Name("frozenset"), [node.args[0]])
					assert (
						isinstance(node.args[1], ast.Constant)
						and isinstance(node.args[1].value, str)
					), f"{self.file}: forms_reach requires arg 2 to be a str."
					if self.indirect_regions is not None:
						region = data.regions[node.args[1].value]
						for start_name in data.form_start_regions:
							start = data.regions[start_name]
							if forms - set(start["names"]): continue
							for form in forms:
								self.indirect_regions.add(start["names"][form])
								self.indirect_regions.add(region["names"][form])
					node.args += [ast.Name(id="state", ctx=ast.Load()), self.player]
					return node
				case "can_form_from_region_reach":
					node.keywords = []
					assert len(node.args) == 3, f"{self.file}: can_form_from_region_reach requires exactly 3 arguments."
					for idx, arg in enumerate(node.args[0:2]):
						assert (
							isinstance(arg, ast.Constant)
							and isinstance(arg.value, str)
						), f"{self.file}: can_form_from_region_reach requires arg {idx+1} to be a string."
					arg = node.args[2]
					assert (
						isinstance(arg, ast.Constant) and isinstance(arg.value, str)
						or isinstance(arg, ast.List)
					), f"{self.file}: can_form_from_region_reach requires arg 3 to be a string or list of strings."
					if isinstance(arg, ast.List):
						to_names: list[str] = []
						for elt in arg.elts:
							assert (
								isinstance(elt, ast.Constant) and isinstance(elt.value, str)
							), f"{self.file}: can_form_from_region_reach requires arg 3 to be a string or list of strings."
							to_names.append(elt.value)
					else: to_names = [cast(str, arg.value)]
					if self.indirect_regions is not None:
						form = cast(data.Form, cast(ast.Constant, node.args[0]).value)
						from_name = cast(str, cast(ast.Constant, node.args[1]).value)
						self.indirect_regions.add(data.regions[from_name]["names"][form])
						for to_name in to_names:
							self.indirect_regions.add(data.regions[to_name]["names"][form])
					node.args += [ast.Name(id="state", ctx=ast.Load()), self.player]
					return node
				case "forms_reach_regions":
					node.keywords = []
					assert len(node.args) == 1, f"{self.file}: forms_reach_regions requires exactly 1 argument."
					arg = node.args[0]
					assert isinstance(arg, ast.Dict), f"{self.file}: forms_reach_regions requires arg 1 to be a dict[str, str]."
					region_names: dict[data.Form, str] = {}
					for idx, key in enumerate(arg.keys):
						value = arg.values[idx]
						assert (
							isinstance(key, ast.Constant) and isinstance(key.value, str)
							and isinstance(value, ast.Constant) and isinstance(value.value, str)
						), f"{self.file}: forms_reach_regions requires arg 1 to be a dict[str, str]."
						region_names[cast(data.Form, key.value)] = value.value
					if self.indirect_regions is not None:
						forms = set(region_names)
						for start_name in data.form_start_regions:
							start = data.regions[start_name]
							if forms - set(start["names"]): continue
							for form, region_name in region_names.items():
								region = data.regions[region_name]
								self.indirect_regions.add(start["names"][form])
								self.indirect_regions.add(region["names"][form])
					node.args += [ast.Name(id="state", ctx=ast.Load()), self.player]
					return node
				case "air":
					node.keywords = []
					assert len(node.args) == 3, f"{self.file}: air requires exactly 3 arguments."
					args = node.args
					for i, arg in enumerate(args[:2]):
						assert (
							isinstance(arg, ast.Constant)
							and isinstance(arg.value, str)
						), f"{self.file}: air requires arg {i+1} to be a str."
					assert (
						isinstance(args[2], ast.Constant)
						and (args[2].value is None or isinstance(args[2].value, str))
					), f"{self.file}: air requires arg 3 to be a str or None."
					node.args += [ast.Name(id="state", ctx=ast.Load()), self.player]
					return node
				case _: pass
		self.generic_visit(node)
		return node
