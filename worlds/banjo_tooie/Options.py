from dataclasses import dataclass
from Options import Toggle, DeathLink, PerGameCommonOptions, Choice, DefaultOnToggle, Range

class EnableMultiWorldMoveList(DefaultOnToggle):
    """Jamjars' Movelist is locked between the MultiWorld. Other players need to unlock Banjo's Moves."""
    display_name = "Jamjars' Movelist"

class EnableMultiWorldBKMoveList(Choice):
    """Banjo-Kazooie Movelist is locked between the MultiWorld. Other players need to unlock Banjo's Moves.
    Mcjiggy Special - No Talon Trot and Tall Jump in the Pool """
    display_name = "BK Original Movelist"
    option_none = 0
    option_mcjiggy_special = 1
    option_all = 2
    default = 0

class EnableCheatoRewards(DefaultOnToggle):
    """Cheato rewards you a cheat + an additional randomized reward. Use Cheato Pages as Filler cannot be set if this is enabled."""
    display_name = "Cheato Rewards"

class DisableOverlayText(Toggle):
    """Disables the overlay text on screen. Useful if your already streaming/viewing the BT_Client."""
    display_name = "Disable Overlay Text"

class EnableMultiWorldJinjos(DefaultOnToggle):
    """Jinjos fled to other worlds. Other players need return them home."""
    display_name = "Randomize Jinjos"

class ForbidMovesOnJinjoFamilyTreasure(Choice):
    """If Jinjos are randomized, do not allow unlockable moves or magic behind Jinjo Families."""
    display_name = "Forbid Unlockable Moves or Magic on Jinjo Family Treasure"
    option_none = 0
    option_moves_only = 1
    option_moves_and_magic = 2
    option_magic_only = 3
    default = 1

class ForbidJinjosOnJinjoFamilyTreasure(Toggle):
    """If Jinjos are randomized, do not allow other colour Jinjos behind Jinjo Families."""
    display_name = "Forbid Jinjos on Jinjo Family Treasure"

class EnableMultiWorldDoubloons(Toggle):
    """Jolly Roger's Doubloons are scattered across the MultiWorld."""
    display_name = "Randomize Doubloons"

class EnableMultiWorldCheatoPages(DefaultOnToggle):
    """Cheato pages are scattered across the MultiWorld."""
    display_name = "Randomize Cheato Pages"

class SetMultiWorldCheatoPagesFiller(Toggle):
    """If Cheato pages are scattered, set to Cheato Items as filler."""
    display_name = "Use Cheato Pages as Filler."

class EnableMultiWorldHoneycombs(DefaultOnToggle):
    """Honeycombs are scattered across the MultiWorld."""
    display_name = "Randomize Honeycombs"

class EnableHoneyBRewards(DefaultOnToggle):
    """Honey B gives you health + a additiona randomized reward"""
    display_name = "Honey B Rewards"

class EnableMultiWorldGlowbos(DefaultOnToggle):
    """Glowbos are scattered across the MultiWorld."""
    display_name = "Randomize Glowbos"

class EnableMultiWorldTrebleClefs(DefaultOnToggle):
    """Treble Clefs are scattered across the MultiWorld."""
    display_name = "Randomize Treble Clefs"

class EnableMultiWorldTrainStationSwitches(Toggle):
    """Train Stations are scattered across the MultiWorld."""
    display_name = "Randomize Train Station Switches"

class EnableMultiWorldChuffyTrain(Toggle):
    """Chuffy is lost across the MultiWorld."""
    display_name = "Chuffy as a randomized AP Item."

class EnableMultiWorldNotes(Toggle):
    """Note Nests are scattered across the MultiWorld."""
    display_name = "Randomize Note Nests"

class KingJingalingHasJiggy(DefaultOnToggle):
    """King Jingaling will always have a Jiggy to give you."""
    display_name = "King Jingaling Jiggy"

class SkipPuzzles(DefaultOnToggle):
    """Open world entrances without having to go to Jiggywiggy."""
    display_name = "Skip Puzzles"

