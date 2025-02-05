from .Options import VictoryCondition
from .test.test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase
from ..Names import locationName, itemName, regionName
from .. import all_item_table, all_group_table

#Tests and make sure that if the correct Victory Condition is set, enough Mumbo Tokens are placed
# and the game is beatable.
class TokenTest(BanjoTooieTestBase):
    mumbo_token_location_group = {}

    def test_mumbo_tokens(self, amt = None) -> None:
        if amt == None:
            amt = len(self.mumbo_token_location_group)

        # Randomized tokens for Token Hunt
        mumbo_tokens = 0
        for item in self.world.multiworld.itempool:
            if "Mumbo Token" == item.name:
                mumbo_tokens += 1

        # Locked locations for every other Mumbo token vic con
        for location in self.mumbo_token_location_group:
            try:
                if "Mumbo Token" == self.world.multiworld.get_location(location, self.player).item.name:
                    mumbo_tokens += 1
            except:
                mumbo_tokens += 0
        assert amt == mumbo_tokens

class TestVictoryHAG1(TokenTest):
    options = {
        'victory_condition': VictoryCondition.option_hag1,
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNGAME1,
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNJINJO1
    }
    def test_mumbo_tokens(self) -> None:
        super().test_mumbo_tokens(0)

class TestVictoryHAG1Intended(TestVictoryHAG1, IntendedLogic):
    options = {
        **TestVictoryHAG1.options,
        **IntendedLogic.options
    }

class TestVictoryHAG1EasyTricks(TestVictoryHAG1, EasyTricksLogic):
    options = {
        **TestVictoryHAG1.options,
        **IntendedLogic.options
    }

class TestVictoryHAG1Intended(TestVictoryHAG1, HardTricksLogic):
    options = {
        **TestVictoryHAG1.options,
        **IntendedLogic.options
    }

class TestVictoryHAG1Intended(TestVictoryHAG1, GlitchesLogic):
    options = {
        **TestVictoryHAG1.options,
        **IntendedLogic.options
    }

class TestVictoryMinigames(TokenTest):
    options = {
        'victory_condition': VictoryCondition.option_minigame_hunt
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNGAME1,
        locationName.MUMBOTKNGAME2,
        locationName.MUMBOTKNGAME3,
        locationName.MUMBOTKNGAME4,
        locationName.MUMBOTKNGAME5,
        locationName.MUMBOTKNGAME6,
        locationName.MUMBOTKNGAME7,
        locationName.MUMBOTKNGAME8,
        locationName.MUMBOTKNGAME9,
        locationName.MUMBOTKNGAME10,
        locationName.MUMBOTKNGAME11,
        locationName.MUMBOTKNGAME12,
        locationName.MUMBOTKNGAME13,
        locationName.MUMBOTKNGAME14,
        locationName.MUMBOTKNGAME15
    }

class TestVictoryMinigamesIntended(TestVictoryMinigames, IntendedLogic):
    options = {
        **TestVictoryMinigames.options,
        **IntendedLogic.options
    }

class TestVictoryMinigamesEasyTricks(TestVictoryMinigames, EasyTricksLogic):
    options = {
        **TestVictoryMinigames.options,
        **IntendedLogic.options
    }

class TestVictoryMinigamesIntended(TestVictoryMinigames, HardTricksLogic):
    options = {
        **TestVictoryMinigames.options,
        **IntendedLogic.options
    }

class TestVictoryMinigamesIntended(TestVictoryMinigames, GlitchesLogic):
    options = {
        **TestVictoryMinigames.options,
        **IntendedLogic.options
    }

class TestVictoryBosses(TokenTest):
    options = {
        'victory_condition': VictoryCondition.option_boss_hunt
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNBOSS2,
        locationName.MUMBOTKNBOSS3,
        locationName.MUMBOTKNBOSS4,
        locationName.MUMBOTKNBOSS5,
        locationName.MUMBOTKNBOSS6,
        locationName.MUMBOTKNBOSS7,
        locationName.MUMBOTKNBOSS8
    }

class TestVictoryBossesIntended(TestVictoryBosses, IntendedLogic):
    options = {
        **TestVictoryBosses.options,
        **IntendedLogic.options
    }

class TestVictoryBossesEasyTricks(TestVictoryBosses, EasyTricksLogic):
    options = {
        **TestVictoryBosses.options,
        **IntendedLogic.options
    }

class TestVictoryBossesIntended(TestVictoryBosses, HardTricksLogic):
    options = {
        **TestVictoryBosses.options,
        **IntendedLogic.options
    }

class TestVictoryBossesIntended(TestVictoryBosses, GlitchesLogic):
    options = {
        **TestVictoryBosses.options,
        **IntendedLogic.options
    }

