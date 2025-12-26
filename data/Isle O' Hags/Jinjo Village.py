from .. import Regions
regions: Regions = {
	"Jinjo Village": {
		"locations": {
			"IoH: White Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(WhiteJinjo, 1)",
			},
			"IoH: Orange Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(OrangeJinjo, 2)",
			},
			"IoH: Yellow Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(YellowJinjo, 3)",
			},
			"IoH: Brown Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(BrownJinjo, 4)",
			},
			"IoH: Green Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(GreenJinjo, 5)",
			},
			"IoH: Red Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(RedJinjo, 6)",
			},
			"IoH: Blue Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(BlueJinjo, 7)",
			},
			"IoH: Purple Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(PurpleJinjo, 8)",
			},
			"IoH: Black Jinjo Family Jiggy": {
				"item": "Jiggy",
				"logic": "(BlackJinjo, 9)",
			},
			"IoH: King Jingaling Jiggy": {
				"item": "Jiggy",
			},
			"IoH: Treble Clef": {
				"item": "TrebleClef",
			},
			"IoH: White Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'White Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'White Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(WhiteJinjo, 1)",
			},
			"IoH: Orange Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Orange Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Orange Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(OrangeJinjo, 2)",
			},
			"IoH: Yellow Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Yellow Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Yellow Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(YellowJinjo, 3)",
			},
			"IoH: Brown Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Brown Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Brown Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(BrownJinjo, 4)",
			},
			"IoH: Green Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Green Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Green Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(GreenJinjo, 5)",
			},
			"IoH: Red Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Red Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Red Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(RedJinjo, 6)",
			},
			"IoH: Blue Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Blue Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Blue Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(BlueJinjo, 7)",
			},
			"IoH: Purple Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Purple Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Purple Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(PurpleJinjo, 8)",
			},
			"IoH: Black Jinjo Family Mumbo Token": {
				"item": {"MumboToken":"'Black Jinjo Family' in ChosenGoals", "Nothing":"true"},
				"enabled": "'Black Jinjo Family' in VictoryGoals",
				"locked": "true",
				"logic": "(BlackJinjo, 9)",
			},
			"IoH: Ice Key": {
				"item": "IceKey",
			},
			"IoH: Jinjo Village By Silo Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village By Silo Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Jinjo Village By Silo Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village By Silo Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Jinjo Village Top Row of Houses Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Jinjo Village Top Row of Houses Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village Outside Bottle's House Feather Nest 1": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village Outside Bottle's House Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village Near Shortcut Egg Nest 1": {
				"item": "EggNest",
			},
			"IoH: Jinjo Village Near Shortcut Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Jinjo Village Top Row of Houses Feather Nest 2": {
				"item": "FeatherNest",
			},
			"IoH: Jinjo Village Top Row of Houses Egg Nest 2": {
				"item": "EggNest",
			},
			"IoH: Grey Jinjo Family House Signpost": {
				"item": "Nothing",
				"groups": {"HintSigns"},
				"enabled": "not ShuffleSigns",
			},
			"IoH: Jinjo Village Silo Tagged": {
				"item": "JinjoVillageWarpSilo",
			},
		},
		"exits": {
			"Inside the Digger Tunnel": {},
			"Bottles' House": {},
			"Wooded Hollow": {},
			"Warp Silos": {},
		},
	},
}
