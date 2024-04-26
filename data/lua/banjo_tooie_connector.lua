-- Banjo Tooie Connector Lua
-- Created by Mike Jackson (jjjj12212) 
-- with the help of Rose (Oktorose), the OOT Archipelago team, ScriptHawk BT.lua & kaptainkohl for BTrando.lua 
-- modifications from Unalive & HemiJackson 

-- local RDRAMBase = 0x80000000;
-- local RDRAMSize = 0x800000;
-- local character_state = 0x136F63;
-- local camera_pointer_pointer = 0x127728;
-- local global_flag_pointer = 0x12C780;

local socket = require("socket")
local json = require('json')
local math = require('math')
require('common')

local SCRIPT_VERSION = 4
local BT_VERSION = "V1.2.0"
local PLAYER = ""
local SEED = 0
local DEATH_LINK = false

local BT_SOCK = nil

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"
local PREV_STATE = ""
local CUR_STATE =  STATE_UNINITIALIZED
local FRAME = 0


local DEBUG = false
local DEBUGLVL2 = false
local DEBUGLVL3 = false

local BYPASS_GAME_LOAD = false;

local BTMODELOBJ = nil;
local BTRAMOBJ = nil;
local BTCONSUMEOBJ = nil;

local CURRENT_MAP = nil;
local SKIP_TOT = ""
local MINIGAMES = ""
local INIT_COMPLETE = false
local PAUSED = false;
local TOTALS_MENU = false;
local SAVE_GAME = false;
local USE_BMM_TBL = false;
local USE_BMM_ONLY_TBL = false;
local USE_BMM_ONLY_TYP = "";

local CLOSE_TO_ALTAR = false;
local DETECT_DEATH = false;
local SNEAK = false;
local AIMASSIST = false;
local SUPERBANJO = false;
local REGEN = false;
local TEXT_TIMER = 2;
local TEXT_START = false;

local ENABLE_AP_HONEYCOMB = false;
local ENABLE_AP_PAGES = false;
local ENABLE_AP_MOVES = false; -- Enable AP Moves Logics
local ENABLE_AP_DOUBLOONS = false;
local ENABLE_AP_TREBLE = false;
local ENABLE_AP_STATIONS = false;
local ENABLE_AP_CHUFFY = false;
local ENABLE_AP_JINJO = false;
local ENABLE_AP_NOTES = false;
local ENABLE_AP_WORLDS = false;
local AP_MESSAGES = {};

local GAME_LOADED = false;
-------------- SILO VARS ------------
local CHECK_FOR_SILO = false; --  If True, you are Transistioning maps
local WATCH_LOADED_SILOS = false; -- Silo found on Map, Need to Monitor Distance
local LOAD_BMK_MOVES = false; -- If close to Silo
local SILOS_LOADED = false; -- Handles if learned a move at Silo
local SILOS_WAIT_TIMER = 0; -- waits until Silos are loaded if any
local LOAD_SILO_NOTES = false;
local TOT_SET_COMPLETE = false;

-------------- TREBLE VARS ------------
local CHECK_FOR_TREBLE = false; -- Treble logic
local TREBLE_WAIT_TIMER = 0; -- waits until Treble is loaded if any
local WATCH_LOADED_TREBLE = false; -- if object is loaded or not 
local TREBLE_SPOTED = false; -- used if Collected Treble
local TREBLE_MAP = 0x00; -- validate TREBLE_MAP
local TREBLE_GONE_CHECK = 2;
local SKIP_PUZZLES = false;
local OPEN_HAG1 = false;

-------------- STATION VARS -----------
local CHECK_FOR_STATIONBTN = false;
local STATION_BTN_TIMER = 0;
local WATCH_LOADED_STATIONBTN = false;

-------------- CHUFFY VARS ------------
DEAD_COAL_CHECK = 0;
CHUFFY_MAP_TRANS = false;
CHUFFY_STOP_WATCH = true;
LEVI_PAD_MOVED = false;

local BATH_PADS_QOL = false


local receive_map = { -- [ap_id] = item_id; --  Required for Async Items
    ["NA"] = "NA"
}

-- Consumable Class
BTConsumable = {
    banjoRAM = nil;
    CONSUME_PTR = 0x12B250;
    CONSUME_IDX = 0x11B080;
    consumeTable = {
        [0]  = {key=0x27BD, name="BLUE EGGS", max=100},
        [1]  = {key=0x0C03, name="FIRE EGGS", max=50},
        [2]  = {key=0x0002, name="ICE EGGS", max=50},
        [3]  = {key=0x01EE, name="GRENADE EGGS", max=25},
        [4]  = {key=0x2401, name="CWK EGGS", max=10},
        [5]  = {key=0x15E0, name="Proximity Eggs"},
        [6]  = {key=0x1000, name="Red Feathers", max=100},
        [7]  = {key=0x3C18, name="Gold Feathers", max=10},
        [8]  = {key=0x0003, name="GLOWBO",max=16},
        [9]  = {key=0x3C0C, name="HONEYCOMB",max=25},
        [10] = {key=0x0319, name="CHEATO",max=25},
        [11] = {key=0x858C, name="Burgers"},
        [12] = {key=0x03E0, name="Fries"},
        [13] = {key=0x27BD, name="Tickets"},
        [14] = {key=0x0C03, name="DOUBLOON",max=30},
        [15] = {key=0x3C05, name="Gold Idols"},
        [16] = {key=0x0002, name="Beans"}, -- CCL
        [17] = {key=0x85E3, name="Fish"}, -- HFP
        [18] = {key=0x0040, name="Eggs"}, -- Stop'n'Swop
        [19] = {key=0x8FBF, name="Ice Keys"}, -- Stop'n'Swop  -- read key is 59
        [20] = {key=0x1461, name="MEGA GLOWBO",max=1}
    };
    consumeIndex = nil;
    consumeKey = nil;
    consumeName = nil;
}

function BTConsumable:new(BTRAM, itemName)
    setmetatable({}, self)
    self.__index = self
    BTConsumable:changeConsumable(itemName)
    self.banjoRAM = BTRAM;
   return self
end

function BTConsumable:setConsumable(value)
    if DEBUG == true
    then
        print("Setting Consumable value to :" .. tostring(value))
    end
    local addr = self.banjoRAM:dereferencePointer(self.CONSUME_PTR);
    mainmemory.write_u16_be(addr + self.consumeIndex * 2, value ~ self.consumeKey);
    mainmemory.write_u16_be(self.CONSUME_IDX + self.consumeIndex * 0x0C, value);
    if DEBUG == true
    then
        print(self.consumeName .. " has been modified")
    end
end

function BTConsumable:getConsumable()
    local amount = mainmemory.read_u16_be(self.CONSUME_IDX + self.consumeIndex * 0x0C);
	return amount;
end

function BTConsumable:getConsumableMax()
    return self.consumeTable[self.consumeIndex]["max"]
end

function BTConsumable:changeConsumable(itemName)
    self.consumeIndex = nil;
    for index, table in pairs(self.consumeTable)
    do
        if itemName == table["name"]
        then
            self.consumeIndex = index
            self.consumeKey = table["key"]
            self.consumeName = itemName
        end
    end
    if self.consumeIndex == nil
    then
        print("Could not find Consumeable name" + itemName)
        print("Please Correct and restart the Banjo Tooie Connector")
        return nil;
    end
end
-- EO Consumable Class

-- Class that requires RAM reading and writing
BTRAM = {
    RDRAMBase = 0x80000000;
    RDRAMSize = 0x800000;
    player_ptr = 0x135490;
    player_index = 0x1354DF;
    flag_block_ptr = 0x12C770;
    map_addr = 0x132DC2;
    player_pos_ptr = 0xE4,
    animationPointer = 0x136E70,
    movement_ptr = 0x120,
    current_state = 0x4,
    map_dest = 0x045702,
    character_state = 0x136F63,
}

function BTRAM:new(t)
    t = t or {}
    setmetatable(t, self)
    self.__index = self
   return self
end

function BTRAM:isPointer(value)
    return type(value) == "number" and value >= self.RDRAMBase and value < self.RDRAMBase + self.RDRAMSize;
end

function BTRAM:dereferencePointer(addr)
    if type(addr) == "number" and addr >= 0 and addr < (self.RDRAMSize - 4) then
        local address = mainmemory.read_u32_be(addr);
        if BTRAM:isPointer(address) then
            return address - self.RDRAMBase;
        else
            if DEBUGLVL3 == true
            then
                print("Failed to Defref:")
                print(address)
            end
            return nil;
        end
    else
        if DEBUGLVL3 == true
        then
            print("Number too big or not number:")
            print(tostring(addr))
        end
    end
end

function BTRAM:banjoPTR()
    local playerPointerIndex = mainmemory.readbyte(self.player_index);
	local addressSpace = BTRAM:dereferencePointer(self.player_ptr + 4 * playerPointerIndex);
    return addressSpace;
end

function BTRAM:getBanjoPos()
    local pos = { 
        ["Xpos"] = 0,
        ["Ypos"] = 0,
        ["Zpos"] = 0
    };
    local banjo = BTRAM:banjoPTR()
    if banjo == nil
    then
        return false;
    end
    local plptr = BTRAM:dereferencePointer(banjo + self.player_pos_ptr);
    if plptr == nil
    then
        return false;
    end
    
    pos["Xpos"] = mainmemory.readfloat(plptr + 0x0, true);
    pos["Ypos"] = mainmemory.readfloat(plptr + 0x4, true);
    pos["Zpos"] = mainmemory.readfloat(plptr + 0x8, true);
    return pos;
end

function BTRAM:getBanjoTState()
    return mainmemory.readbyte(self.character_state);
end

function BTRAM:getBanjoMovementState()
    local player = BTRAM:banjoPTR()
    if player ~= nil
    then
        local movestate = BTRAM:dereferencePointer(player + self.movement_ptr)
        return mainmemory.read_u32_be(movestate + self.current_state)
    end
    return nil
end

function BTRAM:getMap()
    local map = mainmemory.read_u16_be(self.map_addr);
    return map;
end

function BTRAM:checkFlag(byte, _bit, fromfuncDebug)
    local address = self:dereferencePointer(self.flag_block_ptr);
    if address == nil
    then
        if DEBUG == true
        then
            print("can't defef Flag Ptr")
        end
        return false
    end
    if byte == nil then
        print("Null found in " .. fromfuncDebug)
    end
    local currentValue = mainmemory.readbyte(address + byte);
    if bit.check(currentValue, _bit) then
        return true;
    else
        return false;
    end
end

function BTRAM:clearFlag(byte, _bit, fromfuncDebug)
    if DEBUGLVL2 == true then
        print(fromfuncDebug)
    end
	if type(byte) == "number" and type(_bit) == "number" and _bit >= 0 and _bit < 8 then
		local flags = self:dereferencePointer(self.flag_block_ptr);
        local currentValue = mainmemory.readbyte(flags + byte);
        mainmemory.writebyte(flags + byte, bit.clear(currentValue, _bit));
	end
end

function BTRAM:setFlag(byte, _bit)
	if type(byte) == "number" and type(_bit) == "number" and _bit >= 0 and _bit < 8 then
		local address = self:dereferencePointer(self.flag_block_ptr);
        local currentValue = mainmemory.readbyte(address + byte);
        mainmemory.writebyte(address + byte, bit.set(currentValue, _bit));
	end
end

function BTRAM:setMultipleFlags(byte, mask, flags)
	if type(byte) == "number" and type(mask) == "number" and mask >= 0 and mask < 0xFF then
		local address = self:dereferencePointer(self.flag_block_ptr);
        local currentValue = mainmemory.readbyte(address + byte);
        mainmemory.writebyte(address + byte, (currentValue & mask) | flags);
	end
end

BTModel = {
    banjoRAM = nil;
    OBJ_ARR_PTR = 0x136EE0;
    model_name = nil;
    enemy = false;
    obj_model1_slot_base = 0x10;
    obj_model1_slot_size = 0x9C;
    pos = { 
        ["Xpos"] = 0, 
        ["Ypos"] = 0, 
        ["Zpos"] = 0
    };
    model_list = {
        ["Altar"] = 0x977,
        ["Jinjo"] = 0x643,
        ["Silo"] = 0x7D7,
        ["Player"] = 0xFFFF,
        ["Kazooie Split Pad"] = 0x7E1,
        ["Banjo Split Pad"] = 0x7E2,
        ["Doubloon"] = 0x7C0,
        ["Treble Clef"] = 0x6ED,
        ["Station Switch"] = 0x86D,
        ["Levitate Pad"] = 0x7D8,
        ["Jiggy"] = 0x610,
        ["Breakable Door"] = 0x651,
        ["Sign Post"] = 0x7A2,
        ["Jiggy Guy"] = 0x937
    };
    model_enemy_list = {
        ["Ugger"] = 0x671,
        ["Mingy Jongo"] = 0x816,
    };
    singleModelPointer = nil;
    modelObjectList = {};
    animation_index = 0x8C,
    animationPointer = nil;
} 

function BTModel:new(BTRAM, modelName, isEnemy)
    t = t or {}
    setmetatable({}, self)
    self.__index = self
    self.model_name = modelName
    self.enemy = isEnemy
    self.banjoRAM = BTRAM

   return self
end

function BTModel:getModelSlotBase(index)
	return self.obj_model1_slot_base + index * self.obj_model1_slot_size;
end

function BTModel:getModelCount()
	local objects = self.banjoRAM:dereferencePointer(self.OBJ_ARR_PTR);
    if objects == nil
    then
        return
    end
    local firstObject = self.banjoRAM:dereferencePointer(objects + 0x04);
    local lastObject = self.banjoRAM:dereferencePointer(objects + 0x08);
	if lastObject == nil or firstObject == nil
	then
		return
	end
    return math.floor((lastObject - firstObject) / self.obj_model1_slot_size) + 1;
end

function BTModel:getModelPointers()
    local modelTable = {}
	local objectArray = self.banjoRAM:dereferencePointer(self.OBJ_ARR_PTR);
	local num_slots = self:getModelCount();
    if num_slots == nil
    then
        return nil
    end
    for i = 0, num_slots - 1
    do
        table.insert(modelTable, objectArray + self:getModelSlotBase(i));
	end

    return modelTable
end

function BTModel:getObjectAnimation()
    self.animationPointer = mainmemory.read_u16_be(self.singleModelPointer + self.animation_index)
    local defref = self.banjoRAM:dereferencePointer(self.banjoRAM.animationPointer)
    if defref ~= nil
    then
        return mainmemory.read_u16_be(defref + 0x38 + (0x3C * self.animationPointer))
    end
    return false
end

function BTModel:setObjectAnimation(animation2Bytes)
    self.animationPointer = mainmemory.read_u16_be(self.singleModelPointer + self.animation_index)
    local defref = self.banjoRAM:dereferencePointer(self.banjoRAM.animationPointer)
    if defref ~= nil
    then
        print("writing to Mem")
        print(defref + 0x38 + (0x3C * self.animationPointer))
        mainmemory.write_u16_be(defref + 0x38 + (0x3C * self.animationPointer), animation2Bytes)
        return true;
    end
    return false;
end

function BTModel:getAnimationType(modelPtr)
	local objectIDPointer = self.banjoRAM:dereferencePointer(modelPtr + 0x0);
    if objectIDPointer == nil
    then
        return nil
    end
    self.singleModelIndex = mainmemory.read_u16_be(objectIDPointer + 0x14);
    return self.singleModelIndex;
end

function BTModel:checkModel()
    local pointer_list = self:getModelPointers()
    if pointer_list == nil
    then
        return false
    end

    for k, modelptr in pairs(pointer_list)
    do
        local ObjectAddr = self:getAnimationType(modelptr); -- Required for special data
        if ObjectAddr == nil
        then
            return false
        end

        if self.enemy == true
        then
            for k, enemyval in pairs(self.model_enemy_list)
            do
                if ObjectAddr == enemyval
                then
                    self.singleModelPointer = modelptr;
                    return true;
                end
            end
        elseif ObjectAddr == self.model_list[self.model_name]
        then
            self.singleModelPointer = modelptr;
            return true;
        end
    end
    return false;
end

function BTModel:getModels() -- returns list
    self.modelObjectList = {}
    local pointer_list = self:getModelPointers()
    if pointer_list == nil
    then
        return false
    end
    local i = 0
    for k, objptr in pairs(pointer_list)
    do
        local currentObjectName = self:getAnimationType(objptr); -- Required for special data
        if currentObjectName == nil and i == 0
        then
            return false
        end
        i = i + 1
        if currentObjectName == self.model_list[self.model_name]
        then
           self.modelObjectList[i] = objptr;
        end
    end
    return self.modelObjectList;
end

function BTModel:changeName(modelName, isEnemy)
    self.model_name = modelName;
    self.enemy = isEnemy;
end

function BTModel:getSingleModelCoords(modelObjPtr)
    local POS = { 
        ["Xpos"] = 0, 
        ["Ypos"] = 0, 
        ["Zpos"] = 0,
        ["Hdist"] = 0;
        ["Distance"] = 9999;
    };
    local banjoPOS = self.banjoRAM:getBanjoPos();
    if banjoPOS == false
    then
        return false;
    end

    if modelObjPtr == nil
    then
        local result = self:checkModel();
        if result == false
        then
            return false
        end
        POS["Xpos"] = mainmemory.readfloat(self.singleModelPointer + 0x04, true);
        POS["Ypos"] = mainmemory.readfloat(self.singleModelPointer + 0x08, true);
        POS["Zpos"] = mainmemory.readfloat(self.singleModelPointer + 0x0C, true);
        POS["Hdist"] = math.sqrt(((POS["Xpos"] - banjoPOS["Xpos"]) ^ 2) + ((POS["Zpos"] - banjoPOS["Zpos"]) ^ 2));
        POS["Distance"] = math.floor(math.sqrt(((POS["Ypos"] - banjoPOS["Ypos"]) ^ 2) + (POS["Hdist"] ^ 2)));
    else
        POS["Xpos"] = mainmemory.readfloat(modelObjPtr + 0x04, true);
        POS["Ypos"] = mainmemory.readfloat(modelObjPtr + 0x08, true);
        POS["Zpos"] = mainmemory.readfloat(modelObjPtr + 0x0C, true);
        POS["Hdist"] = math.sqrt(((POS["Xpos"] - banjoPOS["Xpos"]) ^ 2) + ((POS["Zpos"] - banjoPOS["Zpos"]) ^ 2));
        POS["Distance"] = math.floor(math.sqrt(((POS["Ypos"] - banjoPOS["Ypos"]) ^ 2) + (POS["Hdist"] ^ 2)));
    end
    return POS;
end

function BTModel:getClosestModelDistance()
    self:getModels();
    local closest = nil;
    closest = 999999;
    for index, modelObjPtr in pairs(self.modelObjectList)
    do
        local checkdistance = self:getSingleModelCoords(modelObjPtr)

        if checkdistance ~= nil and checkdistance ~= false and checkdistance["Distance"] < closest
        then
            closest = checkdistance["Distance"]
        end
    end

    if closest == nil or closest == 999999
    then
        return false;
    end
    return closest
end

function BTModel:getMultipleModelCoords()
    local modelPOS_table = {}
    BTModel:getModels();
    local i = 0;
    for index, modelObjPtr in pairs(self.modelObjectList)
    do
        local objPOS = BTModel:getSingleModelCoords(modelObjPtr);
        if objPOS == false
        then
            return false
        end
        modelPOS_table[modelObjPtr] = objPOS
        i = i + 1
    end
    return modelPOS_table
end

function BTModel:moveModelObject(modelObjPtr, Xnew, Ynew, Znew)
    if modelObjPtr == nil
    then
        modelObjPtr = self.singleModelPointer;
    end
    if Xnew ~= nil
    then
        mainmemory.writefloat(modelObjPtr + 0x04, Xnew, true);
    end
    if Ynew ~= nil
    then
        mainmemory.writefloat(modelObjPtr + 0x08, Ynew, true);
    end
    if Znew ~= nil
    then
        mainmemory.writefloat(modelObjPtr + 0x0C, Znew, true);
    end
end

function BTModel:changeRotation(modelObjPtr, Yrot, Zrot)
    if modelObjPtr == nil
    then
        modelObjPtr = self.singleModelPointer;
    end
    if Yrot ~= nil
    then
        mainmemory.writefloat(modelObjPtr + 0x48, Yrot, true);
    end
    if Zrot ~= nil
    then
        mainmemory.writefloat(modelObjPtr + 0x4C, Zrot, true);
    end
end

function getAltar()
    if CURRENT_MAP == 335 or CURRENT_MAP == 337 -- No need to modify RAM when already in WH
    then
        return
    end
    BTMODELOBJ:changeName("Altar", false);
    local playerDist = BTMODELOBJ:getClosestModelDistance()
    if playerDist == false
    then
        return
    end
    if playerDist <= 300 and (CLOSE_TO_ALTAR == false or USE_BMM_TBL == false)
    then
        CLOSE_TO_ALTAR = true;
        BMMBackup();
        useAGI();
        if DEBUG == true
        then
            print("Altar Closeby");
        end
    elseif playerDist >=301 and CLOSE_TO_ALTAR == true
    then
        BMMRestore()
        CLOSE_TO_ALTAR = false;
        if DEBUG == true
        then
            print("Altar Away");
        end
    end
end

function nearWHJinjo()
    BTMODELOBJ:changeName("Jinjo", false);
    local playerDist = BTMODELOBJ:getClosestModelDistance()
    if playerDist == false
    then
        BMMBackup()
        useAGI()
        return;
    end

    if playerDist <= 400
    then
        if DEBUG == true
        then
            print("Near Jinjo");
        end
        BMMRestore();
    end
end

function nearDisiple()
    BTMODELOBJ:changeName("Jiggy Guy", false);
    local playerDist = BTMODELOBJ:getClosestModelDistance()
    if playerDist == false
    then
        BMMBackup()
        useAGI()
        return;
    end
    if playerDist <= 1500
    then
        if DEBUG == true
        then
            print("Near Disiple");
        end
        useAGINoJiggies();
    elseif playerDist > 1500 and playerDist < 2000
    then
        useAGI()
    end
end


