from .. import Regions
regions: Regions = {
	"Wooded Hollow": {
		"id": 0x014F,
		"locations": {
			"IoH: Wooded Hollow Jinjo": {
				"item": "BlueJinjo",
			},
			"IoH: Pink Mystery Egg Hatched": {
				"item": "BreegullBash",
			},
			"IoH: Blue Mystery Egg Hatched": {
				"item": "HomingEggs",
			},
			"IoH: Yellow Mystery Egg Hatched": {
				"item": "Nothing",
				"enabled": "not ShuffleStopNSwop",
			},
			"IoH: Wooded Hollow Outside Heggy's Egg Shed Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Wooded Hollow Outside Heggy's Egg Shed Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Wooded Hollow Left of Jiggywiggy's Temple Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Wooded Hollow Left of Jiggywiggy's Temple Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Wooded Hollow Left of Jiggywiggy's Temple Feather Nest 3": {
				"item": "FeatherNest",
			},
			"IoH: Wooded Hollow Right of Jiggywiggy's Temple Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Wooded Hollow Right of Jiggywiggy's Temple Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Wooded Hollow Outside Bottles' House Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Wooded Hollow Outside Bottles' House Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Outside Heggy's Egg Shed Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Behind Jiggywiggy's Temple Signpost 1": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Behind Jiggywiggy's Temple Signpost 2": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Behind Jiggywiggy's Temple Signpost 3": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Wooded Hollow Path to Plateau Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Jiggywiggy's Temple Signpost 1": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Jiggywiggy's Temple Signpost 2": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Jiggywiggy's Temple Signpost 3": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Jiggywiggy's Temple Signpost 4": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Jiggywiggy's Temple Signpost 5": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Jiggywiggy's Temple Signpost 6": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Jiggywiggy's Temple Signpost 7": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Jiggywiggy's Temple Signpost 8": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Wooded Hollow Silo Tagged": {
				"item": "WoodedHollowWarpSilo",
			},
		},
		"exits": {
			"Jiggywiggy Challenges": {"logic": {"Banjo-Kazooie"}},
			"Plateau": {},
			"Jinjo Village": {},
			"Bottles' House": {},
			"Mayahem Temple": {
				"id": 0x0A,
				"logic": "MayahemTemple",
				"groups": {"World Entrances"},
			},
			"Warp Silos": {},
		},
	},
	"Jiggywiggy Challenges": {
		# This region has special processing. The locations need to stay in order.
		"locations": {
			"IoH: Wooded Hollow Jiggywiggy Challenge 1": {
				"item": "MayahemTemple",
				"logic": "(Jiggy, JiggywiggysChallengeCostsChallenge1)",
			},
			"IoH: Wooded Hollow Jiggywiggy Challenge 2": {
				"item": "GlitterGulchMine",
				"logic": "(Jiggy, JiggywiggysChallengeCostsChallenge2)",
			},
			"IoH: Wooded Hollow Jiggywiggy Challenge 3": {
				"item": "Witchyworld",
				"logic": "(Jiggy, JiggywiggysChallengeCostsChallenge3)",
			},
			"IoH: Wooded Hollow Jiggywiggy Challenge 4": {
				"item": "JollyRogersLagoon",
				"logic": "(Jiggy, JiggywiggysChallengeCostsChallenge4)",
			},
			"IoH: Wooded Hollow Jiggywiggy Challenge 5": {
				"item": "Terrydactyland",
				"logic": "(Jiggy, JiggywiggysChallengeCostsChallenge5)",
			},
			"IoH: Wooded Hollow Jiggywiggy Challenge 6": {
				"item": "GruntyIndustries",
				"logic": "(Jiggy, JiggywiggysChallengeCostsChallenge6)",
			},
			"IoH: Wooded Hollow Jiggywiggy Challenge 7": {
				"item": "HailfirePeaks",
				"logic": "(Jiggy, JiggywiggysChallengeCostsChallenge7)",
			},
			"IoH: Wooded Hollow Jiggywiggy Challenge 8": {
				"item": "CloudCuckooland",
				"logic": "(Jiggy, JiggywiggysChallengeCostsChallenge8)",
			},
			"IoH: Wooded Hollow Jiggywiggy Challenge 9": {
				"item": "CauldronKeep",
				"logic": "(Jiggy, JiggywiggysChallengeCostsChallenge9)",
			},
			"IoH: Wooded Hollow Jiggywiggy Challenge 10": {
				"item": {"HAG1":"not OpenHAG1", "Nothing":"true"},
				"enabled": "not OpenHAG1 or JiggywiggysChallenges in ['shuffled', 'auto_shuffled']",
				"logic": "(Jiggy, JiggywiggysChallengeCostsChallenge10)",
			},
			"IoH: Wooded Hollow Jiggywiggy's Super Special Challenge": {
				"item": "Nothing",
				"enabled": "ShuffleJiggywiggysSuperSpecialChallenge",
				"logic": "(Jiggy, JiggywiggysChallengeCostsChallenge11)",
			},
		}
	}
}
