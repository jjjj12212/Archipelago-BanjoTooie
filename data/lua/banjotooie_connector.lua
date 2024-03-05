-- Banjo Tooie Connector Lua
-- Created by Mike Jackson (jjjj12212) 
-- with the help of Rose (Oktorose), the OOT Archipelago team, ScriptHawk BT.lua & kaptainkohl for BTrando.lua 

local socket = require("socket")
local json = require('json')
local math = require('math')
require('common')

local last_modified_date = '2024-03-01' -- Should be the last modified date
local script_version = 4
-- Template Variables
local player_name = ""
local seed = 0
local deathlink = false

local btSocket = nil

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"
local DEBUG = false
local DEBUGLVL2 = false

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local frame = 0

local skip_tot = ""
local flag_init_complete = false

--From BTRando.lua
local RDRAMBase = 0x80000000;
local RDRAMSize = 0x800000;
local RAMBase = RDRAMBase;
local RAMSize = RDRAMSize;

local object_array_pointer = 0x136EE0;
local position_pointer = 0xE4
local animation_pointer = 0x1A0;
local player_pointer = 0x135490;
local player_pointer_index = 0x1354DF;
local character_state = 0x136F63;
local camera_pointer_pointer = 0x127728;
local global_flag_pointer = 0x12C780;
local flag_block_pointer = 0x12C770;
local map_location = 0x132DC2;
local last_map = nil;

-- EO BTRando
local isPaused = false;
local checkTotals = false;
local isSaving = false;
local isBackup = false;
local altarClose = false;
local killBTFlag = false;
local isBanjoDed = false;
local isBanjoDedCheck = false;
local multiHoneycomb = false;
local multiPages = false;
local BMMLoaded = false;
local BMMBypass = false;
local APMovesEnabled = false; -- Enable AP Moves Logics
local NeedSiloState = false; --  If True, you are Transistioning maps
local WatchSilo = false; -- Silo found on Map, Need to Monitor Distance
local AMMMovesCleared = false; -- If close to Silo
local FinishedSilo = false; -- Handles if learned a move at Silo
local SiloCounter = 0; -- waits until Silos are loaded if any

local BathPads = false

function isPointer(value)
    return type(value) == "number" and value >= RDRAMBase and value < RDRAMBase + RDRAMSize;
end

function dereferencePointer(address)
    if type(address) == "number" and address >= 0 and address < (RDRAMSize - 4) then
        address = mainmemory.read_u32_be(address);
        if isPointer(address) then
            return address - RDRAMBase;
        end
    end
end

local consumeTable = {
    [8]  = {key=0x0003, name="Glowbos"},
    [9]  = {key=0x3C0C, name="Empty Honeycombs"},
	[10] = {key=0x0319, name="Cheato Pages"},
    [20] = {key=0x1461, name="Mega Glowbo"}
}

function setConsumable(consumable_type, value)
	local index;
	if consumable_type == 'HONEYCOMB'
	then
		index = 9
	elseif consumable_type == 'CHEATO'
	then
		index = 10
    elseif consumable_type == 'GLOWBO'
    then
        index = 8
    elseif consumable_type == 'MEGA GLOWBO'
    then
        index = 20
	end
    local consumablesBlock = dereferencePointer(0x12B250);
    mainmemory.write_u16_be(consumablesBlock + index * 2, value ~ consumeTable[index]["key"]);
    mainmemory.write_u16_be(0x11B080 + index * 0x0C, value);
end

function getConsumable(consumable_type)
	if consumable_type == 'HONEYCOMB'
	then
		index = 9
	elseif consumable_type == 'CHEATO'
	then
		index = 10
    elseif consumable_type == 'GLOWBO'
    then
        index = 8
    elseif consumable_type == 'MEGA GLOWBO'
    then
        index = 20
	end
    local normalValue = mainmemory.read_u16_be(0x11B080 + index * 0x0C);
	return normalValue;
end

function banjoPTR()
    local playerPointerIndex = mainmemory.readbyte(player_pointer_index);
	local banjo = dereferencePointer(player_pointer + 4 * playerPointerIndex);
    return banjo;
end

function getBanjoPos()
    local banjo = banjoPTR()
    if banjo == nil
    then
        return false;
    end
    local plptr = dereferencePointer(banjo + position_pointer);
    if plptr == nil
    then
        return false;
    end
    local pos = { ["Xpos"] = 0, ["Ypos"] = 0, ["Zpos"] = 0};
    pos["Xpos"] = mainmemory.readfloat(plptr + 0x0, true);
    pos["Ypos"] = mainmemory.readfloat(plptr + 0x4, true);
    pos["Zpos"] = mainmemory.readfloat(plptr + 0x8, true);
    return pos;
end

function getBanjoDeathAnimation(check)
    local banjo = banjoPTR()
    if banjo == nil
    then
        return false;
    end

    local ptr = dereferencePointer(banjo + animation_pointer);
    local animation = mainmemory.read_u16_be(ptr + 0x34);

    if check == true
    then
        return animation
    end

    if animation == 216 and isBanjoDedCheck == false
    then
        isBanjoDed = true;
        isBanjoDedCheck = true;
        killBTFlag = false;
        if DEBUG == true
        then
            print("Banjo is Dead");
        end
    elseif isBanjoDedCheck == true and animation ~= 216
    then
        isBanjoDedCheck = false;
        if DEBUG == true
        then
            print("Deathlink Reset");
        end
    end
end

function getMap()
    return mainmemory.read_u16_be(map_location);
end

function checkFlag(byte, _bit)
    local flagBlock = dereferencePointer(flag_block_pointer);
    if flagBlock == nil
    then
        return false
    end
    local currentValue = mainmemory.readbyte(flagBlock + byte);
    if bit.check(currentValue, _bit) then
        return true;
    else
        return false;
    end
end

function clearFlag(byte, _bit)
	if type(byte) == "number" and type(_bit) == "number" and _bit >= 0 and _bit < 8 then
		local flags = dereferencePointer(flag_block_pointer);
        local currentValue = mainmemory.readbyte(flags + byte);
        mainmemory.writebyte(flags + byte, bit.clear(currentValue, _bit));
	end
end

function setFlag(byte, _bit)
	if type(byte) == "number" and type(_bit) == "number" and _bit >= 0 and _bit < 8 then
		local flags = dereferencePointer(flag_block_pointer);
        local currentValue = mainmemory.readbyte(flags + byte);
        mainmemory.writebyte(flags + byte, bit.set(currentValue, _bit));
	end
end


--- Model Detection and logic

local model_list = {
    ["Ugger"] = 0x671,
    ["Altar"] = 0x977,
    ["Jinjo"] = 0x643,
    ["Silo"] = 0x7D7,
    ["Mingy Jongo"] = 0x816,
    ["Player"] = 0xFFFF,
    ["Kazooie Split Pad"] = 0x7E1,
    ["Banjo Split Pad"] = 0x7E2,
}

local obj_model1_slot_base = 0x10;
local obj_model1_slot_size = 0x9C;

function getObjectModel1Pointers()
	object_pointers = {};
	local objectArray = dereferencePointer(object_array_pointer);
	local num_slots = getModelOneCount();
    if num_slots == nil
    then
        return nil
    end
    for i = 0, num_slots - 1 do
        if object_model1_filter == nil then
            table.insert(object_pointers, objectArray + getModelOneSlotBase(i));
        else
            local model1Base = objectArray + getModelOneSlotBase(i);
            if string.contains(getAnimationType(model1Base), object_model1_filter) then
                table.insert(object_pointers, model1Base);
            end
        end
	end
	return object_pointers;
end

function getModelOneCount()
	local objectArray = dereferencePointer(object_array_pointer);
    if objectArray == nil
    then
        return
    end
    local firstObject = dereferencePointer(objectArray + 0x04);
    local lastObject = dereferencePointer(objectArray + 0x08);
	if lastObject == nil 
	then
		return
	end
    return math.floor((lastObject - firstObject) / obj_model1_slot_size) + 1;
end


function getModelOneSlotBase(index)
	return obj_model1_slot_base + index * obj_model1_slot_size;
end

function getAnimationType(model1Base)
	local objectIDPointer = dereferencePointer(model1Base + 0x0);
    if objectIDPointer == nil
    then
        return nil
    end
    local modelIndex = mainmemory.read_u16_be(objectIDPointer + 0x14);
    return modelIndex;
end

------------- End of Model Logics -----------

function setCurrentHealth(value)
	local currentTransformation = mainmemory.readbyte(0x11B065);
	if type(0x11B644) == 'number' then
		value = value or 0;
		value = math.max(0x00, value);
		value = math.min(0xFF, value);
		return mainmemory.write_u8(0x11B644, value);
	end
end

function checkModel(type)
    local pointer_list = getObjectModel1Pointers()
    if pointer_list == nil
    then
        return false
    end

    local enemy = {};
    if type == "enemy"
    then
        table.insert(enemy, model_list["Ugger"]);
    end

    for k, objptr in pairs(pointer_list)
    do
        local currentObjectName = getAnimationType(objptr); -- Required for special data
        if currentObjectName == nil 
        then
            return false
        end

        if type == "enemy"
        then
            for k, enemyval in pairs(enemy)
            do
                if currentObjectName == enemyval
                then
                    return objptr;
                end
            end
        elseif currentObjectName == model_list[type]
        then
            return objptr;
        end
    end
    return false;
end

function checkModels(type) -- returns list
    local pointer_list = getObjectModel1Pointers()
    if pointer_list == nil
    then
        return false
    end

    local i = 0
    local object_list = {}
    for k, objptr in pairs(pointer_list)
    do
        local currentObjectName = getAnimationType(objptr); -- Required for special data
        if currentObjectName == nil and i == 0
        then
            return false
        end
        i = i + 1
        if currentObjectName == model_list[type]
        then
           object_list[i] = objptr;
        end
    end
    return object_list;
end


function getAltar()
    if last_map == 335 or last_map == 337 -- No need to modify RAM when already in WH
    then
        return
    end
    local object = checkModel("Altar");
    if object == false
    then
        return;
    end

    local pos = getBanjoPos()
    if pos == false --possible loading screen
    then
        return false
    end

	local xPos = mainmemory.readfloat(object + 0x04, true);
	local yPos = mainmemory.readfloat(object + 0x08, true);
	local zPos = mainmemory.readfloat(object + 0x0C, true);

	local hDist = math.sqrt(((xPos - pos["Xpos"]) ^ 2) + ((zPos - pos["Zpos"]) ^ 2));
	local playerDist = math.floor(math.sqrt(((yPos - pos["Ypos"]) ^ 2) + (hDist ^ 2)));

    if playerDist <= 300 and (altarClose == false or isBackup == false)
    then
        altarClose = true;
        BMMBackup();
        useAGI();
        if DEBUG == true
        then
            print("Altar Closeby");
        end
    elseif playerDist >=301 and altarClose == true
    then
        BMMRestore()
        altarClose = false;
        if DEBUG == true
        then
            print("Altar Away");
        end
    end
end

function nearWHJinjo()
    
    local object = checkModel("Jinjo");
    if object == false
    then
        BMMBackup()
        useAGI()
        return;
    end

    local pos = getBanjoPos()
    if pos == false --possible loading screen
    then
        return false
    end

	local xPos = mainmemory.readfloat(object + 0x04, true);
	local yPos = mainmemory.readfloat(object + 0x08, true);
	local zPos = mainmemory.readfloat(object + 0x0C, true);

	local hDist = math.sqrt(((xPos - pos["Xpos"]) ^ 2) + ((zPos - pos["Zpos"]) ^ 2));
	local playerDist = math.floor(math.sqrt(((yPos - pos["Ypos"]) ^ 2) + (hDist ^ 2)));

    if playerDist <= 400
    then
        if DEBUG == true
        then
            print("Near Jinjo");
        end
        BMMRestore();
    end
end

local receive_map = { -- [ap_id] = item_id
    [0] = 0
} 

