"""
	File structure of this package:

	/__init__.py -- This file
	/items.py -- File containing all items and their information
	/Major Region/ -- Optional folder for "Major Region"
	/Major Region/__init__.py -- Required logic file. Can contain logic for "Major Region"
	/Major Region/AnyFileName.py -- Optional logic file. Should contain logic for "Major Region"
	/Major Region/AnyFolderName/ -- Optional sub-folder for "Major Region". Follows the same structure as parent folder.
	/Menu/__init__.py -- Required Major Region. Has special parsing properties.

	Logic files can use the following variable names:
		regions - defines region data.
		default_id - defines a default region id for regions defined in the same file.
		instant_transform - defines a default instant_transform set for regions defined in the same file.
	All locations within logic files will automatically be part of a group with the same name as "Major Region".
"""

import sys, re, os, pkgutil, importlib, zipimport, inspect, pathlib, ast
from importlib.machinery import FileFinder
from typing import cast, get_args


from . import groups, items
items_file = inspect.getsourcefile(items)
from .types import ExitLogic, ExplicitForm, FinalLocation, Form, NormalForm, ParentRegion, Location, Region
from .region_names import RegionName
from .items import items
from .forms import FormsReachBlocked, FormsReachTrack, FreeStateChange, InstantTransform
from .types import Regions # pyright: ignore[reportUnusedImport]
from .tricks import tricks # pyright: ignore[reportUnusedImport]
from .progressives import progressives # pyright: ignore[reportUnusedImport]
from .alias import alias # pyright: ignore[reportUnusedImport]

_regions: dict[RegionName, Region] = {}
regions: dict[str, ParentRegion] = {}
locations: dict[str, Location] = {}
item_groups: dict[str, set[str]] = groups.items
location_groups: dict[str, set[str]] = {}
world_path = pathlib.Path(__file__).parents[2]
normal_forms: tuple[NormalForm, ...] = get_args(NormalForm)
explicit_forms: tuple[ExplicitForm, ...] = get_args(ExplicitForm)
all_forms = normal_forms + explicit_forms
form_to_region_name: dict[str, str] = {}
form_start_regions: set[str] = set()
if items_file: items_file = pathlib.Path(items_file).relative_to(world_path)
else: items_file = "items.py"

def item_name(value: str) -> str:
	return re.sub("[^a-zA-Z0-9]+", "", value)

def option_name(value: str) -> str:
	value = re.sub("['\"]+", "", value)
	return re.sub("[^a-zA-Z0-9_]+", "_", value).lower()

def form_name(form: Form, name: str) -> str:
	if normal_forms[0] == form: return name
	return f"{name} - {form}"

def location_region_name(name: str) -> RegionName:
	return f"Location | {name}" # pyright: ignore[reportReturnType]

