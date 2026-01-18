from types import CodeType
from typing import TypedDict, NotRequired, Literal
from dataclasses import dataclass, field
from .region_names import RegionName
from .forms import *
from . import parser

class Location(TypedDict):
	"""
		A location.
	"""

	groups: NotRequired[set[str]]
	"""
		set[str]:
			Specifies the custom groups this location is part of.

		Not specified:
			This location won't be part of any custom groups.
	"""

	item: NotRequired[str | dict[str, str]]
	"""
		str:
			Specifies the vanilla item for this location

		dict[str, str]:
			DictKey specifies the vanilla item for this location, if DictValue evaluates to True using logic parsing.
			The first DictValue that returns True is used, the rest are ignored.
			Logic parsing only has the context of slot options.

		Not specified:
			This location is an event. An event item with the same name as the location will be placed here.
	"""

	enabled: NotRequired[str]
	"""
		str:
			Specifies the logic for whether this location will exist at all.
			Logic parsing only has the context of slot options.

		Not specified:
			This location will exist as either a real location or an event.
	"""

	locked: NotRequired[str]
	"""
		str:
			Specifies the logic for whether the location's vanilla item will be placed at this location.
			Has no affect if the location ends up as an event.
			Logic parsing only has the context of slot options.

		Not specified:
			This location will exist as either a real location or an event.
	"""

	force_event: NotRequired[str]
	"""
		str:
			Specifies the logic for whether the location will be forced as an event.
			The location can still end up as an event if this evaluates to false.
			Logic parsing only has the context of slot options.

		Not specified:
			This location will be an event if its item is not shuffled.
	"""

	logic: NotRequired[dict[Form, str] | set[Form] | str]
	"""
		dict[Form, str]
			Only forms specified by DictKey can access this location.
			DictValue is the logic for this location for the form.

		set[Form]
			Specifies which forms can freely access this location.

		str
			Specifies the logic for all normal forms that this region exists as.

		Not specified:
			This logic will evaluate to True for all normal forms that this region exists as.
	"""

	explicit_logic: NotRequired[dict[Form, str] | set[Form]]
	"""
		Forms added here will replace any in `logic` for this location.
		Useful for allowing a form to access the location, while not needing to specify every other form.

		dict[Form, str]
			DictValue specifies the logic for form DictKey for this location.

		set[Form]
			Specifies which forms can freely access this location.
	"""



class Exit(TypedDict):
	"""
		An exit to another region.
	"""

	id: NotRequired[int]
	"""
		int:
			Specifies the in game entrance id that this exit leads to.
			Should be formatted in hexidecimal with 2 digits.

		Not specified:
			This exit won't be considered a real in-game exit.
	"""

	two_way: NotRequired[bool]
	"""
		Automatically set.

		True:
			Exit is considered a two way exit.

		Not specified:
			if `id` is specified, this exit is considered a one way exit.
	"""

	groups: NotRequired[set[str]]
	"""
		set[str]:
			Specifies the custom groups this exit is part of.

		Not specified:
			This exit won't be part of any custom groups.
	"""

	air: NotRequired[dict[Form, tuple[float, ...]]]
	"""
		Specifies the amount of air used to go through this exit.

		DictKey:
			The form going through this exit.

		DictValue:
			Tuple[0]:
				The amount of air used to go through this exit without Fast Swimming.

			Tuple[1]
				The amount of air used to go through this exit with Fast Swimming.

			Tuple[2]
				The amount of air used to go through this exit with Rhythmic Swimming.
	"""

	logic: NotRequired[dict[Form, str | dict[Form, str] | set[Form]] | set[Form] | str]
	"""
		dict[Form, str | dict[Form, str] | set[Form]]:
			DictKey:
				Only forms specified can access this exit.

			DictValue:
				str
					The logic for this exit for the form.

				dict[Form, str]
					Specifies transformation exit(s). DictValue is the logic for the transformation to DictKey.

				set[Form]
					Specifies transformation exit(s) that can be freely accessed.

		set[Form]
			Specifies which forms can freely access this exit.

		str
			Specifies the logic for all normal forms that this region exists as.

		Not specified:
			This logic will evaluate to True for all normal forms that this region exists as.
	"""

	explicit_logic: NotRequired[dict[Form, str] | set[Form]]
	"""
		Forms added here will replace any in `logic` for this exit.
		Useful for allowing a form to access the exit, while not needing to specify every other form.

		dict[Form, str]
			DictValue specifies the logic for form DictKey for this exit.

		set[Form]
			Specifies which forms can freely access this exit.
	"""

Macros = set[Literal["event", "splitup", "rejoin"]]

