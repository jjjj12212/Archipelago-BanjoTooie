from .. import Regions
instant_transform = {"Mumbo", "Stony"}
regions: Regions = {
	"MT: Targitzan's Temple Lobby": {
		"locations": {
			"MT: Targitzan's Temple Lobby Left Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Lobby Left Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Lobby Left Egg Nest 3": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Lobby Right Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Lobby Right Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Lobby Right Egg Nest 3": {
				"item": "EggNest",
			}
		},
		"exits": {
			"MT: Main Map": {},
			"MT: Targitzan's Temple": {
				"logic": {
					"Banjo-Kazooie": "BreegullBlaster"
				}
			}
		}
	},
	"MT: Targitzan's Temple": {
		"locations": {
			"MT: Targitzan's Temple Right Entrance Relic": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Left Entrance Relic": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Blue Pillar Room Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Blue Pillar Room Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Blue Pillar Room Relic 3": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sput Sput Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sput Sput Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sput Sput Relic 3": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sput Sput Relic 4": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sput Sput Relic 5": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Green Pillar Room Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Green Pillar Room Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Green Pillar Room Relic 3": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Green Pillar Room Relic 4": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Green Pillar Room Relic 5": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sacred Chambers Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Near Sacred Chambers Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Secret Passage Near Sacred Chambers Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Secret Passage Near Sacred Chambers Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Secret Passage Near Sacred Chambers Relic 3": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Secret Passage Near Entrance Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Secret Passage Near Entrance Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Red Pillar Room Relic 1": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Red Pillar Room Relic 2": {
				"item": "GreenRelic",
			},
			"MT: Targitzan's Temple Red Pillar Room Relic 3": {
				"item": "GreenRelic",
			},
			"MT: Targitzan Temple Jinjo": {
				"item": "RedJinjo",
			},
			"MT: Targitzan's Temple Raising Slope Room Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Raising Slope Room Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple 4-Way Room Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple 4-Way Room Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple 4-Way Room Egg Nest 3": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple 4-Way Room Egg Nest 4": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Pillar Maze Egg Nest 1": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Pillar Maze Egg Nest 2": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Pillar Maze Egg Nest 3": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Raising Slope Room Egg Nest 3": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Golden Egg Nest": {
				"item": "EggNest",
			},
			"MT: Targitzan's Temple Signpost 1": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"MT: Targitzan's Temple Signpost 2": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
		},
		"exits": {
			"MT: Targitzan's Temple Lobby": {},
			"MT: Slighty Sacred Chamber": {
				"logic": "(GreenRelic, 10)"
			},
			"MT: Really Sacred Chamber": {
				"logic": "(GreenRelic, 20)"
			}
		}
	},
	"MT: Slighty Sacred Chamber": {
		"locations": {
			"MT: Slighty Sacred Chamber Jiggy": {
				"item": "Jiggy",
			},
		},
		"exits": {
			"MT: Targitzan's Temple": {}
		}
	},
	"MT: Really Sacred Chamber": {
		"locations": {
			"MT: Targitzan Jiggy": {
				"item": "Jiggy",
			},
			"MT: Targitzan Mumbo Token": {
				"item": {"MumboToken":"'Targitzan' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Targitzan' in VictoryGoals",
				"locked": "true",
			},
		},
		"exits": {
			"MT: Targitzan's Temple": {}
		}
	},
}
