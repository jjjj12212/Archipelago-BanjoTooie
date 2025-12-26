from .. import Regions
regions: Regions = {
	"Glitter Gulch Mine": {
		"id": 0x00C7,
		"exits": {
			"Plateau": {
				"id": 0x02,
				"groups":{"World Exits"},
			},
			"Glitter Gulch Mine - Temp": {},
		},
	},
	"Glitter Gulch Mine - Temp": {
		"locations": {
			"GGM: Water Storage Jinjo": {
				"item": "BrownJinjo",
			},
			"GGM: Jail Jinjo": {
				"item": "BlackJinjo",
			},
			"GGM: Toxic Gas Cave Jinjo": {
				"item": "BlueJinjo",
			},
			"GGM: Boulder Jinjo": {
				"item": "BlackJinjo",
			},
			"GGM: Mine Tracks Jinjo": {
				"item": "PurpleJinjo",
			},
			"GGM: Old King Coal Jiggy": {
				"item": "Jiggy",
			},
			"GGM: Canary Mary Jiggy": {
				"item": "Jiggy",
			},
			"GGM: Generator Cavern Jiggy": {
				"item": "Jiggy",
			},
			"GGM: Waterfall Cavern Jiggy": {
				"item": "Jiggy",
			},
			"GGM: Ordnance Storage Jiggy": {
				"item": "Jiggy",
			},
			"GGM: Dilberta Jiggy": {
				"item": "Jiggy",
			},
			"GGM: Crushing Shed Jiggy": {
				"item": "Jiggy",
			},
			"GGM: Waterfall Jiggy": {
				"item": "Jiggy",
			},
			"GGM: Power Hut Basement Jiggy": {
				"item": "Jiggy",
			},
			"GGM: Flooded Caves Jiggy": {
				"item": "Jiggy",
			},
			"GGM: Near Entrance Glowbo": {
				"item": "HumbaDetonator",
			},
			"GGM: Mine Entrance 2 Glowbo": {
				"item": "MumboLevitate",
			},
			"GGM: Toxic Gas Cave Honeycomb": {
				"item": "EmptyHoneycomb",
			},
			"GGM: Prospector Boulder Honeycomb": {
				"item": "EmptyHoneycomb",
			},
			"GGM: Train Station Honeycomb": {
				"item": "EmptyHoneycomb",
			},
			"GGM: Treble Clef": {
				"item": "TrebleClef",
			},
			"GGM: Canary Mary Cheato Page": {
				"item": "CheatoPage",
			},
			"GGM: Entrance Cheato Page": {
				"item": "CheatoPage",
			},
			"GGM: Water Storage Cheato Page": {
				"item": "CheatoPage",
			},
			"GGM: Hill by Crushing Shed Note 1": {
				"item": "NoteNest",
			},
			"GGM: Hill by Crushing Shed Note 2": {
				"item": "NoteNest",
			},
			"GGM: Hill by Crushing Shed Note 3": {
				"item": "NoteNest",
			},
			"GGM: Hill by Crushing Shed Note 4": {
				"item": "NoteNest",
			},
			"GGM: Near Prospector's Hut Bottom-Left Note": {
				"item": "NoteNest",
			},
			"GGM: Near Prospector's Hut Top-Left Note": {
				"item": "NoteNest",
			},
			"GGM: Near Prospector's Hut Top-Right Note": {
				"item": "NoteNest",
			},
			"GGM: Near Prospector's Hut Middle-Right Note": {
				"item": "NoteNest",
			},
			"GGM: Near Prospector's Hut Bottom-Right Note": {
				"item": "NoteNest",
			},
			"GGM: Outside Mumbo's Skull Left Note": {
				"item": "NoteNest",
			},
			"GGM: Outside Mumbo's Skull Bottom-Right Note": {
				"item": "NoteNest",
			},
			"GGM: Outside Mumbo's Skull Top-Right Note": {
				"item": "NoteNest",
			},
			"GGM: Fuel Depot Front-Left Note": {
				"item": "NoteNest",
			},
			"GGM: Fuel Depot Back-Left Note": {
				"item": "NoteNest",
			},
			"GGM: Fuel Depot Back-Right Note": {
				"item": "NoteNest",
			},
			"GGM: Fuel Depot Front-Right Note": {
				"item": "NoteNest",
			},
			"GGM: Bill Drill Silo": {
				"item": "BillDrill",
			},
			"GGM: Beak Bayonet Silo": {
				"item": "BeakBayonet",
			},
			"GGM: Crushing Shed Jiggy Chunk 1": {
				"item": "Nothing",
			},
			"GGM: Crushing Shed Jiggy Chunk 2": {
				"item": "Nothing",
			},
			"GGM: Crushing Shed Jiggy Chunk 3": {
				"item": "Nothing",
			},
			"GGM: Ordnance Storage Mumbo Token": {
				"item": {"MumboToken":"'Ordnance Storage' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Ordnance Storage' in VictoryGoals",
				"locked": "true",
			},
			"GGM: Outside Ordnance Storage Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Outside Ordnance Storage Egg Nest 2": {
				"item": "EggNest",
			},
			"GGM: Near Bill Drill Silo Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Near Bill Drill Silo Egg Nest 2": {
				"item": "EggNest",
			},
			"GGM: Fuel Depot Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Fuel Depot Egg Nest 2": {
				"item": "EggNest",
			},
			"GGM: Fuel Depot Egg Nest 3": {
				"item": "EggNest",
			},
			"GGM: Fuel Depot Feather Nest 1": {
				"item": "FeatherNest",
			},
			"GGM: Fuel Depot Feather Nest 2": {
				"item": "FeatherNest",
			},
			"GGM: Fuel Depot Feather Nest 3": {
				"item": "FeatherNest",
			},
			"GGM: Crushing Shed Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Crushing Shed Egg Nest 2": {
				"item": "EggNest",
			},
			"GGM: Flooded Caves Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Flooded Caves Egg Nest 2": {
				"item": "EggNest",
			},
			"GGM: Water Storage Jinjo Tank Egg Nest": {
				"item": "EggNest",
			},
			"GGM: Gloomy Caverns Near Power Hut Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Gloomy Caverns Near Power Hut Egg Nest 2": {
				"item": "EggNest",
			},
			"GGM: Gloomy Caverns Jail Cell Feather Nest": {
				"item": "FeatherNest",
			},
			"GGM: Gloomy Caverns Near Second Boulder Egg Nest": {
				"item": "EggNest",
			},
			"GGM: Generator Cavern Egg Nest": {
				"item": "EggNest",
			},
			"GGM: Power Hut Feather Nest": {
				"item": "FeatherNest",
			},
			"GGM: Train Station Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Train Station Egg Nest 2": {
				"item": "EggNest",
			},
			"GGM: Train Station Feather Nest 1": {
				"item": "FeatherNest",
			},
			"GGM: Train Station Feather Nest 2": {
				"item": "FeatherNest",
			},
			"GGM: Prospector's Hut Egg Nest": {
				"item": "EggNest",
			},
			"GGM: Mumbo's Skull Feather Nest 1": {
				"item": "FeatherNest",
			},
			"GGM: Mumbo's Skull Feather Nest 2": {
				"item": "FeatherNest",
			},
			"GGM: Mumbo's Skull Feather Nest 3": {
				"item": "FeatherNest",
			},
			"GGM: Toxic Gas Cave Egg Nest": {
				"item": "EggNest",
			},
			"GGM: Toxic Gas Cave Feather Nest": {
				"item": "FeatherNest",
			},
			"GGM: Canary Cave Front-Right Egg Nest": {
				"item": "EggNest",
			},
			"GGM: Canary Cave Back-Left Egg Nest": {
				"item": "EggNest",
			},
			"GGM: Canary Cave Front-Left Feather Nest": {
				"item": "FeatherNest",
			},
			"GGM: Canary Cave Back-Right Feather Nest": {
				"item": "FeatherNest",
			},
			"GGM: Ordnance Storage Lobby Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Ordnance Storage Lobby Egg Nest 2": {
				"item": "EggNest",
			},
			"GGM: Ordnance Storage Lobby Egg Nest 3": {
				"item": "EggNest",
			},
			"GGM: Gloomy Cavern Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"GGM: Generator Cavern Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"GGM: Toxic Gas Cave Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"GGM: World Entry and Exit Warp Pad Tagged": {
				"item": "GGMWorldEntryAndExitWarpPad",
			},
			"GGM: Outside Mumbo's Skull Warp Pad Tagged": {
				"item": "GGMOutsideMumbosSkullWarpPad",
			},
			"GGM: Inside Wumba's Wigwam Warp Pad Tagged": {
				"item": "GGMInsideWumbasWigwamWarpPad",
			},
			"GGM: Outside the Crushing Shed Warp Pad Tagged": {
				"item": "GGMOutsideTheCrushingShedWarpPad",
			},
			"GGM: Near the Train Station Warp Pad Tagged": {
				"item": "GGMNearTheTrainStationWarpPad",
			},
		},
		"exits": {
			"GGM: Levitate Chuffy The Train": {},
		},
	},
	"GGM: Levitate Chuffy The Train": {"macro": {"event"}},
}
