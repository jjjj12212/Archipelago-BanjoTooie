from dataclasses import dataclass
from Options import Toggle, DeathLink, PerGameCommonOptions

class EnableMultiWorldMoveList(Toggle):
    """Banjo Kazooie's Movelist is locked between the MultiWorld. Other players need to unlock Banjo's Moves."""
    display_name = "Banjo Kazooie Movelist"

class EnableMultiWorldJinjos(Toggle):
    """Jinjos fled to other worlds. Other players need return them home."""
    display_name = "MultiWorld Jinjos"

class EnableMultiWorldDabloons(Toggle):
    """Jolly Roger's Dabloons are scattered across the MultiWorld."""
    display_name = "MultiWorld Dabloons"

class EnableMultiWorldCheatoPages(Toggle):
    """Cheato pages are scattered across the MultiWorld."""
    display_name = "MultiWorld Cheato Pages"

class EnableMultiWorldHoneycombs(Toggle):
    """Honeycombs are scattered across the MultiWorld."""
    display_name = "MultiWorld Honeycombs"

class EnableMultiWorldGlowbos(Toggle):
    """Glowbos are scattered across the MultiWorld."""
    display_name = "MultiWorld Glowbos"

class KingJingalingHasJiggy(Toggle):
    """King Jingaling will always have a Jiggy to give you."""
    display_name = "King Jingaling Jiggy"

@dataclass
class BanjoTooieOptions(PerGameCommonOptions):
    death_link: DeathLink
    multiworld_moves: EnableMultiWorldMoveList
    multiworld_jinjos: EnableMultiWorldJinjos
    multiworld_dabloons: EnableMultiWorldDabloons
    mutliworld_cheato: EnableMultiWorldCheatoPages
    multiworld_honeycombs: EnableMultiWorldHoneycombs
    multiworld_glowbos: EnableMultiWorldGlowbos
    jingaling_jiggy: KingJingalingHasJiggy