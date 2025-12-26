from .. import Regions
regions: Regions = {
	"Inside the Digger Tunnel": {
		"locations": {
			"IoH: Inside the Digger Tunnel Egg Nest": {
				"item": "EggNest",
			},
		},
		"exits": {
			"Spiral Mountain": {},
			"Jinjo Village": {},
		},
	},
	"Bottles' House": {
		"locations": {
			"Party At Bottles'": {"logic": "(MumboToken, MaxMumboTokens)"},
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
			},
			"IoH: Bottles' House Feather Nest 2": {
				"item": "FeatherNest",
			},
		},
		"exits": {
			"Jinjo Village": {},
			"Wooded Hollow": {},
		},
	},
	"Another Digger Tunnel": {
		"locations": {
			"IoH: Another Digger Tunnel Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Another Digger Tunnel Egg Nest 2": {
				"item": "EggNest",
			},
		},
		"exits": {
			"Pine Grove": {},
			"Wasteland": {},
		},
	},
	"Warp Silos": {
		"exits": {
			"Jinjo Village": {},
			"Wooded Hollow": {},
			"Plateau": {},
			"Pine Grove": {},
			"Cliff Top": {},
			"Wasteland": {},
			"Quagmire": {},
		},
	},
}
