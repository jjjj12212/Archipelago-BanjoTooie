from ..Items import rando_key_table
from ..Options import LogicType, RandomizeWorldOrder, SkipPuzzles
from ..Names import itemName
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase

class TestRandomizeWorlds(BanjoTooieTestBase):
    options = {
        "skip_puzzles": SkipPuzzles.option_true,
        "randomize_worlds": RandomizeWorldOrder.option_true
    }


