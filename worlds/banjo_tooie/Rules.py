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
    jinjo_forbid = []
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

        self.jinjo_forbid = [
            itemName.MUMBOMT,
            itemName.BDRILL,
            itemName.GGRAB,
            itemName.BBLASTER,
            itemName.FEGGS,
            itemName.TTORP,
            itemName.IEGGS,
            itemName.AUQAIM,
            itemName.HUMBAGM,
            itemName.EGGAIM,
            itemName.GEGGS,
            itemName.HUMBAWW,
            itemName.CEGGS,
            itemName.MUMBOTD,
            itemName.HUMBATD,
            itemName.SPLITUP,
            itemName.HUMBAGI,
            itemName.AIREAIM,
            itemName.HUMBAHP,
            itemName.SHPACK,
            itemName.SPRINGB,
            itemName.CLAWBTS,
            itemName.GLIDE,
            itemName.LSPRING,
            itemName.MUMBOGM
        ]


        self.region_rules = {
            regionName.IOHWH: lambda state: state.has(itemName.JIGGY, self.player, 1),
            regionName.MT: lambda state: state.has(itemName.JIGGY, self.player, 1),
            regionName.IOHPL: lambda state: state.has(itemName.GGRAB, self.player) or
                                            self.dilberta_free(state),
            regionName.GM: lambda state: state.has(itemName.JIGGY, self.player, 4) or
                                         self.dilberta_free(state),
            regionName.IOHPG: lambda state: state.has(itemName.FEGGS, self.player),
            regionName.WW: lambda state: state.has(itemName.JIGGY, self.player, 8),
            regionName.IOHCT: lambda state: state.has(itemName.SPLITUP, self.player),
            regionName.JR: lambda state: state.has(itemName.JIGGY, self.player, 14),
            regionName.IOHWL: lambda state: state.has(itemName.TTORP, self.player),
            regionName.TL: lambda state: state.has(itemName.JIGGY, self.player, 20),
            regionName.IOHQM: lambda state: state.has(itemName.SPRINGB, self.player),
            regionName.GI: lambda state: state.has(itemName.JIGGY, self.player, 28),
            regionName.HP: lambda state: state.has(itemName.JIGGY, self.player, 36),
            regionName.CC: lambda state: state.has(itemName.JIGGY, self.player, 45),
            regionName.CK: lambda state: state.has(itemName.JIGGY, self.player, 55) and state.has(itemName.CLAWBTS, self.player),
            regionName.H1: lambda state: state.has(itemName.JIGGY, self.player, 70) and
                                         (self.check_solo_moves(state, itemName.PACKWH) or self.check_solo_moves(state, itemName.SAPACK)) and
                                         #(self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)) and
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
                                                 (self.MT_flight_pad(state) and 
                                                  state.has(itemName.AIREAIM, self.player)),
            locationName.JIGGYMT5: lambda state: state.has(itemName.EGGAIM,  self.player) and
                                                 state.has(itemName.GGRAB, self.player) or
                                                 self.MT_flight_pad(state),
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
            locationName.JIGGYGM3: lambda state: self.has_fire(state),
            locationName.JIGGYGM5: lambda state: state.has(itemName.BBLASTER, self.player) and
                                                 state.has(itemName.BBAYONET, self.player) and
                                                 self.GM_boulders(state),
            locationName.JIGGYGM6: lambda state: self.dilberta_free(state),
            locationName.JIGGYGM7: lambda state: self.check_mumbo_magic(state, itemName.MUMBOGM),
            locationName.JIGGYGM8: lambda state: state.has(itemName.SPRINGB, self.player) or
                                                 (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)),
            locationName.JIGGYGM9: lambda state: self.GM_boulders(state) and
                                                 (state.has(itemName.SPLITUP, self.player) or
                                                  self.has_fire(state)),

            #Witchyworld Jiggies
            locationName.JIGGYWW1: lambda state: state.has(itemName.SPLITUP, self.player) and
                                                 (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player)),
            locationName.JIGGYWW2: lambda state: self.check_humba_magic(state, itemName.HUMBAWW) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOWW),
            locationName.JIGGYWW3: lambda state: state.has(itemName.AIREAIM, self.player) and
                                                 state.has(itemName.EGGAIM, self.player) and
                                                 state.has(itemName.GEGGS, self.player),
            locationName.JIGGYWW4: lambda state: self.check_humba_magic(state, itemName.HUMBAGM) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOWW) and
                                                 self.check_humba_magic(state, itemName.HUMBAWW) and
                                                 self.saucer_door_open(state),
            locationName.JIGGYWW5: lambda state: state.has(itemName.SPLITUP, self.player) and
                                                 state.has(itemName.AIREAIM, self.player) and
                                                 (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player)),
            locationName.JIGGYWW7: lambda state: self.check_humba_magic(state, itemName.HUMBAWW) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOWW) and
                                                 self.check_solo_moves(state, itemName.TAXPACK) and
                                                 (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player)),
            locationName.JIGGYWW8: lambda state: self.check_mumbo_magic(state, itemName.MUMBOWW) and
                                                 self.check_humba_magic(state, itemName.HUMBAWW),
            locationName.JIGGYWW9: lambda state: self.check_humba_magic(state, itemName.HUMBAWW) and
                                                 state.has(itemName.SPLITUP, self.player),
            locationName.JIGGYWW10: lambda state: state.has(itemName.BDRILL, self.player) and
                                                  state.has(itemName.GEGGS, self.player),

            #Jolly Joger's Lagoon Jiggies
            locationName.JIGGYJR1: lambda state: self.check_humba_magic(state, itemName.HUMBAJR) and
                                                 self.can_reach_atlantis(state),
            locationName.JIGGYJR2: lambda state: self.check_solo_moves(state, itemName.HATCH) and
                                                 (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player)),
            locationName.JIGGYJR3: lambda state: self.can_reach_atlantis(state),
            locationName.JIGGYJR4: lambda state: (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player) or
                                                  state.has(itemName.BDRILL, self.player)) and
                                                 self.HFP_hot_water_cooled(state),
            locationName.JIGGYJR5: lambda state: state.has(itemName.SPLITUP, self.player) and
                                                 self.check_solo_moves(state, itemName.GLIDE),
            locationName.JIGGYJR6: lambda state: state.has(itemName.AUQAIM, self.player) and
                                                 self.can_reach_atlantis(state),
            locationName.JIGGYJR7: lambda state: state.has(itemName.AUQAIM, self.player) and
                                                 state.has(itemName.GEGGS, self.player) and
                                                 self.can_reach_atlantis(state) and
                                                 (self.check_mumbo_magic(state, itemName.MUMBOJR) or
                                                  self.check_humba_magic(state, itemName.HUMBAJR)),
            locationName.JIGGYJR8: lambda state: state.has(itemName.TTORP, self.player) and
                                                 self.can_reach_atlantis(state),
            locationName.JIGGYJR9: lambda state: (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player)) and
                                                 state.has(itemName.SPLITUP, self.player),
            locationName.JIGGYJR10: lambda state: state.has(itemName.EGGAIM, self.player) and
                                                  state.has(itemName.IEGGS, self.player) and
                                                  state.has(itemName.TTORP, self.player),

            #Terrydactyland Jiggies
            locationName.JIGGYTD1: lambda state: (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.BDRILL, self.player) or
                                                  state.has(itemName.CEGGS, self.player)) and
                                                 self.can_beat_terry(state),
            locationName.JIGGYTD2: lambda state: state.has(itemName.TTORP, self.player),
            locationName.JIGGYTD3: lambda state: state.has(itemName.GEGGS, self.player) and
                                                 self.WW_train_station(state) and
                                                 self.check_solo_moves(state, itemName.TAXPACK) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOIH) and
                                                 state.has(itemName.BDRILL, self.player) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOTD),
            locationName.JIGGYTD4: lambda state: self.can_beat_terry(state),
            locationName.JIGGYTD5: lambda state: self.oogle_boogles_open(state) and
                                                 self.has_fire(state) and
                                                 self.smuggle_food(state) and
                                                 state.has(itemName.BDRILL, self.player) and
                                                 state.has(itemName.GGRAB, self.player),
            locationName.JIGGYTD6: lambda state: state.has(itemName.BBLASTER, self.player),
            locationName.JIGGYTD7: lambda state: self.can_beat_terry(state) and
                                                 self.check_solo_moves(state, itemName.HATCH) and
                                                 self.check_solo_moves(state, itemName.TAXPACK) and
                                                 self.oogle_boogles_open(state),
            locationName.JIGGYTD8: lambda state: state.has(itemName.IEGGS, self.player) and
                                                 state.has(itemName.SPRINGB, self.player),
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
            locationName.JIGGYGI5: lambda state: self.can_reach_GI_2F(state) and state.has(itemName.SPLITUP, self.player),
            locationName.JIGGYGI6: lambda state: self.check_mumbo_magic(state, itemName.MUMBOGI) and
                                                 self.can_reach_GI_2F(state) and
                                                 (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player)) and
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
                                                 state.has(itemName.GEGGS, self.player) and
                                                 state.has(itemName.FEGGS, self.player) and
                                                 self.check_humba_magic(state, itemName.HUMBAHP),
            locationName.JIGGYHP6: lambda state: self.check_humba_magic(state, itemName.HUMBAHP) and
                                                 self.check_solo_moves(state, itemName.SHPACK) and
                                                 (self.check_solo_moves(state, itemName.PACKWH) or
                                                  state.has(itemName.GGRAB, self.player)),
            locationName.JIGGYHP7: lambda state: self.check_solo_moves(state, itemName.SNPACK) and
                                                 state.has(itemName.IEGGS, self.player) and
                                                 state.has(itemName.SPRINGB, self.player),
            locationName.JIGGYHP8: lambda state: self.check_humba_magic(state, itemName.HUMBAMT) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOMT) and
                                                 (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player) or
                                                  self.check_mumbo_magic(state, itemName.MUMBOHP)),
            locationName.JIGGYHP9: lambda state: state.has(itemName.EGGAIM, self.player) and
                                                 state.has(itemName.IEGGS, self.player) and
                                                 state.has(itemName.TTORP, self.player) and
                                                 self.check_mumbo_magic(state, itemName.MUMBOHP) and
                                                 state.has(itemName.BDRILL, self.player) and
                                                 self.check_solo_moves(state, itemName.HATCH) and
                                                 (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)),
            locationName.JIGGYHP10: lambda state: state.has(itemName.SPLITUP, self.player) and
                                                  state.has(itemName.GGRAB, self.player),

            #Cloud Cuckooland Jiggies
            locationName.JIGGYCC2: lambda state: state.has(itemName.SPRINGB, self.player) and
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
                                                 self.can_use_floatus(state) and
                                                 self.check_solo_moves(state, itemName.SHPACK),
            locationName.JIGGYCC8: lambda state: self.check_solo_moves(state, itemName.WWHACK),
            locationName.JIGGYCC9: lambda state: state.has(itemName.CEGGS, self.player),
            locationName.JIGGYCC10: lambda state: self.check_solo_moves(state, itemName.SHPACK),

            #Jinjo Family Jiggies
            #locationName.JIGGYIH1: lambda state: state.has(itemName.JIGGY, self.player, 36),
            #locationName.JIGGYIH2: lambda state: state.has(itemName.JIGGY, self.player, 36),
            #locationName.JIGGYIH3: lambda state: state.has(itemName.JIGGY, self.player, 45),
            #locationName.JIGGYIH4: lambda state: state.has(itemName.JIGGY, self.player, 45),
            #locationName.JIGGYIH5: lambda state: state.has(itemName.JIGGY, self.player, 45),
            #locationName.JIGGYIH6: lambda state: state.has(itemName.JIGGY, self.player, 45),
            #locationName.JIGGYIH7: lambda state: state.has(itemName.JIGGY, self.player, 45),
            #locationName.JIGGYIH8: lambda state: state.has(itemName.JIGGY, self.player, 45),
            #locationName.JIGGYIH9: lambda state: state.has(itemName.JIGGY, self.player, 45),

            # locationName.JIGGYIH1: lambda state: self.jiggy_unlock(state, 36) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOMT) and
            #                                      state.has(itemName.BDRILL, self.player) and
            #                                      state.has(itemName.GGRAB, self.player) and
            #                                      state.has(itemName.BBLASTER, self.player) and
            #                                      state.has(itemName.FEGGS, self.player) and
            #                                      state.has(itemName.TTORP, self.player) and
            #                                      state.has(itemName.IEGGS, self.player) and
            #                                      state.has(itemName.AUQAIM, self.player) and
            #                                      self.can_reach_atlantis(state) and
            #                                      self.check_humba_magic(state, itemName.HUMBAGM) and
            #                                      state.has(itemName.GEGGS, self.player) and
            #                                      state.has(itemName.CEGGS, self.player) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOTD) and
            #                                      self.check_humba_magic(state, itemName.HUMBATD) and
            #                                      state.has(itemName.SPLITUP, self.player) and
            #                                      self.can_reach_GI_2F(state) and
            #                                      state.has(itemName.AIREAIM, self.player) and
            #                                      self.check_solo_moves(state, itemName.SHPACK) and
            #                                      state.has(itemName.SPRINGB, self.player),
            # locationName.JIGGYIH2: lambda state: self.jiggy_unlock(state, 36) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOMT) and
            #                                      state.has(itemName.BDRILL, self.player) and
            #                                      state.has(itemName.GGRAB, self.player) and
            #                                      state.has(itemName.BBLASTER, self.player) and
            #                                      state.has(itemName.FEGGS, self.player) and
            #                                      state.has(itemName.TTORP, self.player) and
            #                                      state.has(itemName.IEGGS, self.player) and
            #                                      state.has(itemName.AUQAIM, self.player) and
            #                                      self.can_reach_atlantis(state) and
            #                                      self.check_humba_magic(state, itemName.HUMBAGM) and
            #                                      state.has(itemName.EGGAIM, self.player) and
            #                                      state.has(itemName.GEGGS, self.player) and
            #                                      self.check_humba_magic(state, itemName.HUMBAWW) and
            #                                      state.has(itemName.CEGGS, self.player) and
            #                                      state.has(itemName.SPLITUP, self.player) and
            #                                      self.can_reach_GI_2F(state) and
            #                                      state.has(itemName.AIREAIM, self.player) and
            #                                      self.check_solo_moves(state, itemName.SHPACK) and
            #                                      self.check_humba_magic(state, itemName.HUMBAHP) and
            #                                      state.has(itemName.SPRINGB, self.player),
            # locationName.JIGGYIH3: lambda state: self.jiggy_unlock(state, 45) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOMT) and
            #                                      state.has(itemName.BDRILL, self.player) and
            #                                      state.has(itemName.GGRAB, self.player) and
            #                                      state.has(itemName.BBLASTER, self.player) and
            #                                      state.has(itemName.FEGGS, self.player) and
            #                                      state.has(itemName.TTORP, self.player) and
            #                                      state.has(itemName.IEGGS, self.player) and
            #                                      state.has(itemName.AUQAIM, self.player) and
            #                                      self.can_reach_atlantis(state) and
            #                                      self.check_humba_magic(state, itemName.HUMBAGM) and
            #                                      state.has(itemName.EGGAIM, self.player) and
            #                                      state.has(itemName.GEGGS, self.player) and
            #                                      self.check_humba_magic(state, itemName.HUMBAWW) and
            #                                      state.has(itemName.CEGGS, self.player) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOTD) and
            #                                      self.check_humba_magic(state, itemName.HUMBATD) and
            #                                      state.has(itemName.SPLITUP, self.player) and
            #                                      self.check_humba_magic(itemName.HUMBAGI, self.player) and
            #                                      self.can_reach_GI_2F(state) and
            #                                      self.check_solo_moves(state, itemName.LSPRING) and
            #                                      state.has(itemName.AIREAIM, self.player) and
            #                                      self.check_humba_magic(state, itemName.HUMBAHP) and
            #                                      self.check_solo_moves(state, itemName.GLIDE) and
            #                                      state.has(itemName.SPRINGB, self.player) and
            #                                      state.has(itemName.CLAWBTS, self.player),
            # locationName.JIGGYIH4: lambda state: self.jiggy_unlock(state, 45) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOMT) and
            #                                      state.has(itemName.BDRILL, self.player) and
            #                                      state.has(itemName.GGRAB, self.player) and
            #                                      state.has(itemName.BBLASTER, self.player) and
            #                                      state.has(itemName.FEGGS, self.player) and
            #                                      state.has(itemName.TTORP, self.player) and
            #                                      state.has(itemName.IEGGS, self.player) and
            #                                      state.has(itemName.AUQAIM, self.player) and
            #                                      self.can_reach_atlantis(state) and
            #                                      self.check_humba_magic(state, itemName.HUMBAGM) and
            #                                      state.has(itemName.EGGAIM, self.player) and
            #                                      state.has(itemName.GEGGS, self.player) and
            #                                      self.check_humba_magic(state, itemName.HUMBAWW) and
            #                                      state.has(itemName.CEGGS, self.player) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOTD) and
            #                                      self.check_humba_magic(state, itemName.HUMBATD) and
            #                                      state.has(itemName.SPLITUP, self.player) and
            #                                      self.check_humba_magic(itemName.HUMBAGI, self.player) and
            #                                      self.can_reach_GI_2F(state) and
            #                                      self.check_solo_moves(state, itemName.LSPRING) and
            #                                      state.has(itemName.AIREAIM, self.player) and
            #                                      self.check_solo_moves(state, itemName.SHPACK) and
            #                                      self.check_humba_magic(state, itemName.HUMBAHP) and
            #                                      self.check_solo_moves(state, itemName.GLIDE) and
            #                                      state.has(itemName.SPRINGB, self.player) and
            #                                      state.has(itemName.CLAWBTS, self.player),
            # locationName.JIGGYIH5: lambda state: self.jiggy_unlock(state, 45) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOMT) and
            #                                      state.has(itemName.BDRILL, self.player) and
            #                                      state.has(itemName.GGRAB, self.player) and
            #                                      state.has(itemName.BBLASTER, self.player) and
            #                                      state.has(itemName.FEGGS, self.player) and
            #                                      state.has(itemName.TTORP, self.player) and
            #                                      state.has(itemName.IEGGS, self.player) and
            #                                      state.has(itemName.AUQAIM, self.player) and
            #                                      self.can_reach_atlantis(state) and
            #                                      self.check_humba_magic(state, itemName.HUMBAGM) and
            #                                      state.has(itemName.EGGAIM, self.player) and
            #                                      state.has(itemName.GEGGS, self.player) and
            #                                      self.check_humba_magic(state, itemName.HUMBAWW) and
            #                                      state.has(itemName.CEGGS, self.player) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOTD) and
            #                                      self.check_humba_magic(state, itemName.HUMBATD) and
            #                                      state.has(itemName.SPLITUP, self.player) and
            #                                      self.check_humba_magic(itemName.HUMBAGI, self.player) and
            #                                      self.can_reach_GI_2F(state) and
            #                                      self.check_solo_moves(state, itemName.LSPRING) and
            #                                      state.has(itemName.AIREAIM, self.player) and
            #                                      self.check_solo_moves(state, itemName.SHPACK) and
            #                                      self.check_humba_magic(state, itemName.HUMBAHP) and
            #                                      self.check_solo_moves(state, itemName.GLIDE) and
            #                                      state.has(itemName.SPRINGB, self.player) and
            #                                      state.has(itemName.CLAWBTS, self.player),
            # locationName.JIGGYIH6: lambda state: self.jiggy_unlock(state, 45) and
            #                                      state.has(itemName.BDRILL, self.player) and
            #                                      state.has(itemName.GGRAB, self.player) and
            #                                      state.has(itemName.BBLASTER, self.player) and
            #                                      state.has(itemName.FEGGS, self.player) and
            #                                      state.has(itemName.TTORP, self.player) and
            #                                      state.has(itemName.IEGGS, self.player) and
            #                                      state.has(itemName.AUQAIM, self.player) and
            #                                      self.can_reach_atlantis(state) and
            #                                      self.check_humba_magic(state, itemName.HUMBAGM) and
            #                                      state.has(itemName.EGGAIM, self.player) and
            #                                      state.has(itemName.GEGGS, self.player) and
            #                                      self.check_humba_magic(state, itemName.HUMBAWW) and
            #                                      state.has(itemName.CEGGS, self.player) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOTD) and
            #                                      self.check_humba_magic(state, itemName.HUMBATD) and
            #                                      state.has(itemName.SPLITUP, self.player) and
            #                                      self.check_humba_magic(itemName.HUMBAGI, self.player) and
            #                                      self.can_reach_GI_2F(state) and
            #                                      self.check_solo_moves(state, itemName.LSPRING) and
            #                                      state.has(itemName.AIREAIM, self.player) and
            #                                      self.check_solo_moves(state, itemName.SHPACK) and
            #                                      self.check_humba_magic(state, itemName.HUMBAHP) and
            #                                      state.has(itemName.SPRINGB, self.player) and
            #                                      state.has(itemName.CLAWBTS, self.player),
            # locationName.JIGGYIH7: lambda state: self.jiggy_unlock(state, 45) and
            #                                      state.has(itemName.BDRILL, self.player) and
            #                                      state.has(itemName.GGRAB, self.player) and
            #                                      state.has(itemName.BBLASTER, self.player) and
            #                                      state.has(itemName.FEGGS, self.player) and
            #                                      state.has(itemName.TTORP, self.player) and
            #                                      state.has(itemName.IEGGS, self.player) and
            #                                      state.has(itemName.AUQAIM, self.player) and
            #                                      self.can_reach_atlantis(state) and
            #                                      self.check_humba_magic(state, itemName.HUMBAGM) and
            #                                      state.has(itemName.EGGAIM, self.player) and
            #                                      state.has(itemName.GEGGS, self.player) and
            #                                      self.check_humba_magic(state, itemName.HUMBAWW) and
            #                                      state.has(itemName.CEGGS, self.player) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOTD) and
            #                                      self.check_humba_magic(state, itemName.HUMBATD) and
            #                                      state.has(itemName.SPLITUP, self.player) and
            #                                      self.check_humba_magic(itemName.HUMBAGI, self.player) and
            #                                      self.can_reach_GI_2F(state) and
            #                                      self.check_solo_moves(state, itemName.LSPRING) and
            #                                      state.has(itemName.AIREAIM, self.player) and
            #                                      self.check_solo_moves(state, itemName.SHPACK) and
            #                                      self.check_humba_magic(state, itemName.HUMBAHP) and
            #                                      self.check_solo_moves(state, itemName.GLIDE) and
            #                                      state.has(itemName.SPRINGB, self.player) and
            #                                      state.has(itemName.CLAWBTS, self.player),
            # locationName.JIGGYIH8: lambda state: self.jiggy_unlock(state, 45) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOMT) and
            #                                      state.has(itemName.BDRILL, self.player) and
            #                                      state.has(itemName.GGRAB, self.player) and
            #                                      state.has(itemName.BBLASTER, self.player) and
            #                                      state.has(itemName.FEGGS, self.player) and
            #                                      state.has(itemName.TTORP, self.player) and
            #                                      state.has(itemName.IEGGS, self.player) and
            #                                      state.has(itemName.AUQAIM, self.player) and
            #                                      self.can_reach_atlantis(state) and
            #                                      self.check_humba_magic(state, itemName.HUMBAGM) and
            #                                      state.has(itemName.EGGAIM, self.player) and
            #                                      state.has(itemName.GEGGS, self.player) and
            #                                      self.check_humba_magic(state, itemName.HUMBAWW) and
            #                                      state.has(itemName.CEGGS, self.player) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOTD) and
            #                                      self.check_humba_magic(state, itemName.HUMBATD) and
            #                                      state.has(itemName.SPLITUP, self.player) and
            #                                      self.check_humba_magic(itemName.HUMBAGI, self.player) and
            #                                      self.can_reach_GI_2F(state) and
            #                                      self.check_solo_moves(state, itemName.LSPRING) and
            #                                      state.has(itemName.AIREAIM, self.player) and
            #                                      self.check_solo_moves(state, itemName.SHPACK) and
            #                                      self.check_humba_magic(state, itemName.HUMBAHP) and
            #                                      self.check_solo_moves(state, itemName.GLIDE) and
            #                                      state.has(itemName.SPRINGB, self.player) and
            #                                      state.has(itemName.CLAWBTS, self.player),
            # locationName.JIGGYIH9: lambda state: self.jiggy_unlock(state, 45) and
            #                                      state.has(itemName.BDRILL, self.player) and
            #                                      state.has(itemName.GGRAB, self.player) and
            #                                      state.has(itemName.BBLASTER, self.player) and
            #                                      state.has(itemName.FEGGS, self.player) and
            #                                      state.has(itemName.TTORP, self.player) and
            #                                      state.has(itemName.IEGGS, self.player) and
            #                                      state.has(itemName.AUQAIM, self.player) and
            #                                      self.can_reach_atlantis(state) and
            #                                      self.check_humba_magic(state, itemName.HUMBAGM) and
            #                                      state.has(itemName.EGGAIM, self.player) and
            #                                      state.has(itemName.GEGGS, self.player) and
            #                                      self.check_humba_magic(state, itemName.HUMBAWW) and
            #                                      state.has(itemName.CEGGS, self.player) and
            #                                      self.check_mumbo_magic(state, itemName.MUMBOTD) and
            #                                      self.check_humba_magic(state, itemName.HUMBATD) and
            #                                      state.has(itemName.SPLITUP, self.player) and
            #                                      self.check_humba_magic(itemName.HUMBAGI, self.player) and
            #                                      self.can_reach_GI_2F(state) and
            #                                      self.check_solo_moves(state, itemName.LSPRING) and
            #                                      state.has(itemName.AIREAIM, self.player) and
            #                                      self.check_solo_moves(state, itemName.SHPACK) and
            #                                      self.check_humba_magic(state, itemName.HUMBAHP) and
            #                                      self.check_solo_moves(state, itemName.GLIDE) and
            #                                      state.has(itemName.SPRINGB, self.player) and
            #                                      state.has(itemName.CLAWBTS, self.player),
        }
        self.cheato_rules = {
            locationName.CHEATOMT1: lambda state: self.MT_flight_pad(state) or (state.has(itemName.EGGAIM, self.player) and state.has(itemName.GGRAB, self.player)),
            locationName.CHEATOMT2: lambda state: self.prison_compound_open(state) and state.has(itemName.GGRAB, self.player),
            locationName.CHEATOMT3: lambda state: self.check_mumbo_magic(state, itemName.MUMBOMT) and state.has(itemName.GGRAB, self.player),

            locationName.CHEATOGM1: lambda state: self.canary_mary_free(state),
            locationName.CHEATOGM3: lambda state: state.has(itemName.GGRAB, self.player),

            locationName.CHEATOWW1: lambda state: state.has(itemName.GGRAB, self.player) or 
                                                  (self.check_solo_moves(state, itemName.LSPRING) and 
                                                  (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE))),
            locationName.CHEATOWW2: lambda state: self.check_humba_magic(state, itemName.HUMBAWW),
            locationName.CHEATOWW3: lambda state: self.check_humba_magic(state, itemName.HUMBAGM) and
                                                  self.check_mumbo_magic(state, itemName.MUMBOWW) and
                                                  self.check_humba_magic(state, itemName.HUMBAWW) and
                                                  self.saucer_door_open(state),
                                            
            locationName.CHEATOJR1: lambda state: self.has_enough_doubloons(state, 28),
            locationName.CHEATOJR2: lambda state: (self.long_swim(state) or
                                                   state.has(itemName.GEGGS, self.player) or
                                                   state.has(itemName.CEGGS, self.player)) and
                                                  state.has(itemName.TTORP, self.player),
            locationName.CHEATOJR3: lambda state: self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player) and
                                                  (self.check_solo_moves(state, itemName.GLIDE) or self.check_solo_moves(state, itemName.LSPRING) or
                                                   self.check_solo_moves(state, itemName.WWHACK) or
                                                  (self.check_solo_moves(state, itemName.PACKWH) and state.has(itemName.GGRAB, self.player))),

            locationName.CHEATOTL1: lambda state: state.has(itemName.JIGGY, self.player, 45) and state.has(itemName.SPRINGB, self.player) and
                                                  state.has(itemName.TTORP, self.player),
            locationName.CHEATOTL2: lambda state: self.check_humba_magic(state, itemName.HUMBATD),
            locationName.CHEATOTL3: lambda state: state.has(itemName.BDRILL, self.player) and 
                                                  (state.has(itemName.GGRAB, self.player) or self.can_beat_terry(state)),

            locationName.CHEATOGI1: lambda state: state.has(itemName.GEGGS, self.player) and
                                                  self.enter_GI(state),
            locationName.CHEATOGI2: lambda state: self.can_reach_GI_2F(state),
            locationName.CHEATOGI3: lambda state: self.can_beat_weldar(state),

            locationName.CHEATOHP1: lambda state: state.has(itemName.CLAWBTS, self.player) and
                                                  (state.has(itemName.GEGGS, self.player) or
                                                   state.has(itemName.CEGGS, self.player) or
                                                   self.check_mumbo_magic(state, itemName.MUMBOHP)),
            locationName.CHEATOHP2: lambda state: state.has(itemName.CEGGS, self.player) or self.check_solo_moves(state, itemName.SHPACK),
            locationName.CHEATOHP3: lambda state: state.has(itemName.SPLITUP, self.player),

            locationName.CHEATOCC1: lambda state: self.canary_mary_free(state),
            locationName.CHEATOCC2: lambda state: state.has(itemName.FEGGS, self.player) and
                                                  state.has(itemName.GEGGS, self.player) and
                                                  state.has(itemName.IEGGS, self.player) and
                                                  self.check_mumbo_magic(state, itemName.MUMBOCC),
            locationName.CHEATOCC3: lambda state: self.check_humba_magic(state, itemName.HUMBACC)
        }
        self.honey_rules = {
            locationName.HONEYCMT1: lambda state: (self.check_humba_magic(state, itemName.HUMBAMT) and
                                                   self.check_mumbo_magic(state, itemName.MUMBOMT)) or
                                                  state.has(itemName.CEGGS, self.player),
            locationName.HONEYCMT2: lambda state: self.MT_flight_pad(state) or state.has(itemName.GGRAB, self.player),
            locationName.HONEYCMT3: lambda state: self.MT_flight_pad(state) or state.has(itemName.EGGAIM, self.player),

            locationName.HONEYCGM1: lambda state: self.GM_boulders(state),
            locationName.HONEYCGM2: lambda state: self.GM_boulders(state),

            locationName.HONEYCWW1: lambda state: state.has(itemName.GGRAB, self.player),
            locationName.HONEYCWW2: lambda state: self.check_humba_magic(state, itemName.HUMBAWW),
            locationName.HONEYCWW3: lambda state: state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player),

            locationName.HONEYCJR1: lambda state: self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player),
            locationName.HONEYCJR2: lambda state: self.can_reach_atlantis(state),
            locationName.HONEYCJR3: lambda state: (state.has(itemName.GEGGS, self.player) or state.has(itemName.BDRILL, self.player) or
                                                    state.has(itemName.CEGGS, self.player)) and
                                                   (state.has(itemName.GGRAB, self.player) or 
                                                    (state.has(itemName.SPLITUP, self.player) and self.check_solo_moves(state, itemName.LSPRING) and
                                                     (self.check_solo_moves(state, itemName.GLIDE) or self.check_solo_moves(state, itemName.WWHACK)))),
                                                
            locationName.HONEYCTL2: lambda state: state.has(itemName.BDRILL, self.player) and state.has(itemName.SPLITUP, self.player),

            locationName.HONEYCGI1: lambda state: self.can_reach_GI_2F(state) and
                                                  (state.has(itemName.GGRAB, self.player) or state.has(itemName.SPLITUP, self.player)),
            locationName.HONEYCGI2: lambda state: self.enter_GI(state) and (state.has(itemName.GGRAB, self.player) or state.has(itemName.SPLITUP, self.player)),
            locationName.HONEYCGI3: lambda state: self.can_reach_GI_2F(state),

            locationName.HONEYCHP1: lambda state: (state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or
                                                  state.has(itemName.SPLITUP, self.player),
            locationName.HONEYCHP2: lambda state: state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.LSPRING) or
                                                  self.check_solo_moves(state, itemName.GLIDE),
            locationName.HONEYCHP3: lambda state: state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.GLIDE) or
                                                  (self.check_solo_moves(state, itemName.LSPRING) and self.check_solo_moves(state, itemName.WWHACK)),

            locationName.HONEYCCC1: lambda state: state.has(itemName.BDRILL, self.player)

        }
        self.glowbo_rules = {
            locationName.GLOWBOMT2: lambda state: self.check_mumbo_magic(state, itemName.MUMBOMT),
            locationName.GLOWBOWW1: lambda state: self.check_humba_magic(state, itemName.HUMBAWW),
            locationName.GLOWBOJR2: lambda state: self.can_reach_atlantis(state),
            locationName.GLOWBOGI1: lambda state: self.can_reach_GI_2F(state),
            locationName.GLOWBOGI2: lambda state: self.can_reach_GI_2F(state),
            locationName.GLOWBOMEG: lambda state: state.has(itemName.GGRAB, self.player) and state.has(itemName.TTORP, self.player)

        }
        self.doubloon_rules = {
            #Alcove
            locationName.JRLDB22:   lambda state: state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player)),
            locationName.JRLDB23:   lambda state: state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player)),
            locationName.JRLDB24:   lambda state: state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player)),
            #Underground
            locationName.JRLDB19:   lambda state: state.has(itemName.BDRILL, self.player) or state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player),
            locationName.JRLDB20:   lambda state: state.has(itemName.BDRILL, self.player) or state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player),
            locationName.JRLDB21:   lambda state: state.has(itemName.BDRILL, self.player) or state.has(itemName.GEGGS, self.player) or
                                                  state.has(itemName.CEGGS, self.player),
        }

        self.silo_rules = {
            locationName.EGGAIM: lambda state: self.has_enough_notes(state, 25),
            locationName.BBLASTER: lambda state: self.has_enough_notes(state, 30),
            locationName.GGRAB: lambda state: self.check_mumbo_magic(state, itemName.MUMBOMT) and self.has_enough_notes(state, 35),

            locationName.BDRILL: lambda state: self.has_enough_notes(state, 85),
            locationName.BBAYONET: lambda state: self.GM_boulders(state) and self.has_enough_notes(state, 95),

            locationName.AIREAIM: lambda state: self.has_enough_notes(state, 180),
            locationName.SPLITUP: lambda state: self.has_enough_notes(state, 160),
            locationName.PACKWH: lambda state: state.has(itemName.SPLITUP, self.player) and self.has_enough_notes(state, 120),

            locationName.AUQAIM: lambda state: (state.has(itemName.GEGGS, self.player) or self.has_enough_doubloons(state, 28)) and
                                               self.has_enough_notes(state, 275),
            locationName.TTORP: lambda state:  self.can_reach_atlantis(state) and state.has(itemName.GGRAB, self.player) and
                                               self.has_enough_notes(state, 290),
            locationName.WWHACK: lambda state: state.has(itemName.GEGGS, self.player) and state.has(itemName.SPLITUP, self.player) and
                                               self.has_enough_notes(state, 265),

            locationName.SPRINGB: lambda state: self.has_enough_notes(state, 390),
            locationName.TAXPACK: lambda state: state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GGRAB, self.player)) or
                                                self.check_solo_moves(state, itemName.PACKWH) and self.has_enough_notes(state, 405),
            locationName.HATCH: lambda state:   state.has(itemName.SPLITUP, self.player) and self.has_enough_notes(state, 420),

            locationName.SNPACK: lambda state:  self.enter_GI(state) and self.can_use_battery(state) and self.has_enough_notes(state, 525),
            locationName.LSPRING: lambda state: self.can_reach_GI_2F(state) and self.has_enough_notes(state, 545) and
                                                ((state.has(itemName.SPLITUP, self.player)
                                                and state.has(itemName.CLAWBTS, self.player)) or
                                                self.check_solo_moves(state, itemName.WWHACK) or 
                                                self.check_solo_moves(state, itemName.LSPRING) or
                                                self.check_solo_moves(state, itemName.GLIDE)),
            locationName.CLAWBTS: lambda state: self.enter_GI(state) and self.has_enough_notes(state, 505),

            locationName.SHPACK: lambda state: state.has(itemName.SPLITUP, self.player) and self.has_enough_notes(state, 640),
            locationName.GLIDE: lambda state: state.has(itemName.SPLITUP, self.player) and self.has_enough_notes(state, 660),

            locationName.SAPACK: lambda state: self.check_solo_moves(state, itemName.SHPACK) and self.has_enough_notes(state, 765),

            locationName.FEGGS: lambda state: self.has_enough_notes(state, 45),
            locationName.GEGGS: lambda state: self.has_enough_notes(state, 110),
            locationName.IEGGS: lambda state: self.has_enough_notes(state, 200),
            locationName.CEGGS: lambda state: self.has_enough_notes(state, 315),
        }

    # def jiggy_unlock(self, state: CollectionState, Amount) -> bool:
    #     return state.has_group("Jiggy", self.player, Amount)

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

    def has_enough_notes(self, state: CollectionState, Amount) -> bool:
        count:int = 0
        if state.has(itemName.JIGGY, self.player, 1): # MT Access
            count += 100
        if state.has(itemName.GGRAB, self.player): # JV Treble + Plateau Sign
            count += 30
        if state.has(itemName.GGRAB, self.player) or self.dilberta_free(state): # Honey B.
            count += 10
            if state.has(itemName.JIGGY, self.player, 4) or self.dilberta_free(state): # GGM Access
                count += 100
            if state.has(itemName.FEGGS, self.player): # Pine Grove Access
                count += 20
                if state.has(itemName.JIGGY, self.player, 8): # WW Access
                    count += 70
                    if state.has(itemName.GEGGS, self.player) or state.has(itemName.GEGGS, self.player) or \
                        self.check_solo_moves(state, itemName.GLIDE) or self.check_solo_moves(state, itemName.LSPRING): # Area 51 Fence
                            count += 10
                    if self.check_humba_magic(state, itemName.HUMBAWW): # Van Door
                        count += 20
                if state.has(itemName.TTORP, self.player): # Wasteland Access
                    count += 20
                    if state.has(itemName.JIGGY, self.player, 20): # TDL Access
                        count += 80
                        if state.has(itemName.BDRILL, self.player) and state.has(itemName.GGRAB, self.player): # Boulder Treble Clef
                            count += 20
                    if state.has(itemName.JIGGY, self.player, 45): # CCL Access
                        count += 90
                        if state.has(itemName.CEGGS, self.player) or state.has(itemName.SHPACK, self.player): # Sack Pack Notes
                            count += 10
                    if state.has(itemName.SPRINGB, self.player) and state.has(itemName.JIGGY, self.player, 28) and self.enter_GI(state): # GI 1F
                        count += 25
                        if self.can_reach_GI_2F(state): # Rest of GI
                            count += 75
            if state.has(itemName.SPLITUP, self.player): # Cliff Top
                count += 20
            if state.has(itemName.JIGGY, self.player, 14): # JRL Town Center
                count += 60
                if state.has(itemName.AUQAIM, self.player) or state.has(itemName.TTORP, self.player): # Squid Notes
                    count += 10
                if self.can_reach_atlantis(state): # Deep JRL
                    count += 30
            if state.has(itemName.JIGGY, self.player, 36): # HFP Access
                count += 80
                if state.has(itemName.EGGAIM, self.player) and state.has(itemName.GEGGS, self.player): # Icicle Grotto
                            count += 20
        return count >= Amount

    def has_enough_doubloons(self, state:CollectionState, Amount) -> bool:
        return  state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player) and \
                state.has(itemName.SPLITUP, self.player) and state.has(itemName.DOUBLOON, self.player, Amount)

    def has_fire(self, state: CollectionState) -> bool:
        return state.has(itemName.FEGGS, self.player) or self.check_humba_magic(state, itemName.HUMBAIH)

    def long_swim(self, state: CollectionState) -> bool:
        return state.has(itemName.BDRILL, self.player) or self.check_mumbo_magic(state, itemName.MUMBOJR)

    def can_reach_atlantis(self, state: CollectionState) -> bool:
        return state.has(itemName.IEGGS, self.player) and self.long_swim(state) and state.has(itemName.AUQAIM, self.player)

    def MT_flight_pad(self, state: CollectionState) -> bool:
        return state.has(itemName.BDRILL, self.player) or self.check_mumbo_magic(state, itemName.MUMBOMT)

    def prison_compound_open(self, state: CollectionState) -> bool:
        return state.has(itemName.JIGGY, self.player, 1) and \
               (state.has(itemName.GEGGS, self.player) or
                state.has(itemName.CEGGS, self.player) or
                self.check_mumbo_magic(state, itemName.MUMBOMT))

    def dilberta_free(self, state: CollectionState) -> bool:
        return self.prison_compound_open(state) and \
               self.check_humba_magic(state, itemName.HUMBAMT) and \
               self.check_mumbo_magic(state, itemName.MUMBOMT) and \
               state.has(itemName.BDRILL, self.player)

    def GM_boulders(self, state: CollectionState) -> bool:
        return state.has(itemName.BDRILL, self.player) or self.check_humba_magic(state, itemName.HUMBAGM)

    def canary_mary_free(self, state: CollectionState) -> bool:
        return self.check_humba_magic(state, itemName.HUMBAGM)

    def can_beat_king_coal(self, state) -> bool:
        return self.check_mumbo_magic(state, itemName.MUMBOGM)

    def WW_train_station(self, state) -> bool:
        return self.can_beat_king_coal(state) and \
            (state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.LSPRING))

    #deprecated but might be useful for ticket randomization
    def can_kill_fruity(self, state: CollectionState) -> bool:
        return state.has(itemName.GEGGS, self.player) or \
               state.has(itemName.CEGGS, self.player) or \
               self.check_humba_magic(state, itemName.HUMBAWW)

    def saucer_door_open(self, state: CollectionState) -> bool:
        return (state.has(itemName.GGRAB, self.player) or state.has(itemName.EGGAIM, self.player) or
                (self.check_solo_moves(state, itemName.GLIDE) and self.check_solo_moves(state, itemName.LSPRING))) \
               and (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player))

    def can_beat_terry(self, state: CollectionState) -> bool:
        return state.has(itemName.EGGAIM, self.player) and state.has(itemName.SPRINGB, self.player)

    def smuggle_food(self, state: CollectionState) -> bool:
        return state.has(itemName.CLAWBTS, self.player)

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
                state.has(itemName.GEGGS, self.player) and \
                state.has(itemName.BDRILL, self.player)

    def can_use_battery(self, state) -> bool:
        return self.check_solo_moves(state, itemName.PACKWH) and self.check_solo_moves(state, itemName.TAXPACK)

    def HFP_hot_water_cooled(self, state) -> bool:
        return state.has(itemName.JIGGY, self.player, 45) and \
               state.has(itemName.SPLITUP, self.player) and \
               state.has(itemName.FEGGS, self.player) and \
               state.has(itemName.TTORP, self.player)

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

        for location, rules in self.honey_rules.items():
            honeycomb = self.world.multiworld.get_location(location, self.player)
            set_rule(honeycomb, rules)

        for location, rules in self.cheato_rules.items():
            cheato = self.world.multiworld.get_location(location, self.player)
            set_rule(cheato, rules)
        
        for location, rules in self.glowbo_rules.items():
            glowbo = self.world.multiworld.get_location(location, self.player)
            set_rule(glowbo, rules)

        for location, rules in self.silo_rules.items():
            silo = self.world.multiworld.get_location(location, self.player)
            set_rule(silo, rules)

        for location, rules in self.doubloon_rules.items():
            doubloon = self.world.multiworld.get_location(location, self.player)
            set_rule(doubloon, rules)

        # for item in self.jinjo_forbid:
        #     forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH1, self.player), item, self.player)
        #     forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH2, self.player), item, self.player)
        #     forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH3, self.player), item, self.player)
        #     forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH4, self.player), item, self.player)
        #     forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH5, self.player), item, self.player)
        #     forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH6, self.player), item, self.player)
        #     forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH7, self.player), item, self.player)
        #     forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH8, self.player), item, self.player)
        #     forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH9, self.player), item, self.player)

        self.world.multiworld.completion_condition[self.player] = lambda state: state.has("Kick Around", self.player)