-- Moves that needs to be checked Per Map. some silos NEEDS other moves as well to get to.
local SILO_MAP_CHECK = {
    [0x155] = { -- Cliff Top
        "Ice Eggs",
        ["Exceptions"] = {

        }
    },
    [0x152] = { -- Platau
        "Fire Eggs",
        ["Exceptions"] = {
            "Egg Aim"
        }
    },
    [0x154] = { -- Pine Grove
        "Gernade Eggs",
        ["Exceptions"] = {
            
        }
    },
    [0x15A] = { -- Wasteland
        "Clockwork Kazooie Eggs",
        ["Exceptions"] = {
            
        }
    },
    [0xB8] = { -- MT Main
        "Breegull Blaster",
        "Egg Aim",
        ["Exceptions"] = {
            
        }
    },
    [0xC4] = { -- MT Grove
        "Grip Grab",
        ["Exceptions"] = {
            
        }
    },
    [0xC7] = { -- GM Main
        "Bill Drill",
        ["Exceptions"] = {
            
        }
    },
    [0x163] = { -- GM Storage
        "Beak Bayonet",
        ["Exceptions"] = {
            
        }
    },
    [0xD6] = { -- WW Main
        "Split Up",
        "Airborne Egg Aiming",
        ["Exceptions"] = {
            
        }
    },
    [0xE1] = { -- WW Castle
        "Pack Whack",
        ["Exceptions"] = {
            
        }
    },
    [0x1A7] = { -- JRL Main
        "Wing Whack",
        ["Exceptions"] = {
            
        }
    },
    [0xF6] = { -- JRL Eel Lair
        "Talon Torpedo",
        ["Exceptions"] = {
            
        }
    },
    [0xED] = { -- JRL Jolly
        "Sub-Aqua Egg Aiming",
        ["Exceptions"] = {
            
        }
    },
    [0x122] = { --TDL Main
        "Springy Step Shoes",
        ["Exceptions"] = {
            
        }
    },
    [0x119] = { -- Unga Bunga Cave
        "Hatch",
        ["Exceptions"] = {
  
        }
    },
    [0x117] = { -- TDL River
        "Taxi Pack",
        ["Exceptions"] = {
  
        }
    },
    [0x101] = { -- GI Floor 1
        "Claw Clamber Boots",
        ["Exceptions"] = {
  
        }
    },
    [0x106] = { -- Floor 2
        "Leg Spring",
        ["Exceptions"] = {
  
        }
    },
    [0x111] = { -- GI Waste Disposal
        "Snooze Pack",
        ["Exceptions"] = {
  
        }
    },
    [0x127] = { -- HFP Fire
        "Shack Pack",
        ["Exceptions"] = {
  
        }
    },
    [0x128] = { -- HFP Ice
        "Glide",
        ["Exceptions"] = {
  
        }
    },
    [0x13A] = { -- CC Cave
        "Sack Pack",
        ["Exceptions"] = {
  
        }
    }
}

-- BMM - Backup Memory Map 
local BMM =  {};

-- AMM - Actual Memory Map
local AMM = {};

-- AGI - Archipelago given items
local AGI = {};

-- Banjo Tooie Movelist Table
local BKM = {};

