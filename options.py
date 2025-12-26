from dataclasses import dataclass
from typing import Iterable
if __package__:
	from . import data
else:
	import data
from Options import (
	OptionGroup,
	PerGameCommonOptions,
	ProgressionBalancing,
	Accessibility,
	StartInventoryPool,
	DeathLink,
	Toggle,
	DefaultOnToggle,
	Choice,
	Range,
	OptionSet,
	OptionCounter,
	Visibility,
)

### Common Options ###

class TagLink(Toggle):
	"""
		When other multiworld games tag/swap characters, you will automatically swap with them and vice versa.
	"""
	display_name = "Tag Link"

### Victory Options ###

class PresetVictoryGoals(Choice):
	"""
		Automatically enables specific **Victory Goals** depending on the selected option.

		This option adds to whatever is chosen for **Victory Goals**, allowing you to combine this setting.

		* **None**: No **Victory Goals** are automatically enabled.
		* **HAG1**: Unlock the HAG-1 fight and defeat Gruntilda.
		* **Minigame Hunt**: Clear the 14 minigames and the final Canary Mary race in Cloud Cuckoo Land to collect **Mumbo Tokens**.
		* **Boss Hunt**: Defeat the 8 world bosses and collect their **Mumbo Tokens**.
		* **Jinjo Family Rescue**: Rescue Jinjo Families to collect their prized **Mumbo Tokens**.
		* **Wonderwing Challenge**: Complete every goal to gain access to HAG-1 and Defeat Grunty. The Ultimate Banjo-Tooie experience!!
		* **Token Hunt**: Mumbo's tokens are scattered around the world. Help him find them!
		* **Boss Hunt + Hag1**: Combines **Boss Hunt** with **HAG-1**. HAG-1 won't open until the required amount of bosses are defeated.
	"""
	display_name = "Preset Victory Goals"
	option_none = 0
	option_hag1 = 1
	option_minigame_hunt = 2
	option_boss_hunt = 3
	option_jinjo_family_rescue = 4
	option_wonderwing_challenge = 5
	option_token_hunt = 6
	option_boss_hunt_and_hag1 = 7
	default = 1

class VictoryGoals(OptionSet):
	"""
		Set your **Victory Condition** by selecting which goals you must complete.

		Every selected goal you complete gives you a **Mumbo Token**, except for **HAG-1**.

		The door to HAG-1 won't open until you have your max number of **Mumbo Tokens**.

		If **HAG-1** isn't a goal and a boss or minigame gives you your final **Mumbo Token**, you will automatically achieve your **Victory Condition**.

		Otherwise, you must visit **Bottles' House** to achieve your **Victory Condition**.

		Defaults to **HAG-1** if empty and **Extra Mumbo Tokens** is 0.
	"""
	display_name = "Victory Goals"
	valid_keys: Iterable[str] = [
		"HAG-1",
		"Targitzan",
		"Old King Coal",
		"Mr. Patch",
		"Lord Woo Fak Fak",
		"Terry",
		"Weldar",
		"Chilly Willy",
		"Chilli Billi",
		"Mingy Jongo",
		"MT Kickball",
		"Ordnance Storage",
		"Hoop Hurry",
		"Dodgem Dome",
		"Saucer of Peril",
		"Balloon Burst",
		"Mini-Sub Challenge",
		"Chompas Belly",
		"Clinker's Cavern",
		"Twinkly Packing",
		"HFP Kickball",
		"Pot O' Gold",
		"Zubbas",
		"Trash Can",
		"Canary Mary",
		"Tower of Tragedy",
		"White Jinjo Family",
		"Orange Jinjo Family",
		"Yellow Jinjo Family",
		"Brown Jinjo Family",
		"Green Jinjo Family",
		"Red Jinjo Family",
		"Blue Jinjo Family",
		"Purple Jinjo Family",
		"Black Jinjo Family",
	]
	default: set[str] = set()

class ExtraMumboTokens(Range):
	"""
		Choose how many **Mumbo Tokens** are added to the pool.

		The actual amount of **Mumbo Tokens** added to the pool depends on your settings as extra **Mumbo Tokens** replace filler/useful items.

		**Mumbo Tokens** replace filler items first, then useful items.

		If there isn't enough room in the pool, the remaining **Mumbo Tokens** will be added to your **Starting Inventory**.
	"""
	display_name = "Extra Mumbo Tokens"
	range_start = 0
	range_end = 100
	default = 0

class MaxMumboTokens(Range):
	"""
		Choose the max number of **Mumbo Tokens** required to achieve your **Victory Condition** (or open HAG-1 if it is selected as a goal).

		Setting this to 0 will automatically set it to the sum of all selected goals and **Extra Mumbo Tokens**.

		It will also automatically be reduced to this value if needed.
	"""
	display_name = "Max Mumbo Tokens"
	range_start = 0
	range_end = 200
	default = 0

class ReplaceExcessMumboTokens(Toggle):
	"""
		If enabled, then **Max Mumbo Tokens** will be the actual number of tokens in the pool. The rest will be replaced with filler.

		**Mumbo Tokens** from **Victory Goals** will be removed first (in a random order), followed by any **Extra Mumbo Tokens**.

		This allows you to randomly choose a specific number of goals based on what you've selected.

		For example, you can select all bosses for **Victory Goals**, set **Max Mumbo Tokens** to 3 and enable this setting
		to have 3 random bosses chosen as your **Victory Condition**.
	"""
	display_name = "Replace Excess Mumbo Tokens"

class OpenHAG1(DefaultOnToggle):
	"""
		If enabled, the door to the HAG-1 fight will automatically open once you've received your max number of **Mumbo Tokens**.

		The HAG-1 item that normally opens the door will be replaced with filler.

		Otherwise it'll remain closed until you receive the **HAG-1** item (see the **Jiggywiggy Challenges** option) AND your max number of **Mumbo Tokens**.
	"""
	display_name = "Open HAG-1"

