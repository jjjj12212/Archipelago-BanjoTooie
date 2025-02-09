from ..Names import itemName, locationName
from ..Options import RandomizeNotes
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from ..Locations import all_location_table
from . import BanjoTooieTestBase

class TestRandomizedNotes(BanjoTooieTestBase):
    options = {
        "randomize_notes": RandomizeNotes.option_true,
    }
    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.NOTE) == 144

class TestVanillaNotes(BanjoTooieTestBase):
    options = {
        "randomize_notes": RandomizeNotes.option_false,
    }
    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.NOTE) == 0

    def test_prefills(self) -> None:
        vanilla_locations_names = [location_name for location_name, location_data in all_location_table.items()\
                                   if location_data.group == "Note"]
        vanilla_locations = [location for location in self.world.get_locations()\
                             if location.name in vanilla_locations_names]

        assert len(vanilla_locations) == 144
        for location in vanilla_locations:
            assert location.item.name == itemName.NOTE


class TestRandomizedNotesIntended(TestRandomizedNotes, IntendedLogic):
    options = {
        **TestRandomizedNotes.options,
        **IntendedLogic.options,
    }

class TestRandomizedNotesEasyTricks(TestRandomizedNotes, EasyTricksLogic):
    options = {
        **TestRandomizedNotes.options,
        **EasyTricksLogic.options,
    }

class TestRandomizedNotesHardTricks(TestRandomizedNotes, HardTricksLogic):
    options = {
        **TestRandomizedNotes.options,
        **HardTricksLogic.options,
    }

class TestRandomizedNotesGlitches(TestRandomizedNotes, GlitchesLogic):
    options = {
        **TestRandomizedNotes.options,
        **GlitchesLogic.options,
    }

class TestVanillaNotesIntended(TestVanillaNotes, IntendedLogic):
    options = {
        **TestVanillaNotes.options,
        **IntendedLogic.options,
    }

class TestVanillaNotesEasyTricks(TestVanillaNotes, EasyTricksLogic):
    options = {
        **TestVanillaNotes.options,
        **EasyTricksLogic.options,
    }

class TestVanillaNotesHardTricks(TestVanillaNotes, HardTricksLogic):
    options = {
        **TestVanillaNotes.options,
        **HardTricksLogic.options,
    }

class TestVanillaNotesGlitches(TestVanillaNotes, GlitchesLogic):
    options = {
        **TestVanillaNotes.options,
        **GlitchesLogic.options,
    }
