from .. import Regions
instant_transform = {"Mumbo", "Stony"}
regions: Regions = {
	"MT: Open Top Treasure Chamber Door": {"macro": {"event"}},
	"MT: Treasure Chamber Bottom": {
		"locations": {
			"MT: Treasure Chamber Jiggy": {
				"logic": "TDLPricelessRelicThingy",
				"item": "Jiggy",
			},
		},
		"exits": {
			"MT: Main Map": {
				"id": -1
			},
			"MT: Treasure Chamber Honeycomb Pile": {
				"logic": {
					"Banjo-Kazooie": {
						"Clockwork Kazooie": "ClockworkShot",
						"Banjo-Kazooie": "TalonTrot or SlopeJump and FlapFlip and TallJump and BeakBusterJump",
					},
					"Talon Trot": "true"
				}
			},
			"MT: Open Top Treasure Chamber Door": {
				"logic": {
					"Banjo-Kazooie": "true"
				}
			}
		}
	},
	"MT: Treasure Chamber Honeycomb Pile": {
		"locations": {
			"MT: Treasure Chamber Honeycomb": {
				"item": "EmptyHoneycomb",
				"explicit_logic": {
					"Clockwork Kazooie": "true"
				}
			},
		},
		"exits": {
			"MT: Treasure Chamber Bottom": {},
			"MT: Treasure Chamber In Front of Unga Bunga Gate": {
				"logic": {
					"Banjo-Kazooie": "FlapFlip and GripGrab and TallJump"
				}
			}
		}
	},
	"MT: Treasure Chamber In Front of Unga Bunga Gate": {
		"exits": {
			"MT: Treasure Chamber Honeycomb Pile": {
				"logic": {
					"Banjo-Kazooie": "GripGrab"
				}
			},
			"MT: Top Platform Outside Treasure Chamber": {
				"logic": {
					"Banjo-Kazooie": "TallJump"
				}
			},
			"MT: Treasure Chamber Behind Unga Bunga Gate": {
				"logic": "MTTreasureChamberUngaBungaSwitchPressed"
			},
			"MT: Treasure Chamber Unga Bunga Switch Pressed": {},
		}
	},
	"MT: Treasure Chamber Behind Unga Bunga Gate": {
		# TODO: TDL transition
		"exits": {
			"MT: Treasure Chamber In Front of Unga Bunga Gate": {
				"logic": "MTTreasureChamberUngaBungaSwitchPressed"
			},
		}
	},
	"MT: Treasure Chamber Unga Bunga Switch Pressed": {"macro": {"event"}},
}
