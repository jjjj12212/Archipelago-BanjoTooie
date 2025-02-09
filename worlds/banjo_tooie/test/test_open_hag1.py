from BaseClasses import ItemClassification
from ..Names import itemName
from ..Options import OpenHag1, VictoryCondition
from . import BanjoTooieTestBase

class TestOpenHag1(BanjoTooieTestBase):
    options = {
        "open_hag1": OpenHag1.option_true,
    }

    def test_progression_jiggies(self) -> None:
        # If the victory is specifically a victory condition that depends on Hag 1 being opened through jiggies,
        # Then the option does its effect.

        expected_progression_jiggies = 0
        max_jiggies_for_worlds = max(self.world.randomize_worlds.values()) if self.world.randomize_worlds else 55

        if self.world.options.victory_condition in [VictoryCondition.option_hag1, VictoryCondition.option_boss_hunt_and_hag1]:
            expected_progression_jiggies = max(70, max_jiggies_for_worlds)
        else:
            expected_progression_jiggies = max_jiggies_for_worlds

        assert expected_progression_jiggies == len([
            item.name for item in self.multiworld.itempool
            if item.name == itemName.JIGGY
            and item.classification == ItemClassification.progression
        ])

class TestOpenHag1WithHag1(BanjoTooieTestBase):
    options = {
        **TestOpenHag1.options,
        "victory_condition": VictoryCondition.option_hag1
    }

class TestOpenHag1WithBossesHag1(BanjoTooieTestBase):
    options = {
        **TestOpenHag1.options,
        "victory_condition": VictoryCondition.option_boss_hunt_and_hag1
    }

class TestOpenHag1WithBossesHag1(BanjoTooieTestBase):
    options = {
        **TestOpenHag1.options,
        "victory_condition": VictoryCondition.option_boss_hunt
    }
