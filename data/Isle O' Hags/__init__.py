from .. import Regions
regions: Regions = {
	"IoH: Inside the Digger Tunnel": {
		"locations": {
			"IoH: Inside the Digger Tunnel Egg Nest": {
				"item": "EggNest",
			},
		},
		"exits": {
			"Spiral Mountain": {
				"logic": """
					SkipKlungo or (
						EggUse or BeakBarge or Roll or AirRatatatRap or Wonderwing
						or ExtraAttacks and (BeakBuster or GroundRatatatRap or BreegullBash)
					)
				"""
			},
			"IoH: Jinjo Village": {
				"logic": """
					SkipKlungo or (
						EggUse or BeakBarge or Roll or AirRatatatRap or Wonderwing
						or ExtraAttacks and (BeakBuster or GroundRatatatRap or BreegullBash)
					)
				"""
			},
		},
	},
	"IoH: Bottles' House": {
		"locations": {
			"IoH: Party At Bottles'": {"logic": "(MumboToken, MaxMumboTokens)"},
			"IoH: Amaze-O-Gaze Goggles": {
				"item": "AmazeOGaze",
			},
			"IoH: Bottles' House Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Bottles' House Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Bottles' House Feather Nest 1": {
				"item": "FeatherNest",
				"logic": {
						"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or WonderwingJump or GripGrab or BeakBusterJump",
						"Talon Trot": "true"
					}
			},
			"IoH: Bottles' House Feather Nest 2": {
				"item": "FeatherNest",
				"logic": {
						"Banjo-Kazooie": "TallJump or TalonTrot or FlapFlip or WonderwingJump or GripGrab or BeakBusterJump",
						"Talon Trot": "true"
					}
			},
		},
		"exits": {
			"IoH: Jinjo Village": {},
			"IoH: Bottles' House: Behind the Gate": {
				"logic": "IoHBottlesHouseGateOpened"
			}
		},
	},
	"IoH: Bottles' House: Behind the Gate": {
		"exits": {
			"IoH: Bottles' House": {
				"logic": "IoHBottlesHouseGateOpened"
			},
			"IoH: Wooded Hollow": {}
		}
	},
	"IoH: Bottles' House: Gate Opened": {"macro": {"event"}},
	"IoH: Another Digger Tunnel": {
		"exits": {
			"IoH: Wasteland": {
				"logic": """
							SkipKlungo or (
								EggUse or BeakBarge or Roll or AirRatatatRap or Wonderwing
								or ExtraAttacks and (BeakBuster or GroundRatatatRap or BreegullBash)
							)"""
			},
			"IoH: Another Digger Tunnel: Underwater": {
				"logic": {
					"Banjo-Kazooie": """
						Dive and (SkipKlungo or (
							EggUse or BeakBarge or Roll or AirRatatatRap or Wonderwing
							or ExtraAttacks and (BeakBuster or GroundRatatatRap or BreegullBash)
						)
					)"""
				}
			},
			"IoH: Pine Grove Underwater Behind the Boulder": {
				"logic": """
						BeakBuster and (SkipKlungo or (
							EggUse or BeakBarge or Roll or AirRatatatRap or Wonderwing
							or ExtraAttacks and (BeakBuster or GroundRatatatRap or BreegullBash)
						)
					)"""
			}
		},
	},
	"IoH: Another Digger Tunnel: Underwater": {
		"locations": {
			"IoH: Another Digger Tunnel Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Another Digger Tunnel Egg Nest 2": {
				"item": "EggNest",
			},
		},
		"exits": {
			"IoH: Another Digger Tunnel": {},
			"IoH: Pine Grove Underwater Behind the Boulder": {}
		}
	},
	"IoH: Warp Silos": {
		"exits": {
			"IoH: Jinjo Village": {
				"logic": "JinjoVillageWarpSilo"
			},
			"IoH: Wooded Hollow": {
				"logic": "WoodedHollowWarpSilo"
			},
			"IoH: Plateau": {
				"logic": "PlateauWarpSilo"
			},
			"IoH: Pine Grove": {
				"logic": "PineGroveWarpSilo"
			},
			"IoH: Cliff Top": {
				"logic": "CliffTopWarpSilo"
			},
			"IoH: Wasteland": {
				"logic": "WastelandWarpSilo"
			},
			"IoH: Quagmire": {
				"logic": "QuagmireWarpSilo"
			},
		},
	},
}