-- Moves that needs to be checked Per Map. some silos NEEDS other moves as well to get to.
local ASSET_MAP_CHECK = {
    ["SILO"] = {
        [0x155] = { -- Cliff Top
            "1230763",
            ["Exceptions"] = {

            }
        },
        [0x152] = { -- Platau
            "1230756",
            ["Exceptions"] = {
                "1230755"
            }
        },
        [0x154] = { -- Pine Grove
            "1230759",
            ["Exceptions"] = {
                
            }
        },
        [0x15A] = { -- Wasteland
            "1230767",
            ["Exceptions"] = {
                
            }
        },
        [0xB8] = { -- MT Main
            "1230754",
            "1230755",
            ["Exceptions"] = {
                
            }
        },
        [0xC4] = { -- MT Grove
            "1230753",
            ["Exceptions"] = {
                
            }
        },
        [0xC7] = { -- GM Main
            "1230757",
            ["Exceptions"] = {
                
            }
        },
        [0x163] = { -- GM Storage
            "1230758",
            ["Exceptions"] = {
                
            }
        },
        [0xD6] = { -- WW Main
            "1230761",
            "1230760",
            ["Exceptions"] = {
                
            }
        },
        [0xE1] = { -- WW Castle
            "1230762",
            ["Exceptions"] = {
                
            }
        },
        [0x1A7] = { -- JRL Main
            "1230764",
            ["Exceptions"] = {
                
            }
        },
        [0xF6] = { -- JRL Eel Lair
            "1230765",
            ["Exceptions"] = {
                
            }
        },
        [0xED] = { -- JRL Jolly
            "1230766",
            ["Exceptions"] = {
                
            }
        },
        [0x112] = { --TDL Main
            "1230768",
            ["Exceptions"] = {
                
            }
        },
        [0x119] = { -- Unga Bunga Cave
            "1230770",
            ["Exceptions"] = {
    
            }
        },
        [0x117] = { -- TDL River
            "1230769",
            ["Exceptions"] = {
    
            }
        },
        [0x101] = { -- GI Floor 1
            "1230773",
            ["Exceptions"] = {
    
            }
        },
        [0x106] = { -- Floor 2
            "1230772",
            ["Exceptions"] = {
    
            }
        },
        [0x111] = { -- GI Waste Disposal
            "1230771",
            ["Exceptions"] = {
    
            }
        },
        [0x127] = { -- HFP Fire
            "1230774",
            ["Exceptions"] = {
    
            }
        },
        [0x128] = { -- HFP Ice
            "1230775",
            ["Exceptions"] = {
    
            }
        },
        [0x13A] = { -- CC Cave
            "1230776",
            ["Exceptions"] = {
    
            }
        }
    },
    ["TREBLE"] = {
        [0xB8] = "1230781", -- MT
        [0xCD] = "1230782", -- GGM:Water Storage
        [0xD6] = "1230783", -- WW
        [0x1A8] = "1230784", -- JR:Atlantis
        [0x112] = "1230785", -- TL
        [0x100] = "1230786", -- GI
        [0x132] = "1230787", -- HF:Ice Grotto
        [0x13A] = "1230788", -- CC:Cavern
        [0x142] = "1230789" -- JV
    },
    ["STATIONBTN"] = {
        [0x155] = "1230794", -- Clifftop + Button
        [0x112] = "1230791", -- TDL Button
        [0x100] = "1230790", -- GI Button
        [0x127] = "1230792", -- HFP Lava button
        [0x128] = "1230793", -- HFP Ice button
        [0xEC]  = "1230795" -- WW Button + Station
    }
}

-- Pattern 1 Map
local JINJO_PATTER_MAP = {
    ["1230501"] = {
        ["0"] = "1230570"
    },
    ["1230502"] = {
        ["0"] = "1230564",
        ["1"] = "1230582"
    },
    ["1230503"] = {
        ["0"] = "1230563",
        ["1"] =  "1230584",
        ["2"] = "1230583"
    },
    ["1230504"] = {
        ["0"] = "1230556",
        ["1"] =  "1230567",
        ["2"] = "1230572",
        ["3"] = "1230575"
    },
    ["1230505"] = {
        ["0"] = "1230565",
        ["1"] = "1230566",
        ["2"] =  "1230574",
        ["3"] = "1230577",
        ["4"] = "1230581",
    },
    ["1230506"] = {
        ["0"] = "1230552",
        ["1"] = "1230553",
        ["2"] = "1230555",
        ["3"] = "1230568",
        ["4"] = "1230569",
        ["5"] = "1230562",
    },
    ["1230507"] = {
        ["0"] = "1230558",
        ["1"] = "1230571",
        ["2"] = "1230585",
        ["3"] = "1230587",
        ["4"] = "1230591",
        ["5"] = "1230594",
        ["6"] = "1230595"
    },
    ["1230508"] = {
        ["0"] = "1230551",
        ["1"] = "1230560",
        ["2"] = "1230578",
        ["3"] = "1230586",
        ["4"] = "1230588",
        ["5"] = "1230590",
        ["6"] = "1230592",
        ["7"] = "1230593",
    },
    ["1230509"] = {
        ["0"] = "1230554",
        ["1"] = "1230557",
        ["2"] = "1230559",
        ["3"] = "1230561",
        ["4"] = "1230573",
        ["5"] = "1230576",
        ["6"] = "1230580",
        ["7"] = "1230589",
        ["8"] = "1230579",
    },
}

-- BMM - Backup Memory Map 
local BMM =  {};

-- AMM - Actual Memory Map
local AMM = {};

-- AGI - Archipelago given items
local AGI = {};
local AGI_MOVES = {};
local AGI_NOTES = {};
local AGI_STATIONS = {};
local AGI_CHUFFY = {};
local AGI_JINJOS = {
    ["1230501"] = 0, -- white
    ["1230502"] = 0, -- oragne
    ["1230503"] = 0, -- yellow
    ["1230504"] = 0, -- brown
    ["1230505"] = 0, -- green
    ["1230506"] = 0, -- red
    ["1230507"] = 0, -- blue
    ["1230508"] = 0, -- purple
    ["1230509"] = 0, -- black
};

local BKM = {}; -- Banjo Tooie Movelist Table
local BKNOTES = {}; -- Notes
local BKSTATIONS = {} -- Stations
local BKCHUFFY = {} -- King Coal Progress Flag
local BKJINJOFAM = {} -- Jinjo Family check 
local UNLOCKED_WORLDS = {} -- Worlds unlocked

