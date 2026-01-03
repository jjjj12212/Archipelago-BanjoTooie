from .. import Regions
regions: Regions = {
	"IoH: Quagmire": {
		"id": 0x015C,
		"locations": {
			"IoH: Quagmire Left Feather Nest": {
				"item": "FeatherNest",
				"logic": {
					"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or ClockworkShot or BeakBusterJump or AirRatATatGrab",
					"Talon Trot": "true"
				}
			},
			"IoH: Quagmire Back Feather Nest": {
				"item": "FeatherNest",
			},
			"IoH: Quagmire High Feather Nest": {
				"item": "FeatherNest",
				"logic": {
					"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or ClockworkShot or BeakBusterJump",
					"Talon Trot": "true"
				}
			},
			"IoH: Quagmire Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Quagmire Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Quagmire Egg Nest 3": {
				"item": "EggNest",
			},
			"IoH: Quagmire Silo Tagged": {
				"item": "QuagmireWarpSilo",
				"logic": {
					"Banjo-Kazooie": "true"
				}
			},
		},
		"exits": {
			"IoH: Quagmire on Ledge to Wasteland": {
				"logic": {
					"Banjo-Kazooie": "FlapFlip and GripGrab or FlapFlip and BeakBusterJump"
				}
			},
			"IoH: Quagmire Behind GI Door": {
				"logic": "GruntyIndustries",
			},
			"IoH: Quagmire": {
				"logic": {
					"Banjo-Kazooie": {
						"BK Claw Clamber Boots": "ClawClamberBoots"
					}
				}
			},
			"IoH: Quagmire On Pole": {
				"logic": {
					"Banjo-Kazooie": "TalonTrot and GrenadeEggs and ClockworkKazooieEggs and EggAim and ThirdPersonEggShooting and Climb and BeakBusterJump and ClockworkWarp"
				}
			},
			"IoH: Quagmire Near Cauldron Keep Entrance": {
				"logic": {
					"BK Claw Clamber Boots": "true"
				}
			},
			"IoH: Warp Silos": {
				"logic": {
					"Banjo-Kazooie": "QuagmireWarpSilo"
				}
			},
			"IoH: Quagmire On Pole": {
				"logic": {
					"Banjo-Kazooie": "TallJump and IoHQuagmireSpringPadSwitchPressed and Climb"
				}
			}
		},
	},
	"IoH: Quagmire Behind GI Door": {
		"exits": {
			"Grunty Industries": {
				"id": 0x09,
				"groups": {"World Entrances"},
				"logic": {
					"Banjo-Kazooie": "true",
					"Talon Trot": "TalonTrotSmuggleCrossWorld"
				}
			},
			"IoH: Quagmire": {
				"logic": "GruntyIndustries"
			}
		}
	},
	"IoH: Quagmire on Ledge to Wasteland": {
		"exits": {
			"IoH: Quagmire": {},
			"IoH: Wasteland Ledge to Quagmire": {
				"logic": {
					"Banjo-Kazooie": "true"
				}
			}
		}
	},
	"IoH: Quagmire Near Cauldron Keep Entrance": {
		"exits": {
			"IoH: Quagmire Behind Cauldron Keep Gate": {
				"logic": "CauldronKeep"
			},
			"IoH: Quagmire": {
				"logic": {
					"Banjo-Kazooie": "DamageBoost or Flutter or AirRatatatRap or BeakBusterFall"
				}
			},
			"IoH: Quagmire On Pole": {
				"logic": {
					"Banjo-Kazooie": "Climb"
				}
			},
			"IoH: Quagmire Spring Pad Switch Pressed": {}
		}
	},
	"IoH: Quagmire Spring Pad Switch Pressed": {"macro": {"event"}},
	"IoH: Quagmire Behind Cauldron Keep Gate": {
		"exits": {
			"Cauldron Keep": {
				"id": 0x01,
				"groups": {"World Entrances"},
				"logic": {
					"Banjo-Kazooie": "true",
					"Talon Trot": "TalonTrotSmuggleCrossWorld"
				}
			},
			"IoH: Quagmire Near Cauldron Keep Entrance": {
				"logic": "DamageBoost or CauldronKeep"
			}
		}
	},
	"IoH: Quagmire On Pole": {
		"exits": {
			"IoH: Quagmire": {},
			"IoH: Quagmire Near Cauldron Keep Entrance": {}
		}
	},
}