### Logic Options ###

class PresetLogicTricks(OptionSet):
	"""
		Automatically enables specific **Logic Tricks** depending on the selected option.

		This option adds to whatever is chosen for **Logic Tricks**, allowing you to combine this setting.

		Every option includes all tricks from the option above it.

		Having no tricks enabled is the easiest, but most restricted logic setting. Expectations will be limited to what Rare may have intended.

		* **Easy Tricks**: Easy to perform logic tricks will be enabled. You may be expected to think outside the box.
		* **Easy Tedious Tricks**: Logic tricks that are easy to perform, but annoying if you fail, will be enabled.
		* **Easy Glitches**: Glitches that are easy to perform will be enabled.
		* **Hard Tricks**: Difficult logic tricks will be enabled. You will likely be expected to perform tricky maneuvers.
		* **Hard Tedious Tricks**: Logic tricks that are difficult to perform and annoying if you fail will be enabled.
		* **Hard Glitches**: Glitches that are difficult to perform will be enabled.
		* **Frame Perfect**: Anything that requires **frame perfect** inputs will be enabled. Good luck.
	"""
	display_name = "Preset Logic Tricks"
	valid_keys = [
		"Easy Tricks",
		"Easy Tedious Tricks",
		"Easy Glitches",
		"Hard Tricks",
		"Hard Tedious Tricks",
		"Hard Glitches",
		"Frame Perfect",
	]
	default: set[str] = set()

class LogicTricks(OptionSet):
	"""
		Choose which logic tricks you are willing to perform.
	"""
	display_name = "Logic Tricks"
	valid_keys = [trick for preset_tricks in data.tricks.values() for trick in preset_tricks]
	default: set[str] = set()

class InstantTransform(Choice):
	"""
		Choose how restrictive **Instant Transform** is.

		**Instant Transform** allows you to instantly transform between Banjo-Kazooie, Mumbo and the world's transformation.

		Pressing **D-Pad Left** cycles through available characters.

		* **Disabled**: You won't be able to use **Instant Transform** at all.
		* **Logic**: Once you have the ability to manually transform, you can use **Instant Transform** for that form.
		* **No Logic**: You can freely transform once you have the respective form's item.
	"""
	display_name = "Instant Transform"
	option_disabled = 0
	option_logic = 1
	option_no_logic = 2
	default = 1

### Shuffle Options ###

class ShuffleBKMoves(Choice):
	"""
		Shuffle the moves that were learned in **Banjo-Kazooie**.

		* **None**: You will start with all of the moves from **Banjo-Kazooie**.
		* **Mcjiggy Special**: You will start with **Talon Trot** and **Tall Jump**. The rest of the moves from **Banjo-Kazooie** will be shuffled.
		* **All**: All of the moves from **Banjo-Kazooie** will be shuffled.
	"""
	display_name = "Shuffle Banjo-Kazooie Moves"
	option_none = 0
	option_mcjiggy_special = 1
	option_all = 2
	default = 0

class ShuffleBTMoves(Toggle):
	"""
		Shuffle all of **Jamjars'** and **Roysten's** moves, along with **Baby T-Rex Roar**.
	"""
	display_name = "Shuffle Banjo-Tooie Moves"

class ShuffleGlowbos(Toggle):
	"""
		Shuffle Glowbo locations. Instead of receiving Glowbos as items, you will receive either **Humba** or **Mumbo** access.

		When disabled, collecting a Glowbo will directly give you either **Humba** or **Mumbo** access depending on which is closer.
	"""
	display_name = "Shuffle Glowbos"

class ShuffleJinjos(Toggle):
	"""
		Shuffle **Jinjos**.
	"""
	display_name = "Shuffle Jinjos"

class ShuffleTrebleClefs(Toggle):
	"""
		Shuffle **Treble Clefs** (worth 20 notes).
	"""
	display_name = "Shuffle Treble Clefs"

class ShuffleNoteNests(Toggle):
	"""
		Shuffle **Note Nests** (worth 5 notes).
	"""
	display_name = "Shuffle Note Nests"

class ShuffleHoneycombs(Toggle):
	"""
		Shuffle **Empty Honeycomb Pieces**.
	"""
	display_name = "Shuffle Honeycombs"

class ShuffleHoneyBRewards(Toggle):
	"""
		Shuffle the **Extra Honeycombs** that **Honey B** normally trades.
	"""
	display_name = "Shuffle Honey B Rewards"

class ShuffleCheatoPages(Toggle):
	"""
		Shuffle **Cheato Pages**.
	"""
	display_name = "Shuffle Cheato Pages"

class ShuffleCheatoRewards(Toggle):
	"""
		Shuffle the cheat codes that Cheato normally trades.
	"""
	display_name = "Shuffle Cheato Rewards"

class ShuffleStopNSwop(Toggle):
	"""
		Shuffle the **Blue** and **Pink Mystery Eggs**, their rewards and the **Ice Key**.
	"""
	display_name = "Shuffle Stop 'n' Swop"

class ShuffleDoubloons(Toggle):
	"""
		Shuffle the **Doubloons** found in **Jolly Roger's Lagoon**.
	"""
	display_name = "Shuffle Doubloons"

class ShuffleGreenRelics(Toggle):
	"""
		Shuffle the **Green Relics** found in **Targitzan's Temple**.
	"""
	display_name = "Shuffle Green Relics"

class ShuffleBigTopTickets(Toggle):
	"""
		Shuffle the **Big Top Tickets** found in **Witchyworld**.
	"""
	display_name = "Shuffle Big Top Tickets"

