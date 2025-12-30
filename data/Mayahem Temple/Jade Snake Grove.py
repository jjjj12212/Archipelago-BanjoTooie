from .. import Regions
instant_transform = {"Mumbo", "Stony"}
regions: Regions = {
	"MT: Jade Snake Grove": {
		"locations": {
			"MT: Grip Grab Silo": {
				"item": "GripGrab",
			},
			"MT: Jade Snake Grove Glowbo": {
				"item": "HumbaStony",
			},
			"MT: Jade Snake Grove Near Warp Pad Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Jade Snake Grove Near Warp Pad Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Jade Snake Grove Quicksand Signpost 1": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"MT: Jade Snake Grove Quicksand Signpost 2": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"MT: Jade Snake Grove Jinjo": {
				"item": "PurpleJinjo",
			},
			"MT: Golden Goliath Jiggy": {
				"item": "Jiggy",
			},
			"MT: Near Wumba's Wigwam Warp Pad Tagged": {
				"item": "MTNearWumbasWigwamWarpPad",
			},
		},
		"exits": {
			"MT: Main Map": {},
			"MT: Wumba's Wigwam": {},
			"MT: Jade Snake Grove Top of Slope": {
				"logic": {
					"Banjo-Kazooie": "TalonTrot",
					"Talon Trot": "true"
				}
			},
			"MT: Warp Pads": {
				"logic": "MTNearWumbasWigwamWarpPad"
			},
			"MT: Jade Snake Grove Top of Code Chamber Entrance": {
				"logic": {
					"Banjo-Kazooie": {
						"Banjo-Kazooie": "TalonTrot or (TallJump or FlapFlip) and SlopeJump",
						"Clockwork Kazooie": "ClockworkShot"
					},
					"Mumbo": "TallJump and SlopeJump",
					"Stony": "SlopeJump",
					"Golden Goliath": "SlopeJump",
					"Talon Trot": "true",
				}
			},
			"MT: Open Code Chamber": {
				"logic": {
					"Golden Goliath": "true",
					"Banjo-Kazooie": "ShootExplosives"
				}
			},
			"MT: Code Chamber": {
				"logic": "MTOpenCodeChamber"
			},
			"MT: Jade Snake Grove Cheato Page Platform": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot"
					}
				}
			}
		}
	},
	"MT: Jade Snake Grove Top of Code Chamber Entrance": {
		"locations": {
			"MT: Jade Snake Grove Above Code Chamber Egg Nest": {
				"item": "EggNest",
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		}
	},
	"MT: Jade Snake Grove Top of Slope": {
		"exits": {
			"MT: Jade Snake Grove Ssslumber Jiggy Platform": {
				"logic": "FlapFlip and (GripGrab or BeakBusterJump)"
			},
			"MT: Jade Snake Grove Cheato Page Platform": {
				"logic": "FlapFlip and GripGrab"
			},
			"MT: Jade Snake Grove Left of Code Chamber Signpost Platform": {
				"logic": "FlapFlip and GripGrab"
			},
		}
	},
	"MT: Jade Snake Grove Cheato Page Platform": {
		"locations": {
			"MT: Jade Snake Grove Cheato Page": {
				"item": "CheatoPage",
                "explicit_logic": {
                    "Clockwork Kazooie": "true"
				}
			},
		}
	},
	"MT: Jade Snake Grove Ssslumber Jiggy Platform": {
		"locations": {
			"MT: Ssslumber Jiggy": {
				"item": "Jiggy",
			},
		}
	},
	"MT: Jade Snake Grove Left of Code Chamber Signpost Platform": {
		"locations": {
			"MT: Left of Code Chamber Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		}
	},
	"MT: Code Chamber": {
		"exits": {
			"MT: Jade Snake Grove": {}
		}
	},
	"MT: Open Code Chamber": {"macro": {"event"}},
	"MT: Wumba's Wigwam": {
		"locations": {
			"MT: Wumba's Wigwam Feather Nest 1": {
				"item": "FeatherNest",
			},
			"MT: Wumba's Wigwam Feather Nest 2": {
				"item": "FeatherNest",
			},
		},
		"exits": {
			"MT: Jade Snake Grove": {
				"id": -1
			},
			"MT: Wumba's Wigwam": {
				"logic": {
					"Banjo-Kazooie": {
						"Stony": "HumbaStony"
					}
				}
			}
		}
	},
}
