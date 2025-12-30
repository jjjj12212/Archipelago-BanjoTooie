from .. import Regions
instant_transform = {"Mumbo", "Stony"}
regions: Regions = {
	"Mayahem Temple": {
		"id": 0x00B8,
		"exits": {
			"IoH: Wooded Hollow": {
				"id": 0x02,
				"groups":{"World Exits"},
			},
			"MT: Main Map": {}
		},
	},
	"MT: Warp Pads": {
		"exits": {
			"MT: Main Map": {
				"logic": "MTWorldEntryAndExitWarpPad or MTOutsideMumbosSkullWarpPad"
			},
			"MT: Jade Snake Grove": {
				"logic": "MTNearWumbasWigwamWarpPad"
			},
			"MT: Prison Compound": {
				"logic": "MTPrisonCompoundWarpPad"
			},
			"MT: Kickball Stadium": {
				"logic": "MTKickballStadiumLobbyWarpPad"
			}
		}
	},
}