local MASTER_MAP = {
    ['JIGGY'] = {
        ['Jinjo Village: White Jinjo Family Jiggy'] = {
            ['index'] = 1,
            ['addr'] = 0x4F,
            ['bit'] = 0,
            ['locationId'] = 1230676
        },
        ['Jinjo Village: Orange Jinjo Family Jiggy'] = {
            ['index'] = 2,
            ['addr'] = 0x4F,
            ['bit'] = 1,
            ['locationId'] = 1230677
        },
        ['Jinjo Village: Yellow Jinjo Family Jiggy'] = {
            ['index'] = 3,
            ['addr'] = 0x4F,
            ['bit'] = 2,
            ['locationId'] = 1230678
        },
        ['Jinjo Village: Brown Jinjo Family Jiggy'] = {
            ['index'] = 4,
            ['addr'] = 0x4F,
            ['bit'] = 3,
            ['locationId'] = 1230679
        },
        ['Jinjo Village: Green Jinjo Family Jiggy'] = {
            ['index'] = 5,
            ['addr'] = 0x4F,
            ['bit'] = 4,
            ['locationId'] = 1230680
        },
        ['Jinjo Village: Red Jinjo Family Jiggy'] = {
            ['index'] = 6,
            ['addr'] = 0x4F,
            ['bit'] = 5,
            ['locationId'] = 1230681
        },
        ['Jinjo Village: Blue Jinjo Family Jiggy'] = {
            ['index'] = 7,
            ['addr'] = 0x4F,
            ['bit'] = 6,
            ['locationId'] = 1230682
        },
        ['Jinjo Village: Purple Jinjo Family Jiggy'] = {
            ['index'] = 8,
            ['addr'] = 0x4F,
            ['bit'] = 7,
            ['locationId'] = 1230683
        },
        ['Jinjo Village: Black Jinjo Family Jiggy'] = {
            ['index'] = 9,
            ['addr'] = 0x50,
            ['bit'] = 0,
            ['locationId'] = 1230684
        },
        ['Jinjo Village: King Jingaling Jiggy'] = {
            ['index'] = 10,
            ['addr'] = 0x50,
            ['bit'] = 1,
            ['locationId'] = 1230685
        },
        ['MT: Targitzan Jiggy'] = {
            ['index'] = 11,
            ['addr'] = 0x45,
            ['bit'] = 0,
            ['locationId'] = 1230596
        },
        ['MT: Slightly Sacred Chamber Jiggy'] = {
            ['index'] = 12,
            ['addr'] = 0x45,
            ['bit'] = 1,
            ['locationId'] = 1230597
        },
        ['MT: Kickball Jiggy'] = {
            ['index'] = 13,
            ['addr'] = 0x45,
            ['bit'] = 2,
            ['locationId'] = 1230598
        },
        ['MT: Bovina Jiggy'] = {
            ['index'] = 14,
            ['addr'] = 0x45,
            ['bit'] = 3,
            ['locationId'] = 1230599
        },
        ['MT: Treasure Chamber Jiggy'] = {
            ['index'] = 15,
            ['addr'] = 0x45,
            ['bit'] = 4,
            ['locationId'] = 1230600
        },
        ['MT: Golden Goliath Jiggy'] = {
            ['index'] = 16,
            ['addr'] = 0x45,
            ['bit'] = 5,
            ['locationId'] = 1230601
        },
        ['MT: Prison Compound Quicksand Jiggy'] = {
            ['index'] = 17,
            ['addr'] = 0x45,
            ['bit'] = 6,
            ['locationId'] = 1230602
        },
        ['MT: Pillars Jiggy'] = {
            ['index'] = 18,
            ['addr'] = 0x45,
            ['bit'] = 7,
            ['locationId'] = 1230603
        },
        ['MT: Top of Temple Jiggy'] = {
            ['index'] = 19,
            ['addr'] = 0x46,
            ['bit'] = 0,
            ['locationId'] = 1230604
        },
        ['MT: Ssslumber Jiggy'] = {
            ['index'] = 20,
            ['addr'] = 0x46,
            ['bit'] = 1,
            ['locationId'] = 1230605
        },
        ['GGM: Old King Coal Jiggy'] = {
            ['index'] = 21,
            ['addr'] = 0x46,
            ['bit'] = 2,
            ['locationId'] = 1230606
        },
        ['GGM: Canary Mary Jiggy'] = {
            ['index'] = 22,
            ['addr'] = 0x46,
            ['bit'] = 3,
            ['locationId'] = 1230607
        },
        ['GGM: Generator Cavern Jiggy'] = {
            ['index'] = 23,
            ['addr'] = 0x46,
            ['bit'] = 4,
            ['locationId'] = 1230608
        },
        ['GGM: Waterfall Cavern Jiggy'] = {
            ['index'] = 24,
            ['addr'] = 0x46,
            ['bit'] = 5,
            ['locationId'] = 1230609
        },
        ['GGM: Ordinance Storage Jiggy'] = {
            ['index'] = 25,
            ['addr'] = 0x46,
            ['bit'] = 6,
            ['locationId'] = 1230610
        },
        ['GGM: Dilberta Jiggy'] = {
            ['index'] = 26,
            ['addr'] = 0x46,
            ['bit'] = 7,
            ['locationId'] = 1230611
        },
        ['GGM: Crushing Shed Jiggy'] = {
            ['index'] = 27,
            ['addr'] = 0x47,
            ['bit'] = 0,
            ['locationId'] = 1230612
        },
        ['GGM: Waterfall Jiggy'] = {
            ['index'] = 28,
            ['addr'] = 0x47,
            ['bit'] = 1,
            ['locationId'] = 1230613
        },
        ['GGM: Power Hut Basement Jiggy'] = {
            ['index'] = 29,
            ['addr'] = 0x47,
            ['bit'] = 2,
            ['locationId'] = 1230614
        },
        ['GGM: Flooded Caves Jiggy'] = {
            ['index'] = 30,
            ['addr'] = 0x47,
            ['bit'] = 3,
            ['locationId'] = 1230615
        },
        ['WW: Hoop Hurry Jiggy'] = {
            ['index'] = 31,
            ['addr'] = 0x47,
            ['bit'] = 4,
            ['locationId'] = 1230616
        },
        ['WW: Dodgems Jiggy'] = {
            ['index'] = 32,
            ['addr'] = 0x47,
            ['bit'] = 5,
            ['locationId'] = 1230617
        },
        ['WW: Mr. Patch Jiggy'] = {
            ['index'] = 33,
            ['addr'] = 0x47,
            ['bit'] = 6,
            ['locationId'] = 1230618
        },
        ['WW: Saucer of Peril Jiggy'] = {
            ['index'] = 34,
            ['addr'] = 0x47,
            ['bit'] = 7,
            ['locationId'] = 1230619
        },
        ['WW: Balloon Burst Jiggy'] = {
            ['index'] = 35,
            ['addr'] = 0x48,
            ['bit'] = 0,
            ['locationId'] = 1230620
        },
        ['WW: Dive of Death Jiggy'] = {
            ['index'] = 36,
            ['addr'] = 0x48,
            ['bit'] = 1,
            ['locationId'] = 1230621
        },
        ['WW: Mrs. Boggy Jiggy'] = {
            ['index'] = 37,
            ['addr'] = 0x48,
            ['bit'] = 2,
            ['locationId'] = 1230622
        },
        ['WW: Star Spinner Jiggy'] = {
            ['index'] = 38,
            ['addr'] = 0x48,
            ['bit'] = 3,
            ['locationId'] = 1230623
        },
        ['WW: The Inferno Jiggy'] = {
            ['index'] = 39,
            ['addr'] = 0x48,
            ['bit'] = 4,
            ['locationId'] = 1230624
        },
        ['WW: Cactus of Strength Jiggy'] = {
            ['index'] = 40,
            ['addr'] = 0x48,
            ['bit'] = 5,
            ['locationId'] = 1230625
        },
        ['JRL: Mini-Sub Challenge Jiggy'] = {
            ['index'] = 41,
            ['addr'] = 0x48,
            ['bit'] = 6,
            ['locationId'] = 1230626
        },
        ['JRL: Tiptup Jiggy'] = {
            ['index'] = 42,
            ['addr'] = 0x48,
            ['bit'] = 7,
            ['locationId'] = 1230627
        },
        ['JRL: Chris P. Bacon Jiggy'] = {
            ['index'] = 43,
            ['addr'] = 0x49,
            ['bit'] = 0,
            ['locationId'] = 1230628
        },
        ['JRL: Pig Pool Jiggy'] = {
            ['index'] = 44,
            ['addr'] = 0x49,
            ['bit'] = 1,
            ['locationId'] = 1230629
        },
        ["JRL: Smuggler's Cavern Jiggy"] = {
            ['index'] = 45,
            ['addr'] = 0x49,
            ['bit'] = 2,
            ['locationId'] = 1230630
        },
        ['JRL: Merry Maggie Jiggy'] = {
            ['index'] = 46,
            ['addr'] = 0x49,
            ['bit'] = 3,
            ['locationId'] = 1230631
        },
        ['JRL: Woo Fak Fak Jiggy'] = {
            ['index'] = 47,
            ['addr'] = 0x49,
            ['bit'] = 4,
            ['locationId'] = 1230632
        },
        ['JRL: Seemee Jiggy'] = {
            ['index'] = 48,
            ['addr'] = 0x49,
            ['bit'] = 5,
            ['locationId'] = 1230633
        },
        ['JRL: Pawno Jiggy'] = {
            ['index'] = 49,
            ['addr'] = 0x49,
            ['bit'] = 6,
            ['locationId'] = 1230634
        },
        ['JRL: UFO Jiggy'] = {
            ['index'] = 50,
            ['addr'] = 0x49,
            ['bit'] = 7,
            ['locationId'] = 1230635
        },
        ["TDL: Under Terry's Nest Jiggy"] = {
            ['index'] = 51,
            ['addr'] = 0x4A,
            ['bit'] = 0,
            ['locationId'] = 1230636
        },
        ['TDL: Dippy Jiggy'] = {
            ['index'] = 52,
            ['addr'] = 0x4A,
            ['bit'] = 1,
            ['locationId'] = 1230637
        },
        ['TDL: Scrotty Jiggy'] = {
            ['index'] = 53,
            ['addr'] = 0x4A,
            ['bit'] = 2,
            ['locationId'] = 1230638
        },
        ['TDL: Terry Jiggy'] = {
            ['index'] = 54,
            ['addr'] = 0x4A,
            ['bit'] = 3,
            ['locationId'] = 1230639
        },
        ['TDL: Oogle Boogle Tribe Jiggy'] = {
            ['index'] = 55,
            ['addr'] = 0x4A,
            ['bit'] = 4,
            ['locationId'] = 1230640
        },
        ['TDL: Chompas Belly Jiggy'] = {
            ['index'] = 56,
            ['addr'] = 0x4A,
            ['bit'] = 5,
            ['locationId'] = 1230641
        },
        ["TDL: Terry's Kids Jiggy"] = {
            ['index'] = 57,
            ['addr'] = 0x4A,
            ['bit'] = 6,
            ['locationId'] = 1230642
        },
        ['TDL: Stomping Plains Jiggy'] = {
            ['index'] = 58,
            ['addr'] = 0x4A,
            ['bit'] = 7,
            ['locationId'] = 1230643
        },
        ['TDL: Rocknut Tribe Jiggy'] = {
            ['index'] = 59,
            ['addr'] = 0x4B,
            ['bit'] = 0,
            ['locationId'] = 1230644
        },
        ['TDL: Code of the Dinosaurs Jiggy'] = {
            ['index'] = 60,
            ['addr'] = 0x4B,
            ['bit'] = 1,
            ['locationId'] = 1230645
        },
        ['GI: Underwater Waste Disposal Plant Jiggy'] = {
            ['index'] = 61,
            ['addr'] = 0x4B,
            ['bit'] = 2,
            ['locationId'] = 1230646
        },
        ['GI: Weldar Jiggy'] = {
            ['index'] = 62,
            ['addr'] = 0x4B,
            ['bit'] = 3,
            ['locationId'] = 1230647
        },
        ["GI: Clinker's Cavern Jiggy"] = {
            ['index'] = 63,
            ['addr'] = 0x4B,
            ['bit'] = 4,
            ['locationId'] = 1230648
        },
        ['GI: Skivvies Jiggy'] = {
            ['index'] = 64,
            ['addr'] = 0x4B,
            ['bit'] = 5,
            ['locationId'] = 1230649
        },
        ['GI: Floor 5 Jiggy'] = {
            ['index'] = 65,
            ['addr'] = 0x4B,
            ['bit'] = 6,
            ['locationId'] = 1230650
        },
        ['GI: Quality Control Jiggy'] = {
            ['index'] = 66,
            ['addr'] = 0x4B,
            ['bit'] = 7,
            ['locationId'] = 1230651
        },
        ['GI: Floor 1 Guarded Jiggy'] = {
            ['index'] = 67,
            ['addr'] = 0x4C,
            ['bit'] = 0,
            ['locationId'] = 1230652
        },
        ['GI: Trash Compactor Jiggy'] = {
            ['index'] = 68,
            ['addr'] = 0x4C,
            ['bit'] = 1,
            ['locationId'] = 1230653
        },
        ['GI: Twinkly Packing Jiggy'] = {
            ['index'] = 69,
            ['addr'] = 0x4C,
            ['bit'] = 2,
            ['locationId'] = 1230654
        },
        ['GI: Waste Disposal Plant Box Jiggy'] = {
            ['index'] = 70,
            ['addr'] = 0x4C,
            ['bit'] = 3,
            ['locationId'] = 1230655
        },
        ['HFP: Dragon Brothers Jiggy'] = {
            ['index'] = 71,
            ['addr'] = 0x4C,
            ['bit'] = 4,
            ['locationId'] = 1230656
        },
        ['HFP: Inside the Volcano Jiggy'] = {
            ['index'] = 72,
            ['addr'] = 0x4C,
            ['bit'] = 5,
            ['locationId'] = 1230657
        },
        ['HFP: Sabreman Jiggy'] = {
            ['index'] = 73,
            ['addr'] = 0x4C,
            ['bit'] = 6,
            ['locationId'] = 1230658
        },
        ['HFP: Boggy Jiggy'] = {
            ['index'] = 74,
            ['addr'] = 0x4C,
            ['bit'] = 7,
            ['locationId'] = 1230659
        },
        ['HFP: Icy Side Station Jiggy'] = {
            ['index'] = 75,
            ['addr'] = 0x4D,
            ['bit'] = 0,
            ['locationId'] = 1230660
        },
        ['HFP: Oil Drill Jiggy'] = {
            ['index'] = 76,
            ['addr'] = 0x4D,
            ['bit'] = 1,
            ['locationId'] = 1230661
        },
        ['HFP: Stomping Plains Jiggy'] = {
            ['index'] = 77,
            ['addr'] = 0x4D,
            ['bit'] = 2,
            ['locationId'] = 1230662
        },
        ['HFP: Kickball Jiggy'] = {
            ['index'] = 78,
            ['addr'] = 0x4D,
            ['bit'] = 3,
            ['locationId'] = 1230663
        },
        ['HFP: Aliens Jiggy'] = {
            ['index'] = 79,
            ['addr'] = 0x4D,
            ['bit'] = 4,
            ['locationId'] = 1230664
        },
        ['HFP: Lava Waterfall Jiggy'] = {
            ['index'] = 80,
            ['addr'] = 0x4D,
            ['bit'] = 5,
            ['locationId'] = 1230665
        },
        ['CCL: Mingy Jongo Jiggy'] = {
            ['index'] = 81,
            ['addr'] = 0x4D,
            ['bit'] = 6,
            ['locationId'] = 1230666
        },
        ['CCL: Mr Fit Jiggy'] = {
            ['index'] = 82,
            ['addr'] = 0x4D,
            ['bit'] = 7,
            ['locationId'] = 1230667
        },
        ["CCL: Pot O' Gold Jiggy"] = {
            ['index'] = 83,
            ['addr'] = 0x4E,
            ['bit'] = 0,
            ['locationId'] = 1230668
        },
        ['CCL: Canary Mary Jiggy'] = {
            ['index'] = 84,
            ['addr'] = 0x4E,
            ['bit'] = 1,
            ['locationId'] = 1230669
        },
        ['CCL: Zubbas Jiggy'] = {
            ['index'] = 85,
            ['addr'] = 0x4E,
            ['bit'] = 2,
            ['locationId'] = 1230670
        },
        ['CCL: Jiggium Plant Jiggy'] = {
            ['index'] = 86,
            ['addr'] = 0x4E,
            ['bit'] = 3,
            ['locationId'] = 1230671
        },
        ['CCL: Cheese Wedge Jiggy'] = {
            ['index'] = 87,
            ['addr'] = 0x4E,
            ['bit'] = 4,
            ['locationId'] = 1230672
        },
        ['CCL: Trash Can Jiggy'] = {
            ['index'] = 88,
            ['addr'] = 0x4E,
            ['bit'] = 5,
            ['locationId'] = 1230673
        },
        ['CCL: Superstash Jiggy'] = {
            ['index'] = 89,
            ['addr'] = 0x4E,
            ['bit'] = 6,
            ['locationId'] = 1230674
        },
        ['CCL: Jelly Castle Jiggy'] = {
            ['index'] = 90,
            ['addr'] = 0x4E,
            ['bit'] = 7,
            ['locationId'] = 1230675
        },
    },
    ['JINJO'] = {
        -- ['Wooded Hollow: Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230591
        -- },
        -- ['Spiral Mountain: Jinjo'] = {
        --     ['addr'] = 0x3F,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230595
        -- },
        -- ['Plateau: Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230594
        -- },
        -- ['Mayahem Temple: Jade Snake Grove Jinjo'] = {
        --     ['addr'] = 0x39,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230551
        -- },
        -- ['Mayahem Temple: Stadium Jinjo'] = {
        --     ['addr'] = 0x39,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230552
        -- },
        -- ['Mayahem Temple: Targitzan Temple Jinjo'] = {
        --     ['addr'] = 0x39,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230553
        -- },
        -- ['Mayahem Temple: Water Pool Jinjo'] = {
        --     ['addr'] = 0x39,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230554
        -- },
        -- ['Mayahem Temple: Bridge Jinjo'] = {
        --     ['addr'] = 0x3A,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230555
        -- },
        -- ['Glitter Gultch Mine: Water Storage Jinjo'] = {
        --     ['addr'] = 0x3A,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230556
        -- },
        -- ['Glitter Gultch Mine: Jail Jinjo'] = {
        --     ['addr'] = 0x3A,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230557
        -- },
        -- ['Glitter Gultch Mine: Toxic Gas Cave Jinjo'] = {
        --     ['addr'] = 0x3A,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230558
        -- },
        -- ['Glitter Gultch Mine: Boulder Jinjo'] = {
        --     ['addr'] = 0x3A,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230559
        -- },
        -- ['Glitter Gultch Mine: Mine Tracks Jinjo'] = {
        --     ['addr'] = 0x3A,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230560
        -- },
        -- ['Witchyworld: Big Top Jinjo'] = {
        --     ['addr'] = 0x3A,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230561
        -- },
        -- ['Witchyworld: Cave of Horrors Jinjo'] = {
        --     ['addr'] = 0x3A,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230562
        -- },
        -- ['Witchyworld: Van Door Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230563
        -- },
        -- ['Witchyworld: Dodgem Dome Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230564
        -- },
        -- ['Witchyworld: Cactus of Strength Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230565
        -- },
        -- ['Cliff Top: Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230593
        -- },
        -- ['Jolly Rogers: Lagoon Alcove Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230566
        -- },
        -- ['Jolly Rogers: Blubber Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230567
        -- },
        -- ['Jolly Rogers: Big Fish Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230568
        -- },
        -- ['Jolly Rogers: Seaweed Sanctum Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230569
        -- },
        -- ['Jolly Rogers: Sunken Ship Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230570
        -- },
        -- ['Wasteland: Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230592
        -- },
        -- ['Terrydactyland: Talon Torp Jinjo'] = {
        --     ['addr'] = 0x3C,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230571
        -- },
        -- ['Terrydactyland: Cutscene Skip Jinjo'] = {
        --     ['addr'] = 0x3C,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230572
        -- },
        -- ['Terrydactyland: Beside Rocknut Jinjo'] = {
        --     ['addr'] = 0x3C,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230573
        -- },
        -- ['Terrydactyland: Big T. Rex Skip Jinjo'] = {
        --     ['addr'] = 0x3C,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230574
        -- },
        -- ['Terrydactyland: Stomping Plains Jinjo'] = {
        --     ['addr'] = 0x3C,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230575
        -- },
        -- ['Gruntys Industries: Floor 5 Jinjo'] = {
        --     ['addr'] = 0x3C,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230576
        -- },
        -- ['Gruntys Industries: Leg Spring Jinjo'] = {
        --     ['addr'] = 0x3C,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230577
        -- },
        -- ['Gruntys Industries: Waste Disposal Plant Jinjo'] = {
        --     ['addr'] = 0x3C,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230578
        -- },
        -- ['Gruntys Industries: Boiler Plant Jinjo'] = {
        --     ['addr'] = 0x3D,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230579
        -- },
        -- ['Gruntys Industries: Outside Jinjo'] = {
        --     ['addr'] = 0x3D,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230580
        -- },
        -- ['Hailfire Peaks: Lava Waterfall Jinjo'] = {
        --     ['addr'] = 0x3D,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230581
        -- },
        -- ['Hailfire Peaks: Boiling Hot Pool Jinjo'] = {
        --     ['addr'] = 0x3D,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230582
        -- },
        -- ['Hailfire Peaks: Windy Hole Jinjo'] = {
        --     ['addr'] = 0x3D,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230583
        -- },
        -- ['Hailfire Peaks: Icicle Grotto Jinjo'] = {
        --     ['addr'] = 0x3D,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230584
        -- },
        -- ['Hailfire Peaks: Mildred Ice Cube Jinjo'] = {
        --     ['addr'] = 0x3D,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230585
        -- },
        -- ['Cloud Cuckcooland: Trash Can Jinjo'] = {
        --     ['addr'] = 0x3D,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230586
        -- },
        -- ['Cloud Cuckcooland: Cheese Wedge Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230587
        -- },
        -- ['Cloud Cuckcooland: Central Cavern Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230588
        -- },
        -- ['Cloud Cuckcooland: Fake Mumbo Skull Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230589
        -- },
        -- ['Cloud Cuckcooland: Wumba Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230590
        -- },
    },
    ['CHEATO'] = {
        ['Spiral Mountain: Cheato Page'] = {
            ['addr'] = 0x59,
            ['bit'] = 3,
            ['locationId'] = 1230752
        },
        ['MT: Snake Head Cheato Page'] = {
            ['addr'] = 0x56,
            ['bit'] = 3,
            ['locationId'] = 1230728
        },
        ['MT: Prison Compound Cheato Page'] = {
            ['addr'] = 0x56,
            ['bit'] = 4,
            ['locationId'] = 1230729
        },
        ['MT: Jade Snake Grove Cheato Page'] = {
            ['addr'] = 0x56,
            ['bit'] = 5,
            ['locationId'] = 1230730
        },
        ['GGM: Canary Mary Cheato Page'] = {
            ['addr'] = 0x56,
            ['bit'] = 6,
            ['locationId'] = 1230731
        },
        ['GGM: Entrance Cheato Page'] = {
            ['addr'] = 0x56,
            ['bit'] = 7,
            ['locationId'] = 1230732
        },
        ['GGM: Water Storage Cheato Page'] = {
            ['addr'] = 0x57,
            ['bit'] = 0,
            ['locationId'] = 1230733
        },
        ['WW: The Haunted Cavern Cheato Page'] = {
            ['addr'] = 0x57,
            ['bit'] = 1,
            ['locationId'] = 1230734
        },
        ['WW: The Inferno Cheato Page'] = {
            ['addr'] = 0x57,
            ['bit'] = 2,
            ['locationId'] = 1230735
        },
        ['WW: Saucer of Peril Cheato Page'] = {
            ['addr'] = 0x57,
            ['bit'] = 3,
            ['locationId'] = 1230736
        },
        ["JRL: Pawno's Cheato Page"] = {
            ['addr'] = 0x57,
            ['bit'] = 4,
            ['locationId'] = 1230737
        },
        ['JRL: Seemee Cheato Page'] = {
            ['addr'] = 0x57,
            ['bit'] = 5,
            ['locationId'] = 1230738
        },
        ['JRL: Ancient Baths Cheato Page'] = {
            ['addr'] = 0x57,
            ['bit'] = 6,
            ['locationId'] = 1230739
        },
        ["TDL: Dippy's Pool Cheato Page"] = {
            ['addr'] = 0x57,
            ['bit'] = 7,
            ['locationId'] = 1230740
        },
        ['TDL: Inside the Mountain Cheato Page'] = {
            ['addr'] = 0x58,
            ['bit'] = 0,
            ['locationId'] = 1230741
        },
        ['TDL: Boulder Cheato Page'] = {
            ['addr'] = 0x58,
            ['bit'] = 1,
            ['locationId'] = 1230742
        },
        ['GI: Loggo Cheato Page'] = {
            ['addr'] = 0x58,
            ['bit'] = 2,
            ['locationId'] = 1230743
        },
        ['GI: Floor 2 Cheato Page'] = {
            ['addr'] = 0x58,
            ['bit'] = 3,
            ['locationId'] = 1230744
        },
        ['GI: Repair Depot Cheato Page'] = {
            ['addr'] = 0x58,
            ['bit'] = 4,
            ['locationId'] = 1230745
        },
        ['HFP: Lava Side Cheato Page'] = {
            ['addr'] = 0x58,
            ['bit'] = 5,
            ['locationId'] = 1230746
        },
        ['HFP: Icicle Grotto Cheato Page'] = {
            ['addr'] = 0x58,
            ['bit'] = 6,
            ['locationId'] = 1230747
        },
        ['HFP: Icy Side Cheato Page'] = {
            ['addr'] = 0x58,
            ['bit'] = 7,
            ['locationId'] = 1230748
        },
        ['CCL: Canary Mary Cheato Page'] = {
            ['addr'] = 0x59,
            ['bit'] = 0,
            ['locationId'] = 1230749
        },
        ["CCL: Pot O' Gold Cheato Page"] = {
            ['addr'] = 0x59,
            ['bit'] = 1,
            ['locationId'] = 1230750
        },
        ['CCL: Zubbas Cheato Page'] = {
            ['addr'] = 0x59,
            ['bit'] = 2,
            ['locationId'] = 1230751
        },
    },
    ['HONEYCOMB'] = {
        ['Plateau: Honeycomb'] = {
            ['addr'] = 0x42,
            ['bit'] = 2,
            ['locationId'] = 1230727
        },
        ['MT: Entrance Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 2,
            ['locationId'] = 1230703
        },
        ['MT: Bovina Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 3,
            ['locationId'] = 1230704
        },
        ['MT: Treasure Chamber Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 4,
            ['locationId'] = 1230705
        },
        ['GGM: Toxic Gas Cave Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 5,
            ['locationId'] = 1230706
        },
        ['GGM: Boulder Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 6,
            ['locationId'] = 1230707
        },
        ['GGM: Train Station Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 7,
            ['locationId'] = 1230708
        },
        ['WW: Space Zone Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 0,
            ['locationId'] = 1230709
        },
        ['WW: Mumbo Skull Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 1,
            ['locationId'] = 1230710
        },
        ['WW: Crazy Castle Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 2,
            ['locationId'] = 1230711
        },
        ['JRL: Seemee Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 3,
            ['locationId'] = 1230712
        },
        ['JRL: Atlantis Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 4,
            ['locationId'] = 1230713
        },
        ['JRL: Waste Pipe Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 5,
            ['locationId'] = 1230714
        },
        ['TDL: Lakeside Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 6,
            ['locationId'] = 1230715
        },
        ['TDL: Styracosaurus Cave Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 7,
            ['locationId'] = 1230716
        },
        ['TDL: River Passage Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 0,
            ['locationId'] = 1230717
        },
        ['GI: Floor 3 Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 1,
            ['locationId'] = 1230718
        },
        ['GI: Train Station Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 2,
            ['locationId'] = 1230719
        },
        ['GI: Chimney Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 3,
            ['locationId'] = 1230720
        },
        ['HFP: Inside the Volcano Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 4,
            ['locationId'] = 1230721
        },
        ['HFP: Train Station Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 5,
            ['locationId'] = 1230722
        },
        ['HFP: Lava Side Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 6,
            ['locationId'] = 1230723
        },
        ['CCL: Dirt Patch Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 7,
            ['locationId'] = 1230724
        },
        ['CCL: Trash Can Honeycomb'] = {
            ['addr'] = 0x42,
            ['bit'] = 0,
            ['locationId'] = 1230725
        },
        ["CCL: Pot O' Gold Honeycomb"] = {
            ['addr'] = 0x42,
            ['bit'] = 1,
            ['locationId'] = 1230726
        },
    },
    ['GLOWBO'] = {
         ["MT: Mumbo's Glowbo"] = {
             ['addr'] = 0x42,
             ['bit'] = 7,
             ['locationId'] = 1230686
         },
         ['MT: Jade Snake Grove Glowbo'] = {
             ['addr'] = 0x43,
             ['bit'] = 0,
             ['locationId'] = 1230687
         },
         ['GGM: Near Entrance Glowbo'] = {
             ['addr'] = 0x43,
             ['bit'] = 1,
             ['locationId'] = 1230688
         },
         ['GGM: Mine Entrance 2 Glowbo'] = {
             ['addr'] = 0x43,
             ['bit'] = 2,
             ['locationId'] = 1230689
         },
         ['WW: The Inferno Glowbo'] = {
             ['addr'] = 0x43,
             ['bit'] = 3,
             ['locationId'] = 1230690
         },
         ["WW: Wumba's Glowbo"] = {
             ['addr'] = 0x43,
             ['bit'] = 4,
             ['locationId'] = 1230691
         },
         ['Cliff Top: Glowbo'] = {
             ['addr'] = 0x44,
             ['bit'] = 7,
             ['locationId'] = 1230702
         },
         ["JRL: Pawno's Emporium Glowbo"] = {
             ['addr'] = 0x43,
             ['bit'] = 5,
             ['locationId'] = 123069
         },
         ["JRL: Under Wumba's Wigwam Glowbo"] = {
             ['addr'] = 0x43,
             ['bit'] = 6,
             ['locationId'] = 123070
         },
         ['TDL: Unga Bunga Cave Entrance Glowbo'] = {
             ['addr'] = 0x43,
             ['bit'] = 7,
             ['locationId'] = 1230694
         },
         ["TDL: Behind Mumbo's Skull Glowbo"] = {
             ['addr'] = 0x44,
             ['bit'] = 0,
             ['locationId'] = 1230695
         },
         ['GI: Floor 2 Glowbo'] = {
             ['addr'] = 0x44,
             ['bit'] = 1,
             ['locationId'] = 1230696
         },
         ['GI: Floor 3 Glowbo'] = {
             ['addr'] = 0x44,
             ['bit'] = 2,
             ['locationId'] = 1230697
         },
         ['HFP: Lava Side Glowbo'] = {
             ['addr'] = 0x44,
             ['bit'] = 3,
             ['locationId'] = 1230698
         },
         ['HFP: Icy Side Glowbo'] = {
             ['addr'] = 0x44,
             ['bit'] = 4,
             ['locationId'] = 1230699
         },
         ['CCL: Green Pool Glowbo'] = {
             ['addr'] = 0x44,
             ['bit'] = 5,
             ['locationId'] = 1230700
         },
         ['CCL: Central Cavern Glowbo'] = {
             ['addr'] = 0x44,
             ['bit'] = 6,
             ['locationId'] = 1230701
         },
    },
    ['MEGA GLOWBO'] = {
        ['Mega Glowbo'] = {
            ['addr'] = 0x05,
            ['bit'] = 6,
            ['locationId'] = 1230046
        }

    },
    ['DOUBLOON'] = {
        -- ['Jolly Rogers: Town Center Pole 1 Doubloon'] = {
        --     ['addr'] = 0x22,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230521
        -- },
        -- ['Jolly Rogers: Town Center Pole 2 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230522
        -- },
        -- ['Jolly Rogers: Town Center Pole 3 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230523
        -- },
        -- ['Jolly Rogers: Town Center Pole 4 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230524
        -- },
        -- ['Jolly Rogers: Town Center Pole 5 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230525
        -- },
        -- ['Jolly Rogers: Town Center Pole 6 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230526
        -- },
        -- ['Jolly Rogers: Silo 1 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230527
        -- },
        -- ['Jolly Rogers: Silo 2 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230528
        -- },
        -- ['Jolly Rogers: Silo 3 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230529
        -- },
        -- ['Jolly Rogers: Silo 4 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230530
        -- },
        -- ['Jolly Rogers: Toxic Pool 1 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230531
        -- },
        -- ['Jolly Rogers: Toxic Pool 2 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230532
        -- },
        -- ['Jolly Rogers: Toxic Pool 3 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230533
        -- },
        -- ['Jolly Rogers: Toxic Pool 4 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230534
        -- },
        -- ['Jolly Rogers: Mumbo Skull 1 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230535
        -- },
        -- ['Jolly Rogers: Mumbo Skull 2 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230536
        -- },
        -- ['Jolly Rogers: Mumbo Skull 3 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230537
        -- },
        -- ['Jolly Rogers: Mumbo Skull 4 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230538
        -- },
        -- ['Jolly Rogers: Underground 1 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230539
        -- },
        -- ['Jolly Rogers: Underground 2 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230540
        -- },
        -- ['Jolly Rogers: Underground 3 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230541
        -- },
        -- ['Jolly Rogers: Alcove 1 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230542
        -- },
        -- ['Jolly Rogers: Alcove 2 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230543
        -- },
        -- ['Jolly Rogers: Alcove 3 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230544
        -- },
        -- ['Jolly Rogers: Capt Blackeye 1 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230545
        -- },
        -- ['Jolly Rogers: Capt Blackeye 2 Doubloon'] = {
        --     ['addr'] = 0x26,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230546
        -- },
        -- ['Jolly Rogers: Near Jinjo 1 Doubloon'] = {
        --     ['addr'] = 0x26,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230547
        -- },
        -- ['Jolly Rogers: Near Jinjo 2 Doubloon'] = {
        --     ['addr'] = 0x26,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230548
        -- },
        -- ['Jolly Rogers: Near Jinjo 3 Doubloon'] = {
        --     ['addr'] = 0x26,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230549
        -- },
        -- ['Jolly Rogers: Near Jinjo 4 Doubloon'] = {
        --     ['addr'] = 0x26,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230550
        -- }
    },
	["H1"] = {
	 	['Hag 1 Defeated'] = {
			['addr'] = 0x03,
			['bit'] = 3,
			['locationId'] = 1230027
		},
	},
    ["MOVES"] = {
        ['Grip Grab'] = {
            ['addr'] = 0x1B,
            ['bit'] = 1,
            ['locationId'] = 1230753
        },
        ['Breegull Blaster'] = {
            ['addr'] = 0x1B,
            ['bit'] = 2,
            ['locationId'] = 1230754
        },
        ['Egg Aim'] = {
            ['addr'] = 0x1B,
            ['bit'] = 3,
            ['locationId'] = 1230755
        },
        ['Fire Eggs'] = {
            ['addr'] = 0x1E,
            ['bit'] = 1,
            ['locationId'] = 1230756
        },
        ['Bill Drill'] = {
            ['addr'] = 0x1B,
            ['bit'] = 6,
            ['locationId'] = 1230757
        },
        ['Beak Bayonet'] = {
            ['addr'] = 0x1B,
            ['bit'] = 7,
            ['locationId'] = 1230758
        },
        ['Grenade Eggs'] = {
            ['addr'] = 0x1E,
            ['bit'] = 2,
            ['locationId'] = 1230759
        },
        ['Airborne Egg Aiming'] = {
            ['addr'] = 0x1C,
            ['bit'] = 0,
            ['locationId'] = 1230760
        },
        ['Split Up'] = {
            ['addr'] = 0x1C,
            ['bit'] = 1,
            ['locationId'] = 1230761
        },
        ['Pack Whack'] = {
            ['addr'] = 0x1D,
            ['bit'] = 6,
            ['locationId'] = 1230762
        },
        ['Ice Eggs'] = {
            ['addr'] = 0x1E,
            ['bit'] = 4,
            ['locationId'] = 1230763
        },
        ['Wing Whack'] = {
            ['addr'] = 0x1C,
            ['bit'] = 2,
            ['locationId'] = 1230764
        },
        ['Talon Torpedo'] = {
            ['addr'] = 0x1C,
            ['bit'] = 3,
            ['locationId'] = 1230765
        },
        ['Sub-Aqua Egg Aiming'] = {
            ['addr'] = 0x1C,
            ['bit'] = 4,
            ['locationId'] = 1230766
        },
        ['Clockwork Kazooie Eggs'] = {
            ['addr'] = 0x1E,
            ['bit'] = 3,
            ['locationId'] = 1230767
        },
        ['Springy Step Shoes'] = {
            ['addr'] = 0x1D,
            ['bit'] = 3,
            ['locationId'] = 1230768
        },
        ['Taxi Pack'] = {
            ['addr'] = 0x1D,
            ['bit'] = 4,
            ['locationId'] = 1230769
        },
        ['Hatch'] = {
            ['addr'] = 0x1D,
            ['bit'] = 5,
            ['locationId'] = 1230770
        },
        ['Snooze Pack'] = {
            ['addr'] = 0x1D,
            ['bit'] = 0,
            ['locationId'] = 1230771
        },
        ['Leg Spring'] = {
            ['addr'] = 0x1D,
            ['bit'] = 1,
            ['locationId'] = 1230772
        },
        ['Claw Clamber Boots'] = {
            ['addr'] = 0x1D,
            ['bit'] = 2,
            ['locationId'] = 1230773
        },
        ['Shack Pack'] = {
            ['addr'] = 0x1C,
            ['bit'] = 6,
            ['locationId'] = 1230774
        },
        ['Glide'] = {
            ['addr'] = 0x1C,
            ['bit'] = 7,
            ['locationId'] = 1230775
        },
        ['Sack Pack'] = {
            ['addr'] = 0x1D,
            ['bit'] = 7,
            ['locationId'] = 1230776
        },
        --['Fast Swimming'] = {
        --    ['addr'] = 0x1E,
        --    ['bit'] = 5,
        --    ['locationId'] = 1230777
        --},
	},
    ["MAGIC"] = {
        ['Mumbo: Golden Goliath'] = {
          ['addr'] = 0x6A,
          ['bit'] = 7,
          ['locationId'] = 1230855
        },
        ['Mumbo: Levitate'] = {
          ['addr'] = 0x6B,
          ['bit'] = 0,
          ['locationId'] = 1230856
        },
        ['Mumbo: Power'] = {
          ['addr'] = 0x6B,
          ['bit'] = 1,
          ['locationId'] = 1230857
        },
        ['Mumbo: Oxygenate'] = {
          ['addr'] = 0x6B,
          ['bit'] = 2,
          ['locationId'] = 1230858
        },
        ['Mumbo: Grow/Shrink'] = {
          ['addr'] = 0x6B,
          ['bit'] = 3,
          ['locationId'] = 1230859
        },
        ['Mumbo: EMP'] = {
          ['addr'] = 0x6B,
          ['bit'] = 7,
          ['locationId'] = 1230860
        },
        ['Mumbo: Revive'] = {
          ['addr'] = 0x6B,
          ['bit'] = 4,
          ['locationId'] = 1230861
        },
        ['Mumbo: Rain Dance'] = {
          ['addr'] = 0x6B,
          ['bit'] = 5,
          ['locationId'] = 1230862
        },
        ['Mumbo: Heal'] = {
          ['addr'] = 0x6B,
          ['bit'] = 6,
          ['locationId'] = 1230863
        },
        ['Humba: Stony'] = {
          ['addr'] = 0x15,
          ['bit'] = 6,
          ['locationId'] = 1230174
        },
        ['Humba: Detonator'] = {
          ['addr'] = 0x15,
          ['bit'] = 7,
          ['locationId'] = 1230175
        },
        ['Humba: Money Van'] = {
          ['addr'] = 0x16,
          ['bit'] = 0,
          ['locationId'] = 1230176
        },
        ['Humba: Sub'] = {
          ['addr'] = 0x16,
          ['bit'] = 1,
          ['locationId'] = 1230177
        },
        ['Humba: T-Rex'] = {
          ['addr'] = 0x16,
          ['bit'] = 2,
          ['locationId'] = 1230178
        },
        ['Humba: Washing Machine'] = {
          ['addr'] = 0x16,
          ['bit'] = 3,
          ['locationId'] = 1230179
        },
        ['Humba: Snowball'] = {
          ['addr'] = 0x16,
          ['bit'] = 4,
          ['locationId'] = 1230180
        },
        ['Humba: Bee'] = {
          ['addr'] = 0x16,
          ['bit'] = 5,
          ['locationId'] = 1230181
        },
        ['Humba: Dragon'] = {
          ['addr'] = 0x16,
          ['bit'] = 6,
          ['locationId'] = 1230182
        },
    },
	["SKIP"] = {
		['CUTSCENE'] = {
			['Klungo Flyover'] = {
				['addr'] = 0x02,
				['bit'] = 4
			},
			['Jiggywiggy Flyover'] = {
				['addr'] = 0x67,
				['bit'] = 7
			},
			['Jinjo First Time'] = {
				['addr'] = 0x6E,
				['bit'] = 6
			},
			['Jinjo Flyover'] = {
				['addr'] = 0x82,
				['bit'] = 4
			},
			['Jinjo Flyover - Jiggy'] = {
				['addr'] = 0x82,
				['bit'] = 5
			},
			['Jamjars Flyover'] = {
				['addr'] = 0x9B,
				['bit'] = 6
			},
			['Jiggywiggy Laser'] = {
				['addr'] = 0xAC,
				['bit'] = 2
			},
		},
		['INTRO'] = {
			['Bovina'] = {
				['addr'] = 0x04,
				['bit'] = 5
			},
			['Unogopaz'] = {
				['addr'] = 0x06,
				['bit'] = 1
			},
			['Unogopaz - Stony'] = {
				['addr'] = 0x06,
				['bit'] = 1
			},
			['Dilberta'] = {
				['addr'] = 0x06,
				['bit'] = 3
			},
			['Kickball Coach'] = {
				['addr'] = 0x07,
				['bit'] = 4
			},
			['Cheato'] = {
				['addr'] = 0x08,
				['bit'] = 0
			},
			['Mumbo'] = {
				['addr'] = 0x0A,
				['bit'] = 5
			},
			['Bullion Bill'] = {
				['addr'] = 0x0B,
				['bit'] = 2
			},
			['Mrs. Boggy'] = {
				['addr'] = 0x0C,
				['bit'] = 3
			},
			['Humba Wumba'] = {
				['addr'] = 0x0C,
				['bit'] = 7
			},
			['Big Al'] = {
				['addr'] = 0x0E,
				['bit'] = 5
			},
			['Salty Joe'] = {
				['addr'] = 0x0E,
				['bit'] = 6
			},
			['Conga'] = {
				['addr'] = 0x0F,
				['bit'] = 1
			},
			['Moggy'] = {
				['addr'] = 0x12,
				['bit'] = 0
			},
			['Soggy'] = {
				['addr'] = 0x12,
				['bit'] = 1
			},
			['Groggy'] = {
				['addr'] = 0x12,
				['bit'] = 2
			},
			['Tiptup'] = {
				['addr'] = 0x12,
				['bit'] = 4
			},
			['Jolly'] = {
				['addr'] = 0x13,
				['bit'] = 3
			},
			['Maggie - After Rescue'] = {
				['addr'] = 0x13,
				['bit'] = 4
			},
			['Blubber'] = {
				['addr'] = 0x16,
				['bit'] = 7
			},
			['Scrotty'] = {
				['addr'] = 0x26,
				['bit'] = 5
			},
			['Floatie Pig'] = {
				['addr'] = 0x28,
				['bit'] = 0
			},
			['Loggo'] = {
				['addr'] = 0x28,
				['bit'] = 1
			},
			['Oogle Boogle'] = {
				['addr'] = 0x28,
				['bit'] = 7
			},
			-- ['King Jingaling'] = {
			-- 	 ['addr'] = 0x2F,
			--	 ['bit'] = 5
			-- },
			['Mrs. Bottles'] = {
				['addr'] = 0x2F,
				['bit'] = 7
			},
			['Speccy'] = {
				['addr'] = 0x30,
				['bit'] = 0
			},
			['Dingpot'] = {
				['addr'] = 0x30,
				['bit'] = 4
			},
			['Mildred'] = {
				['addr'] = 0x33,
				['bit'] = 5
			},
			['Biggafoot'] = {
				['addr'] = 0x33,
				['bit'] = 7
			},
			['George'] = {
				['addr'] = 0x34,
				['bit'] = 1
			},
			['Three-Armed Pig'] = {
				['addr'] = 0x34,
				['bit'] = 5
			},
			['Oogle Boogle Guard'] = {
				['addr'] = 0x5F,
				['bit'] = 3
			},
			['Dippy'] = {
				['addr'] = 0x60,
				['bit'] = 0
			},
			['Roysten'] = {
				['addr'] = 0x62,
				['bit'] = 7
			},
			['Jiggywiggy'] = {
				['addr'] = 0x66,
				['bit'] = 3
			},
			['Colosseum Kickball Coach'] = {
				['addr'] = 0x68,
				['bit'] = 6
			},
			['Gamette'] = {
				['addr'] = 0x69,
				['bit'] = 1
			},
			['Superstash'] = {
				['addr'] = 0x6C,
				['bit'] = 0
			},
			['Mr. Fit'] = {
				['addr'] = 0x76,
				['bit'] = 1
			},
			['Heggy'] = {
				['addr'] = 0x78,
				['bit'] = 0
			},
			['Jiggywiggy Disciple'] = {
				['addr'] = 0x78,
				['bit'] = 5
			},
			['Jamjars'] = {
				['addr'] = 0x7C,
				['bit'] = 4
			},
			['Canary Mary - GGM'] = {
				['addr'] = 0x80,
				['bit'] = 2
			},
			['Canary Mary - CCL'] = {
				['addr'] = 0x80,
				['bit'] = 3
			},
			['Honey B'] = {
				['addr'] = 0x98,
				['bit'] = 1
			},
		},
		['TUTORIAL'] = {
			['Sign'] = {
				['addr'] = 0x02,
				['bit'] = 2
			},
			['Springy-Step Shoes Not Learned'] = {
				['addr'] = 0x04,
				['bit'] = 6
			},
			['Claw Clamber Boots Not Learned'] = {
				['addr'] = 0x04,
				['bit'] = 7
			},
			['Golden Goliath'] = {
				['addr'] = 0x05,
				['bit'] = 0
			},
			['Golden Goliath - Time Up'] = {
				['addr'] = 0x05,
				['bit'] = 1
			},
			['Wumba - Pine Grove'] = {
				['addr'] = 0x05,
				['bit'] = 5
			},
			['Minjo'] = {
				['addr'] = 0x05,
				['bit'] = 7
			},
			['Cheato Code List'] = {
				['addr'] = 0x08,
				['bit'] = 1
			},
			['Code Chamber'] = {
				['addr'] = 0x08,
				['bit'] = 2
			},
			['Code Entry'] = {
				['addr'] = 0x08,
				['bit'] = 3
			},
			['Mumbo Pad'] = {
				['addr'] = 0x0E,
				['bit'] = 2
			},
			['Use Mumbo Pad'] = {
				['addr'] = 0x0E,
				['bit'] = 3
			},
			['Cheat Menu'] = {
				['addr'] = 0x15,
				['bit'] = 3
			},
			['Detransform'] = {
				['addr'] = 0x17,
				['bit'] = 2
			},
			['Clockwork Kazooie'] = {
				['addr'] = 0x18,
				['bit'] = 0
			},
			['Hoop Hurry'] = {
				['addr'] = 0x30,
				['bit'] = 5
			},
			['Balloon Burst'] = {
				['addr'] = 0x30,
				['bit'] = 6
			},
			['Twinkly Packing'] = {
				['addr'] = 0x34,
				['bit'] = 0
			},
			['Glowbo Paid'] = {
				['addr'] = 0x35,
				['bit'] = 1
			},
			['Chilly Willy - Wrong Egg'] = {
				['addr'] = 0x35,
				['bit'] = 7
			},
			['Chilli Billi - Wrong Egg'] = {
				['addr'] = 0x36,
				['bit'] = 0
			},
			['Pot O Gold'] = {
				['addr'] = 0x37,
				['bit'] = 2
			},
			['Warp Silo'] = {
				['addr'] = 0x61,
				['bit'] = 4
			},
			['Floatus Floatium'] = {
				['addr'] = 0x63,
				['bit'] = 0
			},
			['BK Game Pak'] = {
				['addr'] = 0x63,
				['bit'] = 2
			},
			['GI Battery Door'] = {
				['addr'] = 0x63,
				['bit'] = 3
			},
			['Broken Jukebox'] = {
				['addr'] = 0x63,
				['bit'] = 4
			},
			['Daddy T-Rex'] = {
				['addr'] = 0x63,
				['bit'] = 6
			},
			['Stony'] = {
				['addr'] = 0x63,
				['bit'] = 7
			},
			['Detonator'] = {
				['addr'] = 0x64,
				['bit'] = 0
			},
			['Van'] = {
				['addr'] = 0x64,
				['bit'] = 1
			},
			['Sub'] = {
				['addr'] = 0x64,
				['bit'] = 2
			},
			['T-Rex'] = {
				['addr'] = 0x64,
				['bit'] = 3
			},
			['Washing Machine'] = {
				['addr'] = 0x64,
				['bit'] = 4
			},
			['Snowball'] = {
				['addr'] = 0x64,
				['bit'] = 5
			},
			['Bee'] = {
				['addr'] = 0x64,
				['bit'] = 6
			},
			['Dragon Kazooie'] = {
				['addr'] = 0x64,
				['bit'] = 7
			},
			['Puzzle Complete'] = {
				['addr'] = 0x78,
				['bit'] = 1
			},
			['Warp Pad'] = {
				['addr'] = 0x78,
				['bit'] = 6
			},
			['Random Stop Honeycomb'] = {
				['addr'] = 0x7C,
				['bit'] = 5
			},
			['Skill Stop Honeycomb'] = {
				['addr'] = 0x7C,
				['bit'] = 6
			},
			['Saucer of Peril Fixed'] = {
				['addr'] = 0x7D,
				['bit'] = 4
			},
			['Saucer of Peril'] = {
				['addr'] = 0x7D,
				['bit'] = 7
			},
			['Mumbo'] = {
				['addr'] = 0x80,
				['bit'] = 1
			},
			['Jiggywiggy Altar'] = {
				['addr'] = 0x98,
				['bit'] = 0
			},
			['Split Up Not Learned'] = {
				['addr'] = 0x99,
				['bit'] = 4
			},
			['Split Up'] = {
				['addr'] = 0x99,
				['bit'] = 5
			},
			['Canary Mary Race'] = {
				['addr'] = 0x9C,
				['bit'] = 0
			},
			['Puzzle'] = {
				['addr'] = 0xA1,
				['bit'] = 3
			},
		}
    }
}

