from . import BanjoTooieTestBase
from ..Names import locationName, itemName

class TestWorldAccess(BanjoTooieTestBase):
    options = {
        "logic": 1,
        "randomize_stations": 'true',
        "randomize_chuffy": 'true'
    }
    def test_pine_grove(self) -> None:
        locations = [locationName.GEGGS]
        items = [[itemName.GGRAB, itemName.FEGGS], [itemName.CHUFFY]]
        self.assertAccessDependency(locations, items, True)

    def test_witchy_world_access(self) -> None:
        locations = [locationName.SPLITUP]
        items = [[itemName.FEGGS], [itemName.CHUFFY]]
        self.assertAccessDependency(locations, items, True)

    def test_cliff_top(self) -> None:
        locations = [locationName.IEGGS]
        items = [[itemName.SPLITUP], [itemName.CHUFFY]]
        self.assertAccessDependency(locations, items, True)

    def test_jrl_access(self) -> None:
        locations = [locationName.JRLDB1]
        items = [[itemName.SPLITUP], [itemName.CHUFFY]]
        self.assertAccessDependency(locations, items, True)