class ShuffleBeans(Toggle):
	"""
		Shuffle the **Beans** found in **Cloud Cuckoo Land**.
	"""
	display_name = "Shuffle Beans"

class ShuffleWarpSilos(Toggle):
	"""
		Shuffle the **Warp Silos** found in **Isle O' Hags**. You won't be able to use a silo until you receive its item.
	"""
	display_name = "Shuffle Warp Silos"

class ShuffleWarpPads(Toggle):
	"""
		Shuffle **Warp Pads**. You won't be able to use a warp pad until you receive its item.
	"""
	display_name = "Shuffle Warp Pads"

class ShuffleSigns(Toggle):
	"""
		Reading a **? Sign** will give a shuffled item. Nothing is given if disabled.
	"""
	display_name = "Shuffle Signs"

class ShuffleJiggywiggysSuperSpecialChallenge(Toggle):
	"""
		Completing **Jiggywiggy's Super Special Challenge** will reward a shuffled item. Nothing is given if disabled.
	"""
	display_name = "Shuffle Jiggywiggy's Super Special Challenge"

class ShuffleNests(Toggle):
	"""
		Shuffle all **Egg** and **Feather** nests. Once collected, they will revert to their vanilla function.
	"""
	display_name = "Shuffle Nests"

class ShuffleChuffy(Toggle):
	"""
		Shuffle **Chuffy**. Once the **Chuffy** item is received, you can call the train to any open station.

		You must defeat **Old King Coal** to ride the train.
	"""
	display_name = "Shuffle Chuffy"

class ShuffleTrainStations(Toggle):
	"""
		Shuffle **Train Stations**. The switches that normally open the station will reward a shuffled item.
	"""
	display_name = "Shuffle Train Stations"

class ShuffleWorldOrder(Toggle):
	"""
		Shuffles the order that worlds unlock in. **Jiggywiggy Challenges** must be set to **Vanilla** or **Auto**.
	"""
	display_name = "Shuffle World Order"

class ShuffleWorldEntrances(Toggle):
	"""
		Shuffle the entrances to each world amongst themselves.
	"""
	display_name = "Shuffle World Entrances"

class ShuffleBossEntrances(Toggle):
	"""
		Shuffle the entrances to each boss amongst themselves.

		**Terry's** entrance from **inside** the mountain will remain vanilla.

		**Terry's** entrance from **outside** the mountain will be vanilla if you are solo Banjo. This is to allow you to **Taxi Pack** the last baby.
	"""
	display_name = "Shuffle Boss Entrances"

### Progressive Options ###

class ProgressiveEggs(Toggle):
	"""
		You will start with **Blue Eggs** and receive them in the following order:

		**Fire Eggs** -> **Grenade Eggs** -> **Ice Eggs** -> **Clockwork Kazooie Eggs**

		Requires shuffling **Banjo-Tooie** moves.
	"""
	display_name = "Progressive Eggs"

class ProgressiveAiming(Toggle):
	"""
		Enable the **Progressive Aiming** item.

		See the **Progressive Aiming List** option to see the order and select which items will be considered progressive.
	"""
	display_name = "Progressive Aiming"

class ProgressiveFlight(Toggle):
	"""
		Enable the **Progressive Flight** item.

		See the **Progressive Flight List** option to see the order and select which items will be considered progressive.
	"""
	display_name = "Progressive Flight"

class ProgressiveWaterTraining(Toggle):
	"""
		Enable the **Progressive Water Training** item.

		See the **Progressive Water Training List** option to see the order and select which items will be considered progressive.
	"""
	display_name = "Progressive Water Training"

class ProgressiveBeakBuster(Toggle):
	"""
		Enable the **Progressive Beak Buster** item. Requires shuffling moves from both **Banjo-Kazooie** and **Banjo-Tooie**.

		You will receive the following items in this order:

		**Beak Buster** -> **Bill Drill**
	"""
	display_name = "Progressive Beak Buster"

class ProgressiveBashAttack(Toggle):
	"""
		Enable the **Progressive Bash Attack** item. Requires shuffling **Stop 'n' Swop** and moves from **Banjo-Kazooie**.

		You will receive the following items in this order:

		**Ground Rat-a-tat Rap** -> **Breegull Bash**
	"""
	display_name = "Progressive Bash Attack"

class ProgressiveShoes(Toggle):
	"""
		Enable the **Progressive Shoes** item.

		See the **Progressive Shoes List** option to see the order and select which items will be considered progressive.
	"""
	display_name = "Progressive Shoes"

### Advanced Progressive Options ###

class ProgressiveAimingList(OptionSet):
	"""
		Specify which moves will be part of the **Progressive Aiming** item. Items not in this list can be received in any order.

		For items in the list, you will receive them in this order:

		**Third Person Egg Shooting** -> **Amaze-O-Gaze** -> **Egg Aim** -> **Breegull Blaster**

		Selected items must be shuffled to take part.
	"""
	display_name = "Progressive Aiming List"
	valid_keys = [
		"Third Person Egg Shooting",
		"Amaze-O-Gaze",
		"Egg Aim",
		"Breegull Blaster",
	]
	default = {
		"Third Person Egg Shooting",
		"Egg Aim",
	}

class ProgressiveFlightList(OptionSet):
	"""
		Specify which moves will be part of the **Progressive Flight** item. Items not in this list can be received in any order.

		For items in the list, you will receive them in this order:

		**Flight Pad** -> **Beak Bomb** -> **Airborne Egg Aiming**

		Selected items must be shuffled to take part.
	"""
	display_name = "Progressive Flight List"
	valid_keys = [
		"Flight Pad",
		"Beak Bomb",
		"Airborne Egg Aiming",
	]
	default = {
		"Flight Pad",
		"Beak Bomb",
		"Airborne Egg Aiming",
	}

