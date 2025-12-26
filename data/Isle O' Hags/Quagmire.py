from .. import Regions
regions: Regions = {
	"Quagmire": {
		"id": 0x015C,
		"locations": {
			"IoH: Quagmire Left Feather Nest": {
				"item": "FeatherNest",
			},
			"IoH: Quagmire Back Feather Nest": {
				"item": "FeatherNest",
			},
			"IoH: Quagmire High Feather Nest": {
				"item": "FeatherNest",
			},
			"IoH: Quagmire Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Quagmire Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Quagmire Egg Nest 3": {
				"item": "EggNest",
			},
			"IoH: Quagmire Silo Tagged": {
				"item": "QuagmireWarpSilo",
			},
		},
		"exits": {
			"Wasteland": {},
			"Grunty Industries": {
				"id": 0x09,
				"logic": "GruntyIndustries",
				"groups": {"World Entrances"},
			},
			"Cauldron Keep": {
				"id": 0x01,
				"logic": "CauldronKeep",
				"groups": {"World Entrances"},
			},
			"Warp Silos": {},
		},
	},
}
