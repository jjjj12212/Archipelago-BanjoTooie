from typing import Literal

Option = str
# If Option evaluates to True using logic parsing, items within are shuffled from their locations.
# Their locations are events otherwise.
# Logic parsing only has the context of slot options.

Name = str
# Item name.

Classifiction = Literal[
	"filler",
	"trap",
	"useful",
	"progression",
	"progression_skip_balancing",
	"progression_deprioritized_skip_balancing",
	"progression_deprioritized"
]
Class = Classifiction | dict[Classifiction, str]
# Classifiction:
#   The item's classification will be set to this.
#
# dict[Classifiction, str]:
#   DictKey specifies the classification for this item, if DictValue evaluates to True using logic parsing.
#   The first DictValue that returns True is used, the rest are ignored.
#   If all return False, "filler" is used.
#   Logic parsing only has the context of slot options.

items: dict[Option, dict[Name, Class]] = {
	"false": {
	# Allows defining event items where the event can happen from multiple locations.
	# Event items must be "progression".

		"GI Cleaned Skivvy": "progression",
	},
	"true": {
	# For items that either don't have a dedicated location, or are always shuffled.

		"Nothing": "filler",
		# A unique item that gets replaced with other items.
		"Big-O Pants": "filler",

		"Jiggy": "progression_skip_balancing",
		"Blue Eggs": "progression",
		"Bass Clef": "progression_skip_balancing",
		"Mumbo Token": "progression_skip_balancing",
		"Trip Trap": "trap",
		"Slip Trap": "trap",
		"Transform Trap": "trap",
		"Squish Trap": "trap",
		"Tip Trap": "trap",
	},
	"ShuffleCheatoPages": {
		"Cheato Page": {"progression_skip_balancing": "ShuffleCheatoRewards"},
	},
	"ShuffleHoneycombs": {
		"Empty Honeycomb": {"progression_skip_balancing": "ShuffleHoneyBRewards", "useful":"true"},
	},
	"ShuffleJinjos": {
		"White Jinjo": "progression_skip_balancing",
		"Orange Jinjo": "progression_skip_balancing",
		"Yellow Jinjo": "progression_skip_balancing",
		"Brown Jinjo": "progression_skip_balancing",
		"Green Jinjo": "progression_skip_balancing",
		"Red Jinjo": "progression_skip_balancing",
		"Blue Jinjo": "progression_skip_balancing",
		"Purple Jinjo": "progression_skip_balancing",
		"Black Jinjo": "progression_skip_balancing",
	},
	"ShuffleDoubloons": {
		"Doubloon": "progression_skip_balancing",
	},
	"ShuffleTrebleClefs": {
		"Treble Clef": "progression_skip_balancing",
	},
	"ShuffleNoteNests": {
		"Note Nest": "progression_skip_balancing",
	},
	"ShuffleBTMoves": {
		"Grip Grab": "progression",
		"Breegull Blaster": "progression",
		"Egg Aim": "progression",
		"Bill Drill": "progression",
		"Beak Bayonet": "progression",
		"Airborne Egg Aiming": "progression",
		"Split Up": "progression",
		"Wing Whack": "progression",
		"Talon Torpedo": "progression",
		"Sub-Aqua Egg Aiming": "progression",
		"Shack Pack": "progression",
		"Glide": "progression",
		"Snooze Pack": "progression",
		"Leg Spring": "progression",
		"Claw Clamber Boots": "progression",
		"Springy Step Shoes": "progression",
		"Taxi Pack": "progression",
		"Hatch": "progression",
		"Pack Whack": "progression",
		"Sack Pack": "progression",
		"Fire Eggs": "progression",
		"Grenade Eggs": "progression",
		"Clockwork Kazooie Eggs": "progression",
		"Ice Eggs": "progression",
		"Fast Swimming": "progression",
		"Double Air": "progression",
		"Amaze-O-Gaze": "progression",
		"Baby T-Rex Roar": "progression",
	},
	"ShuffleStopNSwop": {
		"Breegull Bash": "progression",
		"Homing Eggs": "filler",
		"Ice Key": "progression",
		"Pink Mystery Egg": "progression",
		"Blue Mystery Egg": "progression",
	},
	"ShuffleHoneyBRewards": {
		"Health Upgrade": "progression",
	},
	"ShuffleBKMoves == 'all'": {
		"Tall Jump": "progression",
		"Talon Trot": "progression",
	},
	"ShuffleBKMoves != 'none'": {
		"Dive": "progression",
		"Flight Pad": "progression",
		"Ground Rat-a-tat Rap": "progression",
		"Roll": "progression",
		"Air Rat-a-tat Rap": "progression",
		"Beak Barge": "progression",
		"Flutter": "progression",
		"Flap Flip": "progression",
		"Climb": "progression",
		"Beak Buster": "progression",
		"Wonderwing": "progression",
		"Stilt Stride": "progression",
		"Turbo Trainers": "progression",
		"Beak Bomb": "progression",
		"Third Person Egg Shooting": "progression",
	},
	"ShuffleCheatoRewards": {
		"Cheato Reward: Feathers": "filler",
		"Cheato Reward: Eggs": "filler",
		"Cheato Reward: Fallproof": "filler",
		"Cheato Reward: Honeyback": "filler",
		"Cheato Reward: Jukebox": "filler",
	},
	"ShuffleBigTopTickets": {
		"Big Top Ticket": "progression_skip_balancing",
	},
	"ShuffleGreenRelics": {
		"Green Relic": "progression_skip_balancing",
	},
	"ShuffleBeans": {
		"Bean": "progression_skip_balancing",
	},
	"ShuffleGlowbos": {
		"Mumbo: Golden Goliath": "progression",
		"Mumbo: Levitate": "progression",
		"Mumbo: Power": "progression",
		"Mumbo: Oxygenate": "progression",
		"Mumbo: Enlarge": "progression",
		"Mumbo: EMP": "progression",
		"Mumbo: Life Force": "progression",
		"Mumbo: Rain Dance": "progression",
		"Mumbo: Heal": "progression",
		"Humba: Stony": "progression",
		"Humba: Detonator": "progression",
		"Humba: Money Van": "progression",
		"Humba: Sub": "progression",
		"Humba: T-Rex": "progression",
		"Humba: Washing Machine": "progression",
		"Humba: Snowball": "progression",
		"Humba: Bee": "progression",
		"Humba: Dragon": "progression",
	},
	"ShuffleTrainStations": {
		"IoH: Train Station": "progression",
		"TDL: Train Station": "progression",
		"GI: Train Station": "progression",
		"HFP: Lava Side Train Station": "progression",
		"HFP: Icy Side Train Station": "progression",
		"WW: Train Station": "progression",
	},
	"ShuffleChuffy": {
		"Chuffy": "progression",
	},
	"JiggywiggysChallenges in ['shuffled', 'auto_shuffled']": {
		"Mayahem Temple": "progression",
		"Glitter Gulch Mine": "progression",
		"Witchyworld": "progression",
		"Jolly Roger's Lagoon": "progression",
		"Terrydactyland": "progression",
		"Grunty Industries": "progression",
		"Hailfire Peaks": "progression",
		"Cloud Cuckooland": "progression",
		"Cauldron Keep": "progression",
		"HAG-1": "progression",
	},
	"ShuffleNests": {
		"Egg Nest": "filler",
		"Feather Nest": "filler",
		"Golden Egg Nest": "trap",
	},
	"ShuffleWarpSilos": {
		"Jinjo Village Warp Silo": "progression",
		"Wooded Hollow Warp Silo": "progression",
		"Plateau Warp Silo": "progression",
		"Pine Grove Warp Silo": "progression",
		"Cliff Top Warp Silo": "progression",
		"Wasteland Warp Silo": "progression",
		"Quagmire Warp Silo": "progression",
	},
	"ShuffleWarpPads": {
		"MT: World Entry And Exit Warp Pad": "progression",
		"MT: Outside Mumbo's Skull Warp Pad": "progression",
		"MT: Prison Compound Warp Pad": "progression",
		"MT: Near Wumba's Wigwam Warp Pad": "progression",
		"MT: Kickball Stadium Lobby Warp Pad": "progression",
		"GGM: World Entry And Exit Warp Pad": "progression",
		"GGM: Outside Mumbo's Skull Warp Pad": "progression",
		"GGM: Inside Wumba's Wigwam Warp Pad": "progression",
		"GGM: Outside The Crushing Shed Warp Pad": "progression",
		"GGM: Near The Train Station Warp Pad": "progression",
		"WW: World Entry And Exit Warp Pad": "progression",
		"WW: Behind The Big Top Tent Warp Pad": "progression",
		"WW: Space Zone Warp Pad": "progression",
		"WW: Outside Wumba's Wigwam Warp Pad": "progression",
		"WW: Outside Mumbo's Skull Warp Pad": "progression",
		"JRL: Town Center Warp Pad": "progression",
		"JRL: Atlantis Warp Pad": "progression",
		"JRL: Sunken Ship Warp Pad": "progression",
		"JRL: Big Fish Cavern Warp Pad": "progression",
		"JRL: Lockers Cavern Warp Pad": "progression",
		"TDL: World Entry And Exit Warp Pad": "progression",
		"TDL: Stomping Plains Warp Pad": "progression",
		"TDL: Outside Mumbo's Skull Warp Pad": "progression",
		"TDL: Outside Wumba's Wigwam Warp Pad": "progression",
		"TDL: Top Of The Mountain Warp Pad": "progression",
		"GI Floor 1: Entrance Door Warp Pad": "progression",
		"GI Floor 2: Outside Wumba's Wigwam Warp Pad": "progression",
		"GI Floor 3: Outside Mumbo's Skull Warp Pad": "progression",
		"GI Floor 4: Near The Crushers Warp Pad": "progression",
		"GI Outside: On The Roof Outside Warp Pad": "progression",
		"HFP: Fire Side - Lower Area (Mumbo) Warp Pad": "progression",
		"HFP: Fire Side - Upper Area Warp Pad": "progression",
		"HFP: Ice Side - Upper Area Warp Pad": "progression",
		"HFP: Ice Side - Lower Area (Wumba) Warp Pad": "progression",
		"HFP: Ice Side - Inside Icicle Grotto Warp Pad": "progression",
		"CCL: World Entry And Exit Warp Pad": "progression",
		"CCL: Central Cavern Warp Pad": "progression",
		"CK: Bottom Of The Tower Warp Pad": "progression",
		"CK: Top Of The Tower Warp Pad": "progression",
	},
}
