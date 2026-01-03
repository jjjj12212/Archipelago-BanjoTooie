from .. import Regions
regions: Regions = {
	"IoH: Jinjo Village": {
		"locations": {
			"IoH: Treble Clef": {
				"item": "TrebleClef",
				"logic": {
					"Banjo-Kazooie": "FlapFlip and GripGrab or FlapFlip and BeakBusterJump or ClockworkShot"
				}
			},
			"IoH: Ice Key": {
				"item": "IceKey",
				"logic": {
					"Banjo-Kazooie": "FlapFlip and GripGrab and (AnyAttack or ShootAnyEgg) or ClockworkShot"
				}
			},
			"IoH: Jinjo Village By Silo Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village By Silo Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Jinjo Village By Silo Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village By Silo Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Jinjo Village Top Row of Houses Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Jinjo Village Top Row of Houses Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village Outside Bottle's House Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village Outside Bottle's House Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village Near Shortcut Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Jinjo Village Near Shortcut Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Jinjo Village Top Row of Houses Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village Top Row of Houses Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Grey Jinjo Family House Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Jinjo Village Silo Tagged": {
				"item": "JinjoVillageWarpSilo",
			},
		},
		"exits": {
			"IoH: Inside the Digger Tunnel": {},
			"IoH: Bottles' House": {},
			"IoH: Warp Silos": {
				"logic": {
					"Banjo-Kazooie": "JinjoVillageWarpSilo"
				}
			},
			"IoH: King Jingaling's Throne Room": {},
			"White Jinjo Family House": {},
			"Orange Jinjo Family House": {},
			"Yellow Jinjo Family House": {},
			"Brown Jinjo Family House": {},
			"Green Jinjo Family House": {},
			"Red Jinjo Family House": {},
			"Blue Jinjo Family House": {},
			"Purple Jinjo Family House": {},
			"Black Jinjo Family House": {},
			# "Grey Jinjo Family House": {},
			"IoH: Jinjo Village On Top of the Ledge": {
				"logic": {
					"Banjo-Kazooie": """
						FlapFlip and GripGrab
						or HardJumps and TallJump and Flutter and BeakBusterJump
						or EasyJumps and TalonTrot and Flutter and BeakBusterJump
						or EasyJumps and TalonTrot and AirRatatatRap
					"""
				}
			}
		},
	},
	"Jinjo Family Jiggies": {
		"locations": {
			"IoH: White Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(WhiteJinjo, 1)",
			},
			"IoH: Orange Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(OrangeJinjo, 2)",
			},
			"IoH: Yellow Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(YellowJinjo, 3)",
			},
			"IoH: Brown Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(BrownJinjo, 4)",
			},
			"IoH: Green Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(GreenJinjo, 5)",
			},
			"IoH: Red Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(RedJinjo, 6)",
			},
			"IoH: Blue Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(BlueJinjo, 7)",
			},
			"IoH: Purple Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(PurpleJinjo, 8)",
			},
			"IoH: Black Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(BlackJinjo, 9)",
			},

			"IoH: White Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'White Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'White Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(WhiteJinjo, 1)",
			},
			"IoH: Orange Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Orange Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Orange Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(OrangeJinjo, 2)",
			},
			"IoH: Yellow Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Yellow Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Yellow Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(YellowJinjo, 3)",
			},
			"IoH: Brown Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Brown Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Brown Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(BrownJinjo, 4)",
			},
			"IoH: Green Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Green Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Green Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(GreenJinjo, 5)",
			},
			"IoH: Red Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Red Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Red Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(RedJinjo, 6)",
			},
			"IoH: Blue Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Blue Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Blue Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(BlueJinjo, 7)",
			},
			"IoH: Purple Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Purple Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Purple Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(PurpleJinjo, 8)",
			},
			"IoH: Black Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Black Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Black Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(BlackJinjo, 9)",
			},
		}
	},
	"IoH: Jinjo Village On Top of the Ledge": {
		"exits": {
			"IoH: Jinjo Village": {},
			"IoH: Wooded Hollow": {}
		}
	},
	"IoH: King Jingaling's Throne Room": {
		"locations": {
			"IoH: King Jingaling Jiggy": {
				"item": "Jiggy",
			},
		},
		"exits": {
			"IoH: Bottles' House: Gate Opened": {}
		}
	},
	"White Jinjo Family House": {
		"exits": {
			"IoH: Jinjo Village": {}
		}
	},
	"Orange Jinjo Family House": {
		"exits": {
			"IoH: Jinjo Village": {}
		}
	},
	"Yellow Jinjo Family House": {
		"exits": {
			"IoH: Jinjo Village": {}
		}
	},
	"Brown Jinjo Family House": {
		"exits": {
			"IoH: Jinjo Village": {}
		}
	},
	"Green Jinjo Family House": {
		"exits": {
			"IoH: Jinjo Village": {}
		}
	},
	"Red Jinjo Family House": {
		"exits": {
			"IoH: Jinjo Village": {}
		}
	},
	"Blue Jinjo Family House": {
		"exits": {
			"IoH: Jinjo Village": {}
		}
	},
	"Purple Jinjo Family House": {
		"exits": {
			"IoH: Jinjo Village": {}
		}
	},
	"Black Jinjo Family House": {
		"exits": {
			"IoH: Jinjo Village": {}
		}
	}
	# "Grey Jinjo Family House": {
	#     "exits": {
	#         "IoH: Jinjo Village": {}
	# 	  }
	# }
}
