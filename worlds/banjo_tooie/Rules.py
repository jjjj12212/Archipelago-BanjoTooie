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

        if self.world.options.skip_puzzles == True:
            
            self.access_rules = {
                locationName.W1: lambda state: self.WorldUnlocks_req(state, 1230944),
                locationName.W2: lambda state: self.WorldUnlocks_req(state, 1230945),
                locationName.W3: lambda state: self.WorldUnlocks_req(state, 1230946),
                locationName.W4: lambda state: self.WorldUnlocks_req(state, 1230947),
                locationName.W5: lambda state: self.WorldUnlocks_req(state, 1230948),
                locationName.W6: lambda state: self.WorldUnlocks_req(state, 1230949),
                locationName.W7: lambda state: self.WorldUnlocks_req(state, 1230950),
                locationName.W8: lambda state: self.WorldUnlocks_req(state, 1230951),
                locationName.W9: lambda state: self.WorldUnlocks_req(state, 1230952)
            }

        if self.world.options.victory_condition.value == 1 or self.world.options.victory_condition.value == 4:
            self.gametoken_rules = {
                locationName.MUMBOTKNGAME1: lambda state: self.jiggy_mayhem_kickball(state),
                locationName.MUMBOTKNGAME2: lambda state: self.jiggy_ordnance_storage(state),
                locationName.MUMBOTKNGAME3: lambda state: self.jiggy_hoop_hurry(state),
                locationName.MUMBOTKNGAME4: lambda state: self.jiggy_dodgem(state),
                locationName.MUMBOTKNGAME5: lambda state: self.jiggy_peril(state),
                locationName.MUMBOTKNGAME6: lambda state: self.jiggy_balloon_burst(state),
                locationName.MUMBOTKNGAME7: lambda state: self.jiggy_sub_challenge(state),
                locationName.MUMBOTKNGAME8: lambda state: self.jiggy_chompa(state),
                locationName.MUMBOTKNGAME9: lambda state: self.jiggy_clinkers(state),
                locationName.MUMBOTKNGAME10: lambda state: self.jiggy_twinkly(state),
                locationName.MUMBOTKNGAME11: lambda state: self.jiggy_hfp_kickball(state),
                locationName.MUMBOTKNGAME12: lambda state: self.jiggy_gold_pot(state),
                locationName.MUMBOTKNGAME13: lambda state: self.check_humba_magic(state, itemName.HUMBACC),
                locationName.MUMBOTKNGAME14: lambda state: self.jiggy_trash(state),
                locationName.MUMBOTKNGAME15: lambda state: self.canary_mary_free(state) and self.can_access_GM(state),

            }

        if self.world.options.victory_condition.value == 2 or self.world.options.victory_condition.value == 4:
            self.bosstoken_rules = {
                locationName.MUMBOTKNBOSS1: lambda state: self.jiggy_targitzan(state),
                locationName.MUMBOTKNBOSS2: lambda state: self.can_beat_king_coal(state),
                locationName.MUMBOTKNBOSS3: lambda state: self.jiggy_patches(state),
                locationName.MUMBOTKNBOSS4: lambda state: self.jiggy_lord_woo(state),
                locationName.MUMBOTKNBOSS5: lambda state: self.can_beat_terry(state),
                locationName.MUMBOTKNBOSS6: lambda state: self.can_beat_weldar(state),
                locationName.MUMBOTKNBOSS7: lambda state: self.jiggy_dragons_bros(state),
            }
        
        if self.world.options.victory_condition.value == 3 or self.world.options.victory_condition.value == 4:
            self.jinjotoken_rules = {
                locationName.MUMBOTKNJINJO1: lambda state: state.has(itemName.WJINJO, self.player, 1),
                locationName.MUMBOTKNJINJO2: lambda state: state.has(itemName.OJINJO, self.player, 2),
                locationName.MUMBOTKNJINJO3: lambda state: state.has(itemName.YJINJO, self.player, 3),
                locationName.MUMBOTKNJINJO4: lambda state: state.has(itemName.BRJINJO, self.player, 4),
                locationName.MUMBOTKNJINJO5: lambda state: state.has(itemName.GJINJO, self.player, 5),
                locationName.MUMBOTKNJINJO6: lambda state: state.has(itemName.RJINJO, self.player, 6),
                locationName.MUMBOTKNJINJO7: lambda state: state.has(itemName.BLJINJO, self.player, 7),
                locationName.MUMBOTKNJINJO8: lambda state: state.has(itemName.PJINJO, self.player, 8),
                locationName.MUMBOTKNJINJO9: lambda state: state.has(itemName.BKJINJO, self.player, 9),
            }

        if self.world.options.cheato_rewards.value == True:
            self.cheato_rewards_rules = {
                locationName.CHEATOR1: lambda state: self.reach_cheato(state, 5),
                locationName.CHEATOR2: lambda state: self.reach_cheato(state, 10),
                locationName.CHEATOR3: lambda state: self.reach_cheato(state, 15),
                locationName.CHEATOR4: lambda state: self.reach_cheato(state, 20),
                locationName.CHEATOR5: lambda state: self.reach_cheato(state, 25),
            }

        self.train_rules = {
            locationName.CHUFFY: lambda state: self.can_beat_king_coal(state),
            locationName.TRAINSWIH: lambda state: state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP),
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
            locationName.JIGGYTD6:  lambda state: self.jiggy_chompa(state),
            locationName.JIGGYTD7:  lambda state: self.jiggy_terry_kids(state),
            locationName.JIGGYTD8:  lambda state: self.jiggy_stomping_plains(state),
            locationName.JIGGYTD9:  lambda state: self.jiggy_rocknuts(state),
            locationName.JIGGYTD10: lambda state: self.jiggy_roar_cage(state),

            #Grunty Industries Jiggies
            locationName.JIGGYGI1: lambda state: self.jiggy_underwater_waste_disposal(state),
            locationName.JIGGYGI2: lambda state: self.can_beat_weldar(state),
            locationName.JIGGYGI3: lambda state: self.jiggy_clinkers(state),
            locationName.JIGGYGI4: lambda state: self.jiggy_skivvy(state),
            locationName.JIGGYGI5: lambda state: self.jiggy_floor5(state),
            locationName.JIGGYGI6: lambda state: self.jiggy_qa(state),
            locationName.JIGGYGI7: lambda state: self.jiggy_guarded(state),
            locationName.JIGGYGI8: lambda state: self.jiggy_compactor(state),
            locationName.JIGGYGI9: lambda state: self.jiggy_twinkly(state),
            locationName.JIGGYGI10: lambda state: self.jiggy_plantbox(state),

            #Hailfire Peaks Jiggies
            locationName.JIGGYHP1:  lambda state: self.jiggy_dragons_bros(state),
            locationName.JIGGYHP3:  lambda state: self.jiggy_sabreman(state),
            locationName.JIGGYHP4:  lambda state: self.jiggy_boggy(state),
            locationName.JIGGYHP5:  lambda state: self.jiggy_ice_station(state),
            locationName.JIGGYHP6:  lambda state: self.jiggy_oil_drill(state),
            locationName.JIGGYHP7:  lambda state: self.jiggy_hfp_stomping(state),
            locationName.JIGGYHP8:  lambda state: self.jiggy_hfp_kickball(state),
            locationName.JIGGYHP9:  lambda state: self.jiggy_aliens(state),
            locationName.JIGGYHP10: lambda state: self.jiggy_colosseum_split(state),

            #Cloud Cuckooland Jiggies
            locationName.JIGGYCC2: lambda state: self.jiggy_mr_fit(state),
            locationName.JIGGYCC3: lambda state: self.jiggy_gold_pot(state),
            locationName.JIGGYCC4: lambda state: self.canary_mary_free(state) and self.can_access_GM(state),
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
            locationName.CHEATOGM2: lambda state: self.cheato_gm_entrance(state),
            locationName.CHEATOGM3: lambda state: self.cheato_waterstorage(state),

            locationName.CHEATOWW1: lambda state: self.cheato_hauntedcavern(state),
            locationName.CHEATOWW2: lambda state: self.cheato_inferno(state),
            locationName.CHEATOWW3: lambda state: self.cheato_sauceperil(state),
                                            
            locationName.CHEATOJR1: lambda state: state.has(itemName.DOUBLOON, self.player, 28),
            locationName.CHEATOJR2: lambda state: self.cheato_seemee(state),
            locationName.CHEATOJR3: lambda state: self.cheato_ancientbath(state),

            locationName.CHEATOTL1: lambda state: self.cheato_dippypool(state),
            locationName.CHEATOTL2: lambda state: self.cheato_trex(state),
            locationName.CHEATOTL3: lambda state: self.cheato_tdlboulder(state),

            locationName.CHEATOGI1: lambda state: self.cheato_loggo(state),
            locationName.CHEATOGI3: lambda state: self.can_beat_weldar(state),

            locationName.CHEATOHP1: lambda state: self.cheato_colosseum(state),
            locationName.CHEATOHP2: lambda state: state.has(itemName.CEGGS, self.player) or self.check_solo_moves(state, itemName.SHPACK),
            locationName.CHEATOHP3: lambda state: self.cheato_icypillar(state),

            locationName.CHEATOCC1: lambda state: self.canary_mary_free(state) and self.can_access_GM(state),
            locationName.CHEATOCC2: lambda state: self.cheato_potgold(state),
            locationName.CHEATOCC3: lambda state: self.check_humba_magic(state, itemName.HUMBACC),

            locationName.CHEATOSM1: lambda state: self.cheato_spiral(state)
        }
        self.honey_rules = {
            locationName.HONEYCMT1: lambda state: self.honeycomb_mt_entrance(state),
            locationName.HONEYCMT2: lambda state: self.honeycomb_bovina(state),
            locationName.HONEYCMT3: lambda state: self.honeycomb_tchamber(state),

            locationName.HONEYCGM1: lambda state: self.GM_boulders(state),
            locationName.HONEYCGM2: lambda state: self.honeycomb_prospector(state),
            locationName.HONEYCGM3: lambda state: self.honeycomb_gm_station(state),

            locationName.HONEYCWW1: lambda state: self.honeycomb_spacezone(state),
            locationName.HONEYCWW2: lambda state: self.honeycomb_inferno(state),
            locationName.HONEYCWW3: lambda state: self.honeycomb_crazycastle(state),

            locationName.HONEYCJR1: lambda state: self.honeycomb_seemee(state),
            locationName.HONEYCJR2: lambda state: self.honeycomb_atlantis(state),
            locationName.HONEYCJR3: lambda state: self.honeycomb_jrlpipes(state),
                                                
            locationName.HONEYCTL2: lambda state: self.honeycomb_styracosaurus(state),

            locationName.HONEYCGI1: lambda state: self.honeycomb_floor3(state),
            locationName.HONEYCGI2: lambda state: self.honeycomb_gistation(state),

            locationName.HONEYCHP1: lambda state: self.honeycomb_volcano(state),
            locationName.HONEYCHP2: lambda state: self.honeycomb_hfpstation(state),
            locationName.HONEYCHP3: lambda state: self.honeycomb_lavaside(state),

            locationName.HONEYCCC1: lambda state: state.has(itemName.BDRILL, self.player),

            locationName.HONEYCIH1: lambda state: self.plateauTop(state)

        }
        self.glowbo_rules = {
            locationName.GLOWBOMT2: lambda state: self.can_access_JSG(state),

            locationName.GLOWBOGM1: lambda state: self.GGMSlope(state),

            locationName.GLOWBOWW1: lambda state: self.glowbo_inferno(state),
            locationName.GLOWBOWW2: lambda state: self.glowbo_wigwam(state),

            locationName.GLOWBOJR2: lambda state: self.glowbo_underwigwam(state),

            locationName.GLOWBOCC2: lambda state: self.glowbo_cavern(state),

            locationName.GLOWBOIH1: lambda state: self.glowbo_cliff(state),
            locationName.GLOWBOMEG: lambda state: self.mega_glowbo(state)

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
            locationName.TREBLEGM:  lambda state: self.treble_gm(state),
            locationName.TREBLEWW:  lambda state: self.treble_ww(state),
            locationName.TREBLEJR:  lambda state: self.treble_jrl(state),
            locationName.TREBLETL:  lambda state: self.treble_tdl(state),
            locationName.TREBLEGI:  lambda state: self.treble_gi(state),
            locationName.TREBLEHP:  lambda state: self.treble_hfp(state),
        }

        self.silo_rules = {
            ## Faster swimming and double air rules are here ##
            locationName.ROYSTEN1: lambda state: state.has(itemName.BDRILL, self.player),
            locationName.ROYSTEN2: lambda state: state.has(itemName.BDRILL, self.player),

            locationName.EGGAIM: lambda state: self.check_notes(state, 25),
            locationName.BBLASTER: lambda state: self.check_notes(state, 30),
            locationName.GGRAB: lambda state: self.can_access_JSG(state) and 
                                              self.check_notes(state, 35),

            locationName.BDRILL: lambda state: self.silo_bill_drill(state),
            locationName.BBAYONET: lambda state: self.GM_boulders(state) and self.check_notes(state, 95),

            locationName.AIREAIM: lambda state: self.check_notes(state, 180),
            locationName.SPLITUP: lambda state: self.check_notes(state, 160),
            locationName.PACKWH: lambda state: state.has(itemName.SPLITUP, self.player) and self.check_notes(state, 170),

            locationName.AUQAIM: lambda state: (self.has_explosives(state) or state.has(itemName.DOUBLOON, self.player, 28)) and
                                               self.check_notes(state, 275),
            locationName.TTORP: lambda state:  self.can_reach_atlantis(state) and state.has(itemName.GGRAB, self.player) and
                                               self.check_notes(state, 290),
            locationName.WWHACK: lambda state: (self.has_explosives(state)) and state.has(itemName.SPLITUP, self.player) and
                                               self.check_notes(state, 265),

            locationName.SPRINGB: lambda state: self.check_notes(state, 390),
            locationName.TAXPACK: lambda state: self.can_access_taxi_pack_silo(state) and self.check_notes(state, 405),
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
            locationName.JINJOIH5: lambda state: state.has(itemName.TTORP, self.player) and self.hasBKMove(state, itemName.DIVE),
            locationName.JINJOIH4: lambda state: self.jinjo_plateau(state),
            locationName.JINJOIH3: lambda state: self.jinjo_clifftop(state),
            locationName.JINJOIH2: lambda state: self.jinjo_wasteland(state),

            locationName.JINJOMT1: lambda state: self.jinjo_jadesnakegrove(state),
            locationName.JINJOMT2: lambda state: self.jinjo_stadium(state),
            locationName.JINJOMT3: lambda state: state.has(itemName.BBLASTER, self.player),
            locationName.JINJOMT4: lambda state: self.jinjo_pool(state),

            #Water Storage Jinjo always true because it's in the GMWSJT area
            locationName.JINJOGM2: lambda state: self.humbaGGM(state),
            locationName.JINJOGM4: lambda state: self.humbaGGM(state) or (self.hasBKMove(state, itemName.TTROT) and state.has(itemName.BDRILL, self.player)),

            locationName.JINJOWW2: lambda state: self.jinjo_caveofhorror(state),
            locationName.JINJOWW3: lambda state: self.jinjo_vandoor(state),
            locationName.JINJOWW5: lambda state: self.jinjo_cactus(state),

            locationName.JINJOJR1: lambda state: self.jinjo_alcove(state),
            locationName.JINJOJR5: lambda state: self.jinjo_sunkenship(state),
            locationName.JINJOJR4: lambda state: self.jinjo_seaweedsanctum(state),
            locationName.JINJOJR3: lambda state: self.jinjo_bigfish(state),

            locationName.JINJOTL2: lambda state: self.jinjo_tdlentrance(state),
            locationName.JINJOTL1: lambda state: state.has(itemName.TTORP, self.player),
            locationName.JINJOTL3: lambda state: self.canShootEggs(state, itemName.CEGGS),
            locationName.JINJOTL4: lambda state: self.jinjo_big_t_rex(state),
            locationName.JINJOTL5: lambda state: self.jinjo_stomping_plains(state),

            locationName.JINJOGI2: lambda state: self.jinjo_legspring(state),
            locationName.JINJOGI3: lambda state: self.jinjo_wasteplant(state),
            locationName.JINJOGI5: lambda state: self.jinjo_floor4(state),

            locationName.JINJOHP2: lambda state: self.jinjo_hot_pool(state),
            locationName.JINJOHP3: lambda state: self.jinjo_windtunnel(state),
            locationName.JINJOHP4: lambda state: self.jinjo_icegrotto(state),
            locationName.JINJOHP5: lambda state: self.jinjo_mildred(state),
            
            locationName.JINJOCC1: lambda state: self.jinjo_trashcan(state),
            locationName.JINJOCC2: lambda state: self.jinjo_cheese(state),
            locationName.JINJOCC3: lambda state: self.jinjo_central(state),
        }

        self.notes_rules = {
            locationName.NOTEIH1:  lambda state: self.notes_plateau_sign(state),
            locationName.NOTEIH2:  lambda state: self.notes_plateau_sign(state),
            locationName.NOTEIH3:  lambda state: self.plateauTop(state),
            locationName.NOTEIH4:  lambda state: self.plateauTop(state),
            locationName.NOTEIH13:  lambda state: self.notes_bottom_clockwork(state),
            locationName.NOTEIH14:  lambda state: self.notes_top_clockwork(state),

            locationName.NOTEGGM1:  lambda state: self.notes_green_pile(state),
            locationName.NOTEGGM2:  lambda state: self.notes_green_pile(state),
            locationName.NOTEGGM3:  lambda state: self.notes_green_pile(state),
            locationName.NOTEGGM4:  lambda state: self.notes_green_pile(state),
            # TODO: needs testing and take into consideration top access
            locationName.NOTEGGM5: lambda state: self.placeholder_prospector_note(state),
            locationName.NOTEGGM6: lambda state: self.placeholder_prospector_note(state),
            locationName.NOTEGGM7: lambda state: self.placeholder_prospector_note(state),
            locationName.NOTEGGM8: lambda state: self.placeholder_prospector_note(state),
            locationName.NOTEGGM9: lambda state: self.placeholder_prospector_note(state),
            locationName.NOTEGGM10: lambda state: self.notes_gm_mumbo(state),
            locationName.NOTEGGM11: lambda state: self.notes_gm_mumbo(state),
            locationName.NOTEGGM12: lambda state: self.notes_gm_mumbo(state),
            # TODO Fuel Depot notes are weird, will need a ton of testing
            locationName.NOTEGGM13: lambda state: self.placeholder_fuel_depot(state),
            locationName.NOTEGGM14: lambda state: self.placeholder_fuel_depot(state),
            locationName.NOTEGGM15: lambda state: self.placeholder_fuel_depot(state),
            locationName.NOTEGGM16: lambda state: self.placeholder_fuel_depot(state),


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

        self.stopnswap_rules = {
            locationName.IKEY:      lambda state: self.ice_key(state),
            locationName.PMEGG:     lambda state: self.pink_egg(state),
            locationName.PMEGGH:    lambda state: state.has(itemName.PMEGG, self.player),
            locationName.BMEGG:     lambda state: self.blue_egg(state),
            locationName.BMEGGH:    lambda state: state.has(itemName.BMEGG, self.player),
            locationName.YMEGGH:    lambda state: (self.has_explosives(state) or state.has(itemName.BDRILL, self.player)) and self.check_solo_moves(state, itemName.HATCH)
        }

    def jiggy_targitzan(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
          logic = state.has(itemName.BBLASTER, self.player)
        elif self.world.options.logic_type == 1: # normal
          logic = state.has(itemName.BBLASTER, self.player)
        elif self.world.options.logic_type == 2: # advanced
          logic = state.has(itemName.BBLASTER, self.player)
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.glitchedJSGAccess(state)
        return logic

    def jiggy_bovina(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
          logic = state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
          logic = state.has(itemName.EGGAIM, self.player) or (self.MT_flight_pad(state) and state.has(itemName.AIREAIM, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = (self.hasBKMove(state, itemName.FFLIP) and self.hasBKMove(state, itemName.BBUST)) or self.hasBKMove(state, itemName.EGGSHOOT)\
                        or state.has(itemName.EGGAIM, self.player) or (self.MT_flight_pad(state) and state.has(itemName.AIREAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.hasBKMove(state, itemName.FFLIP) and self.hasBKMove(state, itemName.BBUST)) or self.hasBKMove(state, itemName.EGGSHOOT)\
                        or state.has(itemName.EGGAIM, self.player) or (self.MT_flight_pad(state) and state.has(itemName.AIREAIM, self.player))
        return logic
    
    def jiggy_treasure_chamber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.EGGAIM,  self.player) and\
                (self.hasBKMove(state, itemName.FFLIP) or self.canReachSlightlyElevatedLedge(state)) and\
                  ((state.has(itemName.GGRAB, self.player) and self.BKSpringPad(state) and self.hasBKMove(state, itemName.FFLIP)) or self.MT_flight_pad(state))
        elif self.world.options.logic_type == 1: # normal
            logic = (self.hasBKMove(state, itemName.FFLIP) or self.canReachSlightlyElevatedLedge(state)) and\
                  ((state.has(itemName.GGRAB, self.player) and self.BKSpringPad(state) and self.hasBKMove(state, itemName.FFLIP) and self.canShootLinearEgg(state) and state.has(itemName.EGGAIM, self.player))\
                    or (self.MT_flight_pad(state) and self.canShootLinearEgg(state)))
        elif self.world.options.logic_type == 2: # advanced
            logic = (self.hasBKMove(state, itemName.FFLIP) or self.canReachSlightlyElevatedLedge(state)) and\
                  ((state.has(itemName.GGRAB, self.player) and self.BKSpringPad(state) and self.hasBKMove(state, itemName.FFLIP) and self.canShootLinearEgg(state) and state.has(itemName.EGGAIM, self.player))\
                    or (self.MT_flight_pad(state) and self.canShootLinearEgg(state)))
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.hasBKMove(state, itemName.FFLIP) or self.canReachSlightlyElevatedLedge(state)) and\
                  ((state.has(itemName.GGRAB, self.player) and self.BKSpringPad(state) and self.hasBKMove(state, itemName.FFLIP) and self.canShootLinearEgg(state) and state.has(itemName.EGGAIM, self.player))\
                    or (self.MT_flight_pad(state) and self.canShootLinearEgg(state)))
        return logic
    
    def jiggy_golden_goliath(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT) or (self.glitchedJSGAccess(state) and self.canShootEggs(state, itemName.CEGGS))
        return logic
    
    def jiggy_prison_quicksand(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canReachSlightlyElevatedLedge(state)\
                  and self.hasBKMove(state, itemName.SSTRIDE) and self.prison_compound_open(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.canReachSlightlyElevatedLedge(state)\
                  and self.hasBKMove(state, itemName.SSTRIDE) and self.prison_compound_open(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canReachSlightlyElevatedLedge(state)\
                  and self.hasBKMove(state, itemName.SSTRIDE) and self.prison_compound_open(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canReachSlightlyElevatedLedge(state)\
                  and self.hasBKMove(state, itemName.SSTRIDE) and self.prison_compound_open(state)
        return logic
    
    def jiggy_pillars(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BDRILL, self.player) and (self.hasBKMove(state, itemName.DIVE) or self.canReachSlightlyElevatedLedge(state))\
                    and self.canDoSmallElevation(state) and self.prison_compound_open(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BDRILL, self.player) and self.canDoSmallElevation(state) and self.prison_compound_open(state)\
                    and (self.hasBKMove(state, itemName.DIVE) or self.canReachSlightlyElevatedLedge(state))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.prison_compound_open(state) and \
                ((state.has(itemName.BDRILL, self.player) and self.canDoSmallElevation(state)) or self.extremelyLongJump(state))\
                    and (self.hasBKMove(state, itemName.DIVE) or self.canReachSlightlyElevatedLedge(state))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.prison_compound_open(state) and \
                ((state.has(itemName.BDRILL, self.player) and self.canDoSmallElevation(state)) or self.extremelyLongJump(state))\
                    and (self.hasBKMove(state, itemName.DIVE) or self.canReachSlightlyElevatedLedge(state))
        return logic
    
    def jiggy_ssslumber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hasBKMove(state, itemName.TTROT) and state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP) and self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 1: # normal
            logic = self.hasBKMove(state, itemName.TTROT) and (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST))\
                and self.hasBKMove(state, itemName.FFLIP) and self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.hasBKMove(state, itemName.TTROT) and (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST))\
                and self.hasBKMove(state, itemName.FFLIP) and self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasBKMove(state, itemName.TTROT) and (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST))\
                and self.hasBKMove(state, itemName.FFLIP) and (self.check_mumbo_magic(state, itemName.MUMBOMT) or self.glitchedJSGAccess(state))
        return logic

    def jiggy_generator_cavern(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
          logic = state.has(itemName.FEGGS, self.player) and state.has(itemName.EGGAIM, self.player) and self.canDoSmallElevation(state)
        elif self.world.options.logic_type == 1: # normal
          logic = self.canDoSmallElevation(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canDoSmallElevation(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canDoSmallElevation(state)
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
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.BBLASTER, self.player) and state.has(itemName.BBAYONET, self.player) and \
                    self.GM_boulders(state)
        return logic
    
    def jiggy_crushing_shed(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.mumboGGM(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.mumboGGM(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.mumboGGM(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.mumboGGM(state)
        return logic
    
    def jiggy_waterfall(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPRINGB, self.player)

        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPRINGB, self.player) or \
                    ((self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)) and \
                     self.GM_boulders(state))
            
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPRINGB, self.player) or \
                    ((self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)) and \
                     self.GM_boulders(state))\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.SPRINGB, self.player) or \
                    ((self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)) and \
                     self.GM_boulders(state))\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def jiggy_power_hut(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.GM_boulders(state) and state.has(itemName.SPLITUP, self.player)

        elif self.world.options.logic_type == 1: # normal
            logic = self.GM_boulders(state)
            
        elif self.world.options.logic_type == 2: # advanced
            logic = self.GM_boulders(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.GM_boulders(state)
        return logic
    
    def jiggy_flooded_caves(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.humbaGGM(state) and self.hasBKMove(state, itemName.DIVE)

        elif self.world.options.logic_type == 1: # normal
            logic = self.hasBKMove(state, itemName.DIVE) and self.hasBKMove(state, itemName.TJUMP) and\
                (self.humbaGGM(state) or self.longJump(state))
            
        elif self.world.options.logic_type == 2: # advanced
            logic = self.hasBKMove(state, itemName.DIVE) and self.hasBKMove(state, itemName.TJUMP) and\
                (self.humbaGGM(state) or self.longJump(state))
            
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasBKMove(state, itemName.DIVE) and self.hasBKMove(state, itemName.TJUMP) and\
                (self.humbaGGM(state) or self.longJump(state))
        return logic
    
    def jiggy_hoop_hurry(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player) and self.has_explosives(state) 

        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player) and self.has_explosives(state) 
            
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player) and self.has_explosives(state) 
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.SPLITUP, self.player) and self.has_explosives(state) 
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
        elif self.world.options.logic_type == 3: # glitched
            if self.world.options.speed_up_minigames == 1:
                # No van required if you can clockwork warp into dodgems, since the door is already opened!
                logic = (self.check_humba_magic(state, itemName.HUMBAWW) and self.check_mumbo_magic(state, itemName.MUMBOWW))\
                    or (self.canShootEggs(state, itemName.GEGGS) and self.canShootEggs(state, itemName.CEGGS))
            else:
                logic = self.check_humba_magic(state, itemName.HUMBAWW) and self.check_mumbo_magic(state, itemName.MUMBOWW)
        return logic
    
    # I assume nobody wants to do this from the ground.
    def jiggy_patches(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.AIREAIM, self.player) and state.has(itemName.EGGAIM, self.player) and \
                    state.has(itemName.GEGGS, self.player) and self.hasBKMove(state, itemName.FPAD)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.AIREAIM, self.player) and state.has(itemName.EGGAIM, self.player) and \
                    state.has(itemName.GEGGS, self.player) and self.hasBKMove(state, itemName.FPAD)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.AIREAIM, self.player) and state.has(itemName.EGGAIM, self.player) and \
                    state.has(itemName.GEGGS, self.player) and self.hasBKMove(state, itemName.FPAD)
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.AIREAIM, self.player) and state.has(itemName.EGGAIM, self.player) and \
                    state.has(itemName.GEGGS, self.player) and self.hasBKMove(state, itemName.FPAD)
        return logic

    def jiggy_peril(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.humbaGGM(state) and \
                    self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    self.check_humba_magic(state, itemName.HUMBAWW) and \
                    self.saucer_door_open(state) and state.has(itemName.GGRAB, self.player) and \
                    self.can_access_GM(state) and self.has_explosives(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.humbaGGM(state) and \
                    self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    self.check_humba_magic(state, itemName.HUMBAWW) and \
                    self.saucer_door_open(state) and self.can_access_GM(state) and \
                    self.has_explosives(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.humbaGGM(state) and \
                    self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    self.check_humba_magic(state, itemName.HUMBAWW) and \
                    self.saucer_door_open(state) and self.can_access_GM(state) and \
                    self.has_explosives(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.humbaGGM(state) and \
                    self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    self.check_humba_magic(state, itemName.HUMBAWW) and \
                    self.saucer_door_open(state) and self.can_access_GM(state) and \
                    self.has_explosives(state)
        return logic
    
    def jiggy_balloon_burst(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player) and \
                    state.has(itemName.AIREAIM, self.player) and \
                    self.has_explosives(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player) and \
                    state.has(itemName.AIREAIM, self.player) and \
                    self.has_explosives(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player) and \
                    state.has(itemName.AIREAIM, self.player) and \
                    self.has_explosives(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.SPLITUP, self.player) and \
                    state.has(itemName.AIREAIM, self.player) and \
                    self.has_explosives(state)
        return logic
    
    def jiggy_death_dive(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def jiggy_mrs_boggy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAWW) and \
                self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                self.check_solo_moves(state, itemName.TAXPACK) and \
                self.has_explosives(state) and \
                state.has(itemName.GGRAB, self.player)
            
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAWW) and \
                self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                self.check_solo_moves(state, itemName.TAXPACK) and \
                self.has_explosives(state)
            
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAWW) and \
                self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                self.check_solo_moves(state, itemName.TAXPACK)
            
        elif self.world.options.logic_type == 3: # glitched
            logic = ((self.check_humba_magic(state, itemName.HUMBAWW) and self.check_mumbo_magic(state, itemName.MUMBOWW))\
                     or self.canShootEggs(state, itemName.CEGGS)) and \
                    self.check_solo_moves(state, itemName.TAXPACK)
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
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_mumbo_magic(state, itemName.MUMBOWW) and \
                    self.glitchedInfernoAccess(state)
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
        elif self.world.options.logic_type == 3: # glitched
            logic = self.glitchedInfernoAccess(state)
        return logic
    
    def jiggy_cactus(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BDRILL, self.player) and self.canShootEggs(state, itemName.GEGGS)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BDRILL, self.player) and self.canShootEggs(state, itemName.GEGGS)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.BDRILL, self.player) and self.canShootEggs(state, itemName.GEGGS)
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.BDRILL, self.player) and self.canShootEggs(state, itemName.GEGGS)
        return logic
    
    def jiggy_sub_challenge(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAJR) and self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAJR) and self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAJR)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_humba_magic(state, itemName.HUMBAJR)
        return logic
    
    def jiggy_tiptup(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.HATCH) and self.has_explosives(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_solo_moves(state, itemName.HATCH) and self.has_explosives(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_solo_moves(state, itemName.HATCH) and self.has_explosives(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_solo_moves(state, itemName.HATCH) and self.has_explosives(state)
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
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.AUQAIM, self.player) or \
                (self.check_humba_magic(state, itemName.HUMBAJR) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def jiggy_pigpool(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.HFP_hot_water_cooled(state) and \
                    (self.has_explosives(state) or state.has(itemName.BDRILL, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = (self.has_explosives(state) or \
                    state.has(itemName.BDRILL, self.player)) and \
                    self.HFP_hot_water_cooled(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = (self.has_explosives(state) or \
                    state.has(itemName.BDRILL, self.player)) and \
                    self.HFP_hot_water_cooled(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.has_explosives(state) or \
                    state.has(itemName.BDRILL, self.player)) and \
                    self.HFP_hot_water_cooled(state)
        return logic
    
    def jiggy_smuggler(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.has_explosives(state) and \
                     state.has(itemName.SPLITUP, self.player) and self.check_solo_moves(state, itemName.GLIDE)
        elif self.world.options.logic_type == 1: # normal
            logic = self.has_explosives(state) and \
                     state.has(itemName.SPLITUP, self.player) and self.check_solo_moves(state, itemName.GLIDE)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.has_explosives(state) and \
                     state.has(itemName.SPLITUP, self.player) and self.check_solo_moves(state, itemName.GLIDE)\
                     or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.has_explosives(state) and \
                     state.has(itemName.SPLITUP, self.player) and self.check_solo_moves(state, itemName.GLIDE)\
                     or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def jiggy_merry_maggie(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.AUQAIM, self.player)
        elif self.world.options.logic_type == 3: # glitched
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
            logic = self.can_reach_atlantis(state) and state.has(itemName.GEGGS, self.player) and state.has(itemName.AUQAIM, self.player) and \
                ((state.has(itemName.TTORP, self.player) and state.has(itemName.DAIR, self.player)) or \
                     self.check_mumbo_magic(state, itemName.MUMBOJR) or \
                    self.check_humba_magic(state, itemName.HUMBAJR))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.can_reach_atlantis(state) and state.has(itemName.GEGGS, self.player) and state.has(itemName.AUQAIM, self.player) and \
                ((state.has(itemName.TTORP, self.player) and state.has(itemName.DAIR, self.player)) or \
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
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.TTORP, self.player)
        return logic
    
    def jiggy_ufo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOJR) and state.has(itemName.TTORP, self.player) and \
                    state.has(itemName.EGGAIM, self.player) and state.has(itemName.IEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.TTORP, self.player) and state.has(itemName.EGGAIM, self.player) and \
                    state.has(itemName.IEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.TTORP, self.player) and self.canShootEggs(state, itemName.IEGGS)
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.TTORP, self.player) and self.canShootEggs(state, itemName.IEGGS)
        return logic
    
    def jiggy_terry_nest(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_beat_terry(state) and (self.has_explosives(state) or \
                    state.has(itemName.BDRILL, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = (self.has_explosives(state) or state.has(itemName.BDRILL, self.player)) and self.can_beat_terry(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = (self.has_explosives(state) or state.has(itemName.BDRILL, self.player)) and self.can_beat_terry(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.has_explosives(state) or state.has(itemName.BDRILL, self.player)) and self.can_beat_terry(state)
        return logic
    
    def jiggy_dippy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.TTORP, self.player) and self.can_access_ccl(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.TTORP, self.player) and self.can_access_ccl(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.TTORP, self.player) and self.can_access_ccl(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.TTORP, self.player) and self.can_access_ccl(state)
        return logic
    
    def jiggy_scrotty(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canShootEggs(state, itemName.GEGGS) and self.WW_train_station(state) and \
                    self.CT_train_station(state) and state.has(itemName.TRAINSWTD, self.player) and \
                    self.check_solo_moves(state, itemName.TAXPACK) and self.check_mumbo_magic(state, itemName.MUMBOIH) and \
                    state.has(itemName.BDRILL, self.player) and self.mumboTDL(state) and \
                    state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.canShootEggs(state, itemName.GEGGS) and self.WW_train_station(state) and \
                    self.CT_train_station(state) and state.has(itemName.TRAINSWTD, self.player) and \
                    self.check_solo_moves(state, itemName.TAXPACK) and self.check_mumbo_magic(state, itemName.MUMBOIH) and \
                    state.has(itemName.BDRILL, self.player) and self.mumboTDL(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canShootEggs(state, itemName.GEGGS) and self.WW_train_station(state) and \
                    self.CT_train_station(state) and state.has(itemName.TRAINSWTD, self.player) and \
                    self.check_solo_moves(state, itemName.TAXPACK) and self.check_mumbo_magic(state, itemName.MUMBOIH) and \
                    state.has(itemName.BDRILL, self.player) and self.mumboTDL(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canShootEggs(state, itemName.GEGGS) and self.WW_train_station(state) and \
                    self.CT_train_station(state) and state.has(itemName.TRAINSWTD, self.player) and \
                    self.check_solo_moves(state, itemName.TAXPACK) and self.check_mumbo_magic(state, itemName.MUMBOIH) and \
                    state.has(itemName.BDRILL, self.player) and self.mumboTDL(state)
        return logic
    
    def jiggy_oogle_boogle(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.oogle_boogles_open(state) and self.canShootEggs(itemName.FEGGS) and \
                    self.smuggle_food(state) and state.has(itemName.GGRAB, self.player) and \
                    state.has(itemName.BDRILL, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.oogle_boogles_open(state) and self.has_fire(state) and \
                    self.smuggle_food(state) and state.has(itemName.GGRAB, self.player) and \
                    state.has(itemName.BDRILL, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.oogle_boogles_open(state) and self.has_fire(state) and \
                    state.has(itemName.GGRAB, self.player) and state.has(itemName.BDRILL, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.oogle_boogles_open(state) or self.clockworkWarp(state))\
                    and self.has_fire(state) and state.has(itemName.GGRAB, self.player) and state.has(itemName.BDRILL, self.player)
        return logic

    def jiggy_chompa(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BBLASTER, self.player) and (
                ((self.hasBKMove(state, itemName.TJUMP) or state.has(itemName.GGRAB, self.player)) and self.hasBKMove(state, itemName.FPAD)
                 or (state.has(itemName.EGGAIM, self.player) and self.has_explosives(state)))
            )
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BBLASTER, self.player) and (
                ((self.hasBKMove(state, itemName.TJUMP) or state.has(itemName.GGRAB, self.player)) and self.hasBKMove(state, itemName.FPAD)
                 or (state.has(itemName.EGGAIM, self.player) and self.has_explosives(state) and state.has(itemName.SPRINGB, self.player))
                 or (state.has(itemName.SPRINGB, self.player) and self.veryLongJump(state)))
            )
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.BBLASTER, self.player) and (
                ((self.hasBKMove(state, itemName.TJUMP) or state.has(itemName.GGRAB, self.player)) and self.hasBKMove(state, itemName.FPAD)
                 or (state.has(itemName.EGGAIM, self.player) and self.has_explosives(state) and state.has(itemName.SPRINGB, self.player))
                 or (state.has(itemName.SPRINGB, self.player) and self.veryLongJump(state)))
            )
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.BBLASTER, self.player) and (
                ((self.hasBKMove(state, itemName.TJUMP) or state.has(itemName.GGRAB, self.player)) and self.hasBKMove(state, itemName.FPAD)
                 or (state.has(itemName.EGGAIM, self.player) and self.has_explosives(state) and state.has(itemName.SPRINGB, self.player))
                 or (state.has(itemName.SPRINGB, self.player) and self.veryLongJump(state)))
            )
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
        elif self.world.options.logic_type == 3: # glitched
            logic = self.can_beat_terry(state) and self.check_solo_moves(state, itemName.HATCH) and \
                    self.check_solo_moves(state, itemName.TAXPACK) and self.oogle_boogles_open(state)
        return logic
    
    def jiggy_stomping_plains(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canShootEggs(state, itemName.IEGGS) and state.has(itemName.SPRINGB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPRINGB, self.player) and \
            (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE) or \
            self.canShootEggs(state, itemName.IEGGS))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPRINGB, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def jiggy_rocknuts(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canShootEggs(state, itemName.CEGGS)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canShootEggs(state, itemName.CEGGS)
        return logic

    def jiggy_roar_cage(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBATD)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBATD)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBATD)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_humba_magic(state, itemName.HUMBATD) or (state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player))
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
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_humba_magic(state, itemName.HUMBAGI) and state.has(itemName.BDRILL, self.player)
        return logic
    
    def jiggy_floor5(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.SPLITUP, self.player) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic

    def jiggy_qa(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOGI) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.EGGAIM, self.player) and \
                    self.can_use_battery(state) and self.check_humba_magic(state, itemName.HUMBAGI)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOGI) and self.canShootEggs(state, itemName.GEGGS) and \
                    ((state.has(itemName.EGGAIM, self.player) and (self.check_humba_magic(state, itemName.HUMBAGI)) or \
                    self.check_solo_moves(state, itemName.LSPRING))) and self.can_use_battery(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOGI) and self.canShootEggs(state, itemName.GEGGS) and \
                    self.can_use_battery(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canShootEggs(state, itemName.GEGGS) and\
                  ((self.check_mumbo_magic(state, itemName.MUMBOGI) and self.can_use_battery(state)) or (state.has(itemName.CEGGS, self.player)))
        return logic
    
    def jiggy_guarded(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.SPLITUP, self.player) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def jiggy_compactor(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.SNPACK)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_solo_moves(state, itemName.SNPACK) or self.check_solo_moves(state, itemName.PACKWH)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_solo_moves(state, itemName.SNPACK) or self.check_solo_moves(state, itemName.PACKWH)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_solo_moves(state, itemName.SNPACK) or self.check_solo_moves(state, itemName.PACKWH) or\
                    (state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player) and state.has(itemName.BBASH, self.player) and self.hasBKMove(state, itemName.TTROT))
        return logic
    
    def jiggy_twinkly(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_use_battery(state) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_use_battery(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_use_battery(state)
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
            logic = self.can_use_battery(state)
        return logic

    def jiggy_dragons_bros(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canShootEggs(state, itemName.FEGGS) and self.canShootEggs(state, itemName.IEGGS) and \
                    state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.canShootEggs(state, itemName.FEGGS) and self.canShootEggs(state, itemName.IEGGS) and \
                    state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            # Some people are going to fight Chilly Willy without Claw Clamber Boots, so to prevent softlocks, we also require Pack Whack.
            logic = self.canShootEggs(state, itemName.FEGGS) and self.canShootEggs(state, itemName.IEGGS) and \
                    self.check_solo_moves(state, itemName.PACKWH) and state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 3: # glitched
            # Some people are going to fight Chilly Willy without Claw Clamber Boots, so to prevent softlocks, we also require Pack Whack.
            logic = self.canShootEggs(state, itemName.FEGGS) and self.canShootEggs(state, itemName.IEGGS) and \
                    self.check_solo_moves(state, itemName.PACKWH) and state.has(itemName.CLAWBTS, self.player)
        return logic
    
    def jiggy_sabreman(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOHP) and self.canShootEggs(state, itemName.FEGGS) and \
                    self.check_solo_moves(state, itemName.TAXPACK)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOHP) and self.has_fire(state) and \
                    self.check_solo_moves(state, itemName.TAXPACK)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOHP) and self.has_fire(state) and \
                    self.check_solo_moves(state, itemName.TAXPACK)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_mumbo_magic(state, itemName.MUMBOHP) and self.has_fire(state) and \
                    self.check_solo_moves(state, itemName.TAXPACK)
        return logic

    def jiggy_boggy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_solo_moves(state, itemName.SHPACK) or (state.has(itemName.CEGGS, self.player) and self.hasBKMove(state, itemName.EGGSHOOT)) or self.check_solo_moves(state, itemName.LSPRING)
        return logic
    
    def jiggy_ice_station(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_beat_king_coal(state) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    state.has(itemName.EGGAIM, self.player) and self.can_access_witchyworld(state, False)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_beat_king_coal(state) and self.canShootEggs(state, itemName.GEGGS) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    self.can_access_witchyworld(state, False)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_beat_king_coal(state) and self.canShootEggs(state, itemName.GEGGS) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and self.can_access_witchyworld(state, False)
            
        elif self.world.options.logic_type == 3: # glitched
            logic = self.can_beat_king_coal(state) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and self.can_access_witchyworld(state, False)\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
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
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_humba_magic(state, itemName.HUMBAHP) and self.check_solo_moves(state, itemName.SHPACK) and \
                    (self.check_solo_moves(state, itemName.PACKWH) or state.has(itemName.GGRAB, self.player))
        return logic
    
    def jiggy_hfp_stomping(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.SNPACK) and self.canShootEggs(state, itemName.IEGGS) and \
                    state.has(itemName.SPRINGB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPRINGB, self.player) and \
                    (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE) or \
                     self.canShootEggs(state, itemName.IEGGS)) and \
                    self.check_solo_moves(state, itemName.SNPACK)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPRINGB, self.player) and state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.SPLITUP, self.player) or\
                    (self.can_access_hailfire(state, False) and state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def jiggy_hfp_kickball(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT) and self.has_explosives(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT) and \
                    (self.has_explosives(state) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT) and \
                    (self.has_explosives(state) or self.check_mumbo_magic(state, itemName.MUMBOHP))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT) and \
                    (self.has_explosives(state) or self.check_mumbo_magic(state, itemName.MUMBOHP))
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
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.PACKWH)))\
                    or (state.has(itemName.CEGGS, self.player) and (state.has(itemName.SPLITUP, self.player) or state.has(itemName.EGGAIM, self.player)))
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
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.SPRINGB, self.player) and self.check_solo_moves(state, itemName.SAPACK) and \
                    self.grow_beanstalk(state) and \
                    (self.can_use_floatus(state) or self.check_solo_moves(state, itemName.PACKWH))
        return logic
    
    def jiggy_gold_pot(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canShootEggs(state, itemName.BEGG) and self.canShootEggs(state, itemName.FEGGS) and self.canShootEggs(state, itemName.GEGGS) and self.canShootEggs(state, itemName.IEGGS)\
                     and state.has(itemName.BDRILL, self.player) and self.check_mumbo_magic(state, itemName.MUMBOCC)
        elif self.world.options.logic_type == 1: # normal
            logic = self.canShootEggs(state, itemName.BEGG) and self.canShootEggs(state, itemName.FEGGS) and self.canShootEggs(state, itemName.GEGGS) and self.canShootEggs(state, itemName.IEGGS)\
                     and state.has(itemName.BDRILL, self.player) and self.check_mumbo_magic(state, itemName.MUMBOCC)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canShootEggs(state, itemName.BEGG) and self.canShootEggs(state, itemName.FEGGS) and self.canShootEggs(state, itemName.GEGGS) and self.canShootEggs(state, itemName.IEGGS)\
                        and ((state.has(itemName.BDRILL) and self.check_mumbo_magic(state, itemName.MUMBOCC)) or state.has(itemName.SPLITUP, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canShootEggs(state, itemName.BEGG) and self.canShootEggs(state, itemName.FEGGS) and self.canShootEggs(state, itemName.GEGGS) and self.canShootEggs(state, itemName.IEGGS)\
                        and ((state.has(itemName.BDRILL) and self.check_mumbo_magic(state, itemName.MUMBOCC)) or state.has(itemName.SPLITUP, self.player))
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
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def jiggy_trash(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.WWHACK)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.SPLITUP, self.player)
        return logic
    
    def jiggy_sstash(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canShootEggs(state, itemName.CEGGS) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.canShootEggs(state, itemName.CEGGS)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canShootEggs(state, itemName.CEGGS)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canShootEggs(state, itemName.CEGGS)
        return logic


    def honeycomb_mt_entrance(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == 1: # normal
            logic = (self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT)) or \
                    self.canShootEggs(state, itemName.CEGGS)
        elif self.world.options.logic_type == 2: # advanced
            logic = (self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT)) or \
                    self.canShootEggs(state, itemName.CEGGS)
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT)) or \
                    self.canShootEggs(state, itemName.CEGGS)
        return logic
    
    def honeycomb_bovina(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def honeycomb_tchamber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.MT_flight_pad(state) or state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.MT_flight_pad(state) or state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.MT_flight_pad(state) or state.has(itemName.EGGAIM, self.player)
        return logic
    

    def honeycomb_prospector(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (self.hasBKMove(state, itemName.FFLIP) or self.GGMSlope(state) or self.canReachSlightlyElevatedLedge(state)) and state.has(itemName.BDRILL, self.player)\
                     or self.humbaGGM(state)
        elif self.world.options.logic_type == 1: # normal
            logic = (self.hasBKMove(state, itemName.FFLIP) or self.GGMSlope(state) or self.canReachSlightlyElevatedLedge(state)) and state.has(itemName.BDRILL, self.player)\
                     or self.humbaGGM(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = (self.hasBKMove(state, itemName.FFLIP) or self.GGMSlope(state) or self.canReachSlightlyElevatedLedge(state)) and state.has(itemName.BDRILL, self.player)\
                     or self.humbaGGM(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.hasBKMove(state, itemName.FFLIP) or self.GGMSlope(state) or self.canReachSlightlyElevatedLedge(state)) and state.has(itemName.BDRILL, self.player)\
                     or self.humbaGGM(state)
        return logic
    
    def honeycomb_gm_station(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hasGroundAttack(state) or self.humbaGGM(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.hasGroundAttack(state) or self.humbaGGM(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.hasGroundAttack(state) or self.humbaGGM(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasGroundAttack(state) or self.humbaGGM(state)
        return logic
    
    def honeycomb_spacezone(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def honeycomb_crazycastle(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.has_explosives(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.has_explosives(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.has_explosives(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.has_explosives(state)
        return logic
    
    def honeycomb_inferno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.glitchedInfernoAccess(state)
        return logic
    
    def honeycomb_seemee(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic

    def honeycomb_jrlpipes(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (self.has_explosives(state) or  state.has(itemName.BDRILL, self.player)) and \
                    state.has(itemName.GGRAB, self.player) 
        elif self.world.options.logic_type == 1: # normal
            logic = ((self.has_explosives(state) or state.has(itemName.BDRILL, self.player))\
                    and state.has(itemName.GGRAB, self.player))\
                    or ((self.has_explosives(state))\
                    and (self.check_solo_moves(state, itemName.GLIDE) or (self.check_solo_moves(state, itemName.LSPRING) and \
                    self.check_solo_moves(state, itemName.WWHACK))))
        elif self.world.options.logic_type == 2: # advanced
            logic = ((self.has_explosives(state) or state.has(itemName.BDRILL, self.player))\
                    and state.has(itemName.GGRAB, self.player))\
                    or ((self.has_explosives(state))\
                    and (self.check_solo_moves(state, itemName.GLIDE) or (self.check_solo_moves(state, itemName.LSPRING) and \
                    self.check_solo_moves(state, itemName.WWHACK)))) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = ((self.has_explosives(state) or state.has(itemName.BDRILL, self.player))\
                    and state.has(itemName.GGRAB, self.player))\
                    or ((self.has_explosives(state))\
                    and (self.check_solo_moves(state, itemName.GLIDE) or (self.check_solo_moves(state, itemName.LSPRING) and \
                    self.check_solo_moves(state, itemName.WWHACK)))) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def honeycomb_styracosaurus(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BDRILL, self.player) and state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BDRILL, self.player) and state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.BDRILL, self.player) and state.has(itemName.SPLITUP, self.player)) or \
                    (self.check_solo_moves(state, itemName.LSPRING) and self.check_solo_moves(state, itemName.WWHACK) and self.check_solo_moves(state, itemName.GLIDE))\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.BDRILL, self.player) and state.has(itemName.SPLITUP, self.player)) or \
                    (self.check_solo_moves(state, itemName.LSPRING) and self.check_solo_moves(state, itemName.WWHACK) and self.check_solo_moves(state, itemName.GLIDE))\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def honeycomb_floor3(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic =  (state.has(itemName.GGRAB, self.player) or state.has(itemName.SPLITUP, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def honeycomb_gistation(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or \
                    state.has(itemName.SPLITUP, self.player)
        return logic
    
    def honeycomb_hfpstation(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.LSPRING) or \
                    self.check_solo_moves(state, itemName.GLIDE)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.LSPRING) or \
                    self.check_solo_moves(state, itemName.GLIDE) or (state.has(itemName.SPLITUP, self.player) and \
                     state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player))\
                     or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.LSPRING) or \
                    self.check_solo_moves(state, itemName.GLIDE) or (state.has(itemName.SPLITUP, self.player) and \
                     state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player))\
                     or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def honeycomb_lavaside(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def plateauTop(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hasBKMove(state, itemName.TTROT) or state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.hasBKMove(state, itemName.TTROT) or state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.hasBKMove(state, itemName.TTROT) or state.has(itemName.SPLITUP, self.player)\
                  or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasBKMove(state, itemName.TTROT) or state.has(itemName.SPLITUP, self.player)\
                  or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def cheato_snakehead(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.EGGAIM,  self.player) and\
                  ((state.has(itemName.GGRAB, self.player) and self.BKSpringPad(state) and self.hasBKMove(state, itemName.FFLIP)) or self.MT_flight_pad(state))
        elif self.world.options.logic_type == 1: # normal
            logic = ((state.has(itemName.GGRAB, self.player) and self.BKSpringPad(state) and self.hasBKMove(state, itemName.FFLIP) and self.canShootLinearEgg(state) and state.has(itemName.EGGAIM, self.player))\
                    or (self.MT_flight_pad(state)))
        elif self.world.options.logic_type == 2: # advanced
            logic = ((state.has(itemName.GGRAB, self.player) and self.BKSpringPad(state) and self.hasBKMove(state, itemName.FFLIP) and self.canShootLinearEgg(state) and state.has(itemName.EGGAIM, self.player))\
                    or (self.MT_flight_pad(state)))
        elif self.world.options.logic_type == 3: # glitched
            logic = ((state.has(itemName.GGRAB, self.player) and self.BKSpringPad(state) and self.hasBKMove(state, itemName.FFLIP) and self.canShootLinearEgg(state) and state.has(itemName.EGGAIM, self.player))\
                    or (self.MT_flight_pad(state)))
        return logic
    
    def cheato_prison(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.prison_compound_open(state) and self.canReachSlightlyElevatedLedge(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.prison_compound_open(state) and self.canReachSlightlyElevatedLedge(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.prison_compound_open(state) and (self.canReachSlightlyElevatedLedge(state)\
                    or (state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player)))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.prison_compound_open(state) and (self.canReachSlightlyElevatedLedge(state)\
                    or (state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player)))
        return logic
    
    def cheato_snakegrove(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT) and state.has(itemName.GGRAB, self.player)\
                  and self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT) and state.has(itemName.GGRAB, self.player)\
                  and self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT) and\
                   ((self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FFLIP) and state.has(itemName.GGRAB, self.player)) or\
                       (state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player)))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.glitchedJSGAccess(state) and\
                   ((self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FFLIP) and state.has(itemName.GGRAB, self.player)) or\
                       (state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player)))
        return logic

    def cheato_gm_entrance(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPRINGB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPRINGB, self.player) or \
                    (self.hasBKMove(state, itemName.CLIMB) and (self.hasBKMove(state, itemName.FLUTTER) and self.hasBKMove(state, itemName.ARAT)))\
                    or (self.GM_boulders(state) and self.check_solo_moves(state, itemName.LSPRING))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPRINGB, self.player) or \
                    (self.hasBKMove(state, itemName.CLIMB) and (self.hasBKMove(state, itemName.FLUTTER) and self.hasBKMove(state, itemName.ARAT)))\
                    or (state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player))\
                    or (self.GM_boulders(state) and self.check_solo_moves(state, itemName.LSPRING))
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.SPRINGB, self.player) or \
                    (self.hasBKMove(state, itemName.CLIMB) and (self.hasBKMove(state, itemName.FLUTTER) and self.hasBKMove(state, itemName.ARAT)))\
                    or (state.has(itemName.EGGAIM, self.player) and state.has(itemName.CEGGS, self.player))\
                    or (self.GM_boulders(state) and self.check_solo_moves(state, itemName.LSPRING))
        return logic
    
    def cheato_waterstorage(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)\
                    and self.hasBKMove(state, itemName.DIVE) and self.hasBKMove(state, itemName.CLIMB)
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST))\
                    and self.hasBKMove(state, itemName.FFLIP) and self.hasBKMove(state, itemName.DIVE) and self.hasBKMove(state, itemName.CLIMB)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST))\
                    and self.hasBKMove(state, itemName.FFLIP) and self.hasBKMove(state, itemName.DIVE) and self.hasBKMove(state, itemName.CLIMB)
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST))\
                    and self.hasBKMove(state, itemName.FFLIP) and self.hasBKMove(state, itemName.DIVE) and self.hasBKMove(state, itemName.CLIMB)
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
                    (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)))\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.GGRAB, self.player) or (self.check_solo_moves(state, itemName.LSPRING) and \
                    (self.check_solo_moves(state, itemName.WWHACK) or self.check_solo_moves(state, itemName.GLIDE)))\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def cheato_inferno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.glitchedInfernoAccess(state)
        return logic
    
    def cheato_sauceperil(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.jiggy_peril(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.jiggy_peril(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.jiggy_peril(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.jiggy_peril(state)
        return logic
    
    def cheato_seemee(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.TTORP, self.player) and (state.has(itemName.MUMBOJR, self.player) or self.has_explosives(state) or \
                    state.has(itemName.CEGGS, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.jiggy_see_mee(state)
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.TTORP, self.player) and (self.check_solo_moves(state, itemName.GLIDE) or self.check_solo_moves(state, itemName.LSPRING) or
                    self.check_solo_moves(state, itemName.WWHACK) or
                    (self.check_solo_moves(state, itemName.PACKWH) and state.has(itemName.GGRAB, self.player)))
        return logic
    
    def cheato_trex(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBATD)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBATD)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBATD)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_humba_magic(state, itemName.HUMBATD) or self.canShootEggs(state, itemName.CEGGS)
        return logic
    
    def cheato_dippypool(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_access_ccl(state) and state.has(itemName.SPRINGB, self.player) and \
                                                  state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_access_ccl(state) and state.has(itemName.SPRINGB, self.player) and \
                                                  state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_access_ccl(state) and state.has(itemName.SPRINGB, self.player) and \
                                                  state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.can_access_ccl(state) and state.has(itemName.SPRINGB, self.player) and \
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
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def cheato_loggo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.has_explosives(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.canShootEggs(state, itemName.GEGGS) or (self.canShootEggs(state, itemName.CEGGS) and \
                     state.has(itemName.BDRILL, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canShootEggs(state, itemName.GEGGS) or (self.canShootEggs(state, itemName.CEGGS) and \
                     state.has(itemName.BDRILL, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canShootEggs(state, itemName.GEGGS) or (self.canShootEggs(state, itemName.CEGGS) and \
                     state.has(itemName.BDRILL, self.player))
        return logic
    
    def cheato_colosseum(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.CLAWBTS, self.player) and self.has_explosives(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.CLAWBTS, self.player) and \
                    (self.has_explosives(state) or
                    self.check_mumbo_magic(state, itemName.MUMBOHP))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.CLAWBTS, self.player) and \
                    (self.has_explosives(state) or
                    self.check_mumbo_magic(state, itemName.MUMBOHP))
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def cheato_icypillar(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player) and state.has(itemName.GEGGS, self.player) and \
                    state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player) or\
                (state.has(itemName.GEGGS, self.player) and state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.SPLITUP, self.player) or\
                (state.has(itemName.GEGGS, self.player) and state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def cheato_potgold(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.jiggy_gold_pot(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.jiggy_gold_pot(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.jiggy_gold_pot(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.jiggy_gold_pot(state)
        return logic
    
    def cheato_spiral(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.BKSpringPad(state) or self.hasBKMove(state, itemName.FPAD)
        elif self.world.options.logic_type == 1: # normal
            logic = self.BKSpringPad(state) or self.hasBKMove(state, itemName.FPAD)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.BKSpringPad(state) or self.hasBKMove(state, itemName.FPAD) or\
                (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.BKSpringPad(state) or self.hasBKMove(state, itemName.FPAD) or\
                (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def glowbo_JSG(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.glitchedJSGAccess(state)
        return logic

    def glowbo_inferno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.glitchedInfernoAccess(state)
        return logic
    
    def glowbo_wigwam(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def glowbo_cliff(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hasBKMove(state, itemName.CLIMB)
        elif self.world.options.logic_type == 1: # normal
            logic = self.hasBKMove(state, itemName.CLIMB)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.hasBKMove(state, itemName.CLIMB) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasBKMove(state, itemName.CLIMB) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic

    def mega_glowbo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.TTORP, self.player) and state.has(itemName.IKEY, self.player)\
                    and self.hasBKMove(state, itemName.DIVE) and self.hasBKMove(state, itemName.TJUMP)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.TTORP, self.player) and state.has(itemName.IKEY, self.player)\
                    and self.hasBKMove(state, itemName.DIVE) and self.hasBKMove(state, itemName.TJUMP)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.TTORP, self.player) and state.has(itemName.IKEY, self.player)\
                    and self.hasBKMove(state, itemName.DIVE) and\
                    (self.hasBKMove(state, itemName.TJUMP) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player)))
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.TTORP, self.player) and state.has(itemName.IKEY, self.player)\
                    and self.hasBKMove(state, itemName.DIVE) and\
                    (self.hasBKMove(state, itemName.TJUMP) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player)))
        return logic

    def ice_key(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic

    def pink_egg(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canShootEggs(state, itemName.GEGGS) or (state.has(itemName.AIREAIM, self.player) and state.has(itemName.GEGGS, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = self.canShootEggs(state, itemName.GEGGS) or (state.has(itemName.AIREAIM, self.player) and state.has(itemName.GEGGS, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canShootEggs(state, itemName.GEGGS) or (state.has(itemName.AIREAIM, self.player) and state.has(itemName.GEGGS, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.has_explosives(state) or (state.has(itemName.AIREAIM, self.player) and state.has(itemName.GEGGS, self.player))
        return logic
    
    def blue_egg(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def jinjo_plateau(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BDRILL, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BDRILL, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.BDRILL, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.BDRILL, self.player) or (self.canShootLinearEgg(state) and self.hasBKMove(state, itemName.EGGSHOOT) and self.hasBKMove(state, itemName.BBARGE))
        return logic
    
    def jinjo_clifftop(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.CLAWBTS, self.player) and self.hasBKMove(state, itemName.CLIMB)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.CLAWBTS, self.player) and self.hasBKMove(state, itemName.CLIMB)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.CLAWBTS, self.player) and self.hasBKMove(state, itemName.CLIMB)) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.CLAWBTS, self.player) and self.hasBKMove(state, itemName.CLIMB)) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic

    def jinjo_wasteland(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 2: # advanced
            logic = ((state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP))\
                        or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = ((state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP))\
                        or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def jinjo_jadesnakegrove(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.check_mumbo_magic(state,itemName.MUMBOMT) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state,itemName.MUMBOMT) and self.hasBKMove(state, itemName.FFLIP) and\
                    (self.hasBKMove(state, itemName.BBUST) or state.has(itemName.GGRAB, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state,itemName.MUMBOMT) and (
                    (self.hasBKMove(state, itemName.FFLIP) and self.hasBKMove(state, itemName.BBUST) or state.has(itemName.GGRAB, self.player)) or\
                    (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player)))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.glitchedJSGAccess(state) and (
                    (self.hasBKMove(state, itemName.FFLIP) and self.hasBKMove(state, itemName.BBUST) or state.has(itemName.GGRAB, self.player)) or\
                    (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player)))
        return logic
    
    def jinjo_stadium(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.MT_flight_pad(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.MT_flight_pad(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.MT_flight_pad(state) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.MT_flight_pad(state) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def jinjo_pool(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hasBKMove(state, itemName.DIVE)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def jinjo_caveofhorror(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.canShootEggs(state, itemName.GEGGS)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canShootEggs(state, itemName.GEGGS)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canShootEggs(state, itemName.GEGGS)
        return logic
    
    def jinjo_cactus(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def jinjo_vandoor(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.has_explosives(state) and \
                    self.check_humba_magic(state, itemName.HUMBAWW) and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.has_explosives(state) and \
                    self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.has_explosives(state) and \
                    self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.canShootEggs(state, itemName.GEGGS) and self.check_humba_magic(state, itemName.HUMBAWW)) or self.canShootEggs(state, itemName.CEGGS)
        return logic
    
    def jinjo_alcove(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.DOUBLOON, self.player, 28)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.DOUBLOON, self.player, 28) or (self.has_explosives(state) and (self.check_solo_moves(state, itemName.PACKWH) or \
                    self.check_solo_moves(state, itemName.SAPACK) or (self.check_solo_moves(state, itemName.LSPRING) and \
                    self.check_solo_moves(state, itemName.GLIDE))))
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_humba_magic(state, itemName.HUMBAJR) or state.has(itemName.AUQAIM, self.player) or \
                    state.has(itemName.TTORP, self.player)
        return logic
    
    def jinjo_tdlentrance(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_beat_terry(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_beat_terry(state) or self.canShootEggs(state, itemName.GEGGS)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_beat_terry(state) or self.canShootEggs(state, itemName.GEGGS)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.can_beat_terry(state) or self.canShootEggs(state, itemName.GEGGS)
        return logic

    def jinjo_big_t_rex(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.mumboTDL(state) and self.check_humba_magic(state, itemName.HUMBATD)
        elif self.world.options.logic_type == 1: # normal
            logic = self.mumboTDL(state) and self.check_humba_magic(state, itemName.HUMBATD)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.mumboTDL(state) and self.check_humba_magic(state, itemName.HUMBATD)
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.mumboTDL(state) and self.check_humba_magic(state, itemName.HUMBATD)) or \
                    self.canShootEggs(state, itemName.CEGGS)
        return logic
    
    def jinjo_stomping_plains(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.jiggy_stomping_plains(state) and state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.jiggy_stomping_plains(state) and state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.jiggy_stomping_plains(state) and state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def jinjo_legspring(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.LSPRING)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_solo_moves(state, itemName.LSPRING)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_solo_moves(state, itemName.LSPRING) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_solo_moves(state, itemName.LSPRING) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic

    def jinjo_floor4(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def jinjo_wasteplant(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canShootEggs(state, itemName.IEGGS) and state.has(itemName.AUQAIM, self.player) and \
                    state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canShootEggs(state, itemName.IEGGS) and state.has(itemName.AUQAIM, self.player) and \
                    state.has(itemName.TTORP, self.player)
        return logic
    
    def jinjo_hot_pool(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_solo_moves(state, itemName.SHPACK)
        return logic
    
    def jinjo_windtunnel(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_humba_magic(state, itemName.HUMBAHP)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAHP)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAHP) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_humba_magic(state, itemName.HUMBAHP) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
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
                    self.check_solo_moves(state, itemName.WWHACK)) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_solo_moves(state, itemName.GLIDE) or (self.check_solo_moves(state, itemName.LSPRING) and 
                    self.check_solo_moves(state, itemName.WWHACK)) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def jinjo_mildred(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canShootEggs(state, itemName.FEGGS) or self.has_explosives(state) or \
                    state.has(itemName.BDRILL, self.player) 
        elif self.world.options.logic_type == 1: # normal
            logic = self.canShootEggs(state, itemName.FEGGS) or self.has_explosives(state) or state.has(itemName.BDRILL, self.player) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canShootEggs(state, itemName.FEGGS) or self.has_explosives(state) or state.has(itemName.BDRILL, self.player) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canShootEggs(state, itemName.FEGGS) or self.has_explosives(state) or state.has(itemName.BDRILL, self.player) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)
        return logic
    
    def jinjo_trashcan(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic =  self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 1: # normal
            logic =  self.check_solo_moves(state, itemName.SHPACK) or self.check_solo_moves(state, itemName.LSPRING)
        elif self.world.options.logic_type == 2: # advanced
            logic =  self.check_solo_moves(state, itemName.SHPACK) or self.check_solo_moves(state, itemName.LSPRING) or self.check_solo_moves(state, itemName.GLIDE)\
                    or (state.has(itemName.SPLITUP, self.player) and state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic =  self.check_solo_moves(state, itemName.SHPACK) or self.check_solo_moves(state, itemName.LSPRING) or self.check_solo_moves(state, itemName.GLIDE)\
                    or (state.has(itemName.SPLITUP, self.player) and state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
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
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def jinjo_central(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player) or (state.has(itemName.SPRINGB, self.player) and state.has(itemName.BDRILL, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.SPLITUP, self.player)\
                  or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))\
                  or (state.has(itemName.SPRINGB, self.player) and state.has(itemName.BDRILL, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.SPLITUP, self.player)\
                  or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))\
                  or (state.has(itemName.SPRINGB, self.player) and state.has(itemName.BDRILL, self.player))
        return logic


    def treble_jv(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 2: # advanced
            logic = ((state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP))\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = ((state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP))\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def treble_gm(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hasBKMove(state,itemName.DIVE)
        elif self.world.options.logic_type == 1: # normal
            logic = self.hasBKMove(state,itemName.DIVE)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.hasBKMove(state,itemName.DIVE)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasBKMove(state,itemName.DIVE) or (self.GM_boulders(state) and self.check_solo_moves(state, itemName.LSPRING))
        return logic
    
    def treble_ww(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_humba_magic(state, itemName.HUMBAWW)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_humba_magic(state, itemName.HUMBAWW) or self.canShootEggs(state, itemName.CEGGS)
        return logic
    
    def treble_jrl(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.AUQAIM, self.player) or state.has(itemName.TTORP, self.player) or self.check_humba_magic(state, itemName.HUMBAJR)
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def treble_gi(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic

    def treble_hfp(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or state.has(itemName.SPLITUP, self.player)\
                  or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.GEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or state.has(itemName.SPLITUP, self.player)\
                  or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
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
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def doubloon_ledge(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.SPLITUP, self.player) and self.has_explosives(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.SPLITUP, self.player) and self.has_explosives(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.SPLITUP, self.player) and self.has_explosives(state)) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.SPLITUP, self.player) and self.has_explosives(state)) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def doubloon_dirtpatch(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.BDRILL, self.player) or self.has_explosives(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.BDRILL, self.player) or self.has_explosives(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.BDRILL, self.player) or self.has_explosives(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.BDRILL, self.player) or self.has_explosives(state)
        return logic

    def notes_plateau_sign(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 2: # advanced
            logic = ((state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP))\
                        or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = ((state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP))\
                        or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def notes_ww_area51(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.has_explosives(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.has_explosives(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.has_explosives(state) or \
                    state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.has_explosives(state) or \
                    state.has(itemName.SPLITUP, self.player)
        return logic
    
    def notes_bottom_clockwork(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canDoSmallElevation(state)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def notes_top_clockwork(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hasBKMove(state, itemName.FFLIP) or \
                    (self.hasBKMove(state, itemName.TJUMP) or (self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FLUTTER)))\
                        and state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.hasBKMove(state, itemName.FFLIP) or \
                    (self.hasBKMove(state, itemName.TJUMP) or (self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FLUTTER)))\
                        and (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST))
        elif self.world.options.logic_type == 2: # advanced
            logic = (self.hasBKMove(state, itemName.FFLIP) or \
                    (self.hasBKMove(state, itemName.TJUMP) or (self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FLUTTER)))\
                        and (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)))\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.hasBKMove(state, itemName.FFLIP) or \
                        (self.hasBKMove(state, itemName.TJUMP) or (self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FLUTTER)))\
                        and (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)))\
                        or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def notes_green_pile(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.GGMSlope(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.GGMSlope(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.GGMSlope(state) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.GGMSlope(state) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    # TODO: make something that is proper to every note
    def placeholder_prospector_note(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.GGMSlope(state) or self.hasBKMove(itemName.FFLIP)
        elif self.world.options.logic_type == 1: # normal
            logic = self.GGMSlope(state) or self.hasBKMove(itemName.FFLIP)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.GGMSlope(state) or self.hasBKMove(itemName.FFLIP) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.GGMSlope(state) or self.hasBKMove(itemName.FFLIP) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def notes_gm_mumbo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canDoSmallElevation(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.canDoSmallElevation(state) or state.has(itemName.GGRAB, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canDoSmallElevation(state) or state.has(itemName.GGRAB, self.player) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canDoSmallElevation(state) or state.has(itemName.GGRAB, self.player) or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic

    def placeholder_fuel_depot(self, state: CollectionState) -> bool:
        return self.canDoSmallElevation(state)

    
    def notes_jrl_blubs(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOJR) and (state.has(itemName.AUQAIM, self.player) or 
                    state.has(itemName.TTORP, self.player))
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.AUQAIM, self.player) or state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.AUQAIM, self.player) or state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
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
                    self.check_solo_moves(state, itemName.PACKWH) or self.check_solo_moves(state, itemName.LSPRING)\
                    or self.check_solo_moves(state, itemName.LSPRING)\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.can_access_gi_fl1_2fl2(state) or state.has(itemName.GGRAB, self.player) or \
                    self.check_solo_moves(state, itemName.PACKWH) or self.check_solo_moves(state, itemName.LSPRING)\
                    or self.check_solo_moves(state, itemName.LSPRING)\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def notes_ccl_silo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_solo_moves(state, itemName.SHPACK) or self.canShootEggs(state, itemName.CEGGS)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_solo_moves(state, itemName.SHPACK) or self.canShootEggs(state, itemName.CEGGS)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_solo_moves(state, itemName.SHPACK) or self.canShootEggs(state, itemName.CEGGS)
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
        
    def silo_bill_drill(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_notes(state, 85) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_notes(state, 85) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_notes(state, 85) and (self.hasBKMove(state, itemName.FFLIP) or self.hasBKMove(state, itemName.TTRAIN))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.check_notes(state, 85) and (self.hasBKMove(state, itemName.FFLIP) or self.hasBKMove(state, itemName.TTRAIN))
        return logic
    
    def can_access_taxi_pack_silo(self, state:CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GGRAB, self.player) or self.check_solo_moves(state, itemName.SAPACK))
        elif self.world.options.logic_type == 1: # normal
            return state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GGRAB, self.player) or
                                                self.check_solo_moves(state, itemName.PACKWH) or self.check_solo_moves(state, itemName.SAPACK))
        elif self.world.options.logic_type == 2: # advanced
            return state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GGRAB, self.player) or
                                                self.check_solo_moves(state, itemName.PACKWH) or self.check_solo_moves(state, itemName.SAPACK))
        elif self.world.options.logic_type == 3: # glitched
            return state.has(itemName.SPLITUP, self.player) and (state.has(itemName.GGRAB, self.player) or
                                                self.check_solo_moves(state, itemName.PACKWH) or self.check_solo_moves(state, itemName.SAPACK))

    def has_fire(self, state: CollectionState) -> bool:
        return self.canShootEggs(state, itemName.FEGGS) or self.dragon_kazooie(state)
    
    def dragon_kazooie(self, state: CollectionState) -> bool:
        return self.check_humba_magic(state, itemName.HUMBAIH) and self.can_access_pinegrove(state, False) and self.hasBKMove(state, itemName.GRAT)
    
    def has_explosives(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return self.canShootEggs(state, itemName.GEGGS)
        elif self.world.options.logic_type == 1: # normal
            return self.canShootEggs(state, itemName.GEGGS) or self.canShootEggs(state, itemName.CEGGS)
        elif self.world.options.logic_type == 2: # advanced
            return self.canShootEggs(state, itemName.GEGGS) or self.canShootEggs(state, itemName.CEGGS)
        elif self.world.options.logic_type == 3: # glitched
            return self.canShootEggs(state, itemName.GEGGS) or self.canShootEggs(state, itemName.CEGGS)

    def long_swim(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return self.check_mumbo_magic(state, itemName.MUMBOJR) and self.hasBKMove(state, itemName.DIVE)
        elif self.world.options.logic_type == 1: # normal
            return (state.has(itemName.BDRILL, self.player) or self.check_mumbo_magic(state, itemName.MUMBOJR)) and self.hasBKMove(state, itemName.DIVE)
        elif self.world.options.logic_type == 2: # advanced
            return self.hasBKMove(state, itemName.DIVE)
        elif self.world.options.logic_type == 3: # glitched
            return self.hasBKMove(state, itemName.DIVE)

    def can_reach_atlantis(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return state.has(itemName.IEGGS, self.player) and self.long_swim(state) and state.has(itemName.AUQAIM, self.player)
        elif self.world.options.logic_type == 1: # normal
            return state.has(itemName.IEGGS, self.player) and self.long_swim(state) and state.has(itemName.AUQAIM, self.player)
        elif self.world.options.logic_type == 2: # advanced
            return self.long_swim(state)
        elif self.world.options.logic_type == 3: # glitched
            return self.long_swim(state)

    def MT_flight_pad(self, state: CollectionState) -> bool:
        return self.hasBKMove(state, itemName.FPAD) and\
                (self.check_mumbo_magic(state, itemName.MUMBOMT)\
                    or (state.has(itemName.BDRILL, self.player) and (self.canDoSmallElevation(state) or self.hasBKMove(state, itemName.FLUTTER))))

    def prison_compound_open(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return self.can_access_mt(state) and \
                (state.has(itemName.GEGGS, self.player) or self.check_mumbo_magic(state, itemName.MUMBOMT))
        
        elif self.world.options.logic_type == 1: # normal
            return self.can_access_mt(state) and \
                (self.has_explosives(state) or \
                 self.check_mumbo_magic(state, itemName.MUMBOMT)) and \
                 (self.mt_jiggy(state) or (self.can_access_hailfire(state, True) and self.HFP_to_MT(state)))
        
        elif self.world.options.logic_type == 2: # advanced
            return self.can_access_mt(state) and \
                (self.has_explosives(state) or \
                 self.check_mumbo_magic(state, itemName.MUMBOMT)) and \
                 (self.mt_jiggy(state) or (self.can_access_hailfire(state, True) and self.HFP_to_MT(state)))
        elif self.world.options.logic_type == 3: # glitched
            return self.can_access_mt(state) and \
                (self.has_explosives(state) or \
                 self.check_mumbo_magic(state, itemName.MUMBOMT)) and \
                 (self.mt_jiggy(state) or (self.can_access_hailfire(state, True) and self.HFP_to_MT(state)))
        
    def dilberta_free(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return self.prison_compound_open(state) and state.has(itemName.BDRILL, self.player) and \
                    self.check_humba_magic(state, itemName.HUMBAMT) and self.check_mumbo_magic(state, itemName.MUMBOMT)
        
        elif self.world.options.logic_type == 1: # normal
            return self.prison_compound_open(state) and state.has(itemName.BDRILL, self.player)
        
        elif self.world.options.logic_type == 2: # advanced
            return self.prison_compound_open(state) and state.has(itemName.BDRILL, self.player)

        elif self.world.options.logic_type == 3: # glitched
            return self.prison_compound_open(state) and state.has(itemName.BDRILL, self.player)

    def GM_boulders(self, state: CollectionState) -> bool:
        return (state.has(itemName.BDRILL, self.player) and self.canDoSmallElevation(state)) or self.humbaGGM(state)

    def canary_mary_free(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return self.humbaGGM(state)
 
        elif self.world.options.logic_type == 1: # normal
            return self.humbaGGM(state) or self.canShootEggs(state, itemName.CEGGS)
        
        elif self.world.options.logic_type == 2: # advanced
            return self.humbaGGM(state) or self.canShootEggs(state, itemName.CEGGS)

        elif self.world.options.logic_type == 3: # glitched
            return self.humbaGGM(state) or self.canShootEggs(state, itemName.CEGGS)

    # TODO: make logic for entering the train that makes sense, based on the world.
    def can_beat_king_coal(self, state) -> bool:
        if self.world.options.randomize_chuffy == False:
            return self.mumboGGM(state) and self.can_access_GM(state) and self.canDoSmallElevation(state) and self.hasBKMove(state, itemName.CLIMB)
        else:
            return state.has(itemName.CHUFFY, self.player) and self.canDoSmallElevation(state) and self.hasBKMove(state, itemName.CLIMB)


    #deprecated but might be useful for ticket randomization
    def can_kill_fruity(self, state: CollectionState) -> bool:
        return self.canShootEggs(state, itemName.CEGGS) or \
               self.check_humba_magic(state, itemName.HUMBAWW)

    def saucer_door_open(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == 0: # beginner
            return state.has(itemName.GGRAB, self.player) and self.canShootEggs(state, itemName.GEGGS)
        elif self.world.options.logic_type == 1: # normal
            return state.has(itemName.GGRAB, self.player) or (state.has(itemName.EGGAIM, self.player) and \
                   state.has(itemName.GEGGS, self.player)) or \
            (self.has_explosives(state) and \
             (self.check_solo_moves(state, itemName.LSPRING) and self.check_solo_moves(state, itemName.GLIDE)))
        elif self.world.options.logic_type == 2: # advanced
            return state.has(itemName.GGRAB, self.player) or (state.has(itemName.EGGAIM, self.player) and \
                   (state.has(itemName.GEGGS, self.player) or state.has(itemName.GEGGS, self.player))) or \
            (self.has_explosives(state)  and \
             (self.check_solo_moves(state, itemName.LSPRING) and self.check_solo_moves(state, itemName.GLIDE)))
        elif self.world.options.logic_type == 3: # glitched
            return state.has(itemName.GGRAB, self.player) or (state.has(itemName.EGGAIM, self.player) and \
                   (state.has(itemName.GEGGS, self.player) or state.has(itemName.GEGGS, self.player))) or \
            (self.has_explosives(state)  and \
             (self.check_solo_moves(state, itemName.LSPRING) and self.check_solo_moves(state, itemName.GLIDE))) or\
             (self.can_access_GM(state) and self.canShootEggs(itemName.CEGGS)) # You can shoot a clockwork through the door from GGM.

    def can_beat_terry(self, state: CollectionState) -> bool:
        # I assume nobody wants to do this fight with clockwork eggs.
        if self.world.options.logic_type == 0: # beginner
            return state.has(itemName.EGGAIM, self.player) and self.canShootLinearEgg(state) and state.has(itemName.SPRINGB, self.player)
        elif self.world.options.logic_type == 1: # normal
            return state.has(itemName.EGGAIM, self.player)  and self.canShootLinearEgg(state) and state.has(itemName.SPRINGB, self.player)
        elif self.world.options.logic_type == 2: # advanced
            return state.has(itemName.SPRINGB, self.player) and self.canShootLinearEgg(state) and\
                (self.hasBKMove(state, itemName.FFLIP) or self.hasBKMove(state, itemName.EGGAIM))
        elif self.world.options.logic_type == 3: # glitched
            return self.canShootEggs(state) and \
                    (self.hasBKMove(state, itemName.FFLIP) or self.hasBKMove(state, itemName.EGGAIM)) and\
                    (state.has(itemName.SPRINGB, self.player) or \
                    (self.hasBKMove(state, itemName.FPAD) and (self.hasBKMove(state, itemName.BBOMB) or\
                    self.hasBKMove(state, itemName.EGGAIM) and self.hasBKMove(state, itemName.EGGSHOOT) and self.hasBKMove(state, itemName.GEGGS) and self.hasBKMove(state, itemName.CEGGS))))
        
    def smuggle_food(self, state: CollectionState) -> bool:
        return state.has(itemName.CLAWBTS, self.player)

    def oogle_boogles_open(self, state) -> bool:
        return self.check_humba_magic(state, itemName.HUMBATD) and self.mumboTDL(state)

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
               self.check_humba_magic(state, itemName.HUMBAGI) and self.canShootEggs(state, itemName.GEGGS) and \
               state.has(itemName.BDRILL, self.player)
    
    def jiggy_underwater_waste_disposal(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_beat_weldar(state) and self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_beat_weldar(state) and self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_beat_weldar(state) and self.check_solo_moves(state, itemName.SHPACK)
        elif self.world.options.logic_type == 3: # glitched
            # Getting the jiggy from waste disposal through the wall.
            logic = self.can_use_battery(state) and (state.has(itemName.TTORP, self.player) or self.check_solo_moves(state, itemName.SHPACK))
        return logic
    
    def jiggy_clinkers(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.check_mumbo_magic(state, itemName.MUMBOGI) and state.has(itemName.CLAWBTS, self.player) and state.has(itemName.BBLASTER, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.check_mumbo_magic(state, itemName.MUMBOGI) and state.has(itemName.CLAWBTS, self.player) and state.has(itemName.BBLASTER, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.check_mumbo_magic(state, itemName.MUMBOGI) and state.has(itemName.CLAWBTS, self.player) and state.has(itemName.BBLASTER, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.check_mumbo_magic(state, itemName.MUMBOGI) or state.has(itemName.BBASH, self.player))\
                  and state.has(itemName.CLAWBTS, self.player) and state.has(itemName.BBLASTER, self.player)
        return logic

    def can_use_battery(self, state: CollectionState) -> bool:
        return self.check_solo_moves(state, itemName.PACKWH) and self.check_solo_moves(state, itemName.TAXPACK)
    
    def can_access_JSG(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.MUMBOMT, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.MUMBOMT, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.MUMBOMT, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.glitchedJSGAccess(state)
        return logic
        
    def glitchedJSGAccess(self, state: CollectionState) -> bool:
        return self.MT_flight_pad(state) or state.has(itemName.MUMBOMT, self.player)
    
    def glitchedInfernoAccess(self, state: CollectionState) -> bool:
        return self.check_humba_magic(state, itemName.HUMBAWW) or self.canShootEggs(itemName.CEGGS)
        
    def HFP_to_MT(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.has_explosives(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.has_explosives(state) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.has_explosives(state) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.has_explosives(state) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)
        return logic
    
    def HFP_to_JRL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_access_ccl(state) and state.has(itemName.SPLITUP, self.player)\
                     and self.hasGroundAttack(state) and self.hasBKMove(state, itemName.DIVE)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_access_ccl(state) and state.has(itemName.SPLITUP, self.player)\
                     and self.hasGroundAttack(state) and self.hasBKMove(state, itemName.DIVE)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_access_ccl(state) and state.has(itemName.SPLITUP, self.player)\
                     and self.hasGroundAttack(state) and self.hasBKMove(state, itemName.DIVE)
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.can_access_ccl(state) and state.has(itemName.SPLITUP, self.player) and self.hasGroundAttack(state) and self.hasBKMove(state, itemName.DIVE)) or state.has(itemName.GGRAB, self.player)
        return logic

    def WorldUnlocks_req(self, state: CollectionState, locationId: int) -> bool: #1
        world = ""
        for worldLoc, locationno in self.world.randomize_order.items():
            if locationno == locationId:
                world = worldLoc
                break
        amt = self.world.randomize_worlds[world]
        return state.has(itemName.JIGGY, self.player, amt)
    

    def mt_jiggy(self, state: CollectionState) -> bool: #1
        if self.world.worlds_randomized == True:
            return state.has(itemName.MTA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.MT]
            return state.has(itemName.JIGGY, self.player, amt)
    
    def WH_to_PL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canReachSlightlyElevatedLedge(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.canReachSlightlyElevatedLedge(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.canReachSlightlyElevatedLedge(state) or (self.hasBKMove(state, itemName.FFLIP) and self.hasBKMove(state, itemName.BBUST))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canReachSlightlyElevatedLedge(state) or (self.hasBKMove(state, itemName.FFLIP) and self.hasBKMove(state, itemName.BBUST))
        return logic
    
    def GGM_to_PL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.gm_jiggy(state) and self.hasBKMove(state, itemName.CLIMB)
        elif self.world.options.logic_type == 1: # normal
            logic = self.hasBKMove(state, itemName.CLIMB)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.hasBKMove(state, itemName.CLIMB)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasBKMove(state, itemName.CLIMB)
        return logic
    
    def can_access_GM(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (state.has(itemName.GGRAB, self.player) and self.gm_jiggy(state)) or \
                    self.dilberta_free(state)
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GGRAB, self.player) and self.gm_jiggy(state)) or self.dilberta_free(state) or \
                    (self.can_access_jrl and self.can_reach_atlantis and state.has(itemName.TTORP, self.player) and \
                    state.has(itemName.IEGGS, self.player) and state.has(itemName.AUQAIM, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.gm_jiggy(state) or \
                    (self.can_access_jrl and self.can_reach_atlantis and state.has(itemName.TTORP, self.player) and \
                    state.has(itemName.IEGGS, self.player) and state.has(itemName.AUQAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def gm_jiggy(self, state: CollectionState) -> bool: #4
        if self.world.worlds_randomized == True:
            return state.has(itemName.GGA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.GM]
            return state.has(itemName.JIGGY, self.player, amt)
        

    def can_access_water_storage_jinjo_from_GGM(self, state):
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = False
        elif self.world.options.logic_type == 1 : # normal
            logic = self.check_solo_moves(state, itemName.WWHACK) and self.check_solo_moves(state, itemName.LSPRING) and\
                                                 self.check_solo_moves(state, itemName.GLIDE) and self.GM_boulders(state) 
        elif self.world.options.logic_type == 2: # advanced
            logic = (self.check_solo_moves(state, itemName.WWHACK) and self.check_solo_moves(state, itemName.LSPRING) and\
                                                 self.check_solo_moves(state, itemName.GLIDE) and self.GM_boulders(state))\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.check_solo_moves(state, itemName.WWHACK) and self.check_solo_moves(state, itemName.LSPRING) and\
                                                 self.check_solo_moves(state, itemName.GLIDE) and self.GM_boulders(state))\
                    or (state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player))
        return logic
    
    def can_access_water_storage_jinjo_from_JRL(self, state):
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_reach_atlantis(state) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_reach_atlantis(state) and state.has(itemName.IEGGS, self.player) and state.has(itemName.AUQAIM, self.player) and state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.can_reach_atlantis(state) and state.has(itemName.IEGGS, self.player) and state.has(itemName.AUQAIM, self.player) and state.has(itemName.TTORP, self.player)
        return logic
      
    def PL_to_PG(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.FEGGS, self.player) and state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1 : # normal
            logic = (state.has(itemName.FEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or (self.hasBKMove(state, itemName.TTROT) and self.canShootEggs(state, itemName.FEGGS))
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.FEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or (self.hasBKMove(state, itemName.TTROT) and self.canShootEggs(state, itemName.FEGGS))
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.FEGGS, self.player) and state.has(itemName.EGGAIM, self.player)) or (self.hasBKMove(state, itemName.TTROT) and self.canShootEggs(state, itemName.FEGGS))
        return logic

    def PL_to_GGM(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.gm_jiggy(state)
        elif self.world.options.logic_type == 1 : # normal
            logic = self.gm_jiggy(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.gm_jiggy(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.gm_jiggy(state) or (self.hasBKMove(state, itemName.BBUST) and (self.hasBKMove(state, itemName.FFLIP) or self.hasBKMove(state, itemName.TJUMP)))
        return logic
    
    def hatch_to_TDL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = False
        elif self.world.options.logic_type == 1 : # normal
            logic = False
        elif self.world.options.logic_type == 2: # advanced
            logic = False
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player)
        return logic
    
    def can_access_witchyworld(self, state: CollectionState, fromTrain: bool) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (self.ww_jiggy(state) and self.can_access_pinegrove(state, False))
        elif self.world.options.logic_type == 1: # normal
            if fromTrain:
                logic = self.ww_jiggy(state) and self.can_access_pinegrove(state, fromTrain) or \
                        (self.can_access_tdl(state, True) and state.has(itemName.MUMBOTD, self.player) and \
                        state.has(itemName.HUMBATD, self.player))
            else:
                logic = self.ww_jiggy(state) and self.can_access_pinegrove(state, fromTrain) or \
                        self.has_train_access(state, "WW") or (self.can_access_tdl(state, True) and \
                        state.has(itemName.MUMBOTD, self.player) and state.has(itemName.HUMBATD, self.player))
        elif self.world.options.logic_type == 2: # advanced
            if fromTrain:
                logic = self.ww_jiggy(state) and self.can_access_pinegrove(state, fromTrain) or \
                        (self.can_access_tdl(state, True) and state.has(itemName.MUMBOTD, self.player) and \
                        state.has(itemName.HUMBATD, self.player))
            else:
                logic = self.ww_jiggy(state) and self.can_access_pinegrove(state, fromTrain) or \
                        self.has_train_access(state, "WW") or (self.can_access_tdl(state, True) and \
                        state.has(itemName.MUMBOTD, self.player) and state.has(itemName.HUMBATD, self.player))
        elif self.world.options.logic_type == 3: # glitched
            # TODO: doesn't take into account the skip, but I'm not sure where this is used.
            if fromTrain:
                logic = self.ww_jiggy(state) and self.can_access_pinegrove(state, fromTrain) or \
                        (self.can_access_tdl(state, True) and state.has(itemName.MUMBOTD, self.player) and \
                        state.has(itemName.HUMBATD, self.player))
            else:
                logic = self.ww_jiggy(state) and self.can_access_pinegrove(state, fromTrain) or \
                        self.has_train_access(state, "WW") or (self.can_access_tdl(state, True) and \
                        state.has(itemName.MUMBOTD, self.player) and state.has(itemName.HUMBATD, self.player))
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
        elif self.world.options.logic_type == 3: # glitched
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
            logic = (self.can_access_clifftop(state, False) and self.jrl_jiggy(state)) or \
                (self.can_access_hailfire(state, False) and self.can_access_ccl(state) and state.has(itemName.SPLITUP, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_access_clifftop(state, False) and self.jrl_jiggy(state) or \
                (self.can_access_hailfire(state, False) and self.can_access_ccl(state) and state.has(itemName.SPLITUP, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.can_access_clifftop(state, False) and self.jrl_jiggy(state) or \
                (self.can_access_hailfire(state, False) and self.can_access_ccl(state) and state.has(itemName.SPLITUP, self.player))
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
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
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
        elif self.world.options.logic_type == 3: # glitched
            logic = self.gi_jiggy(state) and self.can_access_quagmire(state, fromTrain)
        return logic
    
    def gi_jiggy(self, state: CollectionState) -> bool: #28
        if self.world.worlds_randomized == True:
            return state.has(itemName.GIA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.GIO]
            return state.has(itemName.JIGGY, self.player, amt)
        
    def ck_jiggy(self, state: CollectionState) -> bool: #55
        if self.world.worlds_randomized == True:
            return state.has(itemName.CKA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.CK]
            return state.has(itemName.JIGGY, self.player, amt)
    
    def quag_to_CK(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.CLAWBTS, self.player) and self.hasBKMove(state, itemName.CLIMB) and self.ck_jiggy(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.CLAWBTS, self.player) and self.hasBKMove(state, itemName.CLIMB) and self.ck_jiggy(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.CLAWBTS, self.player) and self.hasBKMove(state, itemName.CLIMB) and self.ck_jiggy(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasBKMove(state, itemName.CLIMB) and (state.has(itemName.CLAWBTS, self.player) or \
                     (state.has(itemName.GEGGS, self.player) and state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player) and self.hasBKMove(state, itemName.EGGSHOOT)))
        return logic

    def ggm_to_ww(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = False
        elif self.world.options.logic_type == 1: # normal
            logic = False
        elif self.world.options.logic_type == 2: # advanced
            logic = False
        elif self.world.options.logic_type == 3: # glitched
            logic = self.humbaGGM(state) and self.canShootEggs(state,itemName.CEGGS)
        return logic
        
    def QM_to_WL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP)
        return logic
    
    def outside_gi_to_floor1(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = False
        elif self.world.options.logic_type == 1: # normal
            logic = False
        elif self.world.options.logic_type == 2: # advanced
            logic = False
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.CEGGS, self.player) and state.has(itemName.EGGAIM, self.player)
        return logic
    
    def outside_gi_to_floor2(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = False
        elif self.world.options.logic_type == 1: # normal
            logic = False
        elif self.world.options.logic_type == 2: # advanced
            logic = False
        elif self.world.options.logic_type == 3: # glitched
            logic = self.canShootEggs(state, itemName.CEGGS)
        return logic
    
    def outside_gi_to_floor3(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = False
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.CLAWBTS, self.player) and self.hasBKMove(state, itemName.TTROT)\
                     and (self.hasBKMove(state, itemName.FLUTTER) or self.hasBKMove(state, itemName.ARAT))
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.CLAWBTS, self.player) and self.hasBKMove(state, itemName.TTROT)\
                     and (self.hasBKMove(state, itemName.FLUTTER) or self.hasBKMove(state, itemName.ARAT))
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.CLAWBTS, self.player) and self.hasBKMove(state, itemName.TTROT)\
                     and (self.hasBKMove(state, itemName.FLUTTER) or self.hasBKMove(state, itemName.ARAT))
        return logic

    def can_access_gi_outside_from_inside(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.has_train_access(state, "GI") and state.has(itemName.SPLITUP, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_leave_GI_from_inside(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_leave_GI_from_inside(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.can_leave_GI_from_inside(state)
        return logic
    
    def can_access_gi_fl1_from_outside(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.has_train_access(state, "GI") and state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.CLAWBTS, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.CLAWBTS, self.player)
        return logic
    
    def can_access_gi_fl1_2fl2(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (state.has(itemName.CLAWBTS, self.player) and (self.BKSpringPad(state) or self.check_solo_moves(state, itemName.LSPRING)))
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.CLAWBTS, self.player) and (self.BKSpringPad(state) or self.check_solo_moves(state, itemName.LSPRING))) or self.check_solo_moves(state, itemName.LSPRING) and \
                    self.check_solo_moves(state, itemName.GLIDE) and (self.check_solo_moves(state, itemName.WWHACK) or \
                    state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.CLAWBTS, self.player) and (self.BKSpringPad(state) or self.check_solo_moves(state, itemName.LSPRING))) or self.check_solo_moves(state, itemName.LSPRING) and \
                    self.check_solo_moves(state, itemName.GLIDE) and (self.check_solo_moves(state, itemName.WWHACK) or \
                    state.has(itemName.EGGAIM, self.player))
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.CLAWBTS, self.player) and (self.BKSpringPad(state) or self.check_solo_moves(state, itemName.LSPRING))) or self.check_solo_moves(state, itemName.LSPRING) and \
                    self.check_solo_moves(state, itemName.GLIDE) and (self.check_solo_moves(state, itemName.WWHACK) or \
                    state.has(itemName.EGGAIM, self.player))
        return logic
    
    def F1_to_F3(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = False
        elif self.world.options.logic_type == 1: # normal
            logic = False
        elif self.world.options.logic_type == 2: # advanced
            logic = False
        elif self.world.options.logic_type == 3: # glitched
            logic = state.has(itemName.BBASH, self.player) and self.hasBKMove(state, itemName.CLIMB)
        return logic
    
    def F2_to_F1(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 1: # normal
            logic = (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 2: # advanced
            logic = (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP)
        elif self.world.options.logic_type == 3: # glitched
            logic = (state.has(itemName.GGRAB, self.player) or self.hasBKMove(state, itemName.BBUST)) and self.hasBKMove(state, itemName.FFLIP)
        return logic
    
    #TODO check
    def can_access_gi_fl2_2fl3all(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (state.has(itemName.GGRAB, self.player) and state.has(itemName.CLAWBTS, self.player)) or self.check_humba_magic(state, itemName.HUMBAGI)
        elif self.world.options.logic_type == 1: # normal
            logic = (self.check_humba_magic(state, itemName.HUMBAGI) and state.has(itemName.CLAWBTS, self.player))\
                or self.check_solo_moves(state, itemName.LSPRING)
        elif self.world.options.logic_type == 2: # advanced
            logic = (self.check_humba_magic(state, itemName.HUMBAGI) and state.has(itemName.CLAWBTS, self.player))\
                or self.check_solo_moves(state, itemName.LSPRING)
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.check_humba_magic(state, itemName.HUMBAGI) and state.has(itemName.CLAWBTS, self.player))\
                or self.check_solo_moves(state, itemName.LSPRING)
        return logic
    
    def F2_to_F3(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = (self.hasBKMove(state, itemName.FFLIP) and state.has(itemName.GGRAB, self.player) and state.has(itemName.CLAWBTS, self.player))\
                    or self.check_humba_magic(state, itemName.HUMBAGI)
        elif self.world.options.logic_type == 1: # normal
            logic = ((self.hasBKMove(state, itemName.FFLIP) and state.has(itemName.GGRAB, self.player) or self.veryLongJump(state)) and state.has(itemName.CLAWBTS, self.player))\
                    or self.check_humba_magic(state, itemName.HUMBAGI) or self.check_solo_moves(state, itemName.LSPRING)
        elif self.world.options.logic_type == 2: # advanced
            logic = ((self.hasBKMove(state, itemName.FFLIP) and state.has(itemName.GGRAB, self.player) or self.veryLongJump(state)) and state.has(itemName.CLAWBTS, self.player))\
                    or self.check_humba_magic(state, itemName.HUMBAGI) or self.check_solo_moves(state, itemName.LSPRING)
        elif self.world.options.logic_type == 3: # glitched
            logic = ((self.hasBKMove(state, itemName.FFLIP) and state.has(itemName.GGRAB, self.player) or self.veryLongJump(state)) and state.has(itemName.CLAWBTS, self.player))\
                    or self.check_humba_magic(state, itemName.HUMBAGI) or self.check_solo_moves(state, itemName.LSPRING)
        return logic
    
    def F3_to_F2(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hasBKMove(state, itemName.CLIMB)
        elif self.world.options.logic_type == 1: # normal
            logic = self.hasBKMove(state, itemName.CLIMB) or (self.hasBKMove(state, itemName.FFLIP) and self.hasBKMove(state, itemName.BBUST) and self.veryLongJump(state))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.hasBKMove(state, itemName.CLIMB) or (self.hasBKMove(state, itemName.FFLIP) and self.longJump(state))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasBKMove(state, itemName.CLIMB) or (self.hasBKMove(state, itemName.FFLIP) and self.longJump(state))
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
        elif self.world.options.logic_type == 3: # glitched
            if fromTrain:
                logic = self.hfp_jiggy(state) and self.can_access_clifftop(state, fromTrain)
            else:
                logic = (self.hfp_jiggy(state) and self.can_access_clifftop(state, fromTrain)) or \
                        self.has_train_access(state, "HFP")
        return logic
    
    def can_access_plateau(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.GGRAB, self.player) or self.dilberta_free(state)
        elif self.world.options.logic_type == 1: # normal
            logic = state.has(itemName.GGRAB, self.player) or self.dilberta_free(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def can_access_pinegrove(self, state: CollectionState, fromTrain: bool) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.canShootEggs(state, itemName.FEGGS) and self.can_access_plateau(state) and \
                    state.has(itemName.EGGAIM, self.player)
        elif self.world.options.logic_type == 1 : # normal
            if fromTrain:
                logic = (self.canShootEggs(state, itemName.FEGGS) and self.can_access_plateau(state))
            else:
                logic = (self.canShootEggs(state, itemName.FEGGS) and self.can_access_plateau(state)) or \
                        ((self.has_train_access(state, "WW") and self.ww_jiggy(state)) or \
                        (self.has_train_access(state, "TDL") and state.has(itemName.TTORP, self.player)))
        elif self.world.options.logic_type == 2: # advanced
            if fromTrain:
                logic = (self.canShootEggs(state, itemName.FEGGS) and self.can_access_plateau(state))
            else:
                logic = (self.canShootEggs(state, itemName.FEGGS) and self.can_access_plateau(state)) or \
                        ((self.has_train_access(state, "WW") and self.ww_jiggy(state)) or \
                        (self.has_train_access(state, "TDL") and state.has(itemName.TTORP, self.player)))
        elif self.world.options.logic_type == 3: # glitched
            if fromTrain:
                logic = (self.canShootEggs(state, itemName.FEGGS) and self.can_access_plateau(state))
            else:
                logic = (self.canShootEggs(state, itemName.FEGGS) and self.can_access_plateau(state)) or \
                        ((self.has_train_access(state, "WW") and self.ww_jiggy(state)) or \
                        (self.has_train_access(state, "TDL") and state.has(itemName.TTORP, self.player)))
        return logic
    
    def WL_to_PGU(self, state: CollectionState) -> bool:
        logic = True
        # Going through the loading zone gives you dive for free, which is a thing beginners would not know.
        if self.world.options.logic_type == 0: # beginner
            logic = state.has(itemName.TTORP, self.player) and self.hasBKMove(state, itemName.DIVE)
        elif self.world.options.logic_type == 1 : # normal
            logic = state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = state.has(itemName.TTORP, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def JRL_to_CT(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.jrl_jiggy(state)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def HFP_to_CTHFP(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hfp_jiggy(state)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic
    
    def TDL_to_IOHWL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.tdl_jiggy(state)
        elif self.world.options.logic_type == 1: # normal
            logic = True
        elif self.world.options.logic_type == 2: # advanced
            logic = True
        elif self.world.options.logic_type == 3: # glitched
            logic = True
        return logic

    def TDL_to_WW(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.oogle_boogles_open(state) and (self.BKSpringPad(state) or self.has_explosives(state))
        elif self.world.options.logic_type == 1: # normal
            logic = self.oogle_boogles_open(state) and (self.BKSpringPad(state) or self.has_explosives(state))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.oogle_boogles_open(state) and (self.BKSpringPad(state) or self.has_explosives(state))
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.BKSpringPad(state) or self.has_explosives(state)) and (self.oogle_boogles_open(state) or \
                self.clockworkWarp(state))
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
        elif self.world.options.logic_type == 3: # glitched
            logic = self.ccl_jiggy(state) and self.can_access_wasteland(state, False)
        return logic
    
    def ccl_jiggy(self, state: CollectionState) -> bool: # 45
        if self.world.worlds_randomized == True:
            return state.has(itemName.CCA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.CC]
            return state.has(itemName.JIGGY, self.player, amt)
    
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

    def HFP_hot_water_cooled(self, state) -> bool:
        return self.can_access_hailfire(state, False) and\
               self.can_access_ccl(state) and \
               state.has(itemName.SPLITUP, self.player)

    def can_use_floatus(self, state) -> bool:
        return self.check_solo_moves(state, itemName.TAXPACK) and self.check_solo_moves(state, itemName.HATCH)

    def grow_beanstalk(self, state: CollectionState) -> bool:
        return state.has(itemName.BDRILL, self.player) and self.check_mumbo_magic(state, itemName.MUMBOCC)

    def check_hag1_options(self, state: CollectionState) -> bool:
        enough_jiggies = self.world.options.open_hag1 == 1 or state.has(itemName.JIGGY, self.player, 70)
        return enough_jiggies and \
                (self.check_solo_moves(state, itemName.PACKWH) or self.check_solo_moves(state, itemName.SAPACK) or
                self.check_solo_moves(state, itemName.SHPACK)) and \
                state.has(itemName.BBLASTER, self.player) and \
                state.has(itemName.CEGGS, self.player)
    
    def reach_cheato(self, state: CollectionState, page_amt: int) -> bool:
        return state.has(itemName.PAGES, self.player, page_amt) and (self.hasBKMove(state, itemName.FPAD) or (self.hasBKMove(state, itemName.FFLIP) and self.hasBKMove(state, itemName.CLIMB)))

    def hasBKMove(self, state: CollectionState, move) -> bool:
        if move not in [itemName.DIVE,itemName.FPAD,itemName.GRAT,itemName.ROLL,itemName.ARAT,itemName.BBARGE,itemName.TJUMP,itemName.FLUTTER,itemName.FFLIP,itemName.CLIMB,itemName.BEGG,itemName.TTROT,itemName.BBUST,itemName.WWING,itemName.SSTRIDE,itemName.TTRAIN,itemName.BBOMB,itemName.EGGAIM]:
            raise Exception("Not a BK move! {}".format(move))
        if self.world.options.randomize_bk_moves == 0: # Not randomised
            return True
        elif self.world.options.randomize_bk_moves == 1 and move not in [itemName.DIVE, itemName.FPAD, itemName.FFLIP, itemName.EGGSHOOT, itemName.ROLL]: # McJiggy Special, not randomised.
            return True
        return state.has(move, self.player)
    
    # You need tall jump to let the charging animation finish, if you're BK combined.
    def BKSpringPad(self, state: CollectionState) -> bool:
        return self.hasBKMove(state, itemName.TJUMP)
    
    def canDoSmallElevation(self, state: CollectionState) -> bool:
        return self.hasBKMove(state, itemName.FFLIP) or self.hasBKMove(state, itemName.TJUMP) or self.hasBKMove(state, itemName.TTROT)
    
    def canReachSlightlyElevatedLedge(self, state: CollectionState) -> bool:
        return (self.hasBKMove(state, itemName.FFLIP) or self.hasBKMove(state, itemName.TJUMP) or (self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FLUTTER))) and state.has(itemName.GGRAB, self.player)
    
    def hasGroundAttack(self, state: CollectionState) -> bool:
        BKAttack = True in list(map(lambda move: self.hasBKMove(state, move),
                [itemName.EGGSHOOT, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.GRAT, itemName.BDRILL, itemName.BBUST]))
        
        return BKAttack or state.has(itemName.BBASH, self.player)
    
    def hasMobileAttack(self, state: CollectionState) -> bool:
        return True in list(map(lambda move: self.hasBKMove(state, move),
                [itemName.EGGSHOOT, itemName.BBARGE, itemName.ROLL, itemName.ARAT]))
    
    def canShootEggs(self, state: CollectionState, egg: str = None) -> bool:
        if egg not in [itemName.BEGG, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS, None]:
            raise Exception("Not an egg! {}".format(egg))
        if egg is None:
            return state.has(itemName.EGGAIM, self.player) or self.hasBKMove(state, itemName.EGGSHOOT)
        return (state.has(itemName.EGGAIM, self.player) or self.hasBKMove(state, itemName.EGGSHOOT)) and state.has(egg, self.player)
    
    def canShootLinearEgg(self, state: CollectionState) -> bool:
        return True in list(map(lambda egg: self.canShootEggs(state, egg), [itemName.BEGG, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS]))
    
    def canGetPassedKlungo(self, state: CollectionState) -> bool:
        if self.world.options.skip_klungo == 1:
            return True
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hasMobileAttack(state)
        elif self.world.options.logic_type == 1: # normal
            logic = self.hasMobileAttack(state)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.hasGroundAttack(state)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasGroundAttack(state)
        return logic
    
    def clockworkWarp(self, state: CollectionState) -> bool:
        return (state.has(itemName.CEGGS, self.player) and state.has(itemName.GEGGS, self.player)\
                    and state.has(itemName.EGGAIM, self.player) and self.hasBKMove(state, itemName.EGGSHOOT))
    
    def longJump(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.hasBKMove(state, itemName.TTROT) or self.hasBKMove(state, itemName.FLUTTER) or self.hasBKMove(state, itemName.ARAT)
        elif self.world.options.logic_type == 1: # normal
            logic = self.hasBKMove(state, itemName.TTROT) or self.hasBKMove(state, itemName.FLUTTER) or self.hasBKMove(state, itemName.ARAT)
        elif self.world.options.logic_type == 2: # advanced
            logic = self.hasBKMove(state, itemName.TTROT) or self.hasBKMove(state, itemName.FLUTTER) or self.hasBKMove(state, itemName.ARAT)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasBKMove(state, itemName.TTROT) or self.hasBKMove(state, itemName.FLUTTER) or self.hasBKMove(state, itemName.ARAT)
        return logic

    def veryLongJump(self, state: CollectionState) -> bool:
        return self.hasBKMove(state, itemName.TTROT) and (self.hasBKMove(state, itemName.FLUTTER) or self.hasBKMove(state, itemName.ARAT))
    
    def extremelyLongJump(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = False
        elif self.world.options.logic_type == 1: # normal
            logic = False
        elif self.world.options.logic_type == 2: # advanced
            logic = self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FLUTTER) and self.hasBKMove(state, itemName.BBUST)
        elif self.world.options.logic_type == 3: # glitched
            logic = self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FLUTTER) and self.hasBKMove(state, itemName.BBUST)
        return logic

    def humbaGGM(self, state: CollectionState) -> bool:
        return self.hasBKMove(state, itemName.TTROT) and state.has(itemName.HUMBAGM, self.player)
    
    def mumboGGM(self, state: CollectionState) -> bool:
        return self.canDoSmallElevation(state) and state.has(itemName.MUMBOGM, self.player)
    
    def mumboTDL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = ((self.canDoSmallElevation(state) and self.hasBKMove(state, itemName.SSTRIDE)) or self.TDLFlightPad(state))\
                     and state.has(itemName.MUMBOTD, self.player)
        elif self.world.options.logic_type == 1: # normal
            logic = (self.canDoSmallElevation(state) or self.TDLFlightPad(state)) and state.has(itemName.MUMBOTD, self.player)
        elif self.world.options.logic_type == 2: # advanced
            logic = (self.canDoSmallElevation(state) or self.TDLFlightPad(state)) and state.has(itemName.MUMBOTD, self.player)
        elif self.world.options.logic_type == 3: # glitched
            logic = (self.canDoSmallElevation(state) or self.TDLFlightPad(state)) and state.has(itemName.MUMBOTD, self.player)
        return logic
    
    def TDLFlightPad(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == 0: # beginner
            logic = self.can_beat_terry(state) and state.has(itemName.SPRINGB, self.player) and self.hasBKMove(state, itemName.FPAD)
        elif self.world.options.logic_type == 1: # normal
            logic = self.can_beat_terry(state) and ((state.has(itemName.SPRINGB, self.player) and self.hasBKMove(state, itemName.FPAD))\
                    or (self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FLUTTER)))
        elif self.world.options.logic_type == 2: # advanced
            logic = self.can_beat_terry(state) and ((state.has(itemName.SPRINGB, self.player) and self.hasBKMove(state, itemName.FPAD))\
                    or (self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FLUTTER)))
        elif self.world.options.logic_type == 3: # glitched
            logic = self.can_beat_terry(state) and ((state.has(itemName.SPRINGB, self.player) and self.hasBKMove(state, itemName.FPAD))\
                    or (self.hasBKMove(state, itemName.TTROT) and self.hasBKMove(state, itemName.FLUTTER)))
        return logic
    
    def GGMSlope(self, state: CollectionState) -> bool:
        return self.hasBKMove(state, itemName.TTROT) or self.hasBKMove(state, itemName.TTRAIN)\
              or (self.GM_boulders(state) and self.hasBKMove(state, itemName.SPLITUP))

    def set_rules(self) -> None:

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

        for location, rules in self.train_rules.items():
            train = self.world.multiworld.get_location(location, self.player)
            set_rule(train, rules)

        for location, rules in self.jinjo_rules.items():
            jinjo = self.world.multiworld.get_location(location, self.player)
            set_rule(jinjo, rules)

        for location, rules in self.notes_rules.items():
            notes = self.world.multiworld.get_location(location, self.player)
            set_rule(notes, rules)

        for location, rules in self.stopnswap_rules.items():
            stop = self.world.multiworld.get_location(location, self.player)
            set_rule(stop, rules)

        if self.world.options.skip_puzzles:
            for location, rules in self.access_rules.items():
                access = self.world.multiworld.get_location(location, self.player)
                set_rule(access, rules)

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

        if self.world.options.cheato_rewards.value == True:
            for location, rules in self.cheato_rewards_rules.items():
                cheato = self.world.multiworld.get_location(location, self.player)
                set_rule(cheato, rules)

        if self.world.options.victory_condition == 1:
            for location, rules in self.gametoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.MUMBOTOKEN, self.player, 15)
        elif self.world.options.victory_condition == 2:
            for location, rules in self.bosstoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.MUMBOTOKEN, self.player, 8)
        elif self.world.options.victory_condition == 3:
            for location, rules in self.jinjotoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.MUMBOTOKEN, self.player, 9)
        elif self.world.options.victory_condition == 4:
            for location, rules in self.bosstoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            for location, rules in self.gametoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            for location, rules in self.jinjotoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.MUMBOTOKEN, self.player, 32) \
            and self.check_hag1_options(state)
        elif self.world.options.victory_condition == 5:
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.MUMBOTOKEN, self.player, self.world.options.token_hunt_length.value)
        else:
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has("Kick Around", self.player)