local read_JIGGY_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['JIGGY'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['JIGGY'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['JIGGY']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['JIGGY'])
        do
            checks[k] = false
        end
        AGI['JIGGY'] = checks;
    end
    return checks;
end

local read_JINJO_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['JINJO'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['JINJO'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['JINJO']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['JINJO'])
        do
            checks[k] = false
        end
        AGI['JINJO'] = checks;
    end
    return checks
end

local read_CHEATO_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['CHEATO'])
        do
			if multiPages == false
            then
                checks[k] = false
            else
				checks[k] = checkFlag(v['addr'], v['bit'])
			end
        end
        AMM['CHEATO'] = checks;
    elseif type == "BMM"
    then
		if multiPages == false
        then
            for k,v in pairs(MASTER_MAP['CHEATO'])
            do
                    checks[k] = false
            end
		else
			checks = BMM['CHEATO']
		end
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['CHEATO'])
        do
            checks[k] = false
        end
        AGI['CHEATO'] = checks;
    end
    return checks
end

local read_HONEYCOMB_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['HONEYCOMB'])
        do
            if multiHoneycomb == false
            then
                checks[k] = false
            else
                checks[k] = checkFlag(v['addr'], v['bit'])
            end 
        end
        AMM['HONEYCOMB'] = checks;
    elseif type == "BMM"
    then
        if multiHoneycomb == false
        then
            for k,v in pairs(MASTER_MAP['HONEYCOMB'])
            do
                    checks[k] = false
            end
        else
            checks = BMM['HONEYCOMB']
        end   
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['HONEYCOMB'])
        do
            checks[k] = false
        end
        AGI['HONEYCOMB'] = checks;
    end
    return checks
