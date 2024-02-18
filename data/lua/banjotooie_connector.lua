-- Banjo Tooie Connector Lua
-- Created by Mike Jackson (jjjj12212) 
-- with the help of Rose (Oktorose), the OOT Archipelago team, ScriptHawk BT.lua & kaptainkohl for BTrando.lua 

local socket = require("socket")
local json = require('json')
local math = require('math')
require('common')

local last_modified_date = '2024-01-19' -- Should be the last modified date
local script_version = 3
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


-- Relative to Position object
local x_pos = 0x00;
local y_pos = x_pos + 4;
local z_pos = y_pos + 4;

local grounded_pointer_index = 84 * 4;
local position_pointer_index = 57 * 4;

local slot_base = 0x10;
local slot_size = 0x9C;

-- EO BTRando

local isPaused = false;
local checkTotals = false;
local isSaving = false;
local isBackup = false;
local altarClose = false;
local killBTFlag = false;
local isBanjoDed = false;
local isBanjoDedCheck = false;

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
    ["Mingy Jongo"] = 0x816
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
    elseif playerDist >=301 and altarClose == true and isBackup == true
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
        if isBackup == false
        then
            BMMBackup()
            useAGI()
        end
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

    if playerDist <= 400 and isBackup == true
    then
        if DEBUG == true
        then
            print("Near Jinjo");
        end
        BMMRestore();
    end
end

-- BMM - Backup Memory Map 
local BMM =  {};

-- AMM - Actual Memory Map
local AMM = {};

-- AGI - Archipelago given items
local AGI = {};

