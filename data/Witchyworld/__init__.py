from .. import Regions
regions: Regions = {
	"Witchyworld": {
		"id": 0x00D6,
		"exits": {
			"IoH: Pine Grove Behind Witchyworld Gate": {
				"id": 0x02,
				"groups":{"World Exits"},
				"logic": {
					"Banjo-Kazooie": "",
					"Talon Trot": "TalonTrotSmuggleCrossWorld",
				}
			},
            "WW: Main Map": {},
			"Witchyworld - Temp": {},
		},
	},
	"Witchyworld - Temp": {
		"locations": {
			"WW: Mrs. Boggy Jiggy": {
				"item": "Jiggy",
			},
		},
        "exits": {
            "WW: Groggy Fed": {},
            "WW: Groggy Quest Completed": {},
            "WW: Moggy Quest Completed": {},
            "WW: Soggy Quest Completed": {},
		}
	},
	"WW: Main Map": {
        "locations": {
			"WW: Treble Clef": {
				"item": "TrebleClef",
                "logic": {
                    "Van": "true",
					"Banjo-Kazooie": "ClockworkShotThroughGeometry",
                    "Kazooie": "ClockworkShotThroughGeometry"
				}
			},
            "WW: Around the Tent Note 1": {
				"item": "NoteNest",
			},
			"WW: Around the Tent Note 2": {
				"item": "NoteNest",
			},
			"WW: Around the Tent Note 3": {
				"item": "NoteNest",
			},
			"WW: Around the Tent Note 4": {
				"item": "NoteNest",
			},
			"WW: Around the Tent Note 5": {
				"item": "NoteNest",
			},
			"WW: Around the Tent Note 6": {
				"item": "NoteNest",
			},
			"WW: Around the Tent Note 7": {
				"item": "NoteNest",
			},
			"WW: Around the Tent Note 8": {
				"item": "NoteNest",
			},
			"WW: Outside Dodgem Dome Note 1": {
				"item": "NoteNest",
			},
			"WW: Outside Dodgem Dome Note 2": {
				"item": "NoteNest",
			},
			"WW: Crazy Castle Entrance Note 1": {
				"item": "NoteNest",
			},
			"WW: Crazy Castle Entrance Note 2": {
				"item": "NoteNest",
			},
			"WW: Airborne Egg Aiming Silo": {
				"item": "AirborneEggAiming",
                "logic": {"Banjo-Kazooie": "Notes >= ChosenMoveSiloCosts['Airborne Egg Aiming']"},
			},
			"WW: Split Up Silo": {
				"item": "SplitUp",
                "logic": {"Banjo-Kazooie": "Notes >= ChosenMoveSiloCosts['Split Up']"},
			},
			"WW: Near Mrs Boggy Egg Nest 1": {
				"item": "EggNest",
			},
			"WW: Near Mrs Boggy Egg Nest 2": {
				"item": "EggNest",
			},
			"WW: Outside Star Spinner Egg Nest 1": {
				"item": "EggNest",
			},
			"WW: Outside Star Spinner Egg Nest 2": {
				"item": "EggNest",
			},
			"WW: On Big Top Support Feather Nest 1": {
				"item": "FeatherNest",
			},
			"WW: On Big Top Support Feather Nest 2": {
				"item": "FeatherNest",
			},
			"WW: On Big Top Support Feather Nest 3": {
				"item": "FeatherNest",
			},
			"WW: On Big Top Support Feather Nest 4": {
				"item": "FeatherNest",
			},
			"WW: On Big Top Support Feather Nest 5": {
				"item": "FeatherNest",
			},
			"WW: On Big Top Support Feather Nest 6": {
				"item": "FeatherNest",
			},
            "WW: Dodgem Dome Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"WW: Madame Grunty Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"WW: Burger Stand Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"WW: Fries Stand Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"WW: Cactus of Strength Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"WW: World Entry and Exit Warp Pad Tagged": {
				"item": "WWWorldEntryAndExitWarpPad",
			},
			"WW: Behind the Big Top Tent Warp Pad Tagged": {
				"item": "WWBehindTheBigTopTentWarpPad",
			},
			"WW: Space Zone Warp Pad Tagged": {
				"item": "WWSpaceZoneWarpPad",
			},
			"WW: Western Ticket": {
				"item": "BigTopTicket",
                "logic": {
                    "Banjo-Kazooie": """
						ShootExplosives
						or ExtraAttacks and (
							BillDrill
							or EggUse and IceEggs and (
								BeakBuster
								or GroundRatatatRap
								or AirRatatatRap
							)
						)""",
					"Kazooie": "ShootExplosives or ExtraAttacks and EggUse and IceEggs and WingWhack",
                    "Van": "true"
				}
			},
			"WW: Spooky Ticket": {
				"item": "BigTopTicket",
                "logic": {
                    "Banjo-Kazooie": """
						ShootExplosives
						or ExtraAttacks and (
							BillDrill
							or EggUse and IceEggs and (
								BeakBuster
								or GroundRatatatRap
								or AirRatatatRap
							)
						)""",
					"Kazooie": "ShootExplosives or ExtraAttacks and EggUse and IceEggs and WingWhack",
                    "Van": "true"
				}
			},
			"WW: Space Ticket": {
				"item": "BigTopTicket",
                "logic": {
                    "Banjo-Kazooie": """
						ShootExplosives
						or ExtraAttacks and (
							BillDrill
							or EggUse and IceEggs and (
								BeakBuster
								or GroundRatatatRap
								or AirRatatatRap
							)
						)""",
					"Kazooie": "ShootExplosives or ExtraAttacks and EggUse and IceEggs and WingWhack",
                    "Van": "true"
				}
			},
			"WW: Entrance Ticket": {
				"item": "BigTopTicket",
                "logic": {
                    "Banjo-Kazooie": """
						ShootExplosives
						or ExtraAttacks and (
							BillDrill
							or EggUse and IceEggs and (
								BeakBuster
								or GroundRatatatRap
								or AirRatatatRap
							)
						)""",
					"Kazooie": "ShootExplosives or ExtraAttacks and EggUse and IceEggs and WingWhack",
                    "Van": "true"
				}
			},
		},
		"exits": {
			"WW: Area 51 Grate Blown Up": {
				"logic": {
					"Banjo-Kazooie": "ShootExplosives",
					"Kazooie": "ShootExplosives"
				}
			},
			"WW: Area 51": {
				"logic": "WWArea51GrateBlownUp",
				"explicit_logic": {
                    "BK Claw Clamber Boots": "WWArea51GrateBlownUp",
					"SK Claw Clamber Boots": "WWArea51GrateBlownUp"
				}
			},
			"WW: Area 51 Fence Left Note Post": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Kazooie": {
						"Clockwork Kazooie": "ClockworkShot",
						"Kazooie": "LegSpring or TallJump and HardJumps"
					}
				},
			},
			"WW: Area 51 Fence Right Note Post": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Kazooie": {
						"Clockwork Kazooie": "ClockworkShot",
						"Kazooie": "LegSpring or TallJump and HardJumps"
					},
				}
			},
			"WW: Inside The Big Top": {},
			"WW: On Top of Big Top": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TalonTrot",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Kazooie": {
						"Kazooie": "true",
					},
					"Van": "HardJumps and SlopeJump",
					"Talon Trot": "true"
				}
			},
			"WW: Crazy Castle Stockade": {},
            "WW: Cactus of Strength Jinjo Platform": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "FlapFlip and GripGrab",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Banjo": "PackWhackJump and TallJump and GripGrab",
                    "Kazooie": {
						"Kazooie": "LegSpring",
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
            "WW: Cactus of Strength Jiggy Platform": {
                "logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "Climb",
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Banjo": "Climb",
                    "Kazooie": "ClockworkShot"
				}
			},
            "WW: Cactus of Strength Won": {
                "logic": {
					"Banjo-Kazooie": "BeakBuster and BillDrill and GrenadeEggs and EggUse"
				}
			},
			"WW: Above The Ladder On The Gondola Platform": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb"
				}
			},
			"WW: Outside Wumba's Wigwam": {
				"logic": {
					"Banjo": "PackWhackJump and GripGrab and TallJump",
					"Banjo-Kazooie": "FlapFlip and GripGrab",
					"Kazooie": "LegSpring"
				}
			},
			"WW: Behind Bottom Van Door Near Wumba": {
				"logic": {
					"Van": "true"
				}
			},
            "WW: Dive Of Death Ladder Platform": {
                "logic": {
                    "Banjo": "Climb",
                    "Banjo-Kazooie": "Climb"
				}
			},
            "WW: Dive of Death Bucket": {
                "logic": {
                    "Banjo-Kazooie": "FlapFlip and (GripGrab or BeakBusterJump)",
                    "Banjo": "TallJump and PackWhackJump and GripGrab",
                    "Kazooie": "LegSpring"
				}
			},
            "WW: Dive Of Death Bucket Underwater": {
                "logic": {
                    "Banjo-Kazooie": "GroundRatATatClip or BeakBargeClip",
                    "Banjo": "PackWhackClip or TaxiPackClip"
				}
			},
			"WW: Train Station": {},
			"WW: Inferno Entrance Paid": {
				"logic": {
					"Van": "true"
				}
			},
			"WW: Behind Inferno Gate": {
				"logic": "WWInfernoEntrancePaid"
			},
			"WW: Haunted Caverns": {},
			"WW: Star Spinner": {},
			"WW: Dodgem Dome Powered": {
				"logic": {
					"Mumbo": "true"
				}
			},
			"WW: Dodgem Dome Lobby": {
				"logic": "WWDodgemDomePowered"
			},
            "WW: Above Dodgem Dome Entrance": {
                "logic": {
                    "Banjo-Kazooie": "TalonTrot"
				}
			},
			"WW: Warp Pads": {
				"logic": "WWWorldEntryAndExitWarpPad or WWBehindTheBigTopTentWarpPad or WWSpaceZoneWarpPad"
			},
			"WW: Fries Stand Switch Pressed": {}
		},
        "macro": {"splitup"}
	},
	"WW: Area 51": {
        "locations": {
			"WW: Van Door Jinjo": {
				"item": "YellowJinjo",
                "logic": {
                    "Van": "true",
					"Banjo-Kazooie": "ClockworkShotThroughGeometry",
                    "Kazooie": "ClockworkShotThroughGeometry"
				}
			},
			"WW: Area 51 Egg Nest 1": {
				"item": "EggNest",
			},
			"WW: Area 51 Egg Nest 2": {
				"item": "EggNest",
			},
		},
		"exits": {
			"WW: Area 51 Grate Blown Up": {
				"logic": {
					"Banjo-Kazooie": "ShootExplosives",
					"Kazooie": "ShootExplosives"
				}
			},
			"WW: Main Map": {
				"logic": "WWArea51GrateBlownUp"
			},
			"WW: Oogle Boogle Tunnel Entrance": {
				"logic": {
					"Banjo-Kazooie": "Climb and TallJump and TalonTrot and Flutter and HardJumps and BeakBusterJump",
					"BK Claw Clamber Boots": "true",
					"SK Claw Clamber Boots": "true"
				}
			},
			"WW: Saucer of Peril Powered": {
				"logic": {
					"Mumbo": "true"
				}
			},
			"WW: Area 51 Fence Left Note Post": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "Climb and EasyJumps and (Flutter or AirRatatatRap and BeakBusterJump)",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Kazooie": {
						"Kazooie": "LegSpring",
						"Clockwork Kazooie": "ClockworkShot"
					},
				}
			},
			"WW: Area 51 Fence Right Note Post": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TallJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Kazooie": {
						"Kazooie": "LegSpring or TallJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
				}
			},
		}
	},
	"WW: Area 51 Fence Right Note Post": {
        "locations": {
			"WW: Area 51 Gate Right Note": {
				"item": "NoteNest",
				"explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"WW: Main Map": {},
			"WW: Area 51": {},
		}
	},
	"WW: Area 51 Fence Left Note Post": {
        "locations": {
			"WW: Area 51 Gate Left Note": {
				"item": "NoteNest",
				"explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"WW: Main Map": {},
			"WW: Area 51": {},
		}
	},
	"WW: Inside The Big Top": {
		"exits": {
			"WW: Main Map": {},
			"WW: Inside The Big Top Past Conga": {
				"logic": {
					"Banjo-Kazooie": "(BigTopTicket, 4) and GrenadeEggs and AirborneEggAiming"
				}
			}
		}
	},
	"WW: Inside The Big Top Past Conga": {
        "locations": {
			"WW: Mr. Patch Jiggy": {
				"item": "Jiggy",
                "logic": {"Banjo-Kazooie": "EggAim and GrenadeEggs and FlightPad and AirborneEggAiming"}
			},
			"WW: Mr. Patch Mumbo Token": {
				"item": {"MumboToken":"'Mr. Patch' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Mr. Patch' in VictoryGoals",
				"locked": "true",
                "logic": {"Banjo-Kazooie": "EggAim and GrenadeEggs and FlightPad and AirborneEggAiming"}
			},
            "WW: Big Top Left Pack Feather Nest 1": {
				"item": "FeatherNest",
			},
			"WW: Big Top Left Pack Egg Nest 1": {
				"item": "EggNest",
			},
			"WW: Big Top Right Pack Feather Nest 1": {
				"item": "FeatherNest",
			},
			"WW: Big Top Right Pack Egg Nest 1": {
				"item": "EggNest",
			},
			"WW: Big Top Right Pack Feather Nest 2": {
				"item": "FeatherNest",
			},
			"WW: Big Top Left Pack Feather Nest 2": {
				"item": "FeatherNest",
			},
			"WW: Big Top Left Pack Egg Nest 2": {
				"item": "EggNest",
			},
			"WW: Big Top Right Pack Egg Nest 2": {
				"item": "EggNest",
			},
			"WW: Big Top Back Pack Feather Nest 1": {
				"item": "FeatherNest",
			},
			"WW: Big Top Back Pack Egg Nest 1": {
				"item": "EggNest",
			},
			"WW: Big Top Back Pack Egg Nest 2": {
				"item": "EggNest",
			},
			"WW: Big Top Back Pack Feather Nest 2": {
				"item": "FeatherNest",
			},
			"WW: Big Top Front Pack Egg Nest 1": {
				"item": "EggNest",
			},
			"WW: Big Top Front Pack Feather Nest 1": {
				"item": "FeatherNest",
			},
			"WW: Big Top Front Pack Feather Nest 2": {
				"item": "FeatherNest",
			},
			"WW: Big Top Front Pack Egg Nest 2": {
				"item": "EggNest",
			},
		},
		"exits": {
			"WW: Inside The Big Top": {}
		}
	},
	"WW: On Top of Big Top": {
        "locations": {
			"WW: Big Top Jinjo": {
				"item": "BlackJinjo",
				"explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"WW: Main Map": {
				"explicit_logic": {
					"BK Claw Clamber Boots": "true",
					"SK Claw Clamber Boots": "true"
				}
			},
			"WW: Burgers Stand Switch Pressed": {
				"logic": {
					"Kazooie": "EasyJumps and Glide",
				}
			},
			"WW: Area 51 Fence Left Note Post": {
				"logic": {
					"Kazooie": "EasyJumps and Glide"
				}
			},
			"WW: Area 51 Fence Right Note Post": {
				"logic": {
					"Kazooie": "EasyJumps and Glide"
				}
			},
			"WW: Saucer of Peril Platform": {
				"logic": {
					"Kazooie": "LegSpring and GlideExtension"
				}
			},
			"WW: Dive Of Death Bucket Underwater": {
				"logic": {
					"Kazooie": "HardJumps and DeathWarp and Glide"
				}
			},
			"WW: On Top of Big Top": {
				"logic": {
					"Banjo-Kazooie": {
						"BK Claw Clamber Boots": "ClawClamberBoots"
					},
					"Kazooie": {
						"SK Claw Clamber Boots": "true"
					}
				}
			},
		},
	},
	"WW: Outside Wumba's Wigwam": {
        "locations": {
			"WW: Wumba's Glowbo": {
				"item": "WumbaMoneyVan",
			},
			"WW: Outside Wumba's Wigwam Warp Pad Tagged": {
				"item": "WWOutsideWumbasWigwamWarpPad",
			},
		},
		"exits": {
			"GGM: Main Map": {},
			"WW: Wumba's Wigwam": {},
			"WW: Above The Ladder On The Gondola Platform": {
				"logic": {
					"Kazooie": "LegSpring and Glide"
				}
			},
			"WW: Warp Pads": {
				"logic": "WWOutsideWumbasWigwamWarpPad"
			},
		}
	},
	"WW: Above The Ladder On The Gondola Platform": {
		"exits": {
			"WW: Cactus of Strength Jinjo Platform": {
				"logic": {
					"Banjo-Kazooie": "TalonTrot and (Flutter or AirRatatatRap) and EasyJumps",
					"Kazooie": "true"
				}
			},
			"WW: Top Of The Gondola Platform": {
				"logic": {
					"Banjo-Kazooie": "FlapFlip and GripGrab or FlapFlip and BeakBusterJump",
					"Kazooie": "LegSpring",
					"Banjo": "TallJump and PackWhackJump and GripGrab"
				}
			},
            "WW: Space Zone Empty Honeycomb Platform": {
                "logic": {
                    "Banjo-Kazooie": "WWGondolaButtonPressed"
				}
			}
		}
	},
	"WW: Top Of The Gondola Platform": {
		"exits": {
			"WW: Space Zone Empty Honeycomb Platform": {
				"logic": {
				  	"Banjo-Kazooie": "TightropeWalk"
				},
			},
			"WW: Gondola Button Pressed": {
				"logic": {
					"Banjo-Kazooie": "GripGrab or TightropeWalk",
					"Kazooie": "TallJump and (WingWhack or Glide) or TightropeWalk"
				},
			},
		},
	},
	"WW: Cactus of Strength Jinjo Platform": {
        "locations": {
			"WW: Cactus of Strength Jinjo": {
				"item": "GreenJinjo",
				"explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		}
	},
	"WW: Cactus of Strength Jiggy Platform": {
        "locations": {
			"WW: Cactus of Strength Jiggy": {
				"item": "Jiggy",
                "logic": "WWCactusofStrengthWon",
				"explicit_logic": {
                    "Clockwork Kazooie": "WWCactusofStrengthWon"
				}
			},
		},
	},
	"WW: Crazy Castle Stockade": {
        "locations": {
			"WW: Hoop Hurry Jiggy": {
				"item": "Jiggy",
                "logic": {
                    "Banjo-Kazooie": "WWHoopHurryWon and (TallJump or EasyJumps and FlapFlip and BeakBusterJump) and FlapFlip",
                    "Kazooie": "WWHoopHurryWon and (TallJump and HardJumps or LegSpring)"
				}
			},
			"WW: Balloon Burst Jiggy": {
				"item": "Jiggy",
                "logic": {
                    "Banjo-Kazooie": "WWBalloonBurstWon and (TallJump or EasyJumps and FlapFlip and BeakBusterJump) and FlapFlip",
                    "Kazooie": "WWBalloonBurstWon and (TallJump and HardJumps or LegSpring)"
				}
			},
            "WW: Hoop Hurry Mumbo Token": {
				"item": {"MumboToken":"'Hoop Hurry' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Hoop Hurry' in VictoryGoals",
				"locked": "true",
                "logic": {
                    "Banjo-Kazooie": "WWHoopHurryWon and (TallJump or EasyJumps and FlapFlip and BeakBusterJump) and FlapFlip",
                    "Kazooie": "WWHoopHurryWon and (TallJump and HardJumps or LegSpring)"
				}
			},
			"WW: Balloon Burst Mumbo Token": {
				"item": {"MumboToken":"'Balloon Burst' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Balloon Burst' in VictoryGoals",
				"locked": "true",
                "logic": {
                    "Banjo-Kazooie": "WWHoopHurryWon and (TallJump or EasyJumps and FlapFlip and BeakBusterJump) and FlapFlip",
                    "Kazooie": "WWHoopHurryWon and (TallJump and HardJumps or LegSpring)"
				}
			},
			"WW: Pack Whack Silo": {
				"item": "PackWhack",
                "logic": {"Banjo-Kazooie": "Notes >= ChosenMoveSiloCosts['Pack Whack']"},
			},
			"WW: Crazy Castle Stockade Egg Nest 1": {
				"item": "EggNest",
			},
			"WW: Crazy Castle Stockade Egg Nest 2": {
				"item": "EggNest",
			},
		},
        "exits": {
            "WW: Main Map": {},
            "WW: Crazy Castle Stockade Grate Blown Up": {
                "logic": {
                    "Banjo-Kazooie": "ShootExplosives",
                    "Kazooie": "ShootExplosives"
				}
			},
            "WW: Crazy Castle Stockade Behind The Gate": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "(TallJump or TalonTrot or FlapFlip or WonderwingJump) and WWCrazyCastleStockadeGrateBlownUp",
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Banjo": "WWCrazyCastleStockadeGrateBlownUp",
                    "Kazooie": "(TallJump or LegSpring) and WWCrazyCastleStockadeGrateBlownUp",
                    "Mumbo": "TallJump and WWCrazyCastleStockadeGrateBlownUp",
                    "Van": "WWCrazyCastleStockadeGrateBlownUp"
				}
			},
            "WW: Crazy Castle Stockade Honeycomb Grab": {
                "logic": {
                    "Banjo": "TallJump and PackWhackClip"
				}
			},
            "WW: Crazy Castle Lobby": {
                "logic": "WWCrazyCastleInflated"
			}
		},
        "macro": {"splitup"}
	},
    "WW: Crazy Castle Lobby": {
        "exits": {
            "WW: Hoop Hurry": {
                "logic": {
                    "Kazooie": "true"
				},
			},
            "WW: Balloon Burst": {
                "logic": {
                    "Banjo-Kazooie": "AirborneEggAiming"
				},
			},
		}
	},
	"WW: Hoop Hurry": {
        "exits": {
            "WW: Hoop Hurry Won": {
                "logic": {
                    "Kazooie": "TurboTrainers or TightTimers" # Should I remove the tight timer?
				}
			},
		}
	},
	"WW: Balloon Burst": {
        "exits": {
            "WW: Balloon Burst Won": {
                "logic": "true"
			},
		}
	},
	"WW: Crazy Castle Stockade Behind The Gate": {
		"exits": {
            "WW: Crazy Castle Stockade Grate Blown Up": {
                "logic": {
                    "Banjo-Kazooie": "ShootExplosives",
                    "Kazooie": "ShootExplosives"
				}
			},
            "WW: Crazy Castle Stockade": {
                "logic": "WWCrazyCastleStockadeGrateBlownUp"
			},
            "WW: Pump Room": {},
            "WW: Crazy Castle Stockade Honeycomb Grab": {
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		}
	},
	"WW: Crazy Castle Stockade Honeycomb Grab": {
        "locations": {
			"WW: Crazy Castle Honeycomb": {
				"item": "EmptyHoneycomb",
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		}
	},
	"WW: Oogle Boogle Tunnel Entrance": {
        "exits": {
            "WW: Area 51": {},
            "WW: Area 51 Fence Left Note Post": {
                "logic": {
                    "Kazooie": "Glide and EasyTediousJumps",
				},
			},
            "WW: Area 51 Fence Right Note Post": {
                "logic": {
                    "Kazooie": "Glide and EasyTediousJumps",
				}
			},
            "WW: Burgers Stand Switch Pressed": {
                "logic": {
                    "Kazooie": "Glide and EasyTediousJumps",
				}
			},
            "TDL: Oogle Boogle Cave Behind The Gate": {
                "logic": {
					"Banjo-Kazooie": "true"
				}
			}
		}
	},
	"WW: Pump Room": {
        "locations": {
			"WW: Pump Room Feather Nest 1": {
				"item": "FeatherNest",
                "logic": {
                    "Banjo-Kazooie": "FlapFlip or ClockworkShot",
                    "Banjo": "PackWhackJump and TallJump or GripGrab",
					"Kazooie": "ClockworkShot or LegSpring"
				}
			},
			"WW: Pump Room Feather Nest 2": {
				"item": "FeatherNest",
                "logic": {
                    "Banjo-Kazooie": "FlapFlip or ClockworkShot",
                    "Banjo": "PackWhackJump and TallJump or GripGrab",
					"Kazooie": "ClockworkShot or LegSpring"
				}
			},
			"WW: Pump Room Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
                "logic": {
                    "Banjo-Kazooie": "FlapFlip",
                    "Banjo": "PackWhackJump and TallJump or GripGrab",
					"Kazooie": "LegSpring"
				}
			},
		},
        "exits": {
            "WW: Crazy Castle Stockade Behind The Gate": {},
            "WW: Pump Room Solo Banjo Switch": {
                "logic": {
					"Banjo": "true"
				}
			},
            "WW: Pump Room Solo Kazooie Switch": {
                "logic": {
                    "Kazooie": "true"
				}
			},
            "WW: Crazy Castle Inflated": {
                "logic": {
					"Kazooie": """
						forms_reach_regions({
							"Banjo": "WW: Pump Room Solo Banjo Switch",
							"Kazooie": "WW: Pump Room Solo Kazooie Switch",
						})
					""",
				},
			},
		},
        "macro": {"rejoin"}
	},
	"WW: Behind Bottom Van Door Near Wumba": {
        "exits": {
            "WW: Main Map": {
                "logic": {
                    "Van": "true"
				}
			},
            "WW: Behind Top Van Door Near Wumba": {},
		}
	},
	"WW: Behind Top Van Door Near Wumba": {
        "exits": {
            "WW: Outside Wumba's Wigwam": {
                "logic": {
                    "Van": "true"
				}
			},
            "WW: Behind Bottom Van Door Near Wumba": {},
		}
    },
	"WW: Wumba's Wigwam": {
        "exits": {
            "WW: Wumba's Wigwam": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Van": "HumbaMoneyVan"
					}
				}
			},
		}
	},
	"WW: Train Station": {
        "locations": {
			"WW: Train Switch": {
				"item": "WWTrainStation",
                "logic": {
                    "Banjo-Kazooie": "FlapFlip and GripGrab",
                    "Banjo": "PackWhackJump and TallJump",
					"Kazooie": "LegSpring"
				}
			},
			"WW: Train Station Egg Nest 1": {
				"item": "EggNest",
			},
			"WW: Train Station Egg Nest 2": {
				"item": "EggNest",
			},
		},
        "exits": {
            "WW: Main Map": {},
			"Train At WW": {"logic": "Chuffy or WWLevitateChuffyTheTrain"},
			"Chuffy's Cab": {
				"logic": {
					"Banjo-Kazooie": """
							TrainAtWW and (
							Climb and (
								TallJump
								or TalonTrot
								or FlapFlip
								or BeakBusterJump
							)
							or Climb and EasyJumps
							or (TallJump or TalonTrot or FlapFlip) and EasyJumps
							or BeakBusterJump
							or WonderwingJump
						)"""
				}
			},
			"Inside Chuffy's Wagon": {
				"logic": "TrainAtWW"
			},
		},
	},
	"WW: Dive of Death Bucket": {
        "exits": {
            "WW: Dive Of Death Bucket Underwater": {
                "logic": {
                    "Banjo-Kazooie": "(TallJump or GripGrab or EasyTediousJumps and DeathWarp) and (Dive or FlapFlip or BeakBuster)",
                    "Banjo": "(EasyTediousJumps and DeathWarp or TallJump) or (Dive or EasyJumps)",
                    "Kazooie": "LegSpring and (EasyTediousJumps and DeathWarp or TallJump)"
				}
			},
		}
	},
	"WW: Dive Of Death Bucket Underwater": {
        "locations": {
			"WW: Dive of Death Note 1": {
				"item": "NoteNest",
			},
			"WW: Dive of Death Note 2": {
				"item": "NoteNest",
			},
		}
	},
	"WW: Dive Of Death Ladder Platform": {
        "exits": {
            "WW: Dive Of Death Jiggy Platform": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "TightropeWalk or GripGrab",
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Banjo": "TightropeWalk or GripGrab",
				}
			},
		}
	},
	"WW: Dive Of Death Jiggy Platform": {
        "locations": {
			"WW: Dive of Death Jiggy": {
				"item": "Jiggy",
                "logic": {
                    "Banjo": "true",
					"Banjo-Kazooie": "FlapFlip or TalonTrot or TallJump and BeakBusterJump or TallJump and AirRatATatGrab or ClockworkShot"
				},
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		},
        "exits": {
            "WW: Dive of Death Bucket": {},
            "WW: Dive Of Death Bucket Underwater": {
                "logic": "EasyTediousJumps"
			},
		}
	},
	"WW: Behind Inferno Gate": {
        "exits": {
            "WW: Main Map": {
                "logic": "WWInfernoEntrancePaid"
			},
            "WW: Inferno Entrance": {},
		},
	},
	"WW: Inferno Entrance": {
        "locations": {
			"WW: The Inferno Jiggy": {
				"item": "Jiggy",
                "logic": {
                    "Banjo-Kazooie": "(TurboTrainers or TalonTrot) and FlapFlip and SlopeJump",
					"Banjo": "PackWhackSlopeJump and TallJump",
                    "Kazooie": """
                    			LegSpring and EasyJumps or TallJump and forms_reach_regions({
									"Banjo": "WW: Inferno Entrance",
									"Kazooie": "WW: Inferno Entrance",
								})""",
                    "Van": "HardTediousJumps and SlopeJump"
				}
			},
			"WW: The Inferno Cheato Page": {
				"item": "CheatoPage",
                "logic": {
                    "Van": "true",
					"Banjo-Kazooie": "ClockworkShotThroughGeometry",
                    "Kazooie": "ClockworkShotThroughGeometry"
				}
			},
			"WW: The Inferno Egg Nest 1": {
				"item": "EggNest",
			},
			"WW: The Inferno Egg Nest 2": {
				"item": "EggNest",
			},
		},
        "exits": {
            "WW: Behind Inferno Gate": {},
            "WW: Inferno Near Mumbo's Skull": {
                "logic": {
                    "Banjo-Kazooie": "DamageBoost or SlopeJump or TallJump or TalonTrot or FlapFlip or Flutter or AirRatatatRap or BeakBusterJump",
                    "Banjo": "DamageBoost or TallJump or PackWhackJump",
                    "Kazooie": "true",
                    "Mumbo": "DamageBoost or TallJump",
					"Talon Trot": "true"
				}
			},
            "WW: Inferno Entrance": {
                "logic": {
                    "Banjo-Kazooie": {
						"BK Turbo Trainers": "TurboTrainers"
					},
                    "Kazooie": {
						"SK Turbo Trainers": "TurboTrainers"
					},
				}
			}
		},
        "macro": {"splitup"}
	},
	"WW: Inferno Near Mumbo's Skull": {
        "locations": {
            "WW: The Inferno Glowbo": {
				"item": "MumboPower",
			},
			"WW: Outside Mumbo's Skull Warp Pad Tagged": {
				"item": "WWOutsideMumbosSkullWarpPad",
			},
		},
		"exits": {
            "WW: Inferno Entrance": {
                "logic": {
                    "Banjo-Kazooie": "DamageBoost or TallJump or TalonTrot or FlapFlip or Flutter or AirRatatatRap or BeakBusterJump",
                    "Banjo": "DamageBoost or TallJump or PackWhackJump",
                    "Kazooie": "true",
                    "Mumbo": "DamageBoost or TallJump",
					"Talon Trot": "true"
				}
			},
            "WW: Mumbo's Skull": {},
            "WW: Warp Pads": {
                "logic": "WWOutsideMumbosSkullWarpPad"
			},
            "WW: Inferno Spring Pad Button Pressed": {}
		},
	},
    "WW: Mumbo's Skull": {
        "locations": {
			"WW: Mumbo Skull Honeycomb": {
				"item": "EmptyHoneycomb",
			},
        },
        "exits": {
            "WW: Inferno Near Mumbo's Skull": {},
            "WW: Mumbo's Skull": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Mumbo": "MumboPower"
					}
				}
			},
		},
	},
	"WW: Haunted Caverns": {
        "locations": {
			"WW: The Haunted Cavern Cheato Page": {
				"item": "CheatoPage",
                "logic": {
                    "Banjo-Kazooie": "(DamageBoost or TallJump or TalonTrot and (Flutter or AirRatatatRap) or FlapFlip) and GripGrab or ClockworkShot",
                    "Banjo": "GripGrab",
					"Kazooie": "EasyJumps and LegSpring and Glide or ClockworkShot"
				}
			},
			"WW: The Haunted Caverns Egg Nest 1": {
				"item": "EggNest",
			},
			"WW: The Haunted Caverns Egg Nest 2": {
				"item": "EggNest",
			},
			"WW: The Haunted Caverns Egg Nest 3": {
				"item": "EggNest",
			},
			"WW: The Haunted Caverns Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		},
        "exits": {
            "WW: Main Map": {},
            "WW: Cave of Horrors": {},
		},
	},
	"WW: Cave of Horrors": {
        "locations": {
			"WW: Cave of Horrors Jinjo": {
				"item": "RedJinjo",
                "logic": {
                    "Banjo-Kazooie": "GrenadeEggs and (EggAim or ExtraThirdPersonEggShooting)",
                    "Kazooie": "GrenadeEggs and (EggAim or ExtraThirdPersonEggShooting)",
				}
			},

			"WW: Gobi Cage Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
                "logic": {
                    "Banjo-Kazooie": "GrenadeEggs and (EggAim or ExtraThirdPersonEggShooting)",
                    "Kazooie": "GrenadeEggs and (EggAim or ExtraThirdPersonEggShooting)",
				}
			},
		},
        "exits": {
            "WW: Gobi Freed": {
                "logic": {
                    "Banjo-Kazooie": "GrenadeEggs and (EggAim or ExtraThirdPersonEggShooting)",
                    "Kazooie": "GrenadeEggs and (EggAim or ExtraThirdPersonEggShooting)",
				}
			},
            "WW: Scrut Freed": {
                "logic": {
                    "Banjo-Kazooie": "GrenadeEggs and (EggAim or ExtraThirdPersonEggShooting)",
                    "Kazooie": "GrenadeEggs and (EggAim or ExtraThirdPersonEggShooting)",
				}
			},
            "WW: Haunted Caverns": {},
		},
	},
	"WW: Star Spinner": {
        "locations": {
			"WW: Star Spinner Jiggy": {
				"item": "Jiggy",
				"logic": {
                    "Banjo-Kazooie": """
						WWStarSpinnerPowered and (
							TalonTrot
							or TallJump and (Flutter or AirRatatatRap or HardJumps) and (ClockworkShot or HardJumps and SlopeJump)
                        )
					""",
                    "Banjo": "WWStarSpinnerPowered and TallJump and PackWhackJump and PackWhackSlopeJump",
                    "Talon Trot": "WWStarSpinnerPowered",
                    "Kazooie": "WWStarSpinnerPowered and (TallJump or LegSpring)",
					"Mumbo": "WWStarSpinnerPowered and (HardTediousJumps and TallJump and SlopeJump)",
					"Van": "WWStarSpinnerPowered and EasyTediousJumps and SlopeJump"
				}
			},
			"WW: Star Spinner Egg Nest": {
				"item": "EggNest",
			},
			"WW: Star Spinner Feather Nest 1": {
				"item": "FeatherNest",
			},
			"WW: Star Spinner Feather Nest 2": {
				"item": "FeatherNest",
			},
		},
        "exits": {
            "WW: Star Spinner Powered": {
                "logic": {
					"Mumbo": "true"
				}
			},
            "WW: Main Map": {},
		},
	},
	"WW: Dodgem Dome Lobby": {
        "locations": {
			"WW: Dodgem Dome Jiggy": {
				"item": "Jiggy",
                "logic": "WWDodgemDomeWon"
			},
			"WW: Dodgem Dome Mumbo Token": {
				"item": {"MumboToken":"'Dodgem Dome' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Dodgem Dome' in VictoryGoals",
				"locked": "true",
                "logic": "WWDodgemDomeWon"
			},
		},
        "exits": {
            "WW: Dodgem Dome Paid": {
                "logic": {
                    "Van": "true"
				}
			},
            "WW: Dodgem Dome Round 1": {
                "logic": {
					"Banjo-Kazooie": "WWDodgemDomePaid"
				}
			},
            "WW: Dodgem Dome Round 2": {
                "logic": {
					"Banjo-Kazooie": "WWDodgemDomeRound1Won"
				}
			},
            "WW: Dodgem Dome Round 3": {
                "logic": {
					"Banjo-Kazooie": "WWDodgemDomeRound2Won"
				}
			},

		},
	},
	"WW: Dodgem Dome Round 1": {
        "exits": {
			"WW: Dodgem Dome Lobby": {},
			"WW: Dodgem Dome Round 1 Won": {},
		}
	},
	"WW: Dodgem Dome Round 2": {
        "exits": {
			"WW: Dodgem Dome Lobby": {},
			"WW: Dodgem Dome Round 2 Won": {},
		}
	},
	"WW: Dodgem Dome Round 3": {
        "exits": {
			"WW: Dodgem Dome Lobby": {},
			"WW: Dodgem Dome Round 3 Won": {},
		}
	},
    "WW: Above Dodgem Dome Entrance": {
    	"exits": {
            "WW: Top Of Dodgem Dome Pipe": {
                "logic": {
                    "Banjo": "Climb",
                	"Banjo-Kazooie": "Climb"
				}
			},
		},
	},
    "WW: Top Of Dodgem Dome Pipe": {
        "exits": {
            "WW: Dodgem Dome Jinjo Platform": {
                "logic": {
                    "Banjo": "PackWhackSlopeJump",
                    "Kazooie": "true",
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "TalonTrot",
                        "Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
		},
	},
    "WW: Dodgem Dome Jinjo Platform": {
        "locations": {
			"WW: Dodgem Dome Jinjo": {
				"item": "OrangeJinjo",
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		}
	},
	"WW: Space Zone Under Empty Honeycomb Platform": {
        "exits": {
            "WW: Space Zone Empty Honeycomb Platform": {
                "logic": {
					"Banjo-Kazooie": "FlapFlip and (GripGrab or BeakBusterJump)",
                    "Kazooie": "LegSpring"
				}
			}
		}
	},
	"WW: Space Zone Empty Honeycomb Platform": {
        "locations": {
			"WW: Space Zone Honeycomb": {
				"item": "EmptyHoneycomb",
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		},
        "exits": {
            "WW: Cable To Saucer of Peril Platform": {
                "logic": {
                    "Banjo-Kazooie": "TalonTrot and Flutter and GripGrab"
				}
			},
            "WW: Saucer of Peril Button Pressed": {
                "logic": {
                    "Banjo-Kazooie": {
						"Egg": "EggAim and GrenadeEggs or ClockworkShot"
					}
				}
			},
            "WW: Saucer of Peril Platform": {
                "logic": {
                    "Banjo-Kazooie": "TalonTrot and Flutter and BeakBusterJump and TalonTrotSlideJump",
                    "Kazooie": "TallJump or Glide"
				}
			},
            "WW: Top Of Dodgem Dome Pipe": {
                "logic": {
                    "Kazooie": "LegSpring and Glide"
				}
			},
		}
	},
	"WW: Cable To Saucer of Peril Platform": {
        "exits": {
            "WW: Saucer of Peril Platform": {}
		}
	},
	"WW: Saucer of Peril Platform": {
        "locations": {
			"WW: Saucer of Peril Jiggy": {
				"item": "Jiggy",
                "logic": {
                    "Banjo-Kazooie": "GGMFuelDepotRocksBroken and WWSaucerofPerilButtonPressed and WWSaucerofPerilPowered"
				}
			},
			"WW: Saucer of Peril Cheato Page": {
				"item": "CheatoPage",
                "logic": {
                    "Banjo-Kazooie": "GGMFuelDepotRocksBroken and WWSaucerofPerilButtonPressed and WWSaucerofPerilPowered"
				}
			},
			"WW: Saucer of Peril Mumbo Token": {
				"item": {"MumboToken":"'Saucer of Peril' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Saucer of Peril' in VictoryGoals",
				"locked": "true",
                "logic": {
                    "Banjo-Kazooie": "GGMFuelDepotRocksBroken and WWSaucerofPerilButtonPressed and WWSaucerofPerilPowered"
				}
			},
		},
        "exits": {
            "WW: Saucer of Peril Platform Behind Gate": {
                "logic": "WWSaucerofPerilButtonPressed"
			},
            "WW: Saucer of Peril Button Pressed": {
                "logic": {
                    "Banjo-Kazooie": "BeakBarge or ShootExplosives",
                    "Kazooie": "ShootExplosives",
                    "Egg": "true",
					"Clockwork Kazooie": "true"
				}
			},
            "WW: Space Zone Under Empty Honeycomb Platform": {
                "logic": {
                    "Kazooie": "LegSpring and GlideExtension"
				}
			},
            "WW: Space Zone Empty Honeycomb Platform": {
                "logic": {
					"Banjo-Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
		}
	},
	"WW: Saucer of Peril Platform Behind Gate": {
        "exits": {
            "WW: Saucer of Peril Platform": {
                "logic": {
                    "Banjo-Kazooie": {
                    	"Banjo-Kazooie": "WWSaucerofPerilButtonPressed",
                        "Clockwork Kazooie": "ClockworkShotThroughGeometry"
					},
				},
			},
            "GGM: Fuel Depot Behind Rocks": {
                "logic": {
                    "Banjo-Kazooie": "true",
				}
			},
		}
	},

	"WW: Warp Pads": {
        "exits": {
			"WW: Main Map": {
                "logic": "WWWorldEntryAndExitWarpPad or WWBehindTheBigTopTentWarpPad or WWSpaceZoneWarpPad"
			},
			"WW: Outside Wumba's Wigwam": {
                "logic": "WWOutsideWumbasWigwamWarpPad"
			},
			"WW: Inferno Near Mumbo's Skull": {
                "logic": "WWOutsideMumbosSkullWarpPad"
			},
		}
	},
	"WW: Groggy Fed": {"macro": {"event"}},
	"WW: Groggy Quest Completed": {
		"locations": {
			"WW: Groggy": {
				"item": "Nothing",
			},
			"WW: Groggy Quest Completed": {}
		}
	},
	"WW: Moggy Quest Completed": {
		"locations": {
			"WW: Moggy": {
				"item": "Nothing",
			},
			"WW: Moggy Quest Completed": {}
		}
	},
	"WW: Soggy Quest Completed": {
		"locations": {
			"WW: Soggy": {
				"item": "Nothing",
			},
			"WW: Soggy Quest Completed": {}
		}
	},
	"WW: Crazy Castle Stockade Grate Blown Up": {"macro": {"event"}},
	"WW: Crazy Castle Inflated": {"macro": {"event"}},
	"WW: Hoop Hurry Won": {"macro": {"event"}},
	"WW: Balloon Burst Won": {"macro": {"event"}},
	"WW: Pump Room Solo Banjo Switch": {"macro": {"event"}},
	"WW: Pump Room Solo Kazooie Switch": {"macro": {"event"}},
	"WW: Cactus of Strength Won": {"macro": {"event"}},
	"WW: Area 51 Grate Blown Up": {"macro": {"event"}},
	"WW: Fries Stand Switch Pressed": {"macro": {"event"}},
	"WW: Burgers Stand Switch Pressed": {"macro": {"event"}},
	"WW: Gobi Freed": {"macro": {"event"}},
	"WW: Scrut Freed": {"macro": {"event"}},
	"WW: Saucer of Peril Powered": {"macro": {"event"}},
	"WW: Saucer of Peril Button Pressed": {"macro": {"event"}},
	"WW: Star Spinner Powered": {"macro": {"event"}},
	"WW: Inferno Entrance Paid": {"macro": {"event"}},
	"WW: Inferno Spring Pad Button Pressed": {"macro": {"event"}},
	"WW: Dodgem Dome Powered": {"macro": {"event"}},
	"WW: Dodgem Dome Paid": {"macro": {"event"}},
	"WW: Dodgem Dome Round 1 Won": {"macro": {"event"}},
	"WW: Dodgem Dome Round 2 Won": {"macro": {"event"}},
	"WW: Dodgem Dome Round 3 Won": {"macro": {"event"}},
	"WW: Gondola Button Pressed": {"macro": {"event"}},
}
