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

import re, os, pkgutil, importlib, zipimport, inspect, pathlib
from collections import deque
from importlib.machinery import FileFinder
from types import CodeType
from typing import cast, get_args

from . import groups, item_info, tricks, progressives, alias, parser
items_file = inspect.getsourcefile(item_info)
from .types import ExplicitForm, FinalExit, FinalLocation, FinalRegion, Form, Macros, NormalForm, Region
from .region_names import RegionName
from .forms import FormsReachBlocked, FormsReachTrack, FreeStateChange, InstantTransform

Regions = types.Regions
tricks = tricks.tricks
progressives = progressives.progressives
alias = alias.alias
item_name = parser.item_name

regions: dict[str, FinalRegion] = {}
location_groups: dict[str, set[str]] = {}
item_groups = groups.items
ast_items: dict[str, tuple[CodeType, dict[item_info.Classifiction, CodeType]]] = {}
ast_tricks: dict[str, CodeType] = {}
world_path = pathlib.Path(__file__).parents[2]
normal_forms: tuple[NormalForm, ...] = get_args(NormalForm)
explicit_forms: tuple[ExplicitForm, ...] = get_args(ExplicitForm)
all_forms = normal_forms + explicit_forms
form_start_regions: set[str] = set()
if items_file: items_file = pathlib.Path(items_file).relative_to(world_path)
else: items_file = "items.py"
class names:
	regions = set[str]()
	locations = set[str]()

def option_name(value: str) -> str:
	value = re.sub("['\"]+", "", value)
	return re.sub("[^a-zA-Z0-9_]+", "_", value).lower()

def form_name(form: Form, name: str) -> str:
	if form == "Any" or form == normal_forms[0]: return name
	return f"{name} - {form}"

