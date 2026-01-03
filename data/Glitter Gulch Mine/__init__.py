from .. import Regions
regions: Regions = {
	"Glitter Gulch Mine": {
		"id": 0x00C7,
		"exits": {
			"IoH: Plateau: Leaving GGM": {
				"id": 0x02,
				"groups":{"World Exits"},
			},
			"GGM: Main Map": {}
		},
	},
	"GGM: Main Map": {
		"locations": {
			"GGM: Boulder Jinjo": {
				"item": "BlackJinjo",
				"logic": {
					"Banjo-Kazooie": "TalonTrot and (BillDrill or EggBarge)",
					"Talon Trot": "BillDrill or EggBarge",
					"Banjo": "PackWhackSlopeJump and TaxiPackClip",
					"Detonator": "true"
				}
			},
			"GGM: Mine Tracks Jinjo": {
				"item": "PurpleJinjo",
			},
			"GGM: Canary Mary Jiggy": {
				"item": "Jiggy",
				"logic": {
					"Banjo-Kazooie": "GGMCanaryMaryFreed"
				},
			},
			"GGM: Canary Mary Cheato Page": {
				"logic": {
					"Banjo-Kazooie": "GGMCanaryMaryFreed"
				},
			},
			"GGM: Crushing Shed Jiggy": {
				"item": "Jiggy",
				"logic": "GGMLevitateTheCrushingShedBoulder and GGMCrushingShedButtonPressed"
			},
			"GGM: Crushing Shed Jiggy Chunk 1": {
				"item": "Nothing",
				"logic": "GGMLevitateTheCrushingShedBoulder and GGMCrushingShedButtonPressed"
			},
			"GGM: Crushing Shed Jiggy Chunk 2": {
				"item": "Nothing",
				"logic": "GGMLevitateTheCrushingShedBoulder and GGMCrushingShedButtonPressed"
			},
			"GGM: Crushing Shed Jiggy Chunk 3": {
				"item": "Nothing",
				"logic": "GGMLevitateTheCrushingShedBoulder and GGMCrushingShedButtonPressed"
			},
			"GGM: Waterfall Jiggy": {
				"item": "Jiggy",
				"logic": {
					"Banjo-Kazooie": "ClockworkShot",
					"BK Springy Step Shoes": "true",
					"Kazooie": "ClockworkShot or EasyJumps and (Glide or (TallJump or LegSpring) and WingWhack)",
					"SK Claw Clamber Boots": "true"
				}
			},
			"GGM: Near Entrance Glowbo": {
				"item": "HumbaDetonator",
			},
			"GGM: Mine Entrance 2 Glowbo": {
				"item": "MumboLevitate",
			},
			"GGM: Hill by Crushing Shed Note 1": {
				"item": "NoteNest",
				"logic": {
					"Banjo-Kazooie": "TalonTrot or ClockworkShot",
					"Talon Trot": "true",
					"Banjo": "PackWhackJump",
					"Kazooie": "true",
					"Detonator": "true",
				}
			},
			"GGM: Hill by Crushing Shed Note 2": {
				"item": "NoteNest",
				"logic": {
					"Banjo-Kazooie": "TalonTrot or ClockworkShot",
					"Talon Trot": "true",
					"Banjo": "PackWhackJump",
					"Kazooie": "true",
					"Detonator": "true",
				}
			},
			"GGM: Hill by Crushing Shed Note 3": {
				"item": "NoteNest",
				"logic": {
					"Banjo-Kazooie": "TalonTrot or ClockworkShot",
					"Talon Trot": "true",
					"Banjo": "PackWhackJump",
					"Kazooie": "true",
					"Detonator": "true",
				}
			},
			"GGM: Hill by Crushing Shed Note 4": {
				"item": "NoteNest",
				"logic": {
					"Banjo-Kazooie": "TalonTrot or ClockworkShot",
					"Talon Trot": "true",
					"Banjo": "PackWhackJump",
					"Kazooie": "true",
					"Detonator": "true",
				}
			},
			"GGM: Outside Ordnance Storage Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Outside Ordnance Storage Egg Nest 2": {
				"item": "EggNest",
			},
			"GGM: World Entry and Exit Warp Pad Tagged": {
				"item": "GGMWorldEntryAndExitWarpPad",
			},
			"GGM: Outside the Crushing Shed Warp Pad Tagged": {
				"item": "GGMOutsideTheCrushingShedWarpPad",
			},
			"GGM: Near the Train Station Warp Pad Tagged": {
				"item": "GGMNearTheTrainStationWarpPad",
			},
		},
		"exits": {
			"GGM: Outside Wumba's Wigwam": {
				"logic": {
					"Banjo-Kazooie": "TalonTrot",
					"Talon Trot": "true",
					"Detonator": "true",
					"Kazooie": "true",
					"Banjo": "PackWhackSlopeJump"
				}
			},
			"GGM: Fuel Depot Entrance": {},
			"GGM: Ordnance Storage Boulder Broken": {
				"logic": {
					"Banjo-Kazooie": "BillDrill",
					"Detonator": "true"
				}
			},
			"GGM: Ordnance Storage Lobby": {
				"logic": "GGMOrdnanceStorageBoulderBroken"
			},
			"GGM: Toxic Gas Cave": {},
			"GGM: Crushing Shed": {},
			"GGM: Water Storage": {},
			"GGM: Canary Cave Rocks Broken": {
				"logic": {
					"Detonator": "true"
				}
			},
			"GGM: Behind Rocks to Canary Cave": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "GGMCanaryCaveRocksBroken",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Detonator": "GGMCanaryCaveRocksBroken",
					"Banjo": "GGMCanaryCaveRocksBroken",
					"Kazooie": {
						"Kazooie": "GGMCanaryCaveRocksBroken",
						"Clockwork Kazooie": "ClockworkShot",
					},
					"Mumbo": "GGMCanaryCaveRocksBroken"
				}
			},
			"GGM: Both Canary Mary Races Won": {
				"logic": {
					"Banjo-Kazooie": "GGMCanaryMaryFreed"
				}
			},
			"GGM: Mine Entrance 2 Boulder Broken": {
				"logic": {
					"Banjo-Kazooie": "BillDrill",
					"Detonator": "true"
				}
			},
			"GGM: Gloomy Caverns Jail Cell Area": {
				"logic": "GGMMineEntrance2BoulderBroken"
			},
			"GGM: Gloomy Caverns 3 Tunnel Area": {},
			"GGM: Train Station": {},
			"GGM: Waterfall Cavern Entrance Opened": {
				"logic": {
					"Banjo-Kazooie": "TightTimers and TalonTrot or GGMWorldEntryAndExitWarpPad and GGMNearTheTrainStationWarpPad",
					"Talon Trot": "TightTimers",
					"BK Turbo Trainers": "true"
				}
			},
			"GGM: Waterfall Cavern Top Entrance": {
				"logic": "GGMWaterfallCavernEntranceOpened"
			},
			"GGM: Warp Pads": {
				"logic": "GGMWorldEntryAndExitWarpPad or GGMOutsideTheCrushingShedWarpPad"
			},
			"GGM: Main Map": {
				"logic": {
					"Banjo-Kazooie": {
						"BK Turbo Trainers": "TurboTrainers and (AnyAttack or ShootAnyEgg)",
						"BK Springy Step Shoes": "SpringyStepShoes and (AnyAttack or ShootAnyEgg)"
					},
					"Kazooie": {
						"SK Turbo Trainers": "TurboTrainers and (WingWhack or ShootAnyEgg)",
						"SK Springy Step Shoes": "SpringyStepShoes and (WingWhack or ShootAnyEgg)"
					}
				}
			},
			"GGM: Rocks Near Crushing Shed Broken": {
				"logic": {
					"Detonator": "true"
				}
			},
			"GGM: Behind Rocks to Flooded Caves": {
				"logic": "GGMRocksNearCrushingShedBroken"
			},
			"GGM: Near Prospector Bottom-Left Note Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "GripGrab or TallJump or TalonTrot or FlapFlip or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Talon Trot": "true",
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Banjo": "true",
					"Kazooie": {
						"Kazooie": "TallJump or LegSpring",
						"Clockwork Kazooie": "ClockworkShot"
					}
				},
			},
			"GGM: Near Prospector Bottom-Right Note Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "GripGrab or TallJump or TalonTrot or FlapFlip or SlopeJump and (Flutter or AirRatatatRap) or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Talon Trot": "true",
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Banjo": "true",
					"Kazooie": {
						"Kazooie": "TallJump or LegSpring",
						"Clockwork Kazooie": "ClockworkShot"
					}
				},
			},
			"GGM: Near Prospector Top-Right Note Platform": {
				"logic": {
					"Banjo-Kazooie": "TalonTrot or SlopeJump",
					"Talon Trot": "true",
					"Kazooie": "true",
					"Detonator": "true",
					"Banjo": "PackWhackSlopeJump",
					"Mumbo": "SlopeJump",
					"BK Turbo Trainers": "true"
				}
			},
			"GGM: Bill Drill Silo Nest Platforms": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "(TallJump or TalonTrot and Flutter or WonderwingJump) and GripGrab or (TallJump or TalonTrot and Flutter) and BeakBusterJump or FlapFlip",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Talon Trot": {
						"Banjo-Kazooie": "Flutter and GripGrab or Flutter and BeakBusterJump"
					},
					"Banjo": "GripGrab or PackWhackJump",
					"Kazooie": {
						"Kazooie": "LegSpring",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Detonator": "true"
				}
			},
			"GGM: Outside Mumbo's Skull Left Note Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or GripGrab and HardJumps or BeakBusterJump or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Banjo": "true",
					"Kazooie": {
						"Kazooie": "TallJump or LegSpring or Glide and EasyJumps",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Talon Trot": "true"
				}
			},
			"GGM: Outside Mumbo's Skull Warp Pad Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or GripGrab and HardJumps or BillDrillJump or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Banjo": "true",
					"Kazooie": {
						"Kazooie": "TallJump or LegSpring or Glide and EasyJumps",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Talon Trot": "true"
				}
			},

			"GGM: Outside Mumbo's Skull Bottom-Right Note Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TalonTrot or FlapFlip or GripGrab and HardJumps or TallJump and BeakBusterJump or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Banjo": "true",
					"Kazooie": {
						"Kazooie": "TallJump or LegSpring or Glide and EasyJumps",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Talon Trot": "true"
				}
			},
			"GGM: Near Prospector Top-Right Note Platform": {
				"logic": {
					"Kazooie": "Glide and EasyJumps"
				}
			},
			"GGM: Outside Mumbo's Skull": {
				"logic": {
					"Kazooie": "Glide and EasyJumps"
				}
			},
			"GGM: On Entrance Cheato Page Portal": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TalonTrot and TallJump and BeakBusterJump and (Flutter or AirRatatatRap) and HardTediousJumps",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Detonator": "HardTediousJumps",
					"SK Turbo Trainers": "HardTediousJumps and TallJump and WingWhack",
					"BK Springy Step Shoes": {},
					"SK Springy Step Shoes": {},
					"Banjo": "HardTediousJumps and TallJump and PackWhackJump",
					"Kazooie": {
						"Kazooie": "Glide and EasyJumps or GlideExtension",
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
			"GGM: Levitate The Crushing Shed Boulder": {
				"logic": {
					"Mumbo": "true"
				}
			}
		},
		"macro": {"rejoin"}
	},
	"GGM: Falling When Entering": {
		"exits": {
			"GGM: Main Map": {},
			"GGM: On Entrance Rope": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb"
				}
			},
			"GGM: On Entrance Cheato Page Portal": {
				"logic": {
					"Banjo-Kazooie": "EasyTediousJumps and (Flutter and BeakBusterJump)",
					"Kazooie": "true",
					"Banjo": "PackWhackJump and TallJump"
				}
			},
		}
	},
	"GGM: On Entrance Rope": {
		"exits": {
			"IoH: Plateau": {
				"logic": {
					"Banjo-Kazooie": "true"
				}
			},
			"GGM: Main Map": {},
			"GGM: On Entrance Cheato Page Portal": {
				"logic": {
					"Banjo-Kazooie": "TallJump and (Flutter or AirRatatatRap)",
					"Banjo": "TallJump and PackWhack"
				}
			},
		},
	},
	"GGM: On Entrance Cheato Page Portal": {
		"locations": {
			"GGM: Entrance Cheato Page": {
				"item": "CheatoPage",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Main Map": {},
		}
	},
	"GGM: Behind Rocks to Flooded Caves": {
		"exits": {
			"GGM: Main Map": {
				"logic": "GGMRocksNearCrushingShedBroken"
			},
			"GGM: Flooded Caves Above Water Near Crushing Shed Exit": {},
		}
	},
	"GGM: Outside Wumba's Wigwam": {
		"exits": {
			"GGM: Main Map": {},
			"GGM: Wumba's Wigwam": {},
		}
	},
	"GGM: Wumba's Wigwam": {
		"locations": {
			"GGM: Inside Wumba's Wigwam Warp Pad Tagged": {
				"item": "GGMInsideWumbasWigwamWarpPad",
			},
		},
		"exits": {
			"GGM: Wumba's Wigwam": {
				"logic": {
					"Banjo-Kazooie": {
						"Detonator": "HumbaDetonator"
					}
				}
			},
			"GGM: Warp Pads": {
				"logic": "GGMInsideWumbasWigwamWarpPad"
			},
			"GGM: Outside Wumba's Wigwam": {}
		}
	},
	"GGM: Warp Pads": {
		"exits": {
			"GGM: Main Map": {
				"logic": "GGMWorldEntryAndExitWarpPad or GGMOutsideTheCrushingShedWarpPad or GGMNearTheTrainStationWarpPad"
			},
			"GGM: Wumba's Wigwam": {
				"logic": "GGMInsideWumbasWigwamWarpPad"
			},
			"GGM: Outside Mumbo's Skull Warp Pad Platform": {
				"logic": "GGMOutsideMumbosSkullWarpPad"
			}
		}
	},
	"GGM: Fuel Depot Entrance": {
		"locations": {
			"GGM: Fuel Depot Front-Left Note": {
				"item": "NoteNest",
				"logic": {
					"Banjo-Kazooie": "EasyJumps or TallJump or TalonTrot or FlapFlip or ClockworkShot or AirRatATatGrab or BreegullBashGrab or WonderwingJump",
					"Kazooie": "EasyJumps or TallJump or LegSpring or ClockworkShot",
					"Banjo": "true",
					"Talon Trot": "true",
					"Mumbo": "true",
					"Detonator": "true"
				}
			},
			"GGM: Fuel Depot Back-Right Note": {
				"item": "NoteNest",
			},
			"GGM: Fuel Depot Front-Right Note": {
				"item": "NoteNest",
				"logic": {
					"Banjo-Kazooie": "EasyJumps or TallJump or TalonTrot or FlapFlip or ClockworkShot or AirRatATatGrab or BreegullBashGrab or WonderwingJump",
					"Kazooie": "EasyJumps or TallJump or LegSpring or ClockworkShot",
					"Banjo": "true",
					"Talon Trot": "true",
					"Mumbo": "true",
					"Detonator": "true"
				}
			},
		},
		"exits": {
			"GGM: Main Map": {},
			"GGM: Fuel Depot In Front of Rocks": {
				"logic": {
					"Banjo-Kazooie": "TallJump or FlapFlip or TalonTrot or HardJumps and GripGrab or WonderwingJump",
					"Talon Trot": "true",
					"Banjo": "true",
					"Kazooie": "TallJump or LegSpring",
					"Mumbo": "TallJump",
					"Detonator": "true"
				}
			},
			"GGM: Fuel Depot Back-Left Note Barrel": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TallJump or FlapFlip or TalonTrot or HardJumps and GripGrab or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Talon Trot": "true",
					"Banjo": "true",
					"Kazooie": {
						"Kazooie": "TallJump or LegSpring",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Mumbo": "TallJump",
					"Detonator": "true"
				},
			},
		}
	},
	"GGM: Fuel Depot Back-Left Note Barrel": {
		"locations": {
			"GGM: Fuel Depot Back-Left Note": {
				"item": "NoteNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Fuel Depot In Front of Rocks": {
				"logic": {
					"Banjo-Kazooie": "GripGrab"
				}
			}
		}
	},
	"GGM: Fuel Depot In Front of Rocks": {
		"exits": {
			"GGM: Fuel Depot Back-Left Note Barrel": {},
			"GGM: Fuel Depot Entrance": {},
			"GGM: Fuel Depot Rocks Broken": {
				"logic": {
					"Detonator": "true"
				}
			},
			"GGM: Fuel Depot Behind Rocks": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "GGMFuelDepotRocksBroken",
						"Clockwork Kazooie": "ClockworkShotThroughGeometry and EggAim"
					},
					"Talon Trot": "GGMFuelDepotRocksBroken",
					"Detonator": "GGMFuelDepotRocksBroken",
					"Mumbo": "GGMFuelDepotRocksBroken",
					"Banjo": "GGMFuelDepotRocksBroken",
					"Kazooie": {
						"Kazooie": "GGMFuelDepotRocksBroken",
						"Clockwork Kazooie": "ClockworkShotThroughGeometry and EggAim"
					}
				},
			},
		}
	},
	"GGM: Fuel Depot Behind Rocks": {
		"locations": {
			"GGM: Fuel Depot Egg Nest 1": {
				"item": "EggNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
			"GGM: Fuel Depot Egg Nest 2": {
				"item": "EggNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
			"GGM: Fuel Depot Egg Nest 3": {
				"item": "EggNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
			"GGM: Fuel Depot Feather Nest 1": {
				"item": "FeatherNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
			"GGM: Fuel Depot Feather Nest 2": {
				"item": "FeatherNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
			"GGM: Fuel Depot Feather Nest 3": {
				"item": "FeatherNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Fuel Depot In Front of Rocks": {
				"logic": "GGMFuelDepotRocksBroken"
			},
			"WW: Saucer of Peril Platform Behind Gate": {
				"logic": {
					"Banjo-Kazooie": "true",
					"Talon Trot": "true"
				}
			},
		}
	},
	"GGM: Ordnance Storage Lobby": {
		"locations": {
			"GGM: Ordnance Storage Jiggy": {
				"item": "Jiggy",
				"logic": "GGMOrdnanceStorageWon"
			},
			"GGM: Beak Bayonet Silo": {
				"item": "BeakBayonet",
				"logic": {"Banjo-Kazooie": "Notes >= ChosenMoveSiloCosts['Beak Bayonet']"},
			},
			"GGM: Ordnance Storage Mumbo Token": {
				"item": {"MumboToken":"'Ordnance Storage' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Ordnance Storage' in VictoryGoals",
				"locked": "true",
			},
			"GGM: Ordnance Storage Lobby Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Ordnance Storage Lobby Egg Nest 2": {
				"item": "EggNest",
			},
			"GGM: Ordnance Storage Lobby Egg Nest 3": {
				"item": "EggNest",
			},
		},
		"exits": {
			"GGM: Ordnance Storage": {
				"logic": {
					"Banjo-Kazooie": "BeakBayonet and BreegullBlaster"
				}
			},
			"GGM: Main Map": {},
		}
	},
	"GGM: Ordnance Storage": {
		"exits": {
			"GGM: Ordnance Storage Won": {},
		}
	},
	"GGM: Toxic Gas Cave": {
		"locations": {
			"GGM: Toxic Gas Cave Jinjo": {
				"item": "BlueJinjo",
			},
			"GGM: Toxic Gas Cave Honeycomb": {
				"item": "EmptyHoneycomb",
				"logic": {
					"Banjo-Kazooie": "BillDrill",
					"Detonator": "true"
				}
			},
			"GGM: Toxic Gas Cave Egg Nest": {
				"item": "EggNest",
				"logic": {
					"Banjo-Kazooie": "BillDrill or GroundRatATatClip or BeakBargeClip",
					"Banjo": "TaxiPackClip or PackWhackClip",
					"Detonator": "true"
				}
			},
			"GGM: Toxic Gas Cave Feather Nest": {
				"item": "FeatherNest",
				"logic": {
					"Banjo-Kazooie": "BillDrill or GroundRatATatClip or BeakBargeClip",
					"Banjo": "TaxiPackClip or PackWhackClip",
					"Detonator": "true"
				}
			},
			"GGM: Toxic Gas Cave Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		},
		"exits": {
			"GGM: Main Map": {},
		}
	},
	"GGM: Crushing Shed": {
		"locations": {
			"GGM: Crushing Shed Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Crushing Shed Egg Nest 2": {
				"item": "EggNest",
			},
		},
		"exits": {
			"GGM: Main Map": {},
			"GGM: Crushing Shed Button Pressed": {
				"logic": {
					"Banjo-Kazooie": "BeakBarge"
				}
			},
		}
	},
	"GGM: Water Storage": {
		"locations": {
			"GGM: Treble Clef": {
				"item": "TrebleClef",
				"logic": {
					"Banjo-Kazooie": "Dive",
					"Banjo": "Dive",
					"Kazooie": "LegSpringDive"
				}
			},
		},
		"exits": {
			"GGM: Main Map": {},
			"GGM: Waterfall Cavern Bottom Entrance": {},
			"GGM: Water Storage On Top Of Jinjo Tank": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
			"GGM: Water Storage On Top Of Cheato Page Tank": {
				"logic": {
					"Banjo-Kazooie": "FlapFlip and (GripGrab or BeakBusterJump) and Climb",
					"Banjo": "HardJumps and TallJump and PackWhackJump and GripGrab and Climb",
					"Kazooie": "HardJumps and LegSpring and WingWhack and GlideExtension"
				}
			},
		}
	},
	"GGM: Water Storage On Top Of Jinjo Tank": {
		"locations": {
			"GGM: Water Storage Jinjo": {
				"item": "BrownJinjo",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
			"GGM: Water Storage On Top Of Jinjo Tank Egg Nest": {
				"item": "EggNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Water Storage": {},
			"JRL: Water Supply (Glitter Gulch Mine) GGM Side": {
				"logic": {
					"Banjo-Kazooie": "Climb"
				}
			}
		}
	},
	"GGM: Water Storage On Top Of Cheato Page Tank": {
		"locations": {
			"GGM: Water Storage Cheato Page": {
				"item": "CheatoPage",
				"logic": {
					"Banjo-Kazooie": "Dive",
					"Banjo": "ShackPack or Dive",
					"Kazooie": "LegSpringDive"
				}
			},
		},
		"exits": {
			"GGM: Water Storage On Top Of Jinjo Tank": {
				"logic": {
					"Banjo": "TallJump and PackWhackJump and SackPackAirJump and SackPackEndingJump",
					"Kazooie": "GlideExtension"
				}
			}
		}
	},
	"GGM: Behind Rocks to Canary Cave": {
		"exits": {
			"GGM: Main Map": {
				"logic": "GGMCanaryCaveRocksBroken"
			},
			"GGM: Canary Cave": {
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			}
		}
	},
	"GGM: Canary Cave": {
		"locations": {
			"GGM: Canary Cave Back-Left Egg Nest": {
				"item": "EggNest",
			},
			"GGM: Canary Cave Front-Right Egg Nest": {
				"item": "EggNest",
				"logic": {
					"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or BeakBusterJump or GripGrab or ClockworkShot or WonderwingJump",
					"Banjo": "true",
					"Kazooie": "TallJump or LegSpring or EasyJumps or ClockworkShot",
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Talon Trot": "true"
				}
			},
			"GGM: Canary Cave Front-Left Feather Nest": {
				"item": "FeatherNest",
				"logic": {
					"Banjo-Kazooie": "GripGrab or AnyAttack or ShootAnyEgg",
					"Banjo": "PackWhack",
					"Kazooie": "WingWhack or ShootAnyEgg",
					"Mumbo": "true",
					"Detonator": "true"
				}
			},
			"GGM: Canary Cave Back-Right Feather Nest": {
				"item": "FeatherNest",
				"logic": {
					"Banjo-Kazooie": "GripGrab or AnyAttack or ShootAnyEgg",
					"Banjo": "PackWhack",
					"Kazooie": "WingWhack or ShootAnyEgg",
					"Mumbo": "true",
					"Detonator": "true"
				}
			},
		},
		"exits": {
			"GGM: Behind Rocks to Canary Cave": {},
			"GGM: Canary Mary Freed": {
				"logic": {
					"Banjo-Kazooie": "BeakBarge or ShootExplosives or AirRatatatRap or GroundRatatatRap",
					"Banjo": "PackWhack",
					"Kazooie": "true",
					"Detonator": "true",
					"Mumbo": "true"
				},
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		}
	},
	"GGM: Gloomy Caverns Jail Cell Area": {
		"locations": {
			"GGM: Jail Jinjo": {
				"item": "BlackJinjo",
				"logic": {
					"Banjo-Kazooie": "ClockworkShot",
					"Kazooie": "ClockworkShot",
					"Detonator": "true"
				}
			},
			"GGM: Gloomy Caverns Jail Cell Feather Nest": {
				"item": "FeatherNest",
			},
		},
		"exits": {
			"GGM: Main Map": {},
			"GGM: Gloomy Caverns Outside Power Hut Area": {
				"logic": "GGMGloomyCavernNearJailCellRocksBroken"
			},
			"GGM: Gloomy Cavern Near Jail Cell Rocks Broken": {
				"logic": {
					"Detonator": "true"
				}
			},
		}
	},
	"GGM: Gloomy Caverns Outside Power Hut Area": {
		"locations": {
			"GGM: Gloomy Caverns Near Power Hut Egg Nest 1": {
				"item": "EggNest",
				"logic": {
					"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or BeakBusterJump or ClockworkShot or WonderwingJump",
					"Talon Trot": "true",
					"Banjo": "true",
					"Kazooie": "TallJump or LegSpring or EasyJumps and Glide or ClockworkShot",
					"Mumbo": "TallJump",
					"Detonator": "true"
				}
			},
			"GGM: Gloomy Caverns Near Power Hut Egg Nest 2": {
				"item": "EggNest",
				"logic": {
					"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or BeakBusterJump or ClockworkShot or WonderwingJump",
					"Talon Trot": "true",
					"Banjo": "true",
					"Kazooie": "TallJump or LegSpring or EasyJumps and Glide or ClockworkShot",
					"Mumbo": "TallJump",
					"Detonator": "true"
				}
			},
			"GGM: Gloomy Caverns Near Second Boulder Egg Nest": {
				"item": "EggNest",
			},
			"GGM: Gloomy Cavern Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
				"logic": {
					"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or BeakBusterJump or ClockworkShot or WonderwingJump",
					"Talon Trot": "true",
					"Banjo": "true",
					"Kazooie": "TallJump or LegSpring or ClockworkShot",
					"Mumbo": "TallJump",
					"Detonator": "true"
				}
			},
		},
		"exits": {
			"GGM: Power Hut Ground Floor": {},
			"GGM: Gloomy Cavern Near Power Hut Rocks Broken": {
				"logic": {
					"Detonator": "true"
				}
			},
			"GGM: Gloomy Caverns 3 Tunnel Area": {
				"logic": "GGMGloomyCavernNearPowerHutRocksBroken"
			},
		}
	},
	"GGM: Gloomy Caverns 3 Tunnel Area": {
		"exits": {
			"GGM: Main Map": {},
			"GGM: Generator Cavern": {},
			"GGM: Gloomy Caverns Outside Power Hut Area": {
				"logic": "GGMGloomyCavernNearPowerHutRocksBroken"
			},
		}
	},
	"GGM: Power Hut Ground Floor": {
		"locations": {
			"GGM: Power Hut Feather Nest": {
				"item": "FeatherNest",
			},
		},
		"exits": {
			"GGM: Power Hut Top Floor": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb"
				}
			},
			"GGM: Power Hut Basement": {},
			"GGM: Gloomy Caverns Outside Power Hut Area": {},
		},
	},
	"GGM: Power Hut Top Floor": {
		"exits": {
			"GGM: Power Hut Ground Floor": {},
		}
	},
	"GGM: Power Hut Basement": {
		"locations": {
			"GGM: Power Hut Basement Jiggy": {
				"item": "Jiggy",
				"logic": {
					"Banjo-Kazooie": "RoomsInTheDark",
					"Banjo": "RoomsInTheDark",
					"Mumbo": "RoomsInTheDark",
					"Detonator": "RoomsInTheDark",
					"Kazooie": """
						RoomsInTheDark
						or forms_reach_regions({
							"Banjo": "GGM: Power Hut Top Floor",
							"Kazooie": "GGM: Power Hut Basement",
						}) and not RoomsInTheDark
					""",
				},
			},
		},
		"exits": {
			"GGM: Power Hut Ground Floor": {}
		}
	},
	"GGM: Generator Cavern": {
		"locations": {
			"GGM: Generator Cavern Jiggy": {
				"item": "Jiggy",
				"logic": {
					"Banjo-Kazooie": """
							(
								FireEggs and EggAim
								or RoomsWithLimitedLighting and (BillDrill or ShootExplosives or DragonBreath or EggUse and (FireEggs or GrenadeEggs))
								or RoomsInTheDark
							)
							and
							(
								TallJump
								or TalonTrot
								or HardJumps and BeakBusterJump
								or FlapFlipSlideExtension
							)
						or
							FlapFlip and BeakBusterJump and Climb
						or
							ClockworkShot
						or
							RoomsInTheDark and WonderwingJump
					""", # or EasyTediousJumps and WonderwingJump and FeathersCheat and RoomsWithLimitedLighting
					"Banjo": """
						RoomsInTheDark and (PackWhackJump or SackPackAirJump or TallJump)
						or EasyJumps and TallJump and PackWhackJump and Climb
					""",
					"Kazooie": """
							(
								FireEggs and EggAim
								or RoomsWithLimitedLighting and (ShootExplosives or DragonBreathSoloKazooie or EggUse and (FireEggs or GrenadeEggs))
								or RoomsInTheDark
							)
							and (TallJump or LegSpring)
						or
							ClockworkShot
					""",
					"Mumbo": "RoomsInTheDark and TallJump",
					"Detonator": "RoomsInTheDark",
					"Talon Trot": "RoomsInTheDark"
				},
			},
			"GGM: Generator Cavern Egg Nest": {
				"item": "EggNest",
			},
			"GGM: Generator Cavern Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		},
		"exits": {
			"GGM: Gloomy Caverns 3 Tunnel Area": {},
		}
	},
	"GGM: Train Station": {
		"locations": {
			"GGM: Train Station Honeycomb": {
				"item": "EmptyHoneycomb",
				"logic": {
					"Banjo-Kazooie": "ShootAnyEgg or AnyAttack",
					"Banjo": "PackWhack",
					"Kazooie": "WingWhack",
					"Mumbo": "true",
					"Detonator": "true"
				}
			},
			"GGM: Train Station Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Train Station Egg Nest 2": {
				"item": "EggNest",
			},
			"GGM: Train Station Feather Nest 1": {
				"item": "FeatherNest",
			},
			"GGM: Train Station Feather Nest 2": {
				"item": "FeatherNest",
			},
		},
		"exits": {
			"GGM: Levitate Chuffy The Train": {},
			"GGM: Main Map": {},
			"Train At GGM": {"logic": "Chuffy or GGMLevitateChuffyTheTrain"},
			"Chuffy's Cab": {
				"logic": {
					"Banjo-Kazooie": """
							TrainAtGGM and (
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
				"logic": {
					"Banjo-Kazooie": """
							TrainAtGGM and (
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
						)""",
					"Detonator": "true",
					"Banjo": "GripGrab or EasyJumps and TallJump or PackWhackJump",
					"Kazooie": "EasyJumps and TallJump or LegSpring",
					"Mumbo": "EasyJumps and TallJump"
				},
			},
		}
	},
	"GGM: Waterfall Cavern Top Entrance": {
		"exits": {
			"GGM: Main Map": {},
			"GGM: Waterfall Cavern Top Pool": {},
			"GGM: Waterfall Cavern Jiggy Ramp": {
				"logic": {
					"Banjo-Kazooie": "HardTediousJumps and DamageBoost or EasyTediousJumps and (Flutter or AirRatatatRap)",
					"Kazooie": "EasyTediousJumps",
					"Banjo": "HardTediousJumps",
					"Mumbo": "HardTediousJumps",
				}
			},
			"GGM: Waterfall Cavern Side Entrance": {
				"logic": {
					"BK Turbo Trainers": {
						"Banjo-Kazooie": "EasyTediousJumps and DamageBoost"
					}
				}
			},
		}
	},
	"GGM: Waterfall Cavern Top Pool": {
		"exits": {
			"GGM: Waterfall Cavern Bottom Entrance": {},
			"GGM: Waterfall Cavern Jiggy Ramp": {
				"logic": {
					"Banjo": "PackWhackJump or SackPackAirJump",
					"Kazooie": "TallJump or LegSpring",
					"Mumbo": "TallJump",
					"Detonator": "true"
				}
			}
		},
	},
	"GGM: Waterfall Cavern Jiggy Ramp": {
		"locations": {
			"GGM: Waterfall Cavern Jiggy": {
				"item": "Jiggy",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Waterfall Cavern Side Entrance": {
				"logic": {
					"Banjo-Kazooie": "EasyTediousJumps and RollJump and TallJump and (Flutter or AirRatatatRap) or EasyJumps and TalonTrot and Flutter",
					"Kazooie": "EasyTediousJumps and (TallJump or WingWhack or Glide or LegSpring)",
					"Banjo": "EasyTediousJumps and (TallJump and PackWhackJump)"
				}
			}
		}
	},
	"GGM: Waterfall Cavern Side Entrance": {
		"exits": {
			"GGM: Waterfall Cavern Bottom Entrance": {},
			"GGM: Flooded Caves Above Water Near Waterfall Cavern Exit": {},
			"GGM: Waterfall Cavern Jiggy Ramp": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Banjo": "TallJump and PackWhackJump and SackPackAirJump and GripGrab or TallJump and PackWhackJump and SackPackAirJump and SackPackEndingJump",
					"Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
		}
	},
	"GGM: Waterfall Cavern Bottom Entrance": {
		"exits": {
			"GGM: Water Storage": {},
			"GGM: Waterfall Cavern Bottom Pool Underwater": {
				"logic": {
					"Banjo-Kazooie": "Dive",
					"Banjo": "Dive"
				}
			},
		}
	},
	"GGM: Waterfall Cavern Bottom Pool Underwater": {
		"exits": {
			"GGM: Waterfall Cavern Bottom Entrance": {},
			"GGM: Waterfall Cavern Boulder Broken": {
				"logic": {
					"Banjo-Kazooie": "TalonTorpedo"
				}
			},
			"GGM: Waterfall Cavern Behind Boulder": {
				"logic": "GGMWaterfallCavernBoulderBroken"
			},
		}
	},
	"GGM: Waterfall Cavern Behind Boulder": {
		"exits": {
			"GGM: Waterfall Cavern Bottom Entrance": {
				"logic": "GGMWaterfallCavernBoulderBroken"
			},
			"HFP: Mega Glowbo Room Underwater": {},
		}
	},
	"GGM: Flooded Caves Above Water Near Waterfall Cavern Exit": {
		"exits": {
			"GGM: Flooded Caves Underwater": {
				"logic": {
					"Banjo-Kazooie": "Dive",
					"Banjo": "Dive"
				}
			},
			"GGM: Waterfall Cavern Side Entrance": {},
		},
	},
	"GGM: Flooded Caves Above Water Near Crushing Shed Exit": {
		"exits": {
			"GGM: Flooded Caves Underwater": {
				"logic": {
					"Banjo-Kazooie": "Dive",
					"Banjo": "true"
				}
			},
			"GGM: Behind Rocks to Flooded Caves": {},
		},
	},
	"GGM: Flooded Caves Underwater": {
		"locations": {
			"GGM: Flooded Caves Egg Nest 1": {
				"item": "EggNest",
			},
			"GGM: Flooded Caves Egg Nest 2": {
				"item": "EggNest",
			},
		},
		"exits": {
			"GGM: Flooded Caves Above Water Near Crushing Shed Exit": {},
			"GGM: Flooded Caves Above Water Near Waterfall Cavern Exit": {
				"logic": {
					"Banjo-Kazooie": "TallJump or GripGrab or BeakBusterJump",
					"Banjo": "TallJump or PackWhackJump"
				},
			},
			"GGM: Flooded Caves Jiggy Platform": {
				"logic": {
					"Banjo-Kazooie": "TallJump or GripGrab or BeakBusterJump",
					"Banjo": "TallJump or PackWhackJump"
				},
			},
		}
	},
	"GGM: Flooded Caves Jiggy Platform": {
		"locations": {
			"GGM: Flooded Caves Jiggy": {
				"item": "Jiggy",
			},
		}
	},


	"GGM: Near Prospector Bottom-Right Note Platform": {
		"locations": {
			"GGM: Near Prospector's Hut Bottom-Right Note": {
				"item": "NoteNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Main Map": {},
			"GGM: Near Prospector Middle-Right Note Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "GripGrab or TallJump or TalonTrot or FlapFlip or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Talon Trot": "true",
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Banjo": "true",
					"Kazooie": {
						"Kazooie": "TallJump or LegSpring",
						"Clockwork Kazooie": "ClockworkShot"
					}
				},
			},
			"GGM: Near Prospector Empty Honeycomb Platform": {
				"logic": {
					"Banjo-Kazooie": "FlapFlip",
					"Kazooie": "LegSpring",
					"Detonator": "true",
					"Banjo": "PackWhackJump and TallJump"
				}
			}
		}
	},
	"GGM: Near Prospector Bottom-Left Note Platform": {
		"locations": {
			"GGM: Near Prospector's Hut Bottom-Left Note": {
				"item": "NoteNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Main Map": {},
			"GGM: Near Prospector Empty Honeycomb Platform": {
				"logic": {
					"Banjo-Kazooie": "(TallJump or TalonTrot and Flutter or WonderwingJump) and GripGrab or TalonTrot and Flutter and BeakBusterJump or FlapFlip or WonderwingJump",
					"Talon Trot": {
						"Banjo-Kazooie": "Flutter and GripGrab or Flutter and BeakBusterJump"
					},
					"Banjo": "GripGrab or PackWhackJump and TallJump",
					"Kazooie": "LegSpring",
					"Detonator": "true"
				},
			},
		}
	},
	"GGM: Near Prospector Middle-Right Note Platform": {
		"locations": {
			"GGM: Near Prospector's Hut Middle-Right Note": {
				"item": "NoteNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Near Prospector Empty Honeycomb Platform": {
				"logic": {
					"Banjo-Kazooie": "GripGrab and EasyJumps or BeakBusterJump or TalonTrot",
					"Talon Trot": "true",
					"Mumbo": "TallJump",
					"Banjo": "PackWhack",
					"Kazooie": "TallJump or LegSpring",
					"Detonator": "true"
				}
			},
			"GGM: Near Prospector Bottom-Right Note Platform": {},
		}
	},
	"GGM: Near Prospector Empty Honeycomb Platform": {
		"locations": {
			"GGM: Prospector Boulder Honeycomb": {
				"item": "EmptyHoneycomb",
				"logic": {
					"Banjo-Kazooie": "BillDrill or BeakBargeClip or EggBarge",
					"Banjo": "TaxiPackClip or PackWhackClip",
					"Detonator": "true"
				}
			},
		},
		"exits": {
			"GGM: Near Prospector Top-Left Note Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "(TallJump or TalonTrot and Flutter or WonderwingJump) and GripGrab or (TallJump or TalonTrot and Flutter) and BeakBusterJump or FlapFlip",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Talon Trot": "Flutter and GripGrab or Flutter and BeakBusterJump",
					"Banjo": "GripGrab or TallJump and PackWhackJump",
					"Kazooie": {
						"Kazooie": "LegSpring",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Detonator": "true"
				}
			},
			"GGM: Near Prospector Bottom-Left Note Platform": {},
			"GGM: Near Prospector Middle-Right Note Platform": {
				"logic": "EasyTediousJumps"
			},
			"GGM: Near Prospector Bottom-Right Note Platform": {},
		}
	},
	"GGM: Near Prospector Top-Left Note Platform": {
		"locations": {
			"GGM: Near Prospector's Hut Top-Left Note": {
				"item": "NoteNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Near Prospector Empty Honeycomb Platform": {},
			"GGM: Near Prospector Bottom-Left Note Platform": {},
			"GGM: Outside Prospector's Hut": {
				"logic": {
					"Banjo-Kazooie": "FlapFlip and GripGrab",
					"Kazooie": "LegSpring"
				}
			},
		}
	},
	"GGM: Near Prospector Top-Right Note Platform": {
		"locations": {
			"GGM: Near Prospector's Hut Top-Right Note": {
				"item": "NoteNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Outside Prospector's Hut": {
				"logic": {
					"BK Turbo Trainers": "true"
				}
			},
			"GGM: Bill Drill Silo Nest Platforms": {
				"logic": {
					"BK Turbo Trainers": "EasyTediousJumps"
				}
			},
			"GGM: Near Prospector Empty Honeycomb Platform": {},
			"GGM: Near Prospector Middle-Right Note Platform": {},
		}
	},
	"GGM: Outside Prospector's Hut": {
		"exits": {
			"GGM: Prospector's Hut": {},
			"GGM: Near Prospector Top-Left Note Platform": {},
			"GGM: Near Prospector Top-Right Note Platform": {},
			"GGM: Bill Drill Silo Platform": {
				"logic": {
					"BK Turbo Trainers": "HardTediousJumps"
				}
			},
			"GGM: Bill Drill Silo Nest Platforms": {
				"logic": {
					"Kazooie": "true"
				}
			}
		}
	},
	"GGM: Prospector's Hut": {
		"locations": {
			"GGM: Dilberta Jiggy": {
				"item": "Jiggy",
				"logic": "MTPrisonCompoundJailCellBoulderBroken"
			},
			"GGM: Prospector's Hut Egg Nest": {
				"item": "EggNest",
			},
		},
		"exits": {
			"MT: Prison Compound Behind Jail Cell Boulder": {
				"logic": {
					"Banjo-Kazooie": "true",
					"Talon Trot": "true"
				}
			},
			"GGM: Outside Prospector's Hut": {}
		}
	},

	"GGM: Bill Drill Silo Nest Platforms": {
		"locations": {
			"GGM: Near Bill Drill Silo Egg Nest 1": {
				"item": "EggNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
			"GGM: Near Bill Drill Silo Egg Nest 2": {
				"item": "EggNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Bill Drill Silo Platform": {
				"logic": {
					"Banjo-Kazooie": "(TallJump or TalonTrot and Flutter or WonderwingJump) and GripGrab or (TallJump or TalonTrot and Flutter) and BeakBusterJump or FlapFlip"
				}
			}
		}
	},
	"GGM: Bill Drill Silo Platform": {
		"locations": {
			"GGM: Bill Drill Silo": {
				"item": "BillDrill",
				"logic": {"Banjo-Kazooie": "Notes >= ChosenMoveSiloCosts['Bill Drill']"},
			},
		}
	},

	"GGM: Outside Mumbo's Skull Left Note Platform": {
		"locations": {
			"GGM: Outside Mumbo's Skull Left Note": {
				"item": "NoteNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Main Map": {},
			"GGM: Outside Mumbo's Skull Warp Pad Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or GripGrab and HardJumps or BeakBusterJump or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Banjo": "true",
					"Kazooie": {
						"Kazooie": "TallJump or LegSpring or Glide and EasyJumps",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Talon Trot": "true"
				}
			},
		}
	},
	"GGM: Outside Mumbo's Skull Warp Pad Platform": {
		"locations": {
			"GGM: Outside Mumbo's Skull Warp Pad Tagged": {
				"item": "GGMOutsideMumbosSkullWarpPad",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Outside Mumbo's Skull Left Note Platform": {
				"logic": "EasyTediousJumps"
			},
			"GGM: Main Map": {},
			"GGM: Outside Mumbo's Skull Bottom-Right Note Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or GripGrab and HardJumps or BeakBusterJump or Flutter or AirRatatatRap or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Banjo": "true",
					"Kazooie": "true",
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Talon Trot": "true"
				}
			},
			"GGM: Outside Mumbo's Skull Top-Right Note Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or GripGrab and HardJumps or BeakBusterJump or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Banjo": "true",
					"Kazooie": {
						"Kazooie": "TallJump or LegSpring or Glide and EasyJumps",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Talon Trot": "true"
				}
			}
		}
	},
	"GGM: Outside Mumbo's Skull Bottom-Right Note Platform": {
		"locations": {
			"GGM: Outside Mumbo's Skull Bottom-Right Note": {
				"item": "NoteNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Main Map": {},
			"GGM: Outside Mumbo's Skull Warp Pad Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or GripGrab and HardJumps or BeakBusterJump or Flutter or AirRatatatRap or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Banjo": "true",
					"Kazooie": "true",
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Talon Trot": "true"
				}
			},
			"GGM: Outside Mumbo's Skull Top-Right Note Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or GripGrab and HardJumps or BeakBusterJump or WonderwingJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Banjo": "true",
					"Kazooie": {
						"Kazooie": "TallJump or LegSpring or Glide and EasyJumps",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Talon Trot": "true"
				}
			}
		}
	},
	"GGM: Outside Mumbo's Skull Top-Right Note Platform": {
		"locations": {
			"GGM: Outside Mumbo's Skull Top-Right Note": {
				"item": "NoteNest",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"GGM: Outside Mumbo's Skull Warp Pad Platform": {},
			"GGM: Outside Mumbo's Skull Bottom-Right Note Platform": {},
			"GGM: Outside Mumbo's Skull": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or HardJumps or BeakBusterJump or WonderwingJump",
					},
					"Banjo": "true",
					"Kazooie": "TallJump or LegSpring",
					"Mumbo": "TallJump",
					"Detonator": "true",
					"Talon Trot": "true"
				}
			}
		}
	},
	"GGM: Outside Mumbo's Skull": {
		"exits": {
			"GGM: Near Prospector Top-Right Note Platform": {},
			"GGM: Outside Mumbo's Skull Warp Pad Platform": {},
			"GGM: Mumbo's Skull": {}
		}
	},
	"GGM: Mumbo's Skull": {
		"locations": {
			"GGM: Mumbo's Skull Feather Nest 1": {
				"item": "FeatherNest",
			},
			"GGM: Mumbo's Skull Feather Nest 2": {
				"item": "FeatherNest",
			},
			"GGM: Mumbo's Skull Feather Nest 3": {
				"item": "FeatherNest",
			},
		},
		"exits": {
			"GGM: Mumbo's Skull": {
				"logic": {
					"Banjo-Kazooie": {
						"Mumbo": "MumboLevitate"
					}
				}
			},
			"GGM: Outside Mumbo's Skull": {}
		}
	},


	"GGM: Levitate Chuffy The Train": {"macro": {"event"}},
	"GGM: Crushing Shed Button Pressed": {"macro": {"event"}},
	"GGM: Levitate The Crushing Shed Boulder": {"macro": {"event"}},
	"GGM: Rocks Near Crushing Shed Broken": {"macro": {"event"}}, # We need a better name for this. It's the rocks that block the way to flooded caves
	"GGM: Ordnance Storage Boulder Broken": {"macro": {"event"}},
	"GGM: Mine Entrance 2 Boulder Broken": {"macro": {"event"}},
	"GGM: Gloomy Cavern Near Jail Cell Rocks Broken": {"macro": {"event"}},
	"GGM: Gloomy Cavern Near Power Hut Rocks Broken": {"macro": {"event"}},
	"GGM: Waterfall Cavern Entrance Opened": {"macro": {"event"}},
	"GGM: Waterfall Cavern Boulder Broken": {"macro": {"event"}},
	"GGM: Canary Cave Rocks Broken": {"macro": {"event"}},
	"GGM: Canary Mary Freed": {"macro": {"event"}},
	"GGM: Both Canary Mary Races Won": {"macro": {"event"}},
	"GGM: Fuel Depot Rocks Broken": {"macro": {"event"}},
	"GGM: Ordnance Storage Won": {"macro": {"event"}},
}
