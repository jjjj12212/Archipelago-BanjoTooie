from .. import Regions
default_id = 0x010B
instant_transform = {"Mumbo", "Washer"}
regions: Regions = {
	"GI Floor 4": {
		"locations": {
			"GI Floor 4: Activated Flight Pads": {},
			"GI Floor 4: Near Fire Exit Egg Nest 1": {
				"item": "EggNest",
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
				}
			},
			"GI Floor 4: Near Fire Exit Egg Nest 2": {
				"item": "EggNest",
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
				}
			},
			"GI Floor 4: Near Fire Exit Egg Nest 3": {
				"item": "EggNest",
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
				}
			},
			"GI Floor 4: Near Service Elevator Feather Nest 1": {"item": "FeatherNest"},
			"GI Floor 4: Near Service Elevator Feather Nest 2": {"item": "FeatherNest"},
		},
		"exits": {
			"GI Floor 4: Fire Exit Platform": {
				"logic": {
					"Banjo-Kazooie": "EasyJumps and FlapFlip and GripGrab",
					"Banjo": """
						EasyJumps and (
							SackPackEndingJump and TallJump and PackWhackJump
						)
					""",
				},
			},
			"GI Floor 4: Before Crushers": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or BillDrillJump
						or WonderwingJump
						or DamageBoostJump
						or EasyJumps and (
							RollJump and (Flutter or AirRatatatRap) and BeakBusterJump
						)
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": """
						TallJump
						or LegSpring
						or EasyJumps
					""",
					"BK Springy Step Shoes": "",
					"SK Springy Step Shoes": "",
				},
			},
			"GI Floor 4": {
				"logic": {
					"Banjo-Kazooie": {"BK Springy Step Shoes": "SpringyStepShoes and (AnyAttack or EggUse and AnyEggs)"},
					"Kazooie": {"SK Springy Step Shoes": "SpringyStepShoes and (WingWhack or EggUse and AnyEggs)"},
				}
			},
			"GI Floor 4: Before Crushers Catwalk": {"logic": {"SK Springy Step Shoes": ""}},
			"GI: Service Elevator": {"logic": {"Washer"}},
		}
	},
	"GI Floor 4: Fire Exit Platform": {
		"exits": {
			"GI Outside: Fire Exit Upper": {"id": 0x08},
			"GI Floor 4": {},
		}
	},
	"GI Floor 4: Before Crushers": {
		"locations": {
			"GI Floor 4: Box Near Crushers Egg Nest": {
				"item": "EggNest",
				"logic": {
					"Banjo-Kazooie": "AnyAttack or EggUse and AnyEggs",
					"Banjo": "PackWhack",
					"Kazooie": "WingWhack or EggUse and AnyEggs",
				},
			},
			"GI Floor 4: Near the Crushers Warp Pad Tagged": {"item": "GIFloor4NearTheCrushersWarpPad"},
		},
		"exits": {
			"GI: Warp Pads": {"logic": "GIFloor4NearTheCrushersWarpPad"},
			"GI Floor 4": {},
			"GI Floor 4: Before Crushers Catwalk": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or EasyJumps and GripGrab
						or BeakBusterJump
						or WonderwingJump
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": "TallJump or LegSpring",
					"Mumbo": "TallJump",
				},
			},
			"GI Floor 4: After Crushers": {
				"logic": "GIFloor4DisabledCrushers",
				"explicit_logic": {"Banjo-Kazooie": "GIFloor4EMPWallCrushers or GIFloor4DisabledCrushers"},
			},
		}
	},
	"GI Floor 4: Before Crushers Catwalk": {
		"macro": {"splitup"},
		"locations": {
			"GI Floor 4: EMP Wall Crushers": {"logic": {"Mumbo"}},
		},
		"exits": {
			"GI Floor 5: Storage Area 1 Near Floor Exit": {
				"id": 0x01,
				"logic": {
					"Banjo-Kazooie": "GIFloor5UnscrewedPlate and (TallJump or FreeShockSpringPad)",
					"Kazooie": "GIFloor5UnscrewedPlate and (TallJump or FreeShockSpringPad)",
				},
			},
			"GI Floor 4: Before Crushers": {},
		}
	},
	"GI Floor 4: After Crushers": {
		"locations": {
			"GI Floor 4: Disabled Crushers": {"logic": {"Banjo-Kazooie"}},
		},
		"exits": {
			"GI Floor 4: Before Crushers Catwalk": {"id": 0x07},
			"GI Floor 4: Before Crushers": {"logic": "GIFloor4DisabledCrushers"},
			"GI Floor 4: After Crushers Lower Catwalk": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
					"Kazooie": "TallJump or EasyJumps and LegSpring",
				},
			},
		}
	},
	"GI Floor 4: After Crushers Lower Catwalk": {
		"macro": {"rejoin"},
		"locations": {
			"GI Floor 4: Near Battery Door Egg Nest": {"item": "EggNest"},
			"GI Floor 4: Opened Cable Room Door": {
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
			"GI Floor 4: Cable Room": {
			  "id": 0x01,
			  "logic": "GIFloor4OpenedCableRoomDoor",
			},
			"GI Floor 4: Opened Elevator Door": {
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
			"GI Floor 4: After Crushers": {},
			"GI Floor 4: Behind Elevator Door": {"logic": "GIFloor4OpenedElevatorDoor"},
			"GI Floor 4: After Crushers Lower Catwalk": {
				"logic": {
					"Banjo-Kazooie": {"BK Claw Clamber Boots": "ClawClamberBoots"},
					"Kazooie": {"SK Claw Clamber Boots": "ClawClamberBoots"},
				},
			},
			"GI Floor 4: After Crushers Upper Catwalk": {
				"logic": {"BK Claw Clamber Boots", "SK Claw Clamber Boots"},
			}
		}
	},
	"GI Floor 4: After Crushers Upper Catwalk": {
		"exits": {
			"GI Floor 4: Sewer Entrance": {"id": 0x01},
			"GI Floor 4: After Crushers Lower Catwalk": {},
		}
	},
	"GI Floor 4: Behind Elevator Door": {
		"exits": {
			"GI Elevator Shaft: Floor 4": {"id": 0x03},
			"GI Floor 4: Opened Elevator Door": {
				"logic": {
					"Banjo-Kazooie": "BreegullBashClip",
				},
			},
			"GI Floor 4: After Crushers Lower Catwalk": {"logic": "GIFloor4OpenedElevatorDoor"},
		}
	},
	"GI Floor 4: Cable Room": {
		"id": 0x010C,
		"locations": {
			"GI Floor 4: Pressed Quality Control Vent Button": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or BeakBusterJump
						or WonderwingJump
						or DamageBoost
					""",
					"Talon Trot": "",
					"Banjo": "GIQualityControlVentAsBanjo",
					"Kazooie": "TallJump or LegSpring or DamageBoostJump",
				},
			}
		},
		"exits": {
			"GI Floor 4: After Crushers Lower Catwalk": {"id": 0x05},
			"GI Floor 4: Quality Control Front": {},
		}
	},
	"GI Floor 4: Quality Control Front": {
		"id": 0x010D,
		"locations": {
			"GI Floor 4: Spawned Quality Control Jiggy": {
				"logic": {
					"Banjo-Kazooie": "EggAim and GrenadeEggs and GIFloor4PressedQualityControlVentButton",
					"Kazooie": "EggAim and GrenadeEggs and GIFloor4PressedQualityControlVentButton",
				},
			},
			"GI Floor 4: Cable Room": {},
			"GI Floor 4: Quality Control Pit": {},
		},
		"exits": {
			"GI Floor 4: Quality Control 3 Egg Nests": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							Flutter
							or AirRatatatRap
						)
					""",
					"Kazooie": "EasyJumps",
				}
			},
			"GI Floor 4: Quality Control Back": {
				"logic": {
					"Banjo": """
						EasyJumps and (
							SackPackAirJump and PackWhack
						)
					""",
					"Kazooie": "LegSpring and (Glide or EasyJumps)",
				}
			}
		}
	},
	"GI Floor 4: Quality Control Pit": {
		"id": 0x010D,
		"exits": {
			"GI Floor 4: Quality Control Front": {
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
			"GI Floor 4: Quality Control 2 Egg Nests": {
				"logic": {
					"Banjo-Kazooie": "GripGrab",
				}
			},
			"GI Floor 4: Quality Control 3 Egg Nests": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or AirRatatatRapClip
						or BeakBusterJump
						or WonderwingJump
						or DamageBoostJump
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": "TallJump or LegSpring",
				}
			},
		}
	},
	"GI Floor 4: Quality Control 2 Egg Nests": {
		"locations": {
			"GI Floor 4: Quality Control Egg Nest 1": {"item": "EggNest"},
			"GI Floor 4: Quality Control Egg Nest 2": {"item": "EggNest"},
		}
	},
	"GI Floor 4: Quality Control 1 Egg Nest": {
		"locations": {
			"GI Floor 4: Quality Control Egg Nest 3": {"item": "EggNest"},
		}
	},
	"GI Floor 4: Quality Control 3 Egg Nests": {
		"exits": {
			"GI Floor 4: Quality Control 1 Egg Nest": {},
			"GI Floor 4: Quality Control 2 Egg Nests": {},
		}
	},
	"GI Floor 4: Quality Control Back": {
		"id": 0x010D,
		"locations": {
			"GI Floor 4: Quality Control Jiggy": {"item": "Jiggy"},
		},
		"exits": {
			"GI Floor 4: Quality Control Pit": {
				"logic": {
					"Banjo": """
						EasyJumps and (
							SackPackAirJump and GripGrab
							or PackWhackJump and TallJump
						)
					""",
					"Kazooie": "TallJump or LegSpring",
				}
			},
		}
	},
	"GI Floor 4: Sewer Entrance": {
		"id": 0x0187,
		"locations": {
			"GI Floor 4: Clinker's Cavern Jiggy": {
				"item": "Jiggy",
				"logic": "GIFloor4ClearedClinkersCavern",
			},
			"GI Floor 4: Sewer Entrance Left Egg Nest 1": {"item": "EggNest"},
			"GI Floor 4: Sewer Entrance Left Egg Nest 2": {"item": "EggNest"},
			"GI Floor 4: Sewer Entrance Right Egg Nest 1": {"item": "EggNest"},
			"GI Floor 4: Sewer Entrance Right Egg Nest 2": {"item": "EggNest"},
		},
		"exits": {
			"GI Floor 4: Clinkers Cavern": {
				"id": 0x01,
				"logic": {"Banjo-Kazooie": "BreegullBlaster"},
			},
		}
	},
	"GI Floor 4: Clinkers Cavern": {
		"id": 0x0162,
		"locations": {
			"GI Floor 4: Cleared Clinker's Cavern": {"logic": "exclude(AnyEggs, ClockworkKazooieEggs)"},
			"GI Floor 4: Clinker's Cavern Mumbo Token": {
				"item": {"MumboToken":"'Clinker\\'s Cavern' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Clinker\\'s Cavern' in VictoryGoals",
				"locked": "true",
				"logic": "GIFloor4ClearedClinkersCavern",
			},
			"GI Floor 4: Clinker's Cavern Green Room Egg Nest 1": {"item": "EggNest"},
			"GI Floor 4: Clinker's Cavern Green Room Egg Nest 2": {"item": "EggNest"},
			"GI Floor 4: Clinker's Cavern Raising Scaffolding Room Bottom Egg Nest": {"item": "EggNest"},
			"GI Floor 4: Clinker's Cavern Valve Room Egg Nest": {"item": "EggNest"},
			"GI Floor 4: Clinker's Cavern Near Window Egg Nest": {"item": "EggNest"},
			"GI Floor 4: Clinker's Cavern Raising Scaffolding Room Top Egg Nest": {"item": "EggNest"},
			"GI Floor 4: Clinker's Cavern Orange Room Egg Nest": {"item": "EggNest"},
			"GI Floor 4: Clinker's Cavern Spiral Scaffolding Room Egg Nest": {"item": "EggNest"},
		},
		"exits": {
			"GI Floor 4: Sewer Entrance": {"id": 0x02},
		}
	},
	"GI Floor 4: Opened Elevator Door": {"macro": {"event"}},
}