def add_region(major_region: str, module_name: str) -> None:
	module = importlib.import_module(module_name, __name__)
	file = inspect.getsourcefile(module)
	if file: file = str(pathlib.Path(file).relative_to(world_path))
	else: file = major_region
	default_id: int = getattr(module, "default_id", 0)
	instant_transform: set[Form] = getattr(module, "instant_transform", set())

	for region_name, region in cast(dict[RegionName, Region], module.regions).items():
		assert region_name, f"{file}: Region names cannot be blank."
		assert region_name not in names.regions, f"{file}, {region_name}: Region names must be unique."
		names.regions.add(region_name)
		final_region = regions.setdefault(region_name, FinalRegion(
			major_region=major_region,
			file=file,
			id=region.get("id", default_id),
			instant_transform=region.get("instant_transform", instant_transform),
			underwater=region.get("underwater", False)
		))

		for location_name, location in region.get("locations", {}).items():
			assert location_name, f"{file}, {region_name}: Location names cannot be blank."
			assert location_name not in names.locations, f"{file}, {region_name}, {location_name}: Location names must be unique."
			names.locations.add(location_name)
			final_location = final_region.locations.setdefault(location_name, FinalLocation(
				groups=location.get("groups", set[str]()),
				enabled=location.get("enabled", ""),
				locked=location.get("locked", "false"),
				force_event=location.get("force_event", "false")
			))
			final_location.groups.add(major_region)

			location_item = location.get("item")
			if location_item is None:
				parser.events[item_name(location_name)] = location_name
			else:
				if type(location_item) is str: final_location.item = {location_item:""}
				elif type(location_item) is dict: final_location.item = location_item

			if final_location.item:
				item_groups: set[str] = set()
				item_names = set(final_location.item)
				for item in item_names:
					for group_name, items in groups.items.items():
						if item in items: item_groups.add(group_name)
				for item in item_names:
					for group_name, name in groups.locations.items():
						if name in item_groups or name == item: final_location.groups.add(group_name)
			if major_region != "Menu":
				for group_name in final_location.groups:
					location_groups.setdefault(group_name, set()).add(location_name)

			logic = location.get("logic", "")
			if isinstance(logic, str): final_location.logic = {"Any":logic}
			elif isinstance(logic, set): final_location.logic = {form:"" for form in logic}
			else: final_location.logic = logic

			explicit_logic = location.get("explicit_logic")
			if explicit_logic:
				assert "Any" not in explicit_logic, f"{file}, {region_name}, {location_name}: You can't use `Any` with explicit_logic"
				if isinstance(explicit_logic, set):
					for form in explicit_logic:
						final_location.logic[form] = ""
				else:
					for form, logic in explicit_logic.items():
						final_location.logic[form] = logic

		for exit_name, exit_ in region.get("exits", {}).items():
			final_exit = final_region.exits.setdefault(exit_name, FinalExit(
				id=exit_.get("id"),
				groups=exit_.get("groups", set[str]()),
				air=exit_.get("air", {})
			))

			if "id" in exit_ and "groups" not in exit_:
				final_exit.groups.add(f"{major_region} Exits")

			logic = exit_.get("logic", "")
			if isinstance(logic, str): final_exit.logic = {"Any":{"Any":logic}}
			elif isinstance(logic, set): final_exit.logic = {form:{form:""} for form in logic}
			else:
				for key, value in logic.items():
					if isinstance(value, str): final_exit.logic[key] = {key:value}
					else:
						assert "Any" != key, f"{file}: {region_name} -> {exit_name} -> {key}: You can't transform from `Any`"
						assert "Any" not in value, f"{file}: {region_name} -> {exit_name} -> {key}: You can't transform into `Any`"
						if isinstance(value, set): final_exit.logic[key] = {form:"" for form in value}
						else: final_exit.logic[key] = value

			explicit_logic = exit_.get("explicit_logic")
			if explicit_logic:
				assert "Any" not in explicit_logic, f"{file}, {region_name}, {exit_name}: You can't use `Any` with explicit_logic"
				if isinstance(explicit_logic, set):
					for form in explicit_logic:
						final_exit.logic.setdefault(form, {})[form] = ""
				else:
					for form, logic in explicit_logic.items():
						final_exit.logic.setdefault(form, {})[form] = logic

		for macro in region.get("macro", cast(Macros, set())):
			match macro:
				case "event":
					final_region.locations = {
						region_name: FinalLocation(logic={"Any":""})
					}
					final_region.exits = {}
					final_region.event = True
					parser.events[item_name(region_name)] = region_name
				case "splitup" | "rejoin":
					final_exit = final_region.exits.setdefault(region_name, FinalExit())
					if macro == "splitup":
						logic = final_exit.logic.setdefault("Banjo-Kazooie", {})
						logic["Banjo"] = "SplitUp"
						logic["Kazooie"] = "SplitUp"
					for form in ("Banjo", "Kazooie"):
						logic = final_exit.logic.setdefault(form, {})
						logic["Banjo-Kazooie"] = f"forms_reach({{'Banjo', 'Kazooie'}}, '{region_name.replace("'", "\\'")}')"

		for exit_name, exit_ in final_region.exits.items():
			for from_form, to_forms in FormsReachBlocked.items():
				if from_form not in exit_.logic: continue
				for to_form in to_forms:
					if to_form in exit_.logic[from_form]:
						logic = exit_.logic[from_form][to_form]
						if logic: logic = f" and ({logic})"
						exit_.logic[from_form][to_form] = f"not TransformBlock{logic}"

			for from_form, to_forms in FormsReachTrack.items():
				if from_form not in exit_.logic: continue
				for to_form in to_forms:
					if to_form in exit_.logic[from_form]:
						form_start_regions.add(exit_name)

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

