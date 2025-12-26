from .. import Regions
default_id = 0x0105
instant_transform = {"Mumbo", "Washer"}
regions: Regions = {
	"GI Elevator Shaft: Climbing": {
		"exits": {
			"GI Elevator Shaft: Floor 1": {},
			"GI Elevator Shaft: Floor 2": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or Flutter
						or AirRatatatRap
						or BeakBusterJump
					""",
					"Banjo": """
						TallJump
						or PackWhackJump
					""",
				},
			},
			"GI Elevator Shaft: Floor 3": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or Flutter
						or AirRatatatRap
						or BeakBusterJump
					""",
					"Banjo": """
						TallJump
						or PackWhackJump
					""",
				},
			},
			"GI Elevator Shaft: Floor 4": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump
						or Flutter
						or AirRatatatRap
						or BeakBusterJump
					""",
					"Banjo": """
						TallJump
						or PackWhackJump
					""",
				},
			},
			"GI Elevator Shaft: Hint Signs": {
				"logic": {
					"Banjo-Kazooie": """
						TallJump and BeakBusterJump
						or Flutter
						or AirRatatatRap
					""",
					"Banjo": "PackWhackJump",
				},
			},
		}
	},
	"GI Elevator Shaft: Floor 1": {
		"exits": {
			"GI Floor 1": {"id": 0x02},
			"GI Elevator Shaft: Climbing": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
				},
			},
		}
	},
	# Fall damage not part of logic to prevent multiple requirements in a row, possibly exceeding max health.
	"GI Elevator Shaft: Floor 2": {
		"locations": {
			"GI Elevator Shaft: Floor 2 Egg Nest": {"item": "EggNest"},
		},
		"exits": {
			"GI Floor 2: Electromagnet Chamber Behind Elevator Door": {"id": 0x02},
			"GI Elevator Shaft: Climbing": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
				},
			},
			"GI Elevator Shaft: Floor 1": {
				"logic": {
					"Banjo-Kazooie": """
						Flutter
						or BeakBusterFall
						or WonderwingFall
						or SlideJump and GroundRatatatRapFall and AirRatatatRap
					""",
					"Banjo": """
						PackWhackFall and (ShackPackFall or TaxiPackFall)
						or SnoozePackFall
					""",
					"Kazooie": "",
				},
			},
		}
	},
	"GI Elevator Shaft: Floor 3": {
		"locations": {
			"GI Elevator Shaft: Floor 3 Egg Nest": {"item": "EggNest"},
		},
		"exits": {
			"GI Floor 3: Boiler Plant Behind Elevator Door": {"id": 0x02},
			"GI Elevator Shaft: Climbing": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
				},
			},
			"GI Elevator Shaft: Floor 1": {
				"logic": {
					"Banjo": "SnoozePackFall",
				}
			},
			"GI Elevator Shaft: Floor 2": {
				"logic": {
					"Banjo-Kazooie": """
						Flutter
						or BeakBusterFall
						or WonderwingFall
						or SlideJump and GroundRatatatRapFall and AirRatatatRap
					""",
					"Banjo": "PackWhackFall and (ShackPackFall or TaxiPackFall)",
					"Kazooie": "",
				},
			},
		}
	},
	"GI Elevator Shaft: Floor 4": {
		"locations": {
			"GI Elevator Shaft: Floor 4 Egg Nest": {"item": "EggNest"},
		},
		"exits": {
			"GI Floor 4: Behind Elevator Door": {"id": 0x06},
			"GI Elevator Shaft: Climbing": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
				},
			},
			"GI Elevator Shaft: Floor 1": {
				"logic": {
					"Banjo": "SnoozePackFall",
				}
			},
			"GI Elevator Shaft: Floor 3": {
				"logic": {
					"Banjo-Kazooie": """
						Flutter
						or BeakBusterFall
						or WonderwingFall
						or SlideJump and GroundRatatatRapFall and AirRatatatRap
					""",
					"Banjo": "PackWhackFall and (ShackPackFall or TaxiPackFall)",
					"Kazooie": "",
				},
			},
		}
	},
	"GI Elevator Shaft: Hint Signs": {
		"locations": {
			"GI Elevator Shaft: Signpost 1": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"GI Elevator Shaft: Signpost 2": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		},
		"exits": {
			"GI Elevator Shaft: Climbing": {
				"logic": {
					"Banjo-Kazooie": "Climb",
					"Banjo": "Climb",
				},
			},
		}
	},
}
