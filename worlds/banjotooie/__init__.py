import random
import settings
import typing
from jinja2 import Environment, FileSystemLoader
# from .Game import game_name, filler_item_name
from .Items import BanjoTooieItem, all_item_table, all_group_table
from .Locations import BanjoTooieLocation, all_location_table
from .Regions import BANJOTOOIEREGIONS, create_regions, connect_regions
from .Options import BanjoTooieOptions
from .Rules import BanjoTooieRules
from .Names import itemName



#from Utils import get_options
from BaseClasses import ItemClassification, Tutorial, Item, Region, MultiWorld
#from Fill import fill_restrictive
from ..AutoWorld import World, WebWorld

class BanjoTooieWeb(WebWorld):
    setup = Tutorial("Setup Banjo Tooie",
        """Class to build website tutorial pages from a .md file in the world's /docs folder. Order is as follows.
        Name of the tutorial as it will appear on the site. Concise description covering what the guide will entail.
        Language the guide is written in. Name of the file ex 'setup_en.md'. Name of the link on the site; game name is
        filled automatically so 'setup/en' etc. Author or authors.""",
        "English",
        "setup_en.md",
        "setup/en",
        ["Mike J."])
    

class BanjoTooieWorld(World):
    """
    Banjo-Tooie is a single-player platform game in which the protagonists are controlled from a third-person perspective.
    Carrying over most of the mechanics and concepts established in its predecessor,
    the game features three-dimensional worlds consisting of various platforming challenges and puzzles, with a notable
    increased focus on puzzle-solving over the worlds of Banjo-Kazooie.
    """
    game: str = "Banjo Tooie"
    web = BanjoTooieWeb()
    options_dataclass =  BanjoTooieOptions
    options: BanjoTooieOptions
    topology_preset = True
    kingjingalingjiggy = False
    slot_data = []

    # item_name_to_id = {name: data.btid for name, data in all_item_table.items()}
    item_name_to_id = {}
    for name, data in all_item_table.items():
        if data.btid == 1230028:  # Skip Victory Item
            continue
        item_name_to_id[name] = data.btid

    location_name_to_id = {name: data.btid for name, data in all_location_table.items()}

    item_name_groups = {
        "Jiggy": all_group_table["jiggy"],
        "Jinjo": all_group_table["jinjo"],
    }
    

    def create_item(self, itemname: str) -> Item:
        banjoItem = all_item_table.get(itemname)
        if banjoItem.type == 'progress':
            item_classification = ItemClassification.progression
        if banjoItem.type == 'useful':
            item_classification = ItemClassification.useful

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
        for name,id in all_item_table.items():
            item = self.create_item(name)
            if self.item_filter(item):
                for i in range(id.qty):
                    itempool += [self.create_item(name)]
        
        for item in itempool:
            self.multiworld.itempool.append(item)

    def item_filter(self, item: Item) -> Item:
        if(item.code == 1230685 and self.kingjingalingjiggy == False and self.options.jingaling_jiggy == True):
            #Below give the king a guarentee Jiggy if option is set
            self.multiworld.get_location(self.location_id_to_name[1230685], self.player).place_locked_item(item)
            self.kingjingalingjiggy = True
            return False #doesn't need to be in the Pool.
        
        if item.code == 0: #Events
            return False
        
        if(item.code == 1230514 and self.options.multiworld_doubloons == False) :
            return False
        
        if(item.code == 1230513 and self.options.mutliworld_cheato == False) :
            return False
        
        # if((1230703 <= item.code <= 1230727) and self.options.multiworld_honeycombs == False) :
        if(item.code == 1230512 and self.options.multiworld_honeycombs == False) :
            return False
        
        if(item.code == 1230511 and self.options.multiworld_glowbos == False) :
            return False
        
        if((item.code == 1230501 or item.code == 1230502 or item.code == 1230503 or item.code == 1230504 or
            item.code == 1230505 or item.code == 1230506 or item.code == 1230507 or item.code == 1230508 or
            item.code == 1230509 ) and self.options.multiworld_jinjos == False) :
            return False

        return True

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)

    def set_rules(self) -> None:
        rules = Rules.BanjoTooieRules(self)
        return rules.set_rules()
    
    def pre_fill(self) -> None:
        if self.options.multiworld_honeycombs == False:    
            for name, id in self.location_name_to_id.items():
                item = self.create_item(itemName.HONEY)
                if name.find("Honeycomb") != -1:
                    self.multiworld.get_location(name, self.player).place_locked_item(item)

    def fill_slot_data(self) -> dict[str, any]:
        btoptions = dict[str, any]()
        btoptions["player_name"] = self.multiworld.player_name[self.player]
        btoptions["seed"] = random.randint(12212, 69996)
        btoptions["deathlink"] = "true" if self.options.death_link.value == 1 else "false"
        if self.options.skip_tower_of_tragedy == 1:
            btoptions["skip_tot"] = "true"
        elif self.options.skip_tower_of_tragedy == 2:
            btoptions["skip_tot"] = "round 3"
        else:
            btoptions["skip_tot"] = "false"
        btoptions['honeycomb'] = "true" if self.options.multiworld_honeycombs == 1 else "false"
        return btoptions



    