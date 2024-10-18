import random
from multiprocessing import Process
import settings
import typing
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
from .Items import BanjoTooieItem, all_item_table, all_group_table
from .Locations import BanjoTooieLocation, all_location_table
from .Regions import create_regions, connect_regions
from .Options import BanjoTooieOptions
from .Rules import BanjoTooieRules
from .Names import itemName, locationName, regionName
from .WorldOrder import WorldRandomize

#from Utils import get_options
from BaseClasses import ItemClassification, Tutorial, Item, Region, MultiWorld
#from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type


def run_client():
    from worlds.banjo_tooie.BTClient import main  # lazy import
    p = Process(target=main)
    p.start()

components.append(Component("Banjo-Tooie Client", func=run_client, component_type=Type.CLIENT))

#NOTE! For Backward Compatability, don't use type str|None. multi types not allowed on older Pythons
class BanjoTooieWeb(WebWorld):
    setup = Tutorial("Setup Banjo-Tooie",
        """A guide to setting up Archipelago Banjo-Tooie on your computer.""",
        "English",
        "setup_en.md",
        "setup/en",
        ["Beebaleen"])
    
    tutorials = [setup]
    

class BanjoTooieWorld(World):
    """
    Banjo-Tooie is a single-player platform game in which the protagonists are controlled from a third-person perspective.
    Carrying over most of the mechanics and concepts established in its predecessor,
    the game features three-dimensional worlds consisting of various platforming challenges and puzzles, with a notable
    increased focus on puzzle-solving over the worlds of Banjo-Kazooie.
    """
    
    game: str = "Banjo-Tooie"
    web = BanjoTooieWeb()
    topology_preset = True
    # item_name_to_id = {name: data.btid for name, data in all_item_table.items()}
    item_name_to_id = {}

    for name, data in all_item_table.items():
        if data.btid is None:  # Skip Victory Item
            continue
        item_name_to_id[name] = data.btid

    location_name_to_id = {name: data.btid for name, data in all_location_table.items()}

    item_name_groups = {
        # "Jiggy": all_group_table["jiggy"],
        "Jinjo": all_group_table["jinjo"],
        "Moves": all_group_table["moves"],
        "Magic": all_group_table["magic"],
        "Stations": all_group_table["stations"],
        "StopnSwap": all_group_table["stopnswap"],
        "Access": all_group_table["levelaccess"],
        "Dino": all_group_table["dino"]
    }
        
    options_dataclass =  BanjoTooieOptions
    options: BanjoTooieOptions

    def __init__(self, world, player):
        self.version = "V3.1"
        self.kingjingalingjiggy = False
        self.starting_egg: int = 0
        self.starting_attack: int = 0
        self.jiggy_counter: int = 0
        self.doubloon_counter: int = 0
        self.notecounter: int = 0
        self.slot_data = []
        self.use_cheato_filler = False
        self.randomize_worlds = {}
        self.randomize_order = {}
        self.world_sphere_1 = [
            regionName.MT,
            regionName.GM,
            regionName.WW,
            regionName.JR,
            regionName.HP,
            regionName.TL,
            regionName.CC,
            regionName.GIO
        ]
        self.world_sphere_2 = [
        ]
        self.worlds_randomized = False
        super(BanjoTooieWorld, self).__init__(world, player)

    def create_item(self, itemname: str) -> Item:
        banjoItem = all_item_table.get(itemname)
        if banjoItem.type == 'progress':
            if banjoItem.btid == 1230515:
                maxJiggy = max(self.randomize_worlds.values()) if self.randomize_worlds else 70
                if self.jiggy_counter > maxJiggy and self.options.exceeding_items_filler.value == True:
                    item_classification = ItemClassification.filler
                else:
                    item_classification = ItemClassification.progression
                self.jiggy_counter += 1
            elif banjoItem.btid == 1230797 and self.options.randomize_notes.value == True:
                if self.notecounter > 124 and self.options.exceeding_items_filler.value == True:
                    item_classification = ItemClassification.filler
                else:
                    item_classification = ItemClassification.progression
                self.notecounter += 1
            else:
                item_classification = ItemClassification.progression
        if banjoItem.type == 'progression_skip_balancing': #Mumbo Tokens
            item_classification = ItemClassification.progression_skip_balancing
        if banjoItem.type == 'useful':
            if banjoItem.btid == 1230513 and self.use_cheato_filler == False: #pages
                if self.options.cheato_rewards.value == True:
                    item_classification = ItemClassification.progression
                else:
                    item_classification = ItemClassification.useful
            elif banjoItem.btid == 1230513 and self.use_cheato_filler == True: #pages
                if self.options.cheato_rewards.value == True:
                    item_classification = ItemClassification.progression
                else:
                    item_classification = ItemClassification.filler
            elif banjoItem.btid == 1230512 and self.options.honeyb_rewards.value == True: #Honeycombs
                item_classification = ItemClassification.progression
            else:
                item_classification = ItemClassification.useful

        if banjoItem.type == 'filler':
            item_classification = ItemClassification.filler
        
        if banjoItem.type == 'trap':
            item_classification = ItemClassification.trap

        if banjoItem.type == "victory":
            victory_item = BanjoTooieItem("Kick Around", ItemClassification.filler, None, self.player)
            return victory_item

        created_item = BanjoTooieItem(self.item_id_to_name[banjoItem.btid], item_classification, banjoItem.btid, self.player)
        return created_item

    def create_event_item(self, name: str) -> Item:
        item_classification = ItemClassification.progression
        created_item = BanjoTooieItem(name, item_classification, None, self.player)
        return created_item
    
    def create_items(self) -> None:
        itempool = []
        if self.options.cheato_as_filler == True:
            self.use_cheato_filler = True
        for name,id in all_item_table.items():
            item = self.create_item(name)
            if self.item_filter(item):
                if item.code == 1230515 and self.kingjingalingjiggy == True:
                    for i in range(id.qty - 1): #note the -1 in the count here. King Took one already.
                        if self.options.randomize_jinjos == False and self.jiggy_counter > 80:
                            break
                        else:
                            itempool += [self.create_item(name)]
                else:
                    # Mumbo Token Hunt Item Amt
                    if item.code == 1230798 and self.options.victory_condition.value == 5:
                        for i in range(15):
                            itempool += [self.create_item(name)]
                    # EO Mumbo Token Hunt Item Amt

                    #if none in pool
                    elif item.code == 1230888:
                        if self.options.cheato_rewards.value == True and self.options.randomize_bk_moves.value == 0:
                            for i in range(5):
                                itempool += [self.create_item(name)]
                        if self.options.honeyb_rewards.value == True and self.options.randomize_bk_moves.value == 0: #10 if both options are on
                            for i in range(5):
                                itempool += [self.create_item(name)]
                        if self.options.randomize_bk_moves.value == 1: # 2 moves won't be added to the pool
                            for i in range(2):
                                itempool += [self.create_item(name)]
                        if self.options.randomize_bk_moves.value == 0: # No moves added, fills for the Jiggy Chunks, Dino Kids
                            for i in range(6):
                                itempool += [self.create_item(name)]
                    #end of none qty logic

                    else:
                        for i in range(id.qty):
                            if self.options.randomize_jinjos == False and self.jiggy_counter > 81 and item.code == 1230515:
                                break
                            if self.options.victory_condition.value == 5:
                                if (144 - self.notecounter) < 14 and item.code == 1230797:
                                    break #sub in for Mumbo Tokens up to 10
                                if item.code == 1230801: #remove Jinjo Multiplayer
                                    break
                                itempool += [self.create_item(name)]
                            else:
                                itempool += [self.create_item(name)]
            elif item.code == 1230832 and item.code == self.starting_attack and self.options.progressive_bash_attack.value == 1: #we only need 1 more Progressive Bash Attack
                itempool += [self.create_item(name)] #only creates 1 progressive bash attack
        for item in itempool:
            self.multiworld.itempool.append(item)

    def item_filter(self, item: Item) -> Item:
        if(item.code == 1230515 and self.kingjingalingjiggy == False and self.options.jingaling_jiggy == True):
            #Below give the king a guarentee Jiggy if option is set
            self.multiworld.get_location(self.location_id_to_name[1230685], self.player).place_locked_item(item)
            self.kingjingalingjiggy = True
            return True #doesn't need to be in the Pool.
        
        if item.code == 0: #Events
            return False
        
        if(item.code == 1230514 and self.options.randomize_doubloons == False) :
            return False
        
        if(item.code == 1230513 and self.options.randomize_cheato.value == False) : # Added later in Prefill
            return False
        
        if(item.code == 1230512 and self.options.randomize_honeycombs == False) : # Added later in Prefill
            return False
        
        if(item.code in range(1230753, 1230780) and self.options.randomize_moves == False) : #range you need to add +1 to the end. 
            return False
        
        if(item.code in range(1230174, 1230183) and self.options.randomize_glowbos == False) : #range you need to add +1 to the end.
            return False
        
        if(item.code in range(1230855, 1230864) and self.options.randomize_glowbos == False) : #range you need to add +1 to the end.
            return False

        if(item.code in range(1230501, 1230510) and self.options.randomize_jinjos == False) :#range you need to add +1 to the end.
            return False
        
        if(item.code == 1230516 and self.options.randomize_treble.value == False):
            return False
        
        if item.code == 1230796 and self.options.randomize_chuffy == False:
            return False
        
        if item.code in range(1230790, 1230796) and self.options.randomize_stations == False:
            return False
        
        if item.code == 1230797 and self.options.randomize_notes == False: #Notes
            return False
        
        if item.code == 1230798 and self.options.victory_condition != 5: #Mumbo Tokens for Mini Game and Boss Hunt and Jinjo Fam
            return False
        
        # if item.code == 1230799 and self.options.warp_traps == 0: 
        #     return False
        
        if item.code in range(1230944, 1230953):
            return False
        
        if item.code in range(1230799, 1230805) and self.options.randomize_stop_n_swap == False:
            return False

        if item.code in range(1230810, 1230828) and self.options.randomize_bk_moves.value == 0:
            return False
        elif (item.code == 1230815 or item.code == 1230816) and self.options.randomize_bk_moves.value == 1: # talon trot and tall jump not in pool
            return False
        
        # if item.code == 1230888 and self.options.cheato_rewards.value == False and self.options.honeyb_rewards.value == False:
        #     return False
        if item.code == 1230888 and self.options.randomize_bk_moves.value == 2:
            return False
        
        if self.options.progressive_beak_buster.value == True and (item.code == 1230820 or item.code == 1230757):
            return False
        if item.code == 1230828 and self.options.progressive_beak_buster.value == False:
            return False
        
        if self.options.egg_behaviour.value != 1 and item.code == 1230823: #remove blue eggs in pool
            return False
        if self.options.egg_behaviour.value == 2 and (item.code == 1230756 or item.code == 1230759 or item.code == 1230763 \
            or item.code == 1230767):
            return False
        if item.code == 1230829 and self.options.egg_behaviour.value != 2:
            return False
        if self.options.egg_behaviour.value == 1 and item.code == self.starting_egg: #Already has this egg in inventory
            return False
        
        if self.options.progressive_shoes.value == True and (item.code == 1230826 or item.code == 1230821 \
            or item.code == 1230768 or item.code == 1230773):
            return False
        if item.code == 1230830 and self.options.progressive_shoes.value == False:
            return False
        
        if self.options.progressive_water_training.value == True and (item.code == 1230810 or item.code == 1230778 \
            or item.code == 1230777):
            return False
        if item.code == 1230831 and self.options.progressive_water_training.value == False:
            return False
        
        if self.options.progressive_bash_attack.value == True and (item.code == 1230800 or item.code == 1230824):
            return False
        if item.code == 1230832 and self.options.progressive_bash_attack.value == False:
            return False
        
        if item.code == 1230780 and self.options.randomize_dino_roar.value == False:
            return False

        if self.options.randomize_bk_moves.value != 0 and item.code == self.starting_attack: #Already has this attack in inventory
            return False

        return True

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)

    def generate_early(self) -> None:
        if self.options.cheato_as_filler.value == True and self.options.cheato_rewards == True:
            raise ValueError("Cheato Pages cannot be marked as filler if Cheato Rewards are set.")
        if self.options.randomize_worlds.value == True and self.options.randomize_bk_moves.value != 0 and self.options.logic_type == 0:
            raise ValueError("Randomize Worlds and Randomize BK Moves is not compatible with Beginner Logic.")
        if self.options.randomize_notes == False and self.options.randomize_worlds.value == True and self.options.randomize_bk_moves.value != 0:
            if self.multiworld.players == 1:
                raise ValueError("Randomize Notes is required for Randomize BK Moves and Randomize Worlds enabled.")
        if self.options.progressive_beak_buster.value == True and (self.options.randomize_bk_moves.value == False or self.options.randomize_moves == False):
            raise ValueError("You cannot have progressive Beak Buster without randomizing moves and randomizing BK moves")
        if self.options.egg_behaviour.value == 1 and (self.options.randomize_bk_moves.value == False or self.options.randomize_moves == False):
            raise ValueError("You cannot have Randomize Starting Egg without randomizing moves and randomizing BK moves")
        elif self.options.egg_behaviour.value == 2 and (self.options.randomize_moves == False):
            raise ValueError("You cannot have progressive Eggs without randomizing moves")
        if self.options.progressive_shoes.value == True and (self.options.randomize_bk_moves.value == False or self.options.randomize_moves == False):
            raise ValueError("You cannot have progressive Shoes without randomizing moves and randomizing BK moves")
        if self.options.progressive_water_training.value == True and (self.options.randomize_bk_moves.value == False or self.options.randomize_moves == False):
            raise ValueError("You cannot have progressive Water Training without randomizing moves and randomizing BK moves")
        if self.options.progressive_bash_attack.value == True and (self.options.randomize_stop_n_swap.value == False or self.options.randomize_moves == False):
            raise ValueError("You cannot have progressive bash attack without randomizing Stop N Swap and randomizing BK moves")
        if self.options.egg_behaviour.value == 1:
            eggs = list([itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS])
            random.shuffle(eggs)
            starting_egg = self.create_item(eggs[0])
            self.multiworld.push_precollected(starting_egg)
            banjoItem = all_item_table.get(eggs[0])
            self.starting_egg = banjoItem.btid
        if self.options.egg_behaviour.value == 0 or self.options.egg_behaviour.value == 2:
            starting_egg = self.create_item(itemName.BEGGS)
            self.multiworld.push_precollected(starting_egg)
            banjoItem = all_item_table.get(itemName.BEGGS)
            self.starting_egg = banjoItem.btid
        if self.options.randomize_bk_moves.value != 0:
            chosen_attack: str
            if self.options.victory_condition == 4 and not (self.options.logic_type == 0 and self.options.skip_klungo == 0): # Wonderwing challenge: you start with wonderwing if you can do it.
                chosen_attack = itemName.WWING

            else:
                base_attacks: list
                if self.options.logic_type == 0:
                    base_attacks = [itemName.EGGSHOOT, itemName.EGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT]
                if self.options.logic_type == 1:
                    base_attacks = [itemName.EGGSHOOT, itemName.EGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
                else:
                    base_attacks = [itemName.EGGSHOOT, itemName.EGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
                    base_attacks.append(itemName.PBASH if self.options.progressive_bash_attack.value == 1 else itemName.GRAT)
                    base_attacks.append(itemName.PBBUST if self.options.progressive_beak_buster.value == True else itemName.BBUST)
                chosen_attack = random.choice(base_attacks)

            starting_attack = self.create_item(chosen_attack)
            self.multiworld.push_precollected(starting_attack)
            banjoItem = all_item_table.get(chosen_attack)
            self.starting_attack = banjoItem.btid
        WorldRandomize(self)

    def set_rules(self) -> None:
        rules = Rules.BanjoTooieRules(self)
        return rules.set_rules()
    
    def pre_fill(self) -> None:
        if self.options.randomize_honeycombs.value == False:
            self.banjo_pre_fills(itemName.HONEY, "Honeycomb", False)
                    
        if self.options.randomize_cheato.value == False:
            self.banjo_pre_fills(itemName.PAGES, "Page", False)

        if self.options.randomize_doubloons.value == False:
            self.banjo_pre_fills(itemName.DOUBLOON, "Doubloon", False)

        if self.options.randomize_moves.value == False:
            self.banjo_pre_fills("Moves", None, True)

        if self.options.randomize_dino_roar.value == False:
            self.banjo_pre_fills("Dino", None, True)

        if self.options.randomize_glowbos.value == False:
            self.banjo_pre_fills("Magic", None, True)

        if self.options.randomize_treble.value == False:
            self.banjo_pre_fills(itemName.TREBLE, "Treble Clef", False)
        
        if self.options.randomize_stations.value == False:
            self.banjo_pre_fills("Stations", None, True)

        if self.options.randomize_chuffy.value == False:
            self.banjo_pre_fills(itemName.CHUFFY, "Chuffy", False)

        if self.options.randomize_notes.value == False:
            self.banjo_pre_fills(itemName.NOTE, "Note", False)

        if self.options.randomize_stop_n_swap.value == False:
            self.banjo_pre_fills("StopnSwap", None, True)

        if self.worlds_randomized == False and self.options.skip_puzzles.value == True:
            self.banjo_pre_fills("Access", None, True)
        elif self.worlds_randomized == True:
            world_num = 1
            for world, amt in self.randomize_worlds.items():
                if world == regionName.GIO:
                    item = self.create_item(itemName.GIA)
                elif world == regionName.JR:
                    item = self.create_item(itemName.JRA)
                else:
                    item = self.create_item(world)
                if world_num == 10:
                    self.multiworld.get_location("Boss Unlocked").place_locked_item(item)
                else:
                    self.multiworld.get_location("World "+ str(world_num) +" Unlocked", self.player).place_locked_item(item)
                    world_num = world_num + 1
        else:
            world_num = 1
            for world, amt in self.randomize_worlds.items():
                item = self.create_item(itemName.NONE)
                if world_num == 10:
                    self.multiworld.get_location("Boss Unlocked").place_locked_item(item)
                else:
                    self.multiworld.get_location("World "+ str(world_num) +" Unlocked", self.player).place_locked_item(item)
                    world_num = world_num + 1
        
        if self.options.victory_condition.value == 1 or self.options.victory_condition.value == 4:
            item = self.create_item(itemName.MUMBOTOKEN)
            self.multiworld.get_location(locationName.MUMBOTKNGAME1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME6, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME7, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME8, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME9, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME10, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME11, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME12, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME13, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME14, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNGAME15, self.player).place_locked_item(item)
        
        if self.options.victory_condition.value == 2 or self.options.victory_condition.value == 4:
            item = self.create_item(itemName.MUMBOTOKEN)
            self.multiworld.get_location(locationName.MUMBOTKNBOSS1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNBOSS2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNBOSS3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNBOSS4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNBOSS5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNBOSS6, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNBOSS7, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNBOSS8, self.player).place_locked_item(item)

        if self.options.victory_condition.value == 3 or self.options.victory_condition.value == 4:
            item = self.create_item(itemName.MUMBOTOKEN)
            self.multiworld.get_location(locationName.MUMBOTKNJINJO1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNJINJO2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNJINJO3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNJINJO4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNJINJO5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNJINJO6, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNJINJO7, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNJINJO8, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.MUMBOTKNJINJO9, self.player).place_locked_item(item)
        
        elif self.options.randomize_jinjos.value == False:
            item = self.create_item(itemName.JIGGY)
            self.multiworld.get_location(locationName.JIGGYIH1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH6, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH7, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH8, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JIGGYIH9, self.player).place_locked_item(item)

        if self.options.randomize_jinjos.value == False:
            item = self.create_item(itemName.WJINJO)
            self.multiworld.get_location(locationName.JINJOJR5, self.player).place_locked_item(item)

            item = self.create_item(itemName.OJINJO)
            self.multiworld.get_location(locationName.JINJOWW4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOHP2, self.player).place_locked_item(item)

            item = self.create_item(itemName.YJINJO)
            self.multiworld.get_location(locationName.JINJOWW3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOHP4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOHP3, self.player).place_locked_item(item)

            item = self.create_item(itemName.BRJINJO)
            self.multiworld.get_location(locationName.JINJOGM1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOJR2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOTL2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOTL5, self.player).place_locked_item(item)

            item = self.create_item(itemName.GJINJO)
            self.multiworld.get_location(locationName.JINJOWW5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOJR1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOTL4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGI2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOHP1, self.player).place_locked_item(item)

            item = self.create_item(itemName.RJINJO)
            self.multiworld.get_location(locationName.JINJOMT2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOMT3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOMT5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOJR3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOJR4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOWW2, self.player).place_locked_item(item)

            item = self.create_item(itemName.BLJINJO)
            self.multiworld.get_location(locationName.JINJOGM3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOTL1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOHP5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOCC2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOIH1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOIH4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOIH5, self.player).place_locked_item(item)

            item = self.create_item(itemName.PJINJO)
            self.multiworld.get_location(locationName.JINJOMT1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGM5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOCC1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOCC3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOCC5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOIH2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOIH3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGI4, self.player).place_locked_item(item)

            item = self.create_item(itemName.BKJINJO)
            self.multiworld.get_location(locationName.JINJOMT4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGM2, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGM4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOWW1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOTL3, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGI1, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGI5, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOCC4, self.player).place_locked_item(item)
            self.multiworld.get_location(locationName.JINJOGI3, self.player).place_locked_item(item)



    def banjo_pre_fills(self, itemNameOrGroup: str, locationFindCriteria: str, useGroup: bool ) -> None:
        if useGroup:
            for group_name, item_info in self.item_name_groups.items():
                if group_name == itemNameOrGroup:
                    for name in item_info:
                        item = self.create_item(name)
                        banjoItem = all_item_table.get(name)
                        # self.multiworld.get_location(banjoItem.defualt_location, self.player).place_locked_item(item)
                        location = self.multiworld.get_location(banjoItem.default_location, self.player)
                        location.place_locked_item(item)
        else:
            for name, id in self.location_name_to_id.items():
                item = self.create_item(itemNameOrGroup)
                if name.find(locationFindCriteria) != -1:
                    # self.multiworld.get_location(name, self.player).place_locked_item(item)
                    location = self.multiworld.get_location(name, self.player)
                    location.place_locked_item(item)


    def fill_slot_data(self) -> Dict[str, Any]:
        btoptions = {}
        btoptions["player_name"] = self.multiworld.player_name[self.player]
        btoptions["seed"] = random.randint(12212, 69996)
        btoptions["deathlink"] = "true" if self.options.death_link.value == 1 else "false"
        btoptions["activate_text"] = "true" if self.options.activate_overlay_text.value == 1 else "false"
        btoptions['text_colour'] = int(self.options.overlay_text_colour.value)


        if self.options.skip_tower_of_tragedy == 1:
            btoptions["skip_tot"] = "true"
        elif self.options.skip_tower_of_tragedy == 2:
            btoptions["skip_tot"] = "round 3"
        else:
            btoptions["skip_tot"] = "false"
        btoptions['honeycomb'] = "true" if self.options.randomize_honeycombs == 1 else "false"
        btoptions['honeyb_rewards'] = "true" if self.options.honeyb_rewards == 1 else "false"
        btoptions['pages'] = "true" if self.options.randomize_cheato.value == True else "false"
        btoptions['cheato_rewards'] = "true" if self.options.cheato_rewards == 1 else "false"
        btoptions['moves'] = "true" if self.options.randomize_moves == 1 else "false"
        btoptions['roar'] = "true" if self.options.randomize_dino_roar == 1 else "false"
        btoptions['bk_moves'] = int(self.options.randomize_bk_moves.value)
        btoptions['doubloons'] = "true" if self.options.randomize_doubloons == 1 else "false"
        btoptions['magic'] = "true" if self.options.randomize_glowbos == 1 else "false"
        btoptions['minigames'] = 'skip' if self.options.speed_up_minigames == 1 else "full"
        btoptions['trebleclef'] = "true" if self.options.randomize_treble == 1 else "false"
        btoptions['skip_puzzles'] = "true" if self.options.skip_puzzles == 1 else "false"
        btoptions['open_hag1'] = "true" if self.options.open_hag1 == 1 else "false"
        btoptions['stations'] = "true" if self.options.randomize_stations == 1 else "false"
        btoptions['chuffy'] = "true" if self.options.randomize_chuffy == 1 else "false"
        btoptions['jinjo'] = "true" if self.options.randomize_jinjos == 1 else "false"
        btoptions['notes'] = "true" if self.options.randomize_notes == 1 else "false"
        btoptions['worlds'] = "true" if self.worlds_randomized else "false"
        btoptions['world_order'] = self.randomize_worlds
        btoptions['world_keys'] = self.randomize_order

        btoptions['mystery'] = "true" if self.options.randomize_stop_n_swap == 1 else "false"
        btoptions['goal_type'] = int(self.options.victory_condition.value)
        btoptions['minigame_hunt_length'] = int(self.options.minigame_hunt_length.value)
        btoptions['boss_hunt_length'] = int(self.options.boss_hunt_length.value)
        btoptions['jinjo_family_rescue_length'] = int(self.options.jinjo_family_rescue_length.value)
        btoptions['token_hunt_length'] = int(self.options.token_hunt_length.value)
        btoptions['logic_type'] = int(self.options.logic_type.value)
        # btoptions['warp_traps'] = int(self.options.warp_traps.value)
        btoptions['skip_klungo'] = "true" if self.options.skip_klungo == 1 else "false"
        btoptions['progressive_beak_buster'] = "true" if self.options.progressive_beak_buster == 1 else "false"
        btoptions['egg_behaviour'] = int(self.options.egg_behaviour.value)
        btoptions['progressive_shoes'] = "true" if self.options.progressive_shoes == 1 else "false"
        btoptions['progressive_water_training'] = "true" if self.options.progressive_water_training == 1 else "false"
        btoptions['progressive_bash_attack'] = "true" if self.options.progressive_bash_attack == 1 else "false"

        btoptions['starting_egg'] = int(self.starting_egg)
        btoptions['starting_attack'] = int(self.starting_attack)
        btoptions['version'] = self.version

        return btoptions

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data

    