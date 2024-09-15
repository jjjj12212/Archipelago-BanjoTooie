from . import BanjoTooieTestBase
from ..Names import locationName, itemName, regionName

class TestVictoryHAG1(BanjoTooieTestBase):
    options = {
        'victory_condition': 0
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNGAME1,
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNJINJO1
    }

    def test_mumbo_tokens(self) -> None:
        mumbo_tokens = 0
        for item in self.world.multiworld.itempool:
            if "Mumbo Token" == item.name:
                mumbo_tokens += 1
        
        for location in self.mumbo_token_location_group:
            try:
                if "Mumbo Token" == self.world.multiworld.get_location(location, self.player).item.name:
                    mumbo_tokens += 1
            except:
                mumbo_tokens += 0
        assert 0 == mumbo_tokens

class TestVictoryMiniGames(BanjoTooieTestBase):
    options = {
        'victory_condition': 1
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

    def test_mumbo_tokens(self) -> None:
        mumbo_tokens = 0
        for item in self.world.multiworld.itempool:
            if "Mumbo Token" == item.name:
                mumbo_tokens += 1
        
        for location in self.mumbo_token_location_group:
            try:
                if "Mumbo Token" == self.world.multiworld.get_location(location, self.player).item.name:
                    mumbo_tokens += 1
            except:
                mumbo_tokens += 0
        assert 15 == mumbo_tokens

class TestVictoryBosses(BanjoTooieTestBase):
    options = {
        'victory_condition': 2
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

    def test_mumbo_tokens(self) -> None:
        mumbo_tokens = 0
        for item in self.world.multiworld.itempool:
            if "Mumbo Token" == item.name:
                mumbo_tokens += 1
        
        for location in self.mumbo_token_location_group:
            try:
                if "Mumbo Token" == self.world.multiworld.get_location(location, self.player).item.name:
                    mumbo_tokens += 1
            except:
                mumbo_tokens += 0
        assert 8 == mumbo_tokens

class TestVictoryJinjo(BanjoTooieTestBase):
    options = {
        'victory_condition': 3
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

    def test_mumbo_tokens(self) -> None:
        mumbo_tokens = 0
        for item in self.world.multiworld.itempool:
            if "Mumbo Token" == item.name:
                mumbo_tokens += 1
        
        for location in self.mumbo_token_location_group:
            try:
                if "Mumbo Token" == self.world.multiworld.get_location(location, self.player).item.name:
                    mumbo_tokens += 1
            except:
                mumbo_tokens += 0
        assert 9 == mumbo_tokens

class TestVictoryWonderWing(BanjoTooieTestBase):
    options = {
        'victory_condition': 4
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

    def test_mumbo_tokens(self) -> None:
        mumbo_tokens = 0
        for item in self.world.multiworld.itempool:
            if "Mumbo Token" == item.name:
                mumbo_tokens += 1
        
        for location in self.mumbo_token_location_group:
            try:
                if "Mumbo Token" == self.world.multiworld.get_location(location, self.player).item.name:
                    mumbo_tokens += 1
            except:
                mumbo_tokens += 0
        assert 32 == mumbo_tokens
