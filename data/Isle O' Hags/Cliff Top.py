from .. import Regions
regions: Regions = {
	"IoH: Cliff Top": {
		"id": 0x0155,
		"locations": {
			"IoH: Ice Eggs Silo": {
				"item": "IceEggs",
				"logic": {"Banjo-Kazooie": "Notes >= ChosenMoveSiloCosts['Ice Eggs']"},
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
                "logic": {
                    "Banjo-Kazooie": """
						TallJump
                        or TalonTrot
                        or FlapFlip
                        or GripGrab
                        or BeakBusterJump
                        or EasyJumps and (Flutter or AirRatatatRap)
                        or ClockworkShot
					""",
                    "Mumbo": "TallJump"
				}
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
			"IoH: Cliff Top Jinjo": {
				"item": "PurpleJinjo",
                "logic": {"Banjo-Kazooie": "ClockworkShot"},
                "explicit_logic": {"BK Claw Clamber Boots": "true"}
			},
		},
		"exits": {
			"IoH: Plateau": {
                "logic": {
                    "Banjo-Kazooie": "true"
				}
			},
			"Train At IoH": {"logic": "Chuffy and IoHTrainStation"},
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
				"logic": {
                    "Banjo-Kazooie": "JollyRogersLagoon",
                    "Talon Trot": "TalonTrotSmuggleCrossWorld and JollyRogersLagoon"
                },
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
			},
            "Scrat Healed": {
                "logic": {
                    "Mumbo": "TrainAtIoH"
				}
			},
            "IoH: Mumbo's Skull": {},
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
        "locations": {
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
		},
        "exits": {
			"Hailfire Peaks": {
				"id": 0x15,
				"logic": {
                    "Banjo-Kazooie": "HailfirePeaks",
                    "Talon Trot": "TalonTrotSmuggleCrossWorld and HailfirePeaks"
                },
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
    "IoH: Cliff Top On Top of HFP": {
        "locations": {
			"IoH: Cliff Top Glowbo": {
				"item": "MumboHeal",
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		}
	},
    "IoH: Mumbo's Skull": {
        "exits": {
            "IoH: Mumbo's Skull": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Mumbo": "MumboHeal"
					}
				}
			},
            "IoH: Cliff Top": {}
		}
	},
    "Scrat Healed": {"macro": {"event"}},
}
