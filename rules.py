import ast
from collections import defaultdict, deque
from itertools import zip_longest
from typing import Callable, Any, Iterator, cast, TYPE_CHECKING, get_type_hints
from Options import Choice
from BaseClasses import CollectionState, Region, Entrance, MultiWorld
from worlds.AutoWorld import LogicMixin
from .regions import BanjoTooieEntrance
from . import locations, items, data

if TYPE_CHECKING:
	from . import BanjoTooieWorld

PathValue = tuple[str, "PathValue | None"]
RegionPairs = dict[Region, set[Region]]

true: Callable[[CollectionState], bool] = lambda _state: True
false: Callable[[CollectionState], bool] = lambda _state: False

dynamic_options = (
	"chosen_move_silo_costs",
)

class BanjoTooiePathFinder:

	def __init__(self, start: Region):
		self.locked = False
		self.start = start
		self.path: dict[Region | Entrance, PathValue] = {}
		self.reachable_regions: set[Region] = set()
		self.blocked_connections: set[Entrance] = set()

	def copy(self):
		ret = BanjoTooiePathFinder(self.start)
		ret.path = self.path.copy()
		ret.reachable_regions = self.reachable_regions.copy()
		ret.blocked_connections = self.blocked_connections.copy()
		return ret

	@staticmethod
	def flist_to_iter(path_value: PathValue | None) -> Iterator[str]:
		while path_value:
			region_or_entrance, path_value = path_value
			yield region_or_entrance

	def get_path(self, region: Region) -> list[tuple[str, str] | tuple[str, None]]:
		reversed_path_as_flist: PathValue = self.path.get(region, (str(region), None))
		string_path_flat = reversed(list(map(str, BanjoTooiePathFinder.flist_to_iter(reversed_path_as_flist))))
		pathsiter = iter(string_path_flat)
		pathpairs = zip_longest(pathsiter, pathsiter)
		return list(pathpairs)

	def can_reach_entrance(self, exit_: Entrance, state: CollectionState) -> bool:
		assert exit_.parent_region, f"called can_reach on a BanjoTooieEntrance '{self}' with no parent_region"
		if exit_.parent_region in self.reachable_regions and exit_.access_rule(state):
			if not exit_.hide_path and exit_ not in self.path:
				self.path[exit_] = (exit_.name, self.path.get(exit_.parent_region, (exit_.parent_region.name, None)))
			return True
		return False

	def can_reach_region(self, dest: Region) -> bool:
		return dest in self.reachable_regions

	def can_reach(self, dest: Region, state: CollectionState) -> bool:
		if dest in self.reachable_regions: return True
		if self.locked: return False
		self.locked = True
		try:
			if self.start not in self.reachable_regions:
				self.reachable_regions.add(self.start)
				self.blocked_connections.update(self.start.exits)
			queue = deque(self.blocked_connections)
			while queue:
				connection = queue.popleft()
				new_region = connection.connected_region
				if new_region in self.reachable_regions:
					self.blocked_connections.remove(connection)
				elif self.can_reach_entrance(connection, state):
					if not new_region: continue
					self.reachable_regions.add(new_region)
					self.blocked_connections.remove(connection)
					self.blocked_connections.update(new_region.exits)
					queue.extend(new_region.exits)
					self.path[new_region] = (new_region.name, self.path.get(connection, None))
					for new_entrance in state.multiworld.indirect_connections.get(new_region, set()):
						if new_entrance in self.blocked_connections and new_entrance not in queue:
							queue.append(new_entrance)
					if dest is new_region: return True
			return False
		finally:
			self.locked = False

class BanjoTooiePathFinders(dict[Region, BanjoTooiePathFinder]):

	def __missing__(self, start: Region):
		path_finder = BanjoTooiePathFinder(start)
		self[start] = path_finder
		return path_finder

	def copy(self):
		return BanjoTooiePathFinders(super().copy())