class ProgressiveWaterTrainingList(OptionSet):
	"""
		Specify which moves will be part of the **Progressive Water Training** item. Items not in this list can be received in any order.

		For items in the list, you will receive them in this order:

		**Dive** -> **Sub-Aqua Egg Aiming** -> **Talon Torpedo** -> **Double Air** -> **Fast Swimming**

		Selected items must be shuffled to take part.
	"""
	display_name = "Progressive Water Training List"
	valid_keys = [
		"Dive",
		"Sub-Aqua Egg Aiming",
		"Talon Torpedo",
		"Double Air",
		"Fast Swimming",
	]
	default = {
		"Dive",
		"Double Air",
		"Fast Swimming",
	}

class ProgressiveShoesList(OptionSet):
	"""
		Specify which moves will be part of the **Progressive Shoes** item. Items not in this list can be received in any order.

		For items in the list, you will receive them in this order:

		**Stilt Stride** -> **Turbo Trainers** -> **Springy Step Shoes** -> **Claw Clamber Boots**

		Selected items must be shuffled to take part.
	"""
	display_name = "Progressive Shoes List"
	valid_keys = [
		"Stilt Stride",
		"Turbo Trainers",
		"Springy Step Shoes",
		"Claw Clamber Boots",
	]
	default = {
		"Stilt Stride",
		"Turbo Trainers",
		"Springy Step Shoes",
		"Claw Clamber Boots",
	}

### Speedup Options ###

class SkipKlungo(Toggle):
	"""
		You will be able to skip all 3 Klungo fights.
	"""
	display_name = "Skip Klungo"

class TowerOfTragedy(Choice):
	"""
		Choose how **Tower of Tragedy** begins.

		* **Full**: Tower of Tragedy begins as normal, and you must complete the full event to move on.
		* **Skip**: You won't have to take part in Tower of Tragedy at all, it begins as if you completed it.
		* **Round 3**: You will start at Round 3 in Tower of Tragedy. You vs Gruntilda!
	"""
	display_name = "Tower of Tragedy"
	option_full = 0
	option_skip = 1
	option_round_3 = 2

class SpeedupMinigames(Toggle):
	"""
		Start 3-round minigames at Round 3.
	"""
	display_name = "Speedup Minigames"

class OpenGIFrontDoor(Toggle):
	"""
		Opens the front door to **Grunty Industries**, allowing free access to the first floor.
	"""
	display_name = "Open GI Front Door"

class OpenBackDoors(Toggle):
	"""
		Opens many one-way switches, allowing backdoor access to levels.

		The following gates are always opened: MT -> TDL, MT -> HFP, GGM -> WW, WW -> TDL.

		For MT -> TDL, only the gate accessed from TDL's side is opened. For GGM -> WW, the boulders are still intact.

		The bridge in **Cliff Top** from HFP's entrance is extended to allow secondary access to **Cliff Top**.

		George has already cooled the pool in HFP to make HFP -> JRL more accessible.
	"""
	display_name = "Open Back Doors"

class EasyCanary(Toggle):
	"""
		The Canary Mary races will be 2 times easier.
	"""
	display_name = "Easy Canary"

### Hint Options ###

class SignHints(Range):
	"""
		Choose how many **? Signs** give a hint when read.

		The remaining signs will have a fun message.
	"""
	display_name = "Sign Hints"
	range_start = 0
	range_end = 61
	default = 0

class MoveHints(Range):
	"""
		Choose how many hints will be a move hint.

		The remaining hints will be for slow locations.

		Moves from **Banjo-Tooie** (and their silos) will not be hinted if they aren't shuffled.
	"""
	display_name = "Move Hints"
	range_start = 0
	range_end = 61
	default = 20

class HintClarity(Choice):
	"""
		Choose how clear hints will be.

		* **Cryptic**: Hints will only tell you how good the item is.
		* **Clear**: Hints will tell you what the item is.
	"""
	display_name = "Hint Clarity"
	option_cryptic = 0
	option_clear = 1
	default = 1

class AddHintsToArchipelago(Choice):
	"""
		Choose if the hint from a **? Sign** is added to the list of Archipelago hints upon reading the sign.

		This option only has an effect if **Sign Hints** is enabled.

		* **Never**: Hints are never added.
		* **Progression**: Hints are added only if the hinted location has a progression item.
		* **Always**: Hints are always added.
	"""
	display_name = "Add Hints To Archipelago"
	option_never = 0
	option_progression = 1
	option_always = 2
	default = 1

### Filler Options ###

class ReplaceExcessJiggies(Toggle):
	"""
		**Jiggies** over the required amount to beat the seed, plus a generous buffer, are replaced by fillers.
	"""
	display_name = "Replace Excess Jiggies"

class ReplaceExcessNoteNests(Toggle):
	"""
		**Note Nests** over the required amount to beat the seed, plus a generous buffer, are replaced by fillers.

		**Note Nests** must be shuffled.
	"""
	display_name = "Replace Excess Note Nests"

class ExtraJiggies(Range):
	"""
		Choose how many **Jiggies** are added to the pool.

		The actual amount added depends on your settings as extra **Jiggies** replace filler items.
	"""
	display_name = "Extra Jiggies"
	range_start = 0
	range_end = 100
	default = 0

class ExtraNoteNests(Range):
	"""
		Choose how many **Note Nests** are added to the pool.

		The actual amount added depends on your settings as extra **Note Nests** replace filler items.
	"""
	display_name = "Extra Note Nests"
	range_start = 0
	range_end = 100
	default = 0

