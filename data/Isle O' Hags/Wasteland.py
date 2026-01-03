from .. import Regions
regions: Regions = {
	"IoH: Wasteland": {
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
			"IoH: Quagmire": {},
			"IoH: Another Digger Tunnel": {},
			"Terrydactyland": {
				"id": 0x17,
				"groups": {"World Entrances"},
				"logic": {
					"Banjo-Kazooie": "Terrydactyland",
					"Talon Trot": "Terrydactyland and TalonTrotSmuggleCrossWorld",
				}
			},
			"Cloud Cuckooland": {
				"id": 0x14,
				"groups": {"World Entrances"},
				"logic": {
					"Banjo-Kazooie": "CloudCuckooland",
					"Talon Trot": "CloudCuckooland and TalonTrotSmuggleCrossWorld",
				}
			},
			"IoH: Warp Silos": {},
		},
	},
	"IoH: Wasteland Ledge to Quagmire": {}
}
