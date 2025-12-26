from .. import Regions
regions: Regions = {
	"Cliff Top": {
		"id": 0x0155,
		"locations": {
			"IoH: Cliff Top Jinjo": {
				"item": "PurpleJinjo",
			},
			"IoH: Cliff Top Glowbo": {
				"item": "MumboHeal",
			},
			"IoH: Train Switch": {
				"item": "IoHTrainStation",
			},
			"IoH: Outside HFP Note 1": {
				"item": "NoteNest",
			},
			"IoH: Outside HFP Note 2": {
				"item": "NoteNest",
			},
			"IoH: Outside HFP Note 3": {
				"item": "NoteNest",
			},
			"IoH: Outside HFP Note 4": {
				"item": "NoteNest",
			},
			"IoH: Ice Eggs Silo": {
				"item": "IceEggs",
			},
			"IoH: Cliff Top Near Path to Plateau Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Cliff Top Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Cliff Top Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Cliff Top Feather Nest 3": {
				"item": "FeatherNest",
			},
			"IoH: Cliff Top Feather Nest 4": {
				"item": "FeatherNest",
			},
			"IoH: Cliff Top Near Path to Plateau Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Cliff Top Near JRL Egg Nest": {
				"item": "EggNest",
			},
			"IoH: Cliff Top Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Cliff Top Silo Tagged": {
				"item": "CliffTopWarpSilo",
			},
		},
		"exits": {
			"Plateau": {},
			"Chuffy's Cab": {},
			"Jolly Roger's Lagoon": {
				"id": 0x03,
				"logic": "JollyRogersLagoon",
				"groups": {"World Entrances"},
			},
			"Hailfire Peaks": {
				"id": 0x15,
				"logic": "HailfirePeaks",
				"groups": {"World Entrances"},
			},
			"Warp Silos": {},
		},
	},
}