class ExtraBassClefs(Range):
	"""
		Choose how many **Bass Clefs** are added to the pool.

		The actual amount added depends on your settings as extra **Bass Clefs** replace filler items.

		If **Replace Excess Note Nests** is enabled, **Base Clefs** will replace **Note Nests** (2 at a time) first.
	"""
	display_name = "Extra Bass Clefs"
	range_start = 0
	range_end = 100
	default = 0

class ExtraTrebleClefs(Range):
	"""
		Choose how many **Treble Clefs** are added to the pool.

		The actual amount added depends on your settings as extra **Treble Clefs** also replace filler items.

		If **Replace Excess Note Nests** is enabled, **Treble Clefs** will replace **Note Nests** (4 at a time) first.
	"""
	display_name = "Extra Treble Clefs"
	range_start = 0
	range_end = 100
	default = 0

class ExtraDoubloons(Range):
	"""
		Choose how many **Doubloons** are added to the pool.

		The actual amount added depends on your settings as extra **Doubloons** replace filler items.
	"""
	display_name = "Extra Doubloons"
	range_start = 0
	range_end = 100
	default = 0

class ExtraEmptyHoneycombs(Range):
	"""
		Choose how many **Empty Honeycombs** are added to the pool.

		The actual amount added depends on your settings as extra **Empty Honeycombs** replace filler items.
	"""
	display_name = "Extra Empty Honeycombs"
	range_start = 0
	range_end = 100
	default = 0

class ExtraCheatoPages(Range):
	"""
		Choose how many **Cheato Pages** are added to the pool.

		The actual amount added depends on your settings as extra **Cheato Pages** replace filler items.
	"""
	display_name = "Extra Cheato Pages"
	range_start = 0
	range_end = 100
	default = 0

class ExtraEggNests(Range):
	"""
		Choose how many **Egg Nests** are added to the pool.

		The actual amount added depends on your settings as extra **Egg Nests** replace filler items.
	"""
	display_name = "Extra Egg Nests"
	range_start = 0
	range_end = 100
	default = 0

class ExtraFeatherNests(Range):
	"""
		Choose how many **Feather Nests** are added to the pool.

		The actual amount added depends on your settings as extra **Feather Nests** replace filler items.
	"""
	display_name = "Extra Feather Nests"
	range_start = 0
	range_end = 100
	default = 0

### Trap Options ###

class TripTraps(Range):
	"""
		Choose how many **Trip Traps** are added to the pool.

		The actual amount added depends on your settings as **Trip Traps** replace filler items.
	"""
	display_name = "Trip Traps"
	range_start = 0
	range_end = 100
	default = 0

class SlipTraps(Range):
	"""
		Choose how many **Slip Traps** are added to the pool.

		The actual amount added depends on your settings as **Slip Traps** replace filler items.
	"""
	display_name = "Slip Traps"
	range_start = 0
	range_end = 100
	default = 0

class TipTraps(Range):
	"""
		Choose how many **Tip Traps** are added to the pool.

		The actual amount added depends on your settings as **Tip Traps** replace filler items.
	"""
	display_name = "Tip Traps"
	range_start = 0
	range_end = 100
	default = 0

class TransformTraps(Range):
	"""
		Choose how many **Transform Traps** are added to the pool.

		The actual amount added depends on your settings as **Transform Traps** replace filler items.
	"""
	display_name = "Transform Traps"
	range_start = 0
	range_end = 100
	default = 0

class GoldenEggNests(Range):
	"""
		Choose how many **Golden Egg Nests** are added to the pool.

		The actual amount added depends on your settings as **Golden Egg Nests** replace filler items.
	"""
	display_name = "Golden Egg Nests"
	range_start = 0
	range_end = 100
	default = 0

class SquishTraps(Range):
	"""
		Choose how many **Squish Traps** are added to the pool.

		The actual amount added depends on your settings as **Squish Traps** replace filler items.
	"""
	display_name = "Squish Traps"
	range_start = 0
	range_end = 100
	default = 0

### Miscellaneous Options ###

class JiggywiggysChallenges(Choice):
	"""
		Choose how **Jiggywiggy's Challenges** behave.

		* **Vanilla**: You must have enough **Jiggies** and complete the challenge to receive a world item.
		* **Auto**: Challenges are automatically completed once you have enough **Jiggies**
		* **Shuffled**: Once you have enough **Jiggies**, you can complete a challenge for a shuffled item.
		* **Auto Shuffled**: You will automatically receive a shuffled item once you have enough **Jiggies**.
	"""
	display_name = "Jiggywiggy's Challenges"
	option_vanilla = 0
	option_auto = 1
	option_shuffled = 2
	option_auto_shuffled = 3
	default = 1

class PresetJiggywiggyChallengeCosts(Choice):
	"""
		Overrides **Jiggywiggy's Challenge Costs** depending on the choice.

		Costs in challenge order:
		* **Cheap**: 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66
		* **Default**: 1, 4, 8, 14, 20, 28, 36, 45, 55, 70, 70
		* **Expensive**: 1, 8, 16, 25, 34, 43, 52, 61, 70, 80, 90
		* **Randomize**: Costs are randomized.
		* **Custom**: Specify the costs using the **Jiggywiggy Challenge Costs** option.
	"""
	display_name = "Preset Jiggywiggy Challenge Costs"
	option_cheap = 0
	option_default = 1
	option_expensive = 2
	option_randomize = 3
	option_custom = 4
	default = 1

