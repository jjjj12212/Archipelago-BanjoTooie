from .. import Regions
default_id = 0x0101
instant_transform = {"Mumbo", "Washer"}
regions: Regions = {
	"GI Floor 1: Behind Main Door": {
		"locations": {
			"GI Floor 1: Entrance Door Warp Pad Tagged": {"item": "GIFloor1EntranceDoorWarpPad"},
		},
		"exits": {
			"GI Outside: Behind Main Door": {"id": 0x02},
			"GI Floor 1": {"logic": "GIFloor1OpenedMainDoor"},
			"GI: Warp Pads": {"logic": "GIFloor1EntranceDoorWarpPad"},
		}
	},
	"GI Floor 1": {
		"macro": {"splitup"},
		"locations": {
			"GI Floor 1: Claw Clamber Boots Silo": {
				"item": "ClawClamberBoots",
				"logic": {"Banjo-Kazooie": "Notes >= ChosenMoveSiloCosts['Claw Clamber Boots']"},
			},
		},
		"exits": {
			"GI Floor 1: Opened Main Door": {"logic": {"Banjo-Kazooie": "SplitUp"}},
			"GI Basement: AC Plant": {"id": 0x01},
			"GI Floor 1: Start Of Trash Compactor": {"id": 0x01},
			"GI Floor 1: Worker's Quarters": {"id": 0x01},
			"GI Train Station": {"id": 0x01},
			"GI Elevator Shaft: Floor 1": {"id": 0x04},
			"GI Floor 1: Behind Main Door": {"logic": "GIFloor1OpenedMainDoor"},
			"GI Floor 1: Side Of Trash Compactor": {
				"logic": {
					"Banjo-Kazooie": """
						GIFloor2UnscrewedPlate
						or EasyJumps and (
							TallJump and (RollJump or GripGrab or BeakBusterJump)
							or TalonTrot
							or Flutter
							or AirRatatatRap
							or RollJump and FlapFlip and BeakBusterJump
						)
					""",
					"Talon Trot": "GIFloor2UnscrewedPlate or EasyJumps",
					"Banjo": """
						GIFloor2UnscrewedPlate
						or EasyJumps and (
							TallJump and GripGrab
							or PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "GIFloor2UnscrewedPlate or Glide or EasyJumps",
					"Washer": "GIFloor2UnscrewedPlate",
				},
			},
			"GI Floor 1: Top Of Trash Compactor": {
				"logic": {
					"Banjo-Kazooie": "EasyJumps and FlapFlip and BeakBusterJump",
					"Kazooie": "EasyJumps and LegSpring",
				},
			},
			"GI Floor 1": {
				"logic": {
					"Banjo-Kazooie": {"BK Claw Clamber Boots": "ClawClamberBoots"},
					"Kazooie": {"SK Claw Clamber Boots": "ClawClamberBoots"},
				},
			},
			"GI Floor 1: Lower Catwalk": {
				"logic": {"BK Claw Clamber Boots", "SK Claw Clamber Boots"},
			},
			"GI Floor 1: Side Of Waste Disposal Plant": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip
						or TallJump and GripGrab
						or EasyJumps and (
							TalonTrot and Flutter and GripGrab
							or DamageBoostJump and (TallJump or TalonTrot)
						)
						or HardJumps and (
							TalonTrot and Flutter and BeakBusterJump
						)
					""",
					"Talon Trot": {
						"Banjo-Kazooie": """
							EasyJumps and (
								Flutter and GripGrab
							)
							or HardJumps and (
								Flutter and BeakBusterJump
							)
						""",
						"Talon Trot": "EasyJumps and DamageBoostJump"
					},
					"Banjo": """
						GripGrab
						or EasyJumps and (
							TallJump and PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": """
						LegSpring
						or Glide
						or EasyJumps and WingWhack
					""",
				},
			},
			"GI: Service Elevator": {"logic": {"Washer"}},
		}
	},
	"GI Floor 1: Start Of Trash Compactor": {
		"id": 0x0104,
		"exits": {
			"GI Floor 1": {"id": 0x05},
			"GI Floor 1: Middle Of Trash Compactor": {
				"logic": {
					"Banjo": """
						SnoozePack
						or EasyJumps and (
							PackWhackJump and (TallJump or SackPackAirJump)
						)
					""",
				},
			}
		}
	},
	"GI Floor 1: Middle Of Trash Compactor": {
		"id": 0x0104,
		"locations": {
			"GI Floor 1: Trash Compactor Jiggy": {
				"item": "Jiggy",
				"logic": {
					"Banjo": "GIFloor1OpenedTrashCompactorJiggyDoor",
				},
			},
		},
		"exits": {
			"GI Floor 1: Top Of Trash Compactor": {"id": 0x06},
			"GI Floor 1: Start Of Trash Compactor": {
				"logic": {
					"Banjo": """
						SnoozePack
						or EasyJumps and (
							PackWhackJump and (TallJump or SackPackAirJump)
						)
					""",
				}
			},
			"GI Floor 1: End Of Trash Compactor": {
				"logic": {
					"Banjo-Kazooie": """
						ExtraClockworkUsage and EggUse
						or DeathWarp
					""",
					"Banjo": """
						SnoozePack
						or EasyJumps and (
							PackWhackJump and (TallJump or SackPackAirJump)
						)
					""",
					"Kazooie": """
						ExtraClockworkUsage and EggUse
						or DeathWarp
					""",
				},
			}
		}
	},
	"GI Floor 1: End Of Trash Compactor": {
		"id": 0x0104,
		"locations": {
			"GI Floor 1: Trash Compactor Egg Nest 1": {"item": "EggNest"},
			"GI Floor 1: Trash Compactor Egg Nest 2": {"item": "EggNest"},
			"GI Floor 1: Opened Trash Compactor Jiggy Door": {
				"logic": {"Banjo"},
			}
		}
	},
	"GI Floor 1: Side Of Trash Compactor": {
		"exits": {
			"GI Floor 1": {},
			"GI Floor 1: Top Of Trash Compactor": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							FlapFlip
							or TalonTrot
							or TallJump and (
								Flutter
								or AirRatatatRap
								or BeakBusterJump
								or RollJump
								or SlideJump
							)
						)
					""",
					"Talon Trot": "EasyJumps",
					"Banjo": """
						EasyJumps and (
							PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": """
						LegSpring
						or EasyJumps and TallJump
					""",
				},
			},
			"GI Floor 1: Skivvy": {"logic": {"Washer"}},
		}
	},
	"GI Floor 1: Top Of Trash Compactor": {
		"locations": {
			"GI Floor 1: Top of Trash Compactor Feather Nest": {"item": "FeatherNest"},
		},
		"exits": {
			"GI Floor 1: Middle Of Trash Compactor": {"id": 0x02},
			"GI Floor 1": {},
			"GI Floor 1: Side Of Trash Compactor": {},
		}
	},
	"GI Floor 1: Worker's Quarters": {
		"id": 0x0103,
		"locations": {
			"GI Floor 1: Broke Loggo's Door": {
				"logic": {
					"Banjo-Kazooie": "EggUse and (GrenadeEggs or ExtraClockworkUsage)",
					"Kazooie": "EggUse and (GrenadeEggs or ExtraClockworkUsage)",
				},
			},
			"GI Floor 1: Loggo Cheato Page": {
				"item": "CheatoPage",
				"logic": {
					"Banjo-Kazooie": """
						GIFloor1BrokeLoggosDoor and (
							BillDrill
							or GIExtraLoggoMoves and EggUse and GrenadeEggs
						)
					""",
					"Banjo": "GIFloor1BrokeLoggosDoor and GIExtraLoggoMoves",
					"Kazooie": "GIFloor1BrokeLoggosDoor and GIExtraLoggoMoves and EggUse and GrenadeEggs",
				},
			},
			"GI Floor 1: Workers' Quarters Egg Nest": {"item": "EggNest"},
			"GI Floor 1: Workers' Quarters Feather Nest": {"item": "FeatherNest"},
			"GI Floor 1: Workers Quarters Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		},
		"exits": {
			"GI Floor 1": {"id": 0x07},
			"GI Worker's Quarters: Skivvy": {"logic": {"Washer"}},
		}
	},
	"GI Floor 1: Lower Catwalk": {
		"exits": {
			"GI Floor 2: Near Service Elevator": {
				"id": 0x02,
				"logic": {
					"Banjo-Kazooie": "TallJump",
					"Kazooie": "TallJump",
				},
			},
			"GI Floor 1: Lower Catwalk": {
				"logic": {
					"Banjo-Kazooie": {"BK Claw Clamber Boots": "ClawClamberBoots"},
					"Kazooie": {"SK Claw Clamber Boots": "ClawClamberBoots"},
				},
			},
			"GI Floor 1": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							Flutter
							or AirRatatatRap
							or BeakBusterFall
							or WonderwingFall
							or BreegullBashFall
							or FallDamage # 1 damage
						)
					""",
					"Banjo": """
						EasyJumps and (
							PackWhackFall
							or SackPackFall
							or ShackPackFall
							or SnoozePackFall
							or TaxiPackFall
							or FallDamage # 1 damage
						)
					""",
					"Kazooie": "",
					"BK Claw Clamber Boots": "",
					"SK Claw Clamber Boots": "",
				},
			},
			"GI Floor 1: A/C": {"logic": "EasyJumps"},
			"GI Floor 1: Top Of Waste Disposal Plant": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							GripGrab
							or (TallJump or FreeShockSpringPad) and (
								Flutter
								or AirRatatatRap and BeakBusterJump
							)
							or TalonTrot and (
								Flutter and (BeakBusterJump or TalonTrotSlideJump)
								or TalonTrotSlideJump and AirRatatatRap and BeakBusterJump
							)
						)
					""",
					"Talon Trot": {
						"Banjo-Kazooie": """
							EasyTediousJumps and (
								Flutter and (BeakBusterJump or TalonTrotSlideJump)
								or TalonTrotSlideJump and AirRatatatRap and BeakBusterJump
							)
						"""
					},
					"Banjo": """
						EasyTediousJumps and (
							GripGrab
							or PackWhackJump and (TallJump or SackPackAirJump)
						)
					""",
					"Kazooie": "Glide or EasyTediousJumps",
				},
			},
			"GI Floor 1: Lower Pipe": {
				"logic": {
					"Banjo-Kazooie": "TallJump or FreeShockSpringPad",
					"Banjo": "SackPackEndingJump and TallJump and PackWhackJump",
					"Kazooie": "LegSpring or FreeShockSpringPad or TallJump",
				},
			},
			"GI Floor 1: Tintop Arena": {"logic": {"Kazooie": "EasyJumps and (FreeShockSpringPad or TallJump)"}}
		}
	},
	"GI Floor 1: A/C": {
		"locations": {
			"GI Floor 1: Floor 1 on A/C Unit Note 1": {"item": "NoteNest"},
			"GI Floor 1: Floor 1 on A/C Unit Note 2": {"item": "NoteNest"},
		},
		"exits": {
			"GI Floor 1": {},
			"GI Floor 1: Side Of Waste Disposal Plant": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							TalonTrot
							or Flutter
							or RollJump and TallJump and BeakBusterJump
							or AirRatatatRap and (
								TallJump
								or FlapFlip
								or RollJump
								or GroundRatatatRapJump
								or SlideJump
							)
						)
					""",
					"Talon Trot": "EasyTediousJumps",
					"Banjo": """
						EasyTediousJumps and (
							PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "EasyTediousJumps",
				},
			},
		}
	},
	"GI Floor 1: Side Of Waste Disposal Plant": {
		"locations": {
			"GI Floor 1: Near Waste Disposal Feather Nest 1": {"item": "FeatherNest"},
			"GI Floor 1: Near Waste Disposal Feather Nest 2": {"item": "FeatherNest"},
			"GI Floor 1: Opened Waste Disposal Plant": {
				"logic": {
					"Banjo": """
						GIOutsideDeliveredBattery
						and GIFloor2DeliveredBatteryNearFloor3Exit
						and GIFloor2DeliveredToxicRoomBattery
						and GIFloor3DeliveredBattery
					""",
				}
			}
		},
		"exits": {
			"GI Floor 1": {},
			"GI Floor 1: Top Of Waste Disposal Plant": {
				"logic": {
					"Banjo-Kazooie": """
						Climb and (
							FlapFlip
							or TallJump and BeakBusterJump
						)
					""",
					"Banjo": "Climb",
				},
			},
		}
	},
	"GI Floor 1: Top Of Waste Disposal Plant": {
		"exits": {
			"GI Basement: Waste Disposal Plant Upper": {
				"id": 0x01,
				"logic": "GIFloor1OpenedWasteDisposalPlant",
			},
			"GI Floor 1: Side Of Waste Disposal Plant": {},
			"GI Floor 1: A/C": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and GripGrab
						or EasyJumps and (
							GripGrab and (
								TallJump
								or TalonTrot and (Flutter or AirRatatatRap)
							)
							or BeakBusterJump and (
								(TallJump or TalonTrot or FlapFlipSlideExtension) and Flutter
								or TalonTrot and AirRatatatRap
								or (RollJump or SlideJump) and TallJump and AirRatatatRap
							)
							or TalonTrot and DamageBoostJump
						)
					""",
					"Talon Trot": {
						"Banjo-Kazooie": """
							EasyJumps and (
								(Flutter or AirRatatatRap) and (GripGrab or BeakBusterJump)
								or DamageBoostJump
							)
						"""
					},
					"Banjo": """
						GripGrab
						or EasyJumps and (
							PackWhackJump and (TallJump or SackPackAirJump)
						)
					""",
					"Kazooie": "Glide or EasyJumps",
				},
			},
		}
	},
	"GI Floor 1: Ducts Near Waste Disposal Plant": {
		"exits": {
			"GI Floor 1": {},
			"GI Floor 1: Side Of Waste Disposal Plant": {
				"logic": {
					"Banjo-Kazooie": "Flutter or AirRatatatRap",
					"Banjo": "PackWhackJump",
					"Kazooie": "",
				},
			},
		}
	},
	"GI Floor 1: Lower Pipe": {
		"locations": {
			"GI Floor 1: High Pipe Egg Nest 1": {"item": "EggNest"},
			"GI Floor 1: High Pipe Egg Nest 2": {"item": "EggNest"},
		},
		"exits": {
			"GI Floor 1: Lower Catwalk": {},
			"GI Floor 1: Tintop Arena": {"logic": {"Kazooie": "EasyJumps and Glide"}},
		}
	},
	"GI Floor 1: Guarded Jiggy": {
	  "locations": {
	    "GI Floor 1: Guarded Jiggy": {"item": "Jiggy"},
		}
	},
	"GI Floor 1: Tintop Arena": {
	  "locations": {
			"GI Floor 1: Top Pipe Egg Nest": {"item": "EggNest"},
			"GI Floor 1: Defeated Tintops": {
				"logic": {
					"Banjo": "PackWhack and SnoozePack",
					"Kazooie": """
						EggUse and (
							exclude(AnyEggs, IceEggs)
							or IceEggs and WingWhack
						)
					""",
				}
			}
	  },
		"exits": {
			"GI Floor 1: Guarded Jiggy": {
				"logic": {
					"Banjo": "GIFloor1DefeatedTintops",
					"Kazooie": "GIFloor1DefeatedTintops and (TallJump or LegSpring)",
				}
			}
		}
	},
	"GI Floor 1: Upper Catwalk": {
		"exits": {
			"GI Outside: Behind Floor 1 Window": {"id": 0x03},
			"GI Floor 1: Tintop Arena": {
				"logic": {
					"Banjo": """
						EasyTediousJumps and (
							SackPackAirJump and PackWhackJump and (TallJump or SackPackEndingJump)
						)
					""",
					"Kazooie": """
						Glide
						or EasyJumps and (TallJump or WingWhack)
					""",
				}
			},
			"GI Floor 1: Guarded Jiggy": {"logic": {"Kazooie": "GIGuardedJiggyWithoutFighting"}},
		}
	},
	"GI Train Station": {
		"id": 0x0102,
		"locations": {
			"GI Floor 1: Train Station Honeycomb": {
				"item": "EmptyHoneycomb",
				"logic": {
					"Banjo-Kazooie": """
						(AnyAttack or EggUse and AnyEggs) and (TallJump or FreeShockSpringPad) and (GripGrab or EasyJumps)
						or ExtraClockworkUsage and EggAim
					""",
					"Banjo": """
						EasyJumps and (
							SackPackEndingJump and (
								TallJump and (GripGrab or PackWhackJump)
							)
						)
					""",
					"Kazooie": """
						EasyJumps and (
							(WingWhack or EggUse and AnyEggs) and (TallJump or FreeShockSpringPad)
							or LegSpring
						)
						or ExtraClockworkUsage and EggAim
					""",
				},
			},
			"GI Floor 1: Train Station Note 1": {
				"item": "NoteNest",
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or AirRatatatRapClip
						or GripGrab
						or BeakBusterJump
						or WonderwingJump
						or DamageBoostJump
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": """
						TallJump
						or LegSpring
						or DamageBoostJump
					""",
				},
			},
			"GI Floor 1: Train Station Note 2": {
				"item": "NoteNest",
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or GripGrab
						or BeakBusterJump
						or WonderwingJump
						or DamageBoostJump
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": """
						TallJump
						or LegSpring
						or DamageBoostJump
					""",
				},
			},
			"GI Floor 1: Train Station Note 3": {
				"item": "NoteNest",
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or EasyJumps and GripGrab and (Flutter or AirRatatatRap)
						or BeakBusterJump
						or WonderwingJump
						or DamageBoostJump
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": """
						TallJump
						or LegSpring
						or DamageBoostJump
					""",
				},
			},
			"GI Floor 1: Train Station Big Box Egg Nest": {"item": "EggNest"},
			"GI Floor 1: Train Station Small Box Egg Nest": {
				"item": "EggNest",
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or AirRatatatRapClip
						or GripGrab
						or BeakBusterJump
						or WonderwingJump
						or DamageBoostJump
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": """
						TallJump
						or LegSpring
						or DamageBoostJump
						or EasyJumps
					""",
				},
			},
			"GI Floor 1: Train Station Medium Box Egg Nest": {
				"item": "EggNest",
				"logic": {
					"Banjo-Kazooie": """
						(TallJump or TalonTrot and Flutter) and (GripGrab or BeakBusterJump)
						or FlapFlip
						or (TallJump or TalonTrot) and AirRatatatRapClip
						or EasyJumps and (
							TallJump
							or TalonTrot
							or Flutter
							or AirRatatatRap
							or GripGrab
							or BeakBusterJump
							or RollJump
							or GroundRatatatRapJump
							or WonderwingJump
							or SlideJump
							or (AnyAttack or EggUse and AnyEggs) and FreeShockSpringPad
						)
					""",
					"Talon Trot": """
						Flutter and (GripGrab or BeakBusterJump)
						or AirRatatatRapClip
						or EasyJumps
					""",
					"Banjo": "",
					"Kazooie": "LegSpring or EasyJumps",
				},
			},
		},
		"exits": {
			"GI Floor 1": {"id": 0x04},
			"Train At GI": {"logic": "Chuffy"},
			"Chuffy's Cab": {"logic": {"Banjo-Kazooie": "TrainAtGI"}},
			"Inside Chuffy's Wagon": {"logic": "TrainAtGI"},
		}
	},
	"GI Floor 1: Back Door Room": {
		"locations": {
		},
		"exits": {
			"GI Floor 1: Opened Back Door": {},
			"GI Floor 2: Near Tintops": {"id": 0x05},
			"GI Outside: Back Area": {"id": 0x04}
		}
	},
	"GI Floor 1: Opened Main Door": {"macro": {"event"}},
	"GI Floor 1: Opened Back Door": {"macro": {"event"}},
}
