from .. import Regions
regions: Regions = {
	"IoH: Cliff Top": {
		"id": 0x0155,
		"locations": {
			"IoH: Cliff Top Jinjo": {
				"item": "PurpleJinjo",
			},
			"IoH: Cliff Top Glowbo": {
				"item": "MumboHeal",
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
			"IoH: Plateau": {},
			"Train at IoH": {"logic": "Chuffy and IoHTrainStation"},
			"Chuffy's Cab": {"logic": {"Banjo-Kazooie": """ 
										TrainAtIoH and (
										Climb and (
											TallJump
											or TalonTrot 
											or FlapFlip
											or BeakBusterJump
										)
										or Climb and EasyJumps
										or (TallJump or TalonTrot or FlapFlip) and EasyJumps
										or BeakBusterJump
									)"""}},
			"Inside Chuffy's Wagon": {"logic": "TrainAtIoH"},
			"Jolly Roger's Lagoon": {
				"id": 0x03,
				"logic": "JollyRogersLagoon",
				"groups": {"World Entrances"},
			},
			"IoH: Warp Silos": {
                "logic": {
                    "Banjo-Kazooie": "CliffTopWarpSilo"
				}
			},
            "IoH: Cliff Top Bridge Switch Pressed": {},
            "IoH: Cliff Top Around HFP": {
                "logic": "IoHCliffTopBridgeSwitchPressed"
			},
            "IoH: Cliff Top Train Switch Platform": {
                "logic": {
                    "Banjo-Kazooie": "FlapFlip and GripGrab"
				}
			}
		},
	},
    "IoH: Cliff Top Train Switch Platform": {
        "locations": {
			"IoH: Train Switch": {
				"item": "IoHTrainStation",
			},
		}
	},
    "IoH: Cliff Top Bridge Switch Pressed": {"macro": {"event"}},
    "IoH: Cliff Top Around HFP": {
        "exits": {
			"Hailfire Peaks": {
				"id": 0x15,
				"logic": "HailfirePeaks",
				"groups": {"World Entrances"},
			},
            "IoH: Cliff Top On Top of HFP": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "Climb",
                        "Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
            "IoH: Cliff Top Around HFP": {
                "logic": {
                    "Banjo-Kazooie": {
                        "BK Claw Clamber Boots": "ClawClamberBoots"
                    }
				}
			},
            "IoH: Cliff Top": {
                "logic": {
                    "BK Claw Clamber Boots": "IoHCliffTopBridgeSwitchPressed",
                    "Banjo-Kazooie": "IoHCliffTopBridgeSwitchPressed"
				}
			}
		}
	},
    "IoH: Cliff Top On Top of HFP": {},
}