class JiggywiggysChallengeCosts(OptionCounter):
	"""
		Choose how many **Jiggies** are required to complete **Jiggywiggy's Challenges**.

		The max value for each challenge is:

		* **Challenge  1**:  1
		* **Challenge  2**: 10
		* **Challenge  3**: 20
		* **Challenge  4**: 30
		* **Challenge  5**: 40
		* **Challenge  6**: 50
		* **Challenge  7**: 60
		* **Challenge  8**: 70
		* **Challenge  9**: 80
		* **Challenge 10**: 90
		* **Challenge 11**: 90
	"""
	display_name = "Jiggywiggy's Challenge Costs"
	valid_keys = [
		"Challenge 1",
		"Challenge 2",
		"Challenge 3",
		"Challenge 4",
		"Challenge 5",
		"Challenge 6",
		"Challenge 7",
		"Challenge 8",
		"Challenge 9",
		"Challenge 10",
		"Challenge 11",
	]
	default = {
		"Challenge 1": 1,
		"Challenge 2": 4,
		"Challenge 3": 8,
		"Challenge 4": 14,
		"Challenge 5": 20,
		"Challenge 6": 28,
		"Challenge 7": 36,
		"Challenge 8": 45,
		"Challenge 9": 55,
		"Challenge 10": 70,
		"Challenge 11": 70,
	}

class StartingEggs(OptionSet):
	"""
		Select possible starting eggs. One egg type from this list will be chosen at random to be your starting eggs.

		Defaults to **Blue Eggs** if moves from **Banjo-Tooie** are not shuffled or **Progressive Eggs** is enabled.
	"""
	display_name = "Starting Eggs"
	valid_keys: Iterable[str] = [
		"Blue Eggs",
		"Fire Eggs",
		"Grenade Eggs",
		"Ice Eggs",
		"Clockwork Kazooie Eggs",
	]
	default = {"Blue Eggs"}

class OpenWarpSilos(Range):
	"""
		Choose how many **Warp Silos** you start with.

		If you enable **Shuffle World Order**, **Warp Silos** leading you to your first world will be prioritized.
	"""
	display_name = "Open Warp Silos"
	range_start = 0
	range_end = 7
	default = 2

class MoveSiloCosts(Choice):
	"""
		Change the number of notes required to receive an item from **Jamjars' Move Silos**.

		Moves from **Banjo-Tooie** must be shuffled.
	"""
	display_name = "Move Silo Costs"
	option_vanilla = 0
	option_randomize = 1
	option_progressive = 2
	default = 0

class ExtraCheats(Toggle):
	"""
		The following cheats will be added to the CHEATS menu in game:

		* **NESTKING**: Infinite eggs/feathers.
		* **HONEYKING**: Infinite health/air.
		* **SUPERBANJO**: Gotta go fast!
		* **SUPERBADDY**: They gotta go fast!
	"""
	display_name = "Extra Cheats"

class AutoEnableCheats(OptionSet):
	"""
		Specify which cheats to automatically enable once received.
	"""
	display_name = "Auto Enable Cheats"
	valid_keys = [
		"Feathers",
		"Eggs",
		"Fallproof",
		"Honeyback",
		"Homing Eggs",
	]
	default: set[str] = set()

class DialogCharacter(OptionSet):
	"""
		Choose which character(s) will be used for Archipelago related messages.

		If multiple are selected, they will be randomly selected for each message.

		If none are selected, a character will be chosen based on the context of the message.

		If the special entry "**ALL**" is selected, all characters will be randomly selected for each message.
	"""
	display_name = "Dialog Character"
	valid_keys: Iterable[str] = {
		"ALL",
		"GLOWBO",
		"JIGGY",
		"HONEYCOMB",
		"SUB",
		"WASHER",
		"BANJO",
		"KAZOOIE",
		"BOTTLES",
		"MUMBO",
		"JINJO_YELLOW",
		"JINJO_GREEN",
		"JINJO_BLUE",
		"JINJO_PURPLE",
		"JINJO_ORANGE",
		"BEEHIVE",
		"GRUNTY",
		"ZUBBA",
		"JAMJARS",
		"BOVINA",
		"MINJO_WHITE",
		"MINJO_ORANGE",
		"MINJO_YELLOW",
		"MINJO_BROWN",
		"UNOGOPAZ",
		"CHIEF_BLOATAZIN",
		"DILBERTA",
		"STONIES1",
		"CANARY_MARY",
		"CHEATO",
		"GOBI",
		"DINO_KID1",
		"MR_PATCH",
		"MOGGY",
		"SOGGY",
		"GROGGY",
		"MRS_BOGGY",
		"PROSPECTOR",
		"HUMBA",
		"UFO",
		"OLD_KING_COAL",
		"SSSLUMBER",
		"BOGGY",
		"BIG_AL",
		"SALTY_JOE",
		"CONGA",
		"PAWNO",
		"TIPTUP",
		"JOLLY",
		"MERRY_MAGGIE",
		"TERRY",
		"BARGASAURUS",
		"YELLOW_STONY",
		"ALIEN",
		"CHRIS_P_BACON",
		"CAPTAIN_BLUBBER",
		"STYRACOSAURUS_MOM",
		"ROYSTEN",
		"SAFE",
		"GUFFO",
		"MR_FIT",
		"CAPTAIN_BLACKEYE",
		"JINJO_RED",
		"JINJO_WHITE",
		"JINJO_BLACK",
		"JINJO_BROWN",
		"CHILLY_WILLY",
		"CHILLI_BILLI",
		"MINGY_JONGO",
		"YELLOW_DODGEM",
		"MINGELLA",
		"BLOBBELDA",
		"KLUNGO",
		"BOTTLES_DEAD",
		"MINJO_GREEN",
		"MINJO_RED",
		"MINJO_BLUE",
		"MINJO_PURPLE",
		"MINJO_BLACK",
		"RABBIT_WORKER1",
		"UNGA_BUNGA",
		"JIGGYWIGGY",
		"JIGGYWIGGY_DISCIPLE",
		"HONEY_B",
		"BANJO_KAZOOIE",
		"PIG1",
		"OOGLE_BOOGLE",
		"GI_ANNOUNCER",
		"DINGPOT",
		"KING_JINGALING_DEAD",
		"ROCKNUT",
		"MILDRED",
		"BIGGA_FOOT",
		"GEORGE",
		"SABREMAN",
		"DIPPY",
		"LOGGO",
		"KING_JINGALING",
		"MRS_BOTTLES",
		"SPECCY",
		"GOGGLES",
		"TARGITZAN",
		"CHOMPA",
		"LORD_WOO_FAK_FAK",
		"WELDAR",
		"ALIEN_CHILD",
		"EVIL_BOTTLES",
		"DINO_KID2",
		"DINO_SCRIT_SMALL",
		"DINO_SCRIT_BIG",
		"HEGGY",
	}
	default: set[str] = set()

