from typing import TypedDict, NotRequired, Literal
from .region_names import RegionName
from .forms import *

class BaseLocation(TypedDict):
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

	item_rule: NotRequired[str]
	"""
		str:
			Specifies the logic for items allowed at this location.
			Logic parsing only has the context of slot options and the item to check against.

		Not specified:
			This location will always accept any item.
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

class Location(BaseLocation):

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

class FinalLocation(BaseLocation):

	logic: NotRequired[dict[Form, str]]
	"""
		dict[Form, str]
			Only forms specified by DictKey can access this location.
			DictValue is the logic for this location for the form.

		Not specified:
			This logic will evaluate to True for all normal forms that this region exists as.
	"""

class BaseExit(TypedDict):
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

	rid: NotRequired[int]
	"""
		Automatically populated if left blank.

		int:
			Specifies the in game entrance id that leads to this exit, making it a two way exit.
			Should be formatted in hexidecimal with 2 digits.

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

FinalExitLogic = dict[Form, dict[Form, str]]
ExitLogic = dict[Form, str | dict[Form, str] | set[Form]] | set[Form] | str

class Exit(BaseExit):

	logic: NotRequired[ExitLogic]
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

class FinalExit(BaseExit):

	logic: NotRequired[FinalExitLogic]
	"""
		dict[Form, dict[Form, str]]:
			DictKey:
				Only forms specified can access this exit.

			DictValue:
				Specifies transformation exit(s). DictValue is the logic for the transformation to DictKey.

		Not specified:
			This logic will evaluate to True for all normal forms that this region exists as.
	"""

class BaseRegion(TypedDict):
	"""
		Base region class. Used to separate typing requirements.
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

	forms: NotRequired[set[Form]]
	"""
		Specifies which form(s) this region exists as.
		Automatically populated with forms:
			* from any location/exit in this region
			* that can access this region from other regions
	"""

	macro: NotRequired[set[Literal["event", "splitup", "rejoin"]]]
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

class Region(BaseRegion):
	"""
		A region. Must be unique within all logic files.
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

class FinalRegion(BaseRegion):
	"""
		A region. Must be unique within all logic files.
	"""

	locations: NotRequired[dict[str, FinalLocation]]
	"""
		A dictionary containing locations in this region.
		The key is the name of a location.
	"""

	exits: NotRequired[dict[str, FinalExit]]
	"""
		A dictionary containing exits in this region.
		DictKey is the name of a region that this region can exit to.
		If the Exit contains an id, this will be considered a real in-game exit.
	"""


class ParentRegion(FinalRegion):
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

	names: dict[Form, str]
	"""
		Automatically populated with form specific names of this region.
	"""

Regions = dict[str, Region]
