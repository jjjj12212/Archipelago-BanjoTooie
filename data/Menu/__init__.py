# Regions in this file are special.
from .. import Regions
regions: Regions = {
	"Menu": {
		# Logic entry point. Logic will always start here.
		# Locations in this Region will never be sent to Archipelago.

		"locations": {
			"Completion Condition": {
				# This location's logic is passed to Archipelago.

				"logic": """
					'HAG-1' in ChosenGoals and CKDefeatedHAG1
					or 'HAG-1' not in ChosenGoals and PartyAtBottles
				""",
			},
		},
		"exits": {
			"Events": {},
			"Spiral Mountain": {"id": 0x04},
		},
	},

	"Starting Inventory": {
		# Locations in this region will have their item added to the player's starting inventory if:
		#   * The logic evaluates to True
		# Logic parsing only has the context of slot options.
		# Locations in this Region will never be sent to Archipelago.

		"locations": {
		},
	},

	"Starting Inventory From Pool": {
		# Same as Starting Inventory, except the items are removed from the pool.

		"locations": {
			"Starting Eggs": {
				"item": {
					"FireEggs": "ChosenEggs == 'fire_eggs'",
					"GrenadeEggs": "ChosenEggs == 'grenade_eggs'",
					"IceEggs": "ChosenEggs == 'ice_eggs'",
					"ClockworkKazooieEggs": "ChosenEggs == 'clockwork_kazooie_eggs'",
					"Nothing": "true",
				},
			},
		},
	},

	"Extra Items": {
		# Locations in this region will have their item added to the player's starting inventory if:
		#   * The item's option (as defined in items.py) evaluates to False
		#   * Or the location's logic evaluates to False
		#   * Or there aren't enough randomized filler/useful items
		# Logic parsing only has the context of slot options.
		# Locations in this Region will never be sent to Archipelago.

		"locations": {
			"Blue Eggs": {"item": "BlueEggs", "logic": "ChosenEggs != 'blue_eggs'"},
			"Dive": {"item": "Dive"},
			"Flight Pad": {"item": "FlightPad"},
			"Ground Rat-a-tat Rap": {"item": "GroundRatatatRap"},
			"Roll": {"item": "Roll"},
			"Air Rat-a-tat Rap": {"item": "AirRatatatRap"},
			"Beak Barge": {"item": "BeakBarge"},
			"Tall Jump": {"item": "TallJump"},
			"Flutter": {"item": "Flutter"},
			"Flap Flip": {"item": "FlapFlip"},
			"Climb": {"item": "Climb"},
			"Talon Trot": {"item": "TalonTrot"},
			"Beak Buster": {"item": "BeakBuster"},
			"Wonderwing": {"item": "Wonderwing"},
			"Stilt Stride": {"item": "StiltStride"},
			"Turbo Trainers": {"item": "TurboTrainers"},
			"Beak Bomb": {"item": "BeakBomb"},
			"Third Person Egg Shooting": {"item": "ThirdPersonEggShooting"},
		},
	},

	"Events": {
		# This region is for defining globally accessible events.

		"exits": {
			"Open Back Doors": {"logic": "OpenBackDoors"},
			"GGM: Levitate Chuffy The Train": {"logic": "ShuffleChuffy and Chuffy"},
			"GI Floor 1: Opened Main Door": {"logic": "OpenGIFrontDoor"},
		}
	},
	"Open Back Doors": {
		"exits": {
			"GI Floor 1: Opened Back Door": {},
		}
	}
}