class OpenHag1(DefaultOnToggle):
    """HAG 1 boss fight is opened when Cauldron Keep is. Only 55 jiggies are needed to win."""
    display_name = "HAG 1 Open"

class RandomizeWorlds(Toggle):
    """Worlds will open in a randomized order. Randomized Moves & Puzzle Skip Required."""
    display_name = "Randomize Worlds"

class RandomizeStopnSwap(Toggle):
    """Mystery Eggs (and rewards) and Ice Key are scattered across the MultiWorld."""
    display_name = "Randomize Stop n Swap"

class SkipToT(Choice):
    """Choose whether to play the full quiz, start at round 3, or skip it."""
    display_name = "Tower of Tragedy Quiz"
    option_full = 0
    option_skip = 1
    option_round_3 = 2
    default = 1

class LogicType(Choice):
    """Choose your logic difficulty if you are expected to perform tricks to reach certian areas."""
    display_name = "Logic Type"
    option_beginner = 0
    option_normal = 1
    option_advanced = 2
    option_glitched = 3
    default = 0

class SpeedUpMinigames(DefaultOnToggle):
    """Start 3-round minigames at Round 3"""
    display_name = "Speed Up Minigames"

class VictoryCondition(Choice):
    """Choose which victory condition you want
    HAG1: Unlock the HAG1 fight and defeat Gruntilda
    Minigame Hunt: Clear the 14 minigames and the final Canary Mary race in Cloud Cuckcoo Land to collect Mumbo Tokens
    Boss Hunt: Kill the 8 world bosses and collect their Mumbo Tokens
    Jinjo Family Rescue: Rescue Jinjo Families to collect their prized Mumbo Tokens
    Wonderwing Challenge: Collect all 32 Mumbo Tokens across all boss fights, mini games and every Jinjo family
        to gain access to HAG1 and Defeat Grunty. The Ultimate Banjo Tooie experience!
    Token Hunt: Mumbo's Tokens are scattered around the world. Help him find them"""
    display_name = "Victory Condition"
    option_hag1 = 0
    option_minigame_hunt = 1
    option_boss_hunt = 2
    option_jinjo_family_rescue = 3
    option_wonder_wing_challenge = 4
    option_token_hunt = 5
    default = 0

class MinigameHuntLength(Range):
    """How many Mumbo Tokens are needed to clear the Minigame Hunt
    Choose a value between 1 and 15"""
    display_name = "Minigame Hunt Length"
    range_start = 1
    range_end = 15
    default = 14

class BossHuntLength(Range):
    """How many Mumbo Tokens are needed to clear the Boss Hunt
    Choose a value between 1 and 8"""
    display_name = "Boss Hunt Length"
    range_start = 1
    range_end = 8
    default = 8

class JinjoFamilyRescueLength(Range):
    """How many Jinjo families' Mumbo Tokens are needed to clear the Jinjo family rescue
    Choose a value between 1 and 9"""
    display_name = "Jinjo Family Rescue Length"
    range_start = 1
    range_end = 9
    default = 9

class TokenHuntLength(Range):
    """How many Mumbo Tokens of the 25 hidden throughout the world do you need to find
    Choose a value between 1 and 20"""
    display_name = "Token Hunt Length"
    range_start = 1
    range_end = 15
    default = 5

# class WarpTraps(Choice):
#     """Choose if you want warp traps enabled"""
#     display_name = "Warp Traps"
#     option_no_warp_traps = 0
#     option_in_level_warp_traps = 1
#     option_cross_level_warp_traps = 2
#     default = 0

class GameLength(Choice):
    """Choose how quickly the worlds open between each over."""
    display_name = "World Requirements"
    option_quick = 0  #1,3,6,10,15,21,28,36,44 
    option_normal = 1 #1,4,8,14,20,28,36,45,55
    option_long = 2   #1,8,16,25,34,43,52,61,70
    option_custom = 3 #you pick
    default = 1

class World1(Range):
    """If you picked custom, what is the jiggy requirement for World 1."""
    display_name = "World 1 Jiggy requirement"
    range_start = 1
    range_end = 3
    default = 1