def propagate_forms():
	any_form: set[Form] = {"Any"}
	explicits = set(explicit_forms)
	forms: dict[str, set[Form]] = {"Menu": {normal_forms[0]}}
	queue = deque(["Menu"])
	inaccessible_regions = set(regions) - {"Extra Items", "Starting Inventory", "Starting Inventory From Pool"}
	unused_explicit_forms: dict[str, set[Form]] = {}

	while queue:
		region_name = queue.popleft()
		inaccessible_regions.discard(region_name)
		region = regions[region_name]
		if region.event: continue
		all_region_forms = forms[region_name]
		region_forms = all_region_forms - explicits
		region_unused_explicit_forms = all_region_forms - region_forms
		changed = False

		for location in region.locations.values():
			location_forms = set(location.logic) - explicits - any_form
			location_explicit_forms = set(location.logic) - any_form
			all_region_forms |= location_explicit_forms
			region_unused_explicit_forms -= location_explicit_forms

			if "Any" in location.logic:
				for form in region_forms - location_forms:
					location.logic[form] = location.logic["Any"]

			if location_forms - region_forms:
				changed = True
				region_forms |= location_forms

		for exit_ in region.exits.values():
			exit_forms = set(exit_.logic) - explicits - any_form
			exit_explicit_forms = set(exit_.logic) - any_form
			all_region_forms |= exit_explicit_forms
			region_unused_explicit_forms -= exit_explicit_forms

			if "Any" in exit_.logic:
				for form in region_forms:
					exit_.logic.setdefault(form, {})
					if form not in exit_.logic[form]:
						exit_.logic[form][form] = exit_.logic["Any"]["Any"]

			if exit_forms - region_forms:
				changed = True
				region_forms |= exit_forms

		exit_ = region.exits.get(region_name, FinalExit())
		added = False
		for from_form, to_forms in FreeStateChange.items():
			if from_form not in all_region_forms: continue
			region_unused_explicit_forms.discard(from_form)
			exit_.logic.setdefault(from_form, {})
			for to_form, logic in to_forms.items():
				if to_form not in exit_.logic[from_form]:
					added = True
					exit_.logic[from_form][to_form] = logic

		base_form = normal_forms[0]
		transform_items = InstantTransform.get(region.major_region, {})
		for form in region.instant_transform:
			if base_form not in region_forms and form not in region_forms or form not in transform_items: continue
			region_unused_explicit_forms -= {base_form, form}
			exit_.logic.setdefault(base_form, {})
			exit_.logic.setdefault(form, {})

			if base_form not in exit_.logic[form]:
				added = True
				exit_.logic[form][base_form] = "InstantTransformTrick"

			if form not in exit_.logic[base_form]:
				added = True
				exit_.logic[base_form][form] = f"""
					InstantTransformTrick and (
						InstantTransform == "logic" and {transform_items[form]}
						or InstantTransform == "no_logic"
					)
				"""

		if region_unused_explicit_forms: unused_explicit_forms[region_name] = region_unused_explicit_forms

		if added:
			changed = True
			region.exits[region_name] = exit_
			region_forms |= set(exit_.logic) - explicits - any_form

		if changed:
			all_region_forms |= region_forms
			queue.append(region_name)

		for exit_name, exit_ in region.exits.items():
			assert exit_name in regions, f"{region.file}: {region_name} -> {exit_name}: Exit doesn't exist"
			exit_forms = set[Form]()
			for to_forms in exit_.logic.values():
				exit_forms |= set(to_forms) - any_form
			forms.setdefault(exit_name, set())
			if changed or exit_name in inaccessible_regions or exit_forms - forms[exit_name]:
				forms[exit_name] |= exit_forms
				if exit_name not in queue:
					queue.append(exit_name)

	for region_name, region_forms in forms.items():
		region = regions[region_name]
		if region.event:
			region.names["Any"] = region_name
		else:
			for form in region_forms:
				region.names[form] = form_name(form, region_name)

	if inaccessible_regions:
		print("Warning: The following region(s) seem to be inaccessible:")
		print("\n".join(sorted(inaccessible_regions)))

	for region_name, region_explicit_forms in unused_explicit_forms.items():
		print(f"Warning: The following explicit forms have a dead end in {region_name} ({regions[region_name].file})")
		print("\n".join(sorted(region_explicit_forms)))
		print()
propagate_forms()

