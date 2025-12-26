from .. import Regions
default_id = 0x0100
instant_transform = {"Mumbo", "Washer"}
regions: Regions = {
	"GI Outside": {
		"exits": {
			"Grunty Industries": {},
			"GI Outside: Broke Floor 1 Window": {
				"logic": {
					"Banjo-Kazooie": "EggAim and AnyEggs",
					"Kazooie": "EggAim and AnyEggs",
				},
			},
			"GI Outside: Broke Window Above Front Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": "EggAim and AnyEggs",
					"Kazooie": "EggAim and AnyEggs",
				},
			},
			"GI Outside: Broke Window Near Back Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						EggAim and (
							exclude(AnyEggs, ClockworkKazooieEggs)
							or ExtraClockworkUsage and (
								DamageBoost
								or WonderwingDamageBoost
								or DragundaSidle
							)
						)
					""",
					"Kazooie": """
						EggAim and (
							exclude(AnyEggs, ClockworkKazooieEggs)
							or ExtraClockworkUsage and (
								DamageBoost
								or DragundaSidle
								or EasyJumps and (
									Glide
									or (TallJump or LegSpring) and WingWhack
								)
							)
						)
					""",
				},
			},
			"GI Outside: Behind Main Door": {"logic": "GIFloor1OpenedMainDoor"},
			"GI Outside: Battery Platform": {
				"logic": {
					"Banjo-Kazooie": """
						Climb
						or DamageBoostJump
						or WonderwingDamageBoost
						or DragundaSidle and (
							GripGrab
							or TallJump
							or TalonTrot
							or FlapFlip
							or BeakBusterJump
							or WonderwingJump
						)
						or EasyJumps and (
							(Flutter or AirRatatatRap) and (
								TallJump and (GripGrab or BeakBusterJump)
								or TalonTrot
								or DragundaSidle
							)
						)
					""",
					"Talon Trot": {
						"Banjo-Kazooie": "EasyJumps and (Flutter or AirRatatatRap)",
						"Talon Trot": "DragundaSidle",
					},
					"Banjo": """
						Climb
						or SackPack
						or ShackPack
						or DamageBoostJump
						or DragundaSidle
						or EasyJumps and TallJump and PackWhackJump
					""",
					"Kazooie": """
						DamageBoostJump
						or EasyJumps and (
							TallJump
							or LegSpring
							or Glide
						)
					""",
				},
			},
			"GI Outside: Atop Front Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						Climb and (
							DamageBoost
							or WonderwingDamageBoost
							or DragundaSidle
						)
					""",
					"Banjo": """
						Climb and (
							DamageBoost
							or DragundaSidle
							or SackPack
							or ShackPack
						)
					""",
					"Kazooie": """
						LegSpring and (
							DamageBoost
							or DragundaSidle
							or Glide
							or EasyJumps and WingWhack
						)
					""",
				},
			},
			"GI Outside: Atop Drain Pipe": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and GripGrab
						or EasyJumps and (
							(TallJump or TalonTrot) and (Flutter or AirRatatatRap)
							or FlapFlip and (
								Flutter
								or AirRatatatRap and BeakBusterJump
							)
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and (Flutter or AirRatatatRap)"},
					"Banjo": """
						EasyJumps and (
							TallJump and PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": """
						EasyJumps and (
							TallJump
							or LegSpring
						)
					""",
				},
			},
		}
	},
	"GI Outside: Behind Main Door": {
		"exits": {
			"GI Floor 1: Behind Main Door": {"id": 0x01},
			"GI Outside": {"logic": "GIFloor1OpenedMainDoor"},
		},
	},
	"GI Outside: Battery Platform": {
		"locations": {
			"GI Outside: Delivered Battery": {
				"logic": {
					"Banjo": """
						PackWhack and TaxiPack
						and can_form_from_region_reach(
							"Banjo",
							"GI Outside: Battery Platform",
							[
								"GI Floor 1: Side Of Waste Disposal Plant",
								"GI Floor 2: Toxic Waste Tower",
								"GI Floor 3: Boiler Plant",
								"GI Floor 4: After Crushers Lower Catwalk",
							]
						)
					""",
				}
			}
		},
		"exits": {
			"GI Outside": {},
			"GI Outside: Atop Front Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and GripGrab and Climb and (
							TallJump
							or TalonTrot
							or Flutter
							or AirRatatatRap
							or BillDrillJump
							or WonderwingJump
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "FlapFlip and GripGrab and Climb"},
					"Banjo": """
						Climb and GripGrab and (
							TallJump
							or EasyJumps and PackWhackJump
						)
					""",
					"Kazooie": "EasyJumps and LegSpring",
				},
			},
		}
	},
	"GI Outside: Atop Drain Pipe": {
		"exits": {
			"GI Outside": {
				"logic": {
					"Banjo-Kazooie": """
						GripGrab
						or DragundaSidle
						or DamageBoost
						or EasyJumps and (
							BeakBusterJump and (
								TallJump
								or RollJump and FlapFlip
							)
							or TalonTrot
							or Flutter
							or AirRatatatRap
						)
					""",
					"Talon Trot": "EasyJumps",
					"Banjo": """
						GripGrab
						or DragundaSidle
						or DamageBoost
						or EasyJumps and (
							PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Outside: Atop Front Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and Climb and (
							TallJump and (
								Flutter
								or RollJump and AirRatatatRap and BeakBusterJump
							)
							or TalonTrot and (Flutter or AirRatatatRap)
							or FlapFlip and Flutter and BeakBusterJump
						)
						or HardJumps and (
							TalonTrot and (Flutter or AirRatatatRap) and BeakBusterJump
						)
					""",
					"Talon Trot": {
						"Banjo-Kazooie": """
							EasyJumps and Climb and (Flutter or AirRatatatRap)
							or HardJumps and (Flutter or AirRatatatRap) and BeakBusterJump
						""",
					},
					"Banjo": """
						EasyJumps and (
							SackPackAirJump and (Climb or PackWhackJump)
							or TallJump and PackWhackJump
						)
					""",
					"Kazooie": """
						EasyJumps and (
							TallJump
							or LegSpring
						)
					""",
				},
			}
		}
	},
	"GI Outside: Atop Front Door": {
		"locations": {
			"GI Outside: Treble Clef": {"item": "TrebleClef"},
		},
		"exits": {
			"GI Outside: Broke Floor 1 Window": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							GroundRatatatRapJump
							or AirRatatatRap
							or BeakBuster
							or BreegullBashFall
							or EggUse and AnyEggs
							or BeakBargeJump and (
								Flutter
								or AirRatatatRap
								or FallDamage # 1 damage
							)
						)
					""",
					"Banjo": "EasyTediousJumps and PackWhack",
					"Kazooie": """
						EasyTediousJumps and WingWhack
						or EggUse and AnyEggs
					""",
				},
			},
			"GI Outside: Behind Floor 1 Window": {
				"logic": {
					"Banjo-Kazooie": """
						GIOutsideBrokeFloor1Window and EasyTediousJumps and (
							TallJump
							or TalonTrot
							or FlapFlip
							or Flutter
							or AirRatatatRap
							or GripGrab
							or BeakBusterJump
							or RollJump
							or GroundRatatatRapJump
							or WonderwingJump
						)
					""",
					"Talon Trot": "GIOutsideBrokeFloor1Window and EasyTediousJumps",
					"Banjo": "GIOutsideBrokeFloor1Window and EasyTediousJumps",
					"Kazooie": "GIOutsideBrokeFloor1Window and EasyTediousJumps",
				},
			},
			"GI Outside": {},
			"GI Outside: Atop Drain Pipe": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							FallDamage and (TallJump or TalonTrot or FlapFlip or RollJump) # 1 damage
							or Flutter
							or AirRatatatRap
							or BeakBusterJump
							or WonderwingJump and WonderwingFall
						)
						or HardTediousJumps and (
							FallDamage and GripGrab
							or RollJump and FlapFlip
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyTediousJumps and FallDamage"}, # 1 damage
					"Banjo": """
						EasyTediousJumps and (
							FallDamage and TallJump # 1 damage
							or PackWhackJump
							or SackPackAirJump
							or ShackPackAirJump
						)
					""",
					"Kazooie": "EasyTediousJumps",
				},
			},
			"GI Outside: Atop Front Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						HardTediousJumps and (
							TalonTrot and (
								Flutter and (BeakBusterJump or TalonTrotSlideJump)
								or TalonTrotSlideJump and AirRatatatRap and BeakBusterJump
							)
						)
					""",
					"Talon Trot": {
						"Banjo-Kazooie": """
							Flutter and (BeakBusterJump or TalonTrotSlideJump)
							or TalonTrotSlideJump and AirRatatatRap and BeakBusterJump
						""",
					},
					"Kazooie": "Glide or EasyTediousJumps"
				},
			}
		}
	},
	"GI Outside: Atop Front Train Tunnel": {
		"locations": {
			"GI Outside: Atop Front Train Tunnel Feather Nest": {"item": "FeatherNest"},
			"GI Outside: Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		},
		"exits": {
			"GI Outside: Flying": {
				"logic": {
					"Banjo-Kazooie": "FlightPad and GIFloor4ActivatedFlightPads",
					"Kazooie": "FlightPad and GIFloor4ActivatedFlightPads",
				},
			},
			"GI Outside: Atop Drain Pipe": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							(TallJump or TalonTrot) and (Flutter or AirRatatatRap)
							or FlapFlip and Flutter and BeakBusterJump
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and (Flutter or AirRatatatRap)"},
					"Banjo": """
						EasyJumps and (
							PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "Glide or EasyJumps",
				},
			},
			"GI Outside: Battery Platform": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or Flutter
						or AirRatatatRap
						or BillDrillJump
						or WonderwingJump
					""",
					"Talon Trot": "",
					"Banjo": "TallJump or PackWhackJump",
					"Kazooie": "",
				},
			},
			"GI Outside": {
				"logic": {
					"Banjo-Kazooie": """
						DamageBoost
						or WonderwingDamageBoost
						or DragundaSidle
					""",
					"Banjo": """
						DamageBoost
						or DragundaSidle
						or SackPack
						or ShackPack
					""",
					"Kazooie": """
						DamageBoost
						or DragundaSidle
						or Glide
						or EasyJumps and WingWhack
					""",
				},
			},
			"GI Outside: Train Switch Platform": {},
			"GI Outside: Back Area": {
				"logic": {
					"Kazooie": "Glide",
				}
			}
		}
	},
	"GI Outside: Train Switch Platform": {
		"locations": {
			"GI Outside: Train Switch": {"item": "GITrainStation"},
		},
		"exits": {
			"GI Outside: Atop Front Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
					"Kazooie": "LegSpring",
				},
			},
			"GI Outside: Back Area": {
				"logic": {
					"Banjo-Kazooie": """
						DamageBoost
						or WonderwingDamageBoost
						or DragundaSidle
					""",
					"Banjo": """
						DamageBoost
						or DragundaSidle
						or SackPack
						or ShackPack
					""",
					"Kazooie": """
						DamageBoost
						or DragundaSidle
						or LegSpring and Glide
					""",
				},
			},
		}
	},
	"GI Outside: Atop Back Train Tunnel": {
		"locations": {
			"GI Outside: Atop Back Train Tunnel Feather Nest": {"item": "FeatherNest"},
		},
		"exits": {
			"GI Outside: Flying": {
				"logic": {
					"Banjo-Kazooie": "FlightPad and GIFloor4ActivatedFlightPads",
					"Kazooie": "FlightPad and GIFloor4ActivatedFlightPads",
				},
			},
			"GI Outside": {
				"logic": {
					"Banjo-Kazooie": """
						DamageBoost
						or WonderwingDamageBoost
						or DragundaSidle
					""",
					"Banjo": """
						DamageBoost
						or DragundaSidle
						or SackPack
						or ShackPack
					""",
					"Kazooie": """
						DamageBoost
						or DragundaSidle
						or Glide
					""",
				},
			},
			"GI Outside: Back Area": {},
		}
	},
	"GI Outside: Flying": {
		"instant_transform": set(),
		"locations": {
			"GI Outside: Chimney Honeycomb": {"item": "EmptyHoneycomb"},
		},
		"exits": {
			"GI Floor 3: Boiler Plant Top of Boiler": {
				"id": 0x05,
				"logic": "GIOutsideBrokeChimney",
			},
			"GI Outside: Broke Chimney": {
				"logic": {
					"Banjo-Kazooie": """
						BeakBomb
						or (GrenadeEggs or ClockworkKazooieEggs) and (
							AirborneEggAiming
							or EasyJumps and ThirdPersonEggShooting and ( # atop the chimney
								FallDamage # 2 damage
								or Flutter
								or AirRatatatRap
								or BeakBusterFall
								or WonderwingFall
								or BreegullBashFall
							)
						)
					""",
					"Kazooie": """
						(GrenadeEggs or ClockworkKazooieEggs) and (
							AirborneEggAiming
							or EasyJumps and ThirdPersonEggShooting # atop the chimney
						)
					""",
				},
			},
			"GI Outside: Break Lower Windows": {
				"logic": {
					"Banjo-Kazooie": """
						BeakBomb
						or AirborneEggAiming and AnyEggs
						or BeakBuster
					""",
					"Kazooie": "AirborneEggAiming and AnyEggs",
				},
			},
			"GI Outside: Break Upper Windows": {
				"logic": {
					"Banjo-Kazooie": """
						BeakBomb
						or AirborneEggAiming and AnyEggs
						or BeakBuster
					""",
					"Kazooie": "AirborneEggAiming and AnyEggs",
				},
			},
			"GI Outside: Back Area": {
				"logic": {
					"Banjo-Kazooie": {"BK Claw Clamber Boots": "ClawClamberBoots and BeakBombTricks"},
				},
			},
			"GI Outside": {},
			"GI Outside: Battery Platform": {},
			"GI Outside: Atop Drain Pipe": {},
			"GI Outside: Atop Front Door": {},
			"GI Outside: Atop Front Train Tunnel": {},
			"GI Outside: Train Switch Platform": {},
			"GI Outside: Atop Back Train Tunnel": {},
			"GI Outside: Back Area": {},
			"GI Outside: Near Skivvy": {},
			"GI Outside: Lower Roof": {},
			"GI Outside: Upper Roof": {},
			"GI Outside: Upper Roof Side Window": {},
			"GI Outside: Fire Exit Lower": {},
			"GI Outside: Fire Exit Upper": {},
			"GI Outside: Jinjo Platform": {},
			"GI Outside: Behind Floor 1 Window": {"logic": "GIOutsideBrokeFloor1Window"},
			"GI Outside: Behind Window Above Front Train Tunnel": {"logic": "GIOutsideBrokeWindowAboveFrontTrainTunnel"},
			"GI Outside: Behind Window Near Back Train Tunnel": {"logic": "GIOutsideBrokeWindowNearBackTrainTunnel"},
		}
	},
	"GI Outside: Back Area": {
		"exits": {
			"GI Outside: Behind Back Door": {"logic": "GIFloor1OpenedBackDoor"},
			"GI Outside: Back Area": {
				"logic": {
					"Banjo-Kazooie": {"BK Claw Clamber Boots": "ClawClamberBoots and (AnyAttack or EggUse and AnyEggs)"},
					"Kazooie": {"SK Claw Clamber Boots": "ClawClamberBoots and (WingWhack or EggUse and AnyEggs)"},
				},
			},
			"GI Outside: Back Area Button": {
				"logic": {
					"Banjo": "PackWhack",
					"Kazooie": "WingWhack or EggUse and AnyEggs",
				}
			},
			"GI Outside: Jinjo Platform": {
				"logic": {"BK Claw Clamber Boots", "SK Claw Clamber Boots"},
			},
			"GI Outside: Atop Back Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
					"Kazooie": "LegSpring",
				},
			},
			"GI Outside: Near Skivvy": {
				"logic": {
					"Banjo-Kazooie": """
						TalonTrot
						or DragundaSidle
						or DamageBoost
						or WonderwingDamageBoost
						or (TallJump or FlapFlip or BeakBusterJump) and (Flutter or AirRatatatRap)
						or TallJump and BillDrillJump
					""",
					"Talon Trot": "",
					"Banjo": """
						DragundaSidle
						or DamageBoost
						or PackWhackJump
						or SackPack
						or ShackPack
					""",
					"Kazooie": "",
					"Washer": "",
				},
			},
			"GI Outside: Train Switch Platform": {
				"logic": {
					"Banjo-Kazooie": """
						DamageBoost
						or WonderwingDamageBoost
						or DragundaSidle
					""",
					"Banjo": """
						DamageBoost
						or DragundaSidle
						or SackPack
						or ShackPack
					""",
					"Kazooie": """
						DamageBoost
						or DragundaSidle
						or Glide
					""",
				},
			},
		}
	},
	"GI Outside: Back Area Button": {"macro": {"rejoin"}},
	"GI Outside: Behind Back Door": {
		"exits": {
			"GI Floor 1: Back Door Room": {"id": 0x0C},
			"GI Outside: Back Area": {"logic": "GIFloor1OpenedBackDoor"},
		}
	},
	"GI Outside: Near Skivvy": {
		"exits": {
			"GI Outside: Back Area": {
				"logic": {
					"Banjo-Kazooie": """
						TalonTrot
						or DragundaSidle
						or DamageBoost
						or WonderwingDamageBoost
						or (TallJump or FlapFlip or BeakBusterJump) and (Flutter or AirRatatatRap)
						or TallJump and BillDrillJump
					""",
					"Talon Trot": "",
					"Banjo": """
						DragundaSidle
						or DamageBoost
						or PackWhackJump
						or SackPack
						or ShackPack
					""",
					"Kazooie": "",
				},
			},
			"GI Outside: Skivvy": {"logic": {"Washer"}},
		}
	},
	"GI Outside: Jinjo Platform": {
		"locations": {
			"GI Outside: Jinjo": {
				"item": "BlackJinjo",
				"logic": {
					"Banjo-Kazooie": "BeakBargeClip",
					"Banjo": """
						forms_reach_regions({
							"Banjo": "GI Outside: Jinjo Platform",
							"Kazooie": "GI Outside: Back Area Button",
						})
					""",
					"Kazooie": """
						forms_reach_regions({
							"Banjo": "GI Outside: Back Area Button",
							"Kazooie": "GI Outside: Jinjo Platform",
						})
					""",
				},
			},
		},
		"exits": {
			"GI Outside: Jinjo Platform": {
				"logic": {
					"Banjo-Kazooie": {"BK Claw Clamber Boots": "ClawClamberBoots"},
					"Kazooie": {"SK Claw Clamber Boots": "ClawClamberBoots"},
				},
			},
			"GI Outside: Back Area": {
				"logic": {"BK Claw Clamber Boots", "SK Claw Clamber Boots"},
			},
			"GI Outside: Atop Back Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							Flutter
							or AirRatatatRap
							or FallDamage # 3 damage
							or BeakBusterFall
							or WonderwingFall
						)
					""",
					"Banjo": """
						EasyTediousJumps and (
							FallDamage # 3 damage
							or PackWhackFall
							or SackPackFall
							or ShackPackFall
							or SnoozePackFall
							or TaxiPackFall
						)
					""",
					"Kazooie": "EasyTediousJumps",
				},
			},
			"GI Outside: Fire Exit Lower": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							Flutter and (
								TallJump
								or TalonTrot
								or FlapFlip
								or RollJump
								or BeakBusterJump
							)
							or AirRatatatRap and (
								TalonTrot
								or RollJump and TallJump and BeakBusterJump
							)
						)
						or HardTediousJumps and (
							Flutter and GripGrab and (
								BeakBargeJump
								or GroundRatatatRapJump
								or SlideJump
							)
							or TalonTrot and TalonTrotSlideJump and BillDrillJump
						)
					""",
					"Talon Trot": {
						"Banjo-Kazooie": """
							EasyTediousJumps and (Flutter or AirRatatatRap)
							or HardTediousJumps and TalonTrotSlideJump and BillDrillJump
						""",
					},
					"Kazooie": "Glide or EasyTediousJumps",
				},
			}
		}
	},
	"GI Outside: Fire Exit Lower": {
		"exits": {
			"GI Floor 3: Catwalk": {"id": 0x07},
			"GI Outside: Fire Exit Upper": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or FlapFlip
						or TalonTrot
						or Flutter
						or AirRatatatRap
						or WonderwingJump
						or BeakBusterJump
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": "",
				},
			},
			"GI Outside: Back Area": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							FallDamage # 3 damage
							or Flutter
							or AirRatatatRap
							or BeakBusterFall
							or WonderwingFall
							or BreegullBashFall
						)
					""",
					"Banjo": """
						EasyJumps and (
							FallDamage # 3 damage
							or SackPackFall
							or ShackPackFall
							or SnoozePackFall
							or TaxiPackFall
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Outside: Jinjo Platform": {
				"logic": {
					"Kazooie": "Glide",
				}
			}
		}
	},
	"GI Outside: Fire Exit Upper": {
		"exits": {
			"GI Floor 4: Fire Exit Platform": {"id": 0x01},
			"GI Outside: Fire Exit Lower": {},
		}
	},
	"GI Outside: Lower Roof": {
		"locations": {
			"GI Outside: Roof Feather Nest 1": {"item": "FeatherNest"},
			"GI Outside: Roof Feather Nest 2": {"item": "FeatherNest"},
			"GI Outside: Roof Feather Nest 3": {"item": "FeatherNest"},
			"GI Outside: On the Roof Outside Warp Pad Tagged": {"item": "GIOutsideOnTheRoofOutsideWarpPad"},
		},
		"exits": {
			"GI: Warp Pads": {"logic": "GIOutsideOnTheRoofOutsideWarpPad"},
			"GI Outside: Broke Window Above Front Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						ExtraClockworkUsage and EggUse
						or DeathWarp and BeakBuster
						or EasyTediousJumps and FallDamage and ( # land on front train tunnel
							BeakBuster and (
								HealthUpgrade # 5 damage
								or Flutter # 4 damage
							)
							or BillDrill # 4 damage
						)
						or HardTediousJumps and ( # land in the window
							BreegullBashFall and (AirRatatatRap or BeakBuster)
							or BeakBuster and FallDamage # 4 damage
						)
					""",
					"Banjo": """
						PackWhack and (
							EasyTediousJumps and (ShackPackFall or TaxiPackFall)
							or HardTediousJumps and SackPackFall
						)
					""",
					"Kazooie": """
						ExtraClockworkUsage and EggUse
						or EasyTediousJumps and WingWhack
					""",
				},
			},
			"GI Outside: Broke Window Near Back Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						ExtraClockworkUsage and EggUse
						or DeathWarp and BeakBuster
						or EasyTediousJumps and FallDamage and ( # land on pipe
							(DragundaSidle or WonderwingDamageBoost) and (
								BeakBuster and (
									(HealthUpgrade, 2) # 6 damage
									or Flutter # 4 damage
								)
								or BillDrill # 4 damage
							)
							or DamageBoost and (
								BeakBuster and (
									(HealthUpgrade, 4) # 8 damage
									or (HealthUpgrade, 3) and ( # 7 damage
										TallJump
										or TalonTrot
										or AirRatatatRap
										or BeakBusterJump
									)
									or Flutter and HealthUpgrade # 5 damage
								)
								or BillDrill and (
									(HealthUpgrade, 2) # 6 damage
									or HealthUpgrade and ( # 5 damage
										TallJump
										or TalonTrot
										or AirRatatatRap
										or BeakBusterJump
									)
									or Flutter # 4 damage
								)
							)
						)
						or HardTediousJumps and ( # land in the window
							BreegullBashFall and (AirRatatatRap or BeakBuster)
							or BeakBuster and FallDamage # 4 damage
						)
					""",
					"Banjo": """
						PackWhack and (
							EasyTediousJumps and (ShackPackFall or TaxiPackFall)
							or HardTediousJumps and SackPackFall
						)
					""",
					"Kazooie": """
						ExtraClockworkUsage and EggUse
						or EasyTediousJumps and WingWhack
					""",
				},
			},
			"GI Outside: Broke Chimney": {
				"logic": {
					"Banjo-Kazooie": "EggAim and (GrenadeEggs or ClockworkKazooieEggs)",
					"Kazooie": "EggAim and (GrenadeEggs or ClockworkKazooieEggs)",
				},
			},
			"GI Outside: Atop Drain Pipe": {
				"logic": {
					"Banjo-Kazooie": """
						HardTediousJumps and (
							BeakBusterFall
							or WonderwingFall
							or FallDamage and (
								(HealthUpgrade, 2) # 6 damage
								or Flutter # 3 damage
								or AirRatatatRap # 3 damage
							)
							or BreegullBashFall and (Flutter or AirRatatatRap)
						)
					""",
					"Banjo": """
						HardTediousJumps and (
							PackWhackFall and (
								SackPackFall
								or ShackPackFall
								or TaxiPackFall
							)
							or SnoozePackFall
							or FallDamage and (HealthUpgrade, 4) # 6 damage
						)
					""",
					"Kazooie": "EasyTediousJumps",
				},
			},
			"GI Outside: Atop Front Door": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							BeakBusterFall
							or WonderwingFall
							or FallDamage and (
								HealthUpgrade # 5 damage
								or Flutter # 2 damage
								or AirRatatatRap # 2 damage
							)
							or BreegullBashFall and (Flutter or AirRatatatRap)
						)
					""",
					"Banjo": """
						EasyTediousJumps and (
							SackPackFall
							or ShackPackFall
							or SnoozePackFall
							or TaxiPackFall
							or FallDamage and (HealthUpgrade, 3) # 5 damage
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Outside: Atop Front Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							BeakBusterFall
							or WonderwingFall
							or FallDamage and (
								(HealthUpgrade, 2) # 6 damage
								or Flutter # 2 damage
								or AirRatatatRap # 3 damage
							)
							or BreegullBashFall and (Flutter or AirRatatatRap)
						)
					""",
					"Banjo": """
						EasyTediousJumps and (
							PackWhackFall and (SackPackFall or ShackPackFall)
							or TaxiPackFall
							or SnoozePackFall
							or FallDamage and (HealthUpgrade, 4) # 6 damage
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Outside: Flying": {
				"logic": {
					"Banjo-Kazooie": "FlightPad",
					"Kazooie": "FlightPad",
				},
			},
			"GI Outside: Jinjo Platform": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							FallDamage # 1 damage
							or Flutter
							or AirRatatatRap
							or BeakBusterFall
							or WonderwingFall
							or BreegullBashFall
						)
					""",
					"Banjo": """
						EasyTediousJumps and (
							PackWhackFall
							or SackPackFall
							or ShackPackFall
							or TaxiPackFall
							or SnoozePackFall
							or FallDamage # 1 damage
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Outside: Fire Exit Upper": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							FallDamage # 1 damage
							or Flutter
							or AirRatatatRap
							or BeakBusterFall
							or WonderwingFall
							or BreegullBashFall
						)
					""",
					"Banjo": """
						EasyTediousJumps and (
							PackWhackFall
							or SackPackFall
							or ShackPackFall
							or TaxiPackFall
							or SnoozePackFall
							or FallDamage # 1 damage
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Outside: Behind Window Above Front Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						GIOutsideBrokeWindowAboveFrontTrainTunnel and (
							EasyTediousJumps and FallDamage and (
								Flutter # 1 damage
								or AirRatatatRap # 2 damage
							)
							or HardTediousJumps and (
								BreegullBashFall and (Flutter or AirRatatatRap or BeakBuster)
							)
						)
					""",
					"Banjo": """
						GIOutsideBrokeWindowAboveFrontTrainTunnel and PackWhackFall and (
							EasyTediousJumps and (ShackPackFall or TaxiPackFall)
							or HardTediousJumps and SackPackFall
						)
					""",
					"Kazooie": "GIOutsideBrokeWindowAboveFrontTrainTunnel",
				},
			},
			"GI Outside: Behind Window Near Back Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						GIOutsideBrokeWindowNearBackTrainTunnel and (
							EasyTediousJumps and FallDamage and (
								Flutter # 1 damage
								or AirRatatatRap # 2 damage
							)
							or HardTediousJumps and (
								BreegullBashFall and (Flutter or AirRatatatRap or BeakBuster)
							)
						)
					""",
					"Banjo": """
						GIOutsideBrokeWindowNearBackTrainTunnel and PackWhackFall and (
							EasyTediousJumps and (ShackPackFall or TaxiPackFall)
							or HardTediousJumps and SackPackFall
						)
					""",
					"Kazooie": "GIOutsideBrokeWindowNearBackTrainTunnel",
				},
			},
			"GI Outside: Upper Roof": {
				"logic": {
					"Banjo-Kazooie": "TallJump or FreeShockSpringPad",
					"Banjo": "SackPackEndingJump and PackWhackJump and TallJump",
					"Kazooie": "TallJump or FreeShockSpringPad or LegSpring",
				},
			}
		}
	},
	"GI Outside: Upper Roof": {
		"exits": {
			"GI Floor 5: Storage Area 2 Top Of Boxes Near Exit": {
				"id": 0x03,
				"logic": "GIOutsideBrokeUpperMiddleWindow",
			},
			"GI Outside: Broke Upper Middle Window": {
				"logic": {
					"Banjo-Kazooie": """
						GroundRatatatRap
						or AirRatatatRap
						or BeakBarge
						or BeakBuster
						or EggAim and AnyEggs
						or ThirdPersonEggShooting and (
							BlueEggs
							or FireEggs
							or IceEggs
							or DamageBoost and (GrenadeEggs or ClockworkKazooieEggs)
						)
					""",
					"Banjo": "PackWhack",
					"Kazooie": """
						WingWhack
						or EggAim and AnyEggs
						or ThirdPersonEggShooting and (
							BlueEggs
							or FireEggs
							or IceEggs
							or DamageBoost and (GrenadeEggs or ClockworkKazooieEggs)
						)
					""",
				},
			},
			"GI Outside: Lower Roof": {},
			"GI Outside: Upper Roof Side Window": {
				"logic": {
					"Banjo-Kazooie": "TalonTrot or EasyTediousJumps",
					"Talon Trot": "",
					"Banjo": "EasyTediousJumps",
					"Kazooie": "",
				},
			}
		}
	},
	"GI Outside: Upper Roof Side Window": {
		"exits": {
			"GI Floor 5: Storage Area 1 Catwalk": {
				"id": 0x02,
				"logic": "GIOutsideBrokeUpperSideWindow",
			},
			"GI Outside: Broke Upper Side Window": {
				"logic": {
					"Banjo-Kazooie": """
						GroundRatatatRap
						or AirRatatatRap
						or BeakBarge
						or BeakBuster
						or EggAim and AnyEggs
						or ThirdPersonEggShooting and (
							BlueEggs
							or FireEggs
							or IceEggs
							or DamageBoost and (GrenadeEggs or ClockworkKazooieEggs)
						)
					""",
					"Banjo": "PackWhack",
					"Kazooie": """
						WingWhack
						or EggAim and AnyEggs
						or ThirdPersonEggShooting and (
							BlueEggs
							or FireEggs
							or IceEggs
							or DamageBoost and (GrenadeEggs or ClockworkKazooieEggs)
						)
					""",
				},
			},
			"GI Outside: Lower Roof": {},
			"GI Outside: Upper Roof": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							TalonTrot and (Flutter or AirRatatatRap)
						)
					""",
					"Kazooie": "EasyTediousJumps",
				},
			}
		}
	},
	"GI Outside: Behind Floor 1 Window": {
		"exits": {
			"GI Floor 1: Upper Catwalk": {"id": 0x03},
			"GI Outside: Broke Floor 1 Window": {
				"logic": {
					"Banjo-Kazooie": """
						GroundRatatatRap
						or AirRatatatRap
						or BeakBarge
						or BeakBuster
						or EggUse and (
							BlueEggs
							or FireEggs
							or IceEggs
							or DamageBoost and (GrenadeEggs or ClockworkKazooieEggs)
						)
					""",
					"Banjo": "PackWhack",
					"Kazooie": """
						WingWhack
						or EggUse and (
							BlueEggs
							or FireEggs
							or IceEggs
							or DamageBoost and (GrenadeEggs or ClockworkKazooieEggs)
						)
					""",
				},
			},
			"GI Outside": {
				"logic": {
					"Banjo-Kazooie": """
						FallDamage # 1 damage
						or Flutter
						or AirRatatatRap
						or BeakBusterFall
						or WonderwingFall
						or BreegullBashFall
					""",
					"Banjo": """
						PackWhackFall
						or SackPackFall
						or ShackPackFall
						or SnoozePackFall
						or TaxiPackFall
						or FallDamage # 1 damage
					""",
					"Kazooie": "",
				},
			},
			"GI Outside: Atop Front Door": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							FlapFlip and (GripGrab or BeakBusterJump)
						)
					""",
					"Banjo": "EasyTediousJumps and PackWhackJump and TallJump",
					"Kazooie": "EasyTediousJumps and LegSpring",
				},
			}
		}
	},
	"GI Outside: Behind Window Above Front Train Tunnel": {
		"exits": {
			"GI Floor 2: Near Window With Page": {"id": 0x07},
			"GI Outside: Broke Window Above Front Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						GroundRatatatRap
						or AirRatatatRap
						or BeakBarge
						or BeakBuster
						or EggUse and (
							BlueEggs
							or FireEggs
							or IceEggs
							or DamageBoost and (GrenadeEggs or ClockworkKazooieEggs)
						)
					""",
					"Banjo": "PackWhack",
					"Kazooie": """
						WingWhack
						or EggUse and (
							BlueEggs
							or FireEggs
							or IceEggs
							or DamageBoost and (GrenadeEggs or ClockworkKazooieEggs)
						)
					""",
				},
			},
			"GI Outside: Flying": {
				"logic": {
					"Banjo-Kazooie": "FlightPad",
					"Kazooie": "FlightPad",
				},
			},
			"GI Outside: Atop Front Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						FallDamage # 1 damage
						or Flutter
						or AirRatatatRap
						or BeakBusterFall
						or WonderwingFall
						or BreegullBashFall
					""",
					"Banjo": """
						PackWhackFall
						or SackPackFall
						or ShackPackFall
						or SnoozePackFall
						or TaxiPackFall
						or FallDamage # 1 damage
					""",
					"Kazooie": "",
				},
			},
			"GI Outside: Atop Drain Pipe": {
				"logic": {
					"Banjo-Kazooie": """
						EasyTediousJumps and (
							Flutter
							or AirRatatatRap
							or RollJump and (
								BeakBusterJump
								or TallJump and FallDamage # 1 damage
								or FlapFlip and BeakBusterJump
							)
							or (TallJump or FlapFlip) and BillDrillJump
							or TalonTrot and FallDamage # 1 damage
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyTediousJumps and FallDamage"}, # 1 damage
					"Kazooie": "EasyTediousJumps",
				},
			}
		}
	},
	"GI Outside: Behind Window Near Back Train Tunnel": {
		"exits": {
			"GI Floor 2: Near Window With Unscrewable Plate": {"id": 0x06},
			"GI Outside: Broke Window Near Back Train Tunnel": {
				"logic": {
					"Banjo-Kazooie": """
						GroundRatatatRap
						or AirRatatatRap
						or BeakBarge
						or BeakBuster
						or EggUse and (
							BlueEggs
							or FireEggs
							or IceEggs
							or DamageBoost and (GrenadeEggs or ClockworkKazooieEggs)
						)
					""",
					"Banjo": "PackWhack",
					"Kazooie": """
						WingWhack
						or EggUse and (
							BlueEggs
							or FireEggs
							or IceEggs
							or DamageBoost and (GrenadeEggs or ClockworkKazooieEggs)
						)
					""",
				},
			},
			"GI Outside: Flying": {
				"logic": {
					"Banjo-Kazooie": "FlightPad",
					"Kazooie": "FlightPad",
				},
			},
			"GI Outside": {
				"logic": {
					"Banjo-Kazooie": """
						(
							FallDamage # 1 damage
							or Flutter
							or AirRatatatRap
							or BeakBusterFall
							or WonderwingFall
							or BreegullBashFall
						) and (
							DamageBoost
							or WonderwingDamageBoost
							or DragundaSidle
						)
					""",
					"Banjo": """
						(
							PackWhackFall
							or SackPackFall
							or ShackPackFall
							or SnoozePackFall
							or TaxiPackFall
							or FallDamage # 1 damage
						) and (
							DamageBoost
							or DragundaSidle
							or SackPack
							or ShackPack
						)
					""",
					"Kazooie": "",
				},
			}
		}
	},
	"GI Outside: Broke Floor 1 Window": {"macro": {"event"}},
	"GI Outside: Broke Window Above Front Train Tunnel": {"macro": {"event"}},
	"GI Outside: Broke Window Near Back Train Tunnel": {"macro": {"event"}},
	"GI Outside: Break Lower Windows": {
		"exits": {
			"GI Outside: Broke Floor 1 Window": {},
			"GI Outside: Broke Window Above Front Train Tunnel": {},
			"GI Outside: Broke Window Near Back Train Tunnel": {},
		},
	},
	"GI Outside: Broke Upper Middle Window": {"macro": {"event"}},
	"GI Outside: Broke Upper Side Window": {"macro": {"event"}},
	"GI Outside: Break Upper Windows": {
		"exits": {
			"GI Outside: Broke Upper Middle Window": {},
			"GI Outside: Broke Upper Side Window": {},
		},
	},
	"GI Outside: Broke Chimney": {"macro": {"event"}},
}
