from .. import Regions
instant_transform = {"Mumbo", "Stony"}
regions: Regions = {
	"Mayahem Temple": {
		"id": 0x00B8,
		"exits": {
			"Wooded Hollow": {
				"id": 0x02,
				"groups":{"World Exits"},
			},
			"MT: Main Map": {}
		},
	},
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
			},
			"MT: Egg Aim Silo": {
				"item": "EggAim",
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
			"MT: Main Map": {
				"logic": {
					"Banjo-Kazooie": "true"
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
			}
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
	"MT: Open Bottom Treasure Chamber Door": {"macro": {"event"}},
	"MT: Open Top Treasure Chamber Door": {"macro": {"event"}},
	"MT: Top Platform Outside Treasure Chamber": {
		"locations": {
			"MT: Treasure Chamber Cheato Page": {
				"item": "CheatoPage",
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
	"MT: Treasure Chamber Bottom": {
		"locations": {
			"MT: Treasure Chamber Jiggy": {
				"logic": "TDLPricelessRelicThingy",
				"item": "Jiggy",
			},
		},
		"exits": {
			"MT: Main Map": {
				"id": -1
			},
			"MT: Treasure Chamber Honeycomb Pile": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot",
						"Banjo-Kazooie": "TalonTrot",
						"Talon Trot": "true"
					}
				}
			},
			"MT: Open Top Treasure Chamber Door": {
				"logic": {
					"Banjo-Kazooie": "true"
				}
			}
		}
	},
	"MT: Treasure Chamber Honeycomb Pile": {
		"locations": {
			"MT: Treasure Chamber Honeycomb": {
				"item": "EmptyHoneycomb",
			},
		},
		"exits": {
			"MT: Treasure Chamber Bottom": {},
			"MT: Treasure Chamber In Front of Unga Bunga Gate": {
				"logic": {
					"Banjo-Kazooie": "FlapFlip and GripGrab and TallJump"
				}
			}
		}
	},
	"MT: Treasure Chamber In Front of Unga Bunga Gate": {
		"exits": {
			"MT: Treasure Chamber Honeycomb Pile": {
				"logic": {
					"Banjo-Kazooie": "GripGrab"
				}
			},
			"MT: Top Platform Outside Treasure Chamber": {
				"logic": {
					"Banjo-Kazooie": "TallJump"
				}
			},
			"MT: Treasure Chamber Behind Unga Bunga Gate": {
				"logic": "MTTreasureChamberUngaBungaSwitchPressed"
			},
			"MT: Treasure Chamber Unga Bunga Switch Pressed": {},
		}
	},
	"MT: Treasure Chamber Behind Unga Bunga Gate": {
		# TODO: TDL transition
		"exits": {
			"MT: Treasure Chamber In Front of Unga Bunga Gate": {
				"logic": "MTTreasureChamberUngaBungaSwitchPressed"
			},
		}
	},
	"MT: Treasure Chamber Unga Bunga Switch Pressed": {"macro": {"event"}},
	"MT: Top of Kickball Stadium": {
		"locations": {
			"MT: Stadium Jinjo": {
				"item": "RedJinjo",
			},
			"MT: Kickball Stadium Feather Nest 1": {
				"item": "FeatherNest",
			},
			"MT: Kickball Stadium Feather Nest 2": {
				"item": "FeatherNest",
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
	"MT: Kickball Stadium": {
		"locations":{
			"MT: Kickball Jiggy": {
				"item": "Jiggy",
				"logic": "MTKickballRound1Won and MTKickballRound2Won and MTKickballRound3Won"
			},
			"MT: Kickball Mumbo Token": {
				"item": {"MumboToken":"'MT Kickball' in ChosenGoals", "Nothing":"true"},
				"enabled": "'MT Kickball' in VictoryGoals",
				"locked": "true",
			},
			"MT: Kickball Stadium Lobby Warp Pad Tagged": {
				"item": "MTKickballStadiumLobbyWarpPad",
			},
		},
		"exits": {
			"MT: Main Map": {
				"id": -1
			},
			"MT: Kickball Stadium Near Grate Switch": {
				"logic": "MTKickballStadiumSwitchPressed"
			},
			"MT: Warp Pads": {
				"logic": "MTKickballStadiumLobbyWarpPad"
			},
			"MT: Kickball Round 1": {
				"logic": {
					"Stony": "true"
				}
			},
			"MT: Kickball Round 2": {
				"logic": {
					"Stony": "MTKickballRound1Won"
				}
			},
			"MT: Kickball Round 3": {
				"logic": {
					"Stony": "MTKickballRound2Won"
				}
			},
		}
	},
	"MT: Kickball Round 1": {
		"locations": {
			"MT Kickball Round 1 Won": {}
		},
		"exits": {
			"MT: Kickball Stadium": {}
		}
	},
	"MT: Kickball Round 2": {
		"locations": {
			"MT Kickball Round 2 Won": {}
		},
		"exits": {
			"MT: Kickball Stadium": {}
		}
	},
	"MT: Kickball Round 3": {
		"locations": {
			"MT Kickball Round 3 Won": {}
		},
		"exits": {
			"MT: Kickball Stadium": {}
		}
	},
	"MT: Kickball Stadium Near Grate Switch": {
		#TODO: Add HFP entrance
		"exits": {
			"MT: Kickball Stadium": {
				"logic": "MTKickballStadiumSwitchPressed"
			},
			"MT: Kickball Stadium Switch Pressed": {}
		}
	},
	"MT: Kickball Stadium Switch Pressed": {"macro": {"event"}},
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
	"MT: Warp Pads": {
		"exits": {
			"MT: Main Map": {
				"logic": "MTWorldEntryAndExitWarpPad or MTOutsideMumbosSkullWarpPad"
			},
			"MT: Jade Snake Grove": {
				"logic": "MTNearWumbasWigwamWarpPad"
			},
			"MT: Prison Compound": {
				"logic": "MTPrisonCompoundWarpPad"
			},
			"MT: Kickball Stadium": {
				"logic": "MTKickballStadiumLobbyWarpPad"
			}
		}
	},
	"MT: Targitzan's Temple Lobby": {
		"locations": {
			"MT: Targitzan's Temple Lobby Left Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Lobby Left Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Lobby Left Egg Nest 3": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Lobby Right Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Lobby Right Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Lobby Right Egg Nest 3": {
				"item": "EggNest",
			}
		},
		"exits": {
			"MT: Main Map": {},
			"MT: Targitzan's Temple": {
				"logic": {
					"Banjo-Kazooie": "BreegullBlaster"
				}
			}
		}
	},
	"MT: Targitzan's Temple": {
		"locations": {
			"MT: Targitzan's Temple Right Entrance Relic": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Left Entrance Relic": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Blue Pillar Room Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Blue Pillar Room Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Blue Pillar Room Relic 3": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sput Sput Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sput Sput Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sput Sput Relic 3": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sput Sput Relic 4": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sput Sput Relic 5": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Green Pillar Room Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Green Pillar Room Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Green Pillar Room Relic 3": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Green Pillar Room Relic 4": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Green Pillar Room Relic 5": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sacred Chambers Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sacred Chambers Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Secret Passage Near Sacred Chambers Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Secret Passage Near Sacred Chambers Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Secret Passage Near Sacred Chambers Relic 3": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Secret Passage Near Entrance Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Secret Passage Near Entrance Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Red Pillar Room Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Red Pillar Room Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Red Pillar Room Relic 3": {
				"item": "GreenRelic",
			},
			"MT: Targitzan Temple Jinjo": {
				"item": "RedJinjo",
			},
			"MT: Targitzan's Temple Raising Slope Room Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Raising Slope Room Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple 4-Way Room Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple 4-Way Room Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple 4-Way Room Egg Nest 3": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple 4-Way Room Egg Nest 4": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Pillar Maze Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Pillar Maze Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Pillar Maze Egg Nest 3": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Raising Slope Room Egg Nest 3": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Golden Egg Nest": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Signpost 1": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"MT: Targitzan's Temple Signpost 2": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		},
		"exits": {
			"MT: Targitzan's Temple Lobby": {},
			"MT: Slighty Sacred Chamber": {
				"logic": "(GreenRelic, 10)"
			},
			"MT: Really Sacred Chamber": {
				"logic": "(GreenRelic, 20)"
			}
		}
	},
	"MT: Slighty Sacred Chamber": {
		"locations": {
			"MT: Slighty Sacred Chamber Jiggy": {
				"item": "Jiggy",
			},
		},
		"exits": {
			"MT: Targitzan's Temple": {}
		}
	},
	"MT: Really Sacred Chamber": {
		"locations": {
			"MT: Targitzan Jiggy": {
				"item": "Jiggy",
			},
			"MT: Targitzan Mumbo Token": {
				"item": {"MumboToken":"'Targitzan' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Targitzan' in VictoryGoals",
				"locked": "true",
			},
		},
		"exits": {
			"MT: Targitzan's Temple": {}
		}
	},
	"MT: Jade Snake Grove": {
		"locations": {
			"MT: Grip Grab Silo": {
				"item": "GripGrab",
			},
			"MT: Jade Snake Grove Glowbo": {
				"item": "HumbaStony",
			},
			"MT: Jade Snake Grove Near Warp Pad Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Jade Snake Grove Near Warp Pad Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Jade Snake Grove Quicksand Signpost 1": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"MT: Jade Snake Grove Quicksand Signpost 2": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"MT: Jade Snake Grove Jinjo": {
				"item": "PurpleJinjo",
			},
			"MT: Golden Goliath Jiggy": {
				"item": "Jiggy",
			},
			"MT: Near Wumba's Wigwam Warp Pad Tagged": {
				"item": "MTNearWumbasWigwamWarpPad",
			},
		},
		"exits": {
			"MT: Main Map": {},
			"MT: Wumba's Wigwam": {},
			"MT: Jade Snake Grove Top of Slope": {
				"logic": {
					"Banjo-Kazooie": "TalonTrot",
					"Talon Trot": "true"
				}
			},
			"MT: Warp Pads": {
				"logic": "MTNearWumbasWigwamWarpPad"
			},
			"MT: Jade Snake Grove Top of Code Chamber Entrance": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TalonTrot or (TallJump or FlapFlip) and SlopeJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Mumbo": "TallJump and SlopeJump",
					"Stony": "SlopeJump",
					"Golden Goliath": "SlopeJump",
					"Talon Trot": "true",
				}
			},
			"MT: Open Code Chamber": {
				"logic": {
					"Golden Goliath": "true",
					"Banjo-Kazooie": "ShootExplosives"
				}
			},
			"MT: Code Chamber": {
				"logic": "MTOpenCodeChamber"
			},
			"MT: Jade Snake Grove Cheato Page Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			}
		}
	},
	"MT: Jade Snake Grove Top of Code Chamber Entrance": {
		"locations": {
			"MT: Jade Snake Grove Above Code Chamber Egg Nest": {
				"item": "EggNest",
			},
		}
	},
	"MT: Jade Snake Grove Top of Slope": {
		"exits": {
			"MT: Jade Snake Grove Ssslumber Jiggy Platform": {
				"logic": "FlapFlip and (GripGrab or BeakBusterJump)"
			},
			"MT: Jade Snake Grove Cheato Page Platform": {
				"logic": "FlapFlip and GripGrab"
			},
			"MT: Jade Snake Grove Left of Code Chamber Signpost Platform": {
				"logic": "FlapFlip and GripGrab"
			},
		}
	},
	"MT: Jade Snake Grove Cheato Page Platform": {
		"locations": {
			"MT: Jade Snake Grove Cheato Page": {
				"item": "CheatoPage",
			},
		}
	},
	"MT: Jade Snake Grove Ssslumber Jiggy Platform": {
		"locations": {
			"MT: Ssslumber Jiggy": {
				"item": "Jiggy",
			},
		}
	},
	"MT: Jade Snake Grove Left of Code Chamber Signpost Platform": {
		"locations": {
			"MT: Left of Code Chamber Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		}
	},
	"MT: Code Chamber": {
		"exits": {
			"MT: Jade Snake Grove": {}
		}
	},
	"MT: Open Code Chamber": {"macro": {"event"}},
	"MT: Wumba's Wigwam": {
		"locations": {
			"MT: Wumba's Wigwam Feather Nest 1": {
				"item": "FeatherNest",
			},
			"MT: Wumba's Wigwam Feather Nest 2": {
				"item": "FeatherNest",
			},
		},
		"exits": {
			"MT: Jade Snake Grove": {
				"id": -1
			},
			"MT: Wumba's Wigwam": {
				"logic": {
					"Banjo-Kazooie": {
						"Stony": "HumbaStony"
					}
				}
			}
		}
	},
	"MT: Prison Compound": {
		"locations": {
			"MT: Prison Compound Entrance Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Prison Compound Entrance Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Prison Compound Quicksand Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"MT: Prison Compound Warp Pad Tagged": {
				"item": "MTPrisonCompoundWarpPad",
			},
		},
		"exits": {
			"MT: Main Map": {},
			"MT: Warp Pads": {
				"logic": "MTPrisonCompoundWarpPad"
			},
			"MT: Prison Compound Underwater": {
				"logic": {
					"Banjo-Kazooie": "Dive or DiveSkip and BeakBuster",
					"Stony": "true"
				}
			},
			"MT: Prison Compound Moon Switch Pressed": {},
			"MT: Prison Compound Star Switch Pressed": {},
			"MT: Prison Compound Sun Switch Pressed": {},
			"MT: Prison Compound Cell Opened": {
				"logic": """
					MTPrisonCompoundMoonSwitchPressed
					and MTPrisonCompoundStarSwitchPressed
					and MTPrisonCompoundSunSwitchPressed
				"""
			},
			"MT: Prison Compound Top of Jail Cell": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie":"FlapFlip or TallJump and GripGrab or TalonTrot and Flutter and GripGrab",
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
			"MT: Prison Compound Cheato Page Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
			"MT: Prison Compound Inside Jail Cell": {
				"logic": "MTPrisonCompoundCellOpened"
			}
		}
	},
	"MT: Prison Compound Top of Jail Cell": {
		"locations": {
			"MT: Prison Compound Top of Prison Cell Feather Right Nest": {
				"item": "FeatherNest",
			},
			"MT: Prison Compound Top of Prison Cell Feather Left Nest": {
				"item": "FeatherNest",
				"logic": {
					"Banjo-Kazooie": "true",
					"Clockwork Kazooie": "TallJump"
				}
			},
		},
		"exits": {
			"MT: Prison Compound Swamp Jiggy Platform": {
				"logic": {
					"Banjo-Kazooie": "StiltStride and GripGrab and (FlapFlip or TallJump or TalonTrot and Flutter)"
				}
			},
			"MT: Prison Compound Cheato Page Platform": {
				"logic": {
					"Banjo-Kazooie": "GripGrab and (FlapFlip or TallJump or TalonTrot and Flutter)"
				}
			},
		}
	},
	"MT: Prison Compound Underwater": {
		"exits": {
			"MT: Prison Compound Pillar Area": {}
		}
	},
	"MT: Prison Compound Cheato Page Platform": {
		"locations": {
			"MT: Prison Compound Cheato Page": {
				"item": "CheatoPage",
			},
		},
		"exits": {
			"MT: Prison Compound Pillar Area": {}
		}
	},
	"MT: Prison Compound Swamp Jiggy Platform": {
		"locations": {
			"MT: Prison Compound Quicksand Jiggy": {
				"item": "Jiggy",
			},
		}
	},
	"MT: Prison Compound Pillar Area": {
		"locations": {
			"MT: Pillars Jiggy": {
				"logic": """
					MTPillarJiggyLowered and (TallJump or TalonTrot or FlapFlip or WonderwingJump)
					or HardJumps and TalonTrot and Flutter and BeakBuster
					or ClockworkShot
				""",
				"item": "Jiggy",
			},
			"MT: Prison Compound Pillars Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Prison Compound Pillars Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Prison Compound Pillars Egg Nest 3": {
				"item": "EggNest",
			},
			"MT: Pillars Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		},
		"exits": {
			"MT: Column Vaults": {
				"logic": {
					"Banjo-Kazooie": "BillDrill"
				}
			}
		}
	},
	"MT: Column Vaults": {
		"exits": {
			"MT: Prison Compound": {},
			"MT: Pillar Jiggy Lowered": {
				"logic": "AnyAttack"
			}
		}
	},
	"MT: Pillar Jiggy Lowered": {"macro": {"event"}},
	"MT: Prison Compound Sun Switch Pressed": {"macro": {"event"}},
	"MT: Prison Compound Star Switch Pressed": {"macro": {"event"}},
	"MT: Prison Compound Moon Switch Pressed": {"macro": {"event"}},
	"MT: Prison Compound Cell Opened": {"macro": {"event"}},
	"MT: Prison Compound Inside Jail Cell": {
		"exits": {
			"MT: Prison Compound Behind Jail Cell Boulder": {
				"logic": "MTPrisonCompoundJailCellBoulderBroken"
			},
			"MT: Prison Compound Jail Cell Boulder Broken": {
				"logic": {
					"Banjo-Kazooie": "BillDrill"
				}
			}
		}
	},
	"MT: Prison Compound Jail Cell Boulder Broken": {"macro": {"event"}},
	"MT: Prison Compound Behind Jail Cell Boulder": {
		# Transition to GGM
	},
}