def post_processing():
	locations_without_logic = set[str]()
	logic_parser = parser.Parser()
	for enabled, items in item_info.items.items():
		for item, cls in items.items():
			ast_cls: dict[item_info.Classifiction, CodeType] = {}
			if isinstance(cls, dict):
				for new_cls, logic in cls.items():
					ast_cls[new_cls] = logic_parser.parse(logic, "items.py")
			else: ast_cls[cls] = parser.true
			ast_items[item] = (logic_parser.parse(enabled, "items.py"), ast_cls)

	if isinstance(tricks, dict):
		for preset_tricks in tricks.values():
			for trick in preset_tricks:
				ast_tricks[trick] = logic_parser.parse(item_name(trick), "tricks.py")

	for region_name, region in regions.copy().items():
		escaped_region_name = region_name.replace("'", "\\'")
		region.file = f"{region.file}: {region_name}"
		region_forms = set(region.names)
		logic_parser.file = region.file
		logic_parser.region_name = region_name

		logic_parser.is_exit = False
		for location_name, location in region.locations.items():
			location.file = f"{region.file} -> {location_name}"
			location.ast_enabled = logic_parser.parse(location.enabled, location.file)
			location.ast_force_event = logic_parser.parse(location.force_event, location.file)
			location.ast_locked = logic_parser.parse(location.locked, location.file)
			for item, logic in location.item.items():
				location.ast_item[item] = logic_parser.parse(logic, location.file)

		logic_parser.is_exit = True
		for exit_name, exit_ in region.exits.items():
			exit_.file = f"{region.file} -> {exit_name}"

		if region.event: continue

		if region.locations:
			locations_name = f"Locations | {region_name}"
			region_locations = FinalRegion(
				major_region=region.major_region,
				file=region.file,
				id=region.id,
				event=True,
				names={"Any":locations_name}
			)

			logic_parser.is_exit = False
			for location_name, location in region.locations.copy().items():
				if "Any" in location.logic:
					del location.logic["Any"]

				if len(location.logic) > 1:
					del region.locations[location_name]
					location_forms = set[Form]()
					combined_logic: list[str] = []
					if location.logic:
						for form, logic in location.logic.items():
							if logic: logic = f" and ({logic})"
							else: location_forms.add(form)
							combined_logic.append(f"can_form_reach('{form}', '{escaped_region_name}'){logic}")
					elif region.major_region != "Menu":
						locations_without_logic.add(location_name)
					if location_forms == region_forms:
						location.logic = {"Any":""}
					else:
						logic_parser.form = "Any"
						location.ast_logic = {"Any": logic_parser.parse(" or ".join(combined_logic), location.file)}
					region_locations.locations[location_name] = location
				else:
					for form, logic in location.logic.items():
						logic_parser.form = form
						location.ast_logic[form] = logic_parser.parse(logic, location.file)

			if region_locations.locations:
				regions[locations_name] = region_locations
				region.exits[locations_name] = FinalExit(logic={form:{form:""} for form in region.names}, file=region.file)

		logic_parser.is_exit = True
		for exit_name, exit_ in region.exits.items():
			logic_parser.exit = exit_
			logic_parser.exit_name = exit_name
			if "Any" in exit_.logic: del exit_.logic["Any"]
			for from_form, to_forms in exit_.logic.items():
				logic_parser.form = from_form
				if "Any" in to_forms: del to_forms["Any"]
				for to_form, logic in to_forms.items():
					logic = logic_parser.parse(logic, exit_.file)
					if logic_parser.create_exit_event:
						name = f"{region_name} To {exit_name} As {from_form}"
						item = item_name(name)
						parser.events[item] = name
						region.locations[name] = FinalLocation(ast_logic={from_form:logic}, file=region.file)
						logic = logic_parser.parse(item_name(name), exit_.file)
					exit_.ast_logic.setdefault(from_form, {})[to_form] = logic

			if exit_.id is not None and not exit_.two_way:
				to_region = regions[exit_name]
				if region_name in to_region.exits:
					to_exit = to_region.exits[region_name]
					if to_exit.id is not None:
						exit_.two_way = True
						to_exit.two_way = True

	if len(locations_without_logic):
		print("Warning: The following location(s) don't have any form/logic info:")
		print("\n".join(sorted(locations_without_logic)))
		print()

	parser.item_names.update(parser.events)
	parser.item_names.update(parser.items)
post_processing()
