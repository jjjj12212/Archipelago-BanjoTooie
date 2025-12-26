from .. import Regions
regions: Regions = {
	"Pine Grove": {
		"id": 0x0154,
		"locations": {
			"IoH: Pine Grove Note 1": {
				"item": "NoteNest",
			},
			"IoH: Pine Grove Note 2": {
				"item": "NoteNest",
			},
			"IoH: Pine Grove Underwater Note 1": {
				"item": "NoteNest",
			},
			"IoH: Pine Grove Underwater Note 2": {
				"item": "NoteNest",
			},
			"IoH: Grenade Eggs Silo": {
				"item": "GrenadeEggs",
			},
			"IoH: Wumba's Wigwam Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Wumba's Wigwam Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Pine Grove Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Pine Grove Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Pine Grove Feather Nest 3": {
				"item": "FeatherNest",
			},
			"IoH: Pine Grove Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Pine Grove Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Pine Grove Egg Nest 3": {
				"item": "EggNest",
			},
			"IoH: Pine Grove Signpost 1": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Pine Grove Signpost 2": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Pine Grove Signpost 3": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Pine Grove Silo Tagged": {
				"item": "PineGroveWarpSilo",
			},
			"IoH Dragon Transform": {"logic": "HumbaDragon"},
		},
		"exits": {
			"Another Digger Tunnel": {},
			"Plateau": {},
			"Witchyworld": {
				"id": 0x12,
				"logic": "Witchyworld",
				"groups": {"World Entrances"},
			},
			"Warp Silos": {},
		},
	},
}
