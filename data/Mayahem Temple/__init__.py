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
		},
	},
    "Mayahem Temple: Main Map": {
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
                "logic": "MayahemTempleKillFlies"
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
            "Mayahem Temple: Top of Kickball Stadium": {
                "logic": {
					"Banjo-Kazooie": "FlapFlipSlideExtension and BeakBusterJump and Roll and FlapFlip and BeakBuster"
				}
			},
            "Mayahem Temple: Kill Flies": {
                "logic": {
                    "Banjo-Kazooie": """
						ShootLinearEggs
                        or ClockworkShot
						or BovinaWithFlapFlip
					"""
				}
			},
            "Mayahem Temple: Bovina Honeycomb": {
                "logic": {
                    "Banjo-Kazooie": """
                    	ClockworkShot
                        or FlapFlip and GripGrab
                        or BeakBusterJump and FlapFlip
                    """
				}
			},
            "Mayahem Temple: Top Platform Outside Treasure Chamber": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
                    }
				}
			},
            "Mayahem Temple: Top of Kickball Stadium": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
                    }
				}
			},
            "Mayahem Temple: Top of the Temple": {
                "logic": {
                    "Banjo-Kazooie": """
						TalonTrot
                        or HardJumps
					""",
                    "Talon Trot": "true"
				}
			},
            "Mayahem Temple: Targitzan's Temple Lobby": {
                "id": -1
			},
            "Mayahem Temple: Jade Snake Grove": {
                "logic": "MayahemTempleOpenJadeSnakeGrove",
                "explicit_logic": {
                    "Golden Goliath": "MayahemTempleOpenJadeSnakeGrove"
				}
			},
            "Mayahem Temple": {
                "logic": {
                    "Mumbo": {
                        "Golden Goliath": "MumboGoldenGoliath"
					}
				}
			},
            "Mayahem Temple: Open Jade Snake Grove": {
                "logic": {
                    "Golden Goliath": "true"
				}
			},
            "Mayahem Temple: Open Prison Compound": {
                "logic": {
                    "Golden Goliath": "true",
                    "Banjo-Kazooie": "ShootExplosives"
				}
			},
            "Mayahem Temple: Mumbo's Skull": {
                "id": -1,
			},
            "Mayahem Temple: Treasure Chamber Bottom": {
                "logic": "MayahemTempleOpenBottomTreasureChamberDoor",
                "id": -1
			},
            "Mayahem Temple: Warp Pads": {
                "logic": "MTWorldEntryAndExitWarpPad or MTOutsideMumbosSkullWarpPad"
			},
            "Mayahem Temple: Kickball Stadium": {
                "logic": {
                    "Stony": "true"
				}
			},
            "Mayahem Temple: Snake Heads": {
                "logic": {
					"Banjo-Kazooie": "(LinearEggs or ExtraClockworkUsage) and EggAim"
                }
			},
            "Mayahem Temple: Flight": {
                "logic": {
                    "Banjo-Kazooie": "MayahemTempleBreakFlightPadBoulder"
				}
			},
            "Mayahem Temple: Break Flight Pad Boulder": {
                "logic": {
                    "Banjo-Kazooie": "BillDrill",
                    "Golden Goliath": "true"
				}
			}
		}
	},
    "Mayahem Temple: Top of the Temple": {
        "locations": {
			"MT: Top of Temple Jiggy": {
				"item": "Jiggy",
			}
		}
	},
    "Mayahem Temple: Kill Flies": {"macro": {"event"}},
    "Mayahem Temple: Open Prison Compound": {"macro": {"event"}},
    "Mayahem Temple: Open Jade Snake Grove": {"macro": {"event"}},
    "Mayahem Temple: Break Flight Pad Boulder": {"macro": {"event"}},
    "Mayahem Temple: Bovina Honeycomb": {
        "locations": {
            "MT: Bovina Honeycomb": {
				"item": "EmptyHoneycomb",
			},
		}
	},
    "Mayahem Temple: Flight": {
        "exits": {
            "Mayahem Temple: Kill Flies": {
                "logic": {
					"Banjo-Kazooie":"""
						AirborneEggAiming and LinearEggs
						or ExtraClockworkUsage and AirborneEggAiming
					"""
                }
			},
            "Mayahem Temple: Snake Heads": {
                "logic": {
					"Banjo-Kazooie": """
						AirborneEggAiming and LinearEggs
						or ExtraClockworkUsage and AirborneEggAiming
					"""
                }
			},
            "Mayahem Temple: Top Platform Outside Treasure Chamber": {},
            "Mayahem Temple: Top of Kickball Stadium": {},
            "Mayahem Temple: Kickball Stadium": {
                "logic": {
                    "Banjo-Kazooie": "BeakBombClips"
				}
			},
            "Mayahem Temple: Jade Snake Grove": {
                "logic": {
                    "Banjo-Kazooie": "BeakBombClips"
				}
			},
            "Mayahem Temple: Bovina Honeycomb": {}
		}
	},
    "Mayahem Temple: Snake Heads": {
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
            "Mayahem Temple: Open Bottom Treasure Chamber Door": {
                "logic": "(MTSnakeHead, 6)"
			}
		}
	},
    "Mayahem Temple: Open Bottom Treasure Chamber Door": {"macro": {"event"}},
    "Mayahem Temple: Open Top Treasure Chamber Door": {"macro": {"event"}},
    "Mayahem Temple: Top Platform Outside Treasure Chamber": {
        "locations": {
			"MT: Treasure Chamber Cheato Page": {
				"item": "CheatoPage",
			},
		},
        "exits": {
            "Mayahem Temple": {},
            "Mayahem Temple: Treasure Chamber In Front of Unga Bunga Gate": {
                "id": -1,
                "logic": "MayahemTempleOpenTopTreasureChamberDoor"
			}
		}
	},
    "Mayahem Temple: Treasure Chamber Bottom": {
        "locations": {
            "MT: Treasure Chamber Jiggy": {
                "logic": "TDLPricelessRelicThingy",
				"item": "Jiggy",
			},
		},
        "exits": {
            "Mayahem Temple": {
                "id": -1
			},
            "Mayahem Temple: Treasure Chamber Honeycomb Pile": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot",
                        "Banjo-Kazooie": "TalonTrot",
                        "Talon Trot": "true"
                    }
				}
			},
            "Mayahem Temple: Open Top Treasure Chamber Door": {
                "logic": {
                    "Banjo-Kazooie": "true"
				}
			}
		}
	},
    "Mayahem Temple: Treasure Chamber Honeycomb Pile": {
        "locations": {
			"MT: Treasure Chamber Honeycomb": {
				"item": "EmptyHoneycomb",
			},
		},
        "exits": {
            "Mayahem Temple: Treasure Chamber Bottom": {},
            "Mayahem Temple: Treasure Chamber In Front of Unga Bunga Gate": {
                "logic": {
                    "Banjo-Kazooie": "FlapFlip and GripGrab and TallJump"
				}
			}
            
		}
	},
    "Mayahem Temple: Treasure Chamber In Front of Unga Bunga Gate": {
        "exits": {
            "Mayahem Temple: Treasure Chamber Honeycomb Pile": {
                "logic": {
                    "Banjo-Kazooie": "GripGrab"
				}
			},
            "Mayahem Temple: Top Platform Outside Treasure Chamber": {
                "logic": {
                    "Banjo-Kazooie": "TallJump"
				}
			},
            "Mayahem Temple: Treasure Chamber Behind Unga Bunga Gate": {
                "logic": "MayahemTempleTreasureChamberUngaBungaSwitchPressed"
			},
            "Mayahem Temple: Treasure Chamber Unga Bunga Switch Pressed": {},
		}
	},
    "Mayahem Temple: Treasure Chamber Behind Unga Bunga Gate": {
        # TODO: TDL transition
        "exits": {
            "Mayahem Temple: Treasure Chamber In Front of Unga Bunga Gate": {
                "logic": "MayahemTempleTreasureChamberUngaBungaSwitchPressed"
			},
		}
	},
    "Mayahem Temple: Treasure Chamber Unga Bunga Switch Pressed": {"macro": {"event"}},
    "Mayahem Temple: Top of Kickball Stadium": {
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
            "Mayahem Temple: Flight": {
                "logic": {
                    "Banjo-Kazooie": "FlightPad"
				}
			}
		}
	},
    "Mayahem Temple: Kickball Stadium": {
        "locations":{
			"MT: Kickball Jiggy": {
				"item": "Jiggy",
                "logic": "MayahemTempleKickballRound1Won and MayahemTempleKickballRound2Won and MayahemTempleKickballRound3Won"
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
            "Mayahem Temple": {
                "id": -1
			},
            "Mayahem Temple: Kickball Stadium Near Grate Switch": {
                "logic": "MayahemTempleKickballStadiumSwitchPressed"
			},
            "Mayahem Temple: Warp Pads": {
                "logic": "MTKickballStadiumLobbyWarpPad"
			},
            "Mayahem Temple: Kickball Round 1": {
                "logic": {
                    "Stony": "true"
				}
			},
            "Mayahem Temple: Kickball Round 2": {
                "logic": {
                    "Stony": "MayahemTempleKickballRound1Won"
				}
			},
            "Mayahem Temple: Kickball Round 3": {
                "logic": {
                    "Stony": "MayahemTempleKickballRound2Won"
				}
			},
            
		}
	},
    "Mayahem Temple: Kickball Round 1": {
		"locations": {
            "Mayahem Temple Kickball Round 1 Won": {}
		},
        "exits": {
            "Mayahem Temple: Kickball Stadium": {}
		}
	},
    "Mayahem Temple: Kickball Round 2": {
		"locations": {
            "Mayahem Temple Kickball Round 2 Won": {}
		},
        "exits": {
            "Mayahem Temple: Kickball Stadium": {}
		}
	},
    "Mayahem Temple: Kickball Round 3": {
		"locations": {
            "Mayahem Temple Kickball Round 3 Won": {}
		},
        "exits": {
            "Mayahem Temple: Kickball Stadium": {}
		}
	},
    "Mayahem Temple: Kickball Stadium Near Grate Switch": {
        #TODO: Add HFP entrance
        "exits": {
            "Mayahem Temple: Kickball Stadium": {
                "logic": "MayahemTempleKickballStadiumSwitchPressed"
			},
            "Mayahem Temple: Kickball Stadium Switch Pressed": {}
		}
	},
    "Mayahem Temple: Kickball Stadium Switch Pressed": {"macro": {"event"}},
    "Mayahem Temple: Mumbo's Skull": {
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
            "Mayahem Temple: Mumbo's Skull": {
                "logic": {
                    "Banjo-Kazooie": {"Mumbo": "MumboGoldenGoliath"}
				}
			},
            "Mayahem Temple": {}
		}
	},
    "Mayahem Temple: Warp Pads": {
        "exits": {
            "Mayahem Temple": {
                "logic": "MTWorldEntryAndExitWarpPad or MTOutsideMumbosSkullWarpPad"
			},
            "Mayahem Temple: Jade Snake Grove": {
                "logic": "MTNearWumbasWigwamWarpPad"
			},
            "Mayahem Temple: Prison Compound": {
                "logic": "MTPrisonCompoundWarpPad"
			},
            "Mayahem Temple: Kickball Stadium": {
                "logic": "MTKickballStadiumLobbyWarpPad"
			}
		}
	},
    "Mayahem Temple: Targitzan's Temple Lobby": {
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
			"Mayahem Temple": {},
            "Mayahem Temple: Targitzan's Temple": {
                "logic": {
                    "Banjo-Kazooie": "BreegullBlaster"
				}
			}
        }
	},
    "Mayahem Temple: Targitzan's Temple": {
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
            "Mayahem Temple: Targitzan's Temple Lobby": {},
            "Mayahem Temple: Slighty Sacred Chamber": {
                "logic": "(GreenRelic, 10)"
			},
            "Mayahem Temple: Really Sacred Chamber": {
                "logic": "(GreenRelic, 20)"
			}
		}
	},
    "Mayahem Temple: Slighty Sacred Chamber": {
        "locations": {
			"MT: Slighty Sacred Chamber Jiggy": {
				"item": "Jiggy",
			},
		},
        "exits": {
            "Mayahem Temple: Targitzan's Temple": {}
		}
	},
    "Mayahem Temple: Really Sacred Chamber": {
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
            "Mayahem Temple: Targitzan's Temple": {}
		}
	},
    "Mayahem Temple: Jade Snake Grove": {
        "locations": {
			"MT: Grip Grab Silo": {
				"item": "GripGrab",
			},
			"MT: Jade Snake Grove Glowbo": {
				"item": "WumbaStony",
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
            "Mayahem Temple": {},
            "Mayahem Temple: Wumba's Wigwam": {},
            "Mayahem Temple: Jade Snake Grove Top of Slope": {
                "logic": {
                    "Banjo-Kazooie": "TalonTrot",
					"Talon Trot": "true"
				}
			},
            "Mayahem Temple: Warp Pads": {
                "logic": "MTNearWumbasWigwamWarpPad"
			},
            "Mayahem Temple: Jade Snake Grove Top of Code Chamber Entrance": {
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
            "Mayahem Temple: Open Code Chamber": {
                "logic": {
                    "Golden Goliath": "true",
                    "Banjo-Kazooie": "ShootExplosives"
				}
			},
            "Mayahem Temple: Code Chamber": {
                "logic": "MayahemTempleOpenCodeChamber"
			},
            "Mayahem Temple: Jade Snake Grove Cheato Page Platform": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
					}
				}
			}
		}
	},
    "Mayahem Temple: Jade Snake Grove Top of Code Chamber Entrance": {
        "locations": {
            "MT: Jade Snake Grove Above Code Chamber Egg Nest": {
				"item": "EggNest",
			},
		}
	},
    "Mayahem Temple: Jade Snake Grove Top of Slope": {
        "exits": {
            "Mayahem Temple: Jade Snake Grove Ssslumber Jiggy Platform": {
                "logic": "FlapFlip and (GripGrab or BeakBusterJump)"
			},
            "Mayahem Temple: Jade Snake Grove Cheato Page Platform": {
                "logic": "FlapFlip and GripGrab"
			},
            "Mayahem Temple: Jade Snake Grove Left of Code Chamber Signpost Platform": {
                "logic": "FlapFlip and GripGrab"
			},
		}
	},
    "Mayahem Temple: Jade Snake Grove Cheato Page Platform": {
        "locations": {
			"MT: Jade Snake Grove Cheato Page": {
				"item": "CheatoPage",
			},
		}
	},
    "Mayahem Temple: Jade Snake Grove Ssslumber Jiggy Platform": {
        "locations": {
			"MT: Ssslumber Jiggy": {
				"item": "Jiggy",
			},
		}
	},
    "Mayahem Temple: Jade Snake Grove Left of Code Chamber Signpost Platform": {
        "locations": {
			"MT: Left of Code Chamber Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		}
	},
    "Mayahem Temple: Code Chamber": {
        "exits": {
            "Mayahem Temple: Jade Snake Grove": {}
		}
	},
    "Mayahem Temple: Open Code Chamber": {"macro": {"event"}},
    "Mayahem Temple: Wumba's Wigwam": {
        "locations": {
			"MT: Wumba's Wigwam Feather Nest 1": {
				"item": "FeatherNest",
			},
			"MT: Wumba's Wigwam Feather Nest 2": {
				"item": "FeatherNest",
			},
		},
        "exits": {
            "Mayahem Temple: Jade Snake Grove": {
                "id": -1
			},
            "Mayahem Temple: Wumba's Wigwam": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Stony": "HumbaStony"
					}
				}
			}
		}
	},
    "Mayahem Temple: Prison Compound": {
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
            "Mayahem Temple": {},
            "Mayahem Temple: Warp Pads": {
                "logic": "MTPrisonCompoundWarpPad"
			},
            "Mayahem Temple: Prison Compound Underwater": {
                "logic": {
					"Banjo-Kazooie": "Dive or DiveSkip and BeakBuster",
                    "Stony": "true"
				}
			},
            "Mayahem Temple: Prison Compound Moon Switch Pressed": {},
            "Mayahem Temple: Prison Compound Star Switch Pressed": {},
            "Mayahem Temple: Prison Compound Sun Switch Pressed": {},
            "Mayahem Temple: Prison Compound Cell Opened": {
                "logic": """
							MayahemTemplePrisonCompoundMoonSwitchPressed
							and MayahemTemplePrisonCompoundStarSwitchPressed
							and MayahemTemplePrisonCompoundSunSwitchPressed
						"""
			},
            "Mayahem Temple: Prison Compound Top of Jail Cell": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie":"FlapFlip or TallJump and GripGrab or TalonTrot and Flutter and GripGrab",
                        "Clockwork Kazooie": "ClockworkShot"
                    }
				}
			},
            "Mayahem Temple: Prison Compound Cheato Page Platform": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
                    }
				}
			},
            "Mayahem Temple: Prison Compound Inside Jail Cell": {
                "logic": "MayahemTemplePrisonCompoundCellOpened"
			}
		}
	},
    "Mayahem Temple: Prison Compound Top of Jail Cell": {
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
            "Mayahem Temple: Prison Compound Swamp Jiggy Platform": {
                "logic": {
                    "Banjo-Kazooie": "StiltStride and GripGrab and (FlapFlip or TallJump or TalonTrot and Flutter)"
				}
			},
            "Mayahem Temple: Prison Compound Cheato Page Platform": {
                "logic": {
                    "Banjo-Kazooie": "GripGrab and (FlapFlip or TallJump or TalonTrot and Flutter)"
				}
			},
		}
	},
    "Mayahem Temple: Prison Compound Underwater": {
        "exits": {
            "Mayahem Temple: Prison Compound Pillar Area": {}
		}
	},
    "Mayahem Temple: Prison Compound Cheato Page Platform": {
        "locations": {
			"MT: Prison Compound Cheato Page": {
				"item": "CheatoPage",
			},
		},
        "exits": {
            "Mayahem Temple: Prison Compound Pillar Area": {}
		}
	},
    "Mayahem Temple: Prison Compound Swamp Jiggy Platform": {
        "locations": {
			"MT: Prison Compound Quicksand Jiggy": {
				"item": "Jiggy",
			},
		}
	},
    "Mayahem Temple: Prison Compound Pillar Area": {
        "locations": {
			"MT: Pillars Jiggy": {
                "logic": """
					MayahemTemplePillarJiggyLowered and (TallJump or TalonTrot or FlapFlip or WonderwingJump)
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
            "Mayahem Temple: Column Vaults": {
                "logic": {
                    "Banjo-Kazooie": "BillDrill"
				}
			}
		}	
	},
    "Mayahem Temple: Column Vaults": {
        "exits": {
            "Mayahem Temple: Prison Compound": {},
            "Mayahem Temple: Pillar Jiggy Lowered": {
                "logic": "AnyAttack"
			}
		}
	},
    "Mayahem Temple: Pillar Jiggy Lowered": {"macro": {"event"}},
    "Mayahem Temple: Prison Compound Sun Switch Pressed": {"macro": {"event"}},
    "Mayahem Temple: Prison Compound Star Switch Pressed": {"macro": {"event"}},
    "Mayahem Temple: Prison Compound Moon Switch Pressed": {"macro": {"event"}},
    "Mayahem Temple: Prison Compound Cell Opened": {"macro": {"event"}},
    "Mayahem Temple: Prison Compound Inside Jail Cell": {
        "exits": {
            "Mayahem Temple: Prison Compound Behind Jail Cell Boulder": {
                "logic": "MayahemTemplePrisonCompoundJailCellBoulderBroken"
			},
            "Mayahem Temple: Prison Compound Jail Cell Boulder Broken": {
                "logic": {
                    "Banjo-Kazooie": "BillDrill"
				}
			}
		}
	},
    "Mayahem Temple: Prison Compound Jail Cell Boulder Broken": {"macro": {"event"}},
    "Mayahem Temple: Prison Compound Behind Jail Cell Boulder": {
        # Transition to GGM
	},
}
