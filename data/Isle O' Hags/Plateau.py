from .. import Regions
regions: Regions = {
	"IoH: Plateau": {
		"id": 0x0152,
		"locations": {
			"IoH: Plateau Jinjo": {
				"item": "BlueJinjo",
                "logic": {
                    "Banjo-Kazooie": """
						BeakBuster
                        or BeakBargeClip
					""",
                    "Banjo": "TaxiPackClip"
				}
			},
			"IoH: Plateau GGM Sign Note 1": {
				"item": "NoteNest",
                "logic": {
                    "Banjo-Kazooie": "FlapFlip and GripGrab or FlapFlip and BeakBusterJump or ClockworkShot",
                    "Banjo": "HardJumps and (FlapFlip and GripGrab)",
                    "Kazooie": "EasyJumps and (TallJump or Glide)"
				}
			},
			"IoH: Plateau GGM Sign Note 2": {
				"item": "NoteNest",
                "logic": {
                    "Banjo-Kazooie": "FlapFlip and GripGrab or FlapFlip and BeakBusterJump or ClockworkShot",
                    "Banjo": "HardJumps and (FlapFlip and GripGrab)",
                    "Kazooie": "EasyJumps and (TallJump or Glide)"
				}
			},
			"IoH: Fire Eggs Silo": {
				"item": "FireEggs",
				"logic": {"Banjo-Kazooie": "Notes >= ChosenMoveSiloCosts['Fire Eggs']"},
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
                "logic": {
                    "Banjo-Kazooie": "TalonTrot or ClockworkShot",
                    "Talon Trot": "true",
                    "Kazooie": "true",
                    "Banjo": "PackWhackSlopeJump"
				}
			},
			"IoH: Plateau Dirt Pile Feather Nest 2": {
				"item": "FeatherNest",
                "logic": {
                    "Banjo-Kazooie": "TalonTrot or ClockworkShot",
                    "Talon Trot": "true",
                    "Kazooie": "true",
                    "Banjo": "PackWhackSlopeJump"
				}
			},
			"IoH: Plateau Silo Tagged": {
				"item": "PlateauWarpSilo",
			},
		},
		"exits": {
			"IoH: Wooded Hollow": {
                "logic": {
                    "Banjo-Kazooie": "true"
				}
			},
			"IoH: Cliff Top": {
                "logic": {
                    "Banjo-Kazooie": "IoHPlateauPathtoCliffTopOpened"
				}
			},
            "IoH: Plateau: Fire Switch": {
                "logic": {
                    "Banjo-Kazooie": "TalonTrot and ThirdPersonEggShooting and FireEggs or EggAim and FireEggs",
                    "Kazooie": "DragonBreath and (WingWhack or Glide) and WingWhack or EggUse and FireEggs",
                    "Talon Trot": "ThirdPersonEggShooting and FireEggs"
				}
			},
            "IoH: Plateau: Path to Cliff Top Opened": {
                "logic": {
                    "Banjo-Kazooie": "SplitUp"
				}
			},
			"IoH: Pine Grove": {
                "logic": {
                    "Banjo-Kazooie": "IoHPlateauFireSwitch"
				}
			},
			"Glitter Gulch Mine": {
				"id": 0x11,
				"logic": "GlitterGulchMine",
                "explicit_logic": {
                    "Talon Trot": "TalonTrotSmuggleCrossWorld"
				},
				"groups": {"World Entrances"},
			},
			"IoH: Warp Silos": {
                "logic": {
                    "Banjo-Kazooie": "PlateauWarpSilo"
				}
			},
            "IoH: Plateau: Next to Honey B's Hive": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "TalonTrot",
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Kazooie": "true",
                    "Talon Trot": "true",
                    "Banjo": "PackWhackSlopeJump"
				}
			}
		},
        "macro": {"splitup"}
	},
    "IoH: Plateau: Next to Honey B's Hive": {
        "locations": {
			"IoH: Plateau Honeycomb": {
				"item": "EmptyHoneycomb",
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
			"IoH: Plateau Honey B. Note 1": {
				"item": "NoteNest",
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
			"IoH: Plateau Honey B. Note 2": {
				"item": "NoteNest",
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		},
        "exits": {
            "IoH: Plateau: Honey B.'s Hive": {
                "logic": {
                    "Banjo-Kazooie": "true",
                    "Talon Trot": "true"
				}
			},
            "IoH: Plateau": {}
		}
	},
    "IoH: Plateau: Fire Switch": {"macro": {"event"}},
    "IoH: Plateau: Leaving GGM": {
        "exits": {
			"IoH: Plateau": {
                "logic": "Flutter or AirRatatatRap or Climb or BeakBuster"
			}
		}
	},
    "IoH: Plateau: Honey B.'s Hive": {
        "locations": {
			"IoH: Honey B's Reward 1": {
				"item": "HealthUpgrade",
                "logic": {
                    "Banjo-Kazooie": "(EmptyHoneycomb, 1)"
				}
			},
			"IoH: Honey B's Reward 2": {
				"item": "HealthUpgrade",
                "logic": {
                    "Banjo-Kazooie": "(EmptyHoneycomb, 4)"
				}
			},
			"IoH: Honey B's Reward 3": {
				"item": "HealthUpgrade",
                "logic": {
                    "Banjo-Kazooie": "(EmptyHoneycomb, 9)"
				}
			},
			"IoH: Honey B's Reward 4": {
				"item": "HealthUpgrade",
                "logic": {
                    "Banjo-Kazooie": "(EmptyHoneycomb, 16)"
				}
			},
			"IoH: Honey B's Reward 5": {
				"item": "HealthUpgrade",
                "logic": {
                    "Banjo-Kazooie": "(EmptyHoneycomb, 25)"
				}
			},
		},
        "exits": {
            "IoH: Plateau: Next to Honey B's Hive": {}
		}
	},
    "IoH: Plateau: Path to Cliff Top Opened": {"macro": {"event"}},
}
