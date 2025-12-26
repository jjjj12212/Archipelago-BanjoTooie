from .. import Regions
default_id = 0x0106
instant_transform = {"Mumbo", "Washer"}
regions: Regions = {
	"GI Floor 2: Near Service Elevator": {
		"locations": {
			"GI Floor 2: Near Floor 1 Tunnel Egg Nest": {"item": "EggNest"},
		},
		"exits": {
			"GI Floor 1: Lower Catwalk": {
				"id": 0x0A,
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and (GripGrab or BeakBusterJump)
						or HardJumps and (
							(Flutter or AirRatatatRap) and BeakBusterJump and (
								TalonTrot
								or RollJump and TallJump
							)
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "HardJumps and (Flutter or AirRatatatRap) and BeakBusterJump"},
					"Banjo": """
						EasyJumps and (
							PackWhackJump and (TallJump or SackPackAirJump)
							or SackPackEndingJump
						)
					""",
					"Kazooie": """
						LegSpring
						or EasyJumps and TallJump
					""",
				}
			},
			"GI Floor 2: Near Wumba's Wigwam": {},
			"GI: Service Elevator": {"logic": {"Washer"}},
		},
	},
	"GI Floor 2: Near Wumba's Wigwam": {
		"locations": {
			"GI Floor 2: Glowbo": {"item": "HumbaWashingMachine"},
			"GI Floor 2: Outside Wumba's Wigwam Warp Pad Tagged": {"item": "GIFloor2OutsideWumbasWigwamWarpPad"},
		},
		"exits": {
			"GI Floor 2: Near Service Elevator": {},
			"GI Floor 2: Near Tintops": {},
			"GI Floor 2: Wumba's Wigwam": {"id": 0x01},
			"GI: Warp Pads": {"logic": "GIFloor2OutsideWumbasWigwamWarpPad"},
			"GI Floor 2: Broke Grate Near Humba": {
				"logic": {
					"Banjo-Kazooie": "EggUse and (GrenadeEggs or ExtraClockworkUsage)",
					"Kazooie": "EggUse and (GrenadeEggs or ExtraClockworkUsage)",
					"Mumbo": "",
				},
			},
			"GI Floor 2: Behind Grate Near Humba": {"logic": "GIFloor2BrokeGrateNearHumba"},
		},
	},
	"GI Floor 2: Near Tintops": {
		"locations": {
			"GI Floor 2: Box Room Taller Stack Note": {
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
					"Kazooie": "TallJump or LegSpring or DamageBoostJump",
				}
			},
			"GI Floor 2: Box Room Shorter Stack Note": {"item": "NoteNest"},
			"GI Floor 2: In a Box Egg Nest 1": {
				"item": "EggNest",
				"logic": {
					"Banjo-Kazooie": "AnyAttack or EggUse and AnyEggs",
					"Banjo": "PackWhack",
					"Kazooie": "WingWhack or EggUse and AnyEggs",
				},
			},
			"GI Floor 2: In a Box Egg Nest 2": {
				"item": "EggNest",
				"logic": {
					"Banjo-Kazooie": "AnyAttack or EggUse and AnyEggs",
					"Banjo": "PackWhack",
					"Kazooie": "WingWhack or EggUse and AnyEggs",
				},
			},
		},
		"exits": {
			"GI Floor 2: Floor 1 Stairway": {
				"logic": {
					"Banjo-Kazooie": "AnyAttack or EggUse and AnyEggs",
					"Talon Trot": "EggAim and AnyEggs",
					"Banjo": "PackWhack",
					"Kazooie": "WingWhack or EggUse and AnyEggs",
					"Mumbo": "",
					"Washer": "",
				},
			},
			"GI Floor 2: Near Wumba's Wigwam": {},
			"GI Floor 2: Near Floor 3 Exit": {},
			"GI Floor 2: Toxic Waste Room": {},
			"GI Floor 2: Near Tintops": {
				"logic": {
					"Banjo-Kazooie": {"BK Claw Clamber Boots": "AnyAttack and ClawClamberBoots"},
					"Kazooie": {"SK Claw Clamber Boots": "WingWhack and ClawClamberBoots"},
				},
			},
			"GI Floor 2: Jamjars Platform": {
				"logic": {"BK Claw Clamber Boots", "SK Claw Clamber Boots"},
			}
		},
	},
	"GI Floor 2: Floor 1 Stairway": {
		"exits": {
			"GI Floor 1: Back Door Room": {"id": 0x0B},
			"GI Floor 2: Near Tintops": {
				"logic": {
					"Banjo-Kazooie": "AnyAttack or EggUse and AnyEggs",
					"Talon Trot": "EggAim and AnyEggs",
					"Banjo": "PackWhack",
					"Kazooie": "WingWhack or EggUse and AnyEggs",
					"Mumbo": "",
					"Washer": "",
				},
			},
		}
	},
	"GI Floor 2: Near Floor 3 Exit": {
		"locations": {
			"GI Floor 2: Delivered Battery Near Floor 3 Exit": {
				"logic": {
					"Banjo": """
						PackWhack and TaxiPack
						and can_form_from_region_reach(
							"Banjo",
							"GI Floor 2: Near Floor 3 Exit",
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
			"GI Floor 2: Near Tintops": {},
			"GI Floor 2: Near Floor 3 Exit": {
				"logic": {
					"Banjo-Kazooie": {"BK Claw Clamber Boots": "AnyAttack and ClawClamberBoots"},
					"Kazooie": {"SK Claw Clamber Boots": "WingWhack and ClawClamberBoots"},
				},
			},
			"GI Floor 2: Platform Near Claw Clamber Boots": {
				"logic": {"BK Claw Clamber Boots", "SK Claw Clamber Boots"},
			},
			"GI Floor 2: Catwalk": {"logic": "GIFloor2OpenedCatwalkDoor"},
		},
	},
	"GI Floor 2: Toxic Waste Room": {
		"exits": {
			"GI Floor 2: Near Tintops": {},
			"GI Floor 2: Toxic Waste Tower": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
					"Kazooie": "TallJump",
				},
			},
			"GI Floor 2: Battery Platform": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and GripGrab and (
							EasyJumps
							or DamageBoost
							or WonderwingDamageBoost
							or TallJump
							or TalonTrot
							or Flutter
							or AirRatatatRap
							or BeakBusterJump
							or RollJump
							or SlideJump
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "FlapFlip and GripGrab"},
					"Banjo": """
						EasyJumps and TallJump and (
							PackWhackJump and GripGrab
							or SackPackEndingJump and (GripGrab or PackWhackJump)
						)
					""",
					"Kazooie": "LegSpring",
				},
			},
		},
	},
	"GI Floor 2: Wumba's Wigwam": {
		"id": 0x011F,
		"locations": {
			"GI: Washer Transform": {"logic": {"Banjo-Kazooie": "HumbaWashingMachine"}},
		},
		"exits": {
			"GI Floor 2: Near Wumba's Wigwam": {"id": 0x0A},
			"GI Floor 2: Wumba's Wigwam": {
				"logic": {"Banjo-Kazooie": {"Washer": "GIWasherTransform"}},
			},
		}
	},
	"GI Floor 2: Behind Grate Near Humba": {
		"exits": {
			"GI Floor 2: Behind Grate Near Electromagnet Chamber": {"id": 0x04},
			"GI Floor 2: Near Wumba's Wigwam": {"logic": "GIFloor2BrokeGrateNearHumba"},
			"GI Floor 2: Broke Grate Near Humba": {
				"logic": {
					"Banjo-Kazooie": "EggUse and (GrenadeEggs or ExtraClockworkUsage)",
					"Kazooie": "EggUse and (GrenadeEggs or ExtraClockworkUsage)",
					"Mumbo": "",
				},
			}
		}
	},
	"GI Floor 2: Behind Grate Near Electromagnet Chamber": {
		"exits": {
			"GI Floor 2: Behind Grate Near Humba": {"id": 0x03},
			"GI Floor 2: Broke Grate Near Electromagnet Chamber": {
				"logic": {
					"Banjo-Kazooie": "EggUse and (GrenadeEggs or ExtraClockworkUsage)",
					"Kazooie": "EggUse and (GrenadeEggs or ExtraClockworkUsage)",
					"Mumbo": "",
				},
			},
			"GI Floor 2: Toxic Waste Tower": {"logic": "GIFloor2BrokeGrateNearElectromagnetChamber"},
		},
	},
	"GI Floor 2: Catwalk": {
		"locations": {
			"GI Floor 2: Opened Catwalk Door": {},
		},
		"exits": {
			"GI Floor 2: Near Floor 3 Exit": {},
			"GI Floor 2: Nests Catwalk": {
				"logic": {
					"Banjo-Kazooie": "GripGrab",
					"Banjo": """
						GripGrab
						or EasyJumps and (
							SackPackEndingJump and TallJump and PackWhackJump
						)
					""",
					"Kazooie": """
						Glide
						or EasyJumps and LegSpring and WingWhack
					""",
				},
			},
			"GI Floor 2: Platform Near Floor 3": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and GripGrab
						or EasyJumps and (
							TalonTrot
							or RollJump and TallJump and BeakBusterJump
							or FlapFlip and DamageBoostJump
							or Flutter and (
								GripGrab
								or TallJump
								or FlapFlip
								or BeakBusterJump
							)
							or AirRatatatRap and (
								GripGrab
								or TallJump
								or FlapFlipSlideExtension
								or BeakBusterJump
								or RollJump and FlapFlip
							)
						)
					""",
					"Talon Trot": "EasyJumps",
					"Banjo": """
						GripGrab
						or EasyJumps and (
							PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Floor 2: Platform Near Claw Clamber Boots": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and GripGrab
						or EasyJumps and (
							FlapFlip and BeakBusterJump and DamageBoostJump
							or Flutter and (
								(TallJump or TalonTrot) and (GripGrab or BeakBusterJump)
								or FlapFlip and BeakBusterJump
							)
							or AirRatatatRap and (
								TallJump and (GripGrab or BeakBusterJump)
								or TalonTrot
								or FlapFlipSlideExtension and BeakBusterJump
							)
						)
					""",
					"Talon Trot": {
						"Banjo-Kazooie": """
							EasyJumps and (
								Flutter and (GripGrab or BeakBusterJump)
								or AirRatatatRap
							)
						""",
					},
					"Banjo": """
						EasyJumps and (
							PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Floor 2: Skivvy": {"logic": {"Washer"}},
		}
	},
	"GI Floor 2: Nests Catwalk": {
		"locations": {
			"GI Floor 2: On Scaffolding Egg Nest 1": {"item": "EggNest"},
			"GI Floor 2: On Scaffolding Egg Nest 2": {"item": "EggNest"},
			"GI Floor 2: On Scaffolding Egg Nest 3": {"item": "EggNest"},
			"GI Floor 2: On Scaffolding Egg Nest 4": {"item": "EggNest"},
			"GI Floor 2: On Scaffolding Egg Nest 5": {"item": "EggNest"},
		},
	},
	"GI Floor 2: Platform Near Floor 3": {
		"exits": {
			"GI Floor 3: Floor 2 Platform": {
				"id": 0x01,
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": """
						Climb
						or EasyJumps and (
							SackPackEndingJump and TallJump and PackWhackJump
						)
					""",
					"Kazooie": "LegSpring",
				}
			},
			"GI Floor 2: Near Floor 3 Exit": {},
			"GI Floor 2: Catwalk": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and GripGrab
						or EasyJumps and (
							TalonTrot
							or FlapFlip and BeakBusterJump and DamageBoostJump
							or TallJump and (
								Climb and GripGrab
								or RollJump and BeakBusterJump
							)
							or (Flutter or AirRatatatRap) and (
								TallJump
								or FlapFlip
								or GripGrab
								or BeakBusterJump
							)
						)
					""",
					"Talon Trot": "EasyJumps",
					"Banjo": """
						GripGrab
						or EasyJumps and (
							PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Floor 2: Platform Near Claw Clamber Boots": {
				"logic": {
					"Banjo-Kazooie": "(TallJump or FlapFlip or WonderwingJump) and GripGrab and (Flutter or AirRatatatRap)",
					"Banjo": """
						EasyJumps and PackWhackJump and (
							GripGrab
							or TallJump
							or SackPackAirJump
						)
					""",
				},
			},
		}
	},
	"GI Floor 2: Platform Near Claw Clamber Boots": {
		"exits": {
			"GI Floor 2: Near Floor 3 Exit": {},
			"GI Floor 2: Catwalk": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and GripGrab
						or EasyJumps and (
							DamageBoostJump and (
								FlapFlip and BillDrillJump
								or FlapFlipSlideExtension and BeakBusterJump
							)
							or Flutter and (
								TallJump and (GripGrab or BeakBusterJump)
								or TalonTrot
								or FlapFlip and BeakBusterJump
								or FlapFlipSlideExtension and GripGrab
							)
							or AirRatatatRap and (
								TallJump and (GripGrab or BeakBusterJump)
								or TalonTrot
							)
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and (Flutter or AirRatatatRap)"},
					"Banjo": """
						EasyJumps and (
							PackWhackJump and (TallJump or GripGrab)
							or SackPackAirJump
						)
						or HardJumps and PackWhackJump
					""",
					"Kazooie": "",
				},
			},
			"GI Floor 2: Platform Near Floor 3": {
				"logic": {
					"Banjo-Kazooie": """
						GripGrab and (
							TallJump
							or EasyJumps and (
								FlapFlip
								or TalonTrot and (Flutter or DamageBoostJump)
								or WonderwingJump
							)
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and (Flutter or DamageBoostJump)"},
					"Banjo": """
						TallJump and GripGrab
						or EasyJumps and (
							PackWhackJump and (
								GripGrab
								or TallJump
								or SackPackAirJump
							)
						)
					""",
				},
			},
		}
	},
	"GI Floor 2: Toxic Waste Tower": {
		"macro": {"splitup"},
		"locations": {
			"GI Floor 2: Leg Spring Jinjo": {
				"item": "GreenJinjo",
				"logic": {
					"Kazooie": "LegSpring",
				},
			},
			"GI Floor 2: Leg Spring Room Note 1": {"item": "NoteNest"},
			"GI Floor 2: Leg Spring Room Note 2": {"item": "NoteNest"},
			"GI Floor 2: Leg Spring Room Note 3": {"item": "NoteNest"},
			"GI Floor 2: Opened Electromagnet Chamber": {
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
			"GI Floor 2: Toxic Waste Room": {},
			"GI Floor 2: Behind Grate Near Electromagnet Chamber": {"logic": "GIFloor2BrokeGrateNearElectromagnetChamber"},
			"GI Floor 2: Behind Electromagnet Chamber Door": {"logic": "GIFloor2OpenedElectromagnetChamber"},
			"GI Floor 2: Battery Platform": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and GripGrab
						or EasyJumps and (
							TalonTrot
							or Flutter
							or AirRatatatRap
							or RollJump and TallJump and BeakBusterJump
							or WonderwingJump and GripGrab
							or DamageBoostJump and (
								FlapFlip and (BeakBusterJump or RollJump)
								or FlapFlipSlideExtension
							)
						)
						or HardJumps and (
							RollJump and FlapFlipSlideExtension and BillDrillJump
						)
					""",
					"Talon Trot": "EasyJumps",
					"Banjo": """
						GripGrab
						or EasyJumps and (
							PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "EasyJumps",
				},
			},
			"GI Floor 2: Jamjars Platform": {
				"logic": {
					"Kazooie": """
						Glide
						or EasyJumps and (TallJump or LegSpring)
					""",
				}
			}
		}
	},
	"GI Floor 2: Jamjars Platform": {
		"locations": {
			"GI Floor 2: Leg Spring Silo": {
				"item": "LegSpring",
				"logic": {"Kazooie": "Notes >= ChosenMoveSiloCosts['Leg Spring']"},
			},
		},
		"exits": {
			"GI Floor 2: Toxic Waste Tower": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							(Flutter or AirRatatatRap) and BeakBusterJump and (
								RollJump and TallJump
								or TalonTrot
							)
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and (Flutter or AirRatatatRap) and BeakBusterJump"},
					"Kazooie": "Glide or EasyJumps",
				},
			},
		}
	},
	"GI Floor 2: Battery Platform": {
		"locations": {
			"GI Floor 2: Delivered Toxic Room Battery": {
				"logic": {
					"Banjo": """
						PackWhack and TaxiPack
						and can_form_from_region_reach(
							"Banjo",
							"GI Floor 2: Battery Platform",
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
			"GI Floor 2: Toxic Waste Tower": {
				"logic": {
					"Kazooie": """
						LegSpring and (
							Glide
							or EasyJumps and WingWhack
						)
					""",
				}
			},
			"GI Floor 2: Toxic Waste Room": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps
						or DamageBoost
						or WonderwingDamageBoost
						or TallJump
						or TalonTrot
						or Flutter
						or AirRatatatRap
						or BeakBusterJump
						or RollJump
						or SlideJump
					""",
					"Talon Trot": "",
					"Banjo": "EasyJumps or TallJump",
					"Kazooie": "",
				},
			},
		}
	},
	"GI Floor 2: Behind Electromagnet Chamber Door": {
		"exits": {
			"GI Floor 2: Electromagnet Chamber": {"id": 0x01},
			"GI Floor 2: Toxic Waste Tower": {"logic": "GIFloor2OpenedElectromagnetChamber"},
		}
	},
	"GI Floor 2: Electromagnet Chamber": {
		"id": 0x0107,
		"locations": {
			"GI Floor 2: Electromagnetic Chamber Feather Nest": {"item": "FeatherNest"},
			"GI Floor 2: EMP Electromagnet": {"logic": {"Mumbo": "GIFloor3UnscrewedPlate"}},
			"GI Floor 2: Opened Repair Depot": {"logic": {"Washer": "GIFloor2EMPElectromagnet"}},
		},
		"exits": {
			"GI Floor 2: Behind Electromagnet Chamber Door": {"id": 0x01},
			"GI Floor 2: Opened Elevator Door": {
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
			"GI Floor 2: Electromagnet Chamber Atop Magnet Housing": {
				"logic": {
					"Banjo-Kazooie": """
						TalonTrot
						or Flutter
						or AirRatatatRap
						or EasyJumps and (
							BeakBusterJump and (
								TallJump
								or FlapFlip
							)
							or RollJump and TallJump
						)
						or GIFloor2OpenedRepairDepot and (
							TallJump
							or FlapFlip
							or BeakBusterJump
							or WonderwingJump
						)
					""",
					"Talon Trot": "",
					"Banjo": """
						GIFloor2OpenedRepairDepot
						or EasyJumps and (
							PackWhackJump
							or SackPackAirJump
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Floor 2: Electromagnet Chamber Behind Elevator Door": {"logic": "GIFloor2OpenedElevatorDoor"},
		}
	},
	"GI Floor 2: Electromagnet Chamber Atop Magnet Housing": {
		"id": 0x0107,
		"locations": {
			"GI Floor 2: Electromagnetic Chamber Egg Nest 1": {"item": "EggNest"},
			"GI Floor 2: Electromagnetic Chamber Egg Nest 2": {"item": "EggNest"},
		},
	},
	"GI Floor 2: Electromagnet Chamber Behind Elevator Door": {
		"id": 0x0107,
		"exits": {
			"GI Elevator Shaft: Floor 2": {"id": 0x01},
			"GI Floor 2: Opened Elevator Door": {
				"logic": {
					"Banjo-Kazooie": "BreegullBashClip",
				},
			},
			"GI Floor 2: Electromagnet Chamber": {"logic": "GIFloor2OpenedElevatorDoor"},
		}
	},
	"GI Floor 2: Near Window With Page": {
		"locations": {
			"GI Floor 2: Window Cheato Page": {"item": "CheatoPage"},
			"GI Floor 2: Near Cheato Page Feather Nest": {"item": "FeatherNest"},
		},
		"exits": {
			"GI Outside: Behind Window Above Front Train Tunnel": {"id": 0x06},
		}
	},
	"GI Floor 2: Near Window With Unscrewable Plate": {
		"locations": {
			"GI Floor 2: Unscrewed Plate": {"logic": {"Banjo-Kazooie": "BillDrill"}},
			"GI Floor 2: Near Unscrewable Platform Feather Nest": {"item": "FeatherNest"},
		},
		"exits": {
			"GI Outside: Behind Window Near Back Train Tunnel": {"id": 0x05},
		}
	},
	"GI Floor 2: Broke Grate Near Humba": {"macro": {"event"}},
	"GI Floor 2: Broke Grate Near Electromagnet Chamber": {"macro": {"event"}},
	"GI Floor 2: Opened Elevator Door": {"macro": {"event"}},
}
