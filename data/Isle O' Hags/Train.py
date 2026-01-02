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
			"GGM: Defeated Chuffy": {
                "logic": {
                    "Banjo-Kazooie": """
						EggUse and (BlueEggs or GrenadeEggs or IceEggs)
                        or ExtraAttacks and (Roll or BeakBarge or GroundRatatatRap)
					"""
				}
			},
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
            
			
			"GGM: Old King Coal Jiggy": {
				"item": "Jiggy",
				"logic": "GGMDefeatedChuffy",
			},
		},
        "exits": {
            "Chuffy's Cab": {}
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
			"Train At GGM": {},
			"Train At WW": {"logic": "WWTrainStation"},
			"Train At IoH": {"logic": "IoHTrainStation"},
			"Train At TDL": {"logic": "TDLTrainStation"},
			"Train At GI": {"logic": "GITrainStation"},
			"Train At HFP Lava Side": {"logic": "HFPLavaSideTrainStation"},
			"Train At HFP Icy Side": {"logic": "GITrainStation"},
		}
	},
	"Train At GI": {"macro": {"event"}},
    "Train At GGM": {"macro": {"event"}},
    "Train At WW": {"macro": {"event"}},
    "Train At IoH": {"macro": {"event"}},
    "Train At TDL": {"macro": {"event"}},
    "Train At HFP Lava Side": {"macro": {"event"}},
    "Train At HFP Icy Side": {"macro": {"event"}},
}
