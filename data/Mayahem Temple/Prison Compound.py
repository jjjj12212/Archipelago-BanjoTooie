from .. import Regions
instant_transform = {"Mumbo", "Stony"}
regions: Regions = {
	"MT: Prison Compound": {
		"locations": {
			"MT: Prison Compound Entrance Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Prison Compound Entrance Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Prison Compound Quicksand Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"MT: Prison Compound Warp Pad Tagged": {
				"item": "MTPrisonCompoundWarpPad",
			},
		},
		"exits": {
			"MT: Main Map": {},
			"MT: Warp Pads": {
				"logic": "MTPrisonCompoundWarpPad"
			},
			"MT: Prison Compound Underwater": {
				"logic": {
					"Banjo-Kazooie": "Dive or DiveSkip and BeakBuster",
					"Stony": "true"
				}
			},
			"MT: Prison Compound Moon Switch Pressed": {},
			"MT: Prison Compound Star Switch Pressed": {},
			"MT: Prison Compound Sun Switch Pressed": {},
			"MT: Prison Compound Cell Opened": {
				"logic": """
					MTPrisonCompoundMoonSwitchPressed
					and MTPrisonCompoundStarSwitchPressed
					and MTPrisonCompoundSunSwitchPressed
				"""
			},
			"MT: Prison Compound Top of Jail Cell": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie":"FlapFlip or TallJump and GripGrab or TalonTrot and Flutter and GripGrab",
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
			"MT: Prison Compound Cheato Page Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			},
			"MT: Prison Compound Inside Jail Cell": {
				"logic": "MTPrisonCompoundCellOpened"
			}
		}
	},
	"MT: Prison Compound Top of Jail Cell": {
		"locations": {
			"MT: Prison Compound Top of Prison Cell Feather Right Nest": {
				"item": "FeatherNest",
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
			"MT: Prison Compound Top of Prison Cell Feather Left Nest": {
				"item": "FeatherNest",
				"logic": {
					"Banjo-Kazooie": "true",
					"Clockwork Kazooie": "TallJump"
				}
			},
		},
		"exits": {
			"MT: Prison Compound Swamp Jiggy Platform": {
				"logic": {
					"Banjo-Kazooie": "StiltStride and GripGrab and (FlapFlip or TallJump or TalonTrot and Flutter)"
				}
			},
			"MT: Prison Compound Cheato Page Platform": {
				"logic": {
					"Banjo-Kazooie": "GripGrab and (FlapFlip or TallJump or TalonTrot and Flutter)"
				}
			},
		}
	},
	"MT: Prison Compound Underwater": {
		"exits": {
			"MT: Prison Compound Pillar Area": {}
		}
	},
	"MT: Prison Compound Cheato Page Platform": {
		"locations": {
			"MT: Prison Compound Cheato Page": {
				"item": "CheatoPage",
                "explicit_logic": {"Clockwork Kazooie": "true"}
			},
		},
		"exits": {
			"MT: Prison Compound Pillar Area": {}
		}
	},
	"MT: Prison Compound Swamp Jiggy Platform": {
		"locations": {
			"MT: Prison Compound Quicksand Jiggy": {
				"item": "Jiggy",
			},
		}
	},
	"MT: Prison Compound Pillar Area": {
		"locations": {
			"MT: Pillars Jiggy": {
				"logic": """
					MTPillarJiggyLowered and (TallJump or TalonTrot or FlapFlip or WonderwingJump)
					or HardJumps and TalonTrot and Flutter and BeakBuster
					or ClockworkShot
				""",
				"item": "Jiggy",
			},
			"MT: Prison Compound Pillars Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Prison Compound Pillars Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Prison Compound Pillars Egg Nest 3": {
				"item": "EggNest",
			},
			"MT: Pillars Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		},
		"exits": {
			"MT: Column Vaults": {
				"logic": {
					"Banjo-Kazooie": "BillDrill"
				}
			}
		}
	},
	"MT: Column Vaults": {
		"exits": {
			"MT: Prison Compound": {},
			"MT: Pillar Jiggy Lowered": {
				"logic": "AnyAttack"
			}
		}
	},
	"MT: Pillar Jiggy Lowered": {"macro": {"event"}},
	"MT: Prison Compound Sun Switch Pressed": {"macro": {"event"}},
	"MT: Prison Compound Star Switch Pressed": {"macro": {"event"}},
	"MT: Prison Compound Moon Switch Pressed": {"macro": {"event"}},
	"MT: Prison Compound Cell Opened": {"macro": {"event"}},
	"MT: Prison Compound Inside Jail Cell": {
		"exits": {
			"MT: Prison Compound Behind Jail Cell Boulder": {
				"logic": "MTPrisonCompoundJailCellBoulderBroken"
			},
			"MT: Prison Compound Jail Cell Boulder Broken": {
				"logic": {
					"Banjo-Kazooie": "BillDrill"
				}
			}
		}
	},
	"MT: Prison Compound Jail Cell Boulder Broken": {"macro": {"event"}},
	"MT: Prison Compound Behind Jail Cell Boulder": {
		# Transition to GGM
	},
}
