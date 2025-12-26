

from typing import Literal

NormalForm = Literal[
	"Banjo-Kazooie",
	"Talon Trot",
	"Banjo",
	"Kazooie",
	"Mumbo",
	"Stony",
	"Detonator",
	"Van",
	"Sub",
	"Baby T-Rex",
	"Daddy T-Rex",
	"Washer",
	"Snowball",
	"Bee",
]
ExplicitForm = Literal[
	"Talon Torpedo",
	"BK Turbo Trainers",
	"BK Wading Boots",
	"BK Springy Step Shoes",
	"BK Claw Clamber Boots",
	"SK Turbo Trainers",
	"SK Wading Boots",
	"SK Springy Step Shoes",
	"SK Claw Clamber Boots",
	"Clockwork Kazooie",
	"Golden Goliath",
]
Form = NormalForm | ExplicitForm | Literal[""]
"""
	A list of possible forms in-game. A blank string is has special meaning and shouldn't be used in logic.
	This can be actual transformations, or even just different states the player can be in.

	Unless explicitly added, ExplicitForms will not be able to:
	* Collect locations
	* Take exits
	Used for forms that have restrictions in range or ability.

	When sending to Archipelago, form specific regions will have their form appended to the name.
	The first form in the list is exempt from this rule and is considered the "default" form.
"""

FormsReachBlocked: dict[Form, set[Form]] = {
	"Banjo": {"Banjo-Kazooie"},
	"Kazooie": {"Banjo-Kazooie"},
}
"""
	The logic parsing exposes this function: `forms_reach(forms: list[Form], region_name: str)`
	This checks if all provided forms can reach the provided region.
	Sometimes it is undesirable for certain transformations to occur during this check.
	You can block specific transformations by adding the following to the logic: `not TransformBlock`

	FormsReachBlocked allows specifying transformations to always add this logic for.
	It does this by modifying the existing logic to be: `not TransformBlock and (<old logic, if any>)`

	DictKey is the originating form, and DictValue is a list of forms to modify the logic for their transformation exit.
"""

FormsReachTrack: dict[Form, set[Form]] = {
	"Banjo-Kazooie": {"Banjo", "Kazooie"},
}
"""
	In order to for `forms_reach` to work, it needs to have a list of regions to start from.
	FormsReachTrack is a mapping of transformations to track.
	DictKey is the from form, and DictValue is a set of to forms.
	For every transformation from DictKey to a DictValue in logic, the region will be added to a list.
"""

FreeStateChange: dict[Form, dict[Form, str]] = {
	"Talon Trot": {
		"Banjo-Kazooie": "",
	},
	"BK Turbo Trainers": {
		"Banjo-Kazooie": "",
		"Talon Trot": "TalonTrotSmuggle",
	},
	"BK Wading Boots": {
		"Banjo-Kazooie": "",
	},
	"BK Springy Step Shoes": {
		"Banjo-Kazooie": "",
		"Talon Trot": "TalonTrotSmuggle",
	},
	"BK Claw Clamber Boots": {
		"Banjo-Kazooie": "",
		"Talon Trot": "TalonTrotSmuggle",
	},
	"SK Turbo Trainers": {
		"Kazooie": "",
	},
	"SK Wading Boots": {
		"Kazooie": "",
	},
	"SK Springy Step Shoes": {
		"Kazooie": "",
	},
	"SK Claw Clamber Boots": {
		"Kazooie": "",
	},
}
"""
	A mapping of free state changes, where a form can always change into another form at any point.
	Any region specific to DictKey's form will automatically have a transformation exit to DictValue's form.
	The str indicates the logic that will be added to the transformation exit, if not blank.
"""

InstantTransform: dict[str, dict[Form, str]] = {
	"Grunty Industries": {
		"Mumbo": "GIMumboTransform",
		"Washer": "GIWasherTransform"
	}
}
"""
	A mapping of event items for forms in each major region.
	The event items should be the event item collected when transforming manually.

	The event item is checked for when the option `InstantTransform` is set to `logic`.
"""