local MASTER_MAP = {
    ['JV'] = {
        ['Jinjo Village: White Jinjo Family Jiggy'] = {
            ['addr'] = 0x4F,
            ['bit'] = 0,
            ['locationId'] = 1230676
        },
        ['Jinjo Village: Orange Jinjo Family Jiggy'] = {
            ['addr'] = 0x4F,
            ['bit'] = 1,
            ['locationId'] = 1230677
        },
        ['Jinjo Village: Yellow Jinjo Family Jiggy'] = {
            ['addr'] = 0x4F,
            ['bit'] = 2,
            ['locationId'] = 1230678
        },
        ['Jinjo Village: Brown Jinjo Family Jiggy'] = {
            ['addr'] = 0x4F,
            ['bit'] = 3,
            ['locationId'] = 1230679
        },
        ['Jinjo Village: Green Jinjo Family Jiggy'] = {
            ['addr'] = 0x4F,
            ['bit'] = 4,
            ['locationId'] = 1230680
        },
        ['Jinjo Village: Red Jinjo Family Jiggy'] = {
            ['addr'] = 0x4F,
            ['bit'] = 5,
            ['locationId'] = 1230681
        },
        ['Jinjo Village: Blue Jinjo Family Jiggy'] = {
            ['addr'] = 0x4F,
            ['bit'] = 6,
            ['locationId'] = 1230682
        },
        ['Jinjo Village: Purple Jinjo Family Jiggy'] = {
            ['addr'] = 0x4F,
            ['bit'] = 7,
            ['locationId'] = 1230683
        },
        ['Jinjo Village: Black Jinjo Family Jiggy'] = {
            ['addr'] = 0x50,
            ['bit'] = 0,
            ['locationId'] = 1230684
        },
        ['Jinjo Village: King Jingaling Jiggy'] = {
            ['addr'] = 0x50,
            ['bit'] = 1,
            ['locationId'] = 1230685
        },
    },
    ['WH'] = {
        -- ['Wooded Hollow: Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230591
        -- }
    },
    ['SM'] = {
        -- ['Spiral Mountain: Cheato Page'] = {
        --     ['addr'] = 0x59,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230752
        -- },
        -- ['Spiral Mountain: Jinjo'] = {
        --     ['addr'] = 0x3F,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230595
        -- }
    },
    ['PL'] = {
        -- ['Plateau: Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230594
        -- },
        ['Plateau: Honeycomb'] = {
            ['addr'] = 0x42,
            ['bit'] = 2,
            ['locationId'] = 1230727
        }
    },
    ['MT'] = {
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
        ['Mayahem Temple: Targitzan Jiggy'] = {
            ['addr'] = 0x45,
            ['bit'] = 0,
            ['locationId'] = 1230596
        },
        ['Mayahem Temple: Targitzan S. Sacred Chamber Jiggy'] = {
            ['addr'] = 0x45,
            ['bit'] = 1,
            ['locationId'] = 1230597
        },
        ['Mayahem Temple: Kickball Jiggy'] = {
            ['addr'] = 0x45,
            ['bit'] = 2,
            ['locationId'] = 1230598
        },
        ['Mayahem Temple: Bovina Jiggy'] = {
            ['addr'] = 0x45,
            ['bit'] = 3,
            ['locationId'] = 1230599
        },
        ['Mayahem Temple: Treasure Chamber Jiggy'] = {
            ['addr'] = 0x45,
            ['bit'] = 4,
            ['locationId'] = 1230600
        },
        ['Mayahem Temple: Golden Goliath Jiggy'] = {
            ['addr'] = 0x45,
            ['bit'] = 5,
            ['locationId'] = 1230601
        },
        ['Mayahem Temple: Prison Compound Quicksand Jiggy'] = {
            ['addr'] = 0x45,
            ['bit'] = 6,
            ['locationId'] = 1230602
        },
        ['Mayahem Temple: Pillars Jiggy'] = {
            ['addr'] = 0x45,
            ['bit'] = 7,
            ['locationId'] = 1230603
        },
        ['Mayahem Temple: Top of Temple Jiggy'] = {
            ['addr'] = 0x46,
            ['bit'] = 0,
            ['locationId'] = 1230604
        },
        ['Mayahem Temple: Ssslumber Jiggy'] = {
            ['addr'] = 0x46,
            ['bit'] = 1,
            ['locationId'] = 1230605
        },
        -- ['Mayahem Temple: Mumbo Skull Glowbo'] = {
        --     ['addr'] = 0x42,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230686
        -- },
        -- ['Mayahem Temple: Behind Wumba Wigwam Glowbo'] = {
        --     ['addr'] = 0x43,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230687
        -- },
        ['Mayahem Temple: Entrance Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 2,
            ['locationId'] = 1230703
        },
        ['Mayahem Temple: Bovina Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 3,
            ['locationId'] = 1230704
        },
        ['Mayahem Temple: Treasure Chamber Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 4,
            ['locationId'] = 1230705
        },
        -- ['Mayahem Temple: Snake Head Cheato Page'] = {
        --     ['addr'] = 0x56,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230728
        -- },
        -- ['Mayahem Temple: Prison Compound Cheato Page'] = {
        --     ['addr'] = 0x56,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230729
        -- },
        -- ['Mayahem Temple: Jade Snake Grove Cheato Page'] = {
        --     ['addr'] = 0x56,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230730
        -- },
    },
    ['GM'] = {
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
        ['Glitter Gultch Mine: King Coal Jiggy'] = {
            ['addr'] = 0x46,
            ['bit'] = 2,
            ['locationId'] = 1230606
        },
        ['Glitter Gultch Mine: Canary Mary Jiggy'] = {
            ['addr'] = 0x46,
            ['bit'] = 3,
            ['locationId'] = 1230607
        },
        ['Glitter Gultch Mine: Generator Cavern Jiggy'] = {
            ['addr'] = 0x46,
            ['bit'] = 4,
            ['locationId'] = 1230608
        },
        ['Glitter Gultch Mine: Waterfall Cavern Jiggy'] = {
            ['addr'] = 0x46,
            ['bit'] = 5,
            ['locationId'] = 1230609
        },
        ['Glitter Gultch Mine: Ordnance Storage Jiggy'] = {
            ['addr'] = 0x46,
            ['bit'] = 6,
            ['locationId'] = 1230610
        },
        ['Glitter Gultch Mine: Dilberta Jiggy'] = {
            ['addr'] = 0x46,
            ['bit'] = 7,
            ['locationId'] = 1230611
        },
        ['Glitter Gultch Mine: Crushing Shed Jiggy'] = {
            ['addr'] = 0x47,
            ['bit'] = 0,
            ['locationId'] = 1230612
        },
        ['Glitter Gultch Mine: Waterfall Jiggy'] = {
            ['addr'] = 0x47,
            ['bit'] = 1,
            ['locationId'] = 1230613
        },
        ['Glitter Gultch Mine: Power Hut Basement Jiggy'] = {
            ['addr'] = 0x47,
            ['bit'] = 2,
            ['locationId'] = 1230614
        },
        ['Glitter Gultch Mine: Flooded Caves Jiggy'] = {
            ['addr'] = 0x47,
            ['bit'] = 3,
            ['locationId'] = 1230615
        },
        -- ['Glitter Gultch Mine: Near Entrance Glowbo'] = {
        --     ['addr'] = 0x43,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230688
        -- },
        -- ['Glitter Gultch Mine: Mine Entrance Glowbo'] = {
        --     ['addr'] = 0x43,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230689
        -- },
        ['Glitter Gultch Mine: Toxic Gas Cave Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 5,
            ['locationId'] = 1230706
        },
        ['Glitter Gultch Mine: Boulder Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 6,
            ['locationId'] = 1230707
        },
        ['Glitter Gultch Mine: Train Station Honeycomb'] = {
            ['addr'] = 0x3F,
            ['bit'] = 7,
            ['locationId'] = 1230708
        },
        -- ['Glitter Gultch Mine: Canary Mary Cheato Page'] = {
        --     ['addr'] = 0x56,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230731
        -- },
        -- ['Glitter Gultch Mine: Entrance Cheato Page'] = {
        --     ['addr'] = 0x56,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230732
        -- },
        -- ['Glitter Gultch Mine: Water Storage Cheato Page'] = {
        --     ['addr'] = 0x57,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230733
        -- },
    },
    ['WW'] = {
        -- ['Witchy World: Big Top Jinjo'] = {
        --     ['addr'] = 0x3A,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230561
        -- },
        -- ['Witchy World: Cave of Horrors Jinjo'] = {
        --     ['addr'] = 0x3A,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230562
        -- },
        -- ['Witchy World: Van Door Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230563
        -- },
        -- ['Witchy World: Dodgem Dome Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230564
        -- },
        -- ['Witchy World: Cactus of Strength Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230565
        -- },
        ['Witchy World: Hoop Hurry Jiggy'] = {
            ['addr'] = 0x47,
            ['bit'] = 4,
            ['locationId'] = 1230616
        },
        ['Witchy World: Dodgem Jiggy'] = {
            ['addr'] = 0x47,
            ['bit'] = 5,
            ['locationId'] = 1230617
        },
        ['Witchy World: Mr Patches Jiggy'] = {
            ['addr'] = 0x47,
            ['bit'] = 6,
            ['locationId'] = 1230618
        },
        ['Witchy World: Saucer of Peril Jiggy'] = {
            ['addr'] = 0x47,
            ['bit'] = 7,
            ['locationId'] = 1230619
        },
        ['Witchy World: Ballon Burst Jiggy'] = {
            ['addr'] = 0x48,
            ['bit'] = 0,
            ['locationId'] = 1230620
        },
        ['Witchy World: Dive of Death Jiggy'] = {
            ['addr'] = 0x48,
            ['bit'] = 1,
            ['locationId'] = 1230621
        },
        ['Witchy World: Mrs Boggy Jiggy'] = {
            ['addr'] = 0x48,
            ['bit'] = 2,
            ['locationId'] = 1230622
        },
        ['Witchy World: Star Spinner Jiggy'] = {
            ['addr'] = 0x48,
            ['bit'] = 3,
            ['locationId'] = 1230623
        },
        ['Witchy World: The Inferno Jiggy'] = {
            ['addr'] = 0x48,
            ['bit'] = 4,
            ['locationId'] = 1230624
        },
        ['Witchy World: Cactus of Strength Jiggy'] = {
            ['addr'] = 0x48,
            ['bit'] = 5,
            ['locationId'] = 1230625
        },
        -- ['Witchy World: The Inferno Glowbo'] = {
        --     ['addr'] = 0x43,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230690
        -- },
        -- ['Witchy World: Inside Wumba Wigwam Glowbo'] = {
        --     ['addr'] = 0x43,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230691
        -- },
        ['Witchy World: Space Zone Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 0,
            ['locationId'] = 1230709
        },
        ['Witchy World: Mumbo Skull Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 1,
            ['locationId'] = 1230710
        },
        ['Witchy World: Crazy Castle Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 2,
            ['locationId'] = 1230711
        },
        -- ['Witchy World: Haunted Cavern Cheato Page'] = {
        --     ['addr'] = 0x57,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230734
        -- },
        -- ['Witchy World: The Inferno Cheato Page'] = {
        --     ['addr'] = 0x57,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230735
        -- },
        -- ['Witchy World: Saucer of Peril Cheato Page'] = {
        --     ['addr'] = 0x57,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230736
        -- },
    },
    ['CT'] = {
        -- ['Cliff Top: Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230593
        -- },
        -- ['Cliff Top: Glowbo'] = {
        --     ['addr'] = 0x44,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230702
        -- },
    },
    ['JR'] = {
        -- ['Jolly Rodgers: Town Center Pole 1 Doubloon'] = {
        --     ['addr'] = 0x22,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230521
        -- },
        -- ['Jolly Rodgers: Town Center Pole 2 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230522
        -- },
        -- ['Jolly Rodgers: Town Center Pole 3 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230523
        -- },
        -- ['Jolly Rodgers: Town Center Pole 4 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230524
        -- },
        -- ['Jolly Rodgers: Town Center Pole 5 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230525
        -- },
        -- ['Jolly Rodgers: Town Center Pole 6 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230526
        -- },
        -- ['Jolly Rodgers: Silo 1 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230527
        -- },
        -- ['Jolly Rodgers: Silo 2 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230528
        -- },
        -- ['Jolly Rodgers: Silo 3 Doubloon'] = {
        --     ['addr'] = 0x23,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230529
        -- },
        -- ['Jolly Rodgers: Silo 4 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230530
        -- },
        -- ['Jolly Rodgers: Toxic Pool 1 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230531
        -- },
        -- ['Jolly Rodgers: Toxic Pool 2 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230532
        -- },
        -- ['Jolly Rodgers: Toxic Pool 3 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230533
        -- },
        -- ['Jolly Rodgers: Toxic Pool 4 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230534
        -- },
        -- ['Jolly Rodgers: Mumbo Skull 1 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230535
        -- },
        -- ['Jolly Rodgers: Mumbo Skull 2 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230536
        -- },
        -- ['Jolly Rodgers: Mumbo Skull 3 Doubloon'] = {
        --     ['addr'] = 0x24,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230537
        -- },
        -- ['Jolly Rodgers: Mumbo Skull 4 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230538
        -- },
        -- ['Jolly Rodgers: Underground 1 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230539
        -- },
        -- ['Jolly Rodgers: Underground 2 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230540
        -- },
        -- ['Jolly Rodgers: Underground 3 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230541
        -- },
        -- ['Jolly Rodgers: Alcove 1 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230542
        -- },
        -- ['Jolly Rodgers: Alcove 2 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230543
        -- },
        -- ['Jolly Rodgers: Alcove 3 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230544
        -- },
        -- ['Jolly Rodgers: Capt Blackeye 1 Doubloon'] = {
        --     ['addr'] = 0x25,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230545
        -- },
        -- ['Jolly Rodgers: Capt Blackeye 2 Doubloon'] = {
        --     ['addr'] = 0x26,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230546
        -- },
        -- ['Jolly Rodgers: Near Jinjo 1 Doubloon'] = {
        --     ['addr'] = 0x26,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230547
        -- },
        -- ['Jolly Rodgers: Near Jinjo 2 Doubloon'] = {
        --     ['addr'] = 0x26,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230548
        -- },
        -- ['Jolly Rodgers: Near Jinjo 3 Doubloon'] = {
        --     ['addr'] = 0x26,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230549
        -- },
        -- ['Jolly Rodgers: Near Jinjo 4 Doubloon'] = {
        --     ['addr'] = 0x26,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230550
        -- },
        -- ['Jolly Rodgers: Lagoon Alcove Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230566
        -- },
        -- ['Jolly Rodgers: Blubber Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230567
        -- },
        -- ['Jolly Rodgers: Big Fish Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230568
        -- },
        -- ['Jolly Rodgers: Seaweed Sanctum Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230569
        -- },
        -- ['Jolly Rodgers: Sunken Ship Jinjo'] = {
        --     ['addr'] = 0x3B,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230570
        -- },
        ['Jolly Rodgers: Mini-Sub Challenge Jiggy'] = {
            ['addr'] = 0x48,
            ['bit'] = 6,
            ['locationId'] = 1230626
        },
        ['Jolly Rodgers: Tiptup Jiggy'] = {
            ['addr'] = 0x48,
            ['bit'] = 7,
            ['locationId'] = 1230627
        },
        ['Jolly Rodgers: Chris Bacon Jiggy'] = {
            ['addr'] = 0x49,
            ['bit'] = 0,
            ['locationId'] = 1230628
        },
        ['Jolly Rodgers: Piglets Pool Jiggy'] = {
            ['addr'] = 0x49,
            ['bit'] = 1,
            ['locationId'] = 1230629
        },
        ['Jolly Rodgers: Smugglers Cavern Jiggy'] = {
            ['addr'] = 0x49,
            ['bit'] = 2,
            ['locationId'] = 1230630
        },
        ['Jolly Rodgers: Merry Maggie Jiggy'] = {
            ['addr'] = 0x49,
            ['bit'] = 3,
            ['locationId'] = 1230631
        },
        ['Jolly Rodgers: Woo Fak Fak Jiggy'] = {
            ['addr'] = 0x49,
            ['bit'] = 4,
            ['locationId'] = 1230632
        },
        ['Jolly Rodgers: Seemee Jiggy'] = {
            ['addr'] = 0x49,
            ['bit'] = 5,
            ['locationId'] = 1230633
        },
        ['Jolly Rodgers: Pawno Jiggy'] = {
            ['addr'] = 0x49,
            ['bit'] = 6,
            ['locationId'] = 1230634
        },
        ['Jolly Rodgers: UFO Jiggy'] = {
            ['addr'] = 0x49,
            ['bit'] = 7,
            ['locationId'] = 1230635
        },
        -- ['Jolly Rodgers: Pawnos Emporium Glowbo'] = {
        --     ['addr'] = 0x43,
        --     ['bit'] = 5,
        --     ['locationId'] = 123069
        -- },
        -- ['Jolly Rodgers: Under Wumba Wigwam Glowbo'] = {
        --     ['addr'] = 0x43,
        --     ['bit'] = 6,
        --     ['locationId'] = 123070
        -- },
        ['Jolly Rodgers: Seemee Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 3,
            ['locationId'] = 1230712
        },
        ['Jolly Rodgers: Atlantis Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 4,
            ['locationId'] = 1230713
        },
        ['Jolly Rodgers: Waste Pipe Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 5,
            ['locationId'] = 1230714
        },
        -- ['Jolly Rodgers: Pawnos Cheato Page'] = {
        --     ['addr'] = 0x57,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230737
        -- },
        -- ['Jolly Rodgers: Seemee Cheato Page'] = {
        --     ['addr'] = 0x57,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230738
        -- },
        -- ['Jolly Rodgers: Ancient Baths Cheato Page'] = {
        --     ['addr'] = 0x57,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230739
        -- },
    },
    ['WL'] = {
        -- ['Wasteland: Jinjo'] = {
        --     ['addr'] = 0x3E,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230592
        -- },
    },
    ['TL'] = {
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
        ['Terrydactyland: Under Terrys Nest Jiggy'] = {
            ['addr'] = 0x4A,
            ['bit'] = 0,
            ['locationId'] = 1230636
        },
        ['Terrydactyland: Dippy Jiggy'] = {
            ['addr'] = 0x4A,
            ['bit'] = 1,
            ['locationId'] = 1230637
        },
        ['Terrydactyland: Scrotty Jiggy'] = {
            ['addr'] = 0x4A,
            ['bit'] = 2,
            ['locationId'] = 1230638
        },
        ['Terrydactyland: Terrys Jiggy'] = {
            ['addr'] = 0x4A,
            ['bit'] = 3,
            ['locationId'] = 1230639
        },
        ['Terrydactyland: Oogle Boogle Tribe Jiggy'] = {
            ['addr'] = 0x4A,
            ['bit'] = 4,
            ['locationId'] = 1230640
        },
        ['Terrydactyland: Chompas Belly Jiggy'] = {
            ['addr'] = 0x4A,
            ['bit'] = 5,
            ['locationId'] = 1230641
        },
        ['Terrydactyland: Terrys Hatched Jiggy'] = {
            ['addr'] = 0x4A,
            ['bit'] = 6,
            ['locationId'] = 1230642
        },
        ['Terrydactyland: Stomping Plains Jiggy'] = {
            ['addr'] = 0x4A,
            ['bit'] = 7,
            ['locationId'] = 1230643
        },
        ['Terrydactyland: Rocknut Tribe Jiggy'] = {
            ['addr'] = 0x4B,
            ['bit'] = 0,
            ['locationId'] = 1230644
        },
        ['Terrydactyland: Code of the Dinosaurs Jiggy'] = {
            ['addr'] = 0x4B,
            ['bit'] = 1,
            ['locationId'] = 1230645
        },
        -- ['Terrydactyland: Unga Bunga Cave Entrance Glowbo'] = {
        --     ['addr'] = 0x43,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230694
        -- },
        -- ['Terrydactyland: Behind Mumbo Skull Glowbo'] = {
        --     ['addr'] = 0x44,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230695
        -- },
        ['Terrydactyland: Central Area Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 6,
            ['locationId'] = 1230715
        },
        ['Terrydactyland: S. Family Cave Honeycomb'] = {
            ['addr'] = 0x40,
            ['bit'] = 7,
            ['locationId'] = 1230716
        },
        ['Terrydactyland: River Passage Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 0,
            ['locationId'] = 1230717
        },
        -- ['Terrydactyland: Dippys Pool Cheato Page'] = {
        --     ['addr'] = 0x57,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230740
        -- },
        -- ['Terrydactyland: Inside the Mountain Cheato Page'] = {
        --     ['addr'] = 0x58,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230741
        -- },
        -- ['Terrydactyland: Boulder Cheato Page'] = {
        --     ['addr'] = 0x58,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230742
        -- }
    },
    ['GI'] = {
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
        -- ['Gruntys Industries: Toxic Waste Jinjo'] = {
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
        ['Gruntys Industries: Waste Disposal Jiggy'] = {
            ['addr'] = 0x4B,
            ['bit'] = 2,
            ['locationId'] = 1230646
        },
        ['Gruntys Industries: Weldar Jiggy'] = {
            ['addr'] = 0x4B,
            ['bit'] = 3,
            ['locationId'] = 1230647
        },
        ['Gruntys Industries: Clinkers Cavern Jiggy'] = {
            ['addr'] = 0x4B,
            ['bit'] = 4,
            ['locationId'] = 1230648
        },
        ['Gruntys Industries: Laundry Jiggy'] = {
            ['addr'] = 0x4B,
            ['bit'] = 5,
            ['locationId'] = 1230649
        },
        ['Gruntys Industries: Floor 5 Jiggy'] = {
            ['addr'] = 0x4B,
            ['bit'] = 6,
            ['locationId'] = 1230650
        },
        ['Gruntys Industries: Quality Control Jiggy'] = {
            ['addr'] = 0x4B,
            ['bit'] = 7,
            ['locationId'] = 1230651
        },
        ['Gruntys Industries: Floor 1 Guarded Jiggy'] = {
            ['addr'] = 0x4C,
            ['bit'] = 0,
            ['locationId'] = 1230652
        },
        ['Gruntys Industries: Trash Compactor Jiggy'] = {
            ['addr'] = 0x4C,
            ['bit'] = 1,
            ['locationId'] = 1230653
        },
        ['Gruntys Industries: Packing Room Jiggy'] = {
            ['addr'] = 0x4C,
            ['bit'] = 2,
            ['locationId'] = 1230654
        },
        ['Gruntys Industries: Waste Disposal Box Jiggy'] = {
            ['addr'] = 0x4C,
            ['bit'] = 3,
            ['locationId'] = 1230655
        },
        -- ['Gruntys Industries: Floor 2 Glowbo'] = {
        --     ['addr'] = 0x44,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230696
        -- },
        -- ['Gruntys Industries: Floor 3 Glowbo'] = {
        --     ['addr'] = 0x44,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230697
        -- },
        ['Gruntys Industries: Floor 3 Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 1,
            ['locationId'] = 1230718
        },
        ['Gruntys Industries: Train Station Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 2,
            ['locationId'] = 1230719
        },
        ['Gruntys Industries: Chimney Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 3,
            ['locationId'] = 1230720
        },
        -- ['Gruntys Industries: Logo Cheato Page'] = {
        --     ['addr'] = 0x58,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230743
        -- },
        -- ['Gruntys Industries: Floor 2 Cheato Page'] = {
        --     ['addr'] = 0x58,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230744
        -- },
        -- ['Gruntys Industries: Repair Depot Cheato Page'] = {
        --     ['addr'] = 0x58,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230745
        -- },
    },
    ['HP'] = {
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
        ['Hailfire Peaks: Dragon Brothers Jiggy'] = {
            ['addr'] = 0x4C,
            ['bit'] = 4,
            ['locationId'] = 1230656
        },
        ['Hailfire Peaks: Inside the Volcano Jiggy'] = {
            ['addr'] = 0x4C,
            ['bit'] = 5,
            ['locationId'] = 1230657
        },
        ['Hailfire Peaks: Sabreman Jiggy'] = {
            ['addr'] = 0x4C,
            ['bit'] = 6,
            ['locationId'] = 1230658
        },
        ['Hailfire Peaks: Boggy Jiggy'] = {
            ['addr'] = 0x4C,
            ['bit'] = 7,
            ['locationId'] = 1230659
        },
        ['Hailfire Peaks: Icy Side Station Jiggy'] = {
            ['addr'] = 0x4D,
            ['bit'] = 0,
            ['locationId'] = 1230660
        },
        ['Hailfire Peaks: Oil Drill Jiggy'] = {
            ['addr'] = 0x4D,
            ['bit'] = 1,
            ['locationId'] = 1230661
        },
        ['Hailfire Peaks: Stomping Plains C. Jiggy'] = {
            ['addr'] = 0x4D,
            ['bit'] = 2,
            ['locationId'] = 1230662
        },
        ['Hailfire Peaks: Kickball Jiggy'] = {
            ['addr'] = 0x4D,
            ['bit'] = 3,
            ['locationId'] = 1230663
        },
        ['Hailfire Peaks: Aliens Jiggy'] = {
            ['addr'] = 0x4D,
            ['bit'] = 4,
            ['locationId'] = 1230664
        },
        ['Hailfire Peaks: Lava Waterfall Jiggy'] = {
            ['addr'] = 0x4D,
            ['bit'] = 5,
            ['locationId'] = 1230665
        },
        -- ['Hailfire Peaks: Lava Side Glowbo'] = {
        --     ['addr'] = 0x44,
        --     ['bit'] = 3,
        --     ['locationId'] = 1230698
        -- },
        -- ['Hailfire Peaks: Icy Side Glowbo'] = {
        --     ['addr'] = 0x44,
        --     ['bit'] = 4,
        --     ['locationId'] = 1230699
        -- },
        ['Hailfire Peaks: Inside the Volcano Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 4,
            ['locationId'] = 1230721
        },
        ['Hailfire Peaks: Train Station Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 5,
            ['locationId'] = 1230722
        },
        ['Hailfire Peaks: Lava Side Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 6,
            ['locationId'] = 1230723
        },
        -- ['Hailfire Peaks: Lava Side Cheato Page'] = {
        --     ['addr'] = 0x58,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230746
        -- },
        -- ['Hailfire Peaks: Icicle Grotto Cheato Page'] = {
        --     ['addr'] = 0x58,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230747
        -- },
        -- ['Hailfire Peaks: Icy Side Cheato Page'] = {
        --     ['addr'] = 0x58,
        --     ['bit'] = 7,
        --     ['locationId'] = 1230748
        -- },
    },
    ["CC"] = {
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
        ['Cloud Cuckcooland: Mingy Jongo Jiggy'] = {
            ['addr'] = 0x4D,
            ['bit'] = 6,
            ['locationId'] = 1230666
        },
        ['Cloud Cuckcooland: Mr Fit Jiggy'] = {
            ['addr'] = 0x4D,
            ['bit'] = 7,
            ['locationId'] = 1230667
        },
        ['Cloud Cuckcooland: Pot Ol Gold Jiggy'] = {
            ['addr'] = 0x4E,
            ['bit'] = 0,
            ['locationId'] = 1230668
        },
        ['Cloud Cuckcooland: Canary Mary Jiggy'] = {
            ['addr'] = 0x4E,
            ['bit'] = 1,
            ['locationId'] = 1230669
        },
        ['Cloud Cuckcooland: Zubbas Nest Jiggy'] = {
            ['addr'] = 0x4E,
            ['bit'] = 2,
            ['locationId'] = 1230670
        },
        ['Cloud Cuckcooland: Jiggium Plant Jiggy'] = {
            ['addr'] = 0x4E,
            ['bit'] = 3,
            ['locationId'] = 1230671
        },
        ['Cloud Cuckcooland: Cheese Wedge Jiggy'] = {
            ['addr'] = 0x4E,
            ['bit'] = 4,
            ['locationId'] = 1230672
        },
        ['Cloud Cuckcooland: Trash Can Jiggy'] = {
            ['addr'] = 0x4E,
            ['bit'] = 5,
            ['locationId'] = 1230673
        },
        ['Cloud Cuckcooland: Superstash Jiggy'] = {
            ['addr'] = 0x4E,
            ['bit'] = 6,
            ['locationId'] = 1230674
        },
        ['Cloud Cuckcooland: Jelly Castle Jiggy'] = {
            ['addr'] = 0x4E,
            ['bit'] = 7,
            ['locationId'] = 1230675
        },
        -- ['Cloud Cuckcooland: Overworld Glowbo'] = {
        --     ['addr'] = 0x44,
        --     ['bit'] = 5,
        --     ['locationId'] = 1230700
        -- },
        -- ['Cloud Cuckcooland: Central Cavern Glowbo'] = {
        --     ['addr'] = 0x44,
        --     ['bit'] = 6,
        --     ['locationId'] = 1230701
        -- },
        ['Cloud Cuckcooland: Underground Honeycomb'] = {
            ['addr'] = 0x41,
            ['bit'] = 7,
            ['locationId'] = 1230724
        },
        ['Cloud Cuckcooland: Trash Can Honeycomb'] = {
            ['addr'] = 0x42,
            ['bit'] = 0,
            ['locationId'] = 1230725
        },
        ['Cloud Cuckcooland: Pot Ol Gold Honeycomb'] = {
            ['addr'] = 0x42,
            ['bit'] = 1,
            ['locationId'] = 1230726
        },
        -- ['Cloud Cuckcooland: Canary Mary Cheato Page'] = {
        --     ['addr'] = 0x59,
        --     ['bit'] = 0,
        --     ['locationId'] = 1230749
        -- },
        -- ['Cloud Cuckcooland: Pot Ol Gold Cheato Page'] = {
        --     ['addr'] = 0x59,
        --     ['bit'] = 1,
        --     ['locationId'] = 1230750
        -- },
        -- ['Cloud Cuckcooland: Zubbas Nest Cheato Page'] = {
        --     ['addr'] = 0x59,
        --     ['bit'] = 2,
        --     ['locationId'] = 1230751
        -- },
    },
	  ["H1"] = {
	 	['Hag 1 Defeated'] = {
			['addr'] = 0x03,
			['bit'] = 3,
			['locationId'] = 1230027
		},
	}
}

local read_SM_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['SM'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['SM'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['SM']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['SM'])
        do
            checks[k] = false
        end
        AGI['SM'] = checks;
    end
    return checks;
end

local read_JV_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['JV'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['JV'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['JV']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['JV'])
        do
            checks[k] = false
        end
        AGI['JV'] = checks;
    end
    return checks
end

local read_WH_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['WH'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['WH'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['WH']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['WH'])
        do
            checks[k] = false
        end
        AGI['WH'] = checks;
    end
    return checks
end

local read_MT_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['MT'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['MT'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['MT']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['MT'])
        do
            checks[k] = false
        end
        AGI['MT'] = checks;
    end
    return checks
end

local read_PL_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['PL'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['PL'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['PL']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['PL'])
        do
            checks[k] = false
        end
        AGI['PL'] = checks;
    end
    return checks
end

local read_GM_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['GM'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['GM'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['GM']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['GM'])
        do
            checks[k] = false
        end
        AGI['GM'] = checks;
    end
    return checks
end

local read_WW_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['WW'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['WW'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['WW']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['WW'])
        do
            checks[k] = false
        end
        AGI['WW'] = checks;
    end
    return checks
end

local read_CT_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['CT'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['CT'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['CT']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['CT'])
        do
            checks[k] = false
        end
        AGI['CT'] = checks;
    end
    return checks
end

local read_JR_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['JR'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['JR'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['JR']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['JR'])
        do
            checks[k] = false
        end
        AGI['JR'] = checks;
    end
    return checks
end

local read_WL_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['WL'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['WL'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['WL']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['WL'])
        do
            checks[k] = false
        end
        AGI['WL'] = checks;
    end
    return checks
end

local read_TL_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['TL'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['TL'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['TL']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['TL'])
        do
            checks[k] = false
        end
        AGI['TL'] = checks;
    end
    return checks
end

local read_GI_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['GI'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['GI'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['GI']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['GI'])
        do
            checks[k] = false
        end
        AGI['GI'] = checks;
    end
    return checks
end

local read_HP_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['HP'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['HP'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['HP']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['HP'])
        do
            checks[k] = false
        end
        AGI['HP'] = checks;
    end
    return checks
end

local read_CC_checks = function(type)
    local checks = {}
    if type == "AMM"
    then
        for k,v in pairs(MASTER_MAP['CC'])
        do
            checks[k] = checkFlag(v['addr'], v['bit'])
        end
        AMM['CC'] = checks;
    elseif type == "BMM"
    then
        checks = BMM['CC']
    elseif type == "AGI" -- should only run for initialization
    then
        for k,v in pairs(MASTER_MAP['CC'])
        do
            checks[k] = false
        end
        AGI['CC'] = checks;
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

function locationControl()
    local mapaddr = getMap()
    if isBackup == true
    then
        if ((last_map == 335 or last_map == 337) and (mapaddr ~= 335 and mapaddr ~= 337)) -- Wooded Hollow
            or (last_map == 339 and mapaddr ~= 339)                                       -- Honey B Hive
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
        if mapaddr == 335 or mapaddr == 337 -- Wooded Hollow / JiggyTemple
        then
            if last_map ~= 335 and last_map ~= 337
            then
                BMMBackup();
                useAGI();
                last_map = mapaddr
            end
            nearWHJinjo()
            return all_location_checks("BMM");
        elseif mapaddr == 339              -- Honey Bs Hive
        then
            if last_map ~= 339 then
                BMMBackup();
                useAGI();
                last_map = mapaddr
            end
            return all_location_checks("BMM")
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

function BMMBackup()
    if isBackup == true
    then
        return
    end
    for zone,location in pairs(MASTER_MAP)
    do
        for loc,v in pairs(location)
        do
            BMM[zone][loc] = checkFlag(v['addr'], v['bit']);
        end
    end
    if DEBUG == true
    then
        print("Backup complete");
    end
    isBackup = true
end

function BMMRestore()
 for zone,location in pairs(MASTER_MAP)
 do
    for loc,v in pairs(location)
    do
        if AMM[zone][loc] == false and BMM[zone][loc] == true
        then
            setFlag(v['addr'], v['bit'])
            AMM[zone][loc] = BMM[zone][loc]
            if DEBUG == true
            then
                print(loc .. " Flag Set")
            end
        elseif AMM[zone][loc] == true and BMM[zone][loc] == false
        then
            clearFlag(v['addr'], v['bit'])
            AMM[zone][loc] = BMM[zone][loc]
            if DEBUG == true
            then
                print(loc .. " Flag Cleared")
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
    for zone,location in pairs(MASTER_MAP)
    do
        for loc,v in pairs(location)
        do
            if AMM[zone][loc] == false and AGI[zone][loc] == true
            then
                setFlag(v['addr'], v['bit'])
                AMM[zone][loc] = true
                if DEBUG == true
                then
                    print(loc .. " Flag Set");
                end
            elseif AMM[zone][loc] == true and AGI[zone][loc] == false
            then
                clearFlag(v['addr'], v['bit']);
                AMM[zone][loc] = false;
                if DEBUG == true
                then
                    print(loc .. " Flag Cleared");
                end
            end
        end
    end
end

function all_location_checks(type)
    local location_checks = {}
    local MM = { ['SM']  = {}, ['JV'] = {}, ['WH'] = {}, ['MT'] = {}, ['PL'] = {}, ['GM'] = {}, ['WW'] = {},
        ['CT'] = {}, ['JR'] = {}, ['WL'] = {}, ['TL'] = {}, ['GI'] = {}, ['HP'] = {}, ['CC'] = {}, ['H1'] = {}
    };
    for k,v in pairs(read_SM_checks(type))
    do 
        location_checks[k] = v;
        MM['SM'][k] = v;
    end
    for k,v in pairs(read_JV_checks(type)) 
    do
        location_checks[k] = v;
        MM['JV'][k] = v;
    end
    for k,v in pairs(read_WH_checks(type)) 
    do
        location_checks[k] = v;
        MM['WH'][k] = v;
    end
    for k,v in pairs(read_MT_checks(type)) 
    do
        location_checks[k] = v;
        MM['MT'][k] = v;
    end
    for k,v in pairs(read_PL_checks(type)) 
    do
        location_checks[k] = v;
        MM['PL'][k] = v;
    end
    for k,v in pairs(read_GM_checks(type)) 
    do
        location_checks[k] = v;
        MM['GM'][k] = v;
    end
    for k,v in pairs(read_WW_checks(type)) 
    do
        location_checks[k] = v;
        MM['WW'][k] = v;
    end
    for k,v in pairs(read_CT_checks(type)) 
    do
        location_checks[k] = v;
        MM['CT'][k] = v;
    end
    for k,v in pairs(read_JR_checks(type)) 
    do
        location_checks[k] = v;
        MM['JR'][k] = v;
    end
    for k,v in pairs(read_WL_checks(type)) 
    do
        location_checks[k] = v;
        MM['WL'][k] = v;
    end
    for k,v in pairs(read_TL_checks(type)) 
    do
        location_checks[k] = v;
        MM['TL'][k] = v;
    end
    for k,v in pairs(read_GI_checks(type)) 
    do
        location_checks[k] = v;
        MM['GI'][k] = v;
    end
    for k,v in pairs(read_HP_checks(type)) 
    do
        location_checks[k] = v;
        MM['HP'][k] = v;
    end
    for k,v in pairs(read_CC_checks(type)) 
    do
        location_checks[k] = v;
        MM['CC'][k] = v;
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
    if next(AGI) == nil then --only happens once when you first play
        AGI = location_checks
    end
    return location_checks
end

function archipelago_msg_box(msg)
    i = 0
    while i<100 do
        bgcolor = "#FC6600"
        brcolor = "#000000"
        gui.text(400, 700, msg, bgcolor)
        emu.frameadvance()
        i = i + 1
    end
end

function processAGIItem(item_list)
    for zones, location in pairs(MASTER_MAP)
    do
        for loc, v in pairs(location)
        do
            for ap_id, memlocation in pairs(item_list)
            do
                if v['locationId'] == memlocation
                then
                    if DEBUG == true
                    then
                        print("ITEM FOUND FROM AP:" .. loc);
                    end
                    AGI[zones][loc] = true;
                    savingAGI();
                end
            end
        end
    end
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
    if block['slot_player'] ~= nil and block['slot_player'] ~= "" 
    then
        player_name = block['slot_player']
        print("Player is")
        print(player_name)
    end
    if block['slot_seed'] ~= nil and block['slot_seed'] ~= "" 
    then
        seed = block['slot_seed']
    end
    if block['slot_deathlink'] ~= nil and block['slot_deathlink'] ~= false 
    then
        deathlink = true
    end
    -- Write player names on first connect or after reset (N64 logo, title screen, file select)
    -- Queue item for receiving, if one exists
    -- item_queue = block['items']
    -- received_items_count = mainmemory.read_u16_be(internal_count_addr)
    -- if received_items_count < #item_queue then
    --     -- There are items to send: remember lua tables are 1-indexed!
    --     if item_receivable() then
    --         mainmemory.write_u16_be(incoming_player_addr, 0x00)
    --         mainmemory.write_u16_be(incoming_item_addr, item_queue[received_items_count+1])
    --     end
    -- end
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
        retTable["isDead"] = isBanjoDed;

    
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
    local pause_menu = mainmemory.readbyte(0x07ADF3);
    if pause_menu == 1 and isPaused == false
    then
        if DEBUG == true
        then
            print("Game Paused");
        end
        if isBackup == false
        then
            BMMBackup();
        end
        useAGI();
        isPaused = true;
    elseif pause_menu == 0 and isPaused == true  -- unpaused
    then
        isPaused = false
        if DEBUG == true
        then
            print("Game Unpaused");
        end
        if isBackup == true and (last_map ~= 335 and last_map ~= 337 and last_map ~= 339)  -- Don't want to restore while in WH zone
        then
            BMMRestore()
        end
    elseif isPaused == true and DEBUG == true
    then
        local check_controls = joypad.get()
        if check_controls ~= nil and check_controls['P1 Z'] == true
        then
            print("AGI TABLE:");
            for k,v in pairs(AGI)
            do
                for loc, value in pairs(v)
                do
                    if(value == true)
                    then
                        print(loc .. ":" .. tostring(value))
                    end
                end
            end
        elseif check_controls ~= nil and check_controls['P1 C Right'] == true
        then
            print("BMM TABLE:");
            for k,v in pairs(BMM)
            do
                for loc, value in pairs(v)
                do
                    if(value == true)
                    then
                        print(loc .. ":" .. tostring(value))
                    end
                end
            end
        elseif check_controls ~= nil and check_controls['P1 C Left'] == true
        then
            print("AMM TABLE:");
            for k,v in pairs(AMM)
            do
                for loc, value in pairs(v)
                do
                    if(value == true)
                    then
                        print(loc .. ":" .. tostring(value))
                    end
                end
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
    f:write(json.encode(AGI))
    f:close()
    if DEBUG == true
    then
        print("AGI Table Saved");
    end
end

function gameSaving()
    if isPaused ~= true
    then
        return
    else
        local saveM1 = mainmemory.read_u32_be(0x12D580);
        local saveM2 = mainmemory.read_u32_be(0x12D584);
        local saveM3 = mainmemory.read_u32_be(0x12D588);
        if saveM1 == 255 and saveM2 == 255 and saveM3 == 255
        then
            local saveC1 = mainmemory.read_u32_be(0x15C4B4);
            local saveM2 = mainmemory.read_u32_be(0x15C4CC);
            local saveM3 = mainmemory.read_u32_be(0x163B84);
            if saveC1 == 0 and saveC2 == 0 and saveC3 == 0
            then
                if isBackup == true and isSaving == false
                then
                    BMMRestore()
                    isSaving = true
                end
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
    if block['slot_deathlink'] ~= nil and block['slot_deathlink'] ~= false
    then
        deathlink = true
    end

    if seed ~= 0
    then
        local f = io.open("BT" .. player_name .. "_" .. seed .. ".AGI", "r") --generate #BTplayer_seed.AGI
        if f==nil then
            all_location_checks("AGI")
            f = io.open("BT" .. player_name .. "_" .. seed .. ".AGI", "w")
            f:write(json.encode(AGI))
            f:close()
        else
            AGI = json.decode(f:read())
            f:close()
        end
    else
        return false
    end
    return true
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
                getBanjoDeathAnimation(false);
                receive();
                killBT();
            elseif (frame % 10 == 0)
            then
                checkPause();
                checkTotalMenu();
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
