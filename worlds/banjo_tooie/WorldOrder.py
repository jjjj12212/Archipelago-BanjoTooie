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
    # Universal Tracker Magic
    if hasattr(world.multiworld, "re_gen_passthrough"): 
        if "Banjo-Tooie" in world.multiworld.re_gen_passthrough:
            passthrough = world.multiworld.re_gen_passthrough["Banjo-Tooie"]
            world.randomize_worlds = passthrough['world_order']
            world.randomize_order = passthrough['world_keys']
            world.worlds_randomized = bool(passthrough['worlds'] == 'true') 
            world.starting_egg = passthrough['starting_egg']
            world.starting_attack = passthrough['starting_attack']
            world.single_silo = passthrough['first_silo']
            world.loading_zones = passthrough['loading_zones']
    else:
        worlds = [
            regionName.MT,
            regionName.GM,
            regionName.WW,
            regionName.JR,
            regionName.TL,
            regionName.GIO,
            regionName.HP,
            regionName.CC,
            regionName.CK
        ]
        if world.options.randomize_worlds and world.options.randomize_moves == True and \
        world.options.skip_puzzles == True:
            random.shuffle(world.world_sphere_1)
            first_level = world.world_sphere_1[0]
            # #temp
            # while first_level != regionName.CC:
            #     random.shuffle(world.world_sphere_1)
            #     first_level = world.world_sphere_1[0]
            # #temp
            all_good = False
            second_level_selection = []
            while(all_good == False):
                if world.options.randomize_bk_moves == 0:
                    if first_level == regionName.GIO and (world.options.randomize_cheato.value == False or world.options.randomize_jinjos == False or \
                    world.options.randomize_notes == False):
                        random.shuffle(world.world_sphere_1)
                        first_level = world.world_sphere_1[0]
                        continue
                    elif first_level == regionName.TL and (world.options.randomize_cheato.value == False or world.options.randomize_jinjos == False) and \
                    (world.options.randomize_notes == False or world.options.randomize_treble == False):
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
                else:
                    if first_level == regionName.GIO and (world.options.randomize_chuffy.value == False or world.options.randomize_stations.value == False):
                        random.shuffle(world.world_sphere_1)
                        first_level = world.world_sphere_1[0]
                        continue
                    if first_level == regionName.JR and world.options.randomize_doubloons.value == False:
                        second_level_selection = [regionName.MT, regionName.HP, regionName.GM]
                        all_good = True
                    if first_level == regionName.HP:
                        second_level_selection = [regionName.MT, regionName.JR, regionName.GM]
                        all_good = True
                    if first_level == regionName.CC:
                        second_level_selection = [regionName.MT, regionName.TL]
                        all_good = True
                    else:
                        all_good = True
            i = 1

            for level in world.world_sphere_1:
                if i == 1:
                    if world.options.game_length.value != 3:
                        world.randomize_worlds.update({level: 1})
                    else:
                        world.randomize_worlds.update({level: world.options.world_1.value})
                    i = i+1
                else:
                    world.world_sphere_2.append(level)

            random.shuffle(world.world_sphere_2)

            if len(second_level_selection) > 0:
                second_level = random.choice(second_level_selection)
                i = i+1
                if world.options.game_length.value == 1: # Normal
                    world.randomize_worlds.update({second_level: 4})
                elif world.options.game_length.value == 0: # Quick
                    world.randomize_worlds.update({second_level: 3})
                elif world.options.game_length.value == 2: # Long
                    world.randomize_worlds.update({second_level: 8})
                else: # Custom
                    world.randomize_worlds.update({second_level: world.options.world_2.value})
                world.world_sphere_2.remove(second_level)
                for level in world.world_sphere_2:
                    if i == 3:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 8})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 6})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 16})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_3.value})
                    elif i == 4:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 14})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 10})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 25})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_4.value})
                    elif i == 5:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 20})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 15})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 34})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_5.value})                    
                    elif i == 6:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 28})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 21})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 43})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_6.value})  
                    elif i == 7:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 36})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 28})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 52})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_7.value})  
                    elif i == 8:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 45})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 36})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 61})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_8.value})  
                    i = i+1
            else:
                for level in world.world_sphere_2:
                    if i == 2:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 4})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 3})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 8})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_2.value})
                    elif i == 3:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 8})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 6})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 16})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_3.value})
                    elif i == 4:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 14})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 10})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 25})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_4.value})
                    elif i == 5:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 20})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 15})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 34})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_5.value})                    
                    elif i == 6:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 28})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 21})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 43})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_6.value})  
                    elif i == 7:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 36})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 28})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 52})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_7.value})  
                    elif i == 8:
                        if world.options.game_length.value == 1: # Normal
                            world.randomize_worlds.update({level: 45})
                        elif world.options.game_length.value == 0: # Quick
                            world.randomize_worlds.update({level: 36})
                        elif world.options.game_length.value == 2: # Long
                            world.randomize_worlds.update({level: 61})
                        else: # Custom
                            world.randomize_worlds.update({level: world.options.world_8.value})  
                    i = i+1
            # CK is always last
            if world.options.game_length.value == 1: # Normal
                world.randomize_worlds.update({regionName.CK: 55})
            elif world.options.game_length.value == 0: # Quick
                world.randomize_worlds.update({regionName.CK: 44})
            elif world.options.game_length.value == 2: # Long
                world.randomize_worlds.update({regionName.CK: 70})
            else: # Custom
                world.randomize_worlds.update({regionName.CK: world.options.world_9.value})

            i = 1230944
            for location, jiggy in world.randomize_worlds.items():
                world.randomize_order.update({location: i})
                i += 1

            # if world.options.game_length.value == 3:
            #     order = sorted(world.randomize_worlds.items(), key=lambda x: x[1])
            #     world.randomize_worlds = {}
            #     i = 1
            #     for level, jiggy in order:
            #         world.randomize_worlds.update({level: jiggy})
            #         world.randomize_order.update({i: location})
            #         i += 1


            first_level = list(world.randomize_worlds.keys())[0]
            second_level = list(world.randomize_worlds.keys())[1]
            #Silos
            if world.options.open_silos.value == 1:
                if  first_level == regionName.TL or first_level == regionName.CC:
                    world.single_silo = regionName.IOHWL
                if first_level == regionName.GM:
                    world.single_silo = regionName.IOHPL
                if  first_level == regionName.WW:
                    world.single_silo = regionName.IOHPG
                if first_level == regionName.JR or first_level == regionName.HP:
                    world.single_silo = regionName.IOHCT
                if first_level == regionName.GIO:
                    world.single_silo = regionName.IOHCT
            elif world.options.open_silos.value == 2:
                world.single_silo = "ALL"
            else:
                world.single_silo = "NONE"
            #EO Silos
            if world.options.randomize_bk_moves != 2:
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
            else: # All BK Moves shuffled
                #Silos
                if world.options.open_silos.value != 2:
                    #if world.options.open_silos.value == 0:
                        #world.options.open_silos.value = 1 #Override
                    if  first_level == regionName.TL or first_level == regionName.CC:
                        world.single_silo = regionName.IOHWL
                    if first_level == regionName.GM:
                        world.single_silo = regionName.IOHPL
                    if  first_level == regionName.WW:
                        world.single_silo = regionName.IOHPG
                    if first_level == regionName.JR or first_level == regionName.HP:
                        world.single_silo = regionName.IOHCT
                    if first_level == regionName.GIO:
                        world.single_silo = regionName.IOHCT
                #EOSilos
                if  first_level == regionName.WW:
                    world.multiworld.early_items[world.player][itemName.SPLITUP] = 1
                if first_level == regionName.JR and world.options.randomize_doubloons.value == False \
                    and second_level == regionName.HP:
                    move_lst = [itemName.TJUMP, itemName.FFLIP, itemName.SPLITUP, itemName.TTROT]
                    move = random.choice(move_lst)
                    world.multiworld.early_items[world.player][move] = 1
                if first_level == regionName.HP:
                    move_lst = [itemName.TJUMP, itemName.FFLIP, itemName.SPLITUP, itemName.TTROT]
                    move = random.choice(move_lst)
                    world.multiworld.early_items[world.player][move] = 1
                if first_level == regionName.CC:
                    move_lst = [itemName.TJUMP, itemName.FFLIP, itemName.TTROT, itemName.FPAD]
                    move = random.choice(move_lst)
                    world.multiworld.early_items[world.player][move] = 1
                if first_level == regionName.GIO:
                    world.multiworld.early_items[world.player][itemName.CHUFFY] = 1
                    world.multiworld.early_items[world.player][itemName.TRAINSWGI] = 1
                    world.multiworld.early_items[world.player][itemName.CLIMB] = 1
                    world.multiworld.early_items[world.player][itemName.TRAINSWIH] = 1
                    world.multiworld.early_items[world.player][itemName.FFLIP] = 1
            world.worlds_randomized = True
        else:
            world1_jiggy = 0
            world2_jiggy = 0
            world3_jiggy = 0
            world4_jiggy = 0
            world5_jiggy = 0
            world6_jiggy = 0
            world7_jiggy = 0
            world8_jiggy = 0
            world9_jiggy = 0

            if world.options.game_length.value == 1: # Normal
                world1_jiggy = 1
                world2_jiggy = 4
                world3_jiggy = 8
                world4_jiggy = 14
                world5_jiggy = 20
                world6_jiggy = 28
                world7_jiggy = 36
                world8_jiggy = 45
                world9_jiggy = 55
            elif world.options.game_length.value == 0: # Quick
                world1_jiggy = 1
                world2_jiggy = 3
                world3_jiggy = 6
                world4_jiggy = 10
                world5_jiggy = 15
                world6_jiggy = 21
                world7_jiggy = 28
                world8_jiggy = 35
                world9_jiggy = 44
            elif world.options.game_length.value == 2: # Long
                world1_jiggy = 1
                world2_jiggy = 8
                world3_jiggy = 16
                world4_jiggy = 25
                world5_jiggy = 34
                world6_jiggy = 43
                world7_jiggy = 52
                world8_jiggy = 60
                world9_jiggy = 70
            else: # Custom
                world1_jiggy = world.options.world_1.value
                world2_jiggy = world.options.world_2.value
                world3_jiggy = world.options.world_3.value
                world4_jiggy = world.options.world_4.value
                world5_jiggy = world.options.world_5.value
                world6_jiggy = world.options.world_6.value
                world7_jiggy = world.options.world_7.value
                world8_jiggy = world.options.world_8.value
                world9_jiggy = world.options.world_9.value
            world.randomize_worlds = {
                regionName.MT:  world1_jiggy,
                regionName.GM:  world2_jiggy,
                regionName.WW:  world3_jiggy,
                regionName.JR:  world4_jiggy,
                regionName.TL:  world5_jiggy,
                regionName.GIO: world6_jiggy,
                regionName.HP:  world7_jiggy,
                regionName.CC:  world8_jiggy,
                regionName.CK:  world9_jiggy 
            }
            world.randomize_order = {
                regionName.MT:  1230944,
                regionName.GM:  1230945,
                regionName.WW:  1230946,
                regionName.JR:  1230947,
                regionName.TL:  1230948,
                regionName.GIO: 1230949,
                regionName.HP:  1230950,
                regionName.CC:  1230951,
                regionName.CK:  1230952 
            }
            world.worlds_randomized = False
            #Silos
            if world.options.open_silos.value == 0:
                world.single_silo = "NONE"
            elif world.options.open_silos.value == 2:
                world.single_silo = "ALL"
            else:
                silo_rando = [
                    regionName.IOHWL,
                    regionName.IOHPL,
                    regionName.IOHPG,
                    regionName.IOHCT,
                    regionName.IOHQM
                ]
                random.shuffle(silo_rando)
                world.single_silo = silo_rando[0]

        if world.options.randomize_world_loading_zone.value == True:
            gen_res = False
            while(gen_res == False):
                random.shuffle(worlds)
                if worlds[0] != regionName.CK and worlds[0] != regionName.GIO:
                    gen_res = True
            world.loading_zones = {
                regionName.MT : worlds[0],
                regionName.GM : worlds[1],
                regionName.WW : worlds[2],
                regionName.JR : worlds[3],
                regionName.TL : worlds[4],
                regionName.GIO: worlds[5],
                regionName.HP : worlds[6],
                regionName.CC : worlds[7],
                regionName.CK : worlds[8]
            }
        else:
            world.loading_zones = {
                regionName.MT : regionName.MT,
                regionName.GM : regionName.GM,
                regionName.WW : regionName.WW,
                regionName.JR : regionName.JR,
                regionName.TL : regionName.TL,
                regionName.GIO: regionName.GIO,
                regionName.HP : regionName.HP,
                regionName.CC : regionName.CC,
                regionName.CK : regionName.CK
            }


    