from .. import Regions
instant_transform = {"Mumbo", "Washer"}
regions: Regions = {
	"GI: Boss Room": {
		"instant_transform": set(),
		"exits": {
			"GI Basement: Repair Depot": {"logic": "GrenadeEggs"},
			"GI Basement: AC Plant Near Repair Depot": {
				"id": 0x03,
				"groups": {"Boss Exits"},
			}
		}
	},
	"GI Basement: Repair Depot": {
		"id": 0x0110,
		"instant_transform": set(),
		"locations": {
			"GI: Defeated Weldar": {
				"logic": {
					"Banjo-Kazooie": """
						EggUse and (FireEggs or GrenadeEggs)
						or DragonBreath
					""",
				},
			},
			"GI Floor 1: Repair Depot Cheato Page": {
				"item": "CheatoPage",
				"logic": "GIDefeatedWeldar",
			},
			"GI Floor 1: Weldar Mumbo Token": {
				"item": {"MumboToken":"'Weldar' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Weldar' in VictoryGoals",
				"locked": "true",
				"logic": "GIDefeatedWeldar",
			},
			"GI Floor 1: Repair Depot Egg Nest 1": {"item": "EggNest"},
			"GI Floor 1: Repair Depot Egg Nest 2": {"item": "EggNest"},
		},
	},
	"GI Basement: AC Plant": {
		"id": 0x010F,
		"locations": {
			"GI Floor 1: Air Conditioning Plant Note 1": {"item": "NoteNest"},
			"GI Floor 1: Air Conditioning Plant Note 2": {"item": "NoteNest"},
		},
		"exits": {
			"GI Floor 1": {"id": 0x08},
			"GI Basement: AC Plant Near Repair Depot": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and Climb and (
							GripGrab
							or EasyJumps and (
								TallJump and AirRatatatRap
								or Flutter
							)
							or HardJumps and (
								TallJump
								or AirRatatatRap
								or RollJump and (
									FlapFlipSlideExtension
									or BeakBusterJump
								)
							)
							or HardTediousJumps and TalonTrot # 2 frame perfect inputs
						)
					""",
					"Banjo": "PackWhackJump and TallJump and Climb",
				},
			},
			"GI Basement: AC Plant Big Fan Room": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
				},
			},
		}
	},
	"GI Basement: AC Plant Near Repair Depot": {
		"id": 0x010F,
		"locations": {
			"GI Floor 1: Air Conditioning Plant Near Repair Depot Egg Nest 1": {"item": "EggNest"},
			"GI Floor 1: Air Conditioning Plant Near Repair Depot Egg Nest 2": {"item": "EggNest"},
		},
		"exits": {
			"GI: Boss Room": {
				"id": 0x01,
				"groups": {"Boss Entrances"},
				"logic": {"Banjo-Kazooie": "GIFloor2OpenedRepairDepot"},
			},
			"GI Basement: AC Plant": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or Flutter
						or AirRatatatRap
						or EasyJumps and (
							FlapFlip
							or RollJump
							or WonderwingJump
							or BeakBusterJump and (
								BeakBargeJump
								or GroundRatatatRapJump
								or SlideJump
							)
						)
					""",
					"Talon Trot": "",
					"Banjo": """
						TallJump
						or PackWhackJump
						or SackPackAirJump
					""",
				},
			},
			"GI Basement: AC Plant Top Of Big Fan": {"logic": "GIDefeatedWeldar"},
		}
	},
	"GI Basement: AC Plant Top Of Big Fan": {
		"id": 0x010F,
		"locations": {
			"GI Floor 1: Weldar Jiggy": {
				"item": "Jiggy",
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or Flutter
						or AirRatatatRap
						or BeakBusterJump
						or WonderwingJump
					""",
					"Talon Trot": "",
					"Banjo": "",
				},
			},
		},
		"exits": {
			"GI Basement: AC Plant Near Repair Depot": {"logic": "GIDefeatedWeldar"},
			"GI Basement: AC Plant Big Fan Room": {
				"logic": {
					"Banjo-Kazooie": """
						Flutter
						or AirRatatatRap
						or BeakBusterFall
						or WonderwingFall
						or BreegullBashFall
						or GroundRatatatRapFall
						or FallDamage # 1 damage
					""",
					"Banjo": """
						FallDamage # 1 damage
						or PackWhackFall
						or TaxiPackFall
						or SackPackFall
						or ShackPackFall
						or SnoozePackFall
					""",
				},
			},
		}
	},
	"GI Basement: AC Plant Big Fan Room": {
		"id": 0x010F,
		"locations": {
			"GI Floor 1: Air Conditioning Plant In Front of Fan Feather Nest 1": {"item": "FeatherNest"},
			"GI Floor 1: Air Conditioning Plant In Front of Fan Feather Nest 2": {"item": "FeatherNest"},
			"GI Floor 1: Air Conditioning Plant Near Waste Disposal Egg Nest": {
				"item": "EggNest",
				"logic": "GIDefeatedWeldar",
				"explicit_logic": {
					"Banjo-Kazooie": """
						GIDefeatedWeldar
						or TalonTrot and BreegullBashGrab
					""",
					"Talon Trot": "BreegullBashGrab",
				}
			},
		},
		"exits": {
			"GI Basement: Waste Disposal Plant From AC Plant": {
				"id": 0x02,
				"logic": "GIDefeatedWeldar",
			},
			"GI Basement: AC Plant": {},
		}
	},
	"GI Basement: Waste Disposal Plant From AC Plant": {
		"id": 0x0111,
		"macro": {"splitup"},
		"exits": {
			"GI Basement: AC Plant Big Fan Room": {"id": 0x02},
			"GI Basement: Waste Disposal Plant Underwater": {
				"logic": {
					"Banjo": "ShackPack",
				},
			}
		}
	},
	"GI Basement: Waste Disposal Plant Underwater": {
		"locations": {
			"GI Floor 1: Underwater Waste Disposal Plant Jiggy": {"item": "Jiggy"},
		}
	},
	"GI Basement: Waste Disposal Plant Upper": {
		"id": 0x0111,
		"locations": {
			"GI Floor 1: Snooze Pack Silo": {
				"item": "SnoozePack",
				"logic": {"Banjo": "Notes >= ChosenMoveSiloCosts['Snooze Pack']"}
			},
		},
		"exits": {
			"GI Floor 1: Top Of Waste Disposal Plant": {"id": 0x09},
			"GI Basement: Waste Disposal Plant Lower": {},
			"GI Basement: Waste Disposal Plant One Way Exit": {
				"logic": {
					"Kazooie": "EasyJumps and LegSpring and Glide",
				}
			}
		}
	},
	"GI Basement: Waste Disposal Plant Lower": {
		"id": 0x0111,
		"macro": {"splitup"},
		"locations": {
			"GI Floor 1: Waste Disposal Plant Note 1": {"item": "NoteNest"},
			"GI Floor 1: Waste Disposal Plant Note 2": {"item": "NoteNest"},
		},
		"exits": {
			"GI Basement: Waste Disposal Plant Lower": {
				"logic": {
					"Banjo-Kazooie": {"BK Springy Step Shoes": "SpringyStepShoes"},
					"Kazooie": {"SK Springy Step Shoes": "SpringyStepShoes"}
				},
			},
			"GI Basement: Waste Disposal Plant Upper": {
				"logic": {
					"Banjo-Kazooie": """
						Climb and (
							TallJump
							or TalonTrot
							or FlapFlip
							or WonderwingJump
							or EasyJumps and (
								(Flutter or AirRatatatRap) and BeakBusterJump
								or BillDrillJump
							)
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "Climb"},
					"Banjo": "Climb",
					"BK Springy Step Shoes": """
						Climb
						or TallJump
						or TalonTrot
						or FlapFlip
						or Flutter and GripGrab
						or WonderwingJump
					""",
					"SK Springy Step Shoes": "",
				},
			},
			"GI Basement: Waste Disposal Plant Across Toxic Water": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							Climb
							or TallJump
							or GripGrab
							or BeakBusterJump
						)
					""",
					"Banjo": """
						SackPack
						or EasyJumps and (
							Climb
							or TallJump
							or GripGrab
							or PackWhackJump
						)
					""",
				},
			},
			"GI Basement: Waste Disposal Plant One Way Exit": {
				"logic": {
					"SK Springy Step Shoes": "Glide",
				}
			}
		}
	},
	"GI Basement: Waste Disposal Plant Across Toxic Water": {
		"id": 0x0111,
		"locations": {
			"GI Floor 1: Waste Disposal Plant Box Jiggy": {
				"item": "Jiggy",
				"logic": {"Banjo-Kazooie", "Banjo"},
			},
		},
		"exits": {
			"GI Basement: Waste Disposal Plant One Way Exit": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
				},
			},
		}
	},
	"GI Basement: Waste Disposal Plant One Way Exit": {
		"exits": {
			"GI Floor 1: Ducts Near Waste Disposal Plant": {"id": 0x0D},
			"GI Basement: Waste Disposal Plant Across Toxic Water": {
				"logic": {
					"Banjo-Kazooie": """
						Flutter
						or AirRatatatRap
						or BeakBusterFall
						or WonderwingFall
						or BreegullBashFall
						or GroundRatatatRapFall
						or FallDamage # 1 damage
					""",
					"Banjo": """
						FallDamage # 1 damage
						or PackWhackFall
						or TaxiPackFall
						or SackPackFall
						or ShackPackFall
						or SnoozePackFall
					""",
					"Kazooie": "",
				}
			},
		}
	},
	"GI Basement: Waste Disposal Plant Jinjo Tank": {
		"id": 0x0111,
		"locations": {
			"GI Floor 1: Waste Disposal Plant Jinjo": {"item": "BlackJinjo"},
			"GI Floor 1: Waste Disposal Jinjo Tank Egg Nest 1": {"item": "EggNest"},
			"GI Floor 1: Waste Disposal Jinjo Tank Egg Nest 2": {"item": "EggNest"},
		}
	},
	"GI Basement: Waste Disposal Plant Top Of Pump": {
		"id": 0x0111,
		"locations": {
			"GI Floor 1: Waste Disposal Water Pump Egg Nest": {"item": "EggNest"},
			"GI Floor 1: Waste Disposal Water Pump Feather Nest": {"item": "FeatherNest"},
		}
	}
}
