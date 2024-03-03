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
    #can_transform = {}
    mumbo_magic = []
    humba_magic = []
    solo_moves = []
    # banjo_moves = []
    # kazooie_moves = []
    jiggy_rules = {}



    def __init__(self, world: BanjoTooieWorld) -> None:
        self.player = world.player
        self.world = world

        self.mumbo_magic = [
            itemName.MUMBOMT,
            itemName.MUMBOGM,
            itemName.MUMBOWW,
            itemName.MUMBOIH,
            itemName.MUMBOJR,
            itemName.MUMBOTD,
            itemName.MUMBOGI,
            itemName.MUMBOHP,
            itemName.MUMBOCC
        ]

        self.humba_magic = [
            itemName.HUMBAMT,
            itemName.HUMBAGM,
            itemName.HUMBAWW,
            itemName.HUMBAIH,
            itemName.HUMBAJR,
            itemName.HUMBATD,
            itemName.HUMBAGI,
            itemName.HUMBAHP,
            itemName.HUMBACC
        ]

        self.solo_moves = [
            itemName.PACKWH,
            itemName.TAXPACK,
            itemName.SNPACK,
            itemName.SHPACK,
            itemName.SAPACK,
            itemName.WWHACK,
            itemName.HATCH,
            itemName.LSPRING,
            itemName.GLIDE
        ]

        # self.can_transform = {
        #     "Stony":           lambda state: state.has(itemName.HUMBAMT, self.player) and
        #                                      self.golden_goliath(state, itemName.MUMBOMT),
        #     "Detonator":       lambda state: state.has(itemName.HUMBAGM, self.player),
        #     "Money Van":       lambda state: state.has(itemName.HUMBAWW, self.player),
        #     "Sub":             lambda state: state.has(itemName.HUMBAJR, self.player) and
        #                                      self.can_reach_atlantis(state),
        #     "T-Rex":           lambda state: state.has(itemName.HUMBATD, self.player),
        #     "Washing Machine": lambda state: state.has(itemName.HUMBAGI, self.player) and
        #                                      self.can_reach_GI_2F(state),
        #     "Snowball":        lambda state: state.has(itemName.HUMBAHP, self.player),
        #     "Bee":             lambda state: state.has(itemName.HUMBACC, self.player),
        #     "Dragon":          lambda state: state.has(itemName.HUMBAIH, self.player)
        # }

        # self.mumbo_magic = {
        #     "Levitate":       lambda state: self.check_magic(state, itemName.MUMBOGM),
        #     "Power":          lambda state: self.check_magic(state, itemName.MUMBOWW) and
        #                                     self.can_transform["Money Van"],
        #     "Oxygenate":      lambda state: self.check_magic(state, itemName.MUMBOJR),
        #     "Grow/Shrink":    lambda state: self.check_magic(state, itemName.MUMBOTD),
        #     "EMP":            lambda state: self.check_magic(state, itemName.MUMBOGI) and
        #                                     self.can_reach_GI_2F(state),
        #     "Revive":         lambda state: self.check_magic(state, itemName.MUMBOHP),
        #     "Rain Dance":     lambda state: self.check_magic(state, itemName.MUMBOCC),
        #     "Heal":           lambda state: self.check_magic(state, itemName.MUMBOIH)
        # }

        # self.banjo_moves = {
        #     "Pack Whack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.PACKWH, self.player),
        #     "Taxi Pack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.TAXPACK, self.player),
        #     "Snooze Pack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.SNPACK, self.player),
        #     "Shack Pack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.SHPACK, self.player),
        #     "Sack Pack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.SAPACK, self.player),
        # }
        # self.kazooie_moves = {
        #     "Wing Whack": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.WWHACK, self.player),
        #     "Hatch": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.HATCH, self.player),
        #     "Leg Spring": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.LSPRING, self.player),
        #     "Glide": lambda state: state.has(itemName.SPLITUP, self.player) and state.has(itemName.GLIDE, self.player),
        # }

        self.region_rules = {
            regionName.IOHWH: lambda state: self.jiggy_unlock(state, 1),
            regionName.MT: lambda state: self.jiggy_unlock(state, 1),
            regionName.IOHPL: lambda state: state.has(itemName.GGRAB, self.player) or
                                            self.dilberta_free(state),
            regionName.GM: lambda state: self.jiggy_unlock(state, 4) or
                                         self.dilberta_free(state),
            regionName.IOHPG: lambda state: state.has(itemName.FEGGS, self.player),
            regionName.WW: lambda state: self.jiggy_unlock(state, 8),
            regionName.IOHCT: lambda state: state.has(itemName.SPLITUP, self.player),
            regionName.JR: lambda state: self.jiggy_unlock(state, 14),
            regionName.IOHWL: lambda state: state.has(itemName.TTORP, self.player),
            regionName.TL: lambda state: self.jiggy_unlock(state, 20),
            regionName.IOHQM: lambda state: state.has(itemName.SPRINGB, self.player),
            regionName.GI: lambda state: self.jiggy_unlock(state, 28),
            regionName.HP: lambda state: self.jiggy_unlock(state, 36),
            regionName.CC: lambda state: self.jiggy_unlock(state, 45),
            regionName.CK: lambda state: self.jiggy_unlock(state, 55) and state.has(itemName.CLAWBTS, self.player),
            regionName.H1: lambda state: self.jiggy_unlock(state, 70) and
                                         (self.check_solo_moves(state, itemName.PACKWH) or self.check_solo_moves(state, itemName.SAPACK)) and
                                         (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)) and
                                         state.has(itemName.BBLASTER, self.player) and
                                         state.has(itemName.CEGGS, self.player)
        }
        self.jiggy_rules = {
            #Mayahem Temple Jiggies
            locationName.JIGGYMT1: lambda state: state.has(itemName.BBLASTER, self.player),
            locationName.JIGGYMT2: lambda state: state.has(itemName.BBLASTER, self.player),
            locationName.JIGGYMT3: lambda state: self.check_humba_magic(state, itemName.HUMBAMT) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOMT),
            locationName.JIGGYMT4: lambda state: state.has(itemName.EGGAIM, self.player) or
                                                 self.MT_flight_pad(state),
            locationName.JIGGYMT5: lambda state: state.has(itemName.EGGAIM,  self.player) and
                                                 state.has(itemName.GGRAB, self.player) or
                                                 self.MT_flight_pad(state),
            #locationName.JIGGYMT6: self.mumbo_magic["Golden Goliath"],
            locationName.JIGGYMT6: lambda state: self.check_mumbo_magic(state, itemName.MUMBOMT),
            locationName.JIGGYMT7: lambda state: state.has(itemName.GGRAB, self.player) and
                                                 self.prison_compound_open(state),
            locationName.JIGGYMT8: lambda state: state.has(itemName.BDRILL, self.player) and
                                                 self.prison_compound_open(state),
            locationName.JIGGYMT10: lambda state: state.has(itemName.GGRAB, self.player) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOMT),
            #Glitter Gulch Mine Jiggies
            locationName.JIGGYGM1: lambda state: self.check_mumbo_magic(state, itemName.MUMBOGM),
            locationName.JIGGYGM2: lambda state: self.canary_mary_free(state),
            locationName.JIGGYGM5: lambda state: state.has(itemName.BBLASTER, self.player) and
                                                 state.has(itemName.BBAYONET, self.player) and
                                                 self.GM_boulders(state),
            locationName.JIGGYGM6: lambda state: self.dilberta_free(state),
            locationName.JIGGYGM7: lambda state: self.check_mumbo_magic(state, itemName.MUMBOGM),
            locationName.JIGGYGM8: lambda state: state.has(itemName.SPRINGB, self.player) or
                                                 state.has(itemName.CEGGS, self.player),
            locationName.JIGGYGM9: lambda state: self.GM_boulders(state),

            #Witchyworld Jiggies
            locationName.JIGGYWW1: lambda state: state.has(itemName.SPLITUP, self.player),
            locationName.JIGGYWW2: lambda state: self.check_humba_magic(state, itemName.HUMBAWW) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOWW),
            locationName.JIGGYWW3: lambda state: state.has(itemName.AIREAIM, self.player) and
                                                 self.can_kill_fruity(state),
            locationName.JIGGYWW4: lambda state: self.check_humba_magic(state, itemName.HUMBAGM) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOWW) and
                                                 self.saucer_door_open(state),
            locationName.JIGGYWW5: lambda state: state.has(itemName.SPLITUP, self.player) and
                                                 state.has(itemName.AIREAIM, self.player),
            locationName.JIGGYWW7: lambda state: self.check_humba_magic(state, itemName.HUMBAWW) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOWW) and
                                                 self.check_solo_moves(state, itemName.TAXPACK),
            locationName.JIGGYWW8: lambda state: self.check_mumbo_magic(state, itemName.MUMBOWW) and
                                                 self.check_humba_magic(state, itemName.HUMBAWW),
            locationName.JIGGYWW9: lambda state: self.check_humba_magic(state, itemName.HUMBAWW),
            locationName.JIGGYWW10: lambda state: state.has(itemName.BDRILL, self.player) and
                                                  state.has(itemName.GEGGS, self.player),

            #Jolly Joger's Lagoon Jiggies
            locationName.JIGGYJR1: lambda state: self.check_humba_magic(state, itemName.HUMBAJR) and
                                                 self.can_reach_atlantis(state),
            locationName.JIGGYJR2: lambda state: self.check_solo_moves(state, itemName.HATCH) and
                                                  state.has(itemName.GEGGS, self.player),
            locationName.JIGGYJR3: lambda state: self.can_reach_atlantis(state) and
                                                 (state.has(itemName.AUQAIM, self.player) or
                                                  self.check_humba_magic(state, itemName.HUMBAJR)),
            locationName.JIGGYJR4: lambda state: (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.BDRILL, self.player)) and
                                                 self.region_rules[regionName.CC] and
                                                 state.has(itemName.SPLITUP, self.player),
            locationName.JIGGYJR5: lambda state: self.check_solo_moves(state, itemName.WWHACK) or
                                                 self.check_solo_moves(state, itemName.GLIDE),
            locationName.JIGGYJR6: lambda state: state.has(itemName.AUQAIM, self.player) and
                                                 state.has(itemName.GEGGS, self.player) and
                                                 self.can_reach_atlantis(state),
            locationName.JIGGYJR7: lambda state: (state.has(itemName.AUQAIM, self.player) and
                                                 state.has(itemName.GEGGS, self.player) and
                                                 self.can_reach_atlantis(state)) or
                                                 (self.check_humba_magic(state, itemName.HUMBAJR) and
                                                  self.can_reach_atlantis(state)),
            locationName.JIGGYJR8: lambda state: state.has(itemName.TTORP, self.player) and
                                                 self.can_reach_atlantis(state),
            locationName.JIGGYJR9: lambda state: state.has(itemName.GEGGS, self.player) or
                                                 state.has(itemName.BDRILL, self.player),
            locationName.JIGGYJR10: lambda state: state.has(itemName.EGGAIM, self.player) and
                                                  state.has(itemName.IEGGS, self.player) and
                                                  state.has(itemName.TTORP, self.player),

            #Terrydactyland Jiggies
            locationName.JIGGYTD1: lambda state: (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.BDRILL, self.player)) and
                                                 self.can_beat_terry(state),
            locationName.JIGGYTD2: lambda state: self.region_rules[regionName.CC] and
                                                 state.has(itemName.TTORP, self.player),
            locationName.JIGGYTD3: lambda state: state.has(itemName.GEGGS, self.player) and
                                                 state.has(itemName.EGGAIM, self.player) and
                                                 state.has(itemName.GGRAB, self.player) and
                                                 self.can_beat_king_coal(state) and
                                                 self.check_solo_moves(state, itemName.TAXPACK) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOIH) and
                                                 state.has(itemName.BDRILL, self.player) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOTD),
            locationName.JIGGYTD4: lambda state: self.can_beat_terry(state),
            locationName.JIGGYTD5: lambda state: self.oogle_boogles_open(state) and
                                                 self.has_fire(state) and
                                                 self.smuggle_food(state),
            locationName.JIGGYTD6: lambda state: state.has(itemName.BBLASTER, self.player),
            locationName.JIGGYTD7: lambda state: self.can_beat_terry(state) and
                                                 self.check_solo_moves(state, itemName.HATCH) and
                                                 self.check_solo_moves(state, itemName.TAXPACK) and
                                                 self.oogle_boogles_open(state),
            locationName.JIGGYTD9: lambda state: state.has(itemName.EGGAIM, self.player) and
                                                 state.has(itemName.CEGGS, self.player),
            locationName.JIGGYTD10: lambda state: self.check_humba_magic(state, itemName.HUMBATD),

            #Grunty Industries Jiggies
            locationName.JIGGYGI1: lambda state: self.can_beat_weldar(state) and self.check_solo_moves(state, itemName.SHPACK),
            locationName.JIGGYGI2: lambda state: self.can_beat_weldar(state),
            locationName.JIGGYGI3: lambda state: self.check_mumbo_magic(state, itemName.MUMBOGI) and
                                                 state.has(itemName.CLAWBTS, self.player) and
                                                 state.has(itemName.BBLASTER, self.player),
            locationName.JIGGYGI4: lambda state: self.check_humba_magic(state, itemName.HUMBAGI) and
                                                 self.can_reach_GI_2F(state) and
                                                 state.has(itemName.BDRILL, self.player),
            locationName.JIGGYGI5: lambda state: self.can_reach_GI_2F(state),
            locationName.JIGGYGI6: lambda state: self.check_mumbo_magic(state, itemName.MUMBOGI) and
                                                 self.can_reach_GI_2F(state) and
                                                 state.has(itemName.GEGGS, self.player) and
                                                 state.has(itemName.EGGAIM, self.player) and
                                                 self.can_use_battery(state) and
                                                 (self.check_humba_magic(state, itemName.HUMBAGI) or
                                                  self.check_solo_moves(state, itemName.LSPRING)),
            locationName.JIGGYGI7: lambda state: self.can_reach_GI_2F(state),
            locationName.JIGGYGI8: lambda state: self.enter_GI(state) and
                                                 self.check_solo_moves(state, itemName.SNPACK),
            locationName.JIGGYGI9: lambda state: self.can_reach_GI_2F(state) and
                                                 self.can_use_battery(state),
            locationName.JIGGYGI10: lambda state: self.can_use_battery(state) and
                                                  self.GI_front_door(state),

            #Hailfire Peaks Jiggies
            locationName.JIGGYHP1: lambda state: state.has(itemName.FEGGS, self.player) and
                                                 state.has(itemName.IEGGS, self.player) and
                                                 state.has(itemName.CLAWBTS, self.player),
            locationName.JIGGYHP3: lambda state: self.check_mumbo_magic(state, itemName.MUMBOHP) and
                                                 self.has_fire(state) and
                                                 self.check_solo_moves(state, itemName.TAXPACK),
            locationName.JIGGYHP4: lambda state: self.check_solo_moves(state, itemName.SHPACK),
            locationName.JIGGYHP5: lambda state: self.can_beat_king_coal(state) and
                                                 state.has(itemName.EGGAIM, self.player) and
                                                 state.has(itemName.GEGGS, self.player),
            locationName.JIGGYHP6: lambda state: self.check_humba_magic(state, itemName.HUMBAHP) and
                                                 self.check_solo_moves(state, itemName.SHPACK),
            locationName.JIGGYHP7: lambda state: self.check_solo_moves(state, itemName.SNPACK),
            locationName.JIGGYHP8: lambda state: self.check_humba_magic(state, itemName.HUMBAMT) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOMT) and
                                                 state.has(itemName.GEGGS, self.player),
            locationName.JIGGYHP9: lambda state: self.jiggy_rules[locationName.JIGGYJR10] and
                                                 self.check_mumbo_magic(state, itemName.MUMBOHP) and
                                                 state.has(itemName.BDRILL, self.player) and
                                                 self.check_solo_moves(state, itemName.HATCH),
            locationName.JIGGYHP10: lambda state: state.has(itemName.SPLITUP, self.player) and
                                                  state.has(itemName.CLAWBTS, self.player) and
                                                  state.has(itemName.GGRAB, self.player),

            #Cloud Cuckooland Jiggies
            locationName.JIGGYCC2: lambda state: state.has(itemName.BDRILL, self.player) and
                                                 state.has(itemName.SPRINGB, self.player) and
                                                 self.check_solo_moves(state, itemName.SAPACK) and
                                                 self.grow_beanstalk(state) and
                                                 self.can_use_floatus(state),
            locationName.JIGGYCC3: lambda state: state.has(itemName.FEGGS, self.player) and
                                                 state.has(itemName.GEGGS, self.player) and
                                                 state.has(itemName.IEGGS, self.player) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOCC),
            locationName.JIGGYCC4: lambda state: self.canary_mary_free(state),
            locationName.JIGGYCC5: lambda state: self.check_humba_magic(state, itemName.HUMBACC),
            locationName.JIGGYCC6: lambda state: self.check_humba_magic(state, itemName.HUMBACC),
            locationName.JIGGYCC7: lambda state: self.check_solo_moves(state, itemName.SAPACK) and
                                                 self.grow_beanstalk(state) and
                                                 self.can_use_floatus(state),
            locationName.JIGGYCC8: lambda state: self.check_solo_moves(state, itemName.WWHACK),
            locationName.JIGGYCC9: lambda state: state.has(itemName.CEGGS, self.player),
            locationName.JIGGYCC10: lambda state: self.check_solo_moves(state, itemName.SHPACK),

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

    def check_mumbo_magic(self, state: CollectionState, name) -> bool:
        for item_name in self.mumbo_magic:
            if name == item_name:
                return state.has(name, self.player)
    
    def check_humba_magic(self, state: CollectionState, name) -> bool:
        for item_name in self.humba_magic:
            if name == item_name:
                return state.has(name, self.player)
            
    def check_solo_moves(self, state: CollectionState, name) -> bool:
        for item_name in self.solo_moves:
            if name == item_name:
                return state.has(name, self.player) and state.has(itemName.SPLITUP, self.player)
    
    def has_fire(self, state: CollectionState) -> bool:
        return state.has(itemName.FEGGS, self.player) or self.check_humba_magic(state, itemName.HUMBAIH)

    def long_swim(self, state: CollectionState) -> bool:
        return state.has(itemName.BDRILL, self.player) or self.check_mumbo_magic(state, itemName.MUMBOJR)

    def can_reach_atlantis(self, state: CollectionState) -> bool:
        return state.has(itemName.IEGGS, self.player) and self.long_swim(state) and state.has(itemName.AUQAIM, self.player)

    def MT_flight_pad(self, state: CollectionState) -> bool:
        return state.has(itemName.BDRILL, self.player) or self.check_mumbo_magic(state, itemName.MUMBOMT)

    def prison_compound_open(self, state: CollectionState) -> bool:
        return state.has(itemName.GEGGS, self.player) or \
               state.has(itemName.CEGGS, self.player) or \
               self.check_mumbo_magic(state, itemName.MUMBOMT)

    def dilberta_free(self, state: CollectionState) -> bool:
        return self.prison_compound_open(state) and \
               self.check_humba_magic(state, itemName.HUMBAMT) and \
               self.check_mumbo_magic(state, itemName.MUMBOMT) and \
               state.has(itemName.BDRILL, self.player)

    def GM_boulders(self, state: CollectionState) -> bool:
        return state.has(itemName.BDRILL, self.player) or self.check_humba_magic(state, itemName.HUMBAGM)

    def canary_mary_free(self, state: CollectionState) -> bool:
        return self.check_humba_magic(state, itemName.HUMBAGM) or state.has(itemName.CEGGS, self.player)

    def can_beat_king_coal(self, state) -> bool:
        return self.check_mumbo_magic(state, itemName.MUMBOGM)

    def can_kill_fruity(self, state: CollectionState) -> bool:
        return state.has(itemName.GEGGS, self.player) or \
               state.has(itemName.CEGGS, self.player) or \
               self.check_humba_magic(state, itemName.HUMBAWW)

    def saucer_door_open(self, state: CollectionState) -> bool:
        return (state.has(itemName.GGRAB, self.player) or (state.has(itemName.EGGAIM, self.player))) \
               and (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player))

    def can_beat_terry(self, state: CollectionState) -> bool:
        return state.has(itemName.EGGAIM, self.player) and state.has(itemName.SPRINGB, self.player)

    def smuggle_food(self, state: CollectionState) -> bool:
        return (self.can_beat_king_coal(state) and
                state.has(itemName.GGRAB, self.player)) or \
                state.has(itemName.CLAWBTS, self.player)

    def oogle_boogles_open(self, state) -> bool:
        return self.check_humba_magic(state, itemName.HUMBATD) and self.check_mumbo_magic(state, itemName.MUMBOTD)

    def enter_GI(self, state: CollectionState) -> bool:
        return self.can_beat_king_coal(state) or state.has(itemName.CLAWBTS, self.player)

    def GI_front_door(self, state: CollectionState) -> bool:
        return self.enter_GI(state) and state.has(itemName.SPLITUP, self.player)

    def can_reach_GI_2F(self, state: CollectionState) -> bool:
        return state.has(itemName.CLAWBTS, self.player) or \
               (self.GI_front_door(state) and
                self.check_solo_moves(state, itemName.LSPRING) and
                self.check_solo_moves(state, itemName.GLIDE) and
                (self.check_solo_moves(state, itemName.WWHACK) or
                state.has(itemName.EGGAIM, self.player)))

    def can_beat_weldar(self, state: CollectionState) -> bool:
        return self.enter_GI(state) and \
               self.can_use_battery(state) and \
               self.check_mumbo_magic(state, itemName.MUMBOGI) and \
               self.can_reach_GI_2F(state) and \
               self.check_humba_magic(state, itemName.HUMBAGI) and \
               (state.has(itemName.FEGGS, self.player) or
                state.has(itemName.GEGGS, self.player) or
                state.has(itemName.CEGGS, self.player))

    def can_use_battery(self, state) -> bool:
        return self.check_solo_moves(state, itemName.PACKWH) and self.check_solo_moves(state, itemName.TAXPACK)

    def can_use_floatus(self, state) -> bool:
        return self.check_solo_moves(state, itemName.TAXPACK) and self.check_solo_moves(state, itemName.HATCH)

    def grow_beanstalk(self, state: CollectionState) -> bool:
        return state.has(itemName.BDRILL, self.player) and self.check_mumbo_magic(state, itemName.MUMBOCC)

    def set_rules(self) -> None:
        for region_name, rules in self.region_rules.items():
            region = self.world.multiworld.get_region(region_name, self.player)
            for entrance in region.entrances:
                entrance.access_rule = rules
        for location, rules in self.jiggy_rules.items():
            jiggy = self.world.multiworld.get_location(location, self.player)
            set_rule(jiggy, rules)

        self.world.multiworld.completion_condition[self.player] = lambda state: state.has("Kick Around", self.player)