def add_region(major_region: str, module_name: str) -> None:
	module = importlib.import_module(module_name, __name__)
	if not hasattr(module, "regions"): return
	file = inspect.getsourcefile(module)
	if file: file = str(pathlib.Path(file).relative_to(world_path))
	else: file = major_region
	default_id = 0
	instant_transform: set[Form] = set()
	if hasattr(module, "default_id"): default_id = module.default_id
	if hasattr(module, "instant_transform"): instant_transform = module.instant_transform
	for region_name, region in cast(dict[RegionName, Region], module.regions).items():
		assert region_name, f"{file}: Region names cannot be blank."
		assert region_name not in _regions, f"{file}, {region_name}: Region names must be unique."
		if major_region == "Menu": region.setdefault("forms", set()).add(normal_forms[0])
		_regions[region_name] = region
		regions[region_name] = {
			"major_region": major_region,
			"file": file,
			"names": {}
		}
		if default_id and ("id" not in region or not region["id"]):
			region["id"] = default_id
		if instant_transform and "instant_transform" not in region:
			region["instant_transform"] = instant_transform
		macro = region.pop("macro", None)
		if macro:
			if "event" in macro:
				region.setdefault("locations", {})[region_name] = {}
			if "splitup" in macro:
				logic: ExitLogic = region.setdefault("exits", {}).setdefault(region_name, {}).setdefault("logic", {})
				assert isinstance(logic, dict), f"{file}, {region_name}, splitup: Existing logic must be type dict."
				for form in ("Banjo-Kazooie", "Banjo", "Kazooie"):
					if form not in logic:
						logic[form] = {}
				assert (
					isinstance(logic["Banjo-Kazooie"], dict)
					and isinstance(logic["Banjo"], dict)
					and isinstance(logic["Kazooie"], dict)
				), f"{file}, {region_name}, splitup: Existing logic for Banjo-Kazooie, Banjo and Kazooie must be type dict."
				logic["Banjo-Kazooie"]["Banjo"] = "SplitUp"
				logic["Banjo-Kazooie"]["Kazooie"] = "SplitUp"
				logic["Banjo"]["Banjo-Kazooie"] = f"forms_reach({{'Banjo', 'Kazooie'}}, '{region_name}')"
				logic["Kazooie"]["Banjo-Kazooie"] = f"forms_reach({{'Banjo', 'Kazooie'}}, '{region_name}')"
			elif "rejoin" in macro:
				logic: ExitLogic = region.setdefault("exits", {}).setdefault(region_name, {}).setdefault("logic", {})
				assert isinstance(logic, dict), f"{file}, {region_name}, splitup: Existing logic must be type dict."
				for form in ("Banjo", "Kazooie"):
					if form not in logic:
						logic[form] = {}
				assert (
					isinstance(logic["Banjo"], dict)
					and isinstance(logic["Kazooie"], dict)
				), f"{file}, {region_name}, splitup: Existing logic for Banjo and Kazooie must be type dict."
				logic["Banjo"]["Banjo-Kazooie"] = f"forms_reach({{'Banjo', 'Kazooie'}}, '{region_name}')"
				logic["Kazooie"]["Banjo-Kazooie"] = f"forms_reach({{'Banjo', 'Kazooie'}}, '{region_name}')"
		for location_name, location in region.get("locations", {}).items():
			assert location_name, f"{file}, {region_name}: Location names cannot be blank."
			assert location_name not in locations, f"{file}, {region_name}, {location_name}: Location names must be unique."
			locations[location_name] = location
			if "groups" not in location: location["groups"] = set()
			location["groups"].add(major_region)
			item_name = location.get("item")
			if item_name:
				item_groups: set[str] = set()
				item_names: set[str]
				if isinstance(item_name, dict): item_names = set(item_name)
				else: item_names = {item_name}
				for item in item_names:
					for group_name, items in groups.items.items():
						if item in items: item_groups.add(group_name)
				for item in item_names:
					for group_name, name in groups.locations.items():
						if name in item_groups or name == item: location["groups"].add(group_name)
			if major_region != "Menu":
				for group_name in location["groups"]:
					location_groups.setdefault(group_name, set()).add(location_name)
		for exit_ in region.get("exits", {}).values():
			if "id" in exit_ and "groups" not in exit_:
				exit_["groups"] = {f"{major_region} Exits"}

def build_regions():
	def scan_module(major_region: str, module_path: str, module: pkgutil.ModuleInfo):
		add_region(major_region, f"{module_path}.{module.name}")
		if isinstance(module.module_finder, FileFinder):
			path = module.module_finder.path
		elif isinstance(module.module_finder, zipimport.zipimporter):
			path = os.path.join(module.module_finder.archive, module.module_finder.prefix)
		else:
			raise Exception(f"Unknown path type: {module.module_finder}")
		for submodule in pkgutil.iter_modules([os.path.join(path, module.name)]):
			if submodule.ispkg:
				scan_module(major_region, f"{module_path}.{module.name}", submodule)
			else:
				add_region(major_region, f"{module_path}.{module.name}.{submodule.name}")

	for module in pkgutil.iter_modules(__path__):
		if module.ispkg:
			scan_module(module.name, "", module)
build_regions()

