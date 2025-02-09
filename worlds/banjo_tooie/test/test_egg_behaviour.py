from ..Names import itemName, locationName
from ..Options import EggsBehaviour, RandomizeBKMoveList, RandomizeBTMoveList
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase

class BlueEggStartVanillaMovesTest(BanjoTooieTestBase):
    options = {
        "randomize_moves": RandomizeBTMoveList.option_false,
        "egg_behaviour": EggsBehaviour.option_start_with_blue_eggs,
    }

    def test_blue_egg_in_starting_inventory(self):
        assert not itemName.BEGGS in [item.name for item in self.multiworld.itempool]
        assert itemName.BEGGS in [item.name for item in self.multiworld.precollected_items[self.player]]

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for egg in [itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]:
            assert not egg in item_pool_names

    def test_prefill(self) -> None:
        silos = [locationName.FEGGS, locationName.GEGGS, locationName.IEGGS, locationName.CEGGS]
        silos_to_vanilla_item = {
            locationName.FEGGS: itemName.FEGGS,
            locationName.GEGGS: itemName.GEGGS,
            locationName.IEGGS: itemName.IEGGS,
            locationName.CEGGS: itemName.CEGGS,
        }

        for silo in silos:
            assert self.world.get_location(silo).item.name == silos_to_vanilla_item[silo]

class BlueEggStartRandomizedMovesTest(BanjoTooieTestBase):
    options = {
        "randomize_moves": RandomizeBTMoveList.option_true,
        "egg_behaviour": EggsBehaviour.option_start_with_blue_eggs,
    }

    def test_blue_egg_in_starting_inventory(self):
        assert not itemName.BEGGS in [item.name for item in self.multiworld.itempool]
        assert itemName.BEGGS in [item.name for item in self.multiworld.precollected_items[self.player]]

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for egg in [itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]:
            assert egg in item_pool_names

class RandomStartEggTest(BanjoTooieTestBase):
    options = {
        "randomize_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "egg_behaviour": EggsBehaviour.option_random_starting_egg,
    }

    def test_starting_inventory(self) -> None:
        start_inventory_names = [item.name for item in self.multiworld.precollected_items[self.player]]
        eggs_in_inventory = 0
        for egg in [itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]:
            if egg in start_inventory_names:
                eggs_in_inventory += 1
        assert eggs_in_inventory == 1

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        eggs_in_pool = 0
        for egg in [itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]:
            if egg in item_pool_names:
                eggs_in_pool += 1
        assert eggs_in_pool == 4 # One is in the starting inventory.

class ProgressiveEggsTest(BanjoTooieTestBase):
    options = {
        "randomize_moves": RandomizeBTMoveList.option_true,
        "egg_behaviour": EggsBehaviour.option_progressive_eggs,
    }

    def test_blue_egg_in_starting_inventory(self):
        assert not itemName.BEGGS in [item.name for item in self.multiworld.itempool]
        assert itemName.BEGGS in [item.name for item in self.multiworld.precollected_items[self.player]]

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for egg in [itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]:
            assert not egg in item_pool_names

        assert item_pool_names.count(itemName.PEGGS) == 4

class TestBlueEggStartVanillaMovesIntended(BlueEggStartVanillaMovesTest, IntendedLogic):
    options = {
        **BlueEggStartVanillaMovesTest.options,
        **IntendedLogic.options,
    }

class TestBlueEggStartVanillaMovesEasyTricks(BlueEggStartVanillaMovesTest, EasyTricksLogic):
    options = {
        **BlueEggStartVanillaMovesTest.options,
        **EasyTricksLogic.options,
    }

class TestBlueEggStartVanillaMovesHardTricks(BlueEggStartVanillaMovesTest, HardTricksLogic):
    options = {
        **BlueEggStartVanillaMovesTest.options,
        **HardTricksLogic.options,
    }

class TestBlueEggStartVanillaMovesGlitches(BlueEggStartVanillaMovesTest, GlitchesLogic):
    options = {
        **BlueEggStartVanillaMovesTest.options,
        **GlitchesLogic.options,
    }

class TestBlueEggStartRandomizedMovesIntended(BlueEggStartRandomizedMovesTest, IntendedLogic):
    options = {
        **BlueEggStartRandomizedMovesTest.options,
        **IntendedLogic.options,
    }

class TestBlueEggStartRandomizedMovesEasyTricks(BlueEggStartRandomizedMovesTest, EasyTricksLogic):
    options = {
        **BlueEggStartRandomizedMovesTest.options,
        **EasyTricksLogic.options,
    }

class TestBlueEggStartRandomizedMovesHardTricks(BlueEggStartRandomizedMovesTest, HardTricksLogic):
    options = {
        **BlueEggStartRandomizedMovesTest.options,
        **HardTricksLogic.options,
    }

class TestBlueEggStartRandomizedMovesGlitches(BlueEggStartRandomizedMovesTest, GlitchesLogic):
    options = {
        **BlueEggStartRandomizedMovesTest.options,
        **GlitchesLogic.options,
    }

class TestRandomStartEggIntended(RandomStartEggTest, IntendedLogic):
    options = {
        **RandomStartEggTest.options,
        **IntendedLogic.options,
    }

class TestRandomStartEggEasyTricks(RandomStartEggTest, EasyTricksLogic):
    options = {
        **RandomStartEggTest.options,
        **EasyTricksLogic.options,
    }

class TestRandomStartEggHardTricks(RandomStartEggTest, HardTricksLogic):
    options = {
        **RandomStartEggTest.options,
        **HardTricksLogic.options,
    }

class TestRandomStartEggGlitches(RandomStartEggTest, GlitchesLogic):
    options = {
        **RandomStartEggTest.options,
        **GlitchesLogic.options,
    }

class TestProgressiveEggsIntended(ProgressiveEggsTest, IntendedLogic):
    options = {
        **ProgressiveEggsTest.options,
        **IntendedLogic.options,
    }

class TestProgressiveEggsEasyTricks(ProgressiveEggsTest, EasyTricksLogic):
    options = {
        **ProgressiveEggsTest.options,
        **EasyTricksLogic.options,
    }

class TestProgressiveEggsHardTricks(ProgressiveEggsTest, HardTricksLogic):
    options = {
        **ProgressiveEggsTest.options,
        **HardTricksLogic.options,
    }

class TestProgressiveEggsGlitches(ProgressiveEggsTest, GlitchesLogic):
    options = {
        **ProgressiveEggsTest.options,
        **GlitchesLogic.options,
    }
