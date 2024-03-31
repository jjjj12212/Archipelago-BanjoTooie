from dataclasses import dataclass
from Options import Toggle, DeathLink, PerGameCommonOptions, Choice, DefaultOnToggle

class EnableMultiWorldMoveList(DefaultOnToggle):
    """Jamjars' Movelist is locked between the MultiWorld. Other players need to unlock Banjo's Moves."""
    display_name = "Jamjars' Movelist"

class EnableMultiWorldJinjos(Toggle):
    """Jinjos fled to other worlds. Other players need return them home."""
    display_name = "Randomize Jinjos"

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

class KingJingalingHasJiggy(Toggle):
    """King Jingaling will always have a Jiggy to give you."""
    display_name = "King Jingaling Jiggy"

class SkipPuzzles(Toggle):
    """Open world entrances without having to go to Jiggywiggy."""
    display_name = "Skip Puzzles"

class OpenHag1(Toggle):
    """HAG 1 boss fight is opened when Cauldron Keep is. Only 55 jiggies are needed to win."""
    display_name = "HAG 1 Open"

class SkipToT(Choice):
    """Choose whether to play the full quiz, start at round 3, or skip it."""
    display_name = "Tower of Tragedy Quiz"
    option_full = 0
    option_skip = 1
    option_round_3 = 2
    default = 1

class SpeedUpMinigames(DefaultOnToggle):
    """Start 3-round minigames at Round 3"""
    display_name = "Speed Up Minigames"


@dataclass
class BanjoTooieOptions(PerGameCommonOptions):
    death_link: DeathLink
    randomize_moves: EnableMultiWorldMoveList
    randomize_jinjos: EnableMultiWorldJinjos
    randomize_doubloons: EnableMultiWorldDoubloons
    randomize_cheato: EnableMultiWorldCheatoPages
    cheato_as_filler: SetMultiWorldCheatoPagesFiller
    randomize_honeycombs: EnableMultiWorldHoneycombs
    randomize_glowbos: EnableMultiWorldGlowbos
    randomize_treble: EnableMultiWorldTrebleClefs
    randomize_stations: EnableMultiWorldTrainStationSwitches
    randomize_chuffy: EnableMultiWorldChuffyTrain
    jingaling_jiggy: KingJingalingHasJiggy
    skip_puzzles: SkipPuzzles
    open_hag1: OpenHag1
    skip_tower_of_tragedy: SkipToT
    speed_up_minigames: SpeedUpMinigames
    
