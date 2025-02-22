from collections import defaultdict

from ..Names import itemName
from . import BanjoTooieTestBase


class FillersTrapTestBase(BanjoTooieTestBase):
    class Pool:
        def __init__(self):
            self.trap_distribution = defaultdict(int)
            self.filler_distribution = defaultdict(int)

    def pool(self) -> Pool:
        pool = self.Pool()
        for item in self.world.multiworld.itempool:
            if item.trap:
                pool.trap_distribution[item.name] += 1
            if item.filler and not item.name in [itemName.JIGGY, itemName.PAGES, itemName.HONEY, itemName.NOTE]:
                pool.filler_distribution[item.name] += 1

        return pool

class TestMaxTrapsZero(FillersTrapTestBase):
    options = {
        "max_traps": 0,
        "nestsanity": "false",

        # to add 16 filler items
        "extra_trebleclefs_count": 0,
        "bass_clef_amount": 0,
        "randomize_bk_moves": 0,
        "cheato_rewards": "true",
        "honeyb_rewards": "true",
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = super().pool()

        assert sum(pool.filler_distribution.values()) == 16
        assert sum(pool.trap_distribution.values()) == 0

class TestMaxTrapsNonZero(FillersTrapTestBase):
    options = {
        "max_traps": 100,
        "nestsanity": "false",

        # to add 16 filler items
        "extra_trebleclefs_count": 0,
        "bass_clef_amount": 0,
        "randomize_bk_moves": 0,
        "cheato_rewards": "true",
        "honeyb_rewards": "true",
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = super().pool()

        fillers = sum(pool.filler_distribution.values())
        traps = sum(pool.trap_distribution.values())
        assert fillers > 0
        assert traps > 0
        assert fillers + traps == 16

class TestMaxTrapsZeroWithNestsanity(FillersTrapTestBase):
    options = {
        "max_traps": 0,
        "nestsanity": "true",

        "extra_trebleclefs_count": 0,
        "bass_clef_amount": 0,
        "randomize_bk_moves": 2,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = super().pool()

        assert sum(pool.filler_distribution.values()) == 450 + 23
        assert sum(pool.trap_distribution.values()) == 0


class TestFillersExtraClefs(FillersTrapTestBase):
    options = {
        "max_traps": 0,
        "randomize_bk_moves": 2,
        "randomize_notes": "true",
        "extra_trebleclefs_count": 21,
        "bass_clef_amount": 30,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = super().pool()

        assert sum(pool.filler_distribution.values()) == 30 + 21 * 3
        assert sum(pool.trap_distribution.values()) == 0

class TestRespectDistribution(FillersTrapTestBase):
    options = {
        "max_traps": "unlimited",
        "randomize_bk_moves": 2,
        # nests config
        "nestsanity": "true",
        "traps_nests_ratio": 100,
        # notes config
        "randomize_notes": "true",
        "extra_trebleclefs_count": 21,
        "bass_clef_amount": 30,
        # weights
        "big_o_pants_weight": 0,
        "golden_eggs_weight": 0,
        "trip_trap_weight": 0,
        "egg_nests_weight": 1,
        "feather_nests_weight": 1,
        "slip_trap_weight": 50,
        "transform_trap_weight": 50,
        "squish_trap_weight": 100,
        "tip_trap_weight": 100,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = super().pool()

        expected_slots = 315 + 135 + 23 + 30 + 3 * 21  ##566
        assert sum(pool.trap_distribution.values()) + \
               sum(pool.filler_distribution.values()) == expected_slots

        assert pool.filler_distribution[itemName.NONE] == 0
        assert pool.trap_distribution[itemName.TTRAP] == 0
        assert pool.trap_distribution[itemName.GNEST] == 0

        assert pool.filler_distribution[itemName.ENEST] < 10
        assert pool.filler_distribution[itemName.FNEST] < 10

        assert pool.trap_distribution[itemName.STRAP] > 50
        assert pool.trap_distribution[itemName.STRAP] < 150

        assert pool.trap_distribution[itemName.TRTRAP] > 50
        assert pool.trap_distribution[itemName.TRTRAP] < 150

        assert pool.trap_distribution[itemName.SQTRAP] > 150

        assert pool.trap_distribution[itemName.TITRAP] > 150


class TestRespectMaxTraps(FillersTrapTestBase):
    options = {
        "max_traps": 30,
        "randomize_bk_moves": 2,
        # nests config
        "nestsanity": "true",
        "traps_nests_ratio": 100,
        # notes config
        "randomize_notes": "true",
        "extra_trebleclefs_count": 21,
        "bass_clef_amount": 30,
        # weights
        "big_o_pants_weight": 0,
        "egg_nests_weight": 1,
        "feather_nests_weight": 1,

        "golden_eggs_weight": 100,
        "trip_trap_weight": 100,
        "slip_trap_weight": 100,
        "transform_trap_weight": 100,
        "squish_trap_weight": 100,
        "tip_trap_weight": 100,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = super().pool()

        expected_slots = 315 + 135 + 23 + 30 + 3 * 21  ##566
        assert sum(pool.trap_distribution.values()) == 30
        assert sum(pool.filler_distribution.values()) == expected_slots - 30

        assert pool.filler_distribution[itemName.ENEST] > 200
        assert pool.filler_distribution[itemName.ENEST] < 300
        assert pool.filler_distribution[itemName.FNEST] > 200
        assert pool.filler_distribution[itemName.FNEST] < 300
