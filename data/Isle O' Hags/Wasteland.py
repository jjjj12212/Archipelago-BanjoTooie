from .. import Regions
regions: Regions = {
	"IoH: Wasteland": {
		"id": 0x015A,
		"locations": {
			"IoH: Wasteland CCL Area Note 1": {
				"item": "NoteNest",
			},
			"IoH: Wasteland CCL Area Note 2": {
				"item": "NoteNest",
			},
			"IoH: Clockwork Kazooie Eggs Silo": {
				"item": "ClockworkKazooieEggs",
			},
			"IoH: Wasteland Next to Quagmire Entrance Feather Nest": {
				"item": "FeatherNest",
			},
			"IoH: Wasteland TDL Entrance Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Wasteland TDL Entrance Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Wasteland Behind CCL Bubble Feather Nest": {
				"item": "FeatherNest",
			},
			"IoH: Wasteland Near Crevice to CCL Feather Nest": {
				"item": "FeatherNest",
			},
			"IoH: Wasteland Near Digger Tunnel Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Wasteland Near Digger Tunnel Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Wasteland Near Digger Tunnel Egg Nest 3": {
				"item": "EggNest",
			},
			"IoH: Wasteland Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Wasteland Silo Tagged": {
				"item": "WastelandWarpSilo",
			},
		},
		"exits": {
			"IoH: Another Digger Tunnel": {},
            "IoH: Wasteland Behind TDL Teeth": {
                "logic": "Terrydactyland"
			},
			"Cloud Cuckooland": {
				"id": 0x14,
				"groups": {"World Entrances"},
				"logic": {
					"Banjo-Kazooie": "CloudCuckooland",
					"Talon Trot": "CloudCuckooland and TalonTrotSmuggleCrossWorld",
				}
			},
			"IoH: Warp Silos": {
                "logic": {
                    "Banjo-Kazooie": "WastelandWarpSilo"
				}
			},
            "IoH: Wasteland Clockwork Bottom Note Platform": {
				"logic": {
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "EasyJumps or TallJump or TalonTrot or FlapFlip or WonderwingJump or BeakBusterJump",
                        "Talon Trot": "true",
                        "Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
            "IoH: Wasteland Clockwork Top Note Platform": {
				"logic": {
                    "Banjo-Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
            "IoH: Wasteland Jinjo Platform": {
				"logic": {
                    "Banjo-Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
		},
	},
	"IoH: Wasteland Ledge to Quagmire": {
        "exits": {
            "IoH: Wasteland": {},
            "IoH: Quagmire": {},
		}
	},
    "IoH: Wasteland Behind TDL Teeth": {
        "exits": {
            "IoH: Wasteland": {},
			"Terrydactyland": {
				"id": 0x17,
				"groups": {"World Entrances"},
				"logic": {
					"Banjo-Kazooie": "Terrydactyland",
					"Talon Trot": "Terrydactyland and TalonTrotSmuggleCrossWorld",
				}
			},
		}
	},
    "IoH: Wasteland Clockwork Bottom Note Platform": {
        "locations": {
			"IoH: Clockwork Silo Bottom Note": {
				"item": "NoteNest",
			},
		},
        "exits": {
            "IoH: Wasteland Clockwork Top Note Platform": {
                "logic": {
                    "Banjo-Kazooie": "FlapFlip or TalonTrot and Flutter and (GripGrab or BeakBusterJump) or TallJump and GripGrab",
                    "Talon Trot": {
                        "Banjo-Kazooie": "Flutter and (GripGrab or BeakBusterJump)"
					}
				}
			}
		}
	},
    "IoH: Wasteland Clockwork Top Note Platform": {
        "locations": {
			"IoH: Clockwork Silo Top Note": {
				"item": "NoteNest",
			},
		},
        "exits": {
            "IoH: Wasteland Jinjo Platform": {
                "logic": {
                    "Banjo-Kazooie": "FlapFlip and (GripGrab or BeakBusterJump)"
				}
			}
		}
	},
    "IoH: Wasteland Jinjo Platform": {
        "locations": {
			"IoH: Wasteland Jinjo": {
				"item": "PurpleJinjo",
			},
        }
	},
}
