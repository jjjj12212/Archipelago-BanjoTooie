from .. import Regions
regions: Regions = {
	"IoH: Pine Grove": {
		"id": 0x0154,
		"locations": {
			"IoH: Pine Grove Note 1": {
				"item": "NoteNest",
			},
			"IoH: Pine Grove Note 2": {
				"item": "NoteNest",
			},
			"IoH: Grenade Eggs Silo": {
				"item": "GrenadeEggs",
				"logic": {"Banjo-Kazooie": "Notes >= ChosenMoveSiloCosts['Grenade Eggs']"},
			},
			"IoH: Pine Grove Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Pine Grove Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Pine Grove Feather Nest 3": {
				"item": "FeatherNest",
			},
			"IoH: Pine Grove Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Pine Grove Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Pine Grove Egg Nest 3": {
				"item": "EggNest",
			},
			"IoH: Pine Grove Signpost 1": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Pine Grove Signpost 2": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Pine Grove Signpost 3": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Pine Grove Silo Tagged": {
				"item": "PineGroveWarpSilo",
			},
		},
		"exits": {
			"IoH: Plateau": {},
			"IoH: Pine Grove Behind Witchyworld Gate": {
				"logic": "Witchyworld"
			},
			"IoH: Warp Silos": {
				"logic": {
					"Banjo-Kazooie": "PineGroveWarpSilo"
				}
			},
			"IoH: Pine Grove Underwater": {
				"logic": {
					"Banjo-Kazooie": "Dive"
				}
			},
			"IoH: Wumba's Wigwam": {}
		},
	},
	"IoH: Pine Grove Behind Witchyworld Gate": {
		"exits": {
			"Witchyworld": {
				"id": 0x12,
				"groups": {"World Entrances"},
				"logic": {
					"Banjo-Kazooie": "true",
					"Talon Trot": "TalonTrotSmuggleCrossWorld"
				},
			},
			"IoH: Pine Grove": {
				"logic": "Witchyworld"
			}
		}
	},
	"IoH: Pine Grove Underwater": {
		"locations": {
			"IoH: Pine Grove Underwater Note 1": {
				"item": "NoteNest",
			},
			"IoH: Pine Grove Underwater Note 2": {
				"item": "NoteNest",
			},
		},
		"exits": {
			"IoH: Pine Grove": {
				"logic": "TallJump or GripGrab or HardJumps and BeakBusterJump"
			},
			"IoH: Pine Grove Underwater Behind the Boulder": {
				"logic": {
					"Banjo-Kazooie": "TalonTorpedo"
				}
			}
		}
	},
	"IoH: Pine Grove Underwater Behind the Boulder": {
		"exits": {
			"IoH: Pine Grove Underwater": {
				"logic": {
					"Banjo-Kazooie": "ClipPastPineGroveBoulder or TalonTorpedo"
				}
			},
			"IoH: Another Digger Tunnel: Underwater": {},
		}
	},
	"IoH: Wumba's Wigwam": {
		"locations": {
			"IoH Dragon Transform": {"logic": "HumbaDragon"},
			"IoH: Wumba's Wigwam Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Wumba's Wigwam Egg Nest 2": {
				"item": "EggNest",
			},
		}
	},

}
