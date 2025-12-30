from .. import Regions
instant_transform = {"Mumbo", "Stony"}
regions: Regions = {
	"MT: Open Top Treasure Chamber Door": {"macro": {"event"}},
	"MT: Top Platform Outside Treasure Chamber": {
		"locations": {
			"MT: Treasure Chamber Cheato Page": {
				"item": "CheatoPage",
			},
		},
		"exits": {
			"MT: Main Map": {},
			"MT: Treasure Chamber In Front of Unga Bunga Gate": {
				"id": -1,
				"logic": "MTOpenTopTreasureChamberDoor"
			}
		}
	},
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
						"Banjo-Kazooie": "TalonTrot",
						"Talon Trot": "true"
					}
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
