from ..Options import LogicType, RandomizeBKMoveList, RandomizeBTMoveList
from . import BanjoTooieTestBase

# Many tests inherit from logic tests, to make sure that the logic of all collectibles works.
class IntendedLogic:
    options = {
        "logic_type": LogicType.option_intended,
        "randomize_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
    }

class EasyTricksLogic:
    options = {
        "logic_type": LogicType.option_easy_tricks,
        "randomize_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
    }

class HardTricksLogic:
    options = {
        "logic_type": LogicType.option_hard_tricks,
        "randomize_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
    }

class GlitchesLogic:
    options = {
        "logic_type": LogicType.option_glitches,
        "randomize_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
    }
