from .. import Regions
default_id = 0x0108
instant_transform = {"Mumbo", "Washer"}
regions: Regions = {
	"GI Floor 3: Near Mumbo's Skull": {
		"locations": {
			"GI Floor 3: Delivered Battery": {
				"logic": {
					"Banjo": """
						PackWhack and TaxiPack
						and can_form_from_region_reach(
							"Banjo",
							"GI Floor 3: Near Mumbo's Skull",
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
			"GI Floor 3: Floor 2 Platform": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
					"Kazooie": "LegSpring",
				},
			},
			"GI Floor 3: Outside Mumbo's Skull": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or BeakBusterJump
						or WonderwingJump
						or DamageBoostJump
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": "TallJump or LegSpring or DamageBoostJump",
				},
			},
			"GI Floor 3: Near Service Elevator": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or BeakBusterJump
						or WonderwingJump
						or DamageBoostJump
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": "TallJump or LegSpring or DamageBoostJump",
				},
			},
			"GI Floor 3: Top Of Boxes Near Boiler Plant": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and (GripGrab or BeakBusterJump)
						or EasyJumps and (
							(
								GripGrab and (
									TallJump
									or TalonTrot and Flutter
									or WonderwingJump
								)
								or FlapFlip
							) and (
								Flutter and (
									TallJump and (
										BeakBusterJump
										or GripGrab
									)
									or TalonTrot and (GripGrab or BeakBusterJump or TalonTrotSlideJump)
								)
								or AirRatatatRap and (
									TallJump and (
										BeakBusterJump
										or GripGrab
									)
									or TalonTrot
								)
							)
						)
					""",
					"Banjo": """
						EasyJumps and (
							PackWhackJump and TallJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "LegSpring",
				},
			},
			"GI Floor 3: Top Of Boxes Opposite Boiler Plant": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and (GripGrab or BeakBusterJump)
						or EasyJumps and (
							(
								GripGrab and (
									TallJump
									or TalonTrot and Flutter
									or WonderwingJump
								)
								or FlapFlip
							) and (
								(Flutter or AirRatatatRap) and (
									(TallJump or TalonTrot) and (GripGrab or BeakBusterJump)
								)
							)
						)
					""",
					"Banjo": """
						EasyJumps and (
							PackWhackJump and (TallJump or GripGrab)
							or SackPackAirJump
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Floor 3: Top Of Boxes With Split Up Pads": {
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
					"Kazooie": "TallJump or LegSpring or DamageBoostJump",
				},
			},
		}
	},
	"GI Floor 3: Floor 2 Platform": {
		"exits": {
			"GI Floor 2: Platform Near Floor 3": {"id": 0x08},
			"GI Floor 3: Near Mumbo's Skull": {},
			"GI Floor 3: Top Of Boxes With Glowbo": {
				"logic": {
					"Banjo": """
						EasyJumps and (
							PackWhackJump and (TallJump or GripGrab or SackPackAirJump)
							or SackPackEndingJump
						)
					""",
					"Kazooie": "Glide or EasyJumps",
				}
			}
		}
	},
	"GI Floor 3: Outside Mumbo's Skull": {
		"locations": {
			"GI Floor 3: Outside Mumbo's Skull Warp Pad Tagged": {"item": "GIFloor3OutsideMumbosSkullWarpPad"},
		},
		"exits": {
			"GI Floor 3: Mumbo's Skull": {"id": 0x01},
			"GI Floor 2: Near Wumba's Wigwam": {
				"id": 0x09,
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							( # to skull eye
								FlapFlip
								or TallJump and BeakBusterJump
								or TalonTrot and (Flutter or AirRatatatRap)
							) and ( # from skull eye
								TallJump and BeakBusterJump
								or TalonTrot
								or Flutter
								or AirRatatatRap
								or RollJump and FlapFlipSlideExtension and BeakBusterJump
							)
						)
					""",
					"Banjo": """
						EasyJumps and (
							PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "LegSpring or EasyJumps and TallJump",
				}
			},
			"GI: Warp Pads": {"logic": "GIFloor3OutsideMumbosSkullWarpPad"},
			"GI Floor 3: Near Mumbo's Skull": {},
			"GI Floor 3: Top Of Ducts": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or GripGrab
						or BeakBusterJump
						or WonderwingJump
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": "TallJump or LegSpring",
				},
			},
			"GI Floor 3: Top Of Boxes With Ducts": {
				"logic": {
					"Banjo-Kazooie": """
						Flutter
						or AirRatatatRap
						or EasyJumps and (
							RollJump
							or GroundRatatatRapJump
							or SlideJump
						)
					""",
					"Kazooie": "",
				},
			},
		}
	},
	"GI Floor 3: Top Of Ducts": {
		"locations": {
			"GI Floor 3: Near Mumbo's Skull Egg Nest": {"item": "EggNest"},
		},
		"exits": {
			"GI Floor 3: Outside Mumbo's Skull": {},
			"GI Floor 3: Top Of Boxes With Ducts": {},
		}
	},
	"GI Floor 3: Mumbo's Skull": {
		"id": 0x0172,
		"instant_transform": {"Washer"},
		"locations": {
			"GI: Mumbo Transform": {
				"logic": {"Banjo-Kazooie": "MumboEMP"},
			}
		},
		"exits": {
			"GI Floor 3: Outside Mumbo's Skull": {"id": 0x0A},
			"GI Floor 3: Mumbo's Skull": {
				"logic": {"Banjo-Kazooie": {"Mumbo": "GIMumboTransform"}},
			}
		}
	},
	"GI Floor 3: Near Service Elevator": {
		"exits": {
			"GI Floor 3: Near Mumbo's Skull": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or BeakBusterJump
						or WonderwingJump
						or DamageBoostJump
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": "TallJump or LegSpring or DamageBoostJump",
				},
			},
			"GI Floor 3: Top Of Boxes Near Empty Honeycomb": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							FlapFlip and (
								(TallJump or TalonTrot) and Flutter and GripGrab
							)
						)
					""",
					"Banjo": """
						EasyJumps and (
							PackWhackJump and (TallJump or GripGrab)
							or SackPackAirJump
						)
					""",
					"Kazooie": "LegSpring",
				},
			},
			"GI Floor 3: Top Of Boxes Opposite Boiler Plant": {
				"logic": {
					"Banjo-Kazooie": """
						Climb and (
							FlapFlip
							or EasyJumps and (
								GripGrab and (
									TallJump
									or TalonTrot and Flutter
								)
							)
						)
					""",
					"Banjo": """
						Climb and (
							GripGrab
							or PackWhackJump and TallJump
							or SackPackAirJump
						)
					""",
				},
			},
			"GI Floor 3: Top Of Boxes Near Fire Exit": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip
						or EasyJumps and (
							GripGrab and (
								TallJump
								or TalonTrot and Flutter
							)
						)
					""",
					"Banjo": """
						GripGrab
						or EasyJumps and (
							PackWhackJump and TallJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "LegSpring",
				},
			},
			"GI Floor 3: Top Of Boxes With Ducts": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or EasyJumps and (
							BeakBusterJump
							or WonderwingJump
							or Climb
						)
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": "TallJump or LegSpring",
				},
			},
			"GI Floor 3: Top Of Boxes Near Ducts": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump and GripGrab
						or FlapFlip
						or EasyJumps and (
							TalonTrot and Flutter and GripGrab
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and Flutter and GripGrab"},
					"Kazooie": "LegSpring",
				},
			},
			"GI Floor 3: Catwalk": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
					"Kazooie": "LegSpring",
				},
			},
			"GI Floor 3: Near Skivvy": {"logic": {"Washer"}},
			"GI: Service Elevator": {"logic": {"Washer"}},
		}
	},
	"GI Floor 3: Near Skivvy": {
		"id": 0x0109,
		"exits": {
			"GI Floor 3: Near Service Elevator": {"logic": {"Washer"}},
			"GI Floor 3: Skivvy": {"logic": {"Washer"}},
		}
	},
	"GI Floor 3: Top Of Boxes With Glowbo": {
		"locations": {
			"GI Floor 3: Glowbo": {"item": "MumboEMP"},
		},
		"exits": {
			"GI Floor 3: Top Of Boxes Near Boiler Plant": {
				"logic": {
					"Banjo": """
						EasyJumps and (
							SackPackEndingJump and TallJump and (GripGrab or PackWhackJump)
						)
					""",
				}
			},
		}
	},
	"GI Floor 3: Top Of Boxes Near Boiler Plant": {
		"exits": {
			"GI Floor 3: Boiler Plant": {"id": 0x01},
			"GI Floor 3: Near Mumbo's Skull": {},
			"GI Floor 3: Near Service Elevator": {},
			"GI Floor 3: Top Of Boxes With Glowbo": {},
			"GI Floor 3: Top Of Boxes With Nests Near Boiler Plant": {},
			"GI Floor 3: Top Of Boxes Near Empty Honeycomb": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or EasyJumps and (
							FlapFlip
							or Flutter
							or AirRatatatRap
							or GripGrab
							or BeakBusterJump
							or WonderwingJump
						)
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": "TallJump or LegSpring",
				},
			},
			"GI Floor 3: Top Of Boxes Opposite Boiler Plant": {
				"logic": {
					"Banjo-Kazooie": "FlapFlip and (GripGrab or BeakBusterJump)",
					"Banjo": """
						EasyJumps and (
							PackWhackJump and (TallJump or SackPackAirJump)
							or SackPackEndingJump and TallJump
						)
					""",
					"Kazooie": """
						Glide
						or EasyJumps and (TallJump or WingWhack)
					""",
				},
			},
		}
	},
	"GI Floor 3: Top Of Boxes With Nests Near Boiler Plant": {
		"locations": {
			"GI Floor 3: On Boxes Feather Nest 1": {"item": "FeatherNest"},
			"GI Floor 3: On Boxes Feather Nest 2": {"item": "FeatherNest"},
		}
	},
	"GI Floor 3: Top Of Boxes Near Empty Honeycomb": {
		"locations": {
			"GI Floor 3: Honeycomb": {
				"item": "EmptyHoneycomb",
				"logic": {
					"Banjo-Kazooie": """
						(AnyAttack or EggUse and AnyEggs) and (TallJump or FreeShockSpringPad) and (GripGrab or BeakBusterJump)
					""",
					"Banjo": """
						EasyJumps and (
							SackPackEndingJump and TallJump and PackWhackJump and GripGrab
						)
					""",
					"Kazooie": """
						(WingWhack or EggUse and AnyEggs) and (
							TallJump
							or FreeShockSpringPad
							or LegSpring
						)
					""",
				},
			},
		},
		"exits": {
			"GI Floor 3: Near Service Elevator": {},
			"GI Floor 3: Top Of Boxes With Nests Near Boiler Plant": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or Flutter
						or AirRatatatRap
						or EasyJumps and (
							FlapFlip
							or BeakBusterJump
							or (RollJump or SlideJump) and GripGrab
							or WonderwingJump
						)
					""",
					"Talon Trot": "",
					"Banjo": """
						TallJump
						or PackWhackJump
						or SackPack
						or EasyJumps and GripGrab
					""",
					"Kazooie": "",
				},
			},
			"GI Floor 3: Notes Catwalk": {
				"logic": {
					"Banjo-Kazooie": """
						Climb and (
							TallJump
							or TalonTrot
							or Flutter
							or AirRatatatRap
							or EasyJumps and (
								FlapFlip and (GripGrab or BeakBusterJump)
								or FlapFlipSlideExtension
								or (RollJump or SlideJump) and BeakBusterJump
								or WonderwingJump
								or AnyAttack and FreeShockSpringPad and (
									FlapFlip
									or BeakBusterJump
									or RollJump
									or SlideJump
								)
							)
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "Climb"},
					"Banjo": """
						Climb and (
							TallJump
							or EasyJumps and (
								GripGrab
								or PackWhackJump
								or SackPack
							)
						)
					""",
					"Kazooie": "LegSpring and Glide",
				},
			},
		}
	},
	"GI Floor 3: Top Of Boxes Opposite Boiler Plant": {
		"locations": {
			"GI Floor 3: On High Box Stack Egg Nest": {
				"item": "EggNest",
				"explicit_logic": {
					"Kazooie": "LegSpring",
				}
			},
		},
		"exits": {
			"GI Floor 3: Near Mumbo's Skull": {},
			"GI Floor 3: Near Service Elevator": {},
			"GI Floor 3: Top Of Boxes Near Boiler Plant": {
				"logic": {
					"Banjo-Kazooie": """
						GripGrab and (
							TallJump
							or FlapFlip
						)
						or EasyJumps and (
							TalonTrot and Flutter and GripGrab
							or FlapFlip
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and Flutter and GripGrab"},
					"Banjo": """
						GripGrab
						or EasyJumps and (
							PackWhackJump and TallJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "EasyJumps and (TallJump or LegSpring) and WingWhack",
				},
			},
		}
	},
	"GI Floor 3: Top Of Boxes With Split Up Pads": {
		"macro": {"splitup"},
		"exits": {
			"GI Floor 3: Near Mumbo's Skull": {},
		}
	},
	"GI Floor 3: Top Of Boxes Near Fire Exit": {
		"locations": {
			"GI Floor 3: Under Notes Egg Nest": {"item": "EggNest"},
		},
		"exits": {
			"GI Floor 3: Near Service Elevator": {},
		}
	},
	"GI Floor 3: Top Of Boxes With Ducts": {
		"exits": {
			"GI Floor 3: Near Mumbo's Skull": {},
			"GI Floor 3: Outside Mumbo's Skull": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							TallJump
							or TalonTrot
							or Flutter
							or AirRatatatRap
							or GripGrab
							or BeakBusterJump
							or WonderwingJump
						)
					""",
					"Talon Trot": "EasyJumps",
					"Kazooie": "EasyJumps",
				},
			},
			"GI Floor 3: Top Of Ducts": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump and GripGrab
						or FlapFlip
					""",
					"Banjo": "",
					"Kazooie": "LegSpring",
				},
			},
			"GI Floor 3: Near Service Elevator": {},
			"GI Floor 3: Top Of Boxes Near Ducts": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or GripGrab and (Flutter or AirRatatatRap)
						or EasyJumps and (
							FlapFlip
							or Flutter
							or AirRatatatRap
							or GripGrab
							or BeakBusterJump
							or RollJump
							or WonderwingJump
							or SlideJump
						)
					""",
					"Talon Trot": "",
					"Banjo": "TallJump or EasyJumps",
					"Kazooie": "TallJump or LegSpring",
				},
			},
		}
	},
	"GI Floor 3: Top Of Boxes Near Ducts": {
		"locations": {
			"GI Floor 3: On Crate Egg Nest": {"item": "EggNest"},
		}
	},
	"GI Floor 3: Catwalk": {
		"exits": {
			"GI Outside: Fire Exit Lower": {"id": 0x07},
			"GI Floor 3: Near Service Elevator": {},
			"GI Floor 3: Top Of Boxes Near Fire Exit": {},
			"GI Floor 3: Top Of Boxes With Ducts": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							FallDamage # 1 damage
							or Flutter
							or AirRatatatRap
							or BeakBusterFall
							or WonderwingFall
							or BreegullBashFall
							or GroundRatatatRapFall
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Floor 3: Notes Catwalk": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							Flutter and (
								TallJump and (GripGrab or BeakBusterJump)
								or TalonTrot
							)
							or AirRatatatRap and (
								TallJump and (GripGrab or BeakBusterJump or RollJump)
								or TalonTrot
							)
							or FlapFlip and Flutter and (GripGrab or BeakBusterJump)
							or RollJump and FlapFlipSlideExtension and Flutter
						)
						or HardJumps and (
							FlapFlipSlideExtension and Flutter
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and (Flutter or AirRatatatRap)"},
					"Banjo": """
						EasyJumps and (
							PackWhackJump and (TallJump or GripGrab)
							or SackPackAirJump
						)
					""",
					"Kazooie": "Glide or EasyJumps",
				},
			},
		}
	},
	"GI Floor 3: Notes Catwalk": {
		"locations": {
			"GI Floor 3: Note 1": {"item": "NoteNest"},
			"GI Floor 3: Note 2": {"item": "NoteNest"},
		},
		"exits": {
			"GI Floor 3: Top Of Boxes Near Empty Honeycomb": {},
			"GI Floor 3: Top Of Boxes Near Fire Exit": {},
			"GI Floor 3: Catwalk": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							Flutter and (
								TallJump and (GripGrab or BeakBusterJump)
								or TalonTrot
							)
							or AirRatatatRap and (
								TallJump and (GripGrab or BeakBusterJump or RollJump)
								or TalonTrot
							)
							or FlapFlip and Flutter and (GripGrab or BeakBusterJump)
							or RollJump and FlapFlipSlideExtension and Flutter
						)
						or HardJumps and (
							FlapFlipSlideExtension and Flutter
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and (Flutter or AirRatatatRap)"},
					"Banjo": """
						EasyJumps and (
							PackWhackJump and (TallJump or GripGrab)
							or SackPackAirJump
						)
					""",
					"Kazooie": "Glide or EasyJumps",
				},
			},
		}
	},
	"GI Floor 3: Boiler Plant": {
		"id": 0x0109,
		"macro": {"rejoin"},
		"locations": {
			"GI Floor 3: Unscrewed Plate": {"logic": {"Banjo-Kazooie": "BillDrill"}},
			"GI Floor 3: Boiler Plant Left Egg Nest": {"item": "EggNest"},
			"GI Floor 3: Boiler Plant Right Egg Nest": {"item": "EggNest"},
			"GI Floor 3: Opened Twinkly Packing Door": {
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
			"GI Floor 3: Top Of Boxes Near Boiler Plant": {"id": 0x03},
			"GI Floor 3: Boiler Plant Behind Elevator Door": {"logic": "GIFloor3OpenedElevatorDoor"},
			"GI Floor 3: Boiler Plant Behind Twinkly Packing Door": {"logic": "GIFloor3OpenedTwinklyPackingDoor"},
			"GI Floor 3: Opened Elevator Door": {
				"logic": {
					"Banjo-Kazooie": """
						GroundRatatatRap
						or AirRatatatRap
						or BeakBarge
						or EggUse and GrenadeEggs
					""",
					"Banjo": "PackWhack",
					"Kazooie": "EggUse and GrenadeEggs",
				},
			},
			"GI Floor 3: Boiler Plant Top of Boiler": {
				"logic": {
					"Kazooie": "LegSpring and Glide",
				},
			},
		},
	},
	"GI Floor 3: Boiler Plant Top of Boiler": {
		"id": 0x0109,
		"locations": {
			"GI Floor 3: Boiler Plant Jinjo": {"item": "PurpleJinjo"},
		},
		"exits": {
			"GI Floor 3: Boiler Plant": {},
		}
	},
	"GI Floor 3: Boiler Plant Behind Elevator Door": {
		"id": 0x0109,
		"exits": {
			"GI Elevator Shaft: Floor 3": {"id": 0x02},
			"GI Floor 3: Boiler Plant": {"logic": "GIFloor3OpenedElevatorDoor"},
			"GI Floor 3: Opened Elevator Door": {
				"logic": {
					"Banjo-Kazooie": "BreegullBashClip",
				},
			},
		}
	},
	"GI Floor 3: Twinkly Packing": {
		"id": 0x010A,
		"locations": {
			"GI Floor 3: Cleared Twinkly Packing": {
				"logic": {
					"Banjo-Kazooie": "TurboTrainers",
					"Kazooie": "TurboTrainers",
				},
			},
			"GI Floor 3: Twinkly Packing Jiggy": {
				"item": "Jiggy",
				"logic": "GIFloor3ClearedTwinklyPacking",
			},
			"GI Floor 3: Twinkly Packing Mumbo Token": {
				"item": {"MumboToken":"'Twinkly Packing' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Twinkly Packing' in VictoryGoals",
				"locked": "true",
				"logic": "GIFloor3ClearedTwinklyPacking",
			},
		},
		"exits": {
			"GI Floor 3: Boiler Plant Behind Twinkly Packing Door": {"id": 0x04},
			"GI Floor 3: Twinkly Packing": {"logic": {"BK Turbo Trainers": "TurboTrainers"}}
		}
	},
	"GI Floor 3: Boiler Plant Behind Twinkly Packing Door": {
		"id": 0x0109,
		"exits": {
			"GI Floor 3: Twinkly Packing": {"id": 0x01},
			"GI Floor 3: Boiler Plant": {"logic": "GIFloor3OpenedTwinklyPackingDoor"}
		}
	},
	"GI Floor 3: Opened Elevator Door": {"macro": {"event"}},
}
