from .. import Regions
regions: Regions = {
	"Plateau": {
		"id": 0x0152,
		"locations": {
			"IoH: Plateau Jinjo": {
				"item": "BlueJinjo",
			},
			"IoH: Plateau Honeycomb": {
				"item": "EmptyHoneycomb",
			},
			"IoH: Plateau GGM Sign Note 1": {
				"item": "NoteNest",
			},
			"IoH: Plateau GGM Sign Note 2": {
				"item": "NoteNest",
			},
			"IoH: Plateau Honey B. Note 1": {
				"item": "NoteNest",
			},
			"IoH: Plateau Honey B. Note 2": {
				"item": "NoteNest",
			},
			"IoH: Fire Eggs Silo": {
				"item": "FireEggs",
			},
			"IoH: Honey B's Reward 1": {
				"item": "HealthUpgrade",
			},
			"IoH: Honey B's Reward 2": {
				"item": "HealthUpgrade",
			},
			"IoH: Honey B's Reward 3": {
				"item": "HealthUpgrade",
			},
			"IoH: Honey B's Reward 4": {
				"item": "HealthUpgrade",
			},
			"IoH: Honey B's Reward 5": {
				"item": "HealthUpgrade",
			},
			"IoH: Plateau Near GGM Entrance Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Plateau Near GGM Entrance Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Plateau Near Cliff Top Entrance Feather Nest": {
				"item": "FeatherNest",
			},
			"IoH: Plateau Near GGM Entrance Egg Nest 3": {
				"item": "EggNest",
			},
			"IoH: Plateau Near GGM Entrance Egg Nest 4": {
				"item": "EggNest",
			},
			"IoH: Plateau Dirt Pile Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Plateau Dirt Pile Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Plateau Silo Tagged": {
				"item": "PlateauWarpSilo",
			},
		},
		"exits": {
			"Wooded Hollow": {},
			"Cliff Top": {},
			"Pine Grove": {},
			"Glitter Gulch Mine": {
				"id": 0x11,
				"logic": "GlitterGulchMine",
				"groups": {"World Entrances"},
			},
			"Warp Silos": {},
		},
	},
}
