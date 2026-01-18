from .. import Regions
regions: Regions = {
	"Terrydactyland": {
		"id": 0x0112,
		"exits": {
			"IoH: Wasteland": {
				"id": 0x02,
				"groups":{"World Exits"},
				"logic": {
					"Banjo-Kazooie": "",
					"Talon Trot": "TalonTrotSmuggleCrossWorld",
				}
			},
			"Terrydactyland - Temp": {},
            "TDL: Ground Floor": {}
		},
	},
	"Terrydactyland - Temp": {
		"locations": {
			"TDL: Talon Torpedo Jinjo": {
				"item": "BlueJinjo",
			},
			"TDL: Entrance Jinjo": {
				"item": "BrownJinjo",
			},
			"TDL: Beside Rocknut Jinjo": {
				"item": "BlackJinjo",
			},
			"TDL: Big T. Rex Jinjo": {
				"item": "GreenJinjo",
			},
			"TDL: Stomping Plains Jinjo": {
				"item": "BrownJinjo",
			},
			"TDL: Under Terry's Nest Jiggy": {
				"item": "Jiggy",
			},
			"TDL: Dippy Jiggy": {
				"item": "Jiggy",
			},
			"TDL: Scrotty Jiggy": {
				"item": "Jiggy",
			},
			"TDL: Terry Jiggy": {
				"item": "Jiggy",
			},
			"TDL: Oogle Boogle Tribe Jiggy": {
				"item": "Jiggy",
			},
			"TDL: Chompas Belly Jiggy": {
				"item": "Jiggy",
			},
			"TDL: Terry's Kids Jiggy": {
				"item": "Jiggy",
			},
			"TDL: Stomping Plains Jiggy": {
				"item": "Jiggy",
			},
			"TDL: Rocknut Tribe Jiggy": {
				"item": "Jiggy",
			},
			"TDL: Code of the Dinosaurs Jiggy": {
				"item": "Jiggy",
			},
			"TDL: Unga Bunga Cave Entrance Glowbo": {
				"item": "HumbaTRex",
			},
			"TDL: Behind Mumbo's Skull Glowbo": {
				"item": "MumboEnlarge",
			},
			"TDL: Lakeside Honeycomb": {
				"item": "EmptyHoneycomb",
			},
			"TDL: Styracosaurus Cave Honeycomb": {
				"item": "EmptyHoneycomb",
			},
			"TDL: River Passage Honeycomb": {
				"item": "EmptyHoneycomb",
			},
			"TDL: Treble Clef": {
				"item": "TrebleClef",
			},
			"TDL: Train Switch": {
				"item": "TDLTrainStation",
			},
			"TDL: Dippy's Pool Cheato Page": {
				"item": "CheatoPage",
			},
			"TDL: Inside the Mountain Cheato Page": {
				"item": "CheatoPage",
			},
			"TDL: Boulder Cheato Page": {
				"item": "CheatoPage",
			},
			"TDL: Train Station Right Note": {
				"item": "NoteNest",
			},
			"TDL: Train Station Middle Note": {
				"item": "NoteNest",
			},
			"TDL: Train Station Left Note": {
				"item": "NoteNest",
			},
			"TDL: Lakeside Note 1": {
				"item": "NoteNest",
			},
			"TDL: Lakeside Note 2": {
				"item": "NoteNest",
			},
			"TDL: Lakeside Note 3": {
				"item": "NoteNest",
			},
			"TDL: Zig-Zag Path Note 1": {
				"item": "NoteNest",
			},
			"TDL: Zig-Zag Path Note 2": {
				"item": "NoteNest",
			},
			"TDL: Zig-Zag Path Note 3": {
				"item": "NoteNest",
			},
			"TDL: Roar Cage Path Note 1": {
				"item": "NoteNest",
			},
			"TDL: Roar Cage Path Note 2": {
				"item": "NoteNest",
			},
			"TDL: Roar Cage Path Note 3": {
				"item": "NoteNest",
			},
			"TDL: River Passage Note 1": {
				"item": "NoteNest",
			},
			"TDL: River Passage Note 2": {
				"item": "NoteNest",
			},
			"TDL: River Passage Note 3": {
				"item": "NoteNest",
			},
			"TDL: River Passage Note 4": {
				"item": "NoteNest",
			},
			"TDL: Springy Step Shoes Silo": {
				"item": "SpringyStepShoes",
			},
			"TDL: Taxi Pack Silo": {
				"item": "TaxiPack",
			},
			"TDL: Hatch Silo": {
				"item": "Hatch",
			},
			"TDL: Scrut (Lost)": {
				"item": "Nothing",
			},
			"TDL: Scrat (Sick)": {
				"item": "Nothing",
			},
			"TDL: Scrit (Small)": {
				"item": "Nothing",
			},
			"TDL: Baby T-Rex Roar": {
				"item": "BabyTRexRoar",
			},
			"TDL: Terry Mumbo Token": {
				"item": {"MumboToken":"'Terry' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Terry' in VictoryGoals",
				"locked": "true",
			},
			"TDL: Chompas Belly Mumbo Token": {
				"item": {"MumboToken":"'Chompas Belly' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Chompas Belly' in VictoryGoals",
				"locked": "true",
			},
			"TDL: Flight Pad Pillar Feather Nest 1": {
				"item": "FeatherNest",
			},
			"TDL: Flight Pad Pillar Feather Nest 2": {
				"item": "FeatherNest",
			},
			"TDL: Flight Pad Pillar Feather Nest 3": {
				"item": "FeatherNest",
			},
			"TDL: Alcove Near Waterfall Egg Nest 1": {
				"item": "EggNest",
			},
			"TDL: Alcove Near Waterfall Egg Nest 2": {
				"item": "EggNest",
			},
			"TDL: Top of the Mountain Egg Nest": {
				"item": "EggNest",
			},
			"TDL: Entrance Egg Nest": {
				"item": "EggNest",
			},
			"TDL: Path to Terry Egg Nest 1": {
				"item": "EggNest",
			},
			"TDL: Path to Terry Feather Nest 1": {
				"item": "FeatherNest",
			},
			"TDL: Path to Terry Egg Nest 2": {
				"item": "EggNest",
			},
			"TDL: Path to Terry Feather Nest 2": {
				"item": "FeatherNest",
			},
			"TDL: Left of Wall with Holes Egg Nest 1": {
				"item": "EggNest",
			},
			"TDL: Left of Wall with Holes Egg Nest 2": {
				"item": "EggNest",
			},
			"TDL: Right of Wall with Holes Egg Nest 1": {
				"item": "EggNest",
			},
			"TDL: Right of Wall with Holes Egg Nest 2": {
				"item": "EggNest",
			},
			"TDL: Near Shock Spring Pad Up the Mountain Egg Nest 1": {
				"item": "EggNest",
			},
			"TDL: Near Shock Spring Pad Up the Mountain Egg Nest 2": {
				"item": "EggNest",
			},
			"TDL: Near River Passage Entrance Egg Nest": {
				"item": "EggNest",
			},
			"TDL: Right of Scrotty Cave Egg Nest 1": {
				"item": "EggNest",
			},
			"TDL: Right of Scrotty Cave Egg Nest 2": {
				"item": "EggNest",
			},
			"TDL: Terry's Nest Egg Nest 1": {
				"item": "EggNest",
			},
			"TDL: Terry's Nest Egg Nest 2": {
				"item": "EggNest",
			},
			"TDL: Train Station Egg Nest 1": {
				"item": "EggNest",
			},
			"TDL: Train Station Egg Nest 2": {
				"item": "EggNest",
			},
			"TDL: Train Station Feather Nest 1": {
				"item": "FeatherNest",
			},
			"TDL: Train Station Feather Nest 2": {
				"item": "FeatherNest",
			},
			"TDL: Oogle Boogle Feather Nest 1": {
				"item": "FeatherNest",
			},
			"TDL: Oogle Boogle Feather Nest 2": {
				"item": "FeatherNest",
			},
			"TDL: Oogle Boogle Egg Nest 1": {
				"item": "EggNest",
			},
			"TDL: Oogle Boogle Egg Nest 2": {
				"item": "EggNest",
			},
			"TDL: Inside the Mountain Feather Nest 1": {
				"item": "FeatherNest",
			},
			"TDL: Inside the Mountain Feather Nest 2": {
				"item": "FeatherNest",
			},
			"TDL: Inside the Mountain Egg Nest 1": {
				"item": "EggNest",
			},
			"TDL: Inside the Mountain Egg Nest 2": {
				"item": "EggNest",
			},
			"TDL: River Passage Feather Nest": {
				"item": "FeatherNest",
			},
			"TDL: Styracosaurus Family Cave Feather Nest 1": {
				"item": "FeatherNest",
			},
			"TDL: Styracosaurus Family Cave Feather Nest 2": {
				"item": "FeatherNest",
			},
			"TDL: Styracosaurus Family Cave Feather Nest 3": {
				"item": "FeatherNest",
			},
			"TDL: Unga Bunga's Cave Feather Nest 1": {
				"item": "FeatherNest",
			},
			"TDL: Unga Bunga's Cave Feather Nest 2": {
				"item": "FeatherNest",
			},
			"TDL: Unga Bunga's Cave Feather Nest 3": {
				"item": "FeatherNest",
			},
			"TDL: Unga Bunga's Cave Egg Nest 1": {
				"item": "EggNest",
			},
			"TDL: Unga Bunga's Cave Egg Nest 2": {
				"item": "EggNest",
			},
			"TDL: Unga Bunga's Cave Egg Nest 3": {
				"item": "EggNest",
			},
			"TDL: Stomping Plains Middle Path Feather Nest": {
				"item": "FeatherNest",
			},
			"TDL: Stomping Plains Near Entrance Feather Nest": {
				"item": "FeatherNest",
			},
			"TDL: Stomping Plains Left Path Feather Nest 1": {
				"item": "FeatherNest",
			},
			"TDL: Stomping Plains Left Path Feather Nest 2": {
				"item": "FeatherNest",
			},
			"TDL: Stomping Plains Right Path Feather Nest 1": {
				"item": "FeatherNest",
			},
			"TDL: Stomping Plains Right Path Feather Nest 2": {
				"item": "FeatherNest",
			},
			"TDL: Stomping Plains Second Footprint Feather Nest": {
				"item": "FeatherNest",
			},
			"TDL: Bonfire Cavern Entrance Feather Nest": {
				"item": "FeatherNest",
			},
			"TDL: Bonfire Cavern Exit Feather Nest": {
				"item": "FeatherNest",
			},
			"TDL: Mumbo's Skull Feather Nest 1": {
				"item": "FeatherNest",
			},
			"TDL: Mumbo's Skull Feather Nest 2": {
				"item": "FeatherNest",
			},
			"TDL: Roar Cage Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"TDL: Inside The Mountain Near Cheato Page Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"TDL: Inside The Mountain Near Top Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"TDL: River Passage Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"TDL: World Entry and Exit Warp Pad Tagged": {
				"item": "TDLWorldEntryAndExitWarpPad",
			},
			"TDL: Stomping Plains Warp Pad Tagged": {
				"item": "TDLStompingPlainsWarpPad",
			},
			"TDL: Outside Mumbo's Skull Warp Pad Tagged": {
				"item": "TDLOutsideMumbosSkullWarpPad",
			},
			"TDL: Outside Wumba's Wigwam Warp Pad Tagged": {
				"item": "TDLOutsideWumbasWigwamWarpPad",
			},
			"TDL: Top of the Mountain Warp Pad Tagged": {
				"item": "TDLTopOfTheMountainWarpPad",
			},

			"TDL: Priceless Relic Thingy": {},
		},
		"exits": {
			"Train At TDL": {},
		}
	},
    "TDL: Ground Floor": {
        "exits": {
            "TDL: Outside Flight Pad Platform": {
                "logic": {
                    "BK Springy Step Shoes": "true",
                    "SK Springy Step Shoes": "true",
                    "Banjo-Kazooie": "HardJumps and TalonTrot and Flutter and BeakBusterJump",
                    "Talon Trot": {
						"Banjo-Kazooie": "HardJumps and Flutter and BeakBusterJump",
					},
                    "Kazooie": "EasyJumps and (TallJump or LegSpring or Glide)",
				},
			},
            "TDL: Entrance Jinjo Platform": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Clockwork Kazooie": "true"
					},
                    "Kazooie": {
                        "Clockwork Kazooie": "true"
					}
				}
			},
            "TDL: Inside the Mountain Ramp Tunnel": {},
            "TDL: Outside Train Station": {
                "logic": {
                    "Banjo-Kazooie": "HardJumps or TallJump or TalonTrot or FlapFlip or BeakBusterJump or WonderwingJump",
                    "Banjo": "true",
                    "Kazooie": "Jumps or TallJump or LegSpring or Glide",
                    "Talon Trot": "true",
                    "Mumbo": "HardJumps or TallJump",
                    "Baby T-Rex": "true"
				}
			},
            "TDL: Outside Train Station Right Note Platform": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "FlapFlip and (GripGrab or BeakBusterJump)",
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Banjo": "PackWhackJump and (TallJump or GripGrab)",
                    "Kazooie": {
                        "Kazooie": "LegSpring",
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Daddy T-Rex": "true"
				},
			},
            "TDL: Unga Bunga Spooked": {
                "logic": {
                    "Daddy T-Rex": "true"
				}
			},
            "TDL: In Front of Oogle Boogle Cave Behind the Unga Bunga": {
                "logic": {
                    "Banjo-Kazooie": "TDLUngaBungaSpooked or ClockworkWarp and GrenadeEggs and ThirdPersonEggShooting and EggAim",
                    "Banjo": "TDLUngaBungaSpooked",
                    "Kazooie": "TDLUngaBungaSpooked or ClockworkWarp and GrenadeEggs and ThirdPersonEggShooting and EggAim",
                    "Mumbo": "TDLUngaBungaSpooked",
                    "Baby T-Rex": "TDLUngaBungaSpooked",
				}
			},
            "TDL: Near Oogle Boogle Cave Split Up Platform": {
                "logic": {
					"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or WonderwingJump or BeakBusterJump or Flutter or AirRatatatRap or SlideJump",
                    "Talon Trot": "true",
                    "Banjo": "TallJump or PackWhackJump or SackPack or SlideJump or HardJumps",
                    "Kazooie": "true",
                    "Baby T-Rex": "true",
				}
			},
            "TDL: Upper Path Past Oogle Boogle Cave": {},
			"TDL: Upper Platform in Front of Wall With Holes": { # Clockwork walking through the loading zone in TDL: Wall With Holes Funny Clockwork Region
                "logic": {
                    "Banjo-Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
					},
				}
			},
            "TDL: Wall With Holes Jinjo Cell": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "ClockworkWarp and GrenadeEggs and ThirdPersonEggShooting and EggAim",
                        "Clockwork Kazooie": "ClockworkKazooieEggs and EggUse"
					},
                    "Kazooie": {
                        "Kazooie": "ClockworkWarp and GrenadeEggs and ThirdPersonEggShooting and EggAim",
                        "Clockwork Kazooie": "ClockworkKazooieEggs and EggUse"
					}
				}
			},
            "TDL: Outside Styracosaurus Family Cave": {
                "logic": {
                    "Banjo-Kazooie": "SlopeJump and (HardJumps or TallJump or Flutter or AirRatatatRap) or TalonTrot",
                    "Talon Trot": "true",
                    "Banjo": "SlopeJump and TallJump or PackWhackSlopeJump",
                    "Kazooie": "true",
                    "Mumbo": "SlopeJump and (TallJump or HardJumps)",
                    "Baby T-Rex": "true"
				}
			},
            "TDL: Outside Wumba's Wigwam": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or BeakBusterJump or WonderwingJump",
                        "Clockwork Kazooie": "ClockworkShot"
					},
					"Talon Trot": "true",
					"Banjo": "true",
                    "Kazooie": {
                        "Kazooie": "TallJump or LegSpring",
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Mumbo": "true",
                    "Baby T-Rex": "true",
                    "Daddy T-Rex": "true"
				}
			},
            "TDL: Outside Mumbo's Skull": {
                "logic": {
                    "Banjo-Kazooie": "DamageBoost or DragundaSidle and (TallJump or TalonTrot or FlapFlip or BeakBusterJump or WonderwingJump) or WonderwingDamageBoost or TDLOutsideMumboPlatformsEnlarged and (TallJump or TalonTrot or FlapFlip)",
                    "Talon Trot": "DragundaSidle or TDLOutsideMumboPlatformsEnlarged",
                    "Banjo": "DragundaSidle or DamageBoost or TDLOutsideMumboPlatformsEnlarged",
                    "Kazooie": "DragundaSidle and TallJump or DamageBoost or TDLOutsideMumboPlatformsEnlarged and TallJump or LegSpring or Glide",
                    "Mumbo": "DragundaSidle and TallJump or DamageBoost or TDLOutsideMumboPlatformsEnlarged and TallJump",
                    "Baby T-Rex": "true",
                    "Daddy T-Rex": "true"
				}
			},
            "TDL: Near Waterfall Nest Alcove": {
                "logic": {
                    "Banjo-Kazooie": "ClockworkShot",
                    "Kazooie": {
                        "Kazooie": "LegSpring",
                        "Clockwork Kazooie": "ClockworkShot"
					}
				},
			},
            "TDL: Ledge to the Right of Styracosaurus Cave": {
				"logic": {
                    "Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip",
                    "Banjo": "true",
                    "Kazooie": "TallJump or LegSpring",
                    "Talon Trot": "true",
                    "Mumbo": "TallJump",
                    "Baby T-Rex": "true"
				}
			},
            "TDL: Train Switch Platform": {
                "logic": {
                    "Banjo-Kazooie": "(TallJump or TalonTrot and Flutter) and GripGrab or FlapFlip",
                    "Banjo": "GripGrab or PackWhackJump and TallJump or SackPackAirJump",
                    "Kazooie": "true",
                    "Talon Trot": "Flutter and GripGrab",
                    "BK Springy Step Shoes": {
                        "Banjo-Kazooie": "true"
					},
                    "Baby T-Rex": "true",
                    "Daddy T-Rex": "true"
				}
			},
            "TDL: Dippy Pool": {
                "logic": {
                    "BK Springy Step Shoes": {
                        "Banjo-Kazooie": "Dive"
					}
				}
			},
            "TDL: Inside the Mountain": {},
            "TDL: Warp Pads": {
				"logic": "TDLWorldEntryAndExitWarpPad"
			},
            "TDL: Lakeside Honeycomb Platform": {
            	"logic": {
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "TallJump and GripGrab and TalonTrot and Flutter and BeakBusterJump and HardJumps",
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Banjo": "SackPack or TallJump and PackWhackJump",
                    "BK Turbo Trainers": "true",
                    "SK Turbo Trainers": "true",
                    "Kazooie": {
                        "Kazooie": "TallJump or LegSpring",
                        "Clockwork Kazooie": "ClockworkShot"
					},
				}
			},
            "TDL: On Rocknut Bridge": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Kazooie": {
                        "Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
            "TDL: Ground Floor": {
				"logic": {
                    "Banjo-Kazooie": {
                        "BK Turbo Trainers": "TurboTrainers",
                        "BK Springy Step Shoes": "SpringyStepShoes"
					},
                    "Kazooie": {
                        "BK Turbo Trainers": "TurboTrainers",
                        "SK Springy Step Shoes": "SpringyStepShoes"
					}
				}
			},
            "TDL: Entrance Pillar Button Pressed": {
                "logic": {
                    "Banjo-Kazooie": "GrenadeEggs and EggAim",
                    "Kazooie": "GrenadeEggs and EggAim"
				},
			},
		}
	},
    "TDL: On Entrance Pillar": {
        "exits": {
            "TDL: Entrance Pillar Button Pressed": {
                "logic": {
                    "Banjo-Kazooie": "GrenadeEggs and EggUse",
                    "Kazooie": "GrenadeEggs and EggUse"
				}
			},
		},
	},
    "TDL: Entrance Jinjo Platform": {},
    "TDL: Inside the Mountain Ramp Tunnel": {
        "exits": {
            "TDL: Ground Floor": {},
            "TDL: On Rocknut Bridge": {},
		}
	},
    "TDL: On Rocknut Bridge": {
        "exits": {
            "TDL: Ground Floor": {},
            "TDL: Inside the Mountain Ramp Tunnel": {},
            "TDL: Near Waterfall Nest Alcove": {
                "logic": {
                    "Banjo": "GripGrab or TallJump and PackWhackJump or SackPackAirJump",
                    "Kazooie": "TallJump or LegSpring or WingWhack or Glide",
                    "Banjo-Kazooie": "FlapFlip and GripGrab or HardTediousJumps and TalonTrot and (Flutter or AirRatatatRap) and BeakBusterJump",
                    "Talon Trot": {
                        "Banjo-Kazooie": "HardTediousJumps and (Flutter or AirRatatatRap) and BeakBusterJump"
					}
				}
			},
            "TDL: Bridge Rocknut Defeated": {
                "logic": {
                    "Banjo-Kazooie": "EasyJumps and ClockworkKazooieEggs and EggUse or ClockworkKazooieEggs and EggAim",
                    "Kazooie": "EasyJumps and ClockworkKazooieEggs and EggUse or ClockworkKazooieEggs and EggAim",
                    "Clockwork Kazooie": "true"
				},
			},
		},
	},
    "TDL: Near Waterfall Nest Alcove": {
        "exits": {
            "TDL: Ground Floor": {},
            "TDL: On Rocknut Bridge": {
                "logic": {
                    "Banjo": "GripGrab or TallJump and PackWhackJump or SackPackAirJump",
                    "Kazooie": "TallJump or LegSpring or WingWhack or Glide",
                    "Banjo-Kazooie": "FlapFlip and GripGrab or HardTediousJumps and TalonTrot and (Flutter or AirRatatatRap) and BeakBusterJump",
                    "Talon Trot": {
                        "Banjo-Kazooie": "HardTediousJumps and (Flutter or AirRatatatRap) and BeakBusterJump"
					}
				}
			}
		}
	},
    "TDL: Outside Train Station": {
        "exits": {
            "TDL: Train Station": {},
            "TDL: Ground Floor": {},
            "TDL: Outside Train Station Right Note Platform": {
                "logic": {
                    "Banjo": "TallJump or GripGrab or PackWhackJump or SackPackAirJump",
                    "Kazooie": {
                        "Kazooie": "TallJump or LegSpring",
                        "Clockwork Kazooie": "ClockworkShot"
                    },
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "TallJump or TalonTrot",
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Talon Trot": "true",
                    "Mumbo": "true",
                    "Baby T-Rex": "true",
                    "Daddy T-Rex": "true"
				}
			},
		},
	},
    "TDL: Train Station": {
        "exits": {
            "TDL: Ground Floor": {},
			"Train At TDL": {"logic": "Chuffy or TDLLevitateChuffyTheTrain"},
			"Chuffy's Cab": {
				"logic": {
					"Banjo-Kazooie": """
							TrainAtTDL and (
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
				"logic": "TrainAtTDL"
			},
            "TDL: Train Station Rocknut Defeated": {
                "logic": {
                    "Banjo-Kazooie": "EggAim and ClockworkKazooieEggs or DamageBoost and ClockworkKazooieEggs and EggUse and (TallJump or TalonTrot) and (Flutter or AirRatatatRap)",
                    "Kazooie": "EggAim and ClockworkKazooieEggs or DamageBoost and ClockworkKazooieEggs and EggUse"
				}
			}
		},
	},
    "TDL: Outside Train Station Right Note Platform": {
        "exits": {
            "TDL: Springy Step Shoes Silo Platform": {
                "logic": {
                    "Banjo-Kazooie": "FlapFlip and (BeakBusterJump or GripGrab)"
				}
			},
		}
	},
    "TDL: Springy Step Shoes Silo Platform": {},
    "TDL: In Front of Oogle Boogle Cave Behind the Unga Bunga": {
        "exits": {
            "TDL: Ground Floor": {
                "logic": {
                    "Banjo-Kazooie": "TDLUngaBungaSpooked or ClockworkWarp and GrenadeEggs and ThirdPersonEggShooting and EggAim",
                    "Banjo": "TDLUngaBungaSpooked",
                    "Kazooie": "TDLUngaBungaSpooked or ClockworkWarp and GrenadeEggs and ThirdPersonEggShooting and EggAim",
                    "Mumbo": "TDLUngaBungaSpooked",
                    "Baby T-Rex": "TDLUngaBungaSpooked",
				}
			},
            "TDL: Oogle Boogle Cave": {}
		}
	},
	"TDL: Upper Path Past Oogle Boogle Cave": {
        "exits": {
            "TDL: Ground Floor": {},
            "TDL: Unga Bunga Cave Near Springy Step Shoes": {},
            "TDL: River Passage": {},
            "TDL: Outside Wumba's Wigwam": {},
            "TDL: Upper Platform in Front of Wall With Holes": {
                "logic": {
                	"Kazooie": "Glide and EasyJumps"
				}
			},
            "TDL: Lakeside Honeycomb Platform": {
                "logic": {
                    "Kazooie": "EasyTediousJumps"
				}
			},
            "TDL: Unga Bunga Glowbo Platform": {
                "logic": {
                    "Banjo": "true",
                    "Kazooie": {
                        "Kazooie": "TallJump or LegSpring",
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or GripGrab or BeakBuster",
                    "Talon Trot": "true",
                    "Mumbo": "TallJump",
                    "Baby T-Rex": "true"
				}
			},
            "TDL: Outside Flight Pad Platform": {
                "logic": {
                    "Banjo-Kazooie": "HardTediousJumps and TalonTrot and Flutter and BeakBusterJump",
                    "Kazooie": "EasyJumps"
				}
			},
            "TDL: Near Roar Cage": {
                "logic": {
                    "Banjo": "PackWhackJump or SackPackAirJump",
                    "Kazooie": "true",
                    "Banjo-Kazooie": {
                        "Banjo-Kazooie": "TalonTrot or TallJump and (Flutter or AirRatatatRap) or SlideJump and TallJump and BeakBusterJump and EasyTediousJumps",
                        "Clockwork Kazooie": "ClockworkShot"
					},
                    "BK Springy Step Shoes": {
                        "Banjo-Kazooie": "true"
					},
                    "Baby T-Rex": "HardTediousJumps"
				}
			},
		}
	},
    "TDL: Oogle Boogle Cave": {
        "exits": {
            "TDL: In Front of Oogle Boogle Cave Behind the Unga Bunga": {},
            "TDL: Oogle Boogle Cave Gate Opened": {},
            "TDL: Oogle Boogle Cave Behind The Gate": {
                "logic": {
                    "Any": "TDLOogleBoogleCaveGateOpened"
				}
			},
		},
        "macro": {"splitup"}
	},
	"TDL: Near Oogle Boogle Cave Split Up Platform": {
        "exits": {
            "TDL: Ground Floor": {},
            "TDL: Upper Platform in Front of Wall With Holes": {
                "logic": {
                    "Banjo": "TallJump and GripGrab or PackWhackJump and SackPackAirJump",
                    "Kazooie": "TallJump or LegSpring",
                    "Baby T-Rex": "true",
                    "Mumbo": "TallJump"
				}
			},
		},
        "macro": {"splitup"}
	},
	"TDL: Upper Platform in Front of Wall With Holes": {
        "exits": {
            "TDL: Upper Platform in Front of Wall With Holes": {
                "logic": {
                    "Banjo-Kazooie": {
                        "Clockwork Kazooie": "ClockworkKazooieEggs and EggUse"
					},
                    "Kazooie": {
                        "Clockwork Kazooie": "ClockworkKazooieEggs and EggUse"
					}
				}
			},
            "TDL: Wall With Holes Rocknut Cell": {
                "logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		},
	},
	"TDL: Wall With Holes Jinjo Cell": {},
	"TDL: Wall With Holes Rocknut Cell": {},
    "TDL: Wall With Holes Funny Clockwork Region": {},
	"TDL: Outside Styracosaurus Family Cave": {},
	"TDL: Styracosaurus Family Cave": {},
	"TDL: Ledge to the Right of Styracosaurus Cave": {},
	"TDL: Outside Flight Pad Platform": {},
	"TDL: Flight": {},
    "TDL: Lakeside Honeycomb Platform": {},
	"TDL: Outside Wumba's Wigwam": {},
    "TDL: Wumba's Wigwam": {},
    "TDL: Oogle Boogle Cave Behind The Gate": {},
    "TDL: Unga Bunga Glowbo Platform": {},
	"TDL: River Passage": {},
    "TDL: River Passage Underwater": {},
    "TDL: River Passage Empty Honeycomb Slope": {},
    "TDL: River Passage Split Up Platform": {},
    "TDL: River Passage Slit": {},
    "TDL: Outside Mumbo's Skull": {},
    "TDL: Mumbo's Skull": {},
    "TDL: Train Switch Platform": {},
    "TDL: Dippy Pool": {},
    "TDL: Near Roar Cage": {},
    "TDL: Roar Cage Note Platforms": {},
    "TDL: Near Hatch Cave Entrance": {},
    "TDL: Unga Bunga Cave Near Hatch Silo": {},
    "TDL: Unga Bunga Cave Near Terry Egg": {},
    "TDL: Unga Bunga Cave Relic Room": {},
    "TDL: Unga Bunga Cave Near Springy Step Shoes": {},
    "TDL: Relic Ledge": {},
	"TDL: Inside the Mountain": {},
	"TDL: Inside the Mountain Chompa Platform Top": {},
	"TDL: Inside the Mountain Chompa Platform Bottom": {},
	"TDL: Inside the Mountain Underwater": {},
	"TDL: Inside the Mountain Flight Pad Platform": {},
	"TDL: Inside the Mountain Cheato Page Area": {},
	"TDL: Inside the Mountain Terry Egg Platform": {},
	"TDL: Inside the Mountain Split Up Pad Platform": {},
	"TDL: Inside the Mountain Near Gate Switch": {},
	"TDL: Path to Terry Start": {},
	"TDL: Path to Terry Second Segment": {},
	"TDL: Top of the Mountain": {},
	"TDL: Terry's Nest": {},
	"TDL: Terry's Nest Inside the Nest": {},
	"TDL: Terry's Nest": {},
	"TDL: Bonfire Cavern Entrance": {},
	"TDL: Bonfire Cavern Middle Platform": {},
	"TDL: Bonfire Cavern Exit": {},
	"TDL: Stomping Plains Start": {},
	"TDL: Stomping Plains Footprints": {},
	"TDL: Stomping Plains End": {},
	"TDL: Stomping Plains End on Shortcut Ledge": {},


	"TDL: Warp Pads": {},

	"TDL: Train Station Rocknut Defeated": {"macro": {"event"}},
	"TDL: Bridge Rocknut Defeated": {"macro": {"event"}},
	"TDL: Jail Cell Rocknut Defeated": {"macro": {"event"}},
	"TDL: Waterfall Cell Rocknut Defeated": {"macro": {"event"}},
	"TDL: Roar Cage Rocknut Defeated": {"macro": {"event"}},

    "TDL: Entrance Pillar Button Pressed": {"macro": {"event"}},
	"TDL: Scrit Boulder Broken": {"macro": {"event"}},
	"TDL: Styracosaurus Family Cave Empty Honeycomb Boulder Broken": {"macro": {"event"}},
    "TDL: Unga Bunga Spooked": {"macro": {"event"}},
    "TDL: Oogle Boogle Cave Gate Opened": {"macro": {"event"}},
	"TDL: Outside Mumbo Platforms Enlarged": {"macro": {"event"}},
    "TDL: Dippy Pool Filled": {"macro": {"event"}},
    "TDL: Unga Bunga Cave Gate Near Hatch Silo Opened": {"macro": {"event"}},
    "TDL: Unga Bunga Cave Gate Near Springy Step Shoes Opened": {"macro": {"event"}},
	"TDL: Inside the Mountain Path Raised": {"macro": {"event"}},
	"TDL: Inside the Mountain Gate Switch Pressed": {"macro": {"event"}},
	"TDL: Terry Defeated": {"macro": {"event"}},
	"TDL: Stomping Plains Solo Banjo Gate Opened": {"macro": {"event"}},
}
