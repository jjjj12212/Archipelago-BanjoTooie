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
    region_rules = {}
    can_transform = {}
    mumbo_magic = {}
    banjo_moves = {}
    kazooie_moves = {}
    jiggy_rules = {}


    def __init__(self, world: BanjoTooieWorld) -> None:
        self.player = world.player
        self.world = world

        self.region_rules = {
            regionName.IOHWH:   lambda state: self.jiggy_unlock(state, 1),
            regionName.MT:      lambda state: self.jiggy_unlock(state, 1),
            regionName.IOHPL:   lambda state: state.has(itemName.GGRAB, self.player) or
                                              self.jiggy_rules[locationName.JIGGYGM6],
            regionName.GM:      lambda state: self.jiggy_unlock(state, 4) or
                                              self.jiggy_rules[locationName.JIGGYGM6],
            regionName.IOHPG:   lambda state: state.has(itemName.FEGGS, self.player),
            regionName.WW:      lambda state: self.jiggy_unlock(state, 8),
            regionName.IOHCT:   lambda state: state.has(itemName.SPLITUP, self.player),
            regionName.JR:      lambda state: self.jiggy_unlock(state, 14),
            regionName.IOHWL:   lambda state: state.has(itemName.TTORP, self.player),
            regionName.TL:      lambda state: self.jiggy_unlock(state, 20),
            regionName.IOHQM:   lambda state: state.has(itemName.SPRINGB, self.player),
            regionName.GI:      lambda state: self.jiggy_unlock(state, 28),
            regionName.HP:      lambda state: self.jiggy_unlock(state, 36),
            regionName.CC:      lambda state: self.jiggy_unlock(state, 45),
            regionName.CK:      lambda state: self.jiggy_unlock(state, 55) and state.has(itemName.CLAWBTS, self.player),
            regionName.H1:      lambda state: self.jiggy_unlock(state, 70) and
                                              (self.banjo_moves["Pack Whack"] or self.banjo_moves["Sack Pack"]) and
                                              (self.kazooie_moves["Wing Whack"] or self.kazooie_moves["Glide"]) and
                                              state.has(itemName.BBLASTER, self.player) and
                                              state.has(itemName.CEGGS, self.player)
        }

        self.can_transform = {
            "Stony":           lambda state: state.has(itemName.HUMBAMT, self.player) and
                                             self.mumbo_magic["Golden Goliath"],
            "Detonator":       lambda state: state.has(itemName.HUMBAGM, self.player),
            "Money Van":       lambda state: state.has(itemName.HUMBAWW, self.player),
            "Sub":             lambda state: state.has(itemName.HUMBAJR, self.player) and
                                             self.can_reach_atlantis,
            "T-Rex":           lambda state: state.has(itemName.HUMBATD, self.player),
            "Washing Machine": lambda state: state.has(itemName.HUMBAGI, self.player) and
                                             self.can_reach_GI_2F,
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
            "EMP":            lambda state: state.has(itemName.MUMBOGI, self.player) and
                                            self.can_reach_GI_2F,
            "Revive":         lambda state: state.has(itemName.MUMBOHP, self.player),
            "Rain Dance":     lambda state: state.has(itemName.MUMBOCC, self.player),
            "Heal":           lambda state: state.has(itemName.MUMBOIH, self.player)
        }

        self.has_fire = lambda state: state.has(itemName.FEGGS, self.player) or self.can_transform["Dragon"]
        self.long_swim = lambda state: state.has(itemName.BDRILL, self.player) or self.mumbo_magic["Oxygenate"]
        self.can_reach_atlantis = lambda state: state.has(itemName.IEGGS) and self.long_swim and state.has(itemName.AUQAIM, self.player)
        self.banjo_moves = {
            "Pack Whack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.PACKWH, self.player),
            "Taxi Pack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.TAXPACK, self.player),
            "Snooze Pack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.SNPACK, self.player),
            "Shack Pack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.SHPACK, self.player),
            "Sack Pack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.SAPACK, self.player),
        }
        self.kazooie_moves = {
            "Wing Whack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.WWHACK, self.player),
            "Hatch": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.HATCH, self.player),
            "Leg Spring": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.LSPRING, self.player),
            "Glide": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.GLIDE, self.player),
        }
        self.MT_flight_pad = lambda state: state.has(itemName.BDRILL, self.player) or self.mumbo_magic["Golden Goliath"]
        self.prison_compound_open = lambda state: state.has(itemName.GEGGS, self.player) or \
                                                  state.has(itemName.CEGGS, self.player) or \
                                                  self.mumbo_magic["Golden Goliath"]
        self.GM_boulders = lambda state: state.has(itemName.BDRILL, self.player) or self.can_transform["Detonator"]
        self.can_kill_fruity = lambda state: state.has(itemName.GEGGS, self.player) or \
                                             state.has(itemName.CEGGS, self.player) or \
                                             self.can_transform["Money Van"]
        self.saucer_door_open = lambda state: state.has(itemName.GGRAB, self.player) or \
                                              (state.has(itemName.EGGAIM, self.player) and
                                               (state.has(itemName.GEGGS, self.player) or
                                                state.has(itemName.CEGGS, self.player)))
        #self.open_tiptup_beach = lambda state: state.has(itemName.GEGGS, self.player) or self.mumbo_magic["Oxygenate"]
        self.can_beat_terry = lambda state: state.has(itemName.EGGAIM, self.player) and state.has(itemName.SPRINGB, self.player)
        self.oogle_boogles_open = self.can_transform["T-Rex"] and self.mumbo_magic["Grow/Shrink"]
        self.smuggle_food = lambda state: (self.jiggy_rules[locationName.JIGGYGM1] and
                                           state.has(itemName.GGRAB, self.player)) or \
                                          state.has(itemName.CLAWBTS, self.player)
        self.enter_GI = lambda state: self.jiggy_rules[locationName.JIGGYGM1] or \
                                      state.has(itemName.CLAWBTS, self.player)
        self.GI_front_door = lambda state: self.enter_GI and state.has(itemName.SPLITUP, self.player)
        self.can_reach_GI_2F = lambda state: state.has(itemName.CLAWBTS, self.player) or \
                                             (self.GI_front_door and
                                              self.kazooie_moves["Leg Spring"] and
                                              self.kazooie_moves["Glide"] and
                                              (self.kazooie_moves["Wing Whack"] or
                                              state.has(itemName.EGGAIM, self.player)))
        self.can_beat_weldar = lambda state: self.enter_GI and \
                                             self.can_use_battery and \
                                             self.mumbo_magic["EMP"] and \
                                             self.can_transform["Washing Machine"] and \
                                             (state.has(itemName.FEGGS, self.player) or
                                              state.has(itemName.GEGGS, self.player) or
                                              state.has(itemName.CEGGS, self.player))
        self.can_use_battery = self.banjo_moves["Pack Whack"] and self.banjo_moves["Taxi Pack"]
        self.can_use_floatus = self.banjo_moves["Taxi Pack"] and self.kazooie_moves["Hatch"]
        self.grow_beanstalk = lambda state: state.has(itemName.BDRILL, self.player) and self.mumbo_magic["Rain Dance"]

        self.jiggy_rules = {
            #Mayahem Temple Jiggies
            locationName.JIGGYMT1: lambda state: state.has(itemName.BBLASTER, self.player),
            locationName.JIGGYMT2: lambda state: state.has(itemName.BBLASTER, self.player),
            locationName.JIGGYMT3: self.can_transform["Stony"],
            locationName.JIGGYMT4: lambda state: state.has(itemName.EGGAIM, self.player) or
                                                 self.MT_flight_pad,
            locationName.JIGGYMT5: lambda state: state.has(itemName.EGGAIM,  self.player) and
                                                 state.has(itemName.GGRAB, self.player) or
                                                 self.MT_flight_pad,
            locationName.JIGGYMT6: self.mumbo_magic["Golden Goliath"],
            locationName.JIGGYMT7: lambda state: state.has(itemName.GGRAB, self.player) and
                                                 self.prison_compound_open,
            locationName.JIGGYMT8: lambda state: state.has(itemName.BDRILL, self.player) and
                                                 self.prison_compound_open,
            locationName.JIGGYMT10: lambda state: state.has(itemName.GGRAB, self.player) and
                                                 self.mumbo_magic["Golden Goliath"],
            #Glitter Gulch Mine Jiggies
            locationName.JIGGYGM1: self.mumbo_magic["Levitate"],
            locationName.JIGGYGM2: lambda state: self.can_transform["Detonator"] or
                                                 state.has(itemName.CEGGS, self.player),
            locationName.JIGGYGM5: lambda state: state.has(itemName.BBLASTER, self.player) and
                                                 state.has(itemName.BBAYONET, self.player) and
                                                 self.GM_boulders,
            locationName.JIGGYGM6: lambda state: state.has(itemName.BDRILL, self.player) and
                                                 self.prison_compound_open and
                                                 self.can_transform["Stony"],
            locationName.JIGGYGM7: self.mumbo_magic["Levitate"],
            locationName.JIGGYGM8: lambda state: state.has(itemName.SPRINGB, self.player) or
                                                 state.has(itemName.CEGGS, self.player),
            locationName.JIGGYGM9: self.GM_boulders,

            #Witchyworld Jiggies
            locationName.JIGGYWW1: lambda state: state.has(itemName.SPLITUP, self.player),
            locationName.JIGGYWW2: self.can_transform["Money Van"] and self.mumbo_magic["Power"],
            locationName.JIGGYWW3: lambda state: state.has(itemName.AIREAIM, self.player) and
                                                 self.can_kill_fruity,
            locationName.JIGGYWW4: self.can_transform["Detonator"] and
                                   self.mumbo_magic["Power"] and
                                   self.saucer_door_open,
            locationName.JIGGYWW5: lambda state: state.has(itemName.SPLITUP, self.player) and
                                                 state.has(itemName.AIREAIM, self.player),
            locationName.JIGGYWW7: self.can_transform["Money Van"] and
                                   self.mumbo_magic["Power"] and
                                   self.banjo_moves["Taxi Pack"],
            locationName.JIGGYWW8: self.mumbo_magic["Power"],
            locationName.JIGGYWW9: self.can_transform["Money Van"],
            locationName.JIGGYWW10: lambda state: state.has(itemName.BDRILL, self.player) and
                                                  state.has(itemName.GEGGS, self.player),

            #Jolly Joger's Lagoon Jiggies
            locationName.JIGGYJR1: self.can_transform["Sub"],
            locationName.JIGGYJR2: lambda state: self.kazooie_moves["Hatch"] and
                                                  state.has(itemName.GEGGS, self.player),
            locationName.JIGGYJR3: lambda state: self.can_reach_atlantis and
                                                 (state.has(itemName.AUQAIM, self.player) or
                                                  self.can_transform["Sub"]),
            locationName.JIGGYJR4: lambda state: (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.BDRILL, self.player)) and
                                                 self.region_rules[regionName.CC] and
                                                 state.has(itemName.SPLITUP, self.player),
            locationName.JIGGYJR5: self.kazooie_moves["Wing Whack"] or
                                   self.kazooie_moves["Glide"],
            locationName.JIGGYJR6: lambda state: state.has(itemName.AUQAIM, self.player) and
                                                 state.has(itemName.GEGGS, self.player) and
                                                 self.can_reach_atlantis,
            locationName.JIGGYJR7: lambda state: (state.has(itemName.AUQAIM, self.player) and
                                                 state.has(itemName.GEGGS, self.player) and
                                                 self.can_reach_atlantis) or
                                                 self.can_transform["Sub"],
            locationName.JIGGYJR8: lambda state: state.has(itemName.TTORP, self.player) and
                                                 self.can_reach_atlantis,
            locationName.JIGGYJR9: lambda state: state.has(itemName.GEGGS, self.player) or
                                                 state.has(itemName.BDRILL, self.player),
            locationName.JIGGYJR10: lambda state: state.has(itemName.EGGAIM, self.player) and
                                                  state.has(itemName.IEGGS, self.player) and
                                                  state.has(itemName.TTORP, self.player),

            #Terrydactyland Jiggies
            locationName.JIGGYTD1: lambda state: (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.BDRILL, self.player)) and
                                                 self.can_beat_terry,
            locationName.JIGGYTD2: lambda state: self.region_rules[regionName.CC] and
                                                 state.has(itemName.TTORP, self.player),
            locationName.JIGGYTD3: lambda state: state.has(itemName.GEGGS, self.player) and
                                                 state.has(itemName.EGGAIM, self.player) and
                                                 state.has(itemName.GGRAB, self.player) and
                                                 self.jiggy_rules[locationName.JIGGYGM1] and
                                                 self.banjo_moves["Taxi Pack"] and
                                                 self.mumbo_magic["Heal"] and
                                                 state.has(itemName.BDRILL, self.player) and
                                                 self.mumbo_magic["Grow/Shrink"],
            locationName.JIGGYTD4: self.can_beat_terry,
            locationName.JIGGYTD5: self.oogle_boogles_open and
                                   self.has_fire and
                                   self.smuggle_food,
            locationName.JIGGYTD6: lambda state: state.has(itemName.BBLASTER, self.player),
            locationName.JIGGYTD7: self.can_beat_terry and
                                   self.kazooie_moves["Hatch"] and
                                   self.banjo_moves["Taxi Pack"] and
                                   self.oogle_boogles_open,
            locationName.JIGGYTD9: lambda state: state.has(itemName.EGGAIM, self.player) and
                                                 state.has(itemName.CEGGS, self.player),
            locationName.JIGGYTD10: self.can_transform["T-Rex"],

            #Grunty Industries Jiggies
            locationName.JIGGYGI1: self.can_beat_weldar and self.banjo_moves["Shack Pack"],
            locationName.JIGGYGI2: self.can_beat_weldar,
            locationName.JIGGYGI3: lambda state: self.mumbo_magic["EMP"] and
                                                 state.has(itemName.CLAWBTS, self.player) and
                                                 state.has(itemName.BBLASTER, self.player),
            locationName.JIGGYGI4: lambda state: self.can_transform["Washing Machine"] and
                                                 state.has(itemName.BDRILL, self.player),
            locationName.JIGGYGI5: self.can_reach_GI_2F,
            locationName.JIGGYGI6: lambda state: self.mumbo_magic["EMP"] and
                                                 state.has(itemName.GEGGS, self.player) and
                                                 state.has(itemName.EGGAIM, self.player) and
                                                 self.can_use_battery and
                                                 (self.can_transform["Washing Machine"] or
                                                  self.kazooie_moves["Leg Spring"]),
            locationName.JIGGYGI7: self.can_reach_GI_2F,
            locationName.JIGGYGI8: self.enter_GI and
                                   self.banjo_moves["Snooze Pack"],
            locationName.JIGGYGI9: self.can_reach_GI_2F and
                                   self.can_use_battery,
            locationName.JIGGYGI10: self.can_use_battery and self.GI_front_door,

            #Hailfire Peaks Jiggies
            locationName.JIGGYHP1: lambda state: state.has(itemName.FEGGS, self.player) and
                                                 state.has(itemName.IEGGS, self.player) and
                                                 state.has(itemName.CLAWBTS, self.player),
            locationName.JIGGYHP3: self.mumbo_magic["Revive"] and
                                   self.has_fire and
                                   self.banjo_moves["Taxi Pack"],
            locationName.JIGGYHP4: self.banjo_moves["Shack Pack"],
            locationName.JIGGYHP5: lambda state: self.jiggy_rules[locationName.JIGGYGM1] and
                                                 state.has(itemName.EGGAIM, self.player) and
                                                 state.has(itemName.GEGGS, self.player),
            locationName.JIGGYHP6: self.can_transform["Snowball"] and
                                   self.banjo_moves["Shack Pack"],
            locationName.JIGGYHP7: self.banjo_moves["Snooze Pack"],
            locationName.JIGGYHP8: lambda state: self.can_transform["Stony"] and
                                                 state.has(itemName.GEGGS, self.player),
            locationName.JIGGYHP9: lambda state: self.jiggy_rules[locationName.JIGGYJR10] and
                                                 self.mumbo_magic["Revive"] and
                                                 state.has(itemName.BDRILL, self.player) and
                                                 self.kazooie_moves["Hatch"],
            locationName.JIGGYHP10: lambda state: state.has(itemName.SPLITUP, self.player) and
                                                  state.has(itemName.CLAWBTS, self.player) and
                                                  state.has(itemName.GGRAB, self.player),

            #Cloud Cuckooland Jiggies
            locationName.JIGGYCC2: lambda state: state.has(itemName.BDRILL, self.player) and
                                                 state.has(itemName.SPRINGB, self.player) and
                                                 self.banjo_moves["Sack Pack"] and
                                                 self.grow_beanstalk and
                                                 self.can_use_floatus,
            locationName.JIGGYCC3: lambda state: state.has(itemName.FEGGS, self.player) and
                                                 state.has(itemName.GEGGS, self.player) and
                                                 state.has(itemName.IEGGS, self.player) and
                                                 self.mumbo_magic["Rain Dance"],
            locationName.JIGGYCC4: lambda state: self.can_transform["Detonator"] or
                                                 state.has(itemName.CEGGS, self.player),
            locationName.JIGGYCC5: self.can_transform["Bee"],
            locationName.JIGGYCC6: self.can_transform["Bee"],
            locationName.JIGGYCC7: self.banjo_moves["Sack Pack"] and
                                   self.grow_beanstalk and
                                   self.can_use_floatus,
            locationName.JIGGYCC8: self.kazooie_moves["Wing Whack"],
            locationName.JIGGYCC9: lambda state: state.has(itemName.CEGGS, self.player),
            locationName.JIGGYCC10: self.banjo_moves["Shack Pack"],

            #Jinjo Family Jiggies
            locationName.JIGGYIH1: self.region_rules[regionName.HP],
            locationName.JIGGYIH2: self.region_rules[regionName.HP],
            locationName.JIGGYIH3: self.region_rules[regionName.CC],
            locationName.JIGGYIH4: self.region_rules[regionName.CC],
            locationName.JIGGYIH5: self.region_rules[regionName.CC],
            locationName.JIGGYIH6: self.region_rules[regionName.CC],
            locationName.JIGGYIH7: self.region_rules[regionName.CC],
            locationName.JIGGYIH8: self.region_rules[regionName.CC],
            locationName.JIGGYIH9: self.region_rules[regionName.CC],
        }

    def jiggy_unlock(self, state: CollectionState, Amount) -> bool:
        return state.has_group("Jiggy", self.player, Amount)
        

    def set_rules(self) -> None:
        for region_name, rules in self.region_rules.items():
            region = self.world.multiworld.get_region(region_name, self.player)
            for entrance in region.entrances:
                entrance.access_rule = rules
        for location, rules in self.jiggy_rules.items():
            jiggy = self.world.multiworld.get_location(location, self.player)
            set_rule(jiggy, rules)


        self.world.multiworld.completion_condition[self.player] = lambda state: state.has("Kick Around", self.player)
