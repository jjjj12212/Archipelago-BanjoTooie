from .. import Regions
regions: Regions = {
	"Grunty Industries": {
		"id": 0x0100,
		"exits": {
			"Quagmire": {
				"id": 0x02,
				"groups": {"World Exits"},
				"logic": {
					"Banjo-Kazooie": "",
					"Talon Trot": "TalonTrotSmuggleCrossWorld",
				}
			},
			"GI Outside": {},
		}
	},
	"GI: Warp Pads": {
		"exits": {
			"GI: Warp Pad Exits": {
				"logic": {
					"Banjo-Kazooie",
					"Talon Trot",
					"Banjo",
					"Kazooie",
					"Mumbo",
				}
			}
		}
	},
	"GI: Warp Pad Exits": {
		"exits": {
			"GI Floor 1": {"logic": "GIFloor1EntranceDoorWarpPad"},
			"GI Floor 2: Near Wumba's Wigwam": {"logic": "GIFloor2OutsideWumbasWigwamWarpPad"},
			"GI Floor 3: Outside Mumbo's Skull": {"logic": "GIFloor3OutsideMumbosSkullWarpPad"},
			"GI Floor 4: Before Crushers": {"logic": "GIFloor4NearTheCrushersWarpPad"},
			"GI Outside: Lower Roof": {"logic": "GIOutsideOnTheRoofOutsideWarpPad"},
		}
	},
	"GI: Service Elevator": {
		"exits": {
			"GI Floor 1": {},
			"GI Floor 2: Near Service Elevator": {},
			"GI Floor 3: Near Service Elevator": {},
			"GI Floor 4": {},
			"GI Floor 5: Storage Area 1 Near Ladder": {},
		}
	},
	"GI Outside: Skivvy": {
		"locations": {
			"GI Outside: Cleaned Skivvy": {"item": "GICleanedSkivvy"},
			"GI Outside: Skivvy": {"item": "Nothing"},
		},
		"exits": {"GI: Skivvy Workers Jiggy": {}}
	},
	"GI Floor 1: Skivvy": {
		"locations": {
			"GI Floor 1: Cleaned Skivvy": {"item": "GICleanedSkivvy"},
			"GI Floor 1: Skivvy": {"item": "Nothing"},
		},
		"exits": {"GI: Skivvy Workers Jiggy": {}}
	},
	"GI Worker's Quarters: Skivvy": {
		"locations": {
			"GI Worker's Quarters: Cleaned Skivvy": {"item": "GICleanedSkivvy"},
			"GI Worker's Quarters: Skivvy": {"item": "Nothing"},
		},
		"exits": {"GI: Skivvy Workers Jiggy": {}}
	},
	"GI Floor 2: Skivvy": {
		"locations": {
			"GI Floor 2: Cleaned Skivvy": {"item": "GICleanedSkivvy"},
			"GI Floor 2: Skivvy": {"item": "Nothing"},
		},
		"exits": {"GI: Skivvy Workers Jiggy": {}}
	},
	"GI Floor 3: Skivvy": {
		"locations": {
			"GI Floor 3: Cleaned Skivvy": {"item": "GICleanedSkivvy"},
			"GI Floor 3: Skivvy": {"item": "Nothing"},
		},
		"exits": {"GI: Skivvy Workers Jiggy": {}}
	},
	"GI Floor 5: Skivvy": {
		"locations": {
			"GI Floor 5: Cleaned Skivvy": {"item": "GICleanedSkivvy"},
			"GI Floor 5: Skivvy": {"item": "Nothing"},
		},
		"exits": {"GI: Skivvy Workers Jiggy": {}}
	},
	"GI: Skivvy Workers Jiggy": {
		"locations": {
			"GI: Skivvy Workers Jiggy": {
				"item": "Jiggy",
				"logic": "(GICleanedSkivvy, 6)",
			},
		},
	},
}