class World2(Range):
    """If you picked custom, what is the jiggy requirement for World 2."""
    display_name = "World 2 Jiggy requirement"
    range_start = 2
    range_end = 20
    default = 4

class World3(Range):
    """If you picked custom, what is the jiggy requirement for World 3."""
    display_name = "World 3 Jiggy requirement"
    range_start = 3
    range_end = 30
    default = 8

class World4(Range):
    """If you picked custom, what is the jiggy requirement for World 4."""
    display_name = "World 4 Jiggy requirement"
    range_start = 4
    range_end = 40
    default = 14

class World5(Range):
    """If you picked custom, what is the jiggy requirement for World 5."""
    display_name = "World 5 Jiggy requirement"
    range_start = 5
    range_end = 50
    default = 20

class World6(Range):
    """If you picked custom, what is the jiggy requirement for World 6."""
    display_name = "World 6 Jiggy requirement"
    range_start = 6
    range_end = 60
    default = 28

class World7(Range):
    """If you picked custom, what is the jiggy requirement for World 7."""
    display_name = "World 7 Jiggy requirement"
    range_start = 7
    range_end = 70
    default = 36

class World8(Range):
    """If you picked custom, what is the jiggy requirement for World 8."""
    display_name = "World 8 Jiggy requirement"
    range_start = 8
    range_end = 90
    default = 45

class World9(Range):
    """If you picked custom, what is the jiggy requirement for Cauldon Keep."""
    display_name = "Cauldon Keep Jiggy requirement"
    range_start = 9
    range_end = 90
    default = 55

class SkipKlungo(Toggle):
    """Make it so you can skip Klungo 1 and 2."""
    display_name = "Skip Klungo"

class ExceedingItemsFiller(Toggle):
    """Progressive Items that exceeds the required amounts are marked as junk"""
    display_name = "Exceeding Progressive Items marked as junk items"

@dataclass
class BanjoTooieOptions(PerGameCommonOptions):
    death_link: DeathLink
    disable_overlay_text:DisableOverlayText
    randomize_moves: EnableMultiWorldMoveList
    randomize_bk_moves: EnableMultiWorldBKMoveList
    randomize_jinjos: EnableMultiWorldJinjos
    forbid_on_jinjo_family: ForbidMovesOnJinjoFamilyTreasure
    forbid_jinjos_on_jinjo_family: ForbidJinjosOnJinjoFamilyTreasure
    randomize_doubloons: EnableMultiWorldDoubloons
    randomize_cheato: EnableMultiWorldCheatoPages
    cheato_rewards: EnableCheatoRewards
    cheato_as_filler: SetMultiWorldCheatoPagesFiller
    exceeding_items_filler: ExceedingItemsFiller
    randomize_honeycombs: EnableMultiWorldHoneycombs
    honeyb_rewards: EnableHoneyBRewards
    randomize_glowbos: EnableMultiWorldGlowbos
    randomize_treble: EnableMultiWorldTrebleClefs
    randomize_stations: EnableMultiWorldTrainStationSwitches
    randomize_chuffy: EnableMultiWorldChuffyTrain
    randomize_notes: EnableMultiWorldNotes
    randomize_stop_n_swap: RandomizeStopnSwap
    jingaling_jiggy: KingJingalingHasJiggy
    skip_puzzles: SkipPuzzles
    skip_klungo: SkipKlungo
    skip_tower_of_tragedy: SkipToT
    speed_up_minigames: SpeedUpMinigames
    logic_type: LogicType
    victory_condition: VictoryCondition
    minigame_hunt_length: MinigameHuntLength
    boss_hunt_length: BossHuntLength
    jinjo_family_rescue_length: JinjoFamilyRescueLength
    token_hunt_length: TokenHuntLength
    randomize_worlds: RandomizeWorlds
    game_length: GameLength
    open_hag1: OpenHag1
    world_1: World1
    world_2: World2
    world_3: World3
    world_4: World4
    world_5: World5
    world_6: World6
    world_7: World7
    world_8: World8
    world_9: World9
    # warp_traps: WarpTraps