def reformat_logic_structure():
	_regions["Menu"].setdefault("forms", set()).add(normal_forms[0])
	check: set[RegionName] = set()
	for region_name, region in _regions.items():
		parent_region = regions[region_name]
		for exit_name, exit_ in region.get("exits", {}).items():
			assert exit_name in _regions, f"{parent_region["file"]}, {region_name}, {exit_name}: Exit doesn't exist."
		if "forms" not in region: region["forms"] = set()
		forms = region["forms"]
		for location in region.get("locations", {}).values():
			if "logic" not in location or isinstance(location["logic"], str): continue
			if "explicit_logic" in location: forms |= set(location["explicit_logic"])
			for form in location["logic"]:
				forms.add(form)
		for exit_ in region.get("exits", {}).values():
			if "logic" not in exit_ or isinstance(exit_["logic"], str): continue
			if "explicit_logic" in exit_: forms |= set(exit_["explicit_logic"])
			for form in exit_["logic"]:
				forms.add(form)
		if forms: check.add(region_name)
		else: del region["forms"]
	while len(check):
		region_name = check.pop()
		region = _regions[region_name]
		from_forms = region.get("forms", cast(set[Form], set()))
		for from_form, to_forms in FreeStateChange.items():
			if from_form in from_forms:
				from_forms |= set(to_forms)
		for exit_name, exit_ in region.get("exits", {}).items():
			exit_logic = exit_.get("logic")
			if not exit_logic or isinstance(exit_logic, str): forms = from_forms.copy()
			else: forms = set(exit_logic)
			forms -= set(explicit_forms)
			if exit_logic:
				if isinstance(exit_logic, dict):
					for form, value in exit_logic.items():
						if isinstance(value, dict) or isinstance(value, set):
							forms |= set(value)
						else: forms.add(form)
				elif isinstance(exit_logic, set):
					forms |= exit_logic
			to_forms = _regions[exit_name].setdefault("forms", set())
			if forms - to_forms:
				to_forms |= forms
				check.add(exit_name)
	for region_name, region in _regions.copy().items():
		parent_region = regions[region_name]
		names: dict[Form, str] = {}
		# assert "forms" in region and region["forms"], f"{region["file"]}, {region_name}: No forms can access this region."
		if "forms" not in region: continue # replace with above once logic is done
		forms = region["forms"] - set(explicit_forms)
		region_forms: set[Form] = set()
		for exit_name, exit_ in region.get("exits", {}).items():
			if "logic" in exit_:
				exit_logic = exit_["logic"]
				if isinstance(exit_logic, set):
					exit_["logic"] = {form:{form:""} for form in exit_logic}
				elif isinstance(exit_logic, str):
					exit_["logic"] = {form:{form:exit_logic} for form in forms}
				else:
					for form, value in exit_logic.items():
						if isinstance(value, str):
							exit_logic[form] = {form:value}
						elif isinstance(value, set):
							exit_logic[form] = {to_form:"" for to_form in value}
			else:
				exit_["logic"] = {form:{form:""} for form in forms}
			exit_logic = cast(dict[Form, dict[Form, str]], exit_["logic"])
			region_forms |= set(exit_logic)
			exit_logic_explicit = exit_.get("explicit_logic", {})
			if isinstance(exit_logic_explicit, set):
				exit_logic_explicit = cast(dict[ExplicitForm, str], {form:"" for form in exit_logic_explicit})
			for explicit_form, explicit_logic in exit_logic_explicit.items():
				if explicit_form not in exit_logic: exit_logic[explicit_form] = {}
				exit_logic[explicit_form][explicit_form] = explicit_logic
			for from_form, to_forms in FormsReachBlocked.items():
				if from_form not in exit_logic: continue
				for to_form in to_forms:
					if to_form in exit_logic[from_form]:
						logic = f" and ({exit_logic[from_form][to_form]})"
						exit_logic[from_form][to_form] = f"not TransformBlock{logic}"
			for from_form, to_forms in FormsReachTrack.items():
				if from_form not in exit_logic: continue
				for to_form in to_forms:
					if to_form in exit_logic[from_form]:
						form_start_regions.add(exit_name)
		exit_logic = cast(
			dict[Form, dict[Form, str]],
			region.setdefault("exits", {}).setdefault(region_name, {}).setdefault("logic", {})
		)
		for from_form, to_forms in FreeStateChange.items():
			if from_form not in region["forms"]: continue
			if from_form not in exit_logic: exit_logic[from_form] = {}
			for to_form, logic in to_forms.items():
				if to_form not in exit_logic[from_form]:
					exit_logic[from_form][to_form] = logic
					region_forms.add(to_form)
		base_form = normal_forms[0]
		transform_items = InstantTransform.get(parent_region["major_region"], {})
		for form in region.get("instant_transform", cast(set[Form], set())):
			if base_form not in region["forms"] and form not in region["forms"] or form not in transform_items: continue
			if base_form not in exit_logic: exit_logic[base_form] = {}
			if form not in exit_logic: exit_logic[form] = {}
			if base_form not in exit_logic[form]: exit_logic[form][base_form] = "InstantTransformTrick"
			if form not in exit_logic[base_form]:
				exit_logic[base_form][form] = f"""
					InstantTransformTrick and (
						InstantTransform == "logic" and {transform_items[form]}
						or InstantTransform == "no_logic"
					)
				"""
		if exit_logic: region_forms |= set(exit_logic)
		elif "exits" in region:
			del region["exits"][region_name]["logic"]
			if not region["exits"][region_name]:
				del region["exits"][region_name]
				if not region["exits"]: del region["exits"]
		for location_name, location in region.get("locations", {}).copy().items():
			if "logic" in location:
				location_logic = location["logic"]
				if isinstance(location_logic, set):
					location["logic"] = {form:"" for form in location_logic}
				elif isinstance(location_logic, str):
					location["logic"] = {form:location_logic for form in forms}
			else:
				location["logic"] = {form:"" for form in forms}
			location_logic = cast(dict[Form, str], location["logic"])
			location_logic_explicit = location.get("explicit_logic", {})
			if isinstance(location_logic_explicit, set):
				location_logic_explicit = cast(dict[ExplicitForm, str], {form:"" for form in location_logic_explicit})
			for explicit_form, explicit_logic in location_logic_explicit.items():
				location_logic[explicit_form] = explicit_logic
			if len(location_logic) > 1:
				location["logic"] = {"":""}
				if "locations" in region: del region["locations"][location_name]
				name = location_region_name(location_name)
				regions[name] = {
					"major_region": parent_region["major_region"],
					"file": parent_region["file"],
					"names": {"":name},
					"locations": {location_name:cast(FinalLocation, location)},
				}
				region.setdefault("exits", {})[name] = {
					"logic": {form:{form:logic} for form, logic in location_logic.items()}
				}
			region_forms |= set(location_logic)
		if "locations" in region and len(region["locations"]) == 0:
			del region["locations"]
		forms |= region_forms
		for form in forms:
			name = form_name(form, region_name)
			names[form] = name
			form_to_region_name[name] = region_name
		del region["forms"]
		parent_region["names"] = names
