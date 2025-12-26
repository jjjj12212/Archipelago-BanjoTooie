from .. import Regions
regions: Regions = {
	"Chuffy's Cab": {
		"exits": {
			"GGM: Boss Room": {},
			"Train Stations": {"logic": "GGMDefeatedChuffy and Chuffy"},
			"GI Train Station": {"logic": "TrainAtGI"},
		}
	},
	"GGM: Boss Room": {
		"exits": {
			"Chuffy's Cab": {"logic": "GGMLevitateChuffyTheTrain"},
			"Inside Chuffy's Boiler": {},
		}
	},
	"Inside Chuffy's Boiler": {
		"locations": {
			"GGM: Defeated Chuffy": {},
			"GGM: Chuffy": {
				"item": "Chuffy",
				"logic": "GGMDefeatedChuffy",
			},
			"GGM: Old King Coal Mumbo Token": {
				"item": {"MumboToken":"'Old King Coal' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Old King Coal' in VictoryGoals",
				"locked": "true",
				"logic": "GGMDefeatedChuffy",
			},
		}
	},
	"Inside Chuffy's Wagon": {
		"locations": {
			"GGM: Inside Chuffy's Wagon Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		}
	},
	"Train Stations": {
		"exits": {
			"Train At GI": {"logic": "GITrainStation"},
		}
	},
	"Train At GI": {"macro": {"event"}},
}
