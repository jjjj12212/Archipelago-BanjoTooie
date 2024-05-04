import random
from .Names import itemName, regionName
from typing import TYPE_CHECKING

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import BanjoTooieWorld
else:
    BanjoTooieWorld = object

# Shamelessly Stolen from KH2 :D


def WorldRandomize(world: BanjoTooieWorld) -> None:
    if world.options.victory_condition == 1 or world.options.victory_condition == 2:
        world.options.randomize_cheato.value = True
    # Universal Tracker Magic
    if hasattr(world.multiworld, "re_gen_passthrough"): 
        if "Banjo-Tooie" in world.multiworld.re_gen_passthrough:
            passthrough = world.multiworld.re_gen_passthrough["Banjo-Tooie"]
            world.randomize_worlds = passthrough['world_order']
            world.worlds_randomized = bool(passthrough['worlds'] == 'true') 
    else:
        if world.options.randomize_worlds and world.options.randomize_moves == True and \
        world.options.skip_puzzles == True:
            random.shuffle(world.world_sphere_1)
            first_level = world.world_sphere_1[0]
            # #temp
            # while first_level != regionName.TL:
            #     random.shuffle(self.world_sphere_1)
            #     first_level = self.world_sphere_1[0]
            # #temp
            all_good = False
            while(all_good == False):
                if first_level == regionName.GIO and (world.options.randomize_cheato.value == False or world.options.randomize_jinjos == False or \
                world.options.randomize_notes == False):
                    random.shuffle(world.world_sphere_1)
                    first_level = world.world_sphere_1[0]
                    continue
                elif first_level == regionName.TL and (world.options.randomize_cheato.value == False or world.options.randomize_jinjos == False) and \
                world.options.randomize_notes == False:
                    random.shuffle(world.world_sphere_1)
                    first_level = world.world_sphere_1[0]
                    continue
                elif first_level == regionName.CC and (world.options.randomize_cheato.value == False or world.options.randomize_jinjos == False) and \
                world.options.randomize_notes == False:
                    random.shuffle(world.world_sphere_1)
                    first_level = world.world_sphere_1[0]
                    continue
                elif first_level == regionName.WW and (world.options.randomize_cheato.value == False or world.options.randomize_jinjos == False) and \
                world.options.randomize_notes == False:
                    random.shuffle(world.world_sphere_1)
                    first_level = world.world_sphere_1[0]
                    continue
                else:
                    all_good = True
            i = 1
            for level in world.world_sphere_1:
                if i == 1:
                    world.randomize_worlds.update({level: 1})
                    i = i+1
                else:
                    world.world_sphere_2.append(level)

            random.shuffle(world.world_sphere_2)
            for level in world.world_sphere_2:
                if i == 2:
                    world.randomize_worlds.update({level: 4})
                elif i == 3:
                    world.randomize_worlds.update({level: 8})
                elif i == 4:
                    world.randomize_worlds.update({level: 14})
                elif i == 5:
                    world.randomize_worlds.update({level: 20})
                elif i == 6:
                    world.randomize_worlds.update({level: 28})
                elif i == 7:
                    world.randomize_worlds.update({level: 36})
                elif i == 8:
                    world.randomize_worlds.update({level: 45})
                i = i+1
            first_level = list(world.randomize_worlds.keys())[0]

            if  first_level != regionName.MT and world.options.logic_type != 2:
                world.multiworld.early_items[world.player][itemName.GGRAB] = 1
            if  first_level == regionName.WW:
                world.multiworld.early_items[world.player][itemName.FEGGS] = 1
            if  first_level == regionName.JR or first_level == regionName.HP:
                world.multiworld.early_items[world.player][itemName.SPLITUP] = 1
            if first_level == regionName.TL or first_level == regionName.CC:
                world.multiworld.early_items[world.player][itemName.FEGGS] = 1
                world.multiworld.early_items[world.player][itemName.TTORP] = 1
            if first_level == regionName.GIO:
                world.multiworld.early_items[world.player][itemName.FEGGS] = 1
                world.multiworld.early_items[world.player][itemName.TTORP] = 1
                # self.multiworld.early_items[self.player][itemName.SPRINGB] = 1
                # self.multiworld.early_items[self.player][itemName.CLAWBTS] = 1
            world.worlds_randomized = True
        else:
            world.randomize_worlds = {
                regionName.MT: 1,
                regionName.GM: 4,
                regionName.WW: 8,
                regionName.JR: 14,
                regionName.TL: 20,
                regionName.GIO: 28,
                regionName.HP:  36,
                regionName.CC:  45, 
            }
            world.worlds_randomized = False

    