from dataclasses import dataclass
from Options import Toggle, DeathLink, PerGameCommonOptions, Choice

class EnableMultiWorldMoveList(Toggle):
    """Banjo Kazooie's Movelist is locked between the MultiWorld. Other players need to unlock Banjo's Moves."""
    display_name = "Banjo Kazooie Movelist"

class EnableMultiWorldJinjos(Toggle):
    """Jinjos fled to other worlds. Other players need return them home."""
    display_name = "MultiWorld Jinjos"

class EnableMultiWorldDoubloons(Toggle):
    """Jolly Roger's Doubloons are scattered across the MultiWorld."""
    display_name = "MultiWorld Doubloons"

class EnableMultiWorldCheatoPages(Toggle):
    """Cheato pages are scattered across the MultiWorld."""
    display_name = "MultiWorld Cheato Pages"

class SetMultiWorldCheatoPagesFiller(Toggle):
    """If Cheato pages are scattered, set to Cheato Items as filler."""
    display_name = "Use Cheato Pages as Filler."

class EnableMultiWorldHoneycombs(Toggle):
    """Honeycombs are scattered across the MultiWorld."""
    display_name = "MultiWorld Honeycombs"

class EnableMultiWorldGlowbos(Toggle):
    """Glowbos are scattered across the MultiWorld."""
    display_name = "MultiWorld Glowbos"

class KingJingalingHasJiggy(Toggle):
    """King Jingaling will always have a Jiggy to give you."""
    display_name = "King Jingaling Jiggy"

class SkipToT(Choice):
    """Choose whether to play the full quiz, start at round 3, or skip it."""
    display_name = "Tower of Tragedy Quiz"
    option_full = 0
    option_skip = 1
    option_round_3 = 2
    default = 1

class SpeedUpMinigames(Toggle):
    """Start 3-round minigames at Round 3"""
    display_name = "Speed Up Minigames"

class EnableMultiWorldTrebleClefs(Toggle):
    """Treble Clefs are scattered across the MultiWorld."""
    display_name = "MultiWorld Treble Clefs"

@dataclass
class BanjoTooieOptions(PerGameCommonOptions):
    death_link: DeathLink
    multiworld_moves: EnableMultiWorldMoveList
    multiworld_jinjos: EnableMultiWorldJinjos
    multiworld_doubloons: EnableMultiWorldDoubloons
    multiworld_cheato: EnableMultiWorldCheatoPages
    cheato_as_filler: SetMultiWorldCheatoPagesFiller
    multiworld_honeycombs: EnableMultiWorldHoneycombs
    multiworld_glowbos: EnableMultiWorldGlowbos
    jingaling_jiggy: KingJingalingHasJiggy
    skip_tower_of_tragedy: SkipToT
    speed_up_minigames: SpeedUpMinigames
    multiworld_treble: EnableMultiWorldTrebleClefs
