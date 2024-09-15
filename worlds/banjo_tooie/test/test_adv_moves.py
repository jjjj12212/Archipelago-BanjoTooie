from . import BanjoTooieTestBase
from ..Names import locationName, itemName, regionName
from .. import all_item_table

class TestAdvMovesEnabled(BanjoTooieTestBase):
    options = {
        'randomized_moves': 'true'
    }
    def test_item_pool(self) -> None:
        adv_move_count = len(self.world.item_name_groups["Moves"])
        adv_count = 0

        for adv_move in self.world.item_name_groups["Moves"]:    
            for item in self.world.multiworld.itempool:
                if adv_move == item.name:
                    adv_count += 1

        assert adv_move_count == adv_count

class TestAdvMovesDisabled(BanjoTooieTestBase):
    options = {
        'randomize_moves': 'false'
    }
    prefill_locations = {

    }
    def test_item_pool(self) -> None:
        adv_count = 0

        for adv_move in self.world.item_name_groups["Moves"]:    
            for item in self.world.multiworld.itempool:
                if adv_move == item.name:
                    print(f"Item: {adv_move} Should be here!")
                    adv_count += 1

        assert 0 == adv_count


    def test_adv_prefills(self) -> None:
        adv_items = 0
        placed_correctly = 0
        for name in self.world.item_name_groups["Moves"]:
            adv_items += 1
            banjoItem = all_item_table.get(name)
            try:
                location_item = self.multiworld.get_location(banjoItem.default_location, self.player).item.name
                if location_item == name:
                    placed_correctly += 1
            except:
                print(f"Issue with Item: {name} Please Investigate")
                placed_correctly += 0
        assert adv_items == placed_correctly
