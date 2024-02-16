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

    # item_name_to_id = {name: data.btid for name, data in all_item_table.items()}
    item_name_to_id = {}
    for name, data in all_item_table.items():
        if data.btid == 1230028:  # Skip Victory Item
            continue
        item_name_to_id[name] = data.btid


    #location_name_to_id = {name: data.btid for name, data in all_location_table.items()}
    location_name_to_id = {}
    for name, data in all_location_table.items():
        if data.btid == 1230027:  #Skip Victory Location
            continue
        location_name_to_id[name] = data.btid

    item_name_groups = {
        "Jiggy": all_group_table["jiggy"],
        "Jinjo": all_group_table["jinjo"]
    }
    # location_name_to_id = {}
    

    def create_item(self, item: str) -> Item:
        if item.type == 'progress':
            item_classification = ItemClassification.progression
        if item.type == 'useful':
            item_classification = ItemClassification.useful

        if item.type == "victory":
            victory_item = BanjoTooieItem("Kick Around", ItemClassification.filler, None, self.player)
            return victory_item

        created_item = BanjoTooieItem(self.item_id_to_name[item.btid], item_classification, item.btid, self.player)
        if(item.btid == 1230685 and self.kingjingalingjiggy == False and self.options.jingaling_jiggy == True):
            #Below give the king a guarentee Jiggy if option is set
            self.multiworld.get_location(self.location_id_to_name[1230685], self.player).place_locked_item(created_item)
            self.kingjingalingjiggy = True
            junk_item = BanjoTooieItem("Junk", ItemClassification.filler, 0, self.player)
            return junk_item
        
        if(item.btid == 1230514 and self.options.multiworld_dabloons == False) :
            junk_item = BanjoTooieItem("Junk", ItemClassification.filler, 0, self.player)
            return junk_item
        
        if(item.btid == 1230513 and self.options.mutliworld_cheato == False) :
            junk_item = BanjoTooieItem("Junk", ItemClassification.filler, 0, self.player)
            return junk_item
        
        if(item.btid == 1230512 and self.options.multiworld_honeycombs == False) :
            junk_item = BanjoTooieItem("Junk", ItemClassification.filler, 0, self.player)
            return junk_item
        
        if(item.btid == 1230511 and self.options.multiworld_glowbos == False) :
            junk_item = BanjoTooieItem("Junk", ItemClassification.filler, 0, self.player)
            return junk_item
        
        if((item.btid == 1230501 or item.btid == 1230502 or item.btid == 1230503 or item.btid == 1230504 or
            item.btid == 1230505 or item.btid == 1230506 or item.btid == 1230507 or item.btid == 1230508 or
            item.btid == 1230509 ) and self.options.multiworld_jinjos == False) :
            junk_item = BanjoTooieItem("Junk", ItemClassification.filler, 0, self.player)
            return junk_item


        return created_item

    def create_event_item(self, name: str) -> Item:
        item_classification = ItemClassification.progression
        created_item = BanjoTooieItem(name, item_classification, None, self.player)
        return created_item
    
    def create_items(self) -> None:
        # self.multiworld.itempool += [self.create_item(id) for id, id in all_item_table.items() for qty in range(id.qty)]
        itempool = []
        itempool += [self.create_item(id) for id, id in all_item_table.items() for qty in range(id.qty)]
        for item in itempool:
            if(item.code == 0 or item.code == None):
                continue
            self.multiworld.itempool.append(item)
        #  for item in map(self.create_item, all_item_table.items()):
        #     for x in range(all_item_table[item.name].qty):
        #         self.multiworld.itempool.append(item)
    
    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)

    def set_rules(self) -> None:
        rules = Rules.BanjoTooieRules(self)
        return rules.set_rules()

    # def generate_basic(self) -> None:


    

    def generate_output(self, output_directory: str) -> None:
        player_name = self.multiworld.player_name[self.player]
        death_link = "true" if self.options.death_link.value == 1 else "false"
        file_loader = FileSystemLoader("worlds/banjotooie/templates")
        env = Environment(loader=file_loader)
        template = env.get_template("banjotooie_connector_template.lua")
        output = template.render(Player=player_name, seed=random.randint(12212, 69996), deathlink=death_link)
        f = open(output_directory + "\\banjotooie_connector_" + player_name + ".lua", "w")
        f.write(output)
        f.close()


    