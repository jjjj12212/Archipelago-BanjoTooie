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
    moves_forbid = []
    magic_forbid = []
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

        self.moves_forbid = [
            itemName.GGRAB,
            itemName.BBLASTER,
            itemName.EGGAIM,
            itemName.FEGGS,
            itemName.BDRILL,
            itemName.BBAYONET,
            itemName.GEGGS,
            itemName.AIREAIM,
            itemName.SPLITUP,
            itemName.PACKWH,
            itemName.IEGGS,
            itemName.WWHACK,
            itemName.TTORP,
            itemName.AUQAIM,
            itemName.CEGGS,
            itemName.SPRINGB,
            itemName.TAXPACK,
            itemName.HATCH,
            itemName.SNPACK,
            itemName.LSPRING,
            itemName.CLAWBTS,
            itemName.SHPACK,
            itemName.GLIDE,
            itemName.SAPACK,
        ]

        self.magic_forbid = {
            itemName.MUMBOMT,
            itemName.MUMBOGM,
            itemName.MUMBOWW,
            itemName.MUMBOJR,
            itemName.MUMBOTD,
            itemName.MUMBOGI,
            itemName.MUMBOHP,
            itemName.MUMBOCC,
            itemName.MUMBOIH,

            itemName.HUMBAMT,
            itemName.HUMBAGM,
            itemName.HUMBAWW,
            itemName.HUMBAJR,
            itemName.HUMBATD,
            itemName.HUMBAGI,
            itemName.HUMBAHP,
            itemName.HUMBACC,
            itemName.HUMBAIH,
        }

        self.jinjo_forbid = [
            itemName.WJINJO,
            itemName.OJINJO,
            itemName.YJINJO,
            itemName.BRJINJO,
            itemName.GJINJO,
            itemName.RJINJO,
            itemName.BLJINJO,
            itemName.PJINJO,
            itemName.BKJINJO,
        ]

        self.region_rules = {
            regionName.MT: lambda state: self.can_access_mt(state),
            regionName.IOHPL: lambda state: self.can_access_plateau(state),
            regionName.GM: lambda state: self.can_access_GM(state),
            regionName.IOHPG: lambda state: self.can_access_pinegrove(state, False),
            regionName.WW: lambda state: self.can_access_witchyworld(state, False),
            regionName.IOHCT: lambda state: self.can_access_clifftop(state, False),
            regionName.JR: lambda state: self.can_access_jrl(state),
            regionName.IOHWL: lambda state: self.can_access_wasteland(state, False),
            regionName.TL: lambda state: self.can_access_tdl(state, False),
            regionName.IOHQM: lambda state: self.can_access_quagmire(state, False),
            regionName.GIO: lambda state: self.can_access_gruntyindustries_outside(state, False),
            regionName.HP: lambda state: self.can_access_hailfire(state, False),
            regionName.CC: lambda state: self.can_access_ccl(state),
            regionName.CK: lambda state: self.can_access_ck(state),
            regionName.H1: lambda state: self.check_hag1_options(state)
        }

        self.access_rules = {
            locationName.MTA: lambda state: state.has(itemName.JIGGY, self.player, 99)
        }

        self.station_rules = {
            regionName.IOHCTS:  lambda state: state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWIH, self.player),
            regionName.TLS:     lambda state: state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWTD, self.player),
            regionName.GIS:     lambda state: state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWGI, self.player),
            regionName.HPLS:    lambda state: state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player),
            regionName.WWS:     lambda state: state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWWW, self.player),
            regionName.HPIS:    lambda state: state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player) and
                                              state.has(itemName.TRAINSWHP2, self.player) and state.has(itemName.GEGGS, self.player) and
                                              state.has(itemName.TRAINSWWW, self.player),
        }
        self.train_rules = {
            locationName.CHUFFY: lambda state: self.can_beat_king_coal(state),
            locationName.TRAINSWIH: lambda state: state.has(itemName.GGRAB, self.player),
            locationName.TRAINSWHP2: lambda state: self.check_humba_magic(state, itemName.HUMBAHP),
            locationName.TRAINSWHP1: lambda state: self.tswitch_lavaside(state),
            locationName.TRAINSWWW: lambda state: self.tswitch_ww(state)
        }

        self.jiggy_rules = {
            #Mayahem Temple Jiggies
            locationName.JIGGYMT1:  lambda state: self.jiggy_targitzan(state),
            locationName.JIGGYMT2:  lambda state: self.jiggy_sschamber(state),
            locationName.JIGGYMT3:  lambda state: self.jiggy_mayhem_kickball(state),
            locationName.JIGGYMT4:  lambda state: self.jiggy_bovina(state),
            locationName.JIGGYMT5:  lambda state: self.jiggy_treasure_chamber(state),
            locationName.JIGGYMT6:  lambda state: self.jiggy_golden_goliath(state),
            locationName.JIGGYMT7:  lambda state: self.jiggy_prison_quicksand(state),
            locationName.JIGGYMT8:  lambda state: self.jiggy_pillars(state),
            locationName.JIGGYMT10: lambda state: self.jiggy_ssslumber(state),

            #Glitter Gulch Mine Jiggies
            locationName.JIGGYGM1: lambda state: self.can_beat_king_coal(state),
            locationName.JIGGYGM2: lambda state: self.canary_mary_free(state),
            locationName.JIGGYGM3: lambda state: self.jiggy_generator_cavern(state),
            locationName.JIGGYGM5: lambda state: self.jiggy_ordnance_storage(state),
            locationName.JIGGYGM6: lambda state: self.dilberta_free(state),
            locationName.JIGGYGM7: lambda state: self.jiggy_crushing_shed(state),
            locationName.JIGGYGM8: lambda state: self.jiggy_waterfall(state),
            locationName.JIGGYGM9: lambda state: self.jiggy_power_hut(state),
            locationName.JIGGYGM10: lambda state: self.jiggy_flooded_caves(state),

            #Witchyworld Jiggies
            locationName.JIGGYWW1:  lambda state: self.jiggy_hoop_hurry(state),
            locationName.JIGGYWW2:  lambda state: self.jiggy_dodgem(state),
            locationName.JIGGYWW3:  lambda state: self.jiggy_patches(state),
            locationName.JIGGYWW4:  lambda state: self.jiggy_peril(state),
            locationName.JIGGYWW5:  lambda state: self.jiggy_balloon_burst(state),
            locationName.JIGGYWW6:  lambda state: self.jiggy_death_dive(state),
            locationName.JIGGYWW7:  lambda state: self.jiggy_mrs_boggy(state),
            locationName.JIGGYWW8:  lambda state: self.jiggy_star_spinner(state),
            locationName.JIGGYWW9:  lambda state: self.jiggy_inferno(state),
            locationName.JIGGYWW10: lambda state: self.jiggy_cactus(state),

            #Jolly Joger's Lagoon Jiggies
            locationName.JIGGYJR1:  lambda state: self.jiggy_sub_challenge(state),
            locationName.JIGGYJR2:  lambda state: self.jiggy_tiptup(state),
            locationName.JIGGYJR3:  lambda state: self.jiggy_bacon(state),
            locationName.JIGGYJR4:  lambda state: self.jiggy_pigpool(state),
            locationName.JIGGYJR5:  lambda state: self.jiggy_smuggler(state),
            locationName.JIGGYJR6:  lambda state: self.jiggy_merry_maggie(state),
            locationName.JIGGYJR7:  lambda state: self.jiggy_lord_woo(state),
            locationName.JIGGYJR8:  lambda state: self.jiggy_see_mee(state),
            locationName.JIGGYJR9:  lambda state: state.has(itemName.DOUBLOON, self.player, 23),
            locationName.JIGGYJR10: lambda state: self.jiggy_ufo(state),

            #Terrydactyland Jiggies
            locationName.JIGGYTD1:  lambda state: self.jiggy_terry_nest(state),
            locationName.JIGGYTD2:  lambda state: self.jiggy_dippy(state),
            locationName.JIGGYTD3:  lambda state: self.jiggy_scrotty(state),
            locationName.JIGGYTD4:  lambda state: self.can_beat_terry(state),
            locationName.JIGGYTD5:  lambda state: self.jiggy_oogle_boogle(state),
            locationName.JIGGYTD6:  lambda state: state.has(itemName.BBLASTER, self.player),
            locationName.JIGGYTD7:  lambda state: self.jiggy_terry_kids(state),
            locationName.JIGGYTD8:  lambda state: self.jiggy_stomping_plains(state),
            locationName.JIGGYTD9:  lambda state: self.jiggy_rocknuts(state),
            locationName.JIGGYTD10: lambda state: self.check_humba_magic(state, itemName.HUMBATD),

            #Grunty Industries Jiggies
            locationName.JIGGYGI1: lambda state: self.can_beat_weldar(state) and self.check_solo_moves(state, itemName.SHPACK),
            locationName.JIGGYGI2: lambda state: self.can_beat_weldar(state),
            locationName.JIGGYGI3: lambda state: self.check_mumbo_magic(state, itemName.MUMBOGI) and
                                                 state.has(itemName.CLAWBTS, self.player) and
                                                 state.has(itemName.BBLASTER, self.player),
            locationName.JIGGYGI4: lambda state: self.jiggy_skivvy(state),
            locationName.JIGGYGI5: lambda state: state.has(itemName.SPLITUP, self.player),
            locationName.JIGGYGI6: lambda state: self.jiggy_qa(state),
            locationName.JIGGYGI7: lambda state: state.has(itemName.SPLITUP, self.player),
            locationName.JIGGYGI8: lambda state: self.jiggy_compactor(state),
            locationName.JIGGYGI9: lambda state: self.jiggy_twinkly(state),
            locationName.JIGGYGI10: lambda state: self.jiggy_plantbox(state),

            #Hailfire Peaks Jiggies
            locationName.JIGGYHP1:  lambda state: self.jiggy_dragons_bros(state),
            locationName.JIGGYHP3:  lambda state: self.jiggy_sabreman(state),
            locationName.JIGGYHP4:  lambda state: self.check_solo_moves(state, itemName.SHPACK),
            locationName.JIGGYHP5:  lambda state: self.jiggy_ice_station(state),
            locationName.JIGGYHP6:  lambda state: self.jiggy_oil_drill(state),
            locationName.JIGGYHP7:  lambda state: self.jiggy_hfp_stomping(state),
            locationName.JIGGYHP8:  lambda state: self.jiggy_hfp_kickball(state),
            locationName.JIGGYHP9:  lambda state: self.jiggy_aliens(state),
            locationName.JIGGYHP10: lambda state: self.jiggy_colosseum_split(state),

            #Cloud Cuckooland Jiggies
            locationName.JIGGYCC2: lambda state: self.jiggy_mr_fit(state),
            locationName.JIGGYCC3: lambda state: self.jiggy_gold_pot(state),
            locationName.JIGGYCC4: lambda state: self.canary_mary_free(state),
            locationName.JIGGYCC5: lambda state: self.check_humba_magic(state, itemName.HUMBACC),
            locationName.JIGGYCC6: lambda state: self.check_humba_magic(state, itemName.HUMBACC),
            locationName.JIGGYCC7: lambda state: self.jiggy_cheese(state),
            locationName.JIGGYCC8: lambda state: self.jiggy_trash(state),
            locationName.JIGGYCC9: lambda state: self.jiggy_sstash(state),
            locationName.JIGGYCC10: lambda state: self.check_solo_moves(state, itemName.SHPACK),

            #Jinjo Family Jiggies
            locationName.JIGGYIH1: lambda state: state.has(itemName.WJINJO, self.player, 1),
            locationName.JIGGYIH2: lambda state: state.has(itemName.OJINJO, self.player, 2),
            locationName.JIGGYIH3: lambda state: state.has(itemName.YJINJO, self.player, 3),
            locationName.JIGGYIH4: lambda state: state.has(itemName.BRJINJO, self.player, 4),
            locationName.JIGGYIH5: lambda state: state.has(itemName.GJINJO, self.player, 5),
            locationName.JIGGYIH6: lambda state: state.has(itemName.RJINJO, self.player, 6),
            locationName.JIGGYIH7: lambda state: state.has(itemName.BLJINJO, self.player, 7),
            locationName.JIGGYIH8: lambda state: state.has(itemName.PJINJO, self.player, 8),
            locationName.JIGGYIH9: lambda state: state.has(itemName.BKJINJO, self.player, 9),

        }
        self.cheato_rules = {
            locationName.CHEATOMT1: lambda state: self.cheato_snakehead(state),
            locationName.CHEATOMT2: lambda state: self.cheato_prison(state),
            locationName.CHEATOMT3: lambda state: self.cheato_snakegrove(state),

            locationName.CHEATOGM1: lambda state: self.canary_mary_free(state),
            locationName.CHEATOGM3: lambda state: self.cheato_waterstorage(state),

            locationName.CHEATOWW1: lambda state: self.cheato_hauntedcavern(state),
            locationName.CHEATOWW2: lambda state: self.check_humba_magic(state, itemName.HUMBAWW),
            locationName.CHEATOWW3: lambda state: self.cheato_sauceperil(state),
                                            
            locationName.CHEATOJR1: lambda state: state.has(itemName.DOUBLOON, self.player, 28),
            locationName.CHEATOJR2: lambda state: self.cheato_seemee(state),
            locationName.CHEATOJR3: lambda state: self.cheato_ancientbath(state),

            locationName.CHEATOTL1: lambda state: self.cheato_dippypool(state),
            locationName.CHEATOTL2: lambda state: self.check_humba_magic(state, itemName.HUMBATD),
            locationName.CHEATOTL3: lambda state: self.cheato_tdlboulder(state),

            locationName.CHEATOGI1: lambda state: self.cheato_loggo(state),
            locationName.CHEATOGI3: lambda state: self.can_beat_weldar(state),

            locationName.CHEATOHP1: lambda state: self.cheato_colosseum(state),
            locationName.CHEATOHP2: lambda state: state.has(itemName.CEGGS, self.player) or self.check_solo_moves(state, itemName.SHPACK),
            locationName.CHEATOHP3: lambda state: self.cheato_icypillar(state),

            locationName.CHEATOCC1: lambda state: self.canary_mary_free(state),
            locationName.CHEATOCC2: lambda state: self.cheato_potgold(state),
            locationName.CHEATOCC3: lambda state: self.check_humba_magic(state, itemName.HUMBACC)
        }
        self.honey_rules = {
            locationName.HONEYCMT1: lambda state: self.honeycomb_mt_entrance(state),
            locationName.HONEYCMT2: lambda state: self.honeycomb_bovina(state),
            locationName.HONEYCMT3: lambda state: self.honeycomb_tchamber(state),

            locationName.HONEYCGM1: lambda state: self.GM_boulders(state),
            locationName.HONEYCGM2: lambda state: self.GM_boulders(state),

            locationName.HONEYCWW1: lambda state: self.honeycomb_spacezone(state),
            locationName.HONEYCWW2: lambda state: self.check_humba_magic(state, itemName.HUMBAWW),
            locationName.HONEYCWW3: lambda state: self.honeycomb_crazycastle(state),

            locationName.HONEYCJR1: lambda state: self.honeycomb_seemee(state),
            locationName.HONEYCJR2: lambda state: self.honeycomb_atlantis(state),
            locationName.HONEYCJR3: lambda state: self.honeycomb_jrlpipes(state),
                                                
            locationName.HONEYCTL2: lambda state: self.honeycomb_styracosaurus(state),

            locationName.HONEYCGI1: lambda state: self.honeycomb_floor3(state),
            locationName.HONEYCGI2: lambda state: self.honeycomb_station(state),

            locationName.HONEYCHP1: lambda state: self.honeycomb_volcano(state),
            locationName.HONEYCHP2: lambda state: self.honeycomb_station(state),
            locationName.HONEYCHP3: lambda state: self.honeycomb_lavaside(state),

            locationName.HONEYCCC1: lambda state: state.has(itemName.BDRILL, self.player)

        }
        self.glowbo_rules = {
            locationName.GLOWBOMT2: lambda state: self.check_mumbo_magic(state, itemName.MUMBOMT),
            locationName.GLOWBOWW1: lambda state: self.glowbo_inferno(state),
            locationName.GLOWBOWW2: lambda state: self.glowbo_wigwam(state),

            locationName.GLOWBOJR2: lambda state: self.glowbo_underwigwam(state),

            locationName.GLOWBOCC2: lambda state: self.glowbo_cavern(state),

            locationName.GLOWBOMEG: lambda state: state.has(itemName.GGRAB, self.player) and state.has(itemName.TTORP, self.player)

        }
        self.doubloon_rules = {
            #Alcove
            locationName.JRLDB22:   lambda state: self.doubloon_ledge(state),
            locationName.JRLDB23:   lambda state: self.doubloon_ledge(state),
            locationName.JRLDB24:   lambda state: self.doubloon_ledge(state),
            #Underground
            locationName.JRLDB19:   lambda state: self.doubloon_dirtpatch(state),
            locationName.JRLDB20:   lambda state: self.doubloon_dirtpatch(state),
            locationName.JRLDB21:   lambda state: self.doubloon_dirtpatch(state),
        }
        self.treble_clef_rules = {
            locationName.TREBLEJV:  lambda state: self.treble_jv(state),
            locationName.TREBLEWW:  lambda state: self.treble_ww(state),
            locationName.TREBLEJR:  lambda state: self.treble_jrl(state),
            locationName.TREBLETL:  lambda state: self.treble_tdl(state),
            locationName.TREBLEGI:  lambda state: self.treble_gi(state),
            locationName.TREBLEHP:  lambda state: self.treble_hfp(state),
        }

        self.silo_rules = {
            locationName.EGGAIM: lambda state: self.check_notes(state, 25),
            locationName.BBLASTER: lambda state: self.check_notes(state, 30),
            locationName.GGRAB: lambda state: self.check_mumbo_magic(state, itemName.MUMBOMT) and 
                                              self.check_notes(state, 35),

            locationName.BDRILL: lambda state: self.check_notes(state, 85),
            locationName.BBAYONET: lambda state: self.GM_boulders(state) and self.check_notes(state, 95),

            locationName.AIREAIM: lambda state: self.check_notes(state, 180),
            locationName.SPLITUP: lambda state: self.check_notes(state, 160),
            locationName.PACKWH: lambda state: state.has(itemName.SPLITUP, self.player) and self.check_notes(state, 170),

            locationName.AUQAIM: lambda state: (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player) or state.has(itemName.DOUBLOON, self.player, 28)) and
                                               self.check_notes(state, 275),
            locationName.TTORP: lambda state:  self.can_reach_atlantis(state) and state.has(itemName.GGRAB, self.player) and
                                               self.check_notes(state, 290),
            locationName.WWHACK: lambda state: (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player)) and state.has(itemName.SPLITUP, self.player) and
                                               self.check_notes(state, 265),

            locationName.SPRINGB: lambda state: self.check_notes(state, 390),
            locationName.TAXPACK: lambda state: state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GGRAB, self.player) or
                                                self.check_solo_moves(state, itemName.PACKWH) or self.check_solo_moves(state, itemName.SAPACK))
                                                and self.check_notes(state, 405),
            locationName.HATCH: lambda state:   state.has(itemName.SPLITUP, self.player) and self.check_notes(state, 420),

            locationName.SNPACK: lambda state:  self.silo_snooze(state),
            locationName.LSPRING: lambda state: self.check_notes(state, 545),
            locationName.CLAWBTS: lambda state: self.check_notes(state, 505),

            locationName.SHPACK: lambda state: state.has(itemName.SPLITUP, self.player) and self.check_notes(state, 640),
            locationName.GLIDE: lambda state: state.has(itemName.SPLITUP, self.player) and self.check_notes(state, 660),

            locationName.SAPACK: lambda state: self.check_solo_moves(state, itemName.SHPACK) and self.check_notes(state, 765),

            locationName.FEGGS: lambda state: self.check_notes(state, 45),
            locationName.GEGGS: lambda state: self.check_notes(state, 110),
            locationName.IEGGS: lambda state: self.check_notes(state, 220),
            locationName.CEGGS: lambda state: self.check_notes(state, 315)
        }

        self.jinjo_rules = {
            locationName.JINJOIH5: lambda state: state.has(itemName.TTORP, self.player),
            locationName.JINJOIH4: lambda state: state.has(itemName.BDRILL, self.player),
            locationName.JINJOIH3: lambda state: state.has(itemName.CLAWBTS, self.player),
            locationName.JINJOIH2: lambda state: self.jinjo_wasteland(state),

            locationName.JINJOMT1: lambda state: self.jinjo_jadesnakegrove(state),
            locationName.JINJOMT2: lambda state: self.MT_flight_pad(state),
            locationName.JINJOMT3: lambda state: state.has(itemName.BBLASTER, self.player),

            #TODO Needs to be refined later
            locationName.JINJOGM1: lambda state: self.check_solo_moves(state, itemName.WWHACK) and self.check_solo_moves(state, itemName.LSPRING) and
                                                 self.check_solo_moves(state, itemName.GLIDE) and self.GM_boulders(state),
            locationName.JINJOGM2: lambda state: self.check_humba_magic(state, itemName.HUMBAGM),
            locationName.JINJOGM4: lambda state: self.GM_boulders(state),

            locationName.JINJOWW3: lambda state: self.jinjo_vandoor(state),
            locationName.JINJOWW5: lambda state: self.jinjo_cactus(state),
            locationName.JINJOWW2: lambda state: self.jinjo_caveofhorror(state),

            locationName.JINJOJR1: lambda state: self.jinjo_alcove(state),
            locationName.JINJOJR5: lambda state: self.jinjo_sunkenship(state),
            locationName.JINJOJR4: lambda state: self.jinjo_seaweedsanctum(state),
            locationName.JINJOJR3: lambda state: self.jinjo_bigfish(state),

            locationName.JINJOTL2: lambda state: self.jinjo_tdlentrance(state),
            locationName.JINJOTL1: lambda state: state.has(itemName.TTORP, self.player),
            locationName.JINJOTL3: lambda state: state.has(itemName.CEGGS, self.player),
            locationName.JINJOTL4: lambda state: self.check_mumbo_magic(state, itemName.MUMBOTD) and self.check_humba_magic(state, itemName.HUMBATD),
            locationName.JINJOTL5: lambda state: self.jiggy_stomping_plains(state) and state.has(itemName.SPLITUP, self.player),

            locationName.JINJOGI2: lambda state: state.has(itemName.LSPRING, self.player),
            locationName.JINJOGI3: lambda state: self.jinjo_wasteplant(state),
            locationName.JINJOGI5: lambda state: state.has(itemName.SPLITUP, self.player),

            locationName.JINJOHP2: lambda state: self.check_solo_moves(state, itemName.SHPACK),
            locationName.JINJOHP3: lambda state: self.check_humba_magic(state, itemName.HUMBAHP),
            locationName.JINJOHP4: lambda state: self.jinjo_icegrotto(state),
            locationName.JINJOHP5: lambda state: self.jinjo_mildred(state),
            
            locationName.JINJOCC1: lambda state: self.jinjo_trashcan(state),
            locationName.JINJOCC2: lambda state: self.jinjo_cheese(state),
            locationName.JINJOCC3: lambda state: state.has(itemName.SPLITUP, self.player),
        }

        self.notes_rules = {
            locationName.NOTEIH1:  lambda state: self.notes_plateau(state),
            locationName.NOTEIH2:  lambda state: self.notes_plateau(state),

            locationName.NOTEWW9:   lambda state: self.notes_ww_area51(state),
            locationName.NOTEWW10:  lambda state: self.notes_ww_area51(state),

            locationName.NOTEJRL4:  lambda state: self.notes_jrl_blubs(state),
            locationName.NOTEJRL5:  lambda state: self.notes_jrl_blubs(state),

            locationName.NOTEJRL6:  lambda state: self.notes_jrl_eels(state),
            locationName.NOTEJRL7:  lambda state: self.notes_jrl_eels(state),
            
            locationName.NOTEGI4:  lambda state: self.notes_gi_floor1(state),
            locationName.NOTEGI5:  lambda state: self.notes_gi_floor1(state),

            locationName.NOTEGI11:  lambda state: self.can_use_battery(state),
            locationName.NOTEGI12:  lambda state: self.can_use_battery(state),

            locationName.NOTECCL3: lambda state: self.notes_ccl_silo(state),
            locationName.NOTECCL4: lambda state: self.notes_ccl_silo(state),
        }

    def jiggy_targitzan(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
          logic = state.has(itemName.BBLASTER, self.player)
        elif self.world.options.logic_type == 1: # normal
          logic = state.has(itemName.BBLASTER, self.player)
        elif self.world.options.logic_type == 2: # advanced
          logic = state.has(itemName.BBLASTER, self.player)
        return logic

    def jiggy_sschamber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BBLASTER, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BBLASTER, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.BBLASTER, self.player)
        return logic
    
    def jiggy_mayhem_kickball(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT)
        return logic

    def jiggy_bovina(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
          logic = state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
          logic = state.has(itemName.EGGAIM, self.player) or (self.MT_flight_pad(state) and state.has(itemName.AIREAIM, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = True # N/A
        return logic
    
    def jiggy_treasure_chamber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.EGGAIM,  self.player) and state.has(itemName.GGRAB, self.player) or self.MT_flight_pad(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.EGGAIM,  self.player) and state.has(itemName.GGRAB, self.player) or self.MT_flight_pad(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.EGGAIM,  self.player) and state.has(itemName.GGRAB, self.player) or self.MT_flight_pad(state)
        return logic
    
    def jiggy_golden_goliath(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT)
        return logic
    
    def jiggy_prison_quicksand(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.prison_compound_open(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player) and self.prison_compound_open(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GGRAB, self.player) and self.prison_compound_open(state)
        return logic
    
    def jiggy_pillars(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BDRILL, self.player) and self.prison_compound_open(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BDRILL, self.player) and self.prison_compound_open(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.prison_compound_open(state)
        return logic
    
    def jiggy_ssslumber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT)
        return logic

    def jiggy_generator_cavern(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
          logic = state.has(itemName.FEGGS, self.player) and state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
          logic = True # N/A
        elif self.world.options.logic_type == 2: # advanced
            logic = True # N/A
        return logic
    
    def jiggy_ordnance_storage(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BBLASTER, self.player) and state.has(itemName.BBAYONET, self.player) and \
                    self.GM_boulders(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BBLASTER, self.player) and state.has(itemName.BBAYONET, self.player) and \
                    self.GM_boulders(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.BBLASTER, self.player) and state.has(itemName.BBAYONET, self.player) and \
                    self.GM_boulders(state)
        return logic
    
    def jiggy_crushing_shed(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOGM)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOGM)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOGM)
        return logic
    
    def jiggy_waterfall(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPRINGB, self.player)

        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPRINGB, self.player) or \
                    ((self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)) and \
                     (state.has(itemName.BDRILL, self.player) or self.check_humba_magic(state, itemName.HUMBAGM)))
            
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPRINGB, self.player) or \
                    ((self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)) and \
                     (state.has(itemName.BDRILL, self.player) or self.check_humba_magic(state, itemName.HUMBAGM)))
        return logic
    
    def jiggy_power_hut(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.GM_boulders(state) and (state.has(itemName.SPLITUP, self.player) or self.has_fire(state))

        elif self.world.options.logic_type == 1: # normal
            logic = self.GM_boulders(state)
            
        elif self.world.options.logic_type == 2: # advanced
            logic = self.GM_boulders(state)
        return logic
    
    def jiggy_flooded_caves(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAGM)

        elif self.world.options.logic_type == 1: # normal
            logic = True
            
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def jiggy_hoop_hurry(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player) and state.has(itemName.GEGGS, self.player) 

        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player))
            
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player))
        return logic
    
    def jiggy_dodgem(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAWW) and self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAWW) and self.check_mumbo_magic(state, itemName.MUMBOWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAWW) and self.check_mumbo_magic(state, itemName.MUMBOWW)
        return logic
    
    def jiggy_patches(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.AIREAIM, self.player) and state.has(itemName.EGGAIM, self.player) and \
                    state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.AIREAIM, self.player) and state.has(itemName.EGGAIM, self.player) and \
                    state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.AIREAIM, self.player) and state.has(itemName.EGGAIM, self.player) and \
                    state.has(itemName.GEGGS, self.player)
        return logic

    def jiggy_peril(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAGM) and \
                    self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    self.check_humba_magic(state, itemName.HUMBAWW) and \
                    self.saucer_door_open(state) and state.has(itemName.GGRAB, self.player) and \
                    self.can_access_GM(state) and state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAGM) and \
                    self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    self.check_humba_magic(state, itemName.HUMBAWW) and \
                    self.saucer_door_open(state) and self.can_access_GM(state) and \
                    (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAGM) and \
                    self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    self.check_humba_magic(state, itemName.HUMBAWW) and \
                    self.saucer_door_open(state) and self.can_access_GM(state) and \
                    (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player))
        return logic
    
    def jiggy_balloon_burst(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player) and \
                    state.has(itemName.AIREAIM, self.player) and \
                    state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player) and \
                    state.has(itemName.AIREAIM, self.player) and \
                    (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player) and \
                    state.has(itemName.AIREAIM, self.player) and \
                    (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player))
        return logic
    
    def jiggy_death_dive(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True # N/A
        elif self.world.options.logic_type == 2: # advanced
            logic = True # N/A
        return logic
    
    def jiggy_mrs_boggy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAWW) and \
                self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                self.check_solo_moves(state, itemName.TAXPACK) and \
                state.has(itemName.GEGGS, self.player) and \
                state.has(itemName.GGRAB, self.player)
            
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAWW) and \
                self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                self.check_solo_moves(state, itemName.TAXPACK) and \
                (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player))
            
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAWW) and \
                self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                self.check_solo_moves(state, itemName.TAXPACK) and \
                (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player))
        return logic

    def jiggy_star_spinner(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    self.check_humba_magic(state, itemName.HUMBAWW) and \
                    state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    self.check_humba_magic(state, itemName.HUMBAWW)
        return logic
    
    def jiggy_inferno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAWW) and \
                    state.has(itemName.SPLITUP, self.player) and \
                    state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        return logic
    
    def jiggy_cactus(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BDRILL, self.player) and state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BDRILL, self.player) and state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.BDRILL, self.player) and state.has(itemName.GEGGS, self.player)
        return logic
    
    def jiggy_sub_challenge(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAJR) and self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAJR) and self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAJR)
        return logic
    
    def jiggy_tiptup(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.HATCH) and state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_solo_moves(state, itemName.HATCH) and (state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_solo_moves(state, itemName.HATCH) and (state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player))
        return logic
    
    def jiggy_bacon(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.AUQAIM, self.player) or \
                (self.check_humba_magic(state, itemName.HUMBAJR) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def jiggy_pigpool(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.HFP_hot_water_cooled(state) and \
                    (state.has(itemName.GEGGS, self.player) or state.has(itemName.BDRILL, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player) or \
                    state.has(itemName.BDRILL, self.player)) and \
                    self.HFP_hot_water_cooled(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player) or \
                    state.has(itemName.BDRILL, self.player)) and \
                    self.HFP_hot_water_cooled(state)
        return logic
    
    def jiggy_smuggler(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GEGGS, self.player) and \
                     state.has(itemName.SPLITUP, self.player) and self.check_solo_moves(state, itemName.GLIDE)
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player)) and \
                     state.has(itemName.SPLITUP, self.player) and self.check_solo_moves(state, itemName.GLIDE)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player)) and \
                     state.has(itemName.SPLITUP, self.player) and self.check_solo_moves(state, itemName.GLIDE)
        return logic
    
    def jiggy_merry_maggie(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.AUQAIM, self.player)
        return logic
    
    def jiggy_lord_woo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state) and state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state) and state.has(itemName.GEGGS, self.player) \
                and (self.check_humba_magic(state, itemName.HUMBAJR) or self.check_mumbo_magic(state, itemName.MUMBOJR))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GEGGS, self.player) and state.has(itemName.AUQAIM, self.player) and \
                ((state.has(itemName.TTORP, self.player) and state.has(itemName.BDRILL, self.player)) or \
                     self.check_mumbo_magic(state, itemName.MUMBOJR) or \
                    self.check_humba_magic(state, itemName.HUMBAJR))
        return logic
    
    def jiggy_see_mee(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.TTORP, self.player)
        return logic
    
    def jiggy_ufo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOJR) and state.has(itemName.TTORP, self.player) and \
                    state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.TTORP, self.player) and state.has(itemName.EGGAIM, self.player) and \
                    state.has(itemName.IEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.TTORP, self.player) and state.has(itemName.IEGGS, self.player)
        return logic
    
    def jiggy_terry_nest(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_beat_terry(state) and (state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.BDRILL, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GEGGS, self.player) or state.has(itemName.BDRILL, self.player) or \
                     state.has(itemName.CEGGS, self.player)) and self.can_beat_terry(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GEGGS, self.player) or state.has(itemName.BDRILL, self.player) or \
                     state.has(itemName.CEGGS, self.player)) and self.can_beat_terry(state)
        return logic
    
    def jiggy_dippy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.TTORP, self.player) and self.can_access_ccl(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.TTORP, self.player) and self.can_access_ccl(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.TTORP, self.player) and self.can_access_ccl(state)
        return logic
    
    def jiggy_scrotty(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GEGGS, self.player) and self.WW_train_station(state) and \
                    self.CT_train_station(state) and state.has(itemName.TRAINSWTD, self.player) and \
                    self.check_solo_moves(state, itemName.TAXPACK) and self.check_mumbo_magic(state, itemName.MUMBOIH) and \
                    state.has(itemName.BDRILL, self.player) and self.check_mumbo_magic(state, itemName.MUMBOTD) and \
                    state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GEGGS, self.player) and self.WW_train_station(state) and \
                    self.CT_train_station(state) and state.has(itemName.TRAINSWTD, self.player) and \
                    self.check_solo_moves(state, itemName.TAXPACK) and self.check_mumbo_magic(state, itemName.MUMBOIH) and \
                    state.has(itemName.BDRILL, self.player) and self.check_mumbo_magic(state, itemName.MUMBOTD)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GEGGS, self.player) and self.WW_train_station(state) and \
                    self.CT_train_station(state) and state.has(itemName.TRAINSWTD, self.player) and \
                    self.check_solo_moves(state, itemName.TAXPACK) and self.check_mumbo_magic(state, itemName.MUMBOIH) and \
                    state.has(itemName.BDRILL, self.player) and self.check_mumbo_magic(state, itemName.MUMBOTD)
        return logic
    
    def jiggy_oogle_boogle(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.oogle_boogles_open(state) and state.has(itemName.FEGGS, self.player) and \
                    self.smuggle_food(state) and state.has(itemName.GGRAB, self.player) and \
                    state.has(itemName.BDRILL, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.oogle_boogles_open(state) and self.has_fire(state) and \
                    self.smuggle_food(state) and state.has(itemName.GGRAB, self.player) and \
                    state.has(itemName.BDRILL, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.oogle_boogles_open(state) and self.has_fire(state) and \
                    state.has(itemName.GGRAB, self.player) and state.has(itemName.BDRILL, self.player)
        return logic

    def jiggy_terry_kids(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_beat_terry(state) and self.check_solo_moves(state, itemName.HATCH) and \
                    self.check_solo_moves(state, itemName.TAXPACK) and self.oogle_boogles_open(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_beat_terry(state) and self.check_solo_moves(state, itemName.HATCH) and \
                    self.check_solo_moves(state, itemName.TAXPACK) and self.oogle_boogles_open(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_beat_terry(state) and self.check_solo_moves(state, itemName.HATCH) and \
                    self.check_solo_moves(state, itemName.TAXPACK) and self.oogle_boogles_open(state)
        return logic
    
    def jiggy_stomping_plains(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.IEGGS, self.player) and state.has(itemName.SPRINGB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPRINGB, self.player) and \
            (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE) or \
            state.has(itemName.IEGGS, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPRINGB, self.player)
        return logic
    
    def jiggy_rocknuts(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.CEGGS, self.player)
        return logic
    
    def jiggy_skivvy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAGI) and state.has(itemName.BDRILL, self.player) and \
                    state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAGI) and state.has(itemName.BDRILL, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAGI) and state.has(itemName.BDRILL, self.player)
        return logic

    def jiggy_qa(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOGI) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.EGGAIM, self.player) and \
                    self.can_use_battery(state) and self.check_humba_magic(state, itemName.HUMBAGI)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOGI) and state.has(itemName.GEGGS, self.player) and \
                    ((state.has(itemName.EGGAIM, self.player) and (self.check_humba_magic(state, itemName.HUMBAGI)) or \
                    self.check_solo_moves(state, itemName.LSPRING))) and self.can_use_battery(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOGI) and state.has(itemName.GEGGS, self.player) and \
                    self.can_use_battery(state)
        return logic
    
    def jiggy_compactor(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.SNPACK)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_solo_moves(state, itemName.SNPACK) or self.check_solo_moves(state, itemName.PACKWH)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_solo_moves(state, itemName.SNPACK) or self.check_solo_moves(state, itemName.PACKWH)
        return logic
    
    def jiggy_twinkly(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_use_battery(state) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_use_battery(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_use_battery(state)
        return logic
    
    def jiggy_plantbox(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_use_battery(state) and self.check_solo_moves(state, itemName.SAPACK) and \
                    state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_use_battery(state) 
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_use_battery(state)
        return logic

    def jiggy_dragons_bros(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.FEGGS, self.player) and state.has(itemName.IEGGS, self.player) and \
                    state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.FEGGS, self.player) and state.has(itemName.IEGGS, self.player) and \
                    state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.FEGGS, self.player) and state.has(itemName.IEGGS, self.player) and \
                (self.check_solo_moves(state, itemName.PACKWH) or state.has(itemName.CLAWBTS, self.player))
        return logic
    
    def jiggy_sabreman(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOHP) and state.has(itemName.FEGGS, self.player) and \
                    self.check_solo_moves(state, itemName.TAXPACK)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOHP) and self.has_fire(state) and \
                    self.check_solo_moves(state, itemName.TAXPACK)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOHP) and self.has_fire(state) and \
                    self.check_solo_moves(state, itemName.TAXPACK)
        return logic
    
    def jiggy_ice_station(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_beat_king_coal(state) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    state.has(itemName.EGGAIM, self.player) and ((state.has(itemName.FEGGS, self.player) \
                    and self.ww_jiggy(state)) or state.has(itemName.TRAINSWWW, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_beat_king_coal(state) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    ((state.has(itemName.FEGGS, self.player) \
                    and self.ww_jiggy(state)) or state.has(itemName.TRAINSWWW, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_beat_king_coal(state) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    ((state.has(itemName.FEGGS, self.player) \
                    and self.ww_jiggy(state)) or state.has(itemName.TRAINSWWW, self.player))
        return logic

    def jiggy_oil_drill(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAHP) and \
                    self.check_solo_moves(state, itemName.SHPACK) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAHP) and self.check_solo_moves(state, itemName.SHPACK) and \
                    (self.check_solo_moves(state, itemName.PACKWH) or state.has(itemName.GGRAB, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAHP) and self.check_solo_moves(state, itemName.SHPACK) and \
                    (self.check_solo_moves(state, itemName.PACKWH) or state.has(itemName.GGRAB, self.player))
        return logic
    
    def jiggy_hfp_stomping(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.SNPACK) and state.has(itemName.IEGGS, self.player) and \
                    state.has(itemName.SPRINGB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPRINGB, self.player) and \
                    (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE) or \
                     state.has(itemName.IEGGS, self.player)) and \
                    self.check_solo_moves(state, itemName.SNPACK)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPRINGB, self.player) and state.has(itemName.SPLITUP, self.player)
        return logic
    
    def jiggy_hfp_kickball(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT) and \
                    state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT) and \
                    (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT) and \
                    (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP))
        return logic
    
    def jiggy_aliens(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.jiggy_ufo(state) and state.has(itemName.BDRILL, self.player) and \
                    self.check_solo_moves(state, itemName.HATCH) and self.check_solo_moves(state, itemName.GLIDE) and \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)
        elif self.world.options.logic_type == 1: # normal
            logic = self.jiggy_ufo(state) and self.check_mumbo_magic(state, itemName.MUMBOHP) and \
                    state.has(itemName.BDRILL, self.player) and self.check_solo_moves(state, itemName.HATCH) and \
                    (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.jiggy_ufo(state) and self.check_mumbo_magic(state, itemName.MUMBOHP) and \
                    state.has(itemName.BDRILL, self.player) and self.check_solo_moves(state, itemName.HATCH)
        return logic

    def jiggy_colosseum_split(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GGRAB, self.player) or \
                    self.check_solo_moves(state, itemName.PACKWH))
        return logic
    
    def jiggy_mr_fit(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPRINGB, self.player) and self.check_solo_moves(state, itemName.SAPACK) and \
                    self.grow_beanstalk(state) and self.can_use_floatus(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPRINGB, self.player) and self.check_solo_moves(state, itemName.SAPACK) and \
                    self.grow_beanstalk(state) and self.can_use_floatus(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPRINGB, self.player) and self.check_solo_moves(state, itemName.SAPACK) and \
                    self.grow_beanstalk(state) and \
                    (self.can_use_floatus(state) or self.check_solo_moves(state, itemName.PACKWH))
        return logic
    
    def jiggy_gold_pot(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.FEGGS, self.player) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.IEGGS, self.player) and self.check_mumbo_magic(state, itemName.MUMBOCC)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.FEGGS, self.player) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.IEGGS, self.player) and self.check_mumbo_magic(state, itemName.MUMBOCC)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.FEGGS, self.player) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.IEGGS, self.player) and\
                    (self.check_mumbo_magic(state, itemName.MUMBOCC) or state.has(itemName.SPLITUP, self.player))
        return logic
    
    def jiggy_cheese(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.SAPACK) and self.grow_beanstalk(state) and \
                    self.can_use_floatus(state) and self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_solo_moves(state, itemName.SAPACK) and self.grow_beanstalk(state) and \
                    self.can_use_floatus(state) and self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_solo_moves(state, itemName.SAPACK) and self.grow_beanstalk(state) and \
                    self.can_use_floatus(state) and self.check_solo_moves(state, itemName.SHPACK)
        return logic
    
    def jiggy_trash(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.WWHACK)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player)
        return logic
    
    def jiggy_sstash(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.CEGGS, self.player) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.CEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.CEGGS, self.player)
        return logic


    def honeycomb_mt_entrance(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 1: # normal
            logic = (self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT)) or \
                    state.has(itemName.CEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = (self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT)) or \
                    state.has(itemName.CEGGS, self.player)
        return logic
    
    def honeycomb_bovina(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True # N/A
        elif self.world.options.logic_type == 2: # advanced
            logic = True # N/A
        return logic
    
    def honeycomb_tchamber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.MT_flight_pad(state) or state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.MT_flight_pad(state) or state.has(itemName.EGGAIM, self.player)
        return logic
    
    def honeycomb_spacezone(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def honeycomb_crazycastle(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player)
        return logic
    
    def honeycomb_seemee(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.TTORP, self.player)
        return logic
    
    def honeycomb_atlantis(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state) 
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic

    def honeycomb_jrlpipes(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (state.has(itemName.GEGGS, self.player) or  state.has(itemName.BDRILL, self.player)) and \
                    state.has(itemName.GGRAB, self.player) 
        elif self.world.options.logic_type == 1: # normal
            logic = ((state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player) or state.has(itemName.BDRILL, self.player))\
                    and state.has(itemName.GGRAB, self.player))\
                    or ((state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player))\
                    and (self.check_solo_moves(state, itemName.LSPRING) and (self.check_solo_moves(state, itemName.GLIDE) or \
                    self.check_solo_moves(state, itemName.WWHACK))))
        elif self.world.options.logic_type == 2: # advanced
            logic = ((state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player) or state.has(itemName.BDRILL, self.player))\
                    and state.has(itemName.GGRAB, self.player))\
                    or ((state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player))\
                    and (self.check_solo_moves(state, itemName.LSPRING) and (self.check_solo_moves(state, itemName.GLIDE) or \
                    self.check_solo_moves(state, itemName.WWHACK))))
        return logic
    
    def honeycomb_styracosaurus(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BDRILL, self.player) and state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BDRILL, self.player) and state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.BDRILL, self.player) and state.has(itemName.SPLITUP, self.player)) or \
                    (self.check_solo_moves(state, itemName.LSPRING) and self.check_solo_moves(state, itemName.WWHACK) and self.check_solo_moves(state, itemName.GLIDE))
        return logic
    
    def honeycomb_floor3(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic =  (state.has(itemName.GGRAB, self.player) or state.has(itemName.SPLITUP, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def honeycomb_station(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic

    def honeycomb_volcano(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or \
                    state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or \
                    state.has(itemName.SPLITUP, self.player)
        return logic
    
    def honeycomb_station(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.LSPRING) or \
                    self.check_solo_moves(state, itemName.GLIDE)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.LSPRING) or \
                    self.check_solo_moves(state, itemName.GLIDE) or (state.has(itemName.SPLITUP, self.player) and \
                     state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player))
        return logic
    
    def honeycomb_lavaside(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic


    def cheato_snakehead(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (state.has(itemName.EGGAIM, self.player) and state.has(itemName.GGRAB, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = self.MT_flight_pad(state) or (state.has(itemName.EGGAIM, self.player) and state.has(itemName.GGRAB, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.MT_flight_pad(state) or (state.has(itemName.EGGAIM, self.player) and state.has(itemName.GGRAB, self.player))
        return logic
    
    def cheato_prison(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.prison_compound_open(state) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.prison_compound_open(state) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.prison_compound_open(state) and state.has(itemName.GGRAB, self.player)
        return logic
    
    def cheato_snakegrove(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT) and state.has(itemName.GGRAB, self.player)
        return logic
    
    def cheato_waterstorage(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def cheato_hauntedcavern(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player) or (self.check_solo_moves(state, itemName.LSPRING) and \
                    (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GGRAB, self.player) or (self.check_solo_moves(state, itemName.LSPRING) and \
                    (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)))
        return logic
    
    def cheato_sauceperil(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.jiggy_peril(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.jiggy_peril(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.jiggy_peril(state)
        return logic
    
    def cheato_seemee(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.jiggy_see_mee(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.jiggy_see_mee(state)
        return logic
    
    def cheato_ancientbath(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player) and \
                    self.check_solo_moves(state, itemName.GLIDE)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player) and \
                    (self.check_solo_moves(state, itemName.GLIDE) or self.check_solo_moves(state, itemName.LSPRING) or
                    (self.check_solo_moves(state, itemName.PACKWH) and state.has(itemName.GGRAB, self.player)))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.TTORP, self.player) and (self.check_solo_moves(state, itemName.GLIDE) or self.check_solo_moves(state, itemName.LSPRING) or
                    self.check_solo_moves(state, itemName.WWHACK) or
                    (self.check_solo_moves(state, itemName.PACKWH) and state.has(itemName.GGRAB, self.player)))
        return logic
    
    #handle CCL access
    def cheato_dippypool(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.ccl_jiggy(state) and state.has(itemName.SPRINGB, self.player) and \
                                                  state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.ccl_jiggy(state) and state.has(itemName.SPRINGB, self.player) and \
                                                  state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.ccl_jiggy(state) and state.has(itemName.SPRINGB, self.player) and \
                                                  state.has(itemName.TTORP, self.player)
        return logic
    
    def cheato_tdlboulder(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BDRILL, self.player) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BDRILL, self.player) and (state.has(itemName.GGRAB, self.player) or self.can_beat_terry(state))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.BDRILL, self.player) and (state.has(itemName.GGRAB, self.player) or self.can_beat_terry(state))
        return logic
    
    def cheato_loggo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GEGGS, self.player) or (state.has(itemName.CEGGS, self.player) and \
                     state.has(itemName.BDRILL, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GEGGS, self.player) or (state.has(itemName.CEGGS, self.player) and \
                     state.has(itemName.BDRILL, self.player))
        return logic
    
    def cheato_colosseum(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.CLAWBTS, self.player) and state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.CLAWBTS, self.player) and \
                    (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player) or
                    self.check_mumbo_magic(state, itemName.MUMBOHP))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.CLAWBTS, self.player) and \
                    (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player) or
                    self.check_mumbo_magic(state, itemName.MUMBOHP))
        return logic
    
    def cheato_icypillar(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player)
        return logic
    
    def cheato_potgold(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.jiggy_gold_pot(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.jiggy_gold_pot(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.jiggy_gold_pot(state)
        return logic


    def glowbo_inferno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        return logic
    
    def glowbo_wigwam(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def glowbo_underwigwam(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic

    def glowbo_cavern(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    

    def jinjo_wasteland(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def jinjo_jadesnakegrove(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.check_mumbo_magic(state,itemName.MUMBOMT)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state,itemName.MUMBOMT)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state,itemName.MUMBOMT)
        return logic
    
    def jinjo_caveofhorror(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GEGGS, self.player)
        return logic
    
    def jinjo_cactus(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def jinjo_vandoor(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GEGGS, self.player) and \
                    self.check_humba_magic(state, itemName.HUMBAWW) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player)) and \
                    self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player)) and \
                    self.check_humba_magic(state, itemName.HUMBAWW)
        return logic
    
    def jinjo_alcove(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.DOUBLOON, self.player, 28)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.DOUBLOON, self.player, 28) or ((state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player)) and (self.check_solo_moves(state, itemName.PACKWH) or \
                    self.check_solo_moves(state, itemName.SAPACK) or (self.check_solo_moves(state, itemName.LSPRING) and \
                    self.check_solo_moves(state, itemName.GLIDE))))
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def jinjo_bigfish(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.jiggy_merry_maggie(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.jiggy_merry_maggie(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.jiggy_merry_maggie(state)
        return logic
    
    def jinjo_seaweedsanctum(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def jinjo_sunkenship(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAJR) or state.has(itemName.AUQAIM, self.player) or \
                    state.has(itemName.TTORP, self.player)
        return logic
    
    def jinjo_tdlentrance(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_beat_terry(state) and state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GEGGS, self.player)
        return logic

    def jinjo_wasteplant(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.IEGGS, self.player) and state.has(itemName.AUQAIM, self.player) and \
                    state.has(itemName.TTORP, self.player)
        return logic

    def jinjo_icegrotto(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.GLIDE) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_solo_moves(state, itemName.GLIDE) or (self.check_solo_moves(state, itemName.LSPRING) and 
                    self.check_solo_moves(state, itemName.WWHACK))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_solo_moves(state, itemName.GLIDE) or (self.check_solo_moves(state, itemName.LSPRING) and 
                    self.check_solo_moves(state, itemName.WWHACK))
        return logic
    
    def jinjo_mildred(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.FEGGS, self.player) or state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.BDRILL, self.player) 
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.FEGGS, self.player) or state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player) or state.has(itemName.BDRILL, self.player) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.FEGGS, self.player) or state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player) or state.has(itemName.BDRILL, self.player) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)
        return logic
    
    def jinjo_trashcan(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic =  self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 1: # normal
            logic =  self.check_solo_moves(state, itemName.SHPACK) or self.check_solo_moves(state, itemName.LSPRING)
        elif self.world.options.logic_type == 2: # advanced
            logic =  self.check_solo_moves(state, itemName.SHPACK) or self.check_solo_moves(state, itemName.LSPRING)
        return logic

    def jinjo_cheese(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (self.check_solo_moves(state, itemName.SAPACK) and self.grow_beanstalk(state) and \
                     self.can_use_floatus(state))
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic


    def treble_jv(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def treble_ww(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        return logic
    
    def treble_jrl(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.AUQAIM, self.player) or state.has(itemName.TTORP, self.player) or self.check_humba_magic(state, itemName.HUMBAJR)
        return logic
    
    def treble_tdl(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BDRILL, self.player) and (self.can_beat_terry(state) or state.has(itemName.GGRAB, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BDRILL, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.BDRILL, self.player)
        return logic
    
    def treble_gi(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic

    def treble_hfp(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or state.has(itemName.SPLITUP, self.player)
        return logic
    

    def silo_snooze(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.can_use_battery(state) and \
                    self.check_notes(state, 525)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_use_battery(state) and self.check_notes(state, 525)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_use_battery(state) and self.check_notes(state, 525)
        return logic
    
    def tswitch_ww(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.LSPRING)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.LSPRING)
        return logic
    
    def tswitch_lavaside(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def doubloon_ledge(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player) and state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player))
        return logic
    
    def doubloon_dirtpatch(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BDRILL, self.player) or state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BDRILL, self.player) or state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.BDRILL, self.player) or state.has(itemName.GEGGS, self.player) or \
                    state.has(itemName.CEGGS, self.player)
        return logic

    def notes_plateau(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def notes_ww_area51(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player) or \
                    state.has(itemName.SPLITUP, self.player)
        return logic
    
    def notes_jrl_blubs(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOJR) and (state.has(itemName.AUQAIM, self.player) or 
                    state.has(itemName.TTORP, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.AUQAIM, self.player) or state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.AUQAIM, self.player) or state.has(itemName.TTORP, self.player)
        return logic
    
    def notes_jrl_eels(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def notes_gi_floor1(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_access_gi_fl1_2fl2(state) or state.has(itemName.GGRAB, self.player) or \
                    self.check_solo_moves(state, itemName.PACKWH) or self.check_solo_moves(state, itemName.LSPRING)
        return logic
    
    def notes_ccl_silo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_solo_moves(state, itemName.SHPACK) or state.has(itemName.CEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_solo_moves(state, itemName.SHPACK) or state.has(itemName.CEGGS, self.player)
        return logic


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
            
    def check_notes(self, state:CollectionState, amount:int) -> bool:
        count:int = 0
        count = state.count(itemName.TREBLE, self.player) * 20
        count += state.count(itemName.NOTE, self.player) * 5
        if count >= amount:
            return True
        else:
            return False

    def has_enough_notes(self, state: CollectionState, Amount) -> bool:
        count:int = 0
        if self.can_access_mt(state): # MT Access
            count += 80
        if state.has(itemName.GGRAB, self.player): # JV Treble + Plateau Sign
            count += 10
        if state.has(itemName.GGRAB, self.player) or self.dilberta_free(state): # Honey B.
            count += 10
            if self.gm_jiggy(state) or self.dilberta_free(state): # GGM Access
                count += 80
            if state.has(itemName.FEGGS, self.player): # Pine Grove Access
                count += 20
                if self.ww_jiggy(state): # WW Access
                    count += 70
                    if state.has(itemName.GEGGS, self.player) or state.has(itemName.GEGGS, self.player) or \
                        self.check_solo_moves(state, itemName.GLIDE) or self.check_solo_moves(state, itemName.LSPRING): # Area 51 Fence
                            count += 10
                if state.has(itemName.TTORP, self.player): # Wasteland Access
                    count += 20
                    if state.has(itemName.JIGGY, self.player, 20): # TDL Access
                        count += 80
                    if self.ccl_jiggy(state): # CCL Access
                        count += 70
                        if state.has(itemName.CEGGS, self.player) or state.has(itemName.SHPACK, self.player): # Sack Pack Notes
                            count += 10
                    if state.has(itemName.SPRINGB, self.player) and self.gi_jiggy(state) and self.enter_GI(state): # GI 1F
                        count += 25
                        if self.can_use_battery(state):  # Waste Disposal
                            count += 10
                        if self.can_reach_GI_2F(state) or self.check_solo_moves(state, itemName.PACKWH) or \
                                self.check_solo_moves(state, itemName.LSPRING) or state.has(
                            itemName.GGRAB, self.player):  # 1F Window Notes
                            count += 10
                        if self.can_reach_GI_2F(state):  # Rest of GI
                            count += 35
            if state.has(itemName.SPLITUP, self.player) or (self.world.options.randomize_stations == 1 and
                self.can_beat_king_coal(state) and state.has(itemName.TRAINSWHP1, self.player)): # Cliff Top
                    count += 20
            if state.has(itemName.SPLITUP, self.player):
                if self.jrl_jiggy(state): # JRL Town Center
                    count += 60
                    if state.has(itemName.AUQAIM, self.player) or state.has(itemName.TTORP, self.player): # Squid Notes
                        count += 10
                    if self.can_reach_atlantis(state): # Deep JRL
                        count += 10
                if state.has(itemName.JIGGY, self.player, 36): # HFP Access
                    count += 80
        count += state.count(itemName.TREBLE, self.player) * 20
        return count >= Amount

    def has_fire(self, state: CollectionState) -> bool:
        return state.has(itemName.FEGGS, self.player) or (self.check_humba_magic(state, itemName.HUMBAIH) and \
                self.can_access_pinegrove(state, False))

    def long_swim(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return self.check_mumbo_magic(state, itemName.MUMBOJR)
        elif self.world.options.logic_type == 1: # normal
            return state.has(itemName.BDRILL, self.player) or self.check_mumbo_magic(state, itemName.MUMBOJR)
        elif self.world.options.logic_type == 2: # advanced
            return state.has(itemName.BDRILL, self.player) or self.check_mumbo_magic(state, itemName.MUMBOJR)

    def can_reach_atlantis(self, state: CollectionState) -> bool:
        return state.has(itemName.IEGGS, self.player) and self.long_swim(state) and state.has(itemName.AUQAIM, self.player)

    def MT_flight_pad(self, state: CollectionState) -> bool:
        return state.has(itemName.BDRILL, self.player) or self.check_mumbo_magic(state, itemName.MUMBOMT)

    def prison_compound_open(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return self.can_access_mt(state) and \
                (state.has(itemName.GEGGS, self.player) or self.check_mumbo_magic(state, itemName.MUMBOMT))
        
        elif self.world.options.logic_type == 1: # normal
            return self.can_access_mt(state) and \
                (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player) or \
                 self.check_mumbo_magic(state, itemName.MUMBOMT))
        
        elif self.world.options.logic_type == 2: # advanced
            return self.can_access_mt(state) and \
                (state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player) or \
                 self.check_mumbo_magic(state, itemName.MUMBOMT))
        
    def dilberta_free(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return self.prison_compound_open(state) and state.has(itemName.BDRILL, self.player) and \
                    self.check_humba_magic(state, itemName.HUMBAMT)
        
        elif self.world.options.logic_type == 1: # normal
            return self.prison_compound_open(state) and state.has(itemName.BDRILL, self.player)
        
        elif self.world.options.logic_type == 2: # advanced
            return self.prison_compound_open(state) and state.has(itemName.BDRILL, self.player)

    def GM_boulders(self, state: CollectionState) -> bool:
        return state.has(itemName.BDRILL, self.player) or self.check_humba_magic(state, itemName.HUMBAGM)

    def canary_mary_free(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return self.check_humba_magic(state, itemName.HUMBAGM)
 
        elif self.world.options.logic_type == 1: # normal
            return self.check_humba_magic(state, itemName.HUMBAGM) or state.has(itemName.CEGGS, self.player)
        
        elif self.world.options.logic_type == 2: # advanced
            return self.check_humba_magic(state, itemName.HUMBAGM) or state.has(itemName.CEGGS, self.player)

    def can_beat_king_coal(self, state) -> bool:
        if self.world.options.randomize_chuffy == False:
            return self.check_mumbo_magic(state, itemName.MUMBOGM)
        else:
            return state.has(itemName.CHUFFY, self.player)


    #deprecated but might be useful for ticket randomization
    def can_kill_fruity(self, state: CollectionState) -> bool:
        return state.has(itemName.GEGGS, self.player) or \
               state.has(itemName.CEGGS, self.player) or \
               self.check_humba_magic(state, itemName.HUMBAWW)

    def saucer_door_open(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return state.has(itemName.GGRAB, self.player) and state.has(itemName.GEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            return state.has(itemName.GGRAB, self.player) or (state.has(itemName.EGGAIM, self.player) and \
                   state.has(itemName.GEGGS, self.player)) or \
            ((state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player)) and \
             (self.check_solo_moves(state, itemName.LSPRING) and self.check_solo_moves(state, itemName.GLIDE)))
        elif self.world.options.logic_type == 2: # advanced
            return state.has(itemName.GGRAB, self.player) or (state.has(itemName.EGGAIM, self.player) and \
                   (state.has(itemName.GEGGS, self.player) or state.has(itemName.GEGGS, self.player))) or \
            ((state.has(itemName.GEGGS, self.player) or state.has(itemName.CEGGS, self.player)) and \
             (self.check_solo_moves(state, itemName.LSPRING) and self.check_solo_moves(state, itemName.GLIDE)))

    def can_beat_terry(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return state.has(itemName.EGGAIM, self.player) and state.has(itemName.SPRINGB, self.player)
        elif self.world.options.logic_type == 1: # normal
            return state.has(itemName.EGGAIM, self.player) and state.has(itemName.SPRINGB, self.player)
        elif self.world.options.logic_type == 2: # advanced
            return state.has(itemName.SPRINGB, self.player)
        
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
        return self.can_use_battery(state) and self.check_mumbo_magic(state, itemName.MUMBOGI) and \
               self.check_humba_magic(state, itemName.HUMBAGI) and state.has(itemName.GEGGS, self.player) and \
               state.has(itemName.BDRILL, self.player)

    def can_use_battery(self, state: CollectionState) -> bool:
        return self.check_solo_moves(state, itemName.PACKWH) and self.check_solo_moves(state, itemName.TAXPACK)

    def can_access_mt(self, state: CollectionState) -> bool: #1
        if self.world.worlds_randomized == True:
            return state.has(itemName.MTA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.MT]
            logic = True
            if self.world.options.logic_type == 0: # beginner
                logic = state.has(itemName.JIGGY, self.player, amt)
            elif self.world.options.logic_type == 1: # normal
                logic = state.has(itemName.JIGGY, self.player, amt)
            elif self.world.options.logic_type == 2: # advanced
                logic = state.has(itemName.JIGGY, self.player, amt)
            return logic

    def can_access_plateau(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) or self.dilberta_free(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player) or self.dilberta_free(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        return logic
    
    def can_access_GM(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (state.has(itemName.GGRAB, self.player) and self.gm_jiggy(state)) or \
                    self.dilberta_free(state)
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GGRAB, self.player) and self.gm_jiggy(state)) or \
                    self.dilberta_free(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.gm_jiggy(state)
        return logic
    
    def gm_jiggy(self, state: CollectionState) -> bool: #4
        if self.world.worlds_randomized == True:
            return state.has(itemName.GGA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.GM]
            return state.has(itemName.JIGGY, self.player, amt)
    
    def can_access_pinegrove(self, state: CollectionState, fromTrain: bool) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.FEGGS, self.player) and self.can_access_plateau(state) and \
                    state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1 : # normal
            if fromTrain:
                logic = (state.has(itemName.FEGGS, self.player) and self.can_access_plateau(state))
            else:
                logic = (state.has(itemName.FEGGS, self.player) and self.can_access_plateau(state)) or \
                        ((self.has_train_access(state, "WW") and self.ww_jiggy(state)) or \
                        (self.has_train_access(state, "TDL") and state.has(itemName.TTORP, self.player)))
        elif self.world.options.logic_type == 2: # advanced
            if fromTrain:
                logic = (state.has(itemName.FEGGS, self.player) and self.can_access_plateau(state))
            else:
                logic = (state.has(itemName.FEGGS, self.player) and self.can_access_plateau(state)) or \
                        ((self.has_train_access(state, "WW") and self.ww_jiggy(state)) or \
                        (self.has_train_access(state, "TDL") and state.has(itemName.TTORP, self.player)))
        return logic
    
    def can_access_witchyworld(self, state: CollectionState, fromTrain: bool) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (self.ww_jiggy(state) and self.can_access_pinegrove(state, False))
        elif self.world.options.logic_type == 1: # normal
            if fromTrain:
                logic = self.ww_jiggy(state) and self.can_access_pinegrove(state, fromTrain)
            else:
                logic = self.ww_jiggy(state) and self.can_access_pinegrove(state, fromTrain) or \
                        self.has_train_access(state, "WW")
        elif self.world.options.logic_type == 2: # advanced
            if fromTrain:
                logic = self.ww_jiggy(state) and self.can_access_pinegrove(state, fromTrain)
            else:
                logic = self.ww_jiggy(state) and self.can_access_pinegrove(state, fromTrain) or \
                        self.has_train_access(state, "WW")
        return logic
    
    def ww_jiggy(self, state: CollectionState) -> bool: #8
        if self.world.worlds_randomized == True:
            return state.has(itemName.WWA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.WW]
            return state.has(itemName.JIGGY, self.player, amt)
    
    def can_access_clifftop(self, state: CollectionState, fromTrain: bool) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player) and self.can_access_plateau(state)
        elif self.world.options.logic_type == 1: # normal
            if fromTrain:
                logic = (state.has(itemName.SPLITUP, self.player) and self.can_access_plateau(state))
            else: 
                logic = (state.has(itemName.SPLITUP, self.player) and self.can_access_plateau(state)) or \
                    self.has_train_access(state, "CT")
        elif self.world.options.logic_type == 2: # advanced
            if fromTrain:
                logic = (state.has(itemName.SPLITUP, self.player) and self.can_access_plateau(state))
            else: 
                logic = (state.has(itemName.SPLITUP, self.player) and self.can_access_plateau(state)) or \
                    self.has_train_access(state, "CT")
        return logic
    
    def can_access_jrl(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_access_clifftop(state, False) and self.jrl_jiggy(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_access_clifftop(state, False) and self.jrl_jiggy(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_access_clifftop(state, False) and self.jrl_jiggy(state)
        return logic
    
    def jrl_jiggy(self, state: CollectionState) -> bool: #14
        if self.world.worlds_randomized == True:
            return state.has(itemName.JRA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.JR]
            return state.has(itemName.JIGGY, self.player, amt)
    
    def can_access_wasteland(self, state: CollectionState, fromTrain: bool) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_access_pinegrove(state, False) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 1: # normal
            if fromTrain:
                logic = self.can_access_pinegrove(state, fromTrain) and state.has(itemName.TTORP, self.player)
            else:
                logic = (self.can_access_pinegrove(state, fromTrain) and state.has(itemName.TTORP, self.player)) or \
                        self.has_train_access(state, "TDL") or (self.can_leave_GI_from_inside(state) and \
                        self.gi_jiggy(state))
        elif self.world.options.logic_type == 2: # advanced
            if fromTrain:
                logic = self.can_access_pinegrove(state, fromTrain) and state.has(itemName.TTORP, self.player)
            else:
                logic = (self.can_access_pinegrove(state, fromTrain) and state.has(itemName.TTORP, self.player)) or \
                        self.has_train_access(state, "TDL") or (self.can_leave_GI_from_inside(state) and \
                        self.gi_jiggy(state))
        return logic
    
    def can_access_tdl(self, state: CollectionState, fromTrain: bool) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_access_wasteland(state, False) and self.tdl_jiggy(state)
        elif self.world.options.logic_type == 1: # normal
            if fromTrain:  
                logic = (self.can_access_wasteland(state, fromTrain) and self.tdl_jiggy(state))
            else:
                logic = (self.can_access_wasteland(state, fromTrain) and self.tdl_jiggy(state)) or \
                        self.has_train_access(state, "TDL")
        elif self.world.options.logic_type == 2: # advanced
            if fromTrain:  
                    logic = (self.can_access_wasteland(state, fromTrain) and self.tdl_jiggy(state))
            else:
                    logic = (self.can_access_wasteland(state, fromTrain) and self.tdl_jiggy(state)) or \
                            self.has_train_access(state, "TDL")
        return logic
    
    def tdl_jiggy(self, state: CollectionState) -> bool: #20
        if self.world.worlds_randomized == True:
            return state.has(itemName.TDA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.TL]
            return state.has(itemName.JIGGY, self.player, amt)
    
    def can_access_quagmire(self, state: CollectionState, fromTrain: bool) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPRINGB, self.player) and self.can_access_wasteland(state, False)
        elif self.world.options.logic_type == 1: # normal
            if fromTrain:
                logic = state.has(itemName.SPRINGB, self.player) and self.can_access_wasteland(state, fromTrain)
            else:
                logic = (state.has(itemName.SPRINGB, self.player) and self.can_access_wasteland(state, fromTrain)) or \
                        (self.can_leave_GI_from_inside(state) and self.gi_jiggy(state))
        elif self.world.options.logic_type == 2: # advanced
            if fromTrain:
                logic = state.has(itemName.SPRINGB, self.player) and self.can_access_wasteland(state, fromTrain)
            else:
                logic = (state.has(itemName.SPRINGB, self.player) and self.can_access_wasteland(state, fromTrain)) or \
                        (self.can_leave_GI_from_inside(state) and state.has(itemName.JIGGY, self.player, 28))
        return logic
    
    def can_access_gruntyindustries_outside(self, state: CollectionState, fromTrain: bool) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.gi_jiggy(state) and self.can_access_quagmire(state, False)
        elif self.world.options.logic_type == 1: # normal
            logic = self.gi_jiggy(state) and self.can_access_quagmire(state, fromTrain)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.gi_jiggy(state) and self.can_access_quagmire(state, fromTrain)
        return logic
    
    def gi_jiggy(self, state: CollectionState) -> bool: #28
        if self.world.worlds_randomized == True:
            return state.has(itemName.GIA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.GIO]
            return state.has(itemName.JIGGY, self.player, amt)

    def can_access_gi_outside_from_inside(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.has_train_access(state, "GI") and state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_leave_GI_from_inside(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_leave_GI_from_inside(state)
        return logic
    
    def can_access_gi_fl1_2fl2(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.CLAWBTS, self.player) or self.check_solo_moves(state, itemName.LSPRING) and \
                    self.check_solo_moves(state, itemName.GLIDE) and (self.check_solo_moves(state, itemName.WWHACK) or \
                    state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.CLAWBTS, self.player) or self.check_solo_moves(state, itemName.LSPRING) and \
                    self.check_solo_moves(state, itemName.GLIDE) and (self.check_solo_moves(state, itemName.WWHACK) or \
                    state.has(itemName.EGGAIM, self.player))
        return logic
    
    #TODO check
    def can_access_gi_fl2_2fl3all(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (state.has(itemName.GGRAB, self.player) or self.check_humba_magic(state, itemName.HUMBAGI)) and \
                    state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAGI) and state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAGI) and state.has(itemName.CLAWBTS, self.player)
        return logic
    
    def can_access_hailfire(self, state: CollectionState, fromTrain) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hfp_jiggy(state) and self.can_access_clifftop(state, False)
        elif self.world.options.logic_type == 1: # normal
            if fromTrain:
                logic = self.hfp_jiggy(state) and self.can_access_clifftop(state, fromTrain)
            else:
                logic = (self.hfp_jiggy(state) and self.can_access_clifftop(state, fromTrain)) or \
                        self.has_train_access(state, "HFP")
        elif self.world.options.logic_type == 2: # advanced
            if fromTrain:
                logic = self.hfp_jiggy(state) and self.can_access_clifftop(state, fromTrain)
            else:
                logic = (self.hfp_jiggy(state) and self.can_access_clifftop(state, fromTrain)) or \
                        self.has_train_access(state, "HFP")
        return logic
    
    def hfp_jiggy(self, state: CollectionState) -> bool: # 36
        if self.world.worlds_randomized == True:
            return state.has(itemName.HFA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.HP]
            return state.has(itemName.JIGGY, self.player, amt)
    
    def can_access_ccl(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.ccl_jiggy(state) and self.can_access_wasteland(state, False)
        elif self.world.options.logic_type == 1: # normal
            logic = self.ccl_jiggy(state) and self.can_access_wasteland(state, False)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.ccl_jiggy(state) and self.can_access_wasteland(state, False)
        return logic
    
    def ccl_jiggy(self, state: CollectionState) -> bool: # 45
        if self.world.worlds_randomized == True:
            return state.has(itemName.CCA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.CC]
            return state.has(itemName.JIGGY, self.player, amt)
    
    def can_access_ck(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.JIGGY, self.player, 55) and self.can_access_quagmire(state, False) and \
            state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.JIGGY, self.player, 55) and self.can_access_quagmire(state, False) and \
            state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.JIGGY, self.player, 55) and self.can_access_quagmire(state, False) and \
            state.has(itemName.CLAWBTS, self.player)
        return logic
    
    def has_train_access(self, state: CollectionState, station) -> bool:
        # sys.setrecursionlimit(1500)
        logic = False
        if station == "WW":
            #Can't make it 1 Statement, get Python Recursion limit error due to ALOT of checking 
            # logic = (self.TDL_train_station(state) and self.can_access_tdl(state)) or \
            #         (self.can_access_clifftop(state) and self.CT_train_station(state)) or \
            #         (self.can_access_hailfire(state) and self.HFPF_train_station(state)) or \
            #         (self.can_beat_king_coal(state) and self.can_access_GM(state)) and \
            #         self.WW_train_station(state)
            if(self.TDL_train_station(state) and self.can_access_tdl(state, True)) and self.WW_train_station(state):
               return True
            if (self.can_access_clifftop(state, True) and self.CT_train_station(state)) and self.WW_train_station(state):
                return True
            if (self.can_access_hailfire(state, True) and self.HFPF_train_station(state)) and self.WW_train_station(state):
                return True
            if (self.can_beat_king_coal(state) and self.can_access_GM(state)) and self.WW_train_station(state):
                return True
            if (self.can_access_gruntyindustries_outside(state, True) and self.GI_train_station(state)) and \
                (state.has(itemName.CLAWBTS, self.player)) and self.WW_train_station(state):
                return True
        if station == "TDL":
            if(self.WW_train_station(state) and self.can_access_witchyworld(state, True)) and self.TDL_train_station(state):
                return True
            if (self.can_access_clifftop(state, True) and self.CT_train_station(state)) and self.TDL_train_station(state):
                return True
            if (self.can_access_hailfire(state, True) and self.HFPF_train_station(state)) and self.TDL_train_station(state):
                return True
            if (self.can_beat_king_coal(state) and self.can_access_GM(state)) and self.TDL_train_station(state):
                return True
            if (self.can_access_gruntyindustries_outside(state, True) and self.GI_train_station(state)) and \
                (state.has(itemName.CLAWBTS, self.player)) and self.WW_train_station(state):
                return True
        if station == "HFP":
            if(self.WW_train_station(state) and self.can_access_witchyworld(state, True)) and self.HFPF_train_station(state):
                return True
            if (self.can_access_clifftop(state, True) and self.CT_train_station(state)) and self.HFPF_train_station(state):
                return True
            if (self.TDL_train_station(state) and self.can_access_tdl(state, True)) and self.HFPF_train_station(state):
                return True
            if (self.can_beat_king_coal(state) and self.can_access_GM(state)) and self.HFPF_train_station(state):
                return True
            if (self.can_access_gruntyindustries_outside(state, True) and self.GI_train_station(state)) and \
                (state.has(itemName.CLAWBTS, self.player)) and self.HFPF_train_station(state):
                return True
        if station == "CT":
            if(self.WW_train_station(state) and self.can_access_witchyworld(state, True)) and self.CT_train_station(state):
                return True
            if (self.can_access_tdl(state, True) and self.TDL_train_station(state)) and self.CT_train_station(state):
                return True
            if (self.can_beat_king_coal(state) and self.can_access_GM(state)) and self.CT_train_station(state):
                return True
            if (self.can_access_gruntyindustries_outside(state, True) and self.GI_train_station(state)) and \
                (state.has(itemName.CLAWBTS, self.player)) and self.CT_train_station(state):
                return True
        if station == "GI":
            if(self.WW_train_station(state) and self.can_access_witchyworld(state, True)) and self.GI_train_station(state):
                return True
            if (self.can_access_clifftop(state, True) and self.CT_train_station(state)) and self.GI_train_station(state):
                return True
            if (self.can_access_hailfire(state, True) and self.HFPF_train_station(state)) and self.GI_train_station(state):
                return True
            if (self.can_beat_king_coal(state) and self.can_access_GM(state)) and self.GI_train_station(state):
                return True
            if(self.TDL_train_station(state) and self.can_access_tdl(state, True)) and self.GI_train_station(state):
               return True
        # sys.setrecursionlimit(997)
        return logic
    
    def can_leave_GI_from_inside(self, state:CollectionState) -> bool:
        return self.has_train_access(state, "GI") and (state.has(itemName.SPLITUP, self.player) or \
               state.has(itemName.CLAWBTS, self.player))

    def WW_train_station(self, state) -> bool:
        return self.can_beat_king_coal(state) and \
            (state.has(itemName.TRAINSWWW, self.player))

    def CT_train_station(self, state) -> bool:
        return self.can_beat_king_coal(state) and \
            (state.has(itemName.TRAINSWIH, self.player))
    
    def HFPF_train_station(self, state) -> bool:
        return self.can_beat_king_coal(state) and \
            (state.has(itemName.TRAINSWHP1, self.player))
    
    def GI_train_station(self, state) -> bool:
        return self.can_beat_king_coal(state) and \
            (state.has(itemName.TRAINSWGI, self.player))
    
    def TDL_train_station(self, state) -> bool:
        return self.can_beat_king_coal(state) and \
            (state.has(itemName.TRAINSWTD, self.player))

    #TODO Needs to handle proper world access
    def HFP_hot_water_cooled(self, state) -> bool:
        return self.ccl_jiggy(state) and \
               state.has(itemName.SPLITUP, self.player) and \
               state.has(itemName.FEGGS, self.player) and \
               state.has(itemName.TTORP, self.player)

    def can_use_floatus(self, state) -> bool:
        return self.check_solo_moves(state, itemName.TAXPACK) and self.check_solo_moves(state, itemName.HATCH)

    def grow_beanstalk(self, state: CollectionState) -> bool:
        return state.has(itemName.BDRILL, self.player) and self.check_mumbo_magic(state, itemName.MUMBOCC)

    def check_hag1_options(self, state: CollectionState) -> bool:
        enough_jiggies = state.has(itemName.JIGGY, self.player, 55) if self.world.options.open_hag1 == 1 else state.has(itemName.JIGGY, self.player, 70)
        return enough_jiggies and \
                (self.check_solo_moves(state, itemName.PACKWH) or self.check_solo_moves(state, itemName.SAPACK) or
                self.check_solo_moves(state, itemName.SHPACK)) and \
                state.has(itemName.BBLASTER, self.player) and \
                state.has(itemName.CEGGS, self.player)

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

        for location, rules in self.treble_clef_rules.items():
            treble = self.world.multiworld.get_location(location, self.player)
            set_rule(treble, rules)

        for region_name, rules in self.station_rules.items():
            station = self.world.multiworld.get_region(region_name, self.player)
            for entrance in station.entrances:
                entrance.access_rule = rules

        for location, rules in self.train_rules.items():
            train = self.world.multiworld.get_location(location, self.player)
            set_rule(train, rules)

        for location, rules in self.jinjo_rules.items():
            jinjo = self.world.multiworld.get_location(location, self.player)
            set_rule(jinjo, rules)

        for location, rules in self.notes_rules.items():
            notes = self.world.multiworld.get_location(location, self.player)
            set_rule(notes, rules)

        # for location, rules in self.access_rules.items():
        #     access = self.world.multiworld.get_location(location, self.player)
        #     set_rule(access, rules)

        for item in self.moves_forbid:
            #The Doubloons near Wing Wack Silo
            forbid_item(self.world.multiworld.get_location(locationName.JRLDB10, self.player), item, self.player)
            forbid_item(self.world.multiworld.get_location(locationName.JRLDB9, self.player), item, self.player)
            forbid_item(self.world.multiworld.get_location(locationName.JRLDB8, self.player), item, self.player)
            forbid_item(self.world.multiworld.get_location(locationName.JRLDB7, self.player), item, self.player)
            if self.world.options.forbid_on_jinjo_family == 1 or self.world.options.forbid_on_jinjo_family == 2:
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH1, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH2, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH3, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH4, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH5, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH6, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH7, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH8, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH9, self.player), item, self.player)
        
        if self.world.options.forbid_on_jinjo_family == 2 or self.world.options.forbid_on_jinjo_family == 3:
            for item in self.magic_forbid:
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH1, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH2, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH3, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH4, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH5, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH6, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH7, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH8, self.player), item, self.player)
                forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH9, self.player), item, self.player)

        if self.world.options.forbid_jinjos_on_jinjo_family == True:
            for item in self.jinjo_forbid:
                    forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH1, self.player), item, self.player)
                    forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH2, self.player), item, self.player)
                    forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH3, self.player), item, self.player)
                    forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH4, self.player), item, self.player)
                    forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH5, self.player), item, self.player)
                    forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH6, self.player), item, self.player)
                    forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH7, self.player), item, self.player)
                    forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH8, self.player), item, self.player)
                    forbid_item(self.world.multiworld.get_location(locationName.JIGGYIH9, self.player), item, self.player)

        self.world.multiworld.completion_condition[self.player] = lambda state: state.has("Kick Around", self.player)