class ChosenGoals(OptionSet):
	"""
		Hidden option. Used internally.
		Holds which goals were chosen to be required.
	"""
	display_name = "Chosen Goals"
	visibility = Visibility.none
	valid_keys = VictoryGoals.valid_keys
	default = {}

class ChosenEggs(Choice):
	"""
		Hidden option. Used internally.
		Holds which startings eggs were chosen.
	"""
	display_name = "Chosen Eggs"
	visibility = Visibility.none
	option_blue_eggs = 0
	option_fire_eggs = 1
	option_grenade_eggs = 2
	option_ice_eggs = 3
	option_clockwork_kazooie_eggs = 4
	default = 0

class ChosenMoveSiloCosts(OptionCounter):
	"""
		Hidden option. Used internally.
		Holds the chosen costs for move silos.
	"""
	display_name = "Chosen Move Silo Costs"
	visibility = Visibility.none
	valid_keys = [
		"Fire Eggs",
		"Grenade Eggs",
		"Ice Eggs",
		"Clockwork Kazooie Eggs",
		"Egg Aim",
		"Breegull Blaster",
		"Grip Grab",
		"Bill Drill",
		"Beak Bayonet",
		"Split Up",
		"Pack Whack",
		"Airborne Egg Aiming",
		"Wing Whack",
		"Sub Aqua Egg Aiming",
		"Talon Torpedo",
		"Springy Step Shoes",
		"Taxi Pack",
		"Hatch",
		"Claw Clamber Boots",
		"Snooze Pack",
		"Leg Spring",
		"Shack Pack",
		"Glide",
		"Sack Pack",
	]
	default = {
		"Fire Eggs": 45,
		"Grenade Eggs": 110,
		"Ice Eggs": 200,
		"Clockwork Kazooie Eggs": 315,
		"Egg Aim": 25,
		"Breegull Blaster": 30,
		"Grip Grab": 35,
		"Bill Drill": 85,
		"Beak Bayonet": 95,
		"Split Up": 160,
		"Pack Whack": 170,
		"Airborne Egg Aiming": 180,
		"Wing Whack": 265,
		"Sub Aqua Egg Aiming": 275,
		"Talon Torpedo": 290,
		"Springy Step Shoes": 390,
		"Taxi Pack": 405,
		"Hatch": 420,
		"Claw Clamber Boots": 505,
		"Snooze Pack": 525,
		"Leg Spring": 545,
		"Shack Pack": 640,
		"Glide": 660,
		"Sack Pack": 765,
	}

groups: list[OptionGroup] = [
	OptionGroup("Game Options", [
		ProgressionBalancing,
		Accessibility,
		DeathLink,
		TagLink,
	]),
	OptionGroup("Victory Options", [
		PresetVictoryGoals,
		VictoryGoals,
		ExtraMumboTokens,
		MaxMumboTokens,
		ReplaceExcessMumboTokens,
		OpenHAG1,
	]),
	OptionGroup("Logic Options", [
		PresetLogicTricks,
		LogicTricks,
		InstantTransform,
	]),
	OptionGroup("Shuffle Options", [
		ShuffleBKMoves,
		ShuffleBTMoves,
		ShuffleGlowbos,
		ShuffleJinjos,
		ShuffleTrebleClefs,
		ShuffleNoteNests,
		ShuffleHoneycombs,
		ShuffleHoneyBRewards,
		ShuffleCheatoPages,
		ShuffleCheatoRewards,
		ShuffleStopNSwop,
		ShuffleDoubloons,
		ShuffleGreenRelics,
		ShuffleBigTopTickets,
		ShuffleBeans,
		ShuffleWarpSilos,
		ShuffleWarpPads,
		ShuffleSigns,
		ShuffleJiggywiggysSuperSpecialChallenge,
		ShuffleNests,
		ShuffleChuffy,
		ShuffleTrainStations,
		ShuffleWorldOrder,
		ShuffleWorldEntrances,
		ShuffleBossEntrances,
	]),
	OptionGroup("Progressive Options", [
		ProgressiveEggs,
		ProgressiveAiming,
		ProgressiveFlight,
		ProgressiveWaterTraining,
		ProgressiveBeakBuster,
		ProgressiveBashAttack,
		ProgressiveShoes,
	]),
	OptionGroup("Advanced Progressive Options", [
		ProgressiveAimingList,
		ProgressiveFlightList,
		ProgressiveWaterTrainingList,
		ProgressiveShoesList,
	], True),
	OptionGroup("Speedup Options", [
		SkipKlungo,
		TowerOfTragedy,
		SpeedupMinigames,
		OpenGIFrontDoor,
		OpenBackDoors,
		EasyCanary,
	]),
	OptionGroup("Hint Options", [
		SignHints,
		MoveHints,
		HintClarity,
		AddHintsToArchipelago,
	]),
	OptionGroup("Filler Options", [
		ReplaceExcessJiggies,
		ReplaceExcessNoteNests,
		ExtraJiggies,
		ExtraNoteNests,
		ExtraBassClefs,
		ExtraTrebleClefs,
		ExtraDoubloons,
		ExtraEmptyHoneycombs,
		ExtraCheatoPages,
		ExtraEggNests,
		ExtraFeatherNests,
	], True),
	OptionGroup("Trap Options", [
		TripTraps,
		SlipTraps,
		TipTraps,
		TransformTraps,
		GoldenEggNests,
		SquishTraps,
	], True),
	OptionGroup("Miscellaneous Options", [
		JiggywiggysChallenges,
		PresetJiggywiggyChallengeCosts,
		JiggywiggysChallengeCosts,
		StartingEggs,
		OpenWarpSilos,
		MoveSiloCosts,
		ExtraCheats,
		AutoEnableCheats,
		DialogCharacter,
	]),
]

