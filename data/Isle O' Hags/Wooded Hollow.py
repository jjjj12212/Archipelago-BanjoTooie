from .. import Regions
regions: Regions = {
	"IoH: Wooded Hollow": {
		"id": 0x014F,
		"locations": {
			"IoH: Wooded Hollow Jinjo": {
				"item": "BlueJinjo",
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
			"IoH: Wooded Hollow Behind Heggy's Egg Shed Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Wooded Hollow Silo Tagged": {
				"item": "WoodedHollowWarpSilo",
                "logic": {
                    "Banjo-Kazooie": "true"
				}
			},
		},
		"exits": {
            "IoH: Jiggywiggy's Temple": {},
			"IoH: Wooded Hollow Path to Plateau": {
                "logic": {
                    "Banjo-Kazooie": "GripGrab and (TallJump or TalonTrot and Flutter or TalonTrot and AirRatatatRap and HardTediousJumps or FlapFlip) or FlapFlip and BeakBusterJump and HardJumps"
				}
			},
			"IoH: Jinjo Village On Top of the Ledge": {},
			"IoH: Bottles\' House: Behind the Gate": {},
            "IoH: Heggy's Egg Shed": {},
			"Mayahem Temple": {
				"id": 0x0A,
				"groups": {"World Entrances"},
				"logic": {
					"Banjo-Kazooie": "MayahemTemple",
					"Talon Trot": "MayahemTemple and TalonTrotSmuggleCrossWorld",
				}
			},
			"IoH: Warp Silos": {
                "logic": {
                    "Banjo-Kazooie": "WoodedHollowWarpSilo"
				}
			},
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
	},
    "IoH: Heggy's Egg Shed": {
        "locations": {
			"IoH: Pink Mystery Egg Hatched": {
				"item": "BreegullBash",
                "logic": {
                    "Banjo-Kazooie": "PinkMysteryEgg",
                    "Banjo": "PinkMysteryEgg"
				}
			},
			"IoH: Blue Mystery Egg Hatched": {
				"item": "HomingEggs",
                "logic": {
                    "Banjo-Kazooie": "BlueMysteryEgg",
                    "Banjo": "BlueMysteryEgg"
				}
			},
			"IoH: Yellow Mystery Egg Hatched": {
				"item": "Nothing",
				"enabled": "not ShuffleStopNSwop",
                "logic": {
                    "Kazooie": "Hatch"
				}
			},
        },
        "exits": {
            "IoH: Wooded Hollow": {
                "logic": {
                    "Banjo-Kazooie": "true"
				}
			}
		},
        "macro": {"splitup"}
	},
    "IoH: Jiggywiggy's Temple": {
        "locations": {
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
        },
        "exits": {
			"Jiggywiggy Challenges": {"logic": {"Banjo-Kazooie"}},
		}
	},
    "IoH: Jiggywiggy's Temple On Jiggywiggy Pedestal": {
        "exits": {
			"IoH: Jiggywiggy's Temple": {},
			"IoH: Behind Jiggywiggy's Temple": {},
		}
	},
    "IoH: Behind Jiggywiggy's Temple": {
        "locations": {
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
		},
        "exits": {
            "IoH: Jiggywiggy's Temple On Jiggywiggy Pedestal": {
                "logic": {
                    "Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or WonderwingJump or BeakBusterJump or Flutter or AirRatatatRap"
				}
			},
		},
	},
    "IoH: Wooded Hollow Path to Plateau": {
        "locations": {
			"IoH: Wooded Hollow Path to Plateau Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
        },
        "exits": {
            "IoH: Wooded Hollow": {},
            "IoH: Plateau": {},
		}
	},
}