end

local read_GLOWBO_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['GLOWBO'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['GLOWBO'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['GLOWBO']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['GLOWBO'])
        do
            checks[k] = false
        end
        AGI['GLOWBO'] = checks;
    end
    return checks
end

local read_MEGA_GLOWBO_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['MEGA GLOWBO'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['MEGA GLOWBO'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['MEGA GLOWBO']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['MEGA GLOWBO'])
        do
            checks[k] = false
        end
        AGI['MEGA GLOWBO'] = checks;
    end
    return checks
end

local read_DOUBLOON_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['DOUBLOON'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['DOUBLOON'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['DOUBLOON']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['DOUBLOON'])
        do
            checks[k] = false
        end
        AGI['DOUBLOON'] = checks;
    end
    return checks
end

local read_H1_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['H1'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['H1'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['H1']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['H1'])
        do
            checks[k] = false
        end
        AGI['H1'] = checks;
    end
    return checks
end

local update_BMK_MOVES_checks = function() --Only run when close to Silos
    for k,v in pairs(MASTER_MAP['MOVES'])
    do
        if BKM[k] == false
        then
            res = checkFlag(v['addr'], v['bit'])
            if res == true
            then
                BKM[k] = res
                FinishedSilo = true
            end
        end 
    end
end

local init_BMK = function(type) --Only run when close to Silos
    local checks = {}
    for k,v in pairs(MASTER_MAP['MOVES'])
    do
        if type == "BKM"
        then
            BKM[k] = checkFlag(v['addr'], v['bit'])
        elseif type == "AGI"
        then
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
    end
    return checks
end

local clear_AMM_MOVES_checks = function() --Only run when transitioning Maps until BT/Silo Model is loaded OR Close to Silo
    for k,v in pairs(MASTER_MAP['MOVES'])
    do
        if BKM[k] == false
        then
            clearFlag(v['addr'], v['bit'])
        end
    end
end

function checkConsumables(consumable_type, location_checks)
	for location_name, value in pairs(AGI[consumable_type])
	do
		if(isBackup == false and (value == false and location_checks[location_name] == true))
		then
			if(DEBUG == true)
			then
				print("Obtained local consumable. Remove from Inventory")
			end
			setConsumable(consumable_type, getConsumable(consumable_type) - 1)
			AGI[consumable_type][location_name] = true
			savingAGI()
		end
	end
end

local update_BMK_MOVES_checks = function() --Only run when close to Silos
    for keys, moves in pairs(SILO_MAP_CHECK[last_map])
    do
        if keys ~= "Exceptions"
        then
            local get_addr = MASTER_MAP['MOVES'][moves]
            if BKM[moves] == false
            then
                local res = checkFlag(get_addr['addr'], get_addr['bit'])
                if res == true
                then
                    if DEBUG == true 
                    then
                        print("Already learnt this Silo. finished")
                    end
                    BKM[moves] = res
                    FinishedSilo = true
                end
            end
        end
    end
end

local init_BMK = function(type) --Only run when close to Silos
    local checks = {}
    for k,v in pairs(MASTER_MAP['MOVES'])
    do
        if type == "BKM"
        then
            BKM[k] = checkFlag(v['addr'], v['bit'])
        elseif type == "AGI"
        then
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
    end
    return checks
end

local clear_AMM_MOVES_checks = function() --Only run when transitioning Maps until BT/Silo Model is loaded OR Close to Silo
    --Only clear the moves that we need to clear 
    for keys, move in pairs(SILO_MAP_CHECK[last_map])
    do
        if keys ~= "Exceptions"
        then
            local addr_info = MASTER_MAP["MOVES"][move]
            if BKM[move] == false
            then
                clearFlag(addr_info['addr'], addr_info['bit']);
            elseif BKM[move] == true
            then
                setFlag(addr_info['addr'], addr_info['bit'])
            end
        else
            for key, disable_move in pairs(SILO_MAP_CHECK[last_map][keys]) --Exception list, always disable
            do
                local addr_info = MASTER_MAP["MOVES"][disable_move]
                clearFlag(addr_info['addr'], addr_info['bit']);
            end
        end
    end
end

local set_AGI_MOVES_checks = function(msg) -- SET AGI Moves into RAM AFTER BT/Silo Model is loaded
    for k,v in pairs(MASTER_MAP['MOVES'])
    do
        if AGI["MOVES"][k] == true
        then
            setFlag(v['addr'], v['bit']);
            if msg == true
            then
                archipelago_msg_box("Received " .. k);
            end
        else
            clearFlag(v['addr'], v['bit']);
        end
    end
end

function checkConsumables(consumable_type, location_checks)
	for location_name, value in pairs(AGI[consumable_type])
	do
		if(isBackup == false and (value == false and location_checks[location_name] == true))
		then
			if(DEBUG == true)
			then
				print("Obtained local consumable. Remove from Inventory")
			end
			setConsumable(consumable_type, getConsumable(consumable_type) - 1)
			AGI[consumable_type][location_name] = true
			savingAGI()
		end
	end
end

function checkConsumables(consumable_type, location_checks)
	for location_name, value in pairs(AGI[consumable_type])
	do
		if(isBackup == false and (value == false and location_checks[location_name] == true))
		then
			if(DEBUG == true)
			then
				print("Obtained local consumable. Remove from Inventory")
			end
			setConsumable(consumable_type, getConsumable(consumable_type) - 1)
			AGI[consumable_type][location_name] = true
			savingAGI()
		end
	end
end

function loadGame(current_map)
    if(current_map == 0x142 or current_map == 0xAF)
    then
        local f = io.open("BT" .. player_name .. "_" .. seed .. ".BMM", "r") -- get #BTplayer_seed.BMM
        if f==nil then
           return false
        else
            isBackup = true
            BMM = json.decode(f:read("l"));
            BKM = json.decode(f:read("l"));
            f:close()
            all_location_checks("AMM")
            all_location_checks("BMM")
            BMMRestore()
            if DEBUG == true
            then
                print("Restoring from Load Game")
            end
            BMMLoaded = true
--            os.remove("BT" .. player_name .. "_" .. seed .. ".BMM")
        end
    else
        if BMMBypass == true
        then
            BMMLoaded = true
        end
        return false
    end
end

function getSiloPlayerModel()
    if SiloCounter <= 2
    then
        if DEBUG == true
        then
            print("Watching Silo")
        end
        SiloCounter = SiloCounter + 1
        return
    end
    local object = checkModel("Silo");
    if object == false
    then
        local player = checkModel("Player");
        if player == false
        then
            return
        end
        if DEBUG == true
        then
            print("No silo on Map")
            print("AP Abilities enabled")
        end
        set_AGI_MOVES_checks(false) --No Silo on this map
        NeedSiloState = false
        WatchSilo = false
        SiloCounter = 0
        return
    end
    if DEBUG == true
    then
        print("Silo Found")
    end
    set_AGI_MOVES_checks(false)
    NeedSiloState = false
    WatchSilo = true
end

function nearSilo()
    local pos = getBanjoPos()
    if pos == false --possible loading screen
    then
        return false
    end

    local objects = checkModels("Silo");
    if objects == false
    then
        return; --Shouldn't hit here at all
    end

    for index, silos in pairs(objects) do
        local xPos = mainmemory.readfloat(silos + 0x04, true);
        local yPos = mainmemory.readfloat(silos + 0x08, true);
        local zPos = mainmemory.readfloat(silos + 0x0C, true);

        --Move the Silo in Witchyworld.
        if (xPos == 0 and yPos == -163 and zPos == -1257)
            and last_map == 0xD6
        then
            mainmemory.writefloat(silos + 0x0C, zPos + 100, true);
            MoveWitchyPads();
        end
    
        local hDist = math.sqrt(((xPos - pos["Xpos"]) ^ 2) + ((zPos - pos["Zpos"]) ^ 2));
        playerDist = math.floor(math.sqrt(((yPos - pos["Ypos"]) ^ 2) + (hDist ^ 2)));
        if playerDist <= 650
        then
            if DEBUG == true
            then
                print("Near Silo");
            end
            break;
        end
    end

    if playerDist <= 650 
    then
        if AMMMovesCleared == false
        then
            clear_AMM_MOVES_checks();
            update_BMK_MOVES_checks();
            AMMMovesCleared = true
        elseif FinishedSilo == false
        then
            if DEBUG == true
            then
                print("Watching BMK Moves");
            end
            update_BMK_MOVES_checks();
        else
            if DEBUG == true
            then
            print("BMK Move Learnt");
            print(playerDist)
            end
        end
    else
        if AMMMovesCleared == true
        then
            if DEBUG == true
            then
                print("Reseting Movelist");
            end
            set_AGI_MOVES_checks(false)
            AMMMovesCleared = false
            FinishedSilo = false;
        end
    end
end

function MoveWitchyPads()

    local objects = checkModels("Kazooie Split Pad");
    for index, pad in pairs(objects) do
        local xPos = mainmemory.readfloat(pad + 0x04, true);
        local yPos = mainmemory.readfloat(pad + 0x08, true);
        local zPos = mainmemory.readfloat(pad + 0x0C, true);

        --Move the Pads in WitchyWorld.
        if (xPos == -125 and yPos == -163 and zPos == -1580)
            and last_map == 0xD6
        then
            mainmemory.writefloat(pad + 0x0C, zPos - 300, true);
--          mainmemory.writefloat(pad + 0x08, yPos - 10, true);
            mainmemory.writefloat(pad + 0x04, xPos + 850, true);
            break
        end
    end

    local objects = checkModels("Banjo Split Pad");
    for index, pad in pairs(objects) do
        local xPos = mainmemory.readfloat(pad + 0x04, true);
        local yPos = mainmemory.readfloat(pad + 0x08, true);
        local zPos = mainmemory.readfloat(pad + 0x0C, true);

        if (xPos == 125 and zPos == -1580)
            and last_map == 0xD6
        then
            mainmemory.writefloat(pad + 0x0C, zPos - 300, true);
--            mainmemory.writefloat(pad + 0x08, yPos - 10, true);
            mainmemory.writefloat(pad + 0x04, xPos + 850, true);
            break
        end
    end
end

function MoveBathPads()
    local kpad = checkModel("Kazooie Split Pad");
    local bpad = checkModel("Banjo Split Pad");
    if kpad == nil or bpad == nil
    then
        return
    end
    local kxPos = mainmemory.readfloat(kpad + 0x04, true);
    local kyPos = mainmemory.readfloat(kpad + 0x08, true);
    local kzPos = mainmemory.readfloat(kpad + 0x0C, true);
    local kzRot = mainmemory.readfloat(kpad + 0x4C, true);
    local kyRot = mainmemory.readfloat(kpad + 0x48, true);

    local bxPos = mainmemory.readfloat(bpad + 0x04, true);
    local byPos = mainmemory.readfloat(bpad + 0x08, true);
    local bzPos = mainmemory.readfloat(bpad + 0x0C, true);
    local bzRot = mainmemory.readfloat(bpad + 0x4C, true);
    local byRot = mainmemory.readfloat(bpad + 0x48, true);

    mainmemory.writefloat(kpad + 0x4C, 0, true);
    mainmemory.writefloat(kpad + 0x0C, kzPos + 450, true);
    mainmemory.writefloat(kpad + 0x08, byPos - 75, true);

    mainmemory.writefloat(bpad + 0x4C, 0, true);
    mainmemory.writefloat(bpad + 0x0C, bzPos + 450, true);
    mainmemory.writefloat(bpad + 0x08, byPos - 75, true);

    BathPads = true
end

function locationControl()
    local mapaddr = getMap()
    if isBackup == true
    then
        if checkFlag(0x1F, 0)== true -- DEMO FILE
        then
            local DEMO = { ['DEMO'] = true}
            return DEMO
        end
        if (last_map ~= mapaddr) and APMovesEnabled == true
        then
            for map,moves in pairs(SILO_MAP_CHECK)
            do
                if mapaddr == map
                then
                    if DEBUG == true
                    then
                         print("Checking Silos")
                    end
                    SiloCounter = 0;
                    NeedSiloState = true
                end
            end
        end
        if ((last_map == 335 or last_map == 337) and (mapaddr ~= 335 and mapaddr ~= 337)) -- Wooded Hollow
        then
            BMMRestore()
            last_map = mapaddr
            return all_location_checks("AMM")
        else
            getAltar()
            nearWHJinjo()
            last_map = mapaddr
            return all_location_checks("BMM");
        end
    else
        if BMMLoaded == false 
        then
            loadGame(mapaddr)
            local DEMO = { ['DEMO'] = true}
            return DEMO
        else
            if (last_map ~= mapaddr) and APMovesEnabled == true
            then
                for map,moves in pairs(SILO_MAP_CHECK)
                do
                    if mapaddr == map
                    then
                        if DEBUG == true
                        then
                            print("Checking Silos")
                        end
                        SiloCounter = 0;
                        NeedSiloState = true
                    end
                end
            end
            if last_map == 0xF4 and BathPads == false
            then
                MoveBathPads()
            end
            if (mapaddr == 335 or mapaddr == 337) and checkTotals == false -- Wooded Hollow / JiggyTemple
            then
                if last_map ~= 335 and last_map ~= 337
                then
                    BMMBackup();
                    useAGI();
                    last_map = mapaddr
                end
                nearWHJinjo()
                return all_location_checks("BMM");
            else
                last_map = mapaddr
                getAltar()
                if altarClose == true
                then
                    return all_location_checks("BMM");
                end
                return all_location_checks("AMM");
            end 
        end
    end
end

function BMMBackup()
    if isBackup == true or BMMLoaded == false
    then
        return
    end
    for item_group, table in pairs(MASTER_MAP)
    do
		if item_group ~= 'SKIP' and item_group ~= 'MOVES' and item_group ~= 'MAGIC' then
			for location, values in pairs(table)
			do
				BMM[item_group][location] = checkFlag(values['addr'], values['bit']);
			end
		end
    end
    if DEBUG == true
    then
        print("Backup complete");
    end
    savingBMM()
    isBackup = true
end

function BMMRestore()
    if isBackup == false
    then
        return
    end

    for item_group , location in pairs(MASTER_MAP)
    do
        if item_group ~= "MOVES" and item_group ~= "SKIP" and item_group ~= 'MAGIC'
        then
            for loc,v in pairs(location)
            do
                if AMM[item_group][loc] == false and BMM[item_group][loc] == true
                then
                    setFlag(v['addr'], v['bit'])
                    AMM[item_group][loc] = BMM[item_group][loc]
                    if DEBUG == true
                    then
                        print(loc .. " Flag Set")
                    end
                elseif AMM[item_group][loc] == true and BMM[item_group][loc] == false
                then
                    clearFlag(v['addr'], v['bit'])
                    AMM[item_group][loc] = BMM[item_group][loc]
                    if DEBUG == true
                    then
                        print(loc .. " Flag Cleared")
                    end
                end
            end
        end
    end
    if DEBUG == true
    then
        print("BMM Restored")
    end
    isBackup = false;
end

function useAGI()
    for item_group, table in pairs(MASTER_MAP)
    do
		if item_group ~= 'SKIP' and item_group ~= 'MOVES' and item_group ~= 'MAGIC' then
			for location,values in pairs(table)
			do
				if AMM[item_group][location] == false and AGI[item_group][location] == true
				then
					setFlag(values['addr'], values['bit'])
					AMM[item_group][location] = true
					if DEBUG == true
					then
						print(location .. " Flag Set");
					end
				elseif AMM[item_group][location] == true and AGI[item_group][location] == false
				then
					clearFlag(values['addr'], values['bit']);
					AMM[item_group][location] = false;
					if DEBUG == true
					then
						print(location .. " Flag Cleared");
					end
				end
			end
		end
    end
end

function all_location_checks(type)
    local location_checks = {}
    local MM = { ['JIGGY']  = {}, ['JINJO'] = {}, ['CHEATO'] = {}, ['HONEYCOMB'] = {}, ['GLOWBO'] = {}, ['MEGA GLOWBO'] = {}, ['DOUBLOON'] = {}, ['H1'] = {}
    };
    for k,v in pairs(read_JIGGY_checks(type))
    do 
        location_checks[k] = v;
        MM['JIGGY'][k] = v;
    end
    for k,v in pairs(read_JINJO_checks(type)) 
    do
        location_checks[k] = v;
        MM['JINJO'][k] = v;
    end
    for k,v in pairs(read_CHEATO_checks(type)) 
    do
        location_checks[k] = v;
        MM['CHEATO'][k] = v;
    end
    for k,v in pairs(read_HONEYCOMB_checks(type)) 
    do
        location_checks[k] = v;
        MM['HONEYCOMB'][k] = v;
    end
    for k,v in pairs(read_GLOWBO_checks(type)) 
    do
        location_checks[k] = v;
        MM['GLOWBO'][k] = v;
    end
    for k,v in pairs(read_MEGA_GLOWBO_checks(type))
    do
        location_checks[k] = v;
        MM['MEGA GLOWBO'][k] = v;
    end
    for k,v in pairs(read_DOUBLOON_checks(type)) 
    do
        location_checks[k] = v;
        MM['DOUBLOON'][k] = v;
    end
	for k,v in pairs(read_H1_checks(type)) 
    do
        location_checks[k] = v;
        MM['H1'][k] = v;
    end
    if next(AMM) == nil then
        AMM = location_checks
    end
    if next(BMM) == nil then
        BMM = MM;
    end

    if multiHoneycomb == true then
        checkConsumables('HONEYCOMB', location_checks)
    end

    if multiPages == true then
        checkConsumables('CHEATO', location_checks)
    end
    checkConsumables('GLOWBO', location_checks)
    checkConsumables('MEGA GLOWBO', location_checks)

    return location_checks
end

function archipelago_msg_box(msg)
    i = 0
    while i<100 do
        bgcolor = "#FC6600"
        brcolor = "#000000"

        gui.drawText(400, 1500, msg, bgcolor, bgcolor, 58)
        emu.frameadvance()
        i = i + 1
    end
    gui.clearGraphics()
end

function processMagicItem(loc_ID)
    for location, table in pairs(MASTER_MAP['MAGIC'])
    do
        if table['locationId'] == loc_ID
        then
            setFlag(table['addr'], table['bit'])
            archipelago_msg_box("Received " .. location);
        end
    end

end

function processAGIItem(item_list)
    for ap_id, memlocation in pairs(item_list) -- Items unrelated to AGI_MAP like Consumables
    do
        if receive_map[ap_id] == nil
        then
            if(memlocation == 1230512 and multiHoneycomb == true)  -- Honeycomb Item
            then
                if DEBUG == true
                then
                    print("HC Obtained")
                end
                setConsumable('HONEYCOMB', getConsumable('HONEYCOMB') + 1)
                archipelago_msg_box("Received Honeycomb");
            elseif(memlocation == 1230513 and multiPages == true) -- Cheato Item
            then
                if DEBUG == true
                then
                    print("Cheato Page Obtained")
                end
                setConsumable('CHEATO', getConsumable('CHEATO') + 1)
                archipelago_msg_box("Received Cheato Page");
            elseif(memlocation == 1230515)
            then
                if DEBUG == true
                then
                    print("Jiggy Obtained")
                end
                for location, values in pairs(MASTER_MAP["JIGGY"])
                do
                    if AGI['JIGGY'][location] == false
                    then
                        AGI['JIGGY'][location] = true
                        archipelago_msg_box("Received Jiggy");
                        break
                    end
                end
            elseif((1230855 <= memlocation and memlocation <= 1230863) or (1230174 <= memlocation and memlocation <= 1230182))
            then
                processMagicItem(memlocation)
            end
        end
    end

    for item_type, table in pairs(MASTER_MAP)
    do
        if item_type ~= 'MAGIC'
        then
            for location, values in pairs(table)
            do
                for ap_id, memlocation in pairs(item_list)
                do
                    if receive_map[ap_id] == nil
                    then
                        if values['locationId'] == memlocation
                        then
                            if DEBUG == true
                            then
                                print("ITEM FOUND FROM AP:" .. location);
                            end
                            AGI[item_type][location] = true;
                            if(1230753 <= memlocation and memlocation <= 1230777)
                            then
                                set_AGI_MOVES_checks(true)
                            end
                        end
                    end
                end
            end
        end
    end
    receive_map = item_list
    savingAGI();
end

function process_block(block)
    -- Sometimes the block is nothing, if this is the case then quietly stop processing
    if block == nil then
        return
    end
    if block['slot_player'] ~= nil
    then
        return
    end
    if next(block['items']) ~= nil
    then
        processAGIItem(block['items'])
    end
    if block['messages'] ~= nil and block['messages'] ~= "" 
    then
        archipelago_msg_box(block['messages']);
    end
    if block['triggerDeath'] == true
    then
        killBTFlag = true;
    end

    if DEBUGLVL2 == true then
        print(block)
    end
end

function receive()
    if player_name == "" and seed == 0
    then
        getSlotData()
    else
        -- Send the message
        local retTable = {}
        retTable["scriptVersion"] = script_version;
        retTable["playerName"] = player_name;
        retTable["deathlinkActive"] = deathlink;
        retTable['locations'] = locationControl()
        retTable['unlocked_moves'] = BKM;
        retTable["isDead"] = isBanjoDed;
        if BMMLoaded == false
        then
            retTable["sync_ready"] = "false"
        else
            retTable["sync_ready"] = "true"
        end

    
        msg = json.encode(retTable).."\n"
        local ret, error = btSocket:send(msg)
        if ret == nil then
            print(error)
        elseif curstate == STATE_INITIAL_CONNECTION_MADE then
            curstate = STATE_TENTATIVELY_CONNECTED
        elseif curstate == STATE_TENTATIVELY_CONNECTED then
            archipelago_msg_box("Connected to the Banjo Tooie Client!");
            print("Connected!")
            curstate = STATE_OK
        end

        l, e = btSocket:receive()
        -- Handle incoming message
        if e == 'closed' then
            if curstate == STATE_OK then
                archipelago_msg_box("Connection closed")
                print("Connection closed")
            end
            curstate = STATE_UNINITIALIZED
            return
        elseif e == 'timeout' then
            archipelago_msg_box("timeout")
            print("timeout")
            return
        elseif e ~= nil then
            print(e)
            curstate = STATE_UNINITIALIZED
            return
        end
        process_block(json.decode(l))


        if isBanjoDed == true
        then
            isBanjoDed = false;
        end
    end
end

function checkPause()
    local pause_menu = mainmemory.readbyte(0x15961A);
    if pause_menu == 1 and isPaused == false 
    then
        if DEBUG == true
        then
            print("Game Paused");
        end
        BMMBackup();
        useAGI();
        isPaused = true;
    elseif pause_menu == 0 and isPaused == true  -- unpaused
    then
        isPaused = false
        if DEBUG == true
        then
            print("Game Unpaused");
        end
        if last_map ~= 335 and last_map ~= 337  -- Don't want to restore while in WH zone
        then
            BMMRestore()
        end
    elseif isPaused == true and DEBUG == true
    then
        local check_controls = joypad.get()
        if check_controls ~= nil and check_controls['P1 Z'] == true
        then
            print("AGI TABLE:");
            for item_group, table in pairs(AGI)
            do
                for location, value in pairs(table)
                do
                    if(value == true)
                    then
                        print(location .. ":" .. tostring(value))
                    end
                end
            end
        elseif check_controls ~= nil and check_controls['P1 C Right'] == true
        then
            print("BMM TABLE:");
            for item_group, table in pairs(BMM)
            do
                for location, value in pairs(table)
                do
                    if(value == true)
                    then
                        print(location .. ":" .. tostring(value))
                    end
                end
            end
        elseif check_controls ~= nil and check_controls['P1 C Left'] == true
        then
            print("AMM TABLE:");
            for item_group, table in pairs(AMM)
            do
                for location, value in pairs(table)
                do
                    if(value == true)
                    then
                        print(location .. ":" .. tostring(value))
                    end
                end
            end
        elseif check_controls ~= nil and check_controls['P1 C Up'] == true
        then
            print("BKM TABLE + Actual:");
            for location, values in pairs(MASTER_MAP["MOVES"])
            do
                print("AMM:");
                local res = checkFlag(values['addr'], values['bit']);
                print(location .. ":" .. tostring(res))
                print("Checked? : " .. tostring(BKM[location]))
                print("------------------------");
            end
        end
    end
end

function checkTotalMenu()
    if isPaused == false
    then
        return
    else
        local total = mainmemory.readbyte(0x123C48);
        if checkTotals == false and total == 1
        then
            if DEBUG == true
            then
                print("Checking Game Totals");
            end
            checkTotals = true;
            BMMRestore();
        elseif checkTotals == true and total ~= 1
        then
            if DEBUG == true
            then
                print("no longer checking Game Totals");
            end
            checkTotals = false;
            BMMBackup();
            useAGI();
        end
    end
end

function savingAGI()
    local f = io.open("BT" .. player_name .. "_" .. seed .. ".AGI", "w") --generate #BTplayer_seed.AGI
    f:write(json.encode(AGI) .. "\n");
    f:write(json.encode(receive_map))
    f:close()
    if DEBUG == true
    then
        print("AGI Table Saved");
    end
end

function savingBMM()
    local f = io.open("BT" .. player_name .. "_" .. seed .. ".BMM", "w") --generate #BTplayer_seed.AGI
    f:write(json.encode(BMM) .. "\n");
    f:write(json.encode(BKM));
    f:close()
    if DEBUG == true
    then
        print("BMM Table Saved");
    end
end

function gameSaving()
    if isPaused ~= true
    then
        return
    else
        local save_game = mainmemory.read_u8(0x05F450);
        local save_game2 = mainmemory.read_u8(0x044A81);
        if save_game == 1 or save_game2 == 1
        then
            isSaving = true
            if DEBUG == true
            then
                print("Game Entering Save State")
            end
        end
    end
end

function moveEnemytoBK()
    local enemy = checkModel("enemy");
    if enemy == false
    then
        return
    end

    pos = getBanjoPos();
    if pos == false
    then
        return
    end

	mainmemory.writefloat(enemy + 0x04, pos["Xpos"], true);
    mainmemory.writefloat(enemy + 0x08, pos["Ypos"], true);
    mainmemory.writefloat(enemy + 0x0C, pos["Zpos"], true);

    killBTFlag = false --TODO - TEST
    -- print("Object Distance:")
    -- print(playerDist)
end

function killBT()
    if killBTFlag == true then
        setCurrentHealth(0)
        moveEnemytoBK()
    end
end

function getSlotData()
    local retTable = {}
    retTable["getSlot"] = true;
 
    msg = json.encode(retTable).."\n"
    local ret, error = btSocket:send(msg)

    l, e = btSocket:receive()
    -- Handle incoming message
    if e == 'closed' then
        if curstate == STATE_OK then
            archipelago_msg_box("Connection closed")
            print("Connection closed")
        end
        curstate = STATE_UNINITIALIZED
        return
    elseif e == 'timeout' then
        archipelago_msg_box("timeout")
        print("timeout")
        return
    elseif e ~= nil then
        print(e)
        curstate = STATE_UNINITIALIZED
        return
    end
    process_slot(json.decode(l))
end

function process_slot(block)
    
    if DEBUGLVL2 == true then
        print(block)
    end

    if block['slot_player'] ~= nil and block['slot_player'] ~= ""
    then
        player_name = block['slot_player']
    end
    if block['slot_seed'] ~= nil and block['slot_seed'] ~= ""
    then
        seed = block['slot_seed']
    end
    if block['slot_deathlink'] ~= nil and block['slot_deathlink'] ~= "false"
    then
        deathlink = true
    end
    if block['slot_skip_tot'] ~= nil and block['slot_skip_tot'] ~= ""
    then
        skip_tot = block['slot_skip_tot']
    end
    if block['slot_honeycomb'] ~= nil and block['slot_honeycomb'] ~= "false"
    then
        multiHoneycomb = true
    end
	if block['slot_pages'] ~= nil and block['slot_pages'] ~= "false"
    then
        multiPages = true
    end
    if block['slot_moves'] ~= nil and block['slot_moves'] ~= "false"
    then
        APMovesEnabled = true
    end

    if seed ~= 0
    then
        local f = io.open("BT" .. player_name .. "_" .. seed .. ".AGI", "r") --generate #BTplayer_seed.AGI
        if f==nil then
            all_location_checks("AGI")
            AGI["MOVES"] = init_BMK("AGI");
            f = io.open("BT" .. player_name .. "_" .. seed .. ".AGI", "w")
            f:write(json.encode(AGI))
            f:close()
        else
            AGI = json.decode(f:read("l"))
            receive_map = json.decode(f:read("l"))
            f:close()
        end
    else
        return false
    end
    return true
end

function initializeFlags()
	-- Use Cutscene: "2 Years Have Passed..." to check for fresh save
	local current_map = getMap();
	if (current_map == 0xA1) then
		-- First Time Pickup Text
		for i = 0, 7 do
			setFlag(0x00, i) -- Note, Glowbo, Eggs, Feathers, Treble Clef, Honeycomb
		end	
		setFlag(0x01, 2) -- Empty Honeycomb
		setFlag(0x01, 5) -- Jinjo
		setFlag(0x07, 7) -- Cheato Page
		setFlag(0x27, 5) -- Doubloon
		setFlag(0x2E, 7) -- Ticket
		-- Character Introduction Text
		for k,v in pairs(MASTER_MAP['SKIP']['INTRO'])
        do
            setFlag(v['addr'], v['bit'])
        end
		-- Cutscene Flags
		for k,v in pairs(MASTER_MAP['SKIP']['CUTSCENE'])
        do
            setFlag(v['addr'], v['bit'])
        end
		-- Tutorial Dialogues
		for k,v in pairs(MASTER_MAP['SKIP']['TUTORIAL'])
        do
            setFlag(v['addr'], v['bit'])
        end
		-- Kickball Stadium Doors
		setFlag(0xA9, 6) -- MT
		setFlag(0xA9, 7) -- HFP
		
        BMMLoaded = true  -- We don't have a real BMM at this point.  
        init_BMK("BKM")
		if (skip_tot ~= "false") then
			-- ToT Misc Flags
			setFlag(0xAB, 2)
			setFlag(0xAB, 3)
			setFlag(0xAB, 4)
			setFlag(0xAB, 5)
			if (skip_tot == "true") then
			-- ToT Complete Flags
				setFlag(0x83, 0)
				setFlag(0x83, 4)
			else
				setFlag(0x83, 2)
				setFlag(0x83, 3)
			end
		end
        all_location_checks("AMM")
        BMMBackup()
        BMMRestore()
		flag_init_complete = true
	-- Otherwise, the flags were already set, so just stop checking
	elseif (current_map == 0xAF or current_map == 0x142) then
		flag_init_complete = true
	end
end

function setToTComplete()
	-- this fixes a bug that messes up game progression
	current_map = getMap();
	if (current_map == 0x15E and checkFlag(0x83, 1) == false) then -- CK Klungo Boss Room
		setFlag(0x83, 1)
	end
end

function saveGame()
    BMMBackup();
    BMMLoaded = false;
    isSaving = false;
end

function main()
    if not checkBizHawkVersion() then
        return
    end
    server, error = socket.bind('localhost', 21221)

    while true do
        frame = frame + 1
        if not (curstate == prevstate) then
            prevstate = curstate
        end
        if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            if (frame % 60 == 0) then
                --getBanjoDeathAnimation(false);
                receive();
                killBT();
                if (skip_tot == "true") then
					setToTComplete();
				end
                if isSaving == true
                then
                    saveGame();
                end
                if NeedSiloState == true
                then
                    if DEBUG == true
                    then
                        print("clearing all AMM moves")
                    end
                    clear_AMM_MOVES_checks()
                    getSiloPlayerModel()
                end
                gameSaving();
            elseif (frame % 10 == 0)
            then
                checkPause();
                checkTotalMenu();
                if not (flag_init_complete) then
					initializeFlags();
				end
                if WatchSilo == true
                then
                    nearSilo()
                end
            end
        elseif (curstate == STATE_UNINITIALIZED) then
            if  (frame % 60 == 0) then
                server:settimeout(2)
                local client, timeout = server:accept()
                if timeout == nil then
                    print('Initial Connection Made')
                    curstate = STATE_INITIAL_CONNECTION_MADE
                    btSocket = client
                    btSocket:settimeout(0)
                else
                    archipelago_msg_box('Connection failed, ensure Banjo Tooie Client is running, connected and rerun banjotooie_connector.lua')
                    print('Connection failed, ensure Banjo Tooie Client is running, connected and rerun banjotooie_connector.lua')
                    return
                end
            end
        end
        emu.frameadvance()
    end
end

main()
