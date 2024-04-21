from dataclasses import dataclass
from Options import Toggle, DeathLink, PerGameCommonOptions, Choice, DefaultOnToggle

class EnableMultiWorldMoveList(DefaultOnToggle):
    """Jamjars' Movelist is locked between the MultiWorld. Other players need to unlock Banjo's Moves."""
    display_name = "Jamjars' Movelist"

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

class EnableMultiWorldCheatoPages(Toggle):
    """Cheato pages are scattered across the MultiWorld."""
    display_name = "Randomize Cheato Pages"

class SetMultiWorldCheatoPagesFiller(Toggle):
    """If Cheato pages are scattered, set to Cheato Items as filler."""
    display_name = "Use Cheato Pages as Filler."

class EnableMultiWorldHoneycombs(DefaultOnToggle):
    """Honeycombs are scattered across the MultiWorld."""
    display_name = "Randomize Honeycombs"

class EnableMultiWorldGlowbos(DefaultOnToggle):
    """Glowbos are scattered across the MultiWorld."""
    display_name = "Randomize Glowbos"

class EnableMultiWorldTrebleClefs(Toggle):
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

class KingJingalingHasJiggy(Toggle):
    """King Jingaling will always have a Jiggy to give you."""
    display_name = "King Jingaling Jiggy"

class SkipPuzzles(Toggle):
    """Open world entrances without having to go to Jiggywiggy."""
    display_name = "Skip Puzzles"

class OpenHag1(Toggle):
    """HAG 1 boss fight is opened when Cauldron Keep is. Only 55 jiggies are needed to win."""
    display_name = "HAG 1 Open"

class RandomizeWorlds(Toggle):
    """Worlds will open in a randomized order. Randomized Moves & Puzzle Skip Required."""
    display_name = "Randomize Worlds"

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
    default = 0

class SpeedUpMinigames(DefaultOnToggle):
    """Start 3-round minigames at Round 3"""
    display_name = "Speed Up Minigames"

class VictoryCondition(Choice):
    """Choose your whether your victory condition is defeating HAG 1 or completing all 14 scored Mini Games Plus CCL Canary Mary. Requires filler items."""
    display_name = "Victory Condition"
    option_hag1 = 0
    option_minigame_hunt = 1
    default = 0

@dataclass
class BanjoTooieOptions(PerGameCommonOptions):
    death_link: DeathLink
    randomize_moves: EnableMultiWorldMoveList
    randomize_jinjos: EnableMultiWorldJinjos
    forbid_on_jinjo_family: ForbidMovesOnJinjoFamilyTreasure
    forbid_jinjos_on_jinjo_family: ForbidJinjosOnJinjoFamilyTreasure
    randomize_doubloons: EnableMultiWorldDoubloons
    randomize_cheato: EnableMultiWorldCheatoPages
    cheato_as_filler: SetMultiWorldCheatoPagesFiller
    randomize_honeycombs: EnableMultiWorldHoneycombs
    randomize_glowbos: EnableMultiWorldGlowbos
    randomize_treble: EnableMultiWorldTrebleClefs
    randomize_stations: EnableMultiWorldTrainStationSwitches
    randomize_chuffy: EnableMultiWorldChuffyTrain
    randomize_notes: EnableMultiWorldNotes
    jingaling_jiggy: KingJingalingHasJiggy
    skip_puzzles: SkipPuzzles
    open_hag1: OpenHag1
    randomize_worlds: RandomizeWorlds
    skip_tower_of_tragedy: SkipToT
    speed_up_minigames: SpeedUpMinigames
    logic_type: LogicType
    victory_condition: VictoryCondition