class BanjoTooieMixin(LogicMixin):
	banjo_tooie_path_finders: dict[int, BanjoTooiePathFinders]

	def init_mixin(self, multiworld: MultiWorld) -> None:
		self.banjo_tooie_path_finders = {
			player: BanjoTooiePathFinders() for player in multiworld.get_game_players("Banjo-Tooie")
		}

	def copy_mixin(self, new_state: "BanjoTooieMixin"):
		new_state.banjo_tooie_path_finders = {
			player: path_finder.copy() for player, path_finder in self.banjo_tooie_path_finders.items()
		}
		return new_state

class BanjoTooieRules(ast.NodeTransformer):
	debug = False

	def check_region_pairs(self, pairs: list[RegionPairs], state: Any, player: int) -> bool:
		state.add_item("TransformBlock", player)
		for pair in pairs:
			can_reach = True
			for start_region, end_regions in pair.items():
				path_finder = state.banjo_tooie_path_finders[player][start_region]
				for end_region in end_regions:
					if not path_finder.can_reach(end_region, state):
						can_reach = False
						break
				if not can_reach: break
			if can_reach: return True
		return False

	def can_form_from_region_reach(
		self,
		form: data.Form,
		from_name: str,
		to_names: str | list[str],
		state: Any,
		player: int
	) -> bool:
		world = cast("BanjoTooieWorld", state.multiworld.worlds[player])
		start = world.get_region(data.regions[from_name]["names"][form])
		if not start.can_reach(state): return False
		path_finder = state.banjo_tooie_path_finders[player][start]
		if isinstance(to_names, str): to_names = [to_names]
		regions: set[Region] = set()
		for to_name in to_names:
			region = world.get_region(data.regions[to_name]["names"][form])
			if region.can_reach(state): regions.add(region)
		can_reach = True
		for region in regions:
			if not path_finder.can_reach_region(region):
				can_reach = False
				break
		if can_reach: return True
		return self.check_region_pairs([{start:regions}], state.copy(), player)

	def forms_reach(self, forms: set[data.Form], region_name: str, state: Any, player: int) -> bool:
		world = cast("BanjoTooieWorld", state.multiworld.worlds[player])
		region = data.regions[region_name]
		pairs: list[RegionPairs] = []
		for start_name in data.form_start_regions:
			start = data.regions[start_name]
			if forms - set(start["names"]): continue
			pair: RegionPairs = defaultdict(set)
			can_reach = True
			for form in forms:
				start_region = world.get_region(start["names"][form])
				end_region = world.get_region(region["names"][form])
				if not start_region.can_reach(state) or not end_region.can_reach(state):
					pair.clear()
					break
				if can_reach and not state.banjo_tooie_path_finders[player][start_region].can_reach_region(end_region):
					can_reach = False
				pair[start_region].add(end_region)
			if pair:
				if can_reach: return True
				pairs.append(pair)
		return self.check_region_pairs(pairs, state.copy(), player)

	def forms_reach_regions(self, region_names: dict[data.Form, str], state: Any, player: int) -> bool:
		world = cast("BanjoTooieWorld", state.multiworld.worlds[player])
		pairs: list[RegionPairs] = []
		forms = set(region_names)
		for start_name in data.form_start_regions:
			start = data.regions[start_name]
			if forms - set(start["names"]): continue
			pair: RegionPairs = defaultdict(set)
			can_reach = True
			for form, region_name in region_names.items():
				region = data.regions[region_name]
				start_region = world.get_region(start["names"][form])
				end_region = world.get_region(region["names"][form])
				if not start_region.can_reach(state) or not end_region.can_reach(state):
					pair.clear()
					break
				if can_reach and not state.banjo_tooie_path_finders[player][start_region].can_reach_region(end_region):
					can_reach = False
				pair[start_region].add(end_region)
			if pair:
				if can_reach: return True
				pairs.append(pair)
		return self.check_region_pairs(pairs, state.copy(), player)

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
		self.ctx: dict[str, Any] = {
			"ItemGroups": self.item_groups,
			"options": self.world.options,
			"forms_reach": self.forms_reach,
			"forms_reach_regions": self.forms_reach_regions,
			"can_form_from_region_reach": self.can_form_from_region_reach,
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
			case "TransformBlock": return self.make_call("has", [ast.Constant(value=node.id)])
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
				case _: pass
		self.generic_visit(node)
		return node
