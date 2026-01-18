import ast, re
from types import CodeType

true = compile(ast.parse("lambda _state: True", "<string>", "eval"), "<string>", "eval")
false = compile(ast.parse("lambda _state: False", "<string>", "eval"), "<string>", "eval")

from .forms import Form
from .types import FinalExit
from .alias import alias
from .progressives import progressives as real_progressives
from .tricks import tricks as real_tricks
from .item_info import items as real_items

def item_name(value: str) -> str:
	return re.sub("[^a-zA-Z0-9]+", "", value)

progressives = {name for items in real_progressives.values() for name in items}
tricks = {item_name(trick):(trick, logic) for tricks in real_tricks.values() for trick, logic in tricks.items()}
items = {item_name(name):name for items in real_items.values() for name in items}
events: dict[str, str] = {}
item_names: dict[str, str] = {}

class Parser(ast.NodeTransformer):
	player = ast.Name("Player")
	file: str
	alias: set[str]
	is_exit: bool
	create_exit_event: bool
	region_name: str
	form: Form
	exit_name: str
	exit: FinalExit
	item_name_only: int

	def parse(self, logic: str, file: str) -> CodeType:
		match logic:
			case "" | "true" | "True": return true
			case "false" | "False": return false
			case _: pass
		self.file = file
		self.alias = set()
		self.create_exit_event = False
		self.item_name_only = 0
		node = self.visit(ast.parse(f"lambda state: ({logic})", file, "eval"))
		node = ast.fix_missing_locations(node)
		if type(node.body.body) is ast.Constant:
			return true if node.body.body.value else false
		return compile(node, file, "eval")

	@staticmethod
	def expr(expr: str):
		return ast.parse(f"({expr})", "<string>", "eval").body

	@staticmethod
	def simplify_BoolOp(node: ast.BoolOp):
		values: list[ast.expr] = []
		for child in node.values:
			if type(child) is ast.Constant:
				if type(node.op) is ast.And:
					if not child.value: return child
				elif child.value: return child
			elif type(child) is ast.BoolOp and type(node.op) is type(child.op):
				values += child.values
			else: values.append(child)
		node.values = values
		match len(values):
			case 0: return None
			case 1: return values[0]
			case _: return node

	@staticmethod
	def simplify_Compare(node: ast.Compare):
		for comp in [node.left] + node.comparators:
			if isinstance(comp, ast.Tuple) or isinstance(comp, ast.List) or isinstance(comp, ast.Set):
				for elt in comp.elts:
					if not isinstance(elt, ast.Constant):
						return node
			elif not isinstance(comp, ast.Constant):
				return node
		return ast.Constant(value=eval(compile(ast.fix_missing_locations(ast.Expression(body=node)), "<string>", "eval")))

	@staticmethod
	def simplify_UnaryOp(node: ast.UnaryOp):
		if type(node.op) is ast.Not and type(node.operand) is ast.Constant:
			return ast.Constant(value=not node.operand.value)
		return node

	@staticmethod
	def state(attr: str):
		return ast.Attribute(ast.Name("state"), attr)

	def visit_List(self, node: ast.List):
		assert type(node.ctx) is ast.Load, f"Logic is read only\nFile: {self.file}"
		self.generic_visit(node)
		return node

	def visit_Starred(self, node: ast.Starred) -> ast.Starred:
		raise NotImplementedError(f"{self.file}")

	def visit_Subscript(self, node: ast.Subscript) -> ast.Subscript:
		assert type(node.ctx) is ast.Load, f"Logic is read only\nFile: {self.file}"
		self.generic_visit(node)
		return node

	def visit_UnaryOp(self, node: ast.UnaryOp):
		self.generic_visit(node)
		return self.simplify_UnaryOp(node)

	def visit_Compare(self, node: ast.Compare):
		self.generic_visit(node)
		return self.simplify_Compare(node)

	def visit_Attribute(self, node: ast.Attribute) -> ast.Attribute:
		raise AttributeError(f"object has no attribute '{node.attr}'\nFile: {self.file}")

	def visit_Tuple(self, node: ast.Tuple):
		assert type(node.ctx) is ast.Load, f"Logic is read only\nFile: {self.file}"
		assert len(node.elts) == 2, f"{self.file}: Tuples must have exactly 2 elements."
		self.item_name_only += 1
		self.generic_visit(node)
		self.item_name_only -= 1
		return ast.Call(self.state("has"), [node.elts[0], self.player, node.elts[1]])

	def visit_BoolOp(self, node: ast.BoolOp):
		self.generic_visit(node)
		simplified = self.simplify_BoolOp(node)
		if type(simplified) is not ast.BoolOp: return simplified
		is_and = type(node.op) is ast.And
		items: dict[str, tuple[ast.Call, int]] = {}
		values: list[ast.expr] = []
		for child in node.values:
			if type(child) is ast.Call and type(child.args[0]) is not ast.Starred and ast.unparse(child.func) == "state.has":
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

	def visit_Name(self, node: ast.Name):
		assert type(node.ctx) is ast.Load, f"Logic is read only\nFile: {self.file}"
		match node.id:
			case "true": return ast.Constant(value=True)
			case "false": return ast.Constant(value=False)
			case "Player": return node
			case "TransformBlock": return ast.Subscript(self.state("banjo_tooie_transform_block"), self.player)
			case "Air":
				if self.is_exit: self.create_exit_event = True
				return self.visit(ast.Call(
					ast.Name("air"),
					[
						ast.Constant(self.region_name),
						ast.Constant(self.form),
						ast.Constant(self.exit_name if self.is_exit else None),
					]
				))
			case _: pass
		if node.id in alias and node.id not in self.alias:
			self.alias.add(node.id)
			new_node = self.visit(self.expr(alias[node.id]))
			self.alias.remove(node.id)
			return new_node
		if node.id in tricks:
			trick = tricks[node.id]
			return self.simplify_BoolOp(ast.BoolOp(
				ast.And(),
				[
					ast.Call(ast.Name("trick"), [ast.Constant(trick[0])]),
					self.visit(self.expr(trick[1]))
				]
			))
		if node.id in items:
			if self.item_name_only: return ast.Constant(items[node.id])
			if node.id in progressives:
				return ast.Call(self.state("has"), [
					ast.Starred(ast.Subscript(ast.Name("items"), ast.Constant(items[node.id])))
				])
			return ast.Call(self.state("has"), [ast.Constant(items[node.id]), self.player, ast.Constant(1)])
		if node.id in events:
			return ast.Call(self.state("has"), [ast.Constant(events[node.id]), self.player, ast.Constant(1)])
		return ast.Call(ast.Name("option"), [ast.Constant(node.id)])

	def validate_count(self, node: ast.Call):
		node.keywords = []
		assert len(node.args) == 1, f"{self.file}: count requires exactly 1 argument."
		self.item_name_only += 1
		item = self.visit(node.args[0])
		self.item_name_only -= 1
		node.func = self.state("count")
		node.args = [item, self.player]
		return node

	def validate_forms_reach(self, node: ast.Call):
		node.keywords = []
		assert len(node.args) == 2, f"{self.file}: forms_reach requires exactly 2 arguments."
		assert isinstance(node.args[0], ast.Set), f"{self.file}: forms_reach requires arg 1 to be a set."
		for arg in node.args[0].elts:
			assert (
				isinstance(arg, ast.Constant)
				and isinstance(arg.value, str)
			), f"{self.file}: forms_reach requires set to contain only str."
			if self.is_exit:
				self.exit.indirect_starts.add(arg.value) # pyright: ignore[reportArgumentType]
		node.args[0] = ast.Call(ast.Name("frozenset"), [node.args[0]])
		assert (
			isinstance(node.args[1], ast.Constant)
			and isinstance(node.args[1].value, str)
		), f"{self.file}: forms_reach requires arg 2 to be a str."
		node.args += [ast.Name(id="state", ctx=ast.Load()), self.player]
		return node

	def validate_can_form_from_region_reach(self, node: ast.Call):
		node.keywords = []
		assert len(node.args) == 3, f"{self.file}: can_form_from_region_reach requires exactly 3 arguments."
		for i, arg in enumerate(node.args[0:2]):
			assert (
				isinstance(arg, ast.Constant)
				and isinstance(arg.value, str)
			), f"{self.file}: can_form_from_region_reach requires arg {i+1} to be a string."
			if i == 0: form: Form = arg.value # pyright: ignore[reportAssignmentType]
			elif i == 1 and self.is_exit: self.exit.indirect_extras.add((form, arg.value)) # pyright: ignore[reportPossiblyUnboundVariable]
		arg = node.args[2]
		assert (
			isinstance(arg, ast.Constant) and isinstance(arg.value, str)
			or isinstance(arg, ast.List)
		), f"{self.file}: can_form_from_region_reach requires arg 3 to be a string or list of strings."
		if isinstance(arg, ast.List):
			for elt in arg.elts:
				assert (
					isinstance(elt, ast.Constant) and isinstance(elt.value, str)
				), f"{self.file}: can_form_from_region_reach requires arg 3 to be a string or list of strings."
		node.args += [ast.Name(id="state", ctx=ast.Load()), self.player]
		return node

	def validate_forms_reach_regions(self, node: ast.Call):
		node.keywords = []
		assert len(node.args) == 1, f"{self.file}: forms_reach_regions requires exactly 1 argument."
		arg = node.args[0]
		assert isinstance(arg, ast.Dict), f"{self.file}: forms_reach_regions requires arg 1 to be a dict[str, str]."
		for i, key in enumerate(arg.keys):
			value = arg.values[i]
			assert (
				isinstance(key, ast.Constant) and isinstance(key.value, str)
				and isinstance(value, ast.Constant) and isinstance(value.value, str)
			), f"{self.file}: forms_reach_regions requires arg 1 to be a dict[str, str]."
			if self.is_exit:
				self.exit.indirect_starts.add(key.value) # pyright: ignore[reportArgumentType]
		node.args += [ast.Name(id="state", ctx=ast.Load()), self.player]
		return node

	def validate_can_form_reach(self, node: ast.Call):
		node.keywords = []
		assert len(node.args) == 2, f"{self.file}: can_form_reach requires exactly 2 arguments."
		for i, arg in enumerate(node.args[0:2]):
			assert (
				isinstance(arg, ast.Constant)
				and isinstance(arg.value, str)
			), f"{self.file}: can_form_reach requires arg {i+1} to be a string."
			if i == 0: form: Form = arg.value # pyright: ignore[reportAssignmentType]
			elif i == 1 and self.is_exit: self.exit.indirect_extras.add((form, arg.value)) # pyright: ignore[reportPossiblyUnboundVariable]
		node.args += [ast.Name(id="state", ctx=ast.Load()), self.player]
		return node

	def validate_air(self, node: ast.Call):
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
		node.args += [ast.Name(id="state", ctx=ast.Load()), Parser.player]
		return node

	def visit_Call(self, node: ast.Call):
		match ast.unparse(node.func):
			case "count": return self.validate_count(node)
			case "forms_reach": return self.validate_forms_reach(node)
			case "can_form_from_region_reach": return self.validate_can_form_from_region_reach(node)
			case "forms_reach_regions": return self.validate_forms_reach_regions(node)
			case "can_form_reach": return self.validate_can_form_reach(node)
			case "air": return self.validate_air(node)
			case _: raise TypeError(f"'{ast.unparse(node)}' is not a valid callable\nFile: {self.file}")
