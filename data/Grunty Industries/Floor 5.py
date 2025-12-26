from .. import Regions
default_id = 0x010E
instant_transform = {"Mumbo", "Washer"}
regions: Regions = {
	"GI Floor 5: Storage Area 1 Catwalk": {
		"exits": {
			"GI Outside: Upper Roof Side Window": {"id": 0x0B},
			"GI Floor 5: Storage Area 1 Nest Box Tower": {},
			"GI Floor 5: Storage Area 1 Jiggy Box Tower": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							TalonTrot and TalonTrotSlideJump and Flutter and BeakBusterJump
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and TalonTrotSlideJump and Flutter and BeakBusterJump"},
					"Banjo": """
						EasyJumps and (
							PackWhackJump and (TallJump or SackPackAirJump)
						)
					""",
					"Kazooie": """
						Glide
						or TallJump
						or EasyJumps and WingWhack
					""",
				},
			},
		}
	},
	"GI Floor 5: Storage Area 1 Nest Box Tower": {
		"locations": {
			"GI Floor 5: Big Box Stack Egg Nest": {"item": "EggNest"},
		},
		"exits": {
			"GI Floor 5: Storage Area 1 Catwalk": {
				"logic": {
					"Banjo-Kazooie": "FlapFlip and (GripGrab or BeakBusterJump)",
					"Banjo": """
						EasyJumps and (
							PackWhackJump and TallJump and GripGrab
						)
					""",
					"Kazooie": "LegSpring",
				},
			},
			"GI Floor 5: Storage Area 1 Near Ladder": {},
			"GI Floor 5: Storage Area 1 Middle Box Row": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							TallJump
							or TalonTrot
							or FlapFlipSlideExtension
							or Flutter
							or AirRatatatRap
							or RollJump and BeakBusterJump
						)
					""",
					"Talon Trot": "EasyJumps",
					"Banjo": """
						EasyJumps and (
							TallJump
							or PackWhackJump
						)
					""",
					"Kazooie": "",
				},
			},
			"GI Floor 5: Storage Area 1 Jiggy Box Tower": {
				"logic": {
					"Banjo": """
						EasyJumps and (
							SackPackAirJump and PackWhackJump
						)
					""",
					"Kazooie": "EasyJumps and (Glide or WingWhack)",
				}
			}
		}
	},
	"GI Floor 5: Storage Area 1 Jiggy Box Tower": {
		"locations": {
			"GI Floor 5: Jiggy": {"item": "Jiggy"},
		},
		"exits": {
			"GI Floor 5: Storage Area 1 Middle Box Row": {},
		}
	},
	"GI Floor 5: Storage Area 1 Near Ladder": {
		"locations": {
			"GI Floor 5: Box Egg Nest": {"item": "EggNest"},
		},
		"exits": {
			"GI Floor 5: Storage Area 1 Catwalk": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
					"Kazooie": "TallJump or FreeShockSpringPad",
				},
			},
			"GI Floor 5: Storage Area 1 Nest Box Tower": {
				"logic": {
					"Banjo-Kazooie": """
						(TallJump or FreeShockSpringPad) and (
							Climb
							or GripGrab and (
								TallJump
								or EasyJumps and TalonTrot and Flutter
								or WonderwingJump
							)
							or FlapFlip
						)
					""",
					"Banjo": """
						EasyJumps and (
							PackWhackJump and TallJump and GripGrab
						)
					""",
					"Kazooie": "EasyJumps and LegSpring",
				},
			},
			"GI Floor 5: Storage Area 1 Middle Box Row": {
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
					"Kazooie": "TallJump or LegSpring",
				},
			},
			"GI: Service Elevator": {"logic": {"Washer"}},
			"GI Floor 5: Storage Area 2": {"logic": {"Washer"}},
		}
	},
	"GI Floor 5: Storage Area 1 Opposite Ladder": {
		"locations": {
			"GI Floor 5: Small Box Stack Egg Nest": {
				"item": "EggNest",
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or WonderwingJump
						or DamageBoostJump
						or AirRatatatRapClip
						or EasyJumps and (
							Flutter
							or AirRatatatRap
							or BeakBusterJump
						)
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": "TallJump or LegSpring",
				}
			},
		},
		"exits": {
			"GI Floor 5: Storage Area 1 Middle Box Row": {
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
					"Kazooie": "TallJump or LegSpring",
				},
			},
		}
	},
	"GI Floor 5: Storage Area 1 Near Floor Exit": {
		"locations": {
			"GI Floor 5: Unscrewed Plate": {"logic": {"Banjo-Kazooie": "BillDrill"}},
		},
		"exits": {
			"GI Floor 4: Before Crushers Catwalk": {
				"id": 0x03,
				"logic": "GIFloor5UnscrewedPlate"
			},
			"GI Floor 5: Storage Area 1 Middle Box Row": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or TalonTrot
						or FlapFlip
						or BeakBusterJump
						or WonderwingJump
						or DamageBoostJump and ThirdPersonEggShooting and GrenadeEggs
					""",
					"Talon Trot": "",
					"Banjo": "",
					"Kazooie": "TallJump or LegSpring",
				},
			},
		}
	},
	"GI Floor 5: Storage Area 1 Middle Box Row": {
		"exits": {
			"GI Floor 5: Storage Area 1 Near Ladder": {},
			"GI Floor 5: Storage Area 1 Opposite Ladder": {},
			"GI Floor 5: Storage Area 1 Near Floor Exit": {},
		}
	},
	"GI Floor 5: Storage Area 2 Top Of Boxes Near Exit": {
		"exits": {
			"GI Outside: Upper Roof": {
				"id": 0x0A,
				"explicit_logic": {
					"Kazooie": "TallJump or LegSpring",
				}
			},
			"GI Floor 5: Storage Area 2 Top Of H-Beam": {
				"logic": {
					"Banjo-Kazooie": """
						GripGrab and (Flutter or AirRatatatRap) and (
							TallJump
							or FlapFlip
							or RollJump
							or WonderwingJump
							or SlideJump
						)
					""",
					"Banjo": """
						EasyJumps and (
							GripGrab and PackWhackJump
						)
					""",
					"Kazooie": "EasyJumps and Glide",
				},
			},
			"GI Floor 5: Storage Area 2 Top Of Boxes Near Pipe": {
				"logic": {
					"Banjo-Kazooie": """
						GripGrab and (
							TallJump
							or FlapFlip
							or Flutter
							or AirRatatatRap
							or RollJump
							or WonderwingJump
							or SlideJump
						)
						or BeakBusterJump and (
							TallJump and (Flutter or AirRatatatRap)
							or FlapFlip and Flutter
							or FlapFlipSlideExtension and (
								Roll and AirRatatatRap
								or DamageBoostJump
							)
						)
						or Roll and FlapFlipSlideExtension and DamageBoostJump
					""",
					"Banjo": """
						GripGrab and EasyJumps
						or PackWhackJump and TallJump
						or SackPackAirJump
					""",
					"Kazooie": "Glide or EasyJumps",
				},
			},
			"GI Floor 5: Storage Area 2": {},
		}
	},
	"GI Floor 5: Storage Area 2 Top Of Boxes Near Ladder": {
		"exits": {
			"GI Floor 5: Storage Area 2 Top Of Boxes Near Exit": {
				"logic": {
					"Banjo-Kazooie": """
						( # ascent after gap
							FlapFlip
							or GripGrab and (
								TallJump
								or TalonTrot and Flutter
							)
						) and ( # gap
							EasyJumps and (
								Flutter and (
									FlapFlip
									or TallJump
									or TalonTrot
									or BeakBusterJump
									or (RollJump or SlideJump) and GripGrab
								)
								or AirRatatatRap and (
									TallJump and (
										GripGrab
										or BeakBusterJump
										or RollJump
										or SlideJump
									)
									or TalonTrot
								)
							)
							or HardJumps and (
								AirRatatatRap and (
									TallJump
									or RollJump and BeakBusterJump
								)
							)
						)
					""",
					"Banjo": "EasyJumps and SackPackAirJump",
					"Kazooie": "EasyJumps and LegSpring",
				},
			},
			"GI Floor 5: Storage Area 2 Top Of H-Beam": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip
						or GripGrab and (
							TallJump
							or EasyJumps and TalonTrot and Flutter
							or WonderwingJump
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and Flutter and GripGrab"},
					"Banjo": """
						GripGrab
						or PackWhackJump and TallJump
						or SackPackAirJump
					""",
					"Kazooie": "LegSpring",
				},
			},
			"GI Floor 5: Storage Area 2 Top Of Boxes Near Pipe": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							(Flutter or AirRatatatRap) and (
								BeakBusterJump and (TallJump or TalonTrot)
								or GripGrab and (
									TallJump and RollJump
									or TalonTrot
								)
							)
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and (Flutter or AirRatatatRap) and (BeakBusterJump or GripGrab)"},
					"Kazooie": """
						Glide
						or EasyJumps and (TallJump or WingWhack)
					""",
				},
			},
			"GI Floor 5: Storage Area 2": {},
			"GI Floor 5: Storage Area 2 Jinjo Box": {"logic": "EasyJumps"},
		}
	},
	"GI Floor 5: Storage Area 2 Top Of H-Beam": {
		"exits": {
			"GI Floor 5: Storage Area 2 Top Of Boxes Near Exit": {
				"logic": {
					"Banjo-Kazooie": "EasyJumps and GripGrab and Flutter",
				},
			},
			"GI Floor 5: Storage Area 2 Top Of Boxes Near Ladder": {},
			"GI Floor 5: Storage Area 2 Top Of Boxes Near Pipe": {},
		}
	},
	"GI Floor 5: Storage Area 2 Top Of Boxes Near Pipe": {
		"exits": {
			"GI Floor 5: Storage Area 2 Top Of Boxes Near Exit": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and (
							GripGrab
							or EasyJumps and (
								(TallJump or TalonTrot) and (Flutter or AirRatatatRap)
								or FlapFlipSlideExtension and (
									Flutter
									or AirRatatatRap and BeakBusterJump
								)
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
					"Kazooie": "Glide or EasyJumps",
				},
			},
			"GI Floor 5: Storage Area 2 Top Of Boxes Near Ladder": {
				"logic": {
					"Banjo-Kazooie": """
						EasyJumps and (
							(Flutter or AirRatatatRap) and (
								BeakBusterJump and (TallJump or TalonTrot)
								or GripGrab and (
									TallJump and RollJump
									or TalonTrot
								)
							)
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and (Flutter or AirRatatatRap) and (BeakBusterJump or GripGrab)"},
					"Kazooie": """
						Glide
						or EasyJumps and (TallJump or WingWhack)
					""",
				},
			},
			"GI Floor 5: Storage Area 2 Top Of H-Beam": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip
						or GripGrab and (
							TallJump
							or EasyJumps and TalonTrot and Flutter
							or WonderwingJump
						)
					""",
					"Talon Trot": {"Banjo-Kazooie": "EasyJumps and Flutter and GripGrab"},
					"Banjo": """
						GripGrab
						or PackWhackJump and TallJump
						or SackPackAirJump
					""",
					"Kazooie": "LegSpring",
				},
			},
			"GI Floor 5: Storage Area 2": {
				"logic": {
					"Banjo-Kazooie": """
						FallDamage # 1 damage
						or EasyJumps
						or Flutter
						or AirRatatatRap
						or BeakBusterFall
						or WonderwingFall
						or BreegullBashFall
						or GroundRatatatRapFall
					""",
					"Banjo": """
						FallDamage # 1 damage
						or EasyJumps
						or PackWhackFall
						or SackPackFall
						or ShackPackFall
						or SnoozePackFall
						or TaxiPackFall
					""",
					"Kazooie": "",
				},
			},
			"GI Floor 5: Storage Area 2 Jinjo Box": {"logic": "EasyJumps"},
		}
	},
	"GI Floor 5: Storage Area 2": {
		"exits": {
			"GI Floor 5: Storage Area 2 Top Of Boxes Near Exit": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump and (
							GripGrab
							or BeakBusterJump and FlapFlip
						)
					""",
					"Banjo": """
						EasyJumps and (
							SackPackAirJump and PackWhackJump and TallJump and GripGrab
						)
					""",
					"Kazooie": """
						TallJump and LegSpring
						or EasyJumps and LegSpring
					""",
				},
			},
			"GI Floor 5: Storage Area 2 Top Of H-Beam": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
				},
			},
			"GI Floor 5: Storage Area 2 Jinjo Box": {
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
			"GI Floor 5: Skivvy": {"logic": {"Washer"}},
		}
	},
	"GI Floor 5: Storage Area 2 Jinjo Box": {
		"locations": {
			"GI Floor 5: Jinjo": {"item": "BlackJinjo"},
		}
	},
}
