from .. import Regions
regions: Regions = {
	"Cauldron Keep": {
		"id": 0x015D,
		"locations": {
			"CK: Tower Of Tragedy Mumbo Token": {
				"item": {"MumboToken":"'Tower of Tragedy' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Tower of Tragedy' in VictoryGoals",
				"locked": "true",
			},
		},
		"exits": {
			"IoH: Quagmire Behind Cauldron Keep Gate": {
				"id": 0x03,
				"groups":{"World Exits"},
				"logic": {
					"Banjo-Kazooie": "",
					"Talon Trot": "TalonTrotSmuggleCrossWorld",
				}
			},
			"Cauldron Keep - Temp": {},
		},
	},
	"Cauldron Keep - Temp": {
		"locations": {
			"CK: Defeated HAG-1": {"logic": "(MumboToken, MaxMumboTokens)"},
			"CK: Bottom of the Tower Warp Pad Tagged": {
				"item": "CKBottomOfTheTowerWarpPad",
			},
			"CK: Top of the Tower Warp Pad Tagged": {
				"item": "CKTopOfTheTowerWarpPad",
			},
		},
	},
}
