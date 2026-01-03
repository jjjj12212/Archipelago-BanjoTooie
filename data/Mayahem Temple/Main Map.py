from .. import Regions
instant_transform = {"Mumbo", "Stony"}
regions: Regions = {
	"MT: Main Map": {
		"locations": {
			"MT: First Stairs Note 1": {
				"item": "NoteNest",
			},
			"MT: First Stairs Note 2": {
				"item": "NoteNest",
			},
			"MT: First Stairs Note 3": {
				"item": "NoteNest",
			},
			"MT: First Stairs Note 4": {
				"item": "NoteNest",
			},
			"MT: Second Stairs Note 1": {
				"item": "NoteNest",
			},
			"MT: Second Stairs Note 2": {
				"item": "NoteNest",
			},
			"MT: Second Stairs Note 3": {
				"item": "NoteNest",
			},
			"MT: Second Stairs Note 4": {
				"item": "NoteNest",
			},
			"MT: Third Stairs Note 1": {
				"item": "NoteNest",
			},
			"MT: Third Stairs Note 2": {
				"item": "NoteNest",
			},
			"MT: Third Stairs Note 3": {
				"item": "NoteNest",
			},
			"MT: Third Stairs Note 4": {
				"item": "NoteNest",
			},
			"MT: Top Stairs Note 1": {
				"item": "NoteNest",
			},
			"MT: Top Stairs Note 2": {
				"item": "NoteNest",
			},
			"MT: Top Stairs Note 3": {
				"item": "NoteNest",
			},
			"MT: Outside Mumbo's Skull Note": {
				"item": "NoteNest",
			},
			"MT: Water Pool Jinjo": {
				"item": "BlackJinjo",
				"logic": {
					"Banjo-Kazooie": """
						Dive
						or EasyTediousJumps
					""",
					"Mumbo": "EasyTediousJumps",
					"Stony": "true",
					"Golden Goliath": "true",
				}
			},
			"MT: Bridge Jinjo": {
				"item": "RedJinjo",
			},
			"MT: Bovina Jiggy": {
				"item": "Jiggy",
				"logic": "MTKillFlies"
			},
			"MT: In Front of Jade Snake Grove Feather Nest 1": {
				"item": "FeatherNest",
			},
			"MT: In Front of Jade Snake Grove Feather Nest 2": {
				"item": "FeatherNest",
			},
			"MT: Entrance Honeycomb": {
				"item": "EmptyHoneycomb",
			},
			"MT: Treble Clef": {
				"item": "TrebleClef",
			},
			"MT: Breegull Blaster Silo": {
				"item": "BreegullBlaster",
				"logic": {"Banjo-Kazooie": "Notes >= ChosenMoveSiloCosts['Breegull Blaster']"},
			},
			"MT: Egg Aim Silo": {
				"item": "EggAim",
				"logic": {"Banjo-Kazooie": "Notes >= ChosenMoveSiloCosts['Egg Aim']"},
			},
			"MT: In Front of Prison Compound Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: In Front of Prison Compound Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Outside Treasure Chamber Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Outside Treasure Chamber Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Bovina Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Bovina Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Golden Goliath Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"MT: World Entry and Exit Warp Pad Tagged": {
				"item": "MTWorldEntryAndExitWarpPad",
			},
			"MT: Outside Mumbo's Skull Warp Pad Tagged": {
				"item": "MTOutsideMumbosSkullWarpPad",
			},
		},
		"exits": {
			"Mayahem Temple": {
				"logic": {
					"Banjo-Kazooie": "true",
					"Talon Trot": "TalonTrotSmuggleCrossWorld"
				}
			},
			"MT: Top of Kickball Stadium": {
				"logic": {
					"Banjo-Kazooie": "FlapFlipSlideExtension and BeakBusterJump and Roll and FlapFlip and BeakBuster"
				}
			},
			"MT: Kill Flies": {
				"logic": {
					"Banjo-Kazooie": """
						ShootLinearEggs
						or ClockworkShot
						or BovinaWithFlapFlip
					"""
				}
			},
			"MT: Bovina Honeycomb": {
				"logic": {
					"Banjo-Kazooie": """
						ClockworkShot
						or FlapFlip and GripGrab
						or BeakBusterJump and FlapFlip
					"""
				}
			},
			"MT: Top Platform Outside Treasure Chamber": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
			"MT: Top of Kickball Stadium": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
			"MT: Top of the Temple": {
				"logic": {
					"Banjo-Kazooie": """
						TalonTrot
						or HardJumps
					""",
					"Talon Trot": "true"
				}
			},
			"MT: Targitzan's Temple Lobby": {
				"id": -1
			},
			"MT: Jade Snake Grove": {
				"logic": "MTOpenJadeSnakeGrove",
				"explicit_logic": {
					"Golden Goliath": "MTOpenJadeSnakeGrove"
				}
			},
			"MT: Main Map": {
				"logic": {
					"Mumbo": {
						"Golden Goliath": "MumboGoldenGoliath"
					}
				}
			},
			"MT: Open Jade Snake Grove": {
				"logic": {
					"Golden Goliath": "true"
				}
			},
			"MT: Open Prison Compound": {
				"logic": {
					"Golden Goliath": "true",
					"Banjo-Kazooie": "ShootExplosives"
				}
			},
			"MT: Mumbo's Skull": {
				"id": -1,
			},
			"MT: Treasure Chamber Bottom": {
				"logic": "MTOpenBottomTreasureChamberDoor",
				"id": -1
			},
			"MT: Warp Pads": {
				"logic": "MTWorldEntryAndExitWarpPad or MTOutsideMumbosSkullWarpPad"
			},
			"MT: Kickball Stadium": {
				"logic": {
					"Stony": "true"
				}
			},
			"MT: Snake Heads": {
				"logic": {
					"Banjo-Kazooie": "(LinearEggs or ExtraClockworkUsage) and EggAim"
				}
			},
			"MT: Flight": {
				"logic": {
					"Banjo-Kazooie": "MTBreakFlightPadBoulder"
				}
			},
			"MT: Break Flight Pad Boulder": {
				"logic": {
					"Banjo-Kazooie": "BillDrill",
					"Golden Goliath": "true"
				}
			},
			"MT: Prison Compound": {
				"logic": "MTOpenPrisonCompound"
			},
		}
	},
	"MT: Top of the Temple": {
		"locations": {
			"MT: Top of Temple Jiggy": {
				"item": "Jiggy",
			}
		}
	},
	"MT: Kill Flies": {"macro": {"event"}},
	"MT: Open Prison Compound": {"macro": {"event"}},
	"MT: Open Jade Snake Grove": {"macro": {"event"}},
	"MT: Break Flight Pad Boulder": {"macro": {"event"}},
	"MT: Bovina Honeycomb": {
		"locations": {
			"MT: Bovina Honeycomb": {
				"item": "EmptyHoneycomb",
			},
		}
	},
	"MT: Flight": {
		"exits": {
			"MT: Kill Flies": {
				"logic": {
					"Banjo-Kazooie":"""
						AirborneEggAiming and LinearEggs
						or ExtraClockworkUsage and AirborneEggAiming
						or BovinaWithBeakBomb
					"""
				}
			},
			"MT: Snake Heads": {
				"logic": {
					"Banjo-Kazooie": """
						AirborneEggAiming and LinearEggs
						or ExtraClockworkUsage and AirborneEggAiming
					"""
				}
			},
			"MT: Top Platform Outside Treasure Chamber": {},
			"MT: Top of Kickball Stadium": {},
			"MT: Kickball Stadium": {
				"logic": {
					"Banjo-Kazooie": "BeakBombClips"
				}
			},
			"MT: Jade Snake Grove": {
				"logic": {
					"Banjo-Kazooie": "BeakBombClips"
				}
			},
			"MT: Bovina Honeycomb": {}
		}
	},
	"MT: Snake Heads": {
		"locations": {
			"MT: Snake Head 1": {
				"item": "MTSnakeHead"
			},
			"MT: Snake Head 2": {
				"item": "MTSnakeHead"
			},
			"MT: Snake Head 3": {
				"item": "MTSnakeHead"
			},
			"MT: Snake Head 4": {
				"item": "MTSnakeHead"
			},
			"MT: Snake Head 5": {
				"item": "MTSnakeHead"
			},
			"MT: Snake Head 6": {
				"item": "MTSnakeHead"
			},
		},
		"exits": {
			"MT: Open Bottom Treasure Chamber Door": {
				"logic": "(MTSnakeHead, 6)"
			}
		}
	},
	"MT: Top Platform Outside Treasure Chamber": {
		"locations": {
			"MT: Treasure Chamber Cheato Page": {
				"item": "CheatoPage",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"MT: Main Map": {},
			"MT: Treasure Chamber In Front of Unga Bunga Gate": {
				"id": -1,
				"logic": "MTOpenTopTreasureChamberDoor"
			}
		}
	},
	"MT: Open Bottom Treasure Chamber Door": {"macro": {"event"}},
	"MT: Top of Kickball Stadium": {
		"locations": {
			"MT: Stadium Jinjo": {
				"item": "RedJinjo",
				"explicit_logic": {"Clockwork Kazooie": "true"}
			},
			"MT: Kickball Stadium Feather Nest 1": {
				"item": "FeatherNest",
				"explicit_logic": {"Clockwork Kazooie": "true"}
			},
			"MT: Kickball Stadium Feather Nest 2": {
				"item": "FeatherNest",
				"explicit_logic": {"Clockwork Kazooie": "true"}
			},
		},
		"exits": {
			"MT: Flight": {
				"logic": {
					"Banjo-Kazooie": "FlightPad"
				}
			}
		}
	},
	"MT: Mumbo's Skull": {
		"locations": {
			"MT: Mumbo's Skull Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Mumbo's Skull Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Mumbo's Skull Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"MT: Mumbo's Glowbo": {
				"item": "MumboGoldenGoliath",
			},
		},
		"exits": {
			"MT: Mumbo's Skull": {
				"logic": {
					"Banjo-Kazooie": {"Mumbo": "MumboGoldenGoliath"}
				}
			},
			"MT: Main Map": {}
		}
	},
}
