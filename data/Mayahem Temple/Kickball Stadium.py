from .. import Regions
instant_transform = {"Mumbo", "Stony"}
regions: Regions = {
	"MT: Kickball Stadium": {
		"locations":{
			"MT: Kickball Jiggy": {
				"item": "Jiggy",
				"logic": "MTKickballRound1Won and MTKickballRound2Won and MTKickballRound3Won"
			},
			"MT: Kickball Mumbo Token": {
				"item": {"MumboToken":"'MT Kickball' in ChosenGoals", "Nothing":"true"},
				"enabled": "'MT Kickball' in VictoryGoals",
				"locked": "true",
			},
			"MT: Kickball Stadium Lobby Warp Pad Tagged": {
				"item": "MTKickballStadiumLobbyWarpPad",
			},
		},
		"exits": {
			"MT: Main Map": {
				"id": -1
			},
			"MT: Kickball Stadium Near Grate Switch": {
				"logic": "MTKickballStadiumSwitchPressed"
			},
			"MT: Warp Pads": {
				"logic": "MTKickballStadiumLobbyWarpPad"
			},
			"MT: Kickball Round 1 Opened": {
				"logic": {
					"Stony": "true"
				}
			},
			"MT: Kickball Round 1": {
				"logic": {
					"Stony": "true"
				}
			},
			"MT: Kickball Round 2": {
				"logic": {
					"Stony": "MTKickballRound1Won"
				}
			},
			"MT: Kickball Round 3": {
				"logic": {
					"Stony": "MTKickballRound2Won"
				}
			},
		}
	},
	"MT: Kickball Round 1": {
		"locations": {
			"MT Kickball Round 1 Won": {}
		},
		"exits": {
			"MT: Kickball Stadium": {}
		}
	},
	"MT: Kickball Round 2": {
		"locations": {
			"MT Kickball Round 2 Won": {}
		},
		"exits": {
			"MT: Kickball Stadium": {}
		}
	},
	"MT: Kickball Round 3": {
		"locations": {
			"MT Kickball Round 3 Won": {}
		},
		"exits": {
			"MT: Kickball Stadium": {}
		}
	},
	"MT: Kickball Stadium Near Grate Switch": {
		#TODO: Add HFP entrance
		"exits": {
			"MT: Kickball Stadium": {
				"logic": "MTKickballStadiumSwitchPressed"
			},
			"MT: Kickball Stadium Switch Pressed": {}
		}
	},
	"MT: Kickball Round 1 Opened": {"macro": {"event"}},
	"MT: Kickball Stadium Switch Pressed": {"macro": {"event"}},
}
