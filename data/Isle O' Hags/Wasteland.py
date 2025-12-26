from .. import Regions
regions: Regions = {
	"Wasteland": {
		"id": 0x015A,
		"locations": {
			"IoH: Wasteland Jinjo": {
				"item": "PurpleJinjo",
			},
			"IoH: Clockwork Silo Bottom Note": {
				"item": "NoteNest",
			},
			"IoH: Clockwork Silo Top Note": {
				"item": "NoteNest",
			},
			"IoH: Wasteland CCL Area Note 1": {
				"item": "NoteNest",
			},
			"IoH: Wasteland CCL Area Note 2": {
				"item": "NoteNest",
			},
			"IoH: Clockwork Kazooie Eggs Silo": {
				"item": "ClockworkKazooieEggs",
			},
			"IoH: Wasteland Next to Quagmire Entrance Feather Nest": {
				"item": "FeatherNest",
			},
			"IoH: Wasteland TDL Entrance Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Wasteland TDL Entrance Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Wasteland Behind CCL Bubble Feather Nest": {
				"item": "FeatherNest",
			},
			"IoH: Wasteland Near Crevice to CCL Feather Nest": {
				"item": "FeatherNest",
			},
			"IoH: Wasteland Near Digger Tunnel Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Wasteland Near Digger Tunnel Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Wasteland Near Digger Tunnel Egg Nest 3": {
				"item": "EggNest",
			},
			"IoH: Wasteland Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Wasteland Silo Tagged": {
				"item": "WastelandWarpSilo",
			},
		},
		"exits": {
			"Quagmire": {},
			"Another Digger Tunnel": {},
			"Terrydactyland": {
				"id": 0x17,
				"logic": "Terrydactyland",
				"groups": {"World Entrances"},
			},
			"Cloud Cuckooland": {
				"id": 0x14,
				"logic": "CloudCuckooland",
				"groups": {"World Entrances"},
			},
			"Warp Silos": {},
		},
	},
}