@dataclass
class BanjoTooieOptionsList:
	"""
		Options listed in this class are sent to the game.
	"""

	# Common Options
	death_link: DeathLink
	tag_link: TagLink

	# Victory Options
	preset_victory_goals: PresetVictoryGoals
	victory_goals: VictoryGoals
	extra_mumbo_tokens: ExtraMumboTokens
	max_mumbo_tokens: MaxMumboTokens
	replace_excess_mumbo_tokens: ReplaceExcessMumboTokens
	open_hag1: OpenHAG1

	# Logic Options
	preset_logic_tricks: PresetLogicTricks
	logic_tricks: LogicTricks
	instant_transform: InstantTransform

	# Shuffle Options
	shuffle_bk_moves: ShuffleBKMoves
	shuffle_bt_moves: ShuffleBTMoves
	shuffle_glowbos: ShuffleGlowbos
	shuffle_jinjos: ShuffleJinjos
	shuffle_treble_clefs: ShuffleTrebleClefs
	shuffle_note_nests: ShuffleNoteNests
	shuffle_honeycombs: ShuffleHoneycombs
	shuffle_honeyb_rewards: ShuffleHoneyBRewards
	shuffle_cheato_pages: ShuffleCheatoPages
	shuffle_cheato_rewards: ShuffleCheatoRewards
	shuffle_stop_n_swop: ShuffleStopNSwop
	shuffle_doubloons: ShuffleDoubloons
	shuffle_green_relics: ShuffleGreenRelics
	shuffle_big_top_tickets: ShuffleBigTopTickets
	shuffle_beans: ShuffleBeans
	shuffle_warp_silos: ShuffleWarpSilos
	shuffle_warp_pads: ShuffleWarpPads
	shuffle_signs: ShuffleSigns
	shuffle_jiggywiggys_super_special_challenge: ShuffleJiggywiggysSuperSpecialChallenge
	shuffle_nests: ShuffleNests
	shuffle_chuffy: ShuffleChuffy
	shuffle_train_stations: ShuffleTrainStations
	shuffle_world_order: ShuffleWorldOrder
	shuffle_world_entrances: ShuffleWorldEntrances
	shuffle_boss_entrances: ShuffleBossEntrances

	# Progressive Options
	progressive_eggs: ProgressiveEggs
	progressive_aiming: ProgressiveAiming
	progressive_flight: ProgressiveFlight
	progressive_water_training: ProgressiveWaterTraining
	progressive_beak_buster: ProgressiveBeakBuster
	progressive_bash_attack: ProgressiveBashAttack
	progressive_shoes: ProgressiveShoes

	# Advanced Progressive Options
	progressive_aiming_list: ProgressiveAimingList
	progressive_flight_list: ProgressiveFlightList
	progressive_water_training_list: ProgressiveWaterTrainingList
	progressive_shoes_list: ProgressiveShoesList

	# Speedup Options
	skip_klungo: SkipKlungo
	tower_of_tragedy: TowerOfTragedy
	speedup_minigames: SpeedupMinigames
	open_gi_front_door: OpenGIFrontDoor
	open_back_doors: OpenBackDoors
	easy_canary: EasyCanary

	# Hint Options
	sign_hints: SignHints
	move_hints: MoveHints
	hint_clarity: HintClarity
	add_hints_to_archipelago: AddHintsToArchipelago

	# Filler Options
	replace_excess_jiggies: ReplaceExcessJiggies
	replace_excess_note_nests: ReplaceExcessNoteNests
	extra_jiggies: ExtraJiggies
	extra_note_nests: ExtraNoteNests
	extra_bass_clefs: ExtraBassClefs
	extra_treble_clefs: ExtraTrebleClefs
	extra_doubloons: ExtraDoubloons
	extra_empty_honeycombs: ExtraEmptyHoneycombs
	extra_cheato_pages: ExtraCheatoPages
	extra_egg_nests: ExtraEggNests
	extra_feather_nests: ExtraFeatherNests

	# Trap Options
	trip_traps: TripTraps
	slip_traps: SlipTraps
	tip_traps: TipTraps
	transform_traps: TransformTraps
	golden_egg_nests: GoldenEggNests
	squish_traps: SquishTraps

	# Miscellaneous Options
	jiggywiggys_challenges: JiggywiggysChallenges
	preset_jiggywiggys_challenge_costs: PresetJiggywiggyChallengeCosts
	jiggywiggys_challenge_costs: JiggywiggysChallengeCosts
	starting_eggs: StartingEggs
	open_warp_silos: OpenWarpSilos
	move_silo_costs: MoveSiloCosts
	extra_cheats: ExtraCheats
	auto_enable_cheats: AutoEnableCheats
	dialog_character: DialogCharacter

	# Hidden/Internal Options
	chosen_goals: ChosenGoals
	chosen_eggs: ChosenEggs
	chosen_move_silo_costs: ChosenMoveSiloCosts

@dataclass
class BanjoTooieOptions(BanjoTooieOptionsList, PerGameCommonOptions):
	start_inventory_from_pool: StartInventoryPool