-- Mapping required for AGI Table
local AGI_MASTER_MAP = {
    ['JIGGY'] = {
        ["1230676"] = {
            ['addr'] = 0x4F,
            ['bit'] = 0,
            ['name'] = 'JV: White Jinjo Family Jiggy'
        },
        ["1230677"] = {
            ['addr'] = 0x4F,
            ['bit'] = 1,
            ['name'] = 'Jinjo Village: Orange Jinjo Family Jiggy'
        },
        ["1230678"] = {
            ['addr'] = 0x4F,
            ['bit'] = 2,
            ['name'] = 'JV: Yellow Jinjo Family Jiggy'
        },
        ["1230679"] = {
            ['addr'] = 0x4F,
            ['bit'] = 3,
            ['name'] = 'JV: Brown Jinjo Family Jiggy'

        },
        ["1230680"] = {
            ['addr'] = 0x4F,
            ['bit'] = 4,
            ['name'] = 'JV: Green Jinjo Family Jiggy'
        },
        ["1230681"] = {
            ['addr'] = 0x4F,
            ['bit'] = 5,
            ['name'] = 'JV: Red Jinjo Family Jiggy'
        },
        ["1230682"] = {
            ['addr'] = 0x4F,
            ['bit'] = 6,
            ['name'] = 'JV: Blue Jinjo Family Jiggy'
        },
        ["1230683"] = {
            ['addr'] = 0x4F,
            ['bit'] = 7,
            ['name'] = 'JV: Purple Jinjo Family Jiggy'
        },
        ["1230684"] = {
            ['addr'] = 0x50,
            ['bit'] = 0,
            ['name'] = 'JV: Black Jinjo Family Jiggy'
        },
        ["1230685"] = {
            ['addr'] = 0x50,
            ['bit'] = 1,
            ['name'] = 'JV: King Jingaling Jiggy'
        },
        ["1230596"] = {
            ['addr'] = 0x45,
            ['bit'] = 0,
            ['name'] = 'MT: Targitzan Jiggy'
        },
        ["1230597"] = {
            ['addr'] = 0x45,
            ['bit'] = 1,
            ['name'] = 'MT: Slightly Sacred Chamber Jiggy'
        },
        ["1230598"] = {
            ['addr'] = 0x45,
            ['bit'] = 2,
            ['name'] = 'MT: Kickball Jiggy'
        },
        ["1230599"] = {
            ['addr'] = 0x45,
            ['bit'] = 3,
            ['name'] = 'MT: Bovina Jiggy'
        },
        ["1230600"] = {
            ['addr'] = 0x45,
            ['bit'] = 4,
            ['name'] = 'MT: Treasure Chamber Jiggy'
        },
        ["1230601"] = {
            ['addr'] = 0x45,
            ['bit'] = 5,
            ['name'] = 'MT: Golden Goliath Jiggy'
        },
        ["1230602"] = {
            ['addr'] = 0x45,
            ['bit'] = 6,
            ['name'] = 'MT: Prison Compound Quicksand Jiggy'
        },
        ["1230603"] = {
            ['addr'] = 0x45,
            ['bit'] = 7,
            ['name'] = 'MT: Pillars Jiggy'
        },
        ["1230604"] = {
            ['addr'] = 0x46,
            ['bit'] = 0,
            ['name'] = 'MT: Top of Temple Jiggy'
        },
        ["1230605"] = {
            ['addr'] = 0x46,
            ['bit'] = 1,
            ['name'] = 'MT: Ssslumber Jiggy'
        },
        ["1230606"] = {
            ['addr'] = 0x46,
            ['bit'] = 2,
            ['name'] = 'GGM: Old King Coal Jiggy'
        },
        ["1230607"] = {
            ['addr'] = 0x46,
            ['bit'] = 3,
            ['name'] = 'GGM: Canary Mary Jiggy'
        },
        ["1230608"] = {
            ['addr'] = 0x46,
            ['bit'] = 4,
            ['name'] = 'GGM: Generator Cavern Jiggy'
        },
        ["1230609"] = {
            ['addr'] = 0x46,
            ['bit'] = 5,
            ['name'] = 'GGM: Waterfall Cavern Jiggy'
        },
        ["1230610"] = {
            ['addr'] = 0x46,
            ['bit'] = 6,
            ['name'] = 'GGM: Ordinance Storage Jiggy'
        },
        ["1230611"] = {
            ['addr'] = 0x46,
            ['bit'] = 7,
            ['name'] = 'GGM: Dilberta Jiggy'
        },
        ["1230612"] = {
            ['addr'] = 0x47,
            ['bit'] = 0,
            ['name'] = 'GGM: Crushing Shed Jiggy'
        },
        ["1230613"] = {
            ['addr'] = 0x47,
            ['bit'] = 1,
            ['name'] = 'GGM: Waterfall Jiggy'
        },
        ["1230614"] = {
            ['addr'] = 0x47,
            ['bit'] = 2,
            ['name'] = 'GGM: Power Hut Basement Jiggy'
        },
        ["1230615"] = {
            ['addr'] = 0x47,
            ['bit'] = 3,
            ['name'] = 'GGM: Flooded Caves Jiggy'
        },
        ["1230616"] = {
            ['addr'] = 0x47,
            ['bit'] = 4,
            ['name'] = 'WW: Hoop Hurry Jiggy'
        },
        ["1230617"] = {
            ['addr'] = 0x47,
            ['bit'] = 5,
            ['name'] = 'WW: Dodgems Jiggy'
        },
        ["1230618"] = {
            ['addr'] = 0x47,
            ['bit'] = 6,
            ['name'] = 'WW: Mr. Patch Jiggy'
        },
        ["1230619"] = {
            ['addr'] = 0x47,
            ['bit'] = 7,
            ['name'] = 'WW: Saucer of Peril Jiggy'
        },
        ["1230620"] = {
            ['addr'] = 0x48,
            ['bit'] = 0,
            ['name'] = 'WW: Balloon Burst Jiggy'
        },
        ["1230621"] = {
            ['addr'] = 0x48,
            ['bit'] = 1,
            ['name'] = 'WW: Dive of Death Jiggy'
        },
        ["1230622"] = {
            ['addr'] = 0x48,
            ['bit'] = 2,
            ['name'] = 'WW: Mrs. Boggy Jiggy'
        },
        ["1230623"] = {
            ['addr'] = 0x48,
            ['bit'] = 3,
            ['name'] = 'WW: Star Spinner Jiggy'
        },
        ["1230624"] = {
            ['addr'] = 0x48,
            ['bit'] = 4,
            ['name'] = 'WW: The Inferno Jiggy'
        },
        ["1230625"] = {
            ['addr'] = 0x48,
            ['bit'] = 5,
            ['name'] = 'WW: Cactus of Strength Jiggy'
        },
        ["1230626"] = {
            ['addr'] = 0x48,
            ['bit'] = 6,
            ['name'] = 'JRL: Mini-Sub Challenge Jiggy'
        },
        ["1230627"] = {
            ['addr'] = 0x48,
            ['bit'] = 7,
            ['name'] = 'JRL: Tiptup Jiggy'
        },
        ["1230628"] = {
            ['addr'] = 0x49,
            ['bit'] = 0,
            ['name'] = 'JRL: Chris P. Bacon Jiggy'
        },
        ["1230629"] = {
            ['addr'] = 0x49,
            ['bit'] = 1,
            ['name'] = 'JRL: Pig Pool Jiggy'
        },
        ["1230630"] = {
            ['addr'] = 0x49,
            ['bit'] = 2,
            ['name'] = "JRL: Smuggler's Cavern Jiggy"
        },
        ["1230631"] = {
            ['addr'] = 0x49,
            ['bit'] = 3,
            ['name'] = 'JRL: Merry Maggie Jiggy'
        },
        ["1230632"] = {
            ['addr'] = 0x49,
            ['bit'] = 4,
            ['name'] = 'JRL: Woo Fak Fak Jiggy'
        },
        ["1230633"] = {
            ['addr'] = 0x49,
            ['bit'] = 5,
            ['name'] = 'JRL: Seemee Jiggy'
        },
        ["1230634"] = {
            ['addr'] = 0x49,
            ['bit'] = 6,
            ['name'] = 'JRL: Pawno Jiggy'
        },
        ["1230635"] = {
            ['addr'] = 0x49,
            ['bit'] = 7,
            ['name'] = 'JRL: UFO Jiggy'
        },
        ["1230636"] = {
            ['addr'] = 0x4A,
            ['bit'] = 0,
            ['name'] = "TDL: Under Terry's Nest Jiggy"
        },
        ["1230637"] = {
            ['addr'] = 0x4A,
            ['bit'] = 1,
            ['name'] = 'TDL: Dippy Jiggy'
        },
        ["1230638"] = {
            ['addr'] = 0x4A,
            ['bit'] = 2,
            ['name'] = 'TDL: Scrotty Jiggy'
        },
        ["1230639"] = {
            ['addr'] = 0x4A,
            ['bit'] = 3,
            ['name'] = 'TDL: Terry Jiggy'
        },
        ["1230640"] = {
            ['addr'] = 0x4A,
            ['bit'] = 4,
            ['name'] = 'TDL: Oogle Boogle Tribe Jiggy'
        },
        ["1230641"] = {
            ['addr'] = 0x4A,
            ['bit'] = 5,
            ['name'] = 'TDL: Chompas Belly Jiggy'
        },
        ["1230642"] = {
            ['addr'] = 0x4A,
            ['bit'] = 6,
            ['name'] = "TDL: Terry's Kids Jiggy"
        },
        ["1230643"] = {
            ['addr'] = 0x4A,
            ['bit'] = 7,
            ['name'] = 'TDL: Stomping Plains Jiggy'
        },
        ["1230644"] = {
            ['addr'] = 0x4B,
            ['bit'] = 0,
            ['name'] = 'TDL: Rocknut Tribe Jiggy'
        },
        ["1230645"] = {
            ['addr'] = 0x4B,
            ['bit'] = 1,
            ['name'] = 'TDL: Code of the Dinosaurs Jiggy'
        },
        ["1230646"] = {
            ['addr'] = 0x4B,
            ['bit'] = 2,
            ['name'] = 'GI: Underwater Waste Disposal Plant Jiggy'
        },
        ["1230647"] = {
            ['addr'] = 0x4B,
            ['bit'] = 3,
            ['name'] = 'GI: Weldar Jiggy'
        },
        ["1230648"] = {
            ['addr'] = 0x4B,
            ['bit'] = 4,
            ['name'] = "GI: Clinker's Cavern Jiggy"
        },
        ["1230649"] = {
            ['addr'] = 0x4B,
            ['bit'] = 5,
            ['name'] = 'GI: Skivvies Jiggy'
        },
        ["1230650"] = {
            ['addr'] = 0x4B,
            ['bit'] = 6,
            ['name'] = 'GI: Floor 5 Jiggy'
        },
        ["1230651"] = {
            ['addr'] = 0x4B,
            ['bit'] = 7,
            ['name'] = 'GI: Quality Control Jiggy'
        },
        ["1230652"] = {
            ['addr'] = 0x4C,
            ['bit'] = 0,
            ['name'] = 'GI: Floor 1 Guarded Jiggy'
        },
        ["1230653"] = {
            ['addr'] = 0x4C,
            ['bit'] = 1,
            ['name'] = 'GI: Trash Compactor Jiggy'
        },
        ["1230654"] = {
            ['addr'] = 0x4C,
            ['bit'] = 2,
            ['name'] = 'GI: Twinkly Packing Jiggy'
        },
        ["1230655"] = {
            ['addr'] = 0x4C,
            ['bit'] = 3,
            ['name'] = 'GI: Waste Disposal Plant Box Jiggy'
        },
        ["1230656"] = {
            ['addr'] = 0x4C,
            ['bit'] = 4,
            ['name'] = 'HFP: Dragon Brothers Jiggy'
        },
        ["1230657"] = {
            ['addr'] = 0x4C,
            ['bit'] = 5,
            ['name'] = 'HFP: Inside the Volcano Jiggy'
        },
        ["1230658"] = {
            ['addr'] = 0x4C,
            ['bit'] = 6,
            ['name'] = 'HFP: Sabreman Jiggy'
        },
        ["1230659"] = {
            ['addr'] = 0x4C,
            ['bit'] = 7,
            ['name'] = 'HFP: Boggy Jiggy'
        },
        ["1230660"] = {
            ['addr'] = 0x4D,
            ['bit'] = 0,
            ['name'] = 'HFP: Icy Side Station Jiggy'
        },
        ["1230661"] = {
            ['addr'] = 0x4D,
            ['bit'] = 1,
            ['name'] = 'HFP: Oil Drill Jiggy'
        },
        ["1230662"] = {
            ['addr'] = 0x4D,
            ['bit'] = 2,
            ['name'] = 'HFP: Stomping Plains Jiggy'
        },
        ["1230663"] = {
            ['addr'] = 0x4D,
            ['bit'] = 3,
            ['name'] = 'HFP: Kickball Jiggy'
        },
        ["1230664"] = {
            ['addr'] = 0x4D,
            ['bit'] = 4,
            ['name'] = 'HFP: Aliens Jiggy'
        },
        ["1230665"] = {
            ['addr'] = 0x4D,
            ['bit'] = 5,
            ['name'] = 'HFP: Lava Waterfall Jiggy'
        },
        ["1230666"] = {
            ['addr'] = 0x4D,
            ['bit'] = 6,
            ['name'] = 'CCL: Mingy Jongo Jiggy'
        },
        ["1230667"] = {
            ['addr'] = 0x4D,
            ['bit'] = 7,
            ['name'] = 'CCL: Mr Fit Jiggy'
        },
        ["1230668"] = {
            ['addr'] = 0x4E,
            ['bit'] = 0,
            ['name'] = "CCL: Pot O' Gold Jiggy"
        },
        ["1230669"] = {
            ['addr'] = 0x4E,
            ['bit'] = 1,
            ['name'] = 'CCL: Canary Mary Jiggy'
        },
        ["1230670"] = {
            ['addr'] = 0x4E,
            ['bit'] = 2,
            ['name'] = 'CCL: Zubbas Jiggy'
        },
        ["1230671"] = {
            ['addr'] = 0x4E,
            ['bit'] = 3,
            ['name'] = 'CCL: Jiggium Plant Jiggy'
        },
        ["1230672"] = {
            ['addr'] = 0x4E,
            ['bit'] = 4,
            ['name'] = 'CCL: Cheese Wedge Jiggy'
        },
        ["1230673"] = {
            ['addr'] = 0x4E,
            ['bit'] = 5,
            ['name'] = 'CCL: Trash Can Jiggy'
        },
        ["1230674"] = {
            ['addr'] = 0x4E,
            ['bit'] = 6,
            ['name'] = 'CCL: Superstash Jiggy'
        },
        ["1230675"] = {
            ['addr'] = 0x4E,
            ['bit'] = 7,
            ['name'] = 'CCL: Jelly Castle Jiggy'
        },
    },
    ['JINJO'] = {
        ["1230591"] = {
            ['addr'] = 0x3E,
            ['bit'] = 4,
            ['name'] = 'IoH:Wooded Hollow Jinjo'
        },
        ["1230595"] = {
            ['addr'] = 0x3F,
            ['bit'] = 0,
            ['name'] = 'SM: Jinjo'
        },
        ["1230594"] = {
            ['addr'] = 0x3E,
            ['bit'] = 7,
            ['name'] = 'IoH: Plateau Jinjo'
        },
        ["1230551"] = {
            ['addr'] = 0x39,
            ['bit'] = 4,
            ['name'] = 'MT: Jade Snake Grove Jinjo'
        },
        ["1230552"] = {
            ['addr'] = 0x39,
            ['bit'] = 5,
            ['name'] = 'MT: Stadium Jinjo'
        },
        ["1230553"] = {
            ['addr'] = 0x39,
            ['bit'] = 6,
            ['name'] = 'Mayahem Temple: Targitzan Temple Jinjo'
        },
        ["1230554"] = {
            ['addr'] = 0x39,
            ['bit'] = 7,
            ['name'] = 'MT: Water Pool Jinjo'
        },
        ["1230555"] = {
            ['addr'] = 0x3A,
            ['bit'] = 0,
            ['name'] = 'MT: Bridge Jinjo'
        },
        ["1230556"] = {
            ['addr'] = 0x3A,
            ['bit'] = 1,
            ['name'] = 'GGM: Water Storage Jinjo'
        },
        ["1230557"] = {
            ['addr'] = 0x3A,
            ['bit'] = 2,
            ['name'] = 'GGM: Jail Jinjo'
        },
        ["1230558"] = {
            ['addr'] = 0x3A,
            ['bit'] = 3,
            ['name'] = 'GGM: Toxic Gas Cave Jinjo'
        },
        ["1230559"] = {
            ['addr'] = 0x3A,
            ['bit'] = 4,
            ['name'] = 'GGM: Boulder Jinjo'
        },
        ["1230560"] = {
            ['addr'] = 0x3A,
            ['bit'] = 5,
            ['name'] = 'GGM: Mine Tracks Jinjo'
        },
        ["1230561"] = {
            ['addr'] = 0x3A,
            ['bit'] = 6,
            ['name'] = 'WW: Big Top Jinjo'
        },
        ["1230562"] = {
            ['addr'] = 0x3A,
            ['bit'] = 7,
            ['name'] = 'WW: Cave of Horrors Jinjo'
        },
        ["1230563"] = {
            ['addr'] = 0x3B,
            ['bit'] = 0,
            ['name'] = 'WW: Van Door Jinjo'
        },
        ["1230564"] = {
            ['addr'] = 0x3B,
            ['bit'] = 1,
            ['name'] = 'WW: Dodgem Dome Jinjo'
        },
        ["1230565"] = {
            ['addr'] = 0x3B,
            ['bit'] = 2,
            ['name'] = 'WW: Cactus of Strength Jinjo'
        },
        ["1230593"] = {
            ['addr'] = 0x3E,
            ['bit'] = 6,
            ['name'] = 'IoH: Clifftop Jinjo'
        },
        ["1230566"] = {
            ['addr'] = 0x3B,
            ['bit'] = 3,
            ['name'] = 'JRL: Lagoon Alcove Jinjo'
        },
        ["1230567"] = {
            ['addr'] = 0x3B,
            ['bit'] = 4,
            ['name'] = 'JRL: Blubber Jinjo'
        },
        ["1230568"] = {
            ['addr'] = 0x3B,
            ['bit'] = 5,
            ['name'] = 'JRL: Big Fish Jinjo'
        },
        ["1230569"] = {
            ['addr'] = 0x3B,
            ['bit'] = 6,
            ['name'] = 'JRL: Seaweed Sanctum Jinjo'
        },
        ["1230570"] = {
            ['addr'] = 0x3B,
            ['bit'] = 7,
            ['name'] = 'JRL: Sunken Ship Jinjo'
        },
        ["1230592"] = {
            ['addr'] = 0x3E,
            ['bit'] = 5,
            ['name'] = 'IoH: Wasteland Jinjo'
        },
        ["1230571"] = {
            ['addr'] = 0x3C,
            ['bit'] = 0,
            ['name'] = 'TDL: Talon Torp Jinjo'
        },
        ["1230572"] = {
            ['addr'] = 0x3C,
            ['bit'] = 1,
            ['name'] = 'TDL: Cutscene Skip Jinjo'
        },
        ["1230573"] = {
            ['addr'] = 0x3C,
            ['bit'] = 2,
            ['name'] = 'TDL: Beside Rocknut Jinjo'
        },
        ["1230574"] = {
            ['addr'] = 0x3C,
            ['bit'] = 3,
            ['name'] = 'TDL: Big T. Rex Skip Jinjo'
        },
        ["1230575"] = {
            ['addr'] = 0x3C,
            ['bit'] = 4,
            ['name'] = 'TDL: Stomping Plains Jinjo'
        },
        ["1230576"] = {
            ['addr'] = 0x3C,
            ['bit'] = 5,
            ['name'] = 'GI: Floor 5 Jinjo'
        },
        ["1230577"] = {
            ['addr'] = 0x3C,
            ['bit'] = 6,
            ['name'] = 'GI: Leg Spring Jinjo'
        },
        ["1230578"] = {
            ['addr'] = 0x3C,
            ['bit'] = 7,
            ['name'] = 'GI: Waste Disposal Plant Jinjo'
        },
        ["1230579"] = {
            ['addr'] = 0x3D,
            ['bit'] = 0,
            ['name'] = 'GI: Boiler Plant Jinjo'
        },
        ["1230580"] = {
            ['addr'] = 0x3D,
            ['bit'] = 1,
            ['name'] = 'GI: Outside Jinjo'
        },
        ["1230581"] = {
            ['addr'] = 0x3D,
            ['bit'] = 2,
            ['name'] = 'HFP: Lava Waterfall Jinjo'
        },
        ["1230582"] = {
            ['addr'] = 0x3D,
            ['bit'] = 3,
            ['name'] = 'HFP: Boiling Hot Pool Jinjo'
        },
        ["1230583"] = {
            ['addr'] = 0x3D,
            ['bit'] = 4,
            ['name'] = 'HFP: Windy Hole Jinjo'
        },
        ["1230584"] = {
            ['addr'] = 0x3D,
            ['bit'] = 5,
            ['name'] = 'HFP: Icicle Grotto Jinjo'
        },
        ["1230585"] = {
            ['addr'] = 0x3D,
            ['bit'] = 6,
            ['name'] = 'HFP: Mildred Ice Cube Jinjo'
        },
        ["1230586"] = {
            ['addr'] = 0x3D,
            ['bit'] = 7,
            ['name'] = 'CCL: Trash Can Jinjo'
        },
        ["1230587"] = {
            ['addr'] = 0x3E,
            ['bit'] = 0,
            ['name'] = 'CCL: Cheese Wedge Jinjo'
        },
        ["1230588"] = {
            ['addr'] = 0x3E,
            ['bit'] = 1,
            ['name'] = 'CCL: Central Cavern Jinjo'
        },
        ["1230589"] = {
            ['addr'] = 0x3E,
            ['bit'] = 2,
            ['name'] = 'CCL: Fake Mumbo Skull Jinjo'
        },
        ["1230590"] = {
            ['addr'] = 0x3E,
            ['bit'] = 3,
            ['name'] = 'CCL: Wumba Jinjo'
        }
    },
    ['CHEATO'] = {
        ["1230752"] = {
            ['addr'] = 0x59,
            ['bit'] = 3,
            ['name'] = 'Spiral Mountain: Cheato Page'
        },
        ["1230728"] = {
            ['addr'] = 0x56,
            ['bit'] = 3,
            ['name'] = 'MT: Snake Head Cheato Page'
        },
        ["1230729"] = {
            ['addr'] = 0x56,
            ['bit'] = 4,
            ['name'] = 'MT: Prison Compound Cheato Page'
        },
        ["1230730"] = {
            ['addr'] = 0x56,
            ['bit'] = 5,
            ['name'] = 'MT: Jade Snake Grove Cheato Page'
        },
        ["1230731"] = {
            ['addr'] = 0x56,
            ['bit'] = 6,
            ['name'] = 'GGM: Canary Mary Cheato Page'
        },
        ["1230732"] = {
            ['addr'] = 0x56,
            ['bit'] = 7,
            ['name'] = 'GGM: Entrance Cheato Page'
        },
        ["1230733"] = {
            ['addr'] = 0x57,
            ['bit'] = 0,
            ['name'] = 'GGM: Water Storage Cheato Page'
        },
        ["1230734"] = {
            ['addr'] = 0x57,
            ['bit'] = 1,
            ['name'] = 'WW: The Haunted Cavern Cheato Page'
        },
        ["1230735"] = {
            ['addr'] = 0x57,
            ['bit'] = 2,
            ['name'] = 'WW: The Inferno Cheato Page'
        },
        ["1230736"] = {
            ['addr'] = 0x57,
            ['bit'] = 3,
            ['name'] = 'WW: Saucer of Peril Cheato Page'
        },
        ["1230737"] = {
            ['addr'] = 0x57,
            ['bit'] = 4,
            ['name'] = "JRL: Pawno's Cheato Page"
        },
        ["1230738"] = {
            ['addr'] = 0x57,
            ['bit'] = 5,
            ['name'] = 'JRL: Seemee Cheato Page'
        },
        ["1230739"] = {
            ['addr'] = 0x57,
            ['bit'] = 6,
            ['name'] = 'JRL: Ancient Baths Cheato Page'
        },
        ["1230740"] = {
            ['addr'] = 0x57,
            ['bit'] = 7,
            ['name'] = "TDL: Dippy's Pool Cheato Page"
        },
        ["1230741"] = {
            ['addr'] = 0x58,
            ['bit'] = 0,
            ['name'] = 'TDL: Inside the Mountain Cheato Page'
        },
        ["1230742"] = {
            ['addr'] = 0x58,
            ['bit'] = 1,
            ['name'] = 'TDL: Boulder Cheato Page'
        },
        ["1230743"] = {
            ['addr'] = 0x58,
            ['bit'] = 2,
            ['name'] = 'GI: Loggo Cheato Page'
        },
        ["1230744"] = {
            ['addr'] = 0x58,
            ['bit'] = 3,
            ['name'] = 'GI: Floor 2 Cheato Page'
        },
        ["1230745"] = {
            ['addr'] = 0x58,
            ['bit'] = 4,
            ['name'] = 'GI: Repair Depot Cheato Page'
        },
        ["1230746"] = {
            ['addr'] = 0x58,
            ['bit'] = 5,
            ['name'] = 'HFP: Lava Side Cheato Page'
        },
        ["1230747"] = {
            ['addr'] = 0x58,
            ['bit'] = 6,
            ['name'] = 'HFP: Icicle Grotto Cheato Page'
        },
        ["1230748"] = {
            ['addr'] = 0x58,
            ['bit'] = 7,
            ['name'] = 'HFP: Icy Side Cheato Page'
        },
        ["1230749"] = {
            ['addr'] = 0x59,
            ['bit'] = 0,
            ['name'] = 'CCL: Canary Mary Cheato Page'
        },
        ["1230750"] = {
            ['addr'] = 0x59,
            ['bit'] = 1,
            ['name'] = "CCL: Pot O' Gold Cheato Page"
        },
        ["1230751"] = {
            ['addr'] = 0x59,
            ['bit'] = 2,
            ['name'] = 'CCL: Zubbas Cheato Page'
        },
    },
    ['HONEYCOMB'] = {
        ["1230727"] = {
            ['addr'] = 0x42,
            ['bit'] = 2,
            ['name'] = 'Plateau: Honeycomb'
        },
        ["1230703"] = {
            ['addr'] = 0x3F,
            ['bit'] = 2,
            ['name'] = 'MT: Entrance Honeycomb'
        },
        ["1230704"] = {
            ['addr'] = 0x3F,
            ['bit'] = 3,
            ['name'] = 'MT: Bovina Honeycomb'
        },
        ["1230705"] = {
            ['addr'] = 0x3F,
            ['bit'] = 4,
            ['name'] = 'MT: Treasure Chamber Honeycomb'
        },
        ["1230706"] = {
            ['addr'] = 0x3F,
            ['bit'] = 5,
            ['name'] = 'GGM: Toxic Gas Cave Honeycomb'
        },
        ["1230707"] = {
            ['addr'] = 0x3F,
            ['bit'] = 6,
            ['name'] = 'GGM: Boulder Honeycomb'
        },
        ["1230708"] = {
            ['addr'] = 0x3F,
            ['bit'] = 7,
            ['name'] = 'GGM: Train Station Honeycomb'
        },
        ["1230709"] = {
            ['addr'] = 0x40,
            ['bit'] = 0,
            ['name'] = 'WW: Space Zone Honeycomb'
        },
        ["1230710"] = {
            ['addr'] = 0x40,
            ['bit'] = 1,
            ['name'] = 'WW: Mumbo Skull Honeycomb'
        },
        ["1230711"] = {
            ['addr'] = 0x40,
            ['bit'] = 2,
            ['name'] = 'WW: Crazy Castle Honeycomb'
        },
        ["1230712"] = {
            ['addr'] = 0x40,
            ['bit'] = 3,
            ['name'] = 'JRL: Seemee Honeycomb'
        },
        ["1230713"] = {
            ['addr'] = 0x40,
            ['bit'] = 4,
            ['name'] = 'JRL: Atlantis Honeycomb'
        },
        ["1230714"] = {
            ['addr'] = 0x40,
            ['bit'] = 5,
            ['name'] = 'JRL: Waste Pipe Honeycomb'
        },
        ["1230715"] = {
            ['addr'] = 0x40,
            ['bit'] = 6,
            ['name'] = 'TDL: Lakeside Honeycomb'
        },
        ["1230716"] = {
            ['addr'] = 0x40,
            ['bit'] = 7,
            ['name'] = 'TDL: Styracosaurus Cave Honeycomb'
        },
        ["1230717"] = {
            ['addr'] = 0x41,
            ['bit'] = 0,
            ['name'] = 'TDL: River Passage Honeycomb'
        },
        ["1230718"] = {
            ['addr'] = 0x41,
            ['bit'] = 1,
            ['name'] = 'GI: Floor 3 Honeycomb'
        },
        ["1230719"] = {
            ['addr'] = 0x41,
            ['bit'] = 2,
            ['name'] = 'GI: Train Station Honeycomb'
        },
        ["1230720"] = {
            ['addr'] = 0x41,
            ['bit'] = 3,
            ['name'] = 'GI: Chimney Honeycomb'
        },
        ["1230721"] = {
            ['addr'] = 0x41,
            ['bit'] = 4,
            ['name'] = 'HFP: Inside the Volcano Honeycomb'
        },
        ["1230722"] = {
            ['addr'] = 0x41,
            ['bit'] = 5,
            ['name'] = 'HFP: Train Station Honeycomb'
        },
        ["1230723"] = {
            ['addr'] = 0x41,
            ['bit'] = 6,
            ['name'] = 'HFP: Lava Side Honeycomb'
        },
        ["1230724"] = {
            ['addr'] = 0x41,
            ['bit'] = 7,
            ['name'] = 'CCL: Dirt Patch Honeycomb'
        },
        ["1230725"] = {
            ['addr'] = 0x42,
            ['bit'] = 0,
            ['name'] = 'CCL: Trash Can Honeycomb'
        },
        ["1230726"] = {
            ['addr'] = 0x42,
            ['bit'] = 1,
            ['name'] = "CCL: Pot O' Gold Honeycomb"
        },
    },
    ['GLOWBO'] = {
         ["1230686"] = {
             ['addr'] = 0x42,
             ['bit'] = 7,
             ['name'] = "MT: Mumbo's Glowbo"
         },
         ["1230687"] = {
             ['addr'] = 0x43,
             ['bit'] = 0,
             ['name'] = 'MT: Jade Snake Grove Glowbo'

         },
         ["1230688"] = {
             ['addr'] = 0x43,
             ['bit'] = 1,
             ['name'] = 'GGM: Near Entrance Glowbo'

         },
         ["1230689"] = {
             ['addr'] = 0x43,
             ['bit'] = 2,
             ['name'] = 'GGM: Mine Entrance 2 Glowbo'

         },
         ["1230690"] = {
             ['addr'] = 0x43,
             ['bit'] = 3,
             ['name'] = 'WW: The Inferno Glowbo'

         },
         ["1230691"] = {
             ['addr'] = 0x43,
             ['bit'] = 4,
             ['name'] = "WW: Wumba's Glowbo"

         },
         ["1230702"] = {
             ['addr'] = 0x44,
             ['bit'] = 7,
             ['name'] = 'Cliff Top: Glowbo'

         },
         ["1230692"] = {
             ['addr'] = 0x43,
             ['bit'] = 5,
             ['name'] = "JRL: Pawno's Emporium Glowbo"

         },
         ["1230693"] = {
             ['addr'] = 0x43,
             ['bit'] = 6,
             ['name'] = "JRL: Under Wumba's Wigwam Glowbo"

         },
         ["1230694"] = {
             ['addr'] = 0x43,
             ['bit'] = 7,
             ['name'] = 'TDL: Unga Bunga Cave Entrance Glowbo'

         },
         ["1230695"] = {
             ['addr'] = 0x44,
             ['bit'] = 0,
             ['name'] = "TDL: Behind Mumbo's Skull Glowbo"

         },
         ["1230696"] = {
             ['addr'] = 0x44,
             ['bit'] = 1,
             ['name'] = 'GI: Floor 2 Glowbo'

         },
         ["1230697"] = {
             ['addr'] = 0x44,
             ['bit'] = 2,
             ['name'] = 'GI: Floor 3 Glowbo'

         },
         ["1230698"] = {
             ['addr'] = 0x44,
             ['bit'] = 3,
             ['name'] = 'HFP: Lava Side Glowbo'

         },
         ["1230699"] = {
             ['addr'] = 0x44,
             ['bit'] = 4,
             ['name'] = 'HFP: Icy Side Glowbo'

         },
         ["1230700"] = {
             ['addr'] = 0x44,
             ['bit'] = 5,
             ['name'] = 'CCL: Green Pool Glowbo'

         },
         ["1230701"] = {
             ['addr'] = 0x44,
             ['bit'] = 6,
             ['name'] = 'CCL: Central Cavern Glowbo'

         },
    },
    ['MEGA GLOWBO'] = {
        ["1230046"] = {
            ['addr'] = 0x05,
            ['bit'] = 6,
            ['name'] = 'Mega Glowbo'
        }

    },
    ['DOUBLOON'] = {
        ["1230521"] = {
            ['addr'] = 0x22,
            ['bit'] = 7,
            ['name'] = 'JRL: Town Center Pole 1 Doubloon'
        },
        ["1230522"] = {
            ['addr'] = 0x23,
            ['bit'] = 0,
            ['name'] = 'JRL: Town Center Pole 2 Doubloon'
        },
        ["1230523"] = {
            ['addr'] = 0x23,
            ['bit'] = 1,
            ['name'] = 'JRL: Town Center Pole 3 Doubloon'
        },
        ["1230524"] = {
            ['addr'] = 0x23,
            ['bit'] = 2,
            ['name'] = 'JRL: Town Center Pole 4 Doubloon'
        },
        ["1230525"] = {
            ['addr'] = 0x23,
            ['bit'] = 3,
            ['name'] = 'JRL: Town Center Pole 5 Doubloon'
        },
        ["1230526"] = {
            ['addr'] = 0x23,
            ['bit'] = 4,
            ['name'] = 'JRL: Town Center Pole 6 Doubloon'
        },
        ["1230527"] = {
            ['addr'] = 0x23,
            ['bit'] = 5,
            ['name'] = 'JRL: Silo 1 Doubloon'
        },
        ["1230528"] = {
            ['addr'] = 0x23,
            ['bit'] = 6,
            ['name'] = 'JRL: Silo 2 Doubloon'
        },
        ["1230529"] = {
            ['addr'] = 0x23,
            ['bit'] = 7,
            ['name'] = 'JRL: Silo 3 Doubloon'
        },
        ["1230530"] = {
            ['addr'] = 0x24,
            ['bit'] = 0,
            ['name'] = 'JRL: Silo 4 Doubloon'
        },
        ["1230531"] = {
            ['addr'] = 0x24,
            ['bit'] = 1,
            ['name'] = 'JRL: Toxic Pool 1 Doubloon'
        },
        ["1230532"] = {
            ['addr'] = 0x24,
            ['bit'] = 2,
            ['name'] = 'JRL: Toxic Pool 2 Doubloon'
        },
        ["1230533"] = {
            ['addr'] = 0x24,
            ['bit'] = 3,
            ['name'] = 'JRL: Toxic Pool 3 Doubloon'
        },
        ["1230534"] = {
            ['addr'] = 0x24,
            ['bit'] = 4,
            ['name'] = 'JRL: Toxic Pool 4 Doubloon'
        },
        ["1230535"] = {
            ['addr'] = 0x24,
            ['bit'] = 5,
            ['name'] = 'JRL: Mumbo Skull 1 Doubloon'
        },
        ["1230536"] = {
            ['addr'] = 0x24,
            ['bit'] = 6,
            ['name'] = 'JRL: Mumbo Skull 2 Doubloon'
        },
        ["1230537"] = {
            ['addr'] = 0x24,
            ['bit'] = 7,
            ['name'] = 'JRL: Mumbo Skull 3 Doubloon'
        },
        ["1230538"] = {
            ['addr'] = 0x25,
            ['bit'] = 0,
            ['name'] = 'JRL: Mumbo Skull 4 Doubloon'
        },
        ["1230539"] = {
            ['addr'] = 0x25,
            ['bit'] = 1,
            ['name'] = 'JRL: Underground 1 Doubloon'
        },
        ["1230540"] = {
            ['addr'] = 0x25,
            ['bit'] = 2,
            ['name'] = 'JRL: Underground 2 Doubloon'
        },
        ["1230541"] = {
            ['addr'] = 0x25,
            ['bit'] = 3,
            ['name'] = 'JRL: Underground 3 Doubloon'
        },
        ["1230542"] = {
            ['addr'] = 0x25,
            ['bit'] = 4,
            ['name'] = 'JRL: Alcove 1 Doubloon'
        },
        ["1230543"] = {
            ['addr'] = 0x25,
            ['bit'] = 5,
            ['name'] = 'JRL: Alcove 2 Doubloon'
        },
        ["1230544"] = {
            ['addr'] = 0x25,
            ['bit'] = 6,
            ['name'] = 'JRL: Alcove 3 Doubloon'
        },
        ["1230545"] = {
            ['addr'] = 0x25,
            ['bit'] = 7,
            ['name'] = 'JRL: Capt Blackeye 1 Doubloon'
        },
        ["1230546"] = {
            ['addr'] = 0x26,
            ['bit'] = 0,
            ['name'] = 'JRL: Capt Blackeye 2 Doubloon'
        },
        ["1230547"] = {
            ['addr'] = 0x26,
            ['bit'] = 1,
            ['name'] = 'JRL: Near Jinjo 1 Doubloon'
        },
        ["1230548"] = {
            ['addr'] = 0x26,
            ['bit'] = 2,
            ['name'] = 'JRL: Near Jinjo 2 Doubloon'
        },
        ["1230549"] = {
            ['addr'] = 0x26,
            ['bit'] = 3,
            ['name'] = 'JRL: Near Jinjo 3 Doubloon'
        },
        ["1230550"] = {
            ['addr'] = 0x26,
            ['bit'] = 4,
            ['name'] = 'JRL: Near Jinjo 4 Doubloon'
        }
    },
    ['NOTES'] = {
        ["1230800"] = {
            ['addr'] = 0x84,
            ['bit'] = 7,
        },
        ["1230801"] = {
            ['addr'] = 0x85,
            ['bit'] = 0,
        },
        ["1230802"] = {
            ['addr'] = 0x85,
            ['bit'] = 1,
        },
        ["1230803"] = {
            ['addr'] = 0x85,
            ['bit'] = 2,
        },
        ["1230804"] = {
            ['addr'] = 0x85,
            ['bit'] = 3,
        },
        ["1230805"] = {
            ['addr'] = 0x85,
            ['bit'] = 4,
        },
        ["1230806"] = {
            ['addr'] = 0x85,
            ['bit'] = 5,
        },
        ["1230807"] = {
            ['addr'] = 0x85,
            ['bit'] = 6,
        },
        ["1230808"] = {
            ['addr'] = 0x85,
            ['bit'] = 7,
        },
        ["1230809"] = {
            ['addr'] = 0x86,
            ['bit'] = 0,
        },
        ["1230810"] = {
            ['addr'] = 0x86,
            ['bit'] = 1,
        },
        ["1230811"] = {
            ['addr'] = 0x86,
            ['bit'] = 2,
        },
        ["1230812"] = {
            ['addr'] = 0x86,
            ['bit'] = 3,
        },
        ["1230813"] = {
            ['addr'] = 0x86,
            ['bit'] = 4,
        },
        ["1230814"] = {
            ['addr'] = 0x86,
            ['bit'] = 5,
        },
        ["1230815"] = {
            ['addr'] = 0x86,
            ['bit'] = 6,
        },
         -- EO Mayahem Temple
         ["1230816"] = {
            ['addr'] = 0x87,
            ['bit'] = 0,
        },
        ["1230817"] = {
            ['addr'] = 0x87,
            ['bit'] = 1,
        },
        ["1230818"] = {
            ['addr'] = 0x87,
            ['bit'] = 2,
        },
        ["1230819"] = {
            ['addr'] = 0x87,
            ['bit'] = 3,
        },
        ["1230820"] = {
            ['addr'] = 0x87,
            ['bit'] = 4,
        },
        ["1230821"] = {
            ['addr'] = 0x87,
            ['bit'] = 5,
        },
        ["1230822"] = {
            ['addr'] = 0x87,
            ['bit'] = 6,
        },
        ["1230823"] = {
            ['addr'] = 0x87,
            ['bit'] = 7,
        },
        ["1230824"] = {
            ['addr'] = 0x88,
            ['bit'] = 0,
        },
        ["1230825"] = {
            ['addr'] = 0x88,
            ['bit'] = 1,
        },
        ["1230826"] = {
            ['addr'] = 0x88,
            ['bit'] = 2,
        },
        ["1230827"] = {
            ['addr'] = 0x88,
            ['bit'] = 3,
        },
        ["1230828"] = {
            ['addr'] = 0x88,
            ['bit'] = 4,
        },
        ["1230829"] = {
            ['addr'] = 0x88,
            ['bit'] = 5,
        },
        ["1230830"] = {
            ['addr'] = 0x88,
            ['bit'] = 6,
        },
        ["1230831"] = {
            ['addr'] = 0x88,
            ['bit'] = 7,
        },
        -- EO GGM
        ["1230832"] = {
            ['addr'] = 0x89,
            ['bit'] = 1,
        },
        ["1230833"] = {
            ['addr'] = 0x89,
            ['bit'] = 2,
        },
        ["1230834"] = {
            ['addr'] = 0x89,
            ['bit'] = 3,
        },
        ["1230835"] = {
            ['addr'] = 0x89,
            ['bit'] = 4,
        },
        ["1230836"] = {
            ['addr'] = 0x89,
            ['bit'] = 5,
        },
        ["1230837"] = {
            ['addr'] = 0x89,
            ['bit'] = 6,
        },
        ["1230838"] = {
            ['addr'] = 0x89,
            ['bit'] = 7,
        },
        ["1230839"] = {
            ['addr'] = 0x8A,
            ['bit'] = 0,
        },
        ["1230840"] = {
            ['addr'] = 0x8A,
            ['bit'] = 1,
        },
        ["1230841"] = {
            ['addr'] = 0x8A,
            ['bit'] = 2,
        },
        ["1230842"] = {
            ['addr'] = 0x8A,
            ['bit'] = 3,
        },
        ["1230843"] = {
            ['addr'] = 0x8A,
            ['bit'] = 4,
        },
        ["1230844"] = {
            ['addr'] = 0x8A,
            ['bit'] = 5,
        },
        ["1230845"] = {
            ['addr'] = 0x8A,
            ['bit'] = 6,
        },
        ["1230846"] = {
            ['addr'] = 0x8A,
            ['bit'] = 7,
        },
        ["1230847"] = {
            ['addr'] = 0x8B,
            ['bit'] = 0,
        },
        --EO WW
        ["1230848"] = {
            ['addr'] = 0x8B,
            ['bit'] = 2,
        },
        ["1230849"] = {
            ['addr'] = 0x8B,
            ['bit'] = 3,
        },
        ["1230850"] = {
            ['addr'] = 0x8B,
            ['bit'] = 4,
        },
        ["1230851"] = {
            ['addr'] = 0x8B,
            ['bit'] = 5,
        },
        ["1230852"] = {
            ['addr'] = 0x8B,
            ['bit'] = 6,
        },
        ["1230853"] = {
            ['addr'] = 0x8B,
            ['bit'] = 7,
        },
        ["1230854"] = {
            ['addr'] = 0x8C,
            ['bit'] = 0,
        },
        ["1230855"] = {
            ['addr'] = 0x8C,
            ['bit'] = 1,
        },
        ["1230856"] = {
            ['addr'] = 0x8C,
            ['bit'] = 2,
        },
        ["1230857"] = {
            ['addr'] = 0x8C,
            ['bit'] = 3,
        },
        ["1230858"] = {
            ['addr'] = 0x8C,
            ['bit'] = 4,
        },
        ["1230859"] = {
            ['addr'] = 0x8C,
            ['bit'] = 5,
        },
        ["1230860"] = {
            ['addr'] = 0x8C,
            ['bit'] = 6,
        },
        ["1230861"] = {
            ['addr'] = 0x8C,
            ['bit'] = 7,
        },
        ["1230862"] = {
            ['addr'] = 0x8D,
            ['bit'] = 0,
        },
        ["1230863"] = {
            ['addr'] = 0x8D,
            ['bit'] = 1,
        },
        -- EO JRL
        ["1230864"] = {
            ['addr'] = 0x8D,
            ['bit'] = 3,
        },
        ["1230865"] = {
            ['addr'] = 0x8D,
            ['bit'] = 4,
        },
        ["1230866"] = {
            ['addr'] = 0x8D,
            ['bit'] = 5,
        },
        ["1230867"] = {
            ['addr'] = 0x8D,
            ['bit'] = 6,
        },
        ["1230868"] = {
            ['addr'] = 0x8D,
            ['bit'] = 7,
        },
        ["1230869"] = {
            ['addr'] = 0x8E,
            ['bit'] = 0,
        },
        ["1230870"] = {
            ['addr'] = 0x8E,
            ['bit'] = 1,
        },
        ["1230871"] = {
            ['addr'] = 0x8E,
            ['bit'] = 2,
        },
        ["1230872"] = {
            ['addr'] = 0x8E,
            ['bit'] = 3,
        },
        ["1230873"] = {
            ['addr'] = 0x8E,
            ['bit'] = 4,
        },
        ["1230874"] = {
            ['addr'] = 0x8E,
            ['bit'] = 5,
        },
        ["1230875"] = {
            ['addr'] = 0x8E,
            ['bit'] = 6,
        },
        ["1230876"] = {
            ['addr'] = 0x8E,
            ['bit'] = 7,
        },
        ["1230877"] = {
            ['addr'] = 0x8F,
            ['bit'] = 0,
        },
        ["1230878"] = {
            ['addr'] = 0x8F,
            ['bit'] = 1,
        },
        ["1230879"] = {
            ['addr'] = 0x8F,
            ['bit'] = 2,
        },
        -- EO TDL
        ["1230880"] = {
            ['addr'] = 0x8F,
            ['bit'] = 4,
        },
        ["1230881"] = {
            ['addr'] = 0x8F,
            ['bit'] = 5,
        },
        ["1230882"] = {
            ['addr'] = 0x8F,
            ['bit'] = 6,
        },
        ["1230883"] = {
            ['addr'] = 0x8F,
            ['bit'] = 7,
        },
        ["1230884"] = {
            ['addr'] = 0x90,
            ['bit'] = 0,
        },
        ["1230885"] = {
            ['addr'] = 0x90,
            ['bit'] = 1,
        },
        ["1230886"] = {
            ['addr'] = 0x90,
            ['bit'] = 2,
        },
        ["1230887"] = {
            ['addr'] = 0x90,
            ['bit'] = 3,
        },
        ["1230888"] = {
            ['addr'] = 0x90,
            ['bit'] = 4,
        },
        ["1230889"] = {
            ['addr'] = 0x90,
            ['bit'] = 5,
        },
        ["1230890"] = {
            ['addr'] = 0x90,
            ['bit'] = 6,
        },
        ["1230891"] = {
            ['addr'] = 0x90,
            ['bit'] = 7,
        },
        ["1230892"] = {
            ['addr'] = 0x91,
            ['bit'] = 0,
        },
        ["1230893"] = {
            ['addr'] = 0x91,
            ['bit'] = 1,
        },
        ["1230894"] = {
            ['addr'] = 0x91,
            ['bit'] = 2,
        },
        ["1230895"] = {
            ['addr'] = 0x91,
            ['bit'] = 3,
        },
        -- EO GI
        ["1230896"] = {
            ['addr'] = 0x91,
            ['bit'] = 5,
        },
        ["1230897"] = {
            ['addr'] = 0x91,
            ['bit'] = 6,
        },
        ["1230898"] = {
            ['addr'] = 0x91,
            ['bit'] = 7,
        },
        ["1230899"] = {
            ['addr'] = 0x92,
            ['bit'] = 0,
        },
        ["1230900"] = {
            ['addr'] = 0x92,
            ['bit'] = 1,
        },
        ["1230901"] = {
            ['addr'] = 0x92,
            ['bit'] = 2,
        },
        ["1230902"] = {
            ['addr'] = 0x92,
            ['bit'] = 3,
        },
        ["1230903"] = {
            ['addr'] = 0x92,
            ['bit'] = 4,
        },
        ["1230904"] = {
            ['addr'] = 0x92,
            ['bit'] = 5,
        },
        ["1230905"] = {
            ['addr'] = 0x92,
            ['bit'] = 6,
        },
        ["1230906"] = {
            ['addr'] = 0x92,
            ['bit'] = 7,
        },
        ["1230907"] = {
            ['addr'] = 0x93,
            ['bit'] = 0,
        },
        ["1230908"] = {
            ['addr'] = 0x93,
            ['bit'] = 1,
        },
        ["1230909"] = {
            ['addr'] = 0x93,
            ['bit'] = 2,
        },
        ["1230910"] = {
            ['addr'] = 0x93,
            ['bit'] = 3,
        },
        ["1230911"] = {
            ['addr'] = 0x93,
            ['bit'] = 4,
        },
        -- EO HFP
        ["1230912"] = {
            ['addr'] = 0x93,
            ['bit'] = 6,
        },
        ["1230913"] = {
            ['addr'] = 0x93,
            ['bit'] = 7,
        },
        ["1230914"] = {
            ['addr'] = 0x94,
            ['bit'] = 0,
        },
        ["1230915"] = {
            ['addr'] = 0x94,
            ['bit'] = 1,
        },
        ["1230916"] = {
            ['addr'] = 0x94,
            ['bit'] = 2,
        },
        ["1230917"] = {
            ['addr'] = 0x94,
            ['bit'] = 3,
        },
        ["1230918"] = {
            ['addr'] = 0x94,
            ['bit'] = 4,
        },
        ["1230919"] = {
            ['addr'] = 0x94,
            ['bit'] = 5,
        },
        ["1230920"] = {
            ['addr'] = 0x94,
            ['bit'] = 6,
        },
        ["1230921"] = {
            ['addr'] = 0x94,
            ['bit'] = 7,
        },
        ["1230922"] = {
            ['addr'] = 0x95,
            ['bit'] = 0,
        },
        ["1230923"] = {
            ['addr'] = 0x95,
            ['bit'] = 1,
        },
        ["1230924"] = {
            ['addr'] = 0x95,
            ['bit'] = 2,
        },
        ["1230925"] = {
            ['addr'] = 0x95,
            ['bit'] = 3,
        },
        ["1230926"] = {
            ['addr'] = 0x95,
            ['bit'] = 4,
        },
        ["1230927"] = {
            ['addr'] = 0x95,
            ['bit'] = 5,
        },
        -- EO CCL
        ["1230928"] = {
            ['addr'] = 0x95,
            ['bit'] = 7,
        },
        ["1230929"] = {
            ['addr'] = 0x96,
            ['bit'] = 0,
        },
        ["1230930"] = {
            ['addr'] = 0x96,
            ['bit'] = 1,
        },
        ["1230931"] = {
            ['addr'] = 0x96,
            ['bit'] = 2,
        },
        ["1230932"] = {
            ['addr'] = 0x96,
            ['bit'] = 3,
        },
        ["1230933"] = {
            ['addr'] = 0x96,
            ['bit'] = 4,
        },
        ["1230934"] = {
            ['addr'] = 0x96,
            ['bit'] = 5,
        },
        ["1230935"] = {
            ['addr'] = 0x96,
            ['bit'] = 6,
        },
        ["1230936"] = {
            ['addr'] = 0x96,
            ['bit'] = 7,
        },
        ["1230937"] = {
            ['addr'] = 0x97,
            ['bit'] = 0,
        },
        ["1230938"] = {
            ['addr'] = 0x97,
            ['bit'] = 1,
        },
        ["1230939"] = {
            ['addr'] = 0x97,
            ['bit'] = 2,
        },
        ["1230940"] = {
            ['addr'] = 0x97,
            ['bit'] = 3,
        },
        ["1230941"] = {
            ['addr'] = 0x97,
            ['bit'] = 4,
        },
        ["1230942"] = {
            ['addr'] = 0x97,
            ['bit'] = 5,
        },
        ["1230943"] = {
            ['addr'] = 0x97,
            ['bit'] = 6,
        }
    },
	["H1"] = {
	 	["1230027"] = {
			['addr'] = 0x03,
			['bit'] = 3,
            ['name'] = "Hag 1 Defeated"
		},
	},
}

