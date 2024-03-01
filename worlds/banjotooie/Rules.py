from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from .Names import regionName, itemName, locationName
from .Items import BanjoTooieItem, all_item_table, jiggy_table, all_group_table
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import BanjoTooieWorld
else:
    BanjoTooieWorld = object

# Shamelessly Stolen from KH2 :D
    
class BanjoTooieRules:
    player: int
    world: BanjoTooieWorld
    region_rules= {}
    can_transform = {}
    mumbo_magic = {}


    def __init__(self, world: BanjoTooieWorld) -> None:
        self.player = world.player
        self.world = world

        self.region_rules = {
            regionName.IOHWH:   lambda state: self.jiggy_unlock(state, 1),
            regionName.MT:      lambda state: self.jiggy_unlock(state, 1),
            regionName.GM:      lambda state: self.jiggy_unlock(state, 4),
            regionName.WW:      lambda state: self.jiggy_unlock(state, 8),
            regionName.JR:      lambda state: self.jiggy_unlock(state, 14),
            regionName.TL:      lambda state: self.jiggy_unlock(state, 20),
            regionName.GI:      lambda state: self.jiggy_unlock(state, 28),
            regionName.HP:      lambda state: self.jiggy_unlock(state, 36),
            regionName.CC:      lambda state: self.jiggy_unlock(state, 45),
            regionName.CK:      lambda state: self.jiggy_unlock(state, 55),
            regionName.H1:      lambda state: self.jiggy_unlock(state, 70) 
        }

        self.can_transform = {
            "Stony":           lambda state: state.has(itemName.HUMBAMT, self.player) and
                                             self.mumbo_magic["Golden Goliath"],
            "Detonator":       lambda state: state.has(itemName.HUMBAGM, self.player),
            "Money Van":       lambda state: state.has(itemName.HUMBAWW, self.player),
            "Sub":             lambda state: state.has(itemName.HUMBAJR, self.player) and
                                             self.mumbo_magic["Oxygenate"],
            "T-Rex":           lambda state: state.has(itemName.HUMBATD, self.player),
            "Washing Machine": lambda state: state.has(itemName.HUMBAGI, self.player),
            "Snowball":        lambda state: state.has(itemName.HUMBAHP, self.player),
            "Bee":             lambda state: state.has(itemName.HUMBACC, self.player),
            "Dragon":          lambda state: state.has(itemName.HUMBAIH, self.player)
        }

        self.mumbo_magic = {
            "Golden Goliath": lambda state: state.has(itemName.MUMBOMT, self.player),
            "Levitate":       lambda state: state.has(itemName.MUMBOGM, self.player),
            "Power":          lambda state: state.has(itemName.MUMBOWW, self.player) and
                                            self.can_transform["Money Van"],
            "Oxygenate":      lambda state: state.has(itemName.MUMBOJR, self.player),
            "Grow/Shrink":    lambda state: state.has(itemName.MUMBOTD, self.player),
            "EMP":            lambda state: state.has(itemName.MUMBOGI, self.player),
            "Revive":         lambda state: state.has(itemName.MUMBOHP, self.player),
            "Rain Dance":     lambda state: state.has(itemName.MUMBOCC, self.player),
            "Heal":           lambda state: state.has(itemName.MUMBOIH, self.player)
        }


    def jiggy_unlock(self, state: CollectionState, Amount) -> bool:
        return state.has_group("Jiggy", self.player, Amount)
        

    def set_rules(self) -> None:
        for region_name, rules in self.region_rules.items():
            region = self.world.multiworld.get_region(region_name, self.player)
            for entrance in region.entrances:
                entrance.access_rule = rules
        self.world.multiworld.completion_condition[self.player] = lambda state: state.has("Kick Around", self.player)