class TestVictoryJinjos(TokenTest):
    options = {
        'victory_condition': VictoryCondition.option_jinjo_family_rescue,
        'logic_type': 0
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNJINJO1,
        locationName.MUMBOTKNJINJO2,
        locationName.MUMBOTKNJINJO3,
        locationName.MUMBOTKNJINJO4,
        locationName.MUMBOTKNJINJO5,
        locationName.MUMBOTKNJINJO6,
        locationName.MUMBOTKNJINJO7,
        locationName.MUMBOTKNJINJO8,
        locationName.MUMBOTKNJINJO9,
    }

class TestVictoryJinjosIntended(TestVictoryJinjos, IntendedLogic):
    options = {
        **TestVictoryJinjos.options,
        **IntendedLogic.options
    }

class TestVictoryJinjosEasyTricks(TestVictoryJinjos, EasyTricksLogic):
    options = {
        **TestVictoryJinjos.options,
        **IntendedLogic.options
    }

class TestVictoryJinjosIntended(TestVictoryJinjos, HardTricksLogic):
    options = {
        **TestVictoryJinjos.options,
        **IntendedLogic.options
    }

class TestVictoryJinjosIntended(TestVictoryJinjos, GlitchesLogic):
    options = {
        **TestVictoryJinjos.options,
        **IntendedLogic.options
    }

class TestVictoryWonderwing(TokenTest):
    options = {
        'victory_condition': VictoryCondition.option_wonderwing_challenge
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNGAME1,
        locationName.MUMBOTKNGAME2,
        locationName.MUMBOTKNGAME3,
        locationName.MUMBOTKNGAME4,
        locationName.MUMBOTKNGAME5,
        locationName.MUMBOTKNGAME6,
        locationName.MUMBOTKNGAME7,
        locationName.MUMBOTKNGAME8,
        locationName.MUMBOTKNGAME9,
        locationName.MUMBOTKNGAME10,
        locationName.MUMBOTKNGAME11,
        locationName.MUMBOTKNGAME12,
        locationName.MUMBOTKNGAME13,
        locationName.MUMBOTKNGAME14,
        locationName.MUMBOTKNGAME15,
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNBOSS2,
        locationName.MUMBOTKNBOSS3,
        locationName.MUMBOTKNBOSS4,
        locationName.MUMBOTKNBOSS5,
        locationName.MUMBOTKNBOSS6,
        locationName.MUMBOTKNBOSS7,
        locationName.MUMBOTKNBOSS8,
        locationName.MUMBOTKNJINJO1,
        locationName.MUMBOTKNJINJO2,
        locationName.MUMBOTKNJINJO3,
        locationName.MUMBOTKNJINJO4,
        locationName.MUMBOTKNJINJO5,
        locationName.MUMBOTKNJINJO6,
        locationName.MUMBOTKNJINJO7,
        locationName.MUMBOTKNJINJO8,
        locationName.MUMBOTKNJINJO9,
    }

class TestVictoryWonderwingIntended(TestVictoryWonderwing, IntendedLogic):
    options = {
        **TestVictoryWonderwing.options,
        **IntendedLogic.options
    }

class TestVictoryWonderwingEasyTricks(TestVictoryWonderwing, EasyTricksLogic):
    options = {
        **TestVictoryWonderwing.options,
        **IntendedLogic.options
    }

class TestVictoryWonderwingIntended(TestVictoryWonderwing, HardTricksLogic):
    options = {
        **TestVictoryWonderwing.options,
        **IntendedLogic.options
    }

class TestVictoryWonderwingIntended(TestVictoryWonderwing, GlitchesLogic):
    options = {
        **TestVictoryWonderwing.options,
        **IntendedLogic.options
    }

class TestVictoryBossesHAG1(TokenTest):
    options = {
        'victory_condition': VictoryCondition.option_boss_hunt_and_hag1
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNBOSS2,
        locationName.MUMBOTKNBOSS3,
        locationName.MUMBOTKNBOSS4,
        locationName.MUMBOTKNBOSS5,
        locationName.MUMBOTKNBOSS6,
        locationName.MUMBOTKNBOSS7,
        locationName.MUMBOTKNBOSS8
    }

class TestVictoryBossesHAG1Intended(TestVictoryBossesHAG1, IntendedLogic):
    options = {
        **TestVictoryBossesHAG1.options,
        **IntendedLogic.options
    }

class TestVictoryBossesHAG1EasyTricks(TestVictoryBossesHAG1, EasyTricksLogic):
    options = {
        **TestVictoryBossesHAG1.options,
        **IntendedLogic.options
    }

class TestVictoryBossesHAG1Intended(TestVictoryBossesHAG1, HardTricksLogic):
    options = {
        **TestVictoryBossesHAG1.options,
        **IntendedLogic.options
    }

class TestVictoryBossesHAG1Intended(TestVictoryBossesHAG1, GlitchesLogic):
    options = {
        **TestVictoryBossesHAG1.options,
        **IntendedLogic.options
    }