-- Flags not required to send back to BTClient
local NON_AGI_MAP = {
    ["MOVES"] = {
        ["1230753"] = {
            ['addr'] = 0x1B,
            ['bit'] = 1,
            ['name'] = 'Grip Grab'
        },
        ["1230754"] = {
            ['addr'] = 0x1B,
            ['bit'] = 2,
            ['name'] = 'Breegull Blaster'
        },
        ["1230755"] = {
            ['addr'] = 0x1B,
            ['bit'] = 3,
            ['name'] = 'Egg Aim'
        },
        ["1230756"] = {
            ['addr'] = 0x1E,
            ['bit'] = 1,
            ['name'] = 'Fire Eggs'
        },
        ["1230757"] = {
            ['addr'] = 0x1B,
            ['bit'] = 6,
            ['name'] = 'Bill Drill'
        },
        ["1230758"] = {
            ['addr'] = 0x1B,
            ['bit'] = 7,
            ['name'] = 'Beak Bayonet'
        },
        ["1230759"] = {
            ['addr'] = 0x1E,
            ['bit'] = 2,
            ['name'] = 'Grenade Eggs'
        },
        ["1230760"] = {
            ['addr'] = 0x1C,
            ['bit'] = 0,
            ['name'] = 'Airborne Egg Aiming'
        },
        ["1230761"] = {
            ['addr'] = 0x1C,
            ['bit'] = 1,
            ['name'] = 'Split Up'
        },
        ["1230762"] = {
            ['addr'] = 0x1D,
            ['bit'] = 6,
            ['name'] = 'Pack Whack'
        },
        ["1230763"] = {
            ['addr'] = 0x1E,
            ['bit'] = 4,
            ['name'] = 'Ice Eggs'
        },
        ["1230764"] = {
            ['addr'] = 0x1C,
            ['bit'] = 2,
            ['name'] = 'Wing Whack'
        },
        ["1230765"] = {
            ['addr'] = 0x1C,
            ['bit'] = 3,
            ['name'] = 'Talon Torpedo'
        },
        ["1230766"] = {
            ['addr'] = 0x1C,
            ['bit'] = 4,
            ['name'] = 'Sub-Aqua Egg Aiming'
        },
        ["1230767"] = {
            ['addr'] = 0x1E,
            ['bit'] = 3,
            ['name'] = 'Clockwork Kazooie Eggs'
        },
        ["1230768"] = {
            ['addr'] = 0x1D,
            ['bit'] = 3,
            ['name'] = 'Springy Step Shoes'
        },
        ["1230769"] = {
            ['addr'] = 0x1D,
            ['bit'] = 4,
            ['name'] = 'Taxi Pack'
        },
        ["1230770"] = {
            ['addr'] = 0x1D,
            ['bit'] = 5,
            ['name'] = 'Hatch'
        },
        ["1230771"] = {
            ['addr'] = 0x1D,
            ['bit'] = 0,
            ['name'] = 'Snooze Pack'
        },
        ["1230772"] = {
            ['addr'] = 0x1D,
            ['bit'] = 1,
            ['name'] = 'Leg Spring'
        },
        ["1230773"] = {
            ['addr'] = 0x1D,
            ['bit'] = 2,
            ['name'] = 'Claw Clamber Boots'
        },
        ["1230774"] = {
            ['addr'] = 0x1C,
            ['bit'] = 6,
            ['name'] = 'Shack Pack'
        },
        ["1230775"] = {
            ['addr'] = 0x1C,
            ['bit'] = 7,
            ['name'] = 'Glide'
        },
        ["1230776"] = {
            ['addr'] = 0x1D,
            ['bit'] = 7,
            ['name'] = 'Sack Pack'
        },
        --['Fast Swimming'] = {
        --    ['addr'] = 0x1E,
        --    ['bit'] = 5,
        --    ['locationId'] = 1230777
        --},
	},
    ["MAGIC"] = {
        ["1230855"] = {
          ['addr'] = 0x6A,
          ['bit'] = 7,
          ['name'] = 'Mumbo: Golden Goliath'
        },
        ["1230856"] = {
          ['addr'] = 0x6B,
          ['bit'] = 0,
          ['name'] = 'Mumbo: Levitate'
        },
        ["1230857"] = {
          ['addr'] = 0x6B,
          ['bit'] = 1,
          ['name'] = 'Mumbo: Power'
        },
        ["1230858"] = {
          ['addr'] = 0x6B,
          ['bit'] = 2,
          ['name'] = 'Mumbo: Oxygenate'
        },
        ["1230859"] = {
          ['addr'] = 0x6B,
          ['bit'] = 3,
          ['name'] = 'Mumbo: Enlarge'
        },
        ["1230860"] = {
          ['addr'] = 0x6B,
          ['bit'] = 7,
          ['name'] = 'Mumbo: EMP'
        },
        ["1230861"] = {
          ['addr'] = 0x6B,
          ['bit'] = 4,
          ['name'] = 'Mumbo: Life Force'
        },
        ["1230862"] = {
          ['addr'] = 0x6B,
          ['bit'] = 5,
          ['name'] = 'Mumbo: Rain Dance'
        },
        ["1230863"] = {
          ['addr'] = 0x6B,
          ['bit'] = 6,
          ['name'] = 'Mumbo: Heal'
        },
        ["1230174"] = {
          ['addr'] = 0x15,
          ['bit'] = 6,
          ['name'] = 'Humba: Stony'
        },
        ["1230175"] = {
          ['addr'] = 0x15,
          ['bit'] = 7,
          ['name'] = 'Humba: Detonator'
        },
        ["1230176"] = {
          ['addr'] = 0x16,
          ['bit'] = 0,
          ['name'] = 'Humba: Money Van'
        },
        ["1230177"] = {
          ['addr'] = 0x16,
          ['bit'] = 1,
          ['name'] = 'Humba: Sub'
        },
        ["1230178"] = {
          ['addr'] = 0x16,
          ['bit'] = 2,
          ['name'] = 'Humba: T-Rex'
        },
        ["1230179"] = {
          ['addr'] = 0x16,
          ['bit'] = 3,
          ['name'] = 'Humba: Washing Machine'
        },
        ["1230180"] = {
          ['addr'] = 0x16,
          ['bit'] = 4,
          ['name'] = 'Humba: Snowball'
        },
        ["1230181"] = {
          ['addr'] = 0x16,
          ['bit'] = 5,
          ['name'] = 'Humba: Bee'
        },
        ["1230182"] = {
          ['addr'] = 0x16,
          ['bit'] = 6,
          ['name'] = 'Humba: Dragon'
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
            ['Dodgems 1v1 Flyover'] = {
				['addr'] = 0x7E,
				['bit'] = 1
			},
            ['Dodgems 2v1 Flyover'] = {
				['addr'] = 0x7E,
				['bit'] = 2
			},
            ['Dodgems 3v1 Flyover'] = {
				['addr'] = 0x7E,
				['bit'] = 3
			},
            ['MT Kickball Quarterfinal Flyover'] = {
				['addr'] = 0x7E,
				['bit'] = 4
			},
            ['MT Kickball Semifinal Flyover'] = {
				['addr'] = 0x7E,
				['bit'] = 5
			},
            ['MT Kickball Final Flyover'] = {
				['addr'] = 0x7E,
				['bit'] = 6
			},
            ['HFP Kickball Quarterfinal Flyover'] = {
				['addr'] = 0x7E,
				['bit'] = 7
			},
            ['HFP Kickball Semifinal Flyover'] = {
				['addr'] = 0x7F,
				['bit'] = 0
			},
            ['HFP Kickball Final Flyover'] = {
				['addr'] = 0x7F,
				['bit'] = 1
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
            ['Targitzan'] = {
                ['addr'] = 0x0C,
                ['bit'] = 7
            },
            ['Klungo 3'] = {
                ['addr'] = 0x11,
                ['bit'] = 7
            },
            ['Klungo 2'] = {
                ['addr'] = 0x32,
                ['bit'] = 2
            },
            ['Klungo 1'] = {
                ['addr'] = 0x13,
                ['bit'] = 1
            },
            ['Terry'] = {
                ['addr'] = 0x29,
                ['bit'] = 2
            },
            ['Weldar'] = {
                ['addr'] = 0x29,
                ['bit'] = 4
            },
            ['King Coal'] = {
                ['addr'] = 0x2A,
                ['bit'] = 1
            },
            -- ['Patches'] = {
            --     ['addr'] = 0x2A,
            --     ['bit'] = 7
            -- },
            ['Woo Fak Fak'] = {
                ['addr'] = 0x30,
                ['bit'] = 7
            },
            ['Chilly Willy'] = {
                ['addr'] = 0x35,
                ['bit'] = 3
            },
            ['Chilly Billi'] = {
                ['addr'] = 0x35,
                ['bit'] = 4
            },
            ['HAG1'] = {
                ['addr'] = 0x03,
                ['bit'] = 4
            }
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
				['bit'] = 6
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
    },
    ["TREBLE"] = {
        ["1230781"] = {
            ['addr'] = 0x86,
            ['bit'] = 7,
            ['name'] = 'MT: Treble Clef'
        },
        ["1230782"] = {
            ['addr'] = 0x89,
            ['bit'] = 0,
            ['name'] = 'GGM: Treble Clef'
        },
        ["1230783"] = {
            ['addr'] = 0x8B,
            ['bit'] = 1,
            ['name'] = 'WW: Treble Clef'
        },
        ["1230784"] = {
            ['addr'] = 0x8D,
            ['bit'] = 2,
            ['name'] = 'JRL: Treble Clef'
        },
        ["1230785"] = {
            ['addr'] = 0x8F,
            ['bit'] = 3,
            ['name'] = 'TDL: Treble Clef'
        },
        ["1230786"] = {
            ['addr'] = 0x91,
            ['bit'] = 4,
            ['name'] = 'GI: Treble Clef'
        },
        ["1230787"] = {
            ['addr'] = 0x93,
            ['bit'] = 5,
            ['name'] = 'HFP: Treble Clef'
        },
        ["1230788"] = {
            ['addr'] = 0x95,
            ['bit'] = 6,
            ['name'] = 'CCL: Treble Clef'
        },
        ["1230789"] = {
            ['addr'] = 0x97,
            ['bit'] = 7,
            ['name'] = 'JV: Treble Clef'
        },
    },
    ["STATIONS"] = {
        ["1230790"] = {
            ['addr'] = 0x27,
            ['bit'] = 3,
            ['name'] = "Train Switch GI"
        },
        ["1230791"] = {
            ['addr'] = 0x27,
            ['bit'] = 4,
            ['name'] = "Train Switch TDL"
        },
        ["1230792"] = {
            ['addr'] = 0x35,
            ['bit'] = 0,
            ['name'] = "Train Switch HFP Lava"
        },
        ["1230793"] = {
            ['addr'] = 0x34,
            ['bit'] = 7,
            ['name'] = "Train Switch HFP Ice"
        },
        ["1230794"] = {
            ['addr'] = 0x7B,
            ['bit'] = 3,
            ['name'] = "Train Switch Clifftop"
        },
        ["1230795"] = {
            ['addr'] = 0x0D,
            ['bit'] = 6,
            ['name'] = "Train Switch WW"
        }
    },
    ["CHUFFY"] = {
        ["1230796"] = {
            ['addr'] = 0x0B,
            ['bit'] = 6,
            ['name'] = "King Coal Defeated"
        },
    },
    ["JINJOFAM"] = {
        ["1230676"] = {
            ['addr'] = 0x4F,
            ['bit'] = 0,
            ['name'] = 'JV: White Jinjo Family Jiggy'
        },
        ["1230677"] = {
            ['addr'] = 0x4F,
            ['bit'] = 1,
            ['name'] = 'JV: Orange Jinjo Family Jiggy'
        },
        ["1230678"] = {
            ['addr'] = 0x4F,
            ['bit'] = 2,
            ['name'] = 'JV: Yellow Jinjo Family Jiggy'
        },
        ["1230679"] = {
            ['addr'] = 0x4F,
            ['bit'] = 3,
            ['name'] = 'JV: Brown Jinjo Family Jiggy'
        },
        ["1230680"] = {
            ['addr'] = 0x4F,
            ['bit'] = 4,
            ['name'] = 'JV: Green Jinjo Family Jiggy'
        },
        ["1230681"] = {
            ['addr'] = 0x4F,
            ['bit'] = 5,
            ['name'] = 'JV: Red Jinjo Family Jiggy'
        },
        ["1230682"] = {
            ['addr'] = 0x4F,
            ['bit'] = 6,
            ['name'] = 'JV: Blue Jinjo Family Jiggy'
        },
        ["1230683"] = {
            ['addr'] = 0x4F,
            ['bit'] = 7,
            ['name'] = 'JV: Purple Jinjo Family Jiggy'
        },
        ["1230684"] = {
            ['addr'] = 0x50,
            ['bit'] = 0,
            ['name'] = 'JV: Black Jinjo Family Jiggy'
        },
    }

}

-- Properties of world entrances and associated puzzles
local WORLD_ENTRANCE_MAP = {
    ["WORLD 1"] = {
        ["defaultName"] = "Mayahem Temple",
        ["defaultCost"] = 1,
        ["addr"] = 0x6D,
        ["bit"] = 2,
        ["puzzleFlags"] = 0x10, -- 0b00010000
        ["opened"] = false,
        ["locationId"] = "0"
    },
    ["WORLD 2"] = {
        ["defaultName"] = "Glitter Gulch Mine",
        ["defaultCost"] = 4,
        ["addr"] = 0x6D,
        ["bit"] = 3,
        ["puzzleFlags"] = 0x20, -- 0b00100000
        ["opened"] = false,
        ["locationId"] = "0"
    },
    ["WORLD 3"] = {
        ["defaultName"] = "Witchyworld",
        ["defaultCost"] = 8,
        ["addr"] = 0x6D,
        ["bit"] = 4,
        ["puzzleFlags"] = 0x30, -- 0b00110000
        ["opened"] = false,
        ["locationId"] = "0"
    },
    ["WORLD 4"] = {
        ["defaultName"] = "Jolly Roger's Lagoon",
        ["defaultCost"] = 14,
        ["addr"] = 0x6D,
        ["bit"] = 5,
        ["puzzleFlags"] = 0x40, -- 0b01000000
        ["opened"] = false,
        ["locationId"] = "0"
    },
    ["WORLD 5"] = {
        ["defaultName"] = "Terrydactyland",
        ["defaultCost"] = 20,
        ["addr"] = 0x6D,
        ["bit"] = 6,
        ["puzzleFlags"] = 0x50, -- 0b01010000
        ["opened"] = false,
        ["locationId"] = "0"
    },
    ["WORLD 6"] = {
        ["defaultName"] = "Grunty Industries",
        ["defaultCost"] = 28,
        ["addr"] = 0x6D,
        ["bit"] = 7,
        ["puzzleFlags"] = 0x60, -- 0b01100000
        ["opened"] = false,
        ["locationId"] = "0"
    },
    ["WORLD 7"] = {
        ["defaultName"] = "Hailfire Peaks",
        ["defaultCost"] = 36,
        ["addr"] = 0x6E,
        ["bit"] = 0,
        ["puzzleFlags"] = 0x70, -- 0b01110000
        ["opened"] = false,
        ["locationId"] = "0"
    },
    ["WORLD 8"] = {
        ["defaultName"] = "Cloud Cuckooland",
        ["defaultCost"] = 45,
        ["addr"] = 0x6E,
        ["bit"] = 1,
        ["puzzleFlags"] = 0x80, -- 0b10000000
        ["opened"] = false,
        ["locationId"] = "0"
    },
    ["WORLD 9"] = {
        ["defaultName"] = "Cauldron Keep",
        ["defaultCost"] = 55,
        ["addr"] = 0x6E,
        ["bit"] = 2,
        ["puzzleFlags"] = 0x90, -- 0b10010000
        ["opened"] = false,
        ["locationId"] = "0"
    },
    ["HAG 1"] = {
        ["defaultName"] = "HAG 1",
        ["defaultCost"] = 70,
        ["addr"] = 0x6E,
        ["bit"] = 3,
        ["puzzleFlags"] = 0xA0, -- 0b10100000
        ["opened"] = false,
        ["locationId"] = "0"
    },
}

function readAPLocationChecks(type)
    local checks = {}
    if type ~= "BMM"
    then
        for check_type, location in pairs(AGI_MASTER_MAP)
        do
            if USE_BMM_ONLY_TBL == true
            then
                if check_type == USE_BMM_ONLY_TYP
                then
                    for locId, value in pairs(BMM[check_type])
                    do
                        if checks[check_type] == nil
                        then
                            checks[check_type] = {}
                        end
                        checks[check_type][locId] = value
                    end
                else
                    for locId, table in pairs(location)
                    do
                        if checks[check_type] == nil
                        then
                            checks[check_type] = {}
                        end
                        checks[check_type][locId] = BTRAMOBJ:checkFlag(table['addr'], table['bit'], table['name'])
                    end
                end
            else
                for locId, table in pairs(location)
                do
                    if checks[check_type] == nil
                    then
                        checks[check_type] = {}
                    end
                    checks[check_type][locId] = BTRAMOBJ:checkFlag(table['addr'], table['bit'], table['name'])
                end
            end
        end
        return checks;
    else
        return BMM;
    end
end

function init_AGI()
    local checks = {}
    for location, value in pairs(AGI_MASTER_MAP['JIGGY'])
    do
        AGI['JIGGY'][location] = false
    end
end

---------------------------------- BKNOTES ---------------------------------

function init_BKNOTES(type) -- Initialize BMK
    local checks = {}
    for k,v in pairs(NON_AGI_MAP['TREBLE'])
    do
        if type == "BKNOTES"
        then
            BKNOTES[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_BMK")
        elseif type == "AGI"
        then
            checks[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_BMK_AGI")
        end
    end
    return checks
end

function set_checked_BKNOTES() --Only run transitioning maps
    if ASSET_MAP_CHECK["TREBLE"][CURRENT_MAP] == nil --Happens when exiting map too quickly when entering a new map
    then
        if DEBUG == true 
        then
            print("Canceling Clearing of Treble")
        end
        return false
    end
    local noteId = ASSET_MAP_CHECK["TREBLE"][CURRENT_MAP];
    local get_addr = NON_AGI_MAP['TREBLE'][noteId];
    if BKNOTES[noteId] == true
    then
        BTRAMOBJ:setFlag(get_addr['addr'], get_addr['bit'], "BKNOTES_CHECK");
    else
        BTRAMOBJ:clearFlag(get_addr['addr'], get_addr['bit'], "CLEAR_BKNOTES_CHECK");
    end
    return true;
end

function set_AP_BKNOTES() -- Only run after Transistion
    for noteId, value in pairs(AGI_NOTES)
    do
        local get_addr = NON_AGI_MAP['TREBLE'][noteId]
        if value == true
        then
            BTRAMOBJ:setFlag(get_addr['addr'], get_addr['bit'], "BKNOTES_SET");
        else
            BTRAMOBJ:clearFlag(get_addr['addr'], get_addr['bit'], "CLEAR_BKNOTES_SET");
        end
    end
end

function obtained_AP_BKNOTE()
    for locationId, value in pairs(AGI_NOTES)
    do
        if value == false
        then
            AGI_NOTES[locationId] = true;
            local get_addr = NON_AGI_MAP['TREBLE'][tostring(locationId)]
            BTRAMOBJ:setFlag(get_addr['addr'], get_addr['bit'], "BKNOTES_OBTAIN");
            break
        end
    end
end

function getTreblePlayerModel()
    if TREBLE_WAIT_TIMER <= 3
    then
        if DEBUG == true
        then
            print("Watching Treble")
        end
        TREBLE_WAIT_TIMER = TREBLE_WAIT_TIMER + 1
        return
    end
    BTMODELOBJ:changeName("Treble Clef", false)
    local object = BTMODELOBJ:checkModel();
    if object == false
    then
        BTMODELOBJ:changeName("Player", false)
        local player = BTMODELOBJ:checkModel();
        if player == false
        then
            return
        end
        if DEBUG == true
        then
            print("No Treble on Map")
            print("AP Trebles enabled")
        end
        set_AP_BKNOTES() --No Treble on this map
        CHECK_FOR_TREBLE = false
        WATCH_LOADED_TREBLE = false
        TREBLE_WAIT_TIMER = 0
        return
    end
    if DEBUG == true
    then
        print("Treble Found")
    end
    set_AP_BKNOTES();
    CHECK_FOR_TREBLE = false
    TREBLE_GONE_CHECK = 2
    WATCH_LOADED_TREBLE = true
end

function nearTreble()
    BTMODELOBJ:changeName("Treble Clef", false);
    local POS = BTMODELOBJ:getSingleModelCoords();
    if POS == false
    then
        return false
    end
    TREBLE_SPOTED = true
    TREBLE_MAP = CURRENT_MAP
    return true
end


---------------------------------- BKStation ---------------------------------

function init_BKSTATIONS(type) -- Initialize BMK
    local checks = {}
    for k,v in pairs(NON_AGI_MAP['STATIONS'])
    do
        if type == "BKSTATIONS"
        then
            BKSTATIONS[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_BMK")
        elseif type == "AGI"
        then
            checks[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_BMK_AGI")
        end
    end
    return checks
end

function set_checked_BKSTATIONS() --Only run transitioning maps
    if ASSET_MAP_CHECK["STATIONBTN"][CURRENT_MAP] == nil --Happens when exiting map too quickly when entering a new map
    then
        if DEBUG == true 
        then
            print("Canceling Clearing of Stations")
        end
        return false
    end
    local stationId = ASSET_MAP_CHECK["STATIONBTN"][CURRENT_MAP];
    local get_addr = NON_AGI_MAP['STATIONS'][stationId];
    if BKSTATIONS[stationId] == true
    then
        BTRAMOBJ:setFlag(get_addr['addr'], get_addr['bit'], "BKSTATIONS_CHECK");
    else
        BTRAMOBJ:clearFlag(get_addr['addr'], get_addr['bit'], "CLEAR_BKSTATIONS_CHECK");
    end
    return true;
end

function set_AP_STATIONS() -- Only run after Transistion
    for stationId, value in pairs(AGI_STATIONS)
    do
        local get_addr = NON_AGI_MAP['STATIONS'][stationId]
        if value == true
        then
            BTRAMOBJ:setFlag(get_addr['addr'], get_addr['bit'], "BKSTATIONS_SET");
        else
            BTRAMOBJ:clearFlag(get_addr['addr'], get_addr['bit'], "CLEAR_BKSTATIONS_SET");
        end
    end
end

function obtained_AP_STATIONS(itemId)
    AGI_STATIONS[tostring(itemId)] = true
    local get_addr = NON_AGI_MAP['STATIONS'][tostring(itemId)]
    BTRAMOBJ:setFlag(get_addr['addr'], get_addr['bit'], "BKSTATIONS_OBTAIN");
end

function getStationBtnPlayerModel()
    if STATION_BTN_TIMER <= 3
    then
        if DEBUG == true
        then
            print("Watching Station Btn")
        end
        STATION_BTN_TIMER = STATION_BTN_TIMER + 1
        return
    end
    BTMODELOBJ:changeName("Station Switch", false)
    local object = BTMODELOBJ:checkModel();
    if object == false
    then
        BTMODELOBJ:changeName("Player", false)
        local player = BTMODELOBJ:checkModel();
        if player == false
        then
            return
        end
        if DEBUG == true
        then
            print("No Button on Map")
            print("AP Stations enabled")
        end
        set_AP_STATIONS() --No Button on this map
        CHECK_FOR_STATIONBTN = false
        WATCH_LOADED_STATIONBTN = false
        STATION_BTN_TIMER = 0
        return
    end
    set_AP_STATIONS();
    local currentAnimation = BTMODELOBJ:getObjectAnimation();
    if DEBUG == true
    then
        print("Button Found")
    end
    if currentAnimation ~= 0x81 --Button Pressed
    then
        CHECK_FOR_STATIONBTN = false
        WATCH_LOADED_STATIONBTN = true
    else
        CHECK_FOR_STATIONBTN = false
    end
end

function watchBtnAnimation()
    BTMODELOBJ:changeName("Station Switch", false);
    local POS = BTMODELOBJ:getSingleModelCoords();
    if POS == false
    then
        return false
    end
    if CURRENT_MAP == nil
    then
        return
    end
    if ASSET_MAP_CHECK["STATIONBTN"][CURRENT_MAP] == nil or BKSTATIONS[ASSET_MAP_CHECK["STATIONBTN"][CURRENT_MAP]] == nil
    then
        return
    end
    local currentAnimation = BTMODELOBJ:getObjectAnimation();
    if currentAnimation ~= 0x81 -- not yet pressed
    then
        if DEBUG == true
        then
            print("Station Button not pressed")
        end
    else
        if DEBUG == true
        then
            print("Detected Station Button got pressed")
        end
        BKSTATIONS[ASSET_MAP_CHECK["STATIONBTN"][CURRENT_MAP]] = true;
        --Removed the Stop Watch here as the Stations doesn't get set right away. this will cover it at least...
        set_AP_STATIONS()
    end
end

---------------------------------- Chuffy ------------------------------------

function init_CHUFFY(type) -- Initialize BMK
    local checks = {}
    for k,v in pairs(NON_AGI_MAP['CHUFFY'])
    do
        if type == "BKCHUFFY"
        then
            BKCHUFFY[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_BMK")
        elseif type == "AGI"
        then
            checks[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_BMK_AGI")
        end
    end
    return checks
end

function set_checked_BKCHUFFY() --Only when Inside Chuffy
    local get_addr = NON_AGI_MAP['CHUFFY']["1230796"];
    if BKCHUFFY["1230796"] == false and BMM['JIGGY']["1230606"] == false
    then
        BTRAMOBJ:clearFlag(get_addr['addr'], get_addr['bit'], "CLEAR_BKCHUFFY_CHECK");
        BTRAMOBJ:setFlag(0x0D, 5, "Levitate")
    else
        BTRAMOBJ:setFlag(get_addr['addr'], get_addr['bit'], "BKCHUFFY_CHECK");
    end
end

function watchChuffyFlag()
    BTMODELOBJ:changeName("Jiggy", false)
    killedKing = BTMODELOBJ:checkModel()
    if killedKing == true
    then  -- Sanity check incase Pointer is moving
        BKCHUFFY["1230796"] = true
        CHUFFY_STOP_WATCH = true
    end
end

function set_AP_CHUFFY() -- Only run after Transistion
    local get_addr = NON_AGI_MAP['CHUFFY']["1230796"];
    if AGI_CHUFFY["1230796"] == true
    then
        BTRAMOBJ:setFlag(get_addr['addr'], get_addr['bit'], "APCHUFFY_SET");
        return true
    else
        BTRAMOBJ:clearFlag(get_addr['addr'], get_addr['bit'], "CLEAR_APCHUFFY_SET");
        return false
    end
end

function obtained_AP_CHUFFY()
    AGI_CHUFFY["1230796"] = true
    BTRAMOBJ:setFlag(0x0D, 5, "Levitate")
    local get_addr = NON_AGI_MAP['CHUFFY']["1230796"]
    if CURRENT_MAP == 0xD0 or CURRENT_MAP == 0xD1
    then
        return
    end
    BTRAMOBJ:setFlag(get_addr['addr'], get_addr['bit'], "APCHUFFY_OBTAIN");
end

function getChuffyMaps()
    if CURRENT_MAP == nil
    then
        return
    end
    if CURRENT_MAP == 0xD0 or CURRENT_MAP == 0xD1
    then
        set_checked_BKCHUFFY()
    else
        set_AP_CHUFFY()
        CHUFFY_STOP_WATCH = true
    end
    if CURRENT_MAP == 0xD1
    then
        watchChuffyFlag()
    else
        CHUFFY_STOP_WATCH = true
    end
end

function moveLevitatePad()
    BTMODELOBJ:changeName("Levitate Pad", false)
    local model = BTMODELOBJ:checkModel();
    if model == false
    then
        return false
    end
    BTMODELOBJ:moveModelObject(nil, nil, -100, nil)
    LEVI_PAD_MOVED = true;
    return true
end

---------------------------------- BKMOVES -----------------------------------

function init_BMK(type) -- Initialize BMK
    local checks = {}
    for k,v in pairs(NON_AGI_MAP['MOVES'])
    do
        if type == "BKM"
        then
            BKM[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_BMK")
        elseif type == "AGI"
        then
            checks[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_BMK_AGI")
        end
    end
    return checks
end

function update_BMK_MOVES_checks() --Only run when close to Silos
    for keys, moveId in pairs(ASSET_MAP_CHECK["SILO"][CURRENT_MAP])
    do
        if keys ~= "Exceptions"
        then
            local get_addr = NON_AGI_MAP['MOVES'][moveId]
            if BKM[moveId] == false
            then
                local res = BTRAMOBJ:checkFlag(get_addr['addr'], get_addr['bit'], "BMK_MOVES_CHECK")
                if res == true
                then
                    if DEBUG == true 
                    then
                        print("Already learnt this Silo. finished")
                    end
                    BKM[moveId] = res
                    SILOS_LOADED = true
                end
            end
        end
    end
end

function clear_AMM_MOVES_checks() --Only run when transitioning Maps until BT/Silo Model is loaded OR Close to Silo
    --Only clear the moves that we need to clear
    if ASSET_MAP_CHECK["SILO"][CURRENT_MAP] == nil --Happens when exiting map too quickly when entering a new map
    then
        if DEBUG == true 
        then
            print("Canceling Clearing of AMM Moves")
        end
        return false
    end
    for keys, moveId in pairs(ASSET_MAP_CHECK["SILO"][CURRENT_MAP])
    do
        if keys ~= "Exceptions"
        then
            local addr_info = NON_AGI_MAP["MOVES"][moveId]
            if BKM[moveId] == false
            then
                BTRAMOBJ:clearFlag(addr_info['addr'], addr_info['bit'], "CLEAR_AMM_MOVES");
            elseif BKM[moveId] == true
            then
                BTRAMOBJ:setFlag(addr_info['addr'], addr_info['bit'])
            end
        else
            for key, disable_move in pairs(ASSET_MAP_CHECK["SILO"][CURRENT_MAP][keys]) --Exception list, always disable
            do
                local addr_info = NON_AGI_MAP["MOVES"][disable_move]
                BTRAMOBJ:clearFlag(addr_info['addr'], addr_info['bit'], "CLEAR_AMM_MOVES_EXCEPTION");
            end
        end
    end
    return true
end

function set_AGI_MOVES_checks() -- SET AGI Moves into RAM AFTER BT/Silo Model is loaded
    for moveId, table in pairs(NON_AGI_MAP['MOVES'])
    do
        if AGI_MOVES[moveId] == true
        then
            BTRAMOBJ:setFlag(table['addr'], table['bit']);
        else
            BTRAMOBJ:clearFlag(table['addr'], table['bit'], "CLEAR_AGI_MOVES");
        end
    end
end

function getSiloPlayerModel()
    if SILOS_WAIT_TIMER <= 2
    then
        if DEBUG == true
        then
            print("Watching Silo")
        end
        SILOS_WAIT_TIMER = SILOS_WAIT_TIMER + 1
        return
    end
    BTMODELOBJ:changeName("Silo", false)
    local object = BTMODELOBJ:checkModel();
    if object == false
    then
        BTMODELOBJ:changeName("Player", false)
        local player = BTMODELOBJ:checkModel();
        if player == false
        then
            return
        end
        if DEBUG == true
        then
            print("No silo on Map")
            print("AP Abilities enabled")
        end
        set_AGI_MOVES_checks() --No Silo on this map
        CHECK_FOR_SILO = false
        WATCH_LOADED_SILOS = false
        SILOS_WAIT_TIMER = 0
        return
    end
    if DEBUG == true
    then
        print("Silo Found")
    end
    set_AGI_MOVES_checks()
    CHECK_FOR_SILO = false
    WATCH_LOADED_SILOS = true
end

function nearSilo()
    BTMODELOBJ:changeName("Silo", false);
    local modelPOS = BTMODELOBJ:getMultipleModelCoords()
    if modelPOS == false
    then
        return
    end
    local siloPOS = { ["Distance"] = 9999};
    for modelObjPtr, POS in pairs(modelPOS) do
        if POS ~= false
        then
            siloPOS = POS
            --Move the Silo in Witchyworld.
            if POS["Xpos"] == 0 and POS["Ypos"] == -163 and POS["Zpos"] == -1257
                and CURRENT_MAP == 0xD6
            then
                mainmemory.writefloat(modelObjPtr + 0x0C, POS["Zpos"] + 100, true);
                MoveWitchyPads();
            end

            if POS["Distance"] <= 650 and CURRENT_MAP ~= 0x1A7
            then
                if DEBUG == true and LOAD_BMK_MOVES == false
                then
                    print("Near Silo");
                end
                break;
            elseif POS["Distance"] <= 300 and CURRENT_MAP == 0x1A7
            then
                if DEBUG == true and LOAD_BMK_MOVES == false
                then
                    print("Near Silo");
                end
                break;
            end
        end
    end
   
    if siloPOS["Distance"] <= 650 -- and CURRENT_MAP ~= 0x1A7
    then
        if LOAD_BMK_MOVES == false
        then
            clear_AMM_MOVES_checks();
            update_BMK_MOVES_checks();
            LOAD_BMK_MOVES = true
        elseif SILOS_LOADED == false
        then
            -- if DEBUG == true
            -- then
            --     print("Watching BKM Moves");
            -- end
            update_BMK_MOVES_checks();
        else
            -- if DEBUG == true
            -- then
            -- print("BKM Move Learnt");
            -- end
        end
    else
        if LOAD_BMK_MOVES == true
        then
            if DEBUG == true
            then
                print("Reseting Movelist");
            end
            set_AGI_MOVES_checks();
            BMMRestoreOnly("NOTES");
            LOAD_BMK_MOVES = false;
            SILOS_LOADED = false;
        end
    end

    if ENABLE_AP_NOTES == true
    then
        if siloPOS["Distance"] <= 410 and CURRENT_MAP ~= 0x13A -- Notes and not CCL
        then
            if LOAD_SILO_NOTES == false
            then
                BMMBackupOnly("NOTES");
                useAGIOnly("NOTES");
                LOAD_SILO_NOTES = true
            end
        elseif siloPOS["Distance"] > 410 and CURRENT_MAP ~= 0x13A
        then
            if LOAD_SILO_NOTES == true
            then
                if DEBUG == true
                then
                    print("Reseting Note Count");
                end
                BMMRestoreOnly("NOTES");
                LOAD_SILO_NOTES = false;
            end
        end
        if siloPOS["Distance"] <= 260 and CURRENT_MAP == 0x13A -- Notes and CCL
        then
            if LOAD_SILO_NOTES == false
            then
                BMMBackupOnly("NOTES");
                useAGIOnly("NOTES");
                LOAD_SILO_NOTES = true
            end
        elseif siloPOS["Distance"] > 260 and CURRENT_MAP == 0x13A -- Notes and CCL
        then
            if LOAD_SILO_NOTES == true
            then
                if DEBUG == true
                then
                    print("Reseting Note Count");
                end
                BMMRestoreOnly("NOTES");
                LOAD_SILO_NOTES = false;
            end
        end
    end
end

function MoveWitchyPads()
    BTMODELOBJ:changeName("Kazooie Split Pad", false)
    local modelPOS = BTMODELOBJ:getMultipleModelCoords()
    if modelPOS == false
    then
        return;
    end
    for modelObjPtr, POS in pairs(modelPOS) do

        if (POS["Xpos"] == -125 and POS["Ypos"] == -163 and POS["Zpos"] == -1580)
            and CURRENT_MAP == 0xD6
        then
            BTModel:moveModelObject(modelObjPtr, POS["Xpos"] + 850, nil, POS["Zpos"] - 300)
            break
        end
    end
    BTMODELOBJ:changeName("Banjo Split Pad", false)
    local modelPOS = BTMODELOBJ:getMultipleModelCoords()
    if modelPOS == false
    then
        return;
    end
    for modelObjPtr, POS in pairs(modelPOS) do
        if (POS["Xpos"] == 125 and POS["Zpos"] == -1580)
            and CURRENT_MAP == 0xD6
        then
            BTMODELOBJ:moveModelObject(modelObjPtr, POS["Xpos"] + 850, nil, POS["Zpos"] - 300)
            break
        end
    end
end

------------------ Jinjos -------------------
-- Jinjos themselves are stored in MASTER_AGI_MAP
-- Famify complete checks are stored in BKJINJOFAM

function init_JinjoFam()
    for locId, table in pairs(NON_AGI_MAP["JINJOFAM"])
    do
        BKJINJOFAM[locId] = false
    end
end

function JinjoCounter() -- counts AP jinjos and Marks as Completed if true
    for locId, value in pairs(BKJINJOFAM) do
        if value == false
        then
            if locId == "1230676"
            then
                if AGI_JINJOS["1230501"] >= 1 then
                    BKJINJOFAM[locId] = true
                end
            end
            if locId == "1230677"
            then
                if AGI_JINJOS["1230502"] >= 2 then
                    BKJINJOFAM[locId] = true
                end
            end
            if locId == "1230678"
            then
                if AGI_JINJOS["1230503"] >= 3 then
                    BKJINJOFAM[locId] = true
                end
            end
            if locId == "1230679"
            then
                if AGI_JINJOS["1230504"] >= 4 then
                    BKJINJOFAM[locId] = true
                end
            end
            if locId == "1230680"
            then
                if AGI_JINJOS["1230505"] >= 5 then
                    BKJINJOFAM[locId] = true
                end
            end
            if locId == "1230681"
            then
                if AGI_JINJOS["1230506"] >= 6 then
                    BKJINJOFAM[locId] = true
                end
            end
            if locId == "1230682"
            then
                if AGI_JINJOS["1230507"] >= 7 then
                    BKJINJOFAM[locId] = true
                end
            end
            if locId == "1230683"
            then
                if AGI_JINJOS["1230508"] >= 8 then
                    BKJINJOFAM[locId] = true
                end
            end
            if locId == "1230684"
            then
                if AGI_JINJOS["1230509"] >= 9 then
                    BKJINJOFAM[locId] = true
                end
            end
        end
    end
end

function JinjoPause()
    -- Clear all Jinjo AMM Flags first, then Set. after
    for locId, value in pairs(AGI_MASTER_MAP["JINJO"])
    do
        AMM["JINJO"][locId] = false
    end
    -- 15 =  0000 1111
    -- 254 = 1111 1110
    BTRAMOBJ:setMultipleFlags(0x39, 15, 0)
    BTRAMOBJ:setMultipleFlags(0x3A, 0, 0)
    BTRAMOBJ:setMultipleFlags(0x3B, 0, 0)
    BTRAMOBJ:setMultipleFlags(0x3C, 0, 0)
    BTRAMOBJ:setMultipleFlags(0x3D, 0, 0)
    BTRAMOBJ:setMultipleFlags(0x3E, 0, 0)
    BTRAMOBJ:setMultipleFlags(0x3F, 254, 0)
    for itemId, value in pairs(AGI_JINJOS)
    do
        if value > 0
        then
            for i = 0, value - 1,1
            do
                if JINJO_PATTER_MAP[itemId][tostring(i)] == nil
                then
                    if DEBUG == true
                    then
                        print("Jinjo Overflow. Stopping Loop but everything is OK.")
                    end
                    break;
                end
                if DEBUG == true
                then
                    print("Setting Jinjo ID: " .. itemId .. " # " .. tostring(i))
                end
                AMM["JINJO"][JINJO_PATTER_MAP[itemId][tostring(i)]] = true
                AGI["JINJO"][JINJO_PATTER_MAP[itemId][tostring(i)]] = true
                BTRAMOBJ:setFlag(AGI_MASTER_MAP["JINJO"][JINJO_PATTER_MAP[itemId][tostring(i)]]['addr'],
                AGI_MASTER_MAP["JINJO"][JINJO_PATTER_MAP[itemId][tostring(i)]]['bit'])
            end
        end
    end
end


function check_open_level(show_message)  -- See if entrance conditions for a level have been met
    local jiggy_count = 0;
    for location, values in pairs(AGI_MASTER_MAP["JIGGY"])
    do
        if AGI['JIGGY'][location] == true
        then
            jiggy_count = jiggy_count + 1
        end
    end
    for location, values in pairs(WORLD_ENTRANCE_MAP)
    do
        if values["opened"] == false
        then
            if jiggy_count >= values["defaultCost"]
            then
                if DEBUG == true
                then
                    print(values["defaultName"] .. tostring(values["defaultCost"]))
                end
                BTRAMOBJ:setFlag(values["addr"], values["bit"])
                if values["locationId"] ~= "0"
                then
                    UNLOCKED_WORLDS[values["locationId"]] = true
                end
                if ENABLE_AP_WORLDS == false
                then
                    BTRAMOBJ:setMultipleFlags(0x66, 0xF, values["puzzleFlags"])
                end
                values["opened"] = true
                if (OPEN_HAG1 == true and values["defaultName"] ~= "HAG 1") or OPEN_HAG1 == false
                    and show_message == true
                then
                    table.insert(AP_MESSAGES, values["defaultName"] .. " is now unlocked!")
                    print(values["defaultName"] .. " is now unlocked!")
                end
            end
        else --Make sure its open regardless but no message
            if jiggy_count >= values["defaultCost"] and values["opened"] == true
            then
                BTRAMOBJ:setFlag(values["addr"], values["bit"])
                if ENABLE_AP_WORLDS == false
                then
                    BTRAMOBJ:setMultipleFlags(0x66, 0xF, values["puzzleFlags"])
                end
            end
        end
    end
end

function checkConsumables(consumable_type, location_checks)
    BTCONSUMEOBJ:changeConsumable(consumable_type)
	for location_name, value in pairs(AGI[consumable_type])
	do
        if(USE_BMM_TBL == false and (value == false and location_checks[consumable_type][location_name] == true))
        then
            if(DEBUG == true)
            then
                print("Obtained local consumable. Remove from Inventory")
            end
            BTCONSUMEOBJ:setConsumable(BTCONSUMEOBJ:getConsumable() - 1)
			AGI[consumable_type][location_name] = true
			savingAGI()
		end
	end
end

function loadGame(current_map)
    if(current_map == 0x142 or current_map == 0xAF)
    then
        local f = io.open("BT" .. PLAYER .. "_" .. SEED .. ".BMM", "r") -- get #BTplayer_seed.BMM
        if f==nil then
           return false
        else
            if DEBUGLVL2 == true
            then
                print("Loading BMM Files");
            end
            USE_BMM_TBL = true
            BMM = json.decode(f:read("l"));
            BKM = json.decode(f:read("l"));
            BKNOTES = json.decode(f:read("l"));
            BKSTATIONS = json.decode(f:read("l"));
            BKCHUFFY = json.decode(f:read("l"));
            BKJINJOFAM = json.decode(f:read("l"));
            f:close();
            all_location_checks("AMM");
            all_location_checks("BMM");
            BMMRestore();
            if DEBUG == true
            then
                print("Restoring from Load Game")
            end
            set_AGI_MOVES_checks();
            set_AP_BKNOTES();
            set_AP_STATIONS();
            if ENABLE_AP_CHUFFY == true -- Sanity Check
            then
                if BTRAMOBJ:checkFlag(0x98, 5) == false and BTRAMOBJ:checkFlag(0x98, 6) == false and
                BTRAMOBJ:checkFlag(0x98, 7) == false and BTRAMOBJ:checkFlag(0x99, 0) == false and
                BTRAMOBJ:checkFlag(0x99, 1) == false and BTRAMOBJ:checkFlag(0x99, 2) == false and
                BTRAMOBJ:checkFlag(0x99, 3) == false
                then
                    if DEBUG == true
                    then
                        print("Moving Chuffy to GGM")
                    end
                    BTRAMOBJ:setFlag(0x98, 5) -- Set Chuffy at GGM Station
                else
                    if DEBUG == true
                    then
                        print("Sorry, but Chuffy is at a different Station")
                    end
                end
            end
            for ap_id, itemId in pairs(receive_map) -- Sanity Check
            do
                if itemId ~= "NA"
                then
                    if (1230855 <= tonumber(itemId) and tonumber(itemId) <= 1230863) or (1230174 <= tonumber(itemId) and tonumber(itemId) <= 1230182)
                    then
                        processMagicItem(itemId);
                    end
                end
            end
            if SKIP_PUZZLES == true
            then
                check_open_level(true)
            end
            if OPEN_HAG1 == true and BTRAMOBJ:checkFlag(0x6E, 2, "WORLD_9_OPEN") == true and BTRAMOBJ:checkFlag(0x6E, 3, "HAG_1_OPEN") == false then
                BTRAMOBJ:setFlag(0x6E, 3);
                table.insert(AP_MESSAGES, "HAG 1 is now unlocked!")
                print("HAG 1 is now unlocked!")
            elseif OPEN_HAG1 == true and BTRAMOBJ:checkFlag(0x6E, 2, "WORLD_9_OPEN") == true and BTRAMOBJ:checkFlag(0x6E, 3, "HAG_1_OPEN") == true then
                table.insert(AP_MESSAGES, "HAG 1 is now unlocked!")
                print("HAG 1 is now unlocked!")
            end
            GAME_LOADED = true;
        end
    else
        if BYPASS_GAME_LOAD == true
        then
            GAME_LOADED = true;
        end
        return false;
    end
end

function MoveBathPads()
    BTMODELOBJ:changeName("Kazooie Split Pad", false)
    POS = BTMODELOBJ:getSingleModelCoords(nil)
    if POS == false
    then
        return
    end

    BTMODELOBJ:moveModelObject(nil, nil, POS["Ypos"] - 75, POS["Zpos"] + 450 );
    BTMODELOBJ:changeRotation(nil, nil, 0);

    BTMODELOBJ:changeName("Banjo Split Pad", false)
    POS = BTMODELOBJ:getSingleModelCoords(nil)
    if POS == false
    then
        return
    end
    BTMODELOBJ:moveModelObject(nil, nil, POS["Ypos"] - 75, POS["Zpos"] + 450);
    BTMODELOBJ:changeRotation(nil, nil, 0)
    BATH_PADS_QOL = true
end

function SolvingPuzzle(mapaddr) -- Avoid false checks when working on puzzles
    if CURRENT_MAP ~= 0x151 --The Temple
    then
        return false
    end
    if mapaddr == 0xC5 or mapaddr == 0xD8 or mapaddr == 0x152 or mapaddr == 0xE1
        or mapaddr == 0x154 or mapaddr == 0xF4 or mapaddr == 0x155 or mapaddr == 0x114
        or mapaddr == 0x15A or mapaddr == 0x107 or mapaddr == 0x15C or mapaddr == 0x129
        or mapaddr == 0x13A or mapaddr == 0x151 or mapaddr == 0x15D or mapaddr == 0x160
    then
        return true
    end
end

function BKLogics(mapaddr)
    BTMODELOBJ:changeName("Player", false)
    local player = BTMODELOBJ:checkModel();

    if ((CURRENT_MAP ~= mapaddr) or player == false) and ENABLE_AP_MOVES == true
    then
        WATCH_LOADED_SILOS = false
        for map,moves in pairs(ASSET_MAP_CHECK["SILO"])
        do
            if mapaddr == map
            then
                if DEBUG == true
                then
                    print("Checking Silos")
                end
                SILOS_WAIT_TIMER = 0;
                CHECK_FOR_SILO = true
            end
        end
    end
    if ((CURRENT_MAP ~= mapaddr) or player == false) and ENABLE_AP_TREBLE == true
    then
        set_checked_BKNOTES();
        TREBLE_WAIT_TIMER = 0
        CHECK_FOR_TREBLE = true
    end
    if ((CURRENT_MAP ~= mapaddr) or player == false) and ENABLE_AP_STATIONS == true
    then
        set_checked_BKSTATIONS()
        STATION_BTN_TIMER = 0
        CHECK_FOR_STATIONBTN = true
    end
    if ((CURRENT_MAP ~= mapaddr) or player == false) and ENABLE_AP_CHUFFY == true
    then
        CHUFFY_MAP_TRANS = true
    elseif ENABLE_AP_CHUFFY == false and BKCHUFFY["1230796"] == false then
        if CURRENT_MAP == 0xD1 -- Only watch for King Coal Check.
        then
            watchChuffyFlag()
        end
    end
    if CURRENT_MAP == 0xF4 and BATH_PADS_QOL == false
    then
        MoveBathPads()
    elseif  CURRENT_MAP ~= 0xF4 and BATH_PADS_QOL == true
    then
        BATH_PADS_QOL = false
    end
    -- if CURRENT_MAP == 0x1A7 and DOUBLOON_SILO_MOVE == false
    -- then
    --     MoveDoubloon()
    -- elseif DOUBLOON_SILO_MOVE == true and  CURRENT_MAP ~= 0x1A7 
    -- then
    --     DOUBLOON_SILO_MOVE = false
    -- end
    if (CURRENT_MAP ~= mapaddr)
    then
        if ENABLE_AP_JINJO == true
        then
            JinjoCounter()
        end
        client.saveram()
        if SKIP_PUZZLES == true -- another sanity check
        then
            check_open_level(false)
        end
    end
end

function BKCheckAssetLogic()
    if CHECK_FOR_SILO == true
    then
        if DEBUG == true
        then
            print("clearing all AMM moves")
        end
        local res = clear_AMM_MOVES_checks()
        if res == true
        then
            getSiloPlayerModel()
        else
            CHECK_FOR_SILO = false
            set_AGI_MOVES_checks()
        end
    end
    if CHECK_FOR_TREBLE == true
    then
        if DEBUG == true
        then
            print("clearing all AP Trebles")
        end
        local res = set_checked_BKNOTES()
        if res == true
        then
            getTreblePlayerModel()
        else
            CHECK_FOR_TREBLE = false
            set_AP_BKNOTES()
        end
    end
    if CHECK_FOR_STATIONBTN == true
    then
        if DEBUG == true
        then
            print("clearing all AP Stations")
        end
        local res = set_checked_BKSTATIONS()
        if res == true
        then
            getStationBtnPlayerModel()
        else
            CHECK_FOR_STATIONBTN = false
            set_AP_STATIONS()
        end
    end
    if (CHUFFY_MAP_TRANS == true or CHUFFY_STOP_WATCH == false or (CURRENT_MAP == 0xD7 and LEVI_PAD_MOVED == false)) and ENABLE_AP_CHUFFY == true
    then
        if AGI_CHUFFY["1230796"] == false and CURRENT_MAP == 0xD7 and LEVI_PAD_MOVED == false
        then
            moveLevitatePad()
        elseif AGI_CHUFFY["1230796"] == false and CURRENT_MAP ~= 0xD7 and LEVI_PAD_MOVED == true
        then
            LEVI_PAD_MOVED = false
        end
        CHUFFY_STOP_WATCH = false
        CHUFFY_MAP_TRANS = false
        getChuffyMaps()
    end
end

function BKAssetFound()
    if WATCH_LOADED_SILOS == true
    then
        nearSilo()
    end
    if WATCH_LOADED_TREBLE == true
    then
        res = nearTreble()
        if res == false and TREBLE_SPOTED == true and CURRENT_MAP == TREBLE_MAP and TREBLE_GONE_CHECK == 0 --Treble collected
        then
            BTMODELOBJ:changeName("Player", false)
            local player = BTMODELOBJ:checkModel();
            if player == true
            then
                BKNOTES[ASSET_MAP_CHECK["TREBLE"][TREBLE_MAP]] = true;
                TREBLE_SPOTED = false;
                WATCH_LOADED_TREBLE = false;
                set_AP_BKNOTES()
            else
                TREBLE_SPOTED = false;
                TREBLE_MAP = 0x00;
            end
        elseif res == false and TREBLE_SPOTED == true and CURRENT_MAP == TREBLE_MAP and TREBLE_GONE_CHECK > 0
        then
            TREBLE_GONE_CHECK = TREBLE_GONE_CHECK - 1
        elseif res == false and CURRENT_MAP ~= TREBLE_MAP
        then
            TREBLE_SPOTED = false;
            TREBLE_MAP = 0x00;
            WATCH_LOADED_TREBLE = false
        end
    end
    if WATCH_LOADED_STATIONBTN == true --Don't need to watch every 10 frames
    then
        watchBtnAnimation()
    end
end

function locationControl()
    local mapaddr = BTRAMOBJ:getMap()
    if mapaddr == nil --We don't want this to process anything
    then
        local DEMO = { ['DEMO'] = true}
        return DEMO
    end
    if SolvingPuzzle(mapaddr) == true
    then
        local DEMO = { ['DEMO'] = true}
        return DEMO
    end

    if USE_BMM_TBL == true --Only used If Maps are AROUND or IN Wooded Hollow or JWTemple
    then
        if BTRAMOBJ:checkFlag(0x1F, 0, "LocControl1")== true -- DEMO FILE
        then
            local DEMO = { ['DEMO'] = true}
            return DEMO
        end
        BKLogics(mapaddr)
        if ((CURRENT_MAP == 335 or CURRENT_MAP == 337) and (mapaddr ~= 335 and mapaddr ~= 337)) -- Wooded Hollow
        then
            BMMRestore()
            CURRENT_MAP = mapaddr
            return all_location_checks("AMM")
        else
            getAltar()
            nearWHJinjo()
            if ENABLE_AP_WORLDS == true
            then
                nearDisiple()
            end
            CURRENT_MAP = mapaddr
            return all_location_checks("BMM");
        end
    else
        if GAME_LOADED == false
        then
            loadGame(mapaddr)
            local DEMO = { ['DEMO'] = true}
            return DEMO
        else
            BKLogics(mapaddr)         
            if (mapaddr == 335 or mapaddr == 337) and TOTALS_MENU == false -- Wooded Hollow / JiggyTemple
            then
                if CURRENT_MAP ~= 335 and CURRENT_MAP ~= 337
                then
                    BMMBackup();
                    useAGI();
                    CURRENT_MAP = mapaddr
                end
                nearWHJinjo()
                if ENABLE_AP_WORLDS == true
                then
                    nearDisiple()
                end
                return all_location_checks("BMM");
            else
                CURRENT_MAP = mapaddr
                getAltar()
                if CLOSE_TO_ALTAR == true
                then
                    return all_location_checks("BMM");
                end
                return all_location_checks("AMM");
            end
        end
    end
end

function BMMBackup()
    if USE_BMM_TBL == true or GAME_LOADED == false
    then
        return
    end
    for item_group, table in pairs(AGI_MASTER_MAP)
    do
        if BMM[item_group] == nil then
            BMM[item_group] = {}
        end
        if USE_BMM_ONLY_TBL == true
        then
            if USE_BMM_ONLY_TYP ~= item_group
            then
                for location, values in pairs(table)
                do
                    BMM[item_group][location] = BTRAMOBJ:checkFlag(values['addr'], values['bit'], "BMMBackup");
                end
            else
                if DEBUG == true
                then
                    print("Backup excluding " .. USE_BMM_ONLY_TYP);
                end
            end
        else
            if ENABLE_AP_NOTES == false and item_group == "NOTES"
            then
                goto continue_BMM_backup
            end
            for location, values in pairs(table)
            do
                BMM[item_group][location] = BTRAMOBJ:checkFlag(values['addr'], values['bit'], "BMMBackup");
            end
        end
        ::continue_BMM_backup::
    end
    if DEBUG == true
    then
        print("Backup complete");
    end
    savingBMM()
    USE_BMM_TBL = true
end

function BMMBackupOnly(backup_type)
    if USE_BMM_TBL == true or GAME_LOADED == false or
    (USE_BMM_ONLY_TBL == true and USE_BMM_ONLY_TYP == backup_type)
    then
        return
    end
    for item_group, table in pairs(AGI_MASTER_MAP)
    do
        if BMM[item_group] == nil then
            BMM[item_group] = {}
        end
        if item_group == backup_type
        then
            for location, values in pairs(table)
            do
                BMM[item_group][location] = BTRAMOBJ:checkFlag(values['addr'], values['bit'], "BMMBackup");
            end
        end
    end
    if DEBUG == true
    then
        print("Backup " .. backup_type .. " complete");
    end
    USE_BMM_ONLY_TBL = true
    USE_BMM_ONLY_TYP = backup_type
end

function BMMRestore()
    if USE_BMM_TBL == false
    then
        return
    end

    for item_group , location in pairs(AGI_MASTER_MAP)
    do
        if USE_BMM_ONLY_TBL == true
        then
            if item_group ~= USE_BMM_ONLY_TYP
            then
                for loc,v in pairs(location)
                do
                    if AMM[item_group][loc] == false and BMM[item_group][loc] == true
                    then
                        BTRAMOBJ:setFlag(v['addr'], v['bit'])
                        AMM[item_group][loc] = BMM[item_group][loc]
                        if DEBUG == true
                        then
                            print(loc .. " Flag Set")
                        end
                    elseif AMM[item_group][loc] == true and BMM[item_group][loc] == false
                    then
                        BTRAMOBJ:clearFlag(v['addr'], v['bit'], "CLEAR_BMM_RESTORE")
                        AMM[item_group][loc] = BMM[item_group][loc]
                        if DEBUG == true
                        then
                            print(loc .. " Flag Cleared")
                        end
                    end
                end
            else
                if DEBUG == true
                then
                    print("BMM Restoring exlude " .. USE_BMM_ONLY_TYP)
                end
            end
        else
            for loc,v in pairs(location)
            do
                if AMM[item_group][loc] == false and BMM[item_group][loc] == true
                then
                    BTRAMOBJ:setFlag(v['addr'], v['bit'])
                    AMM[item_group][loc] = BMM[item_group][loc]
                    if DEBUG == true
                    then
                        print(loc .. " Flag Set")
                    end
                elseif AMM[item_group][loc] == true and BMM[item_group][loc] == false
                then
                    BTRAMOBJ:clearFlag(v['addr'], v['bit'], "CLEAR_BMM_RESTORE")
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
    USE_BMM_TBL = false;
end

function BMMRestoreOnly(backup_type)
    if USE_BMM_ONLY_TBL == false
    then
        return
    end

    for item_group , location in pairs(AGI_MASTER_MAP)
    do
        if item_group == backup_type
        then
            for loc,v in pairs(location)
            do
                if AMM[item_group][loc] == false and BMM[item_group][loc] == true
                then
                    BTRAMOBJ:setFlag(v['addr'], v['bit'])
                    AMM[item_group][loc] = BMM[item_group][loc]
                    if DEBUG == true
                    then
                        print(loc .. " Flag Set")
                    end
                elseif AMM[item_group][loc] == true and BMM[item_group][loc] == false
                then
                    BTRAMOBJ:clearFlag(v['addr'], v['bit'], "CLEAR_BMM_RESTORE_ONLY")
                    AMM[item_group][loc] = BMM[item_group][loc]
                    if DEBUG == true
                    then
                        print(loc .. " Flag Cleared")
                    end
                end
            end
            USE_BMM_ONLY_TBL = false;
            USE_BMM_ONLY_TYP = "";
            if DEBUG == true
            then
                print(backup_type .. " BMM Restored")
            end
        end
    end
end

function useAGI()
    for item_group, table in pairs(AGI_MASTER_MAP)
    do
        if ENABLE_AP_NOTES == false and item_group == "NOTES"
        then
            if DEBUG == true
            then
                print("Skipping Notes, not enabled.")
            end
            goto continue_USE_AGI
        end
        if USE_BMM_ONLY_TBL == true
        then
            if USE_BMM_ONLY_TYP ~= item_group
            then
                for location,values in pairs(table)
                do
                    if AMM[item_group][location] == false and AGI[item_group][location] == true
                    then
                        BTRAMOBJ:setFlag(values['addr'], values['bit'])
                        AMM[item_group][location] = true
                        if DEBUG == true
                        then
                            print(location .. " Flag Set from AGI");
                        end
                    elseif AMM[item_group][location] == true and AGI[item_group][location] == false
                    then
                        BTRAMOBJ:clearFlag(values['addr'], values['bit'], "CLEAR_USEAGI");
                        AMM[item_group][location] = false;
                        if DEBUG == true
                        then
                            print(location .. " Flag Cleared from AGI");
                        end
                    elseif ENABLE_AP_JINJO == true
                    then
                        if (location == "1230676" or location == "1230677" or location == "1230678" or location == "1230679"
                        or location == "1230680" or location == "1230681" or location == "1230682" or location == "1230683"
                        or location == "1230684") and AGI[item_group][location] == true
                        then
                            BTRAMOBJ:setFlag(values['addr'], values['bit'])
                            AMM[item_group][location] = true
                            if DEBUG == true
                            then
                                print(location .. " Flag Set from AGI");
                            end
                        end
                    end
                end
            else
                if DEBUG == true
                then
                    print("AGI exclude " .. USE_BMM_ONLY_TYP);
                end
            end
        else
            for location,values in pairs(table)
            do
                if AMM[item_group][location] == false and AGI[item_group][location] == true
                then
                    BTRAMOBJ:setFlag(values['addr'], values['bit'])
                    AMM[item_group][location] = true
                    if DEBUG == true
                    then
                        print(location .. " Flag Set from AGI");
                    end
                elseif AMM[item_group][location] == true and AGI[item_group][location] == false
                then
                    BTRAMOBJ:clearFlag(values['addr'], values['bit'], "CLEAR_USEAGI");
                    AMM[item_group][location] = false;
                    if DEBUG == true
                    then
                        print(location .. " Flag Cleared from AGI");
                    end
                elseif ENABLE_AP_JINJO == true
                then
                    if (location == "1230676" or location == "1230677" or location == "1230678" or location == "1230679"
                    or location == "1230680" or location == "1230681" or location == "1230682" or location == "1230683"
                    or location == "1230684") and AGI[item_group][location] == true
                    then
                        BTRAMOBJ:setFlag(values['addr'], values['bit'])
                        AMM[item_group][location] = true
                        if DEBUG == true
                        then
                            print(location .. " Flag Set from AGI");
                        end
                    end
                end
            end
        end
        ::continue_USE_AGI::
    end
end

function useAGINoJiggies()
    for location,values in pairs(AGI_MASTER_MAP["JIGGY"])
    do
        if AMM["JIGGY"][location] == true
        then
            BTRAMOBJ:clearFlag(values['addr'], values['bit'])
            AMM["JIGGY"][location] = false
            if DEBUG == true
            then
                print(location .. " Flag Cleared from AGI JIGGY");
            end
        end
    end
end

function useAGIOnly(agi_type)
    for item_group, table in pairs(AGI_MASTER_MAP)
    do
        if item_group == agi_type
        then
            for location,values in pairs(table)
            do
                if AMM[item_group][location] == false and AGI[item_group][location] == true
                then
                    BTRAMOBJ:setFlag(values['addr'], values['bit'])
                    AMM[item_group][location] = true
                    if DEBUG == true
                    then
                        print(location .. " Flag Set from AGI");
                    end
                elseif AMM[item_group][location] == true and AGI[item_group][location] == false
                then
                    BTRAMOBJ:clearFlag(values['addr'], values['bit'], "CLEAR_USEAGI");
                    AMM[item_group][location] = false;
                    if DEBUG == true
                    then
                        print(location .. " Flag Cleared from AGI");
                    end
                elseif ENABLE_AP_JINJO == true
                then
                    if (location == "1230676" or location == "1230677" or location == "1230678" or location == "1230679"
                    or location == "1230680" or location == "1230681" or location == "1230682" or location == "1230683"
                    or location == "1230684") and AGI[item_group][location] == true
                    then
                        BTRAMOBJ:setFlag(values['addr'], values['bit'])
                        AMM[item_group][location] = true
                        if DEBUG == true
                        then
                            print(location .. " Flag Set from AGI");
                        end
                    end
                end
            end
        end
    end
end

function all_location_checks(type)

    local location_checks = readAPLocationChecks(type)

    if type == "AMM"
    then
        for item_group, locations in pairs(location_checks)
        do
            if AMM[item_group] == nil
            then
                AMM[item_group] = {}
            end
            if USE_BMM_ONLY_TBL == true
            then
                if item_group ~= USE_BMM_ONLY_TYP
                then
                    for locationId, value in pairs(locations)
                    do
                        AMM[item_group][locationId] = value
                    end
                end
            else
                for locationId, value in pairs(locations)
                do
                    AMM[item_group][locationId] = value
                end
            end
        end
    end
    if next(AGI) == nil then --Only runs first time starting the game.
        for item_group, locations in pairs(location_checks)
        do
             if AGI[item_group] == nil
             then
                 AGI[item_group] = {}
             end  
             for locationId, value in pairs(locations)
             do
                 AGI[item_group][locationId] = value
             end
        end
    end

    if ENABLE_AP_HONEYCOMB == true then
        checkConsumables('HONEYCOMB', location_checks)
    end

    if ENABLE_AP_PAGES == true then
        checkConsumables('CHEATO', location_checks)
    end
    checkConsumables('GLOWBO', location_checks)
    checkConsumables('MEGA GLOWBO', location_checks)
    if ENABLE_AP_DOUBLOONS == true then
        checkConsumables('DOUBLOON', location_checks)
    end

    return location_checks
end

function processMessages()
    if next(AP_MESSAGES) ~= nil
    then
        if TEXT_START == false
        then
            message = table.remove(AP_MESSAGES)
            archipelago_msg_box(message)
        end
    end
end

function archipelago_msg_box(msg)
        bgcolor = "#FC6600"
        brcolor = "#000000"
        if TEXT_START == false
        then
            gui.drawText(300, 1500, msg, bgcolor, bgcolor, 40)
            TEXT_START = true
        end
end

function clearText()
    if TEXT_TIMER > 0
    then
        TEXT_TIMER = TEXT_TIMER - 1
    else
        gui.clearGraphics()
        TEXT_TIMER = 2
        TEXT_START = false
    end
end

function processMagicItem(loc_ID)
    for location, table in pairs(NON_AGI_MAP['MAGIC'])
    do
        if location == tostring(loc_ID)
        then
            BTRAMOBJ:setFlag(table['addr'], table['bit'])
--            archipelago_msg_box("Received " .. location);
        end
    end

end

function processAGIItem(item_list)
    for ap_id, memlocation in pairs(item_list) -- Items unrelated to AGI_MAP like Consumables
    do
        if receive_map[tostring(ap_id)] == nil
        then
            if(memlocation == 1230512 and ENABLE_AP_HONEYCOMB == true)  -- Honeycomb Item
            then
                if DEBUG == true
                then
                    print("HC Obtained")
                end
                BTCONSUMEOBJ:changeConsumable("HONEYCOMB");
                BTCONSUMEOBJ:setConsumable(BTCONSUMEOBJ:getConsumable() + 1);
 --               archipelago_msg_box("Received Honeycomb");
            elseif(memlocation == 1230513 and ENABLE_AP_PAGES == true) -- Cheato Item
            then
                if DEBUG == true
                then
                    print("Cheato Page Obtained")
                end
                BTCONSUMEOBJ:changeConsumable("CHEATO");
                BTCONSUMEOBJ:setConsumable(BTCONSUMEOBJ:getConsumable() + 1);
 --               archipelago_msg_box("Received Cheato Page");
            elseif(memlocation == 1230515)
            then
                if DEBUG == true
                then
                    print("Jiggy Obtained")
                end
                for location, values in pairs(AGI_MASTER_MAP["JIGGY"])
                do
                    if AGI['JIGGY'][location] == false
                    then
                        AGI['JIGGY'][location] = true
                        break
                    end
                end
                if SKIP_PUZZLES == true then
                    check_open_level(true) -- check if the current jiggy count opens a new level
                end
            elseif((1230855 <= memlocation and memlocation <= 1230863) or (1230174 <= memlocation and memlocation <= 1230182))
            then
                processMagicItem(memlocation)
            elseif(1230753 <= memlocation and memlocation <= 1230777)
            then
                if DEBUG == true
                then
                    print("Move Obtained")
                end
                for location, values in pairs(NON_AGI_MAP["MOVES"])
                do
                    if AGI_MOVES[location] == false and location == tostring(memlocation)
                    then
                        AGI_MOVES[location] = true
                        if NON_AGI_MAP["MOVES"][location]['name'] == ('Fire Eggs')
                        then
                            BTCONSUMEOBJ:changeConsumable("FIRE EGGS")
                            BTCONSUMEOBJ:setConsumable(50)
                        elseif NON_AGI_MAP["MOVES"][location]['name'] == ('Grenade Eggs')
                        then
                            BTCONSUMEOBJ:changeConsumable("GRENADE EGGS")
                            BTCONSUMEOBJ:setConsumable(25)
                        elseif NON_AGI_MAP["MOVES"][location]['name'] == ('Ice Eggs')
                        then
                            BTCONSUMEOBJ:changeConsumable("ICE EGGS")
                            BTCONSUMEOBJ:setConsumable(50)
                        elseif NON_AGI_MAP["MOVES"][location]['name'] == ('Clockwork Kazooie Eggs')
                        then
                            BTCONSUMEOBJ:changeConsumable("CWK EGGS")
                            BTCONSUMEOBJ:setConsumable(10)
                        end
                        set_AGI_MOVES_checks()
                    end
                end
            elseif(memlocation == 1230514 and ENABLE_AP_DOUBLOONS == true) -- Doubloon Item
            then
                if DEBUG == true
                then
                    print("Doubloon Obtained")
                end
                BTCONSUMEOBJ:changeConsumable("DOUBLOON");
                BTCONSUMEOBJ:setConsumable(BTCONSUMEOBJ:getConsumable() + 1);
            elseif(memlocation == 1230778 and ENABLE_AP_TREBLE == true) -- Treble Clef
            then
                obtained_AP_BKNOTE();
            elseif(1230790 <= memlocation and memlocation <= 1230795) and ENABLE_AP_STATIONS == true -- Station Btns
            then
                obtained_AP_STATIONS(memlocation);
            elseif memlocation == 1230796 and ENABLE_AP_CHUFFY == true
            then
                obtained_AP_CHUFFY()
            elseif( 1230501 <= memlocation and memlocation <= 1230509) and ENABLE_AP_JINJO == true
            then
                AGI_JINJOS[tostring(memlocation)] = AGI_JINJOS[tostring(memlocation)] + 1
                JinjoCounter() -- check and see if family completes and mark true
            elseif(memlocation == 1230797) and ENABLE_AP_NOTES == true
            then
                if DEBUG == true
                then
                    print("5 Notes Obtained")
                end
                for location, values in pairs(AGI_MASTER_MAP["NOTES"])
                do
                    if AGI['NOTES'][location] == false
                    then
                        AGI['NOTES'][location] = true
                        break
                    end
                end
            end
            receive_map[tostring(ap_id)] = tostring(memlocation)
            savingAGI();
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
    if next(block['messages']) ~= nil
    then
        for k, message in pairs(block['messages'])
        do
            table.insert(AP_MESSAGES, message)
        end
    end
--     if block['triggerDeath'] == true
--     then
--         KILL_BANJO = true;
--     end

    if DEBUGLVL3 == true then
        print(block)
    end
end

function SendToBTClient()
    local retTable = {}
    retTable["scriptVersion"] = SCRIPT_VERSION;
    retTable["playerName"] = PLAYER;
    retTable["deathlinkActive"] = DEATH_LINK;
    retTable['locations'] = locationControl()
    retTable['unlocked_moves'] = BKM;
    retTable['treble'] = BKNOTES;
    retTable['stations'] = BKSTATIONS;
    retTable['chuffy'] = BKCHUFFY;
    retTable["isDead"] = DETECT_DEATH;
    retTable["jinjofam"] = BKJINJOFAM;
    retTable["worlds"] = UNLOCKED_WORLDS;
    if GAME_LOADED == false
    then
        retTable["sync_ready"] = "false"
    else
        retTable["sync_ready"] = "true"
    end
    if DEBUGLVL3 == true
    then
        print("Send Data")
    end

    local msg = json.encode(retTable).."\n"
    local ret, error = BT_SOCK:send(msg)
    if ret == nil then
        print(error)
    elseif CUR_STATE == STATE_INITIAL_CONNECTION_MADE then
        CUR_STATE = STATE_TENTATIVELY_CONNECTED
    elseif CUR_STATE == STATE_TENTATIVELY_CONNECTED then
        archipelago_msg_box("Connected to the Banjo Tooie Client!");
        print("Connected!")
        CUR_STATE = STATE_OK
    end
end

function receive()
    if PLAYER == "" and SEED == 0
    then
        getSlotData()
    else
        -- Send the message
        SendToBTClient()

        l, e = BT_SOCK:receive()
        -- Handle incoming message
        if e == 'closed' then
            if CUR_STATE == STATE_OK then
                archipelago_msg_box("Connection closed")
                print("Connection closed")
            end
            CUR_STATE = STATE_UNINITIALIZED
            return
        elseif e == 'timeout' then
            archipelago_msg_box("timeout")
            print("timeout")
            return
        elseif e ~= nil then
            print(e)
            CUR_STATE = STATE_UNINITIALIZED
            return
        end
        if DEBUGLVL3 == true
        then
            print("Processing Block");
        end
        process_block(json.decode(l))
        if DEBUGLVL3 == true
        then
            print("Finish");
        end
        -- if DETECT_DEATH == true
        -- then
        --     DETECT_DEATH = false;
        -- end
    end
end

function checkPause()
    local pause_menu = mainmemory.readbyte(0x15961A);
    if pause_menu == 1 and PAUSED == false
    then
        if DEBUG == true
        then
            print("Game Paused");
        end
        BMMBackup();
        useAGI();
        if ENABLE_AP_JINJO == true
        then
            JinjoPause();
        end
        PAUSED = true;
    elseif pause_menu == 0 and PAUSED == true  -- unpaused
    then
        PAUSED = false
        if DEBUG == true
        then
            print("Game Unpaused");
        end
        if CURRENT_MAP ~= 335 and CURRENT_MAP ~= 337  -- Don't want to restore while in WH zone
        then
            BMMRestore()
        end
    elseif PAUSED == true and DEBUG == true
    then
        local check_controls = joypad.get()
        if check_controls ~= nil and check_controls['P1 Z'] == true
        then
            print("AGI TABLE:");
            for item_group, table in pairs(AGI)
            do
                for locationId, value in pairs(table)
                do
                    if(value == true)
                    then
                        print(AGI_MASTER_MAP[item_group][locationId]['name'] .. ":" .. tostring(value))
                    end
                end
            end
        elseif check_controls ~= nil and check_controls['P1 C Right'] == true
        then
            print("BMM TABLE:");
            for item_group, table in pairs(BMM)
            do
                for locationId, value in pairs(table)
                do
                    if(value == true)
                    then
                        print(AGI_MASTER_MAP[item_group][locationId]['name'] .. ":" .. tostring(value))
                    end
                end
            end
        elseif check_controls ~= nil and check_controls['P1 C Left'] == true
        then
            print("AMM TABLE:");
            for item_group, table in pairs(AMM)
            do
                for locationId, value in pairs(table)
                do
                    if(value == true)
                    then
                        print(AGI_MASTER_MAP[item_group][locationId]['name'] .. ":" .. tostring(value))
                    end
                end
            end
        elseif check_controls ~= nil and check_controls['P1 C Up'] == true
        then
            print("BKM TABLE + Actual:");
            for locationId, values in pairs(NON_AGI_MAP["MOVES"])
            do             
                local res = BTRAMOBJ:checkFlag(values['addr'], values['bit'], "PAUSE MOVE DEBUG");
                print(NON_AGI_MAP["MOVES"][locationId]['name'] .. ":" .. tostring(res))
                print("Checked? : " .. tostring(BKM[locationId]))
                print("AGI? : " .. tostring(AGI_MOVES[locationId]))
                print("------------------------");
            end
        end
    end
end

function checkTotalMenu()
    if PAUSED == false
    then
        return
    else
        local total = mainmemory.readbyte(0x123C48);
        if TOTALS_MENU == false and total == 1
        then
            if DEBUG == true
            then
                print("Checking Game Totals");
            end
            TOTALS_MENU = true;
            BMMRestore();
        elseif TOTALS_MENU == true and total ~= 1
        then
            if DEBUG == true
            then
                print("no longer checking Game Totals");
            end
            TOTALS_MENU = false;
            BMMBackup();
            useAGI();
        end
    end
end

function DPadStats()
    if GAME_LOADED == true
    then
        local check_controls = joypad.get()
        
		if check_controls ~= nil and check_controls['P1 DPad U'] == true and SNEAK == false
        then
            joypad.setanalog({['P1 Y Axis'] = 18 })
            SNEAK = true
        elseif check_controls ~= nil and check_controls['P1 DPad U'] == false and SNEAK == true
        then
            joypad.setanalog({['P1 Y Axis'] = '' })
            SNEAK = false
        end
		
		if check_controls ~= nil and check_controls['P1 DPad R'] == true and check_controls['P1 L'] == false
        then
            print(" ")
            print(" ")
            print("Unlocked Moves:")
            for locationId, values in pairs(NON_AGI_MAP["MOVES"])
            do             
                if AGI_MOVES[locationId] == true
                then
                    print(values['name'])
                end
            end
		end
		
		if check_controls ~= nil and check_controls['P1 DPad L'] == true and check_controls['P1 L'] == false
        then
            print(" ")
            print(" ")
            print("Unlocked Magic:")
            for locationId, values in pairs(NON_AGI_MAP["MAGIC"])
            do        
                local results = BTRAMOBJ:checkFlag(values['addr'], values['bit'])
                if results == true then
                    print(values['name'])
                end
            end
        end
		
		if check_controls ~= nil and check_controls['P1 DPad D'] == true and check_controls['P1 L'] == false
        then
            print(" ")
            print(" ")
            print("Collected Treble Clefs:")
            for locationId, values in pairs(NON_AGI_MAP["TREBLE"])
            do        
                local results = BTRAMOBJ:checkFlag(values['addr'], values['bit'])
                if results == true then
                    print(values['name'])
                end
            end
			print(" ")
			print("Opened Train Stations:")
            for locationId, values in pairs(NON_AGI_MAP["STATIONS"])
            do        
                local results = BTRAMOBJ:checkFlag(values['addr'], values['bit'])
                if results == true then
                    print(values['name'])
                end
            end
        end
		
        if check_controls ~= nil and check_controls['P1 DPad U'] == true and check_controls['P1 L'] == true
        then
			BTCONSUMEOBJ:changeConsumable("Red Feathers")
			BTCONSUMEOBJ:setConsumable(100)
			BTCONSUMEOBJ:changeConsumable("Gold Feathers")
			BTCONSUMEOBJ:setConsumable(10)
			BTCONSUMEOBJ:changeConsumable("BLUE EGGS")
			BTCONSUMEOBJ:setConsumable(100)
			BTCONSUMEOBJ:changeConsumable("FIRE EGGS")
			BTCONSUMEOBJ:setConsumable(50)
            BTCONSUMEOBJ:changeConsumable("GRENADE EGGS")
            BTCONSUMEOBJ:setConsumable(25)
            BTCONSUMEOBJ:changeConsumable("ICE EGGS")
            BTCONSUMEOBJ:setConsumable(50)
            BTCONSUMEOBJ:changeConsumable("CWK EGGS")
            BTCONSUMEOBJ:setConsumable(10)
			print(" ")
			print("Eggs and Feathers Refilled")
        end

        if check_controls ~= nil and check_controls['P1 DPad R'] == true and check_controls['P1 L'] == true and SUPERBANJO == false
        then
           BTRAMOBJ:setFlag(0xA2, 2, "Super Banjo")
           SUPERBANJO = true
           print(" ")
           print("Super Banjo Enabled")
        elseif check_controls ~= nil and check_controls['P1 DPad R'] == true and check_controls['P1 L'] == true and SUPERBANJO == true
        then
            BTRAMOBJ:clearFlag(0xA2, 2)
            SUPERBANJO = false
            print(" ")
            print("Super Banjo Disabled")
        end

        if check_controls ~= nil and check_controls['P1 DPad L'] == true and check_controls['P1 L'] == true and AIMASSIST == false
        then
           BTRAMOBJ:setFlag(0xAF, 3, "Aim Assist")
           AIMASSIST = true
           print(" ")
           print("Aim Assist Enabled")
        elseif check_controls ~= nil and check_controls['P1 DPad L'] == true and check_controls['P1 L'] == true and AIMASSIST == true
        then
            BTRAMOBJ:clearFlag(0xAF, 3)
            AIMASSIST = false
            print(" ")
            print("Aim Assist Disabled")
        end
		
		if check_controls ~= nil and check_controls['P1 DPad D'] == true and check_controls['P1 L'] == true and REGEN == false
        then
           BTRAMOBJ:setFlag(0xA1, 7, "Automatic Energy Regain")
           REGEN = true
           print(" ")
           print("Automatic Energy Regain Enabled")
        elseif check_controls ~= nil and check_controls['P1 DPad D'] == true and check_controls['P1 L'] == true and REGEN == true
        then
            BTRAMOBJ:clearFlag(0xA1, 7)
            REGEN = false
            print(" ")
            print("Automatic Energy Regain Disabled")
        end
    end
end

function savingAGI()
    local f = io.open("BT" .. PLAYER .. "_" .. SEED .. ".AGI", "w") --generate #BTplayer_seed.AGI
    if DEBUGLVL2 == true
    then
        print("Writing AGI File from Saving");
        print(AGI)
        print(AGI["HONEYCOMB"]);
        print(receive_map)
    end
    f:write(json.encode(AGI) .. "\n");
    if DEBUGLVL2 == true
    then
        print("Writing AGI MOVES from Saving");
    end
    f:write(json.encode(AGI_MOVES) .. "\n");
    if DEBUGLVL2 == true
    then
        print("Writing Treble");
    end
    f:write(json.encode(AGI_NOTES) .. "\n");
    if DEBUGLVL2 == true
    then
        print("Writing Stations");
    end
    f:write(json.encode(AGI_STATIONS) .. "\n");
    if DEBUGLVL2 == true
    then
        print("Writing Chuffy");
    end
    f:write(json.encode(AGI_CHUFFY) .. "\n");
    if DEBUGLVL2 == true
    then
        print("Writing JINJOS");
    end
    f:write(json.encode(AGI_JINJOS) .. "\n");
    if DEBUGLVL2 == true
    then
        print("Writing Received_Map");
    end
    f:write(json.encode(receive_map))
    f:close()
    if DEBUG == true
    then
        print("AGI Table Saved");
    end
end

function loadAGI()
    local f = io.open("BT" .. PLAYER .. "_" .. SEED .. ".AGI", "r") --generate #BTplayer_seed.AGI
    if f==nil then
        AGI = all_location_checks("AGI");
        if next(AGI_MOVES) == nil then
            AGI_MOVES = init_BMK("AGI");
        end
        if next(AGI_NOTES) == nil then
            AGI_NOTES = init_BKNOTES("AGI");
        end
        if next(AGI_STATIONS) == nil then
            AGI_STATIONS = init_BKSTATIONS("AGI");
        end
        if next(AGI_CHUFFY) == nil then
            AGI_CHUFFY = init_CHUFFY("AGI");
        end
        f = io.open("BT" .. PLAYER .. "_" .. SEED .. ".AGI", "w");
        if DEBUGLVL2 == true
        then
            print("Writing AGI File from LoadAGI");
            print(AGI);
        end
        f:write(json.encode(AGI).."\n");
        f:write(json.encode(AGI_MOVES).."\n");
        f:write(json.encode(AGI_NOTES).."\n");
        f:write(json.encode(AGI_STATIONS) .. "\n");
        f:write(json.encode(AGI_CHUFFY) .. "\n");
        f:write(json.encode(AGI_JINJOS) .. "\n");
        f:write(json.encode(receive_map));
        f:close();
    else
        if DEBUGLVL2 == true
        then
            print("Loading AGI File");
        end
        AGI = json.decode(f:read("l"));
        AGI_MOVES = json.decode(f:read("l"));
        AGI_NOTES = json.decode(f:read("l"));
        AGI_STATIONS = json.decode(f:read("l"));
        AGI_CHUFFY = json.decode(f:read("l"));
        AGI_JINJOS = json.decode(f:read("l"));
        receive_map = json.decode(f:read("l"));
        f:close();
    end
end

function savingBMM()
    local f = io.open("BT" .. PLAYER .. "_" .. SEED .. ".BMM", "w") --generate #BTplayer_seed.AGI
    if DEBUGLVL2 == true
    then
        print("Saving BMM File");
    end
    f:write(json.encode(BMM) .. "\n");
    f:write(json.encode(BKM) .. "\n");
    f:write(json.encode(BKNOTES) .. "\n");
    f:write(json.encode(BKSTATIONS) .. "\n");
    f:write(json.encode(BKCHUFFY) .. "\n");
    f:write(json.encode(BKJINJOFAM));
    f:close()
    if DEBUG == true
    then
        print("BMM Table Saved");
    end
end

function gameSaving()
    if PAUSED ~= true
    then
        return
    else
        -- local save_game = mainmemory.read_u8(0x05F450);
        local save_game2 = mainmemory.read_u8(0x044A81);
        if save_game2 == 1
        then
            SAVE_GAME = true
            if DEBUG == true
            then
                print("Game Entering Save State")
            end
        end
    end
end

function getSlotData()
    local retTable = {}
    retTable["getSlot"] = true;
    if DEBUGLVL2 == true
    then
        print("Encoding getSlot");
    end
    local msg = json.encode(retTable).."\n"
    local ret, error = BT_SOCK:send(msg)
    l, e = BT_SOCK:receive()
    -- Handle incoming message
    if e == 'closed' then
        if CUR_STATE == STATE_OK then
            archipelago_msg_box("Connection closed")
            print("Connection closed")
        end
        CUR_STATE = STATE_UNINITIALIZED
        return
    elseif e == 'timeout' then
        archipelago_msg_box("timeout")
        print("timeout")
        return
    elseif e ~= nil then
        print(e)
        CUR_STATE = STATE_UNINITIALIZED
        return
    end
    if DEBUGLVL2 == true
    then
        print("Processing Slot Data");
    end
    process_slot(json.decode(l))
end

function process_slot(block)
    
    if DEBUGLVL3 == true then
        print(block)
    end

    if block['slot_player'] ~= nil and block['slot_player'] ~= ""
    then
        PLAYER = block['slot_player']
    end
    if block['slot_seed'] ~= nil and block['slot_seed'] ~= ""
    then
        SEED = block['slot_seed']
    end
    if block['slot_deathlink'] ~= nil and block['slot_deathlink'] ~= "false"
    then
        DEATH_LINK = true
    end
    if block['slot_skip_tot'] ~= nil and block['slot_skip_tot'] ~= ""
    then
        SKIP_TOT = block['slot_skip_tot']
    end
    if block['slot_honeycomb'] ~= nil and block['slot_honeycomb'] ~= "false"
    then
        ENABLE_AP_HONEYCOMB = true
    end
	if block['slot_pages'] ~= nil and block['slot_pages'] ~= "false"
    then
        ENABLE_AP_PAGES = true
    end
    if block['slot_moves'] ~= nil and block['slot_moves'] ~= "false"
    then
        ENABLE_AP_MOVES = true
    end
    if block['slot_doubloon'] ~= nil and block['slot_doubloon'] ~= "false"
    then
        ENABLE_AP_DOUBLOONS = true
    end
    if block['slot_minigames'] ~= nil and block['slot_minigames'] ~= ""
    then
        MINIGAMES = block['slot_minigames']
    end
    if block['slot_treble'] ~= nil and block['slot_treble'] ~= "false"
    then
        ENABLE_AP_TREBLE = true
    end
    if block['slot_skip_puzzles'] ~= nil and block['slot_skip_puzzles'] ~= "false"
    then
        SKIP_PUZZLES = true
    end
    if block['slot_open_hag1'] ~= nil and block['slot_open_hag1'] ~= "false"
    then
        OPEN_HAG1 = true
    end
    if block['slot_stations'] ~= nil and block['slot_stations'] ~= "false"
    then
        ENABLE_AP_STATIONS = true
    end
    if block['slot_chuffy'] ~= nil and block['slot_chuffy'] ~= "false"
    then
        ENABLE_AP_CHUFFY = true
    end
    if block['slot_jinjo'] ~= nil and block['slot_jinjo'] ~= "false"
    then
        ENABLE_AP_JINJO = true
    end
    if block['slot_worlds'] ~= nil and block['slot_worlds'] ~= "false"
    then
        ENABLE_AP_WORLDS = true
    end
    if block['slot_notes'] ~= nil and block['slot_notes'] ~= "false"
    then
        ENABLE_AP_NOTES = true
    end
    if block['slot_world_order'] ~= nil
    then
        local REORG_WORLDS = { }
        local starting_location_id = 1230944
        local locationId = starting_location_id
        
        for location, jiggy_amt in pairs(block['slot_world_order'])
        do
            table.insert(REORG_WORLDS, {location, tonumber(jiggy_amt)}) --Convert to table to sort based on lowest Jiggy count
        end

        table.sort(REORG_WORLDS, function(a, b)
            return a[2] < b[2]
        end)

        for key, table in pairs(REORG_WORLDS)
        do
            local location = table[1]
            local jiggy_amt = tonumber(table[2])

            if location == "Outside Grunty's Industries"
            then
                location = "Grunty Industries"
            end
            for worlds, t in pairs(WORLD_ENTRANCE_MAP)
            do
                if t['defaultName'] == location
                then
                    WORLD_ENTRANCE_MAP[worlds]["defaultCost"] = jiggy_amt
                    WORLD_ENTRANCE_MAP[worlds]["locationId"] = tostring(locationId)
                    locationId = locationId + 1
                end
            end
        end
    end
    if SEED ~= 0
    then
        loadAGI()
    else
        return false
    end
    return true
end


function initializeFlags()
	-- Use Cutscene: "2 Years Have Passed..." to check for fresh save
	local current_map = BTRAMOBJ:getMap();
	if (current_map == 0xA1) then
		-- First Time Pickup Text
		for i = 0, 7 do
			BTRAMOBJ:setFlag(0x00, i) -- Note, Glowbo, Eggs, Feathers, Treble Clef, Honeycomb
		end	
		BTRAMOBJ:setFlag(0x01, 2) -- Empty Honeycomb
		BTRAMOBJ:setFlag(0x01, 5) -- Jinjo
		BTRAMOBJ:setFlag(0x07, 7) -- Cheato Page
		BTRAMOBJ:setFlag(0x27, 5) -- Doubloon
		BTRAMOBJ:setFlag(0x2E, 7) -- Ticket
		-- Character Introduction Text
		for k,v in pairs(NON_AGI_MAP['SKIP']['INTRO'])
        do
            BTRAMOBJ:setFlag(v['addr'], v['bit'])
        end
		-- Cutscene Flags
		for k,v in pairs(NON_AGI_MAP['SKIP']['CUTSCENE'])
        do
            BTRAMOBJ:setFlag(v['addr'], v['bit'])
        end
		-- Tutorial Dialogues
		for k,v in pairs(NON_AGI_MAP['SKIP']['TUTORIAL'])
        do
            BTRAMOBJ:setFlag(v['addr'], v['bit'])
        end
		-- Minigame Doors
		BTRAMOBJ:setFlag(0xA9, 6) -- MT Kickball
		BTRAMOBJ:setFlag(0xA9, 7) -- HFP Kickball
        if MINIGAMES == "skip"
        then
            BTRAMOBJ:setFlag(0x06, 6) -- MT Semifinal
            BTRAMOBJ:setFlag(0x06, 7) -- MT Final
            BTRAMOBJ:setFlag(0x68, 0) -- HFP Semifinal
            BTRAMOBJ:setFlag(0x68, 1) -- HFP Final
            BTRAMOBJ:setFlag(0x10, 1) -- Dodgems 1v1 Complete
            BTRAMOBJ:setFlag(0x10, 2) -- Dodgems 2v1 Complete
            BTRAMOBJ:setFlag(0x10, 3) -- Dodgems 1v1 Door
            BTRAMOBJ:setFlag(0x10, 4) -- Dodgems 2v1 Door
            BTRAMOBJ:setFlag(0x10, 5) -- Dodgems 3v1 Door
        end
        if ENABLE_AP_CHUFFY == true
        then
            BTRAMOBJ:setFlag(0x98, 5) -- Set Chuffy at GGM Station
        end
        GAME_LOADED = true  -- We don't have a real BMM at this point.  
        init_BMK("BKM");
        init_BKNOTES("BKNOTES");
        init_BKSTATIONS("BKSTATIONS");
        init_CHUFFY("BKCHUFFY");
        init_JinjoFam();
        init_AGI()
        AGI_MOVES = init_BMK("AGI");
        AGI_NOTES = init_BKNOTES("AGI");
        receive_map = { -- initialize incase suffered a hard crash and losing save file.
        ["NA"] = "NA"
        }
		if (SKIP_TOT ~= "false") then
			-- ToT Misc Flags
			BTRAMOBJ:setFlag(0xAB, 2)
			BTRAMOBJ:setFlag(0xAB, 3)
			BTRAMOBJ:setFlag(0xAB, 4)
			BTRAMOBJ:setFlag(0xAB, 5)
			if (SKIP_TOT == "true") then
			-- ToT Complete Flags
                BTRAMOBJ:setFlag(0x83, 0)
                BTRAMOBJ:setFlag(0x83, 4)
			else
				BTRAMOBJ:setFlag(0x83, 2)
				BTRAMOBJ:setFlag(0x83, 3)
			end
		end
        all_location_checks("AMM")
        BMMBackup()
        BMMRestore()
		INIT_COMPLETE = true
        if SKIP_PUZZLES == true then
            check_open_level(true) -- sanity check that level open flags are still set
        end
        if OPEN_HAG1 == true and BTRAMOBJ:checkFlag(0x6E, 2, "WORLD_9_OPEN") == true and BTRAMOBJ:checkFlag(0x6E, 3, "HAG_1_OPEN") == false then
            BTRAMOBJ:setFlag(0x6E, 3);
            table.insert(AP_MESSAGES, "HAG 1 is now unlocked!")
            print("HAG 1 is now unlocked!")
        elseif OPEN_HAG1 == true and BTRAMOBJ:checkFlag(0x6E, 2, "WORLD_9_OPEN") == true and BTRAMOBJ:checkFlag(0x6E, 3, "HAG_1_OPEN") == true then
            table.insert(AP_MESSAGES, "HAG 1 is now unlocked!")
            print("HAG 1 is now unlocked!")
        end
        if ENABLE_AP_JINJO == true then
            -- 129 is 1000 0001
            -- 2 is   0000 0010
            if DEBUG == true
            then
                print("Setting Jinjo Pattern")
            end
            BTRAMOBJ:setMultipleFlags(0x6A, 129, 2)
        end

        
	-- Otherwise, the flags were already set, so just stop checking
	elseif (current_map == 0xAF or current_map == 0x142) then
		INIT_COMPLETE = true
    elseif current_map == 0x158 and INIT_COMPLETE == true
    then
        INIT_COMPLETE = false
	end
end

function setToTComplete()
	-- this fixes a bug that messes up game progression
	if BTRAMOBJ:checkFlag(0x83, 1, "setTotComplete") == false and TOT_SET_COMPLETE == false then -- CK Klungo Boss Room
		BTRAMOBJ:setFlag(0x83, 1);
        TOT_SET_COMPLETE = true;
	end
end

function saveGame()
    BMMBackup();
    GAME_LOADED = false;
    SAVE_GAME = false;
end


function main()
    if not checkBizHawkVersion() then
        return
    end
    print("Banjo-Tooie Archipelago Version " .. BT_VERSION)
    server, error = socket.bind('localhost', 21221)
    BTRAMOBJ = BTRAM:new(nil);
    BTMODELOBJ = BTModel:new(BTRAMOBJ, "Player", false);
    BTCONSUMEOBJ = BTConsumable:new(BTRAMOBJ, "HONEYCOMB");

    while true do
        FRAME = FRAME + 1
        if not (CUR_STATE == PREV_STATE) then
            PREV_STATE = CUR_STATE
        end
        if (CUR_STATE == STATE_OK) or (CUR_STATE == STATE_INITIAL_CONNECTION_MADE) or (CUR_STATE == STATE_TENTATIVELY_CONNECTED) then
            if (FRAME % 60 == 1) then
                BTRAM:banjoPTR()
                receive();
                if SKIP_TOT == "true" and CURRENT_MAP == 0x15E then
					setToTComplete();
				end
                if SAVE_GAME == true
                then
                    saveGame();
                end
                BKCheckAssetLogic()
                gameSaving();
                if TEXT_START == true then
                    clearText()
                elseif TEXT_START == false then
                    processMessages()
                end
                if OPEN_HAG1 == true and BTRAMOBJ:checkFlag(0x6E, 2, "WORLD_9_OPEN") == true and BTRAMOBJ:checkFlag(0x6E, 3, "HAG_1_OPEN") == false then
                    BTRAMOBJ:setFlag(0x6E, 3);
                    table.insert(AP_MESSAGES, "HAG 1 is now unlocked!")
                    print("HAG 1 is now unlocked!")
                end
            elseif (FRAME % 10 == 1)
            then
                checkPause();
                checkTotalMenu();
                if not (INIT_COMPLETE) or CURRENT_MAP == 0x158 then
					initializeFlags();
				end
                BKAssetFound();
                DPadStats();
            end
        elseif (CUR_STATE == STATE_UNINITIALIZED) then
            if  (FRAME % 60 == 1) then
                server:settimeout(2)
                local client, timeout = server:accept()
                if timeout == nil then
                    print('Initial Connection Made')
                    CUR_STATE = STATE_INITIAL_CONNECTION_MADE
                    BT_SOCK = client
                    BT_SOCK:settimeout(0)
                else
                    print('Connection failed, ensure Banjo Tooie Client is running, connected and rerun banjotooie_connector.lua')
                    return
                end
            end
        end
        emu.frameadvance()
    end
end

main()


--Unused Functions (Function Graveyard)


-- function getBanjoDeathAnimation(check)
--     local banjo = banjoPTR()
--     if banjo == nil
--     then
--         return false;
--     end

--     local ptr = dereferencePointer(banjo + ANIMATION_PTR);
--     local animation = mainmemory.read_u16_be(ptr + 0x34);

--     if check == true
--     then
--         return animation
--     end

--     if animation == 216 and CHECK_DEATH == false
--     then
--         DETECT_DEATH = true;
--         CHECK_DEATH = true;
--         KILL_BANJO = false;
--         if DEBUG == true
--         then
--             print("Banjo is Dead");
--         end
--     elseif CHECK_DEATH == true and animation ~= 216
--     then
--         CHECK_DEATH = false;
--         if DEBUG == true
--         then
--             print("Deathlink Reset");
--         end
--     end
-- end

-- function setCurrentHealth(value)
-- 	local currentTransformation = mainmemory.readbyte(0x11B065);
-- 	if type(0x11B644) == 'number' then
-- 		value = value or 0;
-- 		value = math.max(0x00, value);
-- 		value = math.min(0xFF, value);
-- 		return mainmemory.write_u8(0x11B644, value);
-- 	end
-- end

-- function killBT()
--     if KILL_BANJO == true then
--         setCurrentHealth(0)
--         moveEnemytoBK()
--     end
-- end

-- function moveEnemytoBK()
--     local enemy = checkModel("enemy");
--     if enemy == false
--     then
--         return
--     end

--     pos = getBanjoPos();
--     if pos == false
--     then
--         return
--     end

-- 	mainmemory.writefloat(enemy + 0x04, pos["Xpos"], true);
--     mainmemory.writefloat(enemy + 0x08, pos["Ypos"], true);
--     mainmemory.writefloat(enemy + 0x0C, pos["Zpos"], true);

--     KILL_BANJO = false --TODO - TEST
--     -- print("Object Distance:")
--     -- print(playerDist)
-- end