class Region(TypedDict):
	"""
		A region. Must be unique within all logic files.
	"""

	id: NotRequired[int]
	"""
		int:
			Specifies the in game map id for this region.
			Should be formatted in hexidecimal with 4 digits.

		Not specified:
			Will be filled in using "default_id" if defined.
			All regions should have an id specified in some way.
	"""

	macro: NotRequired[Macros]
	"""
		Allows adding macros for easier logic building.

		"event"
			Inserts a blank location with the same name as the region, creating an event.

		"splitup"
			Macro for adding splitup logic to region.

		"rejoin"
			Macro for adding rejoin logic to region.

		Not specified:
			No changes.
	"""

	instant_transform: NotRequired[set[Form]]
	"""
		Specifies which forms can freely swap with the main form.
		Transformation exits will be automatically added.
	"""

	underwater: NotRequired[bool]
	"""
		Specifies that this region is underwater.
	"""

	locations: NotRequired[dict[str, Location]]
	"""
		A dictionary containing locations in this region.
		The key is the name of a location.
	"""

	exits: NotRequired[dict[RegionName, Exit]]
	"""
		A dictionary containing exits in this region.
		DictKey is the name of a region that this region can exit to.
		If the Exit contains an id, this will be considered a real in-game exit.
	"""

Regions = dict[str, Region]

@dataclass
class FinalLocation():

	groups: set[str] = field(default_factory=set[str])
	"""
		Specifies the custom groups this location is part of.
	"""

	ast_item: dict[str, CodeType] = field(default_factory=dict[str, CodeType])
	item: dict[str, str] = field(default_factory=dict[str, str])
	"""
		DictKey specifies the vanilla item for this location, if DictValue evaluates to True using logic parsing.
		The first DictValue that returns True is used, the rest are ignored.
		Logic parsing only has the context of slot options.
	"""

	ast_enabled: CodeType = parser.true
	enabled: str = ""
	"""
		Specifies the logic for whether this location will exist at all.
		Logic parsing only has the context of slot options.
	"""

	ast_locked: CodeType = parser.false
	locked: str = "false"
	"""
		Specifies the logic for whether the location's vanilla item will be placed at this location.
		Has no affect if the location ends up as an event.
		Logic parsing only has the context of slot options.
	"""

	ast_force_event: CodeType = parser.false
	force_event: str = "false"
	"""
		Specifies the logic for whether the location will be forced as an event.
		The location can still end up as an event if this evaluates to false.
		Logic parsing only has the context of slot options.
	"""

	ast_logic: dict[Form, CodeType] = field(default_factory=dict[Form, CodeType])
	logic: dict[Form, str] = field(default_factory=dict[Form, str])
	"""
		Only forms specified by DictKey can access this location.
		DictValue is the logic for this location for the form.
	"""

	file: str = "Location"

@dataclass
class FinalExit():

	id: int | None = None
	"""
		int:
			Specifies the in game entrance id that this exit leads to.
			Should be formatted in hexidecimal with 2 digits.

		None:
			This exit won't be considered a real in-game exit.
	"""

	two_way: bool = False
	"""
		Automatically set.

		True:
			Exit is considered a two way exit.

		False:
			Exit is considered a one way exit.
	"""

	groups: set[str] = field(default_factory=set[str])
	"""
		Specifies the custom groups this exit is part of.
	"""

	air: dict[Form, tuple[float, ...]] = field(default_factory=dict[Form, tuple[float, ...]])
	"""
		Specifies the amount of air used to go through this exit.

		DictKey:
			The form going through this exit.

		DictValue:
			Tuple[0]:
				The amount of air used to go through this exit without Fast Swimming.

			Tuple[1]
				The amount of air used to go through this exit with Fast Swimming.

			Tuple[2]
				The amount of air used to go through this exit with Rhythmic Swimming.
	"""

	ast_logic: dict[Form, dict[Form, CodeType]] = field(default_factory=dict[Form, dict[Form, CodeType]])
	logic: dict[Form, dict[Form, str]] = field(default_factory=dict[Form, dict[Form, str]])
	"""
		DictKey:
			Only forms specified can access this exit.

		DictValue:
			Specifies transformation exit(s). DictValue is the logic for the transformation to DictKey.
	"""

	file: str = "Exit"

	indirect_starts: set[Form] = field(default_factory=set[Form])

	indirect_extras: set[tuple[Form, str]] = field(default_factory=set[tuple[Form, str]])

@dataclass
class FinalRegion():
	"""
		A parent region holding extra data.
	"""

	major_region: str
	"""
		Automatically set to the Major Region this belongs to.
	"""

	file: str
	"""
		Automatically set to the file path where this region is defined.
	"""

	id: int
	"""
		Specifies the in game map id for this region.
		Should be formatted in hexidecimal with 4 digits.
	"""

	names: dict[Form, str] = field(default_factory=dict[Form, str])

	event: bool = False
	"""
		Specifies that this region contains only location(s) with free access.
	"""

	locations: dict[str, FinalLocation] = field(default_factory=dict[str, FinalLocation])
	"""
		A dictionary containing locations in this region.
		The key is the name of a location.
	"""

	exits: dict[str, FinalExit] = field(default_factory=dict[str, FinalExit])
	"""
		A dictionary containing exits in this region.
		DictKey is the name of a region that this region can exit to.
		If the Exit contains an id, this will be considered a real in-game exit.
	"""

	instant_transform: set[Form] = field(default_factory=set[Form])
	"""
		Specifies which forms can freely swap with the main form.
		Transformation exits will be automatically added.
	"""

	underwater: bool = False
	"""
		Specifies that this region is underwater.
	"""