reformat_logic_structure()
for region_name, region in _regions.items():
	for key, value in region.items():
		regions[region_name][key] = value
del _regions

class BasicParser(ast.NodeTransformer):

	def parse(self, file: str, logic: str):
		if not logic: return logic
		ret = ast.unparse(self.visit(ast.parse(f"({logic})", file)))
		return sys.intern(ret)

def post_processing():
	parser = BasicParser()
	for region_name, region in regions.items():
		region_file = f"{region['file']}: {region_name}"
		for location_name, location in region.get("locations", {}).items():
			if "logic" in location:
				parser_str = f"{region_file} -> {location_name}"
				for form, logic in location["logic"].items():
					location["logic"][form] = parser.parse(f"{parser_str} -> logic", logic)
		for exit_name, exit_ in region.get("exits", {}).items():
			if "logic" in exit_:
				exit_names = regions[exit_name]["names"]
				location_exit = "" in exit_names
				for from_form, to_forms in exit_["logic"].items():
					for to_form, logic in to_forms.items():
						if location_exit: form_exit_name = exit_name
						else: form_exit_name = exit_names[to_form]
						parser_str = f"{region_file} -> {form_exit_name}"
						exit_["logic"][from_form][to_form] = parser.parse(f"{parser_str} -> logic", logic)
			if "id" in exit_ and "rid" not in exit_:
				to_region = regions[exit_name]
				if "exits" in to_region and region_name in to_region["exits"]:
					to_exit = to_region["exits"][region_name]
					if "id" in to_exit:
						exit_["rid"] = to_exit["id"]
						if "rid" not in to_exit: to_exit["rid"] = exit_["id"]
post_processing()
