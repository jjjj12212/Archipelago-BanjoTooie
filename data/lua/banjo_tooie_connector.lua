-- Banjo Tooie Connector Lua
-- Created by Mike Jackson (jjjj12212) 
-- with the help of Rose (Oktorose), the OOT Archipelago team, ScriptHawk BT.lua & kaptainkohl for BTrando.lua 
-- modifications from Unalive, HemiJackson & fhnnhf 

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
local BT_VERSION = "V2.1.3"
local PLAYER = ""
local SEED = 0

local BT_SOCK = nil

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"
local PREV_STATE = ""
local CUR_STATE =  STATE_UNINITIALIZED
local FRAME = 0
local VERROR = false
local CLIENT_VERSION = 0


local DEBUG = false
local DEBUGLVL2 = false
local DEBUGLVL3 = false

local BTMODELOBJ = nil;
local BTRAMOBJ = nil;
local BTCONSUMEOBJ = nil;

local DEMO_MODE = true;
local SKIP_TOT = ""
local MINIGAMES = ""
local INIT_COMPLETE = false
local PAUSED = false;
local TOTALS_MENU = false;
local OBJ_TOTALS_MENU = false;
local SAVE_GAME = false;
local USE_BMM_TBL = false;
local USE_BMM_ONLY_TBL = false;
local USE_BMM_ONLY_TYP = "";


local CLOSE_TO_ALTAR = false;

local SNEAK = false;
local AIMASSIST = false;
local SUPERBANJO = false;
local REGEN = false;
local TEXT_TIMER = 2;
local TEXT_START = false;
local FPS = false

local ENABLE_AP_HONEYCOMB = false;
local ENABLE_AP_PAGES = false;
local ENABLE_AP_MOVES = false; -- Enable AP Moves Logics
local ENABLE_AP_BK_MOVES = 0; -- 0: disable 1: Talon Trot + Full Jump 2: ALL REMOVED
local ENABLE_AP_CHEATO_REWARDS = false;
local ENABLE_AP_HONEYB_REWARDS = false;
local ENABLE_AP_DOUBLOONS = false;
local ENABLE_AP_CHUFFY = false;
local ENABLE_AP_JINJO = false;
local ENABLE_AP_NOTES = false;
local ENABLE_AP_WORLDS = false;
local ENABLE_AP_MYSTERY = false;
local DISABLE_TEXT_OVERLAY = false;
local AP_MESSAGES = {};

local GAME_LOADED = false;

-------------- MAP VARS -------------
local MAP_TRANSITION = false;
local PREVIOUS_MAP = nil;
local CURRENT_MAP = nil;
local NEXT_MAP = nil;


-------------- JIGGY VARS -----------
local JIGGY_COUNT = 0; -- Used for UI
local BMM_BACKUP_JIGGY = false;
local AGI_JIGGY_SET = false;

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

-------------- SKIP VARS ------------
local OPEN_HAG1 = false;
local SKIP_PUZZLES = false;
local SKIP_KLUNGO = false;
local SKIP_KING = false;

-------------- MYSTERY VARS -----------
local EGGS_CLEARED = true;
local KEY_DROPPED = false;
local KEY_GRABBED = false;
local WAIT_FOR_HATCH = false;

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


-------------- GOAL TYPE VARS ------------
local GOAL_TYPE = nil;
local MGH_LENGTH = nil;
local BH_LENGTH = nil;
local JFR_LENGTH = nil;
local TH_LENGTH = nil;

-------------- TRAP VARS ------------

-- local TOTAL_WARP_COUNTER = 0
-- local WARP_TRAP_LOGIC = 0
-- local WARP_TABLE = {
--     [1]  = {mapId = 0xAF, worldName = "Spiral Mountain", xPos = 10000, yPos = 10320, zPos = 10231}, -- notes: CCL cavern, by the treble clef
-- }

--------------- ROYSTEN VARS --------------------
local FAST_SWIM = false
local DOUBLE_AIR = false

--------------- DEATH LINK ----------------------
local KILL_BANJO = false
local DEATH_LINK = false
local DETECT_DEATH = false;
local CHECK_DEATH = false;

---------------- AMAZE-O-GAZE VARS ---------------
local GOGGLES = false;


-------------- ENCOURAGEMENT MESSAGES ------------
local ENCOURAGEMENT = {
         [1]  = {message = " GUH-HUH!"},
         [2]  = {message = " BREEE!"},
         [3]  = {message = " EEKUM BOKUM!"},
         [4]  = {message = " YEEHAW!"},
         [5]  = {message = " JINJOO!!"},
         [6]  = {message = " WAHEY!!!"},
}


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
        [18] = {key=0x0040, name="Eggs", max=2}, -- Stop'n'Swop
        [59] = {key=0x8FBF, name="Ice Keys", max=1}, -- Stop'n'Swop  -- read key is 59
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
    if self.consumeIndex == 59
    then
        mainmemory.write_u16_be(addr + 19 * 2, value ~ self.consumeKey);
    else
        mainmemory.write_u16_be(addr + self.consumeIndex * 2, value ~ self.consumeKey);
    end
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

function BTConsumable:getEggConsumable()
    local addr = self.banjoRAM:dereferencePointer(self.CONSUME_PTR);
    local amount = mainmemory.read_u16_be(addr + 18 * 2)
    newamt = amount ~ 0x0040
	return newamt;
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
    next_map = 0x127640;
    entrance_id = 0x127643;
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

function BTRAM:setBanjoPos(Xnew, Ynew, Znew, Yvel)
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
	if Ynew ~= nil and Yvel ~= nil
    then
        mainmemory.writefloat(plptr + 0x04, Ynew, true);
        mainmemory.writefloat(plptr + 0x04 + 12, Ynew, true);
        mainmemory.writefloat(plptr + 0x04 + 24, Ynew, true);
        mainmemory.writefloat(plptr + 0xC8 + 0x14, Yvel, true);
    end
    if Xnew ~= nil
    then
        mainmemory.writefloat(plptr + 0x00, Xnew, true);
        mainmemory.writefloat(plptr + 0x00 + 12, Xnew, true);
        mainmemory.writefloat(plptr + 0x00 + 24, Xnew, true);
    end
    if Znew ~= nil
    then
        mainmemory.writefloat(plptr + 0x08, Znew, true);
        mainmemory.writefloat(plptr + 0x08 + 12, Znew, true);
        mainmemory.writefloat(plptr + 0x08 + 24, Znew, true);
    end
end

function BTRAM:getBanjoTState()
    return mainmemory.readbyte(self.character_state);
end

function BTRAM:getBanjoMovementState()
    local player = BTRAM:banjoPTR()
    if player ~= nil
    then
        local movestate = BTRAM:dereferencePointer(player + self.movement_ptr)
        if movestate == nil
        then
            return nil
        end
        return mainmemory.read_u32_be(movestate + self.current_state)
    end
    return nil
end

function BTRAM:getMap(nextmap)
    if nextmap == false
    then
        local map = mainmemory.read_u16_be(self.map_addr);
        return map;
    else
        local map = mainmemory.read_u16_be(self.next_map);
        return map;
    end
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
        ["Jiggy Guy"] = 0x937,
        ["Ice Key"] = 0x63B,
        ["Cartridge"] = 0x910,
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
    BTMODELOBJ:changeName("Altar", false);
    if SKIP_PUZZLES == false
    then
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
    else -- Move Altar off the map 
        local modelPOS = BTMODELOBJ:getMultipleModelCoords()
        if modelPOS == false
        then
            return
        end
        for modelObjPtr, POS in pairs(modelPOS) do
            if POS ~= false
            then
                BTMODELOBJ:moveModelObject(modelObjPtr, nil, -5000, nil)
            end
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
    },
    ["STOPNSWAP"] = {
        [0xAF] = "1230956",
        [0xAE] = "1230957",
    },
    ["ICEKEY"] = {
        [0x142] = "1230958"
    },
    ["AGI_ASSETS"] = {
        ["ALL"] = {
            ["JIGGIES"] = { --Jinjo Jiggies
                "1230676", --Jinjo
                "1230677", --Jinjo
                "1230678", --Jinjo
                "1230679", --Jinjo
                "1230680", --Jinjo
                "1230681", --Jinjo
                "1230682", --Jinjo
                "1230683", --Jinjo
                "1230684", --Jinjo
                "1230685", --Jingaling
--                "1230629", -- Pig Pool
--                "1230637" -- Dippy
            }
        },
        --SPIRAL MOUNTAIN
        ["0xAF"]  = { --SM - Spiral Mountain
            ["STOPNSWAP"] = {
                "1230956"
            },
            ["JINJOS"] = {
                "1230595" -- SM Jinjo
            }
        },
        [0xAE]  =	{ --SM - Behind the waterfall
            ["STOPNSWAP"] = {
                "1230957"
            }
        },
        [0xAD]  =	{ --SM - Grunty's Lair
            -- Cheato Rewards should be here
        },
        --JINJO VILLAGE
        [0x143] =	{ --JV - Bottles' House
            --Amaze-O-Gaze should be here
        },
        --ISLE O' HAGS
        [0x155] =	{ --IoH - Cliff Top
            ["JINJOS"] = {
                "1230593" -- Clifftop Jinjo
            }
        },
        -- ["0x150"] =	{"Isle O' Hags", "Wooded Hollow"},      --IoH - Heggy's Egg Shed
        -- ["0x15b"] =	{"Isle O' Hags", "Pine Grove"},         --IoH - Inside another digger tunnel
        -- ["0x151"] =	{"Isle O' Hags", "Wooded Hollow"},      --IoH - Jiggywiggy's Temple
        -- ["0x154"] =	{"Isle O' Hags", "Pine Grove"},         --IoH - Pine Grove
        -- ["0x157"] =	{"Isle O' Hags", "Pine Grove"},         --IoH - Pine Grove - Wumba's Wigwam
        [0x152] = { --IoH - Plateau
            ["JINJOS"] = {
                "1230594" -- Plateau Jinjo
            }
        },
        -- ["0x153"] =	{"Isle O' Hags", "Plateau"},            --IoH - Plateau - Honey B's Hive
        -- ["0x15c"] =	{"Isle O' Hags", "Quagmire"},           --IoH - Quagmire
        [0x15A] = { --IoH - Wasteland
            ["JINJOS"] = {
                "1230592" -- Wasteland Jinjo
            }
        },
        [0x14F] = { --IoH - Wooded Hollow
            ["JINJOS"] = {
                "1230591" -- Wooded Hollow Jinjo
            }
        },
        --MAYAHEM TEMPLE
        [0xB8] = { --MT
            ["JIGGIES"] = {
                "1230599",
                "1230604"
            },
            ["JINJOS"] = {
                "1230552", -- Stadium
                "1230554", -- Pool
                "1230555", -- Bridge
            }
        },
        [0xC4] = { --MT - Jade Snake Grove
            ["JIGGIES"] = {
                "1230601", -- Golden Goliath
                "1230605"  -- Ssslumber
            },
            ["JINJOS"] = {
                "1230551" -- Snake Grove
            }
        },
        [0xBB] = { --MT - Mayan Kickball Stadium (Lobby)
            ["JIGGIES"] = {
                "1230598", -- Kickball
            }
        },
        [0xB7] = { --MT - Mumbo's Skull
            --glowbo
        },
        [0xB9] = { --MT - Prison Compound
            ["JIGGIES"] = {
                "1230602", --quicksand
                "1230603", --pillars
            }
        },
        [0x17A] =	{ --MT - Targitzan's Really Sacred Chamber
            ["JIGGIES"] = {
                "1230596" --Targitzan
            }
        },
        [0x177] =	{ --MT - Targitzan's Slightly Sacred Chamber
            ["JIGGIES"] = {
                "1230597" --Slightly Sacred Chamber
            }
        },
        [0xC5] = { --MT - Treasure Chamber
            ["JIGGIES"] = {
                "1230600" --Treasure Chamber
            }
        },
        [0x178] = { --MT - Inside Tatgitzan's Temple
            ["JINJOS"] = {
                "1230553" -- Temple Jiggy
            }
        },
        --GLITTER GULCH MINE
        [0xC7] ={ --GGM
            ["JIGGIES"] = {
                "1230607", -- Canary Mary
                "1230612", -- Crushing Shed
                "1230613" -- Waterfall
            },
            ["JINJOS"] = {
                "1230559", -- Boulder
                "1230560", -- Tracks
            }
        },
        [0xCC] ={ --GGM - Flooded Caves
            ["JIGGIES"] = {
                "1230615" -- Flooded Cave
            }
        },
        [0xCA] ={ --GGM - Fuel Depot
            --Notes
        },
        [0xD3] = { --GGM - Generator Cavern
            ["JIGGIES"] = {
                "1230608" -- Generator Cavern
            }
        },
        [0xD2] = { --GGM - Gloomy Caverns
            ["JINJOS"] = {
                "1230557" -- Jail
            }
        },
        [0xD1] = { --GGM - Inside Chuffy's Boiler
            ["JIGGIES"] = {
                "1230606" -- King Coal
            },
        },
        [0x163] =	{ --GGM - Ordnance Storage Entrance
            ["JIGGIES"] = {
                "1230610" -- Ordnance Storage
            },
        },
        [0xCF] = { --GGM - Power Hut Basement
            ["JIGGIES"] = {
                "1230614" -- Power Hut Basement
            },
        },
        [0xD8] = { --GGM - Prospector's Hut
            ["JIGGIES"] = {
                "1230611" -- Dilberta
            },
        },
        [0xDA] = { --GGM - Toxic Gas Cave
            ["JINJOS"] = {
                "1230558" -- Toxic
            }
        },
        [0xD7] = { --GGM - Train Station

        },
        [0xCD] = { --GGM - Water Storage
            ["JINJOS"] = {
                "1230556" -- Water Storage
            }
        },
        [0xCE] = { --GGM - Waterfall Cavern
            ["JIGGIES"] = {
                "1230609" -- Waterfall Cavern
            },
        },
        --WITCHYWORLD
        [0xD6] = { --WW
            ["JIGGIES"] = {
                "1230619", -- Saucer of Peril
                "1230621", -- Dive of Death
                "1230622", -- Mrs Boggy
                "1230625", -- Cactus of Strength
            },
            ["JINJOS"] = {
                "1230561", -- Top of Tent
                "1230563", -- Van door
                "1230564", -- dogdem dome
                "1230565", -- Cactus of Strength
            }
        },
        [0xEA] = { --WW - Cave of Horrors
            ["JINJOS"] = {
                "1230562", -- Cave of Horrors
            }
        },
        [0xE1] = { --WW - Crazy Castle Stockade
            ["JIGGIES"] = {
                "1230616", -- Hoop Hurry
                "1230620", -- Balloon Burst
            },
        },
        [0xDD] = { --WW - Dodgem Dome Lobby
            ["JIGGIES"] = {
                "1230617", -- Dodgem
            },
        },
        [0xEB] = { --WW - Haunted Cavern

        },
        [0xF9] = { --WW - Mr. Patch
            ["JIGGIES"] = {
                "1230618", -- Patches
            },
        },
        [0xE6] = { --WW - Star Spinner
            ["JIGGIES"] = {
                "1230623", -- Star Spinner
            },
        },
        [0xE7] = { --WW - The Inferno
            ["JIGGIES"] = {
                "1230624", -- The Inferno
            },
        },
        [0xD5] = { --WW - Wumba's Wigwam

        },

        --JOLLY ROGER'S LAGOON
        [0x1A7] = { --JRL
            ["JIGGIES"] = {
                "1230627", -- Tiptup
                "1230635", -- UFO
                "1230629", -- Pig Pool
            },
            ["JINJOS"] = {
                "1230566", -- alcove
            }
        },
        [0xF4] = { --JRL - Ancient Swimming Baths

        },
        [0x1A8] =	{ --JRL - Atlantis
            ["JIGGIES"] = {
                "1230633", -- SEEMEE
            },
            ["JINJOS"] = {
                "1230570", -- Sunken Ship
            }
        },
        [0xFF] = { --JRL - Blubber's Wave Race Hire
            ["JINJOS"] = {
                "1230567", -- Blubber
            }
        },
        [0xF6] = {  --JRL - Electric Eel's lair

        },
        [0xF8] = { --JRL - Inside the Big Fish
            ["JINJOS"] = {
                "1230568", -- Big Fish
            }
        },
        [0xED] =	{ --JRL - Jolly's
            ["JIGGIES"] = {
                "1230631", -- Merry Maggie
            },
        },
        [0xFC] =	{ --JRL - Lord Woo Fak Fak
            ["JIGGIES"] = {
                "1230632", -- Lord Woo
            },
        },      
        [0xEE] =	{ --JRL - Pawno's Emporium
            ["JIGGIES"] = {
                "1230634", -- Pawno
            },
        },
        [0x1A9] =	{ --JRL - Sea Bottom
            ["JIGGIES"] = {
                "1230633", -- SEEMEE
            },
        },       
        [0x181] =	{ --JRL - Sea Botom Cavern
            ["JIGGIES"] = {
                "1230626", -- Mini-Sub Challenge
            },
        },
        [0xF7] = { --JRL - Seaweed Sanctum
            ["JINJOS"] = {
                "1230569", -- Seaweed
            }
        },
        [0x1A6] =	{ --JRL - Smuggler's cavern
            ["JIGGIES"] = {
                "1230633", -- SEEMEE
                "1230630", -- Smuggler
            },
        },     
        [0xFA] = { --JRL - Temple of the Fishes
            ["JIGGIES"] = {
                "1230628", -- Chris P. Bacon
            },
        },

        --TERRYDACTYLAND
        [0x112] =	{ --TDL
            ["JIGGIES"] = {
                "1230637", -- Dippy
                "1230644", -- Rocknut
                "1230645", -- Dino Code
            },
            ["JINJOS"] = {
                "1230571", -- Talon Torp
                "1230572", -- Entrance
                "1230573", -- Maze Cave
                "1230574", -- T-rex
            }
        },
        [0x123] = { --TDL - Inside Chompa's Belly
            ["JIGGIES"] = {
                "1230641", -- Chompa
            },
        },
        [0x116] = { --TDL - Inside the Mountain
            ["JIGGIES"] = {
                "1230636", -- Under Terry Nest
            },
        },
        [0x115] = { --TDL - Oogle Boogles' Cave
            ["JIGGIES"] = {
                "1230640", -- Oogle Boogle Tribe
            },
        },
        [0x117] =	{ --TDL - River Passage

        },
        [0x11A] =	{ --TDL - Stomping Plains
            ["JIGGIES"] = {
                "1230643", -- Stomping
            },
            ["JINJOS"] = {
                "1230575", -- Stomping
            }
        },
        [0x118] =	{ --TDL - Styracosaurus Family Cave
            ["JIGGIES"] = {
                "1230638", -- Scrotty
            },
        },
        [0x113] =	{ --TDL - Terry's Nest
            ["JIGGIES"] = {
                "1230639", -- Terry
                "1230642", -- Terry's Kids
            },
        },
        [0x114] =	{ --TDL - Train Station
            ["JIGGIES"] = {
                "1230644", -- Rocknut
            },
        },
        --GRUNTY'S INDUSTRIES
        [0x100] =	{ --GI
            ["JIGGIES"] = {
                "1230646", -- Skivvy
            },
            ["JINJOS"] = {
                "1230580" -- Outside
            }
        },
        [0x10F] = { --GI - Basement
            ["JIGGIES"] = {
                "1230647", -- Weldar
            },
        },
        [0x110] =	{ --GI - Basement (Repair Depot)
            -- cheato
        },
        [0x111] =	{ --GI - Basement (Waste Disposal)
            ["JIGGIES"] = {
                "1230646", -- Underwater Waste Disposal
                "1230655", -- Plant Box
                "1230661", -- HFP Oil Drill
            },
            ["JINJOS"] = {
                "1230578" -- Waste Disposal
            }
        },
        [0x101] =	{ --GI - Floor 1
            ["JIGGIES"] = {
                "1230646", -- Skivvy
                "1230652", -- Floor 1 Guarded
            },
        },
        [0x106] =	{ --GI - Floor 2
            ["JIGGIES"] = {
                "1230646", -- Skivvy
            },
            ["JINJOS"] = {
                "1230577" -- leg spring
            }
        },
        [0x108] =	{ --GI - Floor 3
            ["JIGGIES"] = {
                "1230646", -- Skivvy
            },
        },
        [0x109] =	{ --GI - Floor 3 (Boiler Plant)
            ["JINJOS"] = {
                "1230579" -- Top of Boiler
            }
        },
        [0x10A] =	{ --GI - Floor 3 (Packing Room)
            ["JIGGIES"] = {
                "1230654", -- Twinkly Packing
            },
        },
        [0x10B] =	{ --GI - Floor 4

        },
        [0x10D] =	{ --GI - Floor 4 (Quality Control)
            ["JIGGIES"] = {
                "1230651", -- Quality Control
            },
        },
        [0x10E] =	{ --GI - Floor 5
            ["JIGGIES"] = {
                "1230646", -- Skivvy
                "1230650", -- Floor 5
            },
            ["JINJOS"] = {
                "1230576" -- 5 floor
            }
        },
        [0x187] =	{ --GI - Sewer Entrance
            ["JIGGIES"] = {
                "1230648", -- Clinker
            },
        },
        [0x102] =	{ --GI - Train Station

        },
        [0x104] =	{ --GI - Trash Compactor
            ["JIGGIES"] = {
                "1230653", -- Trash Compactor
            },
        },
        [0x103] =	{ --GI - Workers' Quarters
            ["JIGGIES"] = {
                "1230646", -- Skivvy
            },
        },

        --HAILFIRE PEAKS
        [0x131] =	{ --HFP - Boggy's Igloo
            ["JIGGIES"] = {
                "1230659", -- Boggy
            },
        },
        [0x12B] =	{ --HFP - Chilli Billi
            ["JIGGIES"] = {
                "1230656", -- Brothers
            },
        },
        [0x12C] =	{ --HFP - Chilly Willy
            ["JIGGIES"] = {
                "1230656", -- Brothers
            },
        },
        [0x132] =	{ --HFP - Icicle Grotto
            ["JINJOS"] = {
                "1230584", -- Grotto
            }
        },
        [0x128] =	{ --HFP - Icy Side
            ["JIGGIES"] = {
                "1230660", -- Icy Train Station
                "1230662", -- Stomping
                "1230664", -- Aliens
            },
            ["JINJOS"] = {
                "1230585", -- Mildred
                "1230583" -- Windy Hole
            }
        },
        [0x133] =	{ --HFP - Inside the Volcano
            ["JIGGIES"] = {
                "1230657", -- Volcano
            },
        },
        [0x12D] =	{ --HFP - Kickball Stadium lobby
            ["JIGGIES"] = {
                "1230663", -- Kickball
            },
        },
        [0x127] =	{ --HFP - Lava Side
            ["JIGGIES"] = {
                "1230658", -- Sabreman
                "1230665", -- Lava waterfall
            },
            ["JINJOS"] = {
                "1230581", -- Lava waterfall
                "1230582" -- Boiling Pool
            }
        },
        [0x129] =	{ --HFP - Lava Train Station
            --honeycomb
        },

        --CLOUD CUCKOOLAND
        [0x136] =	{ --CCL
            ["JIGGIES"] = {
                "1230667", -- Mr Fit
                "1230669", -- Canary Mary 3
                "1230671", -- Jiggium Plant
                "1230675", -- Jelly Castle
            },
        },
        [0x13A] =	{ --CCL - Central Cavern
            ["JIGGIES"] = {
                "1230674", -- Superstash
            },
            ["JINJOS"] = {
                "1230588" -- Central
            }
        },
        [0x138] =	{ --CCL - Inside the Cheese Wedge
            ["JIGGIES"] = {
                "1230672", -- Cheese Wedge
            },
            ["JINJOS"] = {
                "1230587" -- Cheese
            }
        },
        [0x13D] =	{ --CCL - Inside the Pot o' Gold
            ["JIGGIES"] = {
                "1230668", -- pot o gold
            },
        },
        [0x137] =	{ --CCL - Inside the Trash Can
            ["JIGGIES"] = {
                "1230673", -- Trash Can
            },
            ["JINJOS"] = {
                "1230586" -- Trash
            }
        },
        [0x13F] =	{ --CCL - Mingy Jongo's Skull
            ["JIGGIES"] = {
                "1230666", -- Mingy Jongo
            },
            ["JINJOS"] = {
                "1230589" -- Mumbo
            }
        },
        [0x13E] =	{ --CCL - Mumbo's Skull
            ["JIGGIES"] = {
                "1230666", -- Mingy Jongo
            },
            ["JINJOS"] = {
                "1230589" -- Mumbo
            }
        },
        [0x140] =	{ --CCL - Wumba's Wigwam
            ["JINJOS"] = {
                "1230590" -- Balasters
            }
        },
        [0x139] =	{ --CCL - Zubbas' Nest
            ["JIGGIES"] = {
                "1230670", -- Zubba
            },
        },

        --CAULDRON KEEP
        [0x19A] =	{ --CK - HAG 1

        },
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
        ["2"] = "1230586",
        ["3"] = "1230588",
        ["4"] = "1230590",
        ["5"] = "1230592",
        ["6"] = "1230593",
        ["7"] = "1230579",
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
        ["8"] = "1230578",
    },
}

-- BMM - Backup Memory Map 
local BMM =  {};

-- AMM - Actual Memory Map
local AMM = {};

-- AGI - Archipelago given items
local AGI = {};
local AGI_JIGGIES = {};
local AGI_JINJO_LOCATIONS = {}
local AGI_MOVES = {};
local AGI_NOTES = {};
local AGI_STATIONS = {};
local AGI_CHUFFY = {};
local AGI_MYSTERY = {};
local AGI_JINJOS = {
    ["1230501"] = 0, -- white
    ["1230502"] = 0, -- orange
    ["1230503"] = 0, -- yellow
    ["1230504"] = 0, -- brown
    ["1230505"] = 0, -- green
    ["1230506"] = 0, -- red
    ["1230507"] = 0, -- blue
    ["1230508"] = 0, -- purple
    ["1230509"] = 0, -- black
};

-- local AGI_TRAPS = {
--     ["1230799"] = 0,
-- };

local BMM_JIGGIES = {}; -- BMM JIGGIES
local BMM_JINJOS = {}; -- BMM JINJOS
local BKM = {}; -- Banjo Tooie Movelist Table
local BKNOTES = {}; -- Notes
local BKSTATIONS = {} -- Stations
local BKCHUFFY = {} -- King Coal Progress Flag
local BKJINJOFAM = {} -- Jinjo Family check 
local UNLOCKED_WORLDS = {} -- Worlds unlocked
local BKMYSTERY = {} -- Stop n Swap 
local ROYSTEN = {} -- Roysten flags. Because the flags are separate from moves, we don't need to save this.
local CHEATO_REWARDS = {} -- Cheato Check Locations
local HONEYB_REWARDS = {} -- Honey B Check Locations
local JIGGY_CHUNKS = {} -- Jiggy Chunky Check Locations
local DINO_KIDS = {} -- the 3 Dino Kids


-- Mapping required for AGI Table
local AGI_MASTER_MAP = {
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
			-- ['Three-Armed Pig'] = {
			-- 	['addr'] = 0x34,
			-- 	['bit'] = 6
			-- },
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
    },
    ['STOPNSWAP'] = {
        ["1230953"] = {
            ['addr'] = 0x77,
            ['bit'] = 7,
            ['name'] = "Yellow Egg Hatched"
        },
        ["1230954"] = {
            ['addr'] = 0x77,
            ['bit'] = 6,
            ['name'] = "Pink Egg Hatched"
        },
        ["1230955"] = {
            ['addr'] = 0x77,
            ['bit'] = 4,
            ['name'] = "Blue Egg Hatched"
        },
        ["1230956"] = {
            ['addr'] = 0x77,
            ['bit'] = 5,
            ['name'] = "Pink Egg"
        },
        ["1230957"] = {
            ['addr'] = 0x77,
            ['bit'] = 3,
            ['name'] = "Blue Egg"
        },
    },
    ['ROYSTEN'] = {
        ["1230777"] = {
            ['addr'] = 0x36,
            ['bit'] = 2,
            ['name'] = "SM: Roysten Reward 1"
        },
        ["1230778"] = {
            ['addr'] = 0x9E,
            ['bit'] = 6,
            ['name'] = "SM: Roysten Reward 2"
        }
    },
    ["CHEATO"] = {
        ["1230992"] = {
            ['addr'] = 0x08,
            ['bit'] = 4,
            ['name'] = "SM: Cheato Reward 1"
        },
        ["1230993"] = {
            ['addr'] = 0x08,
            ['bit'] = 5,
            ['name'] = "SM: Cheato Reward 2"
        },
        ["1230994"] = {
            ['addr'] = 0x08,
            ['bit'] = 6,
            ['name'] = "SM: Cheato Reward 3"
        },
        ["1230995"] = {
            ['addr'] = 0x08,
            ['bit'] = 7,
            ['name'] = "SM: Cheato Reward 4"
        },
        ["1230996"] = {
            ['addr'] = 0x09,
            ['bit'] = 0,
            ['name'] = "SM: Cheato Reward 5"
        },
    },
    ["BKMOVES"] = {
        ["1230810"] = {
            ['addr'] = 0x1A,
            ['bit'] = 4,
            ['name'] = "Dive"
        },
        ["1230811"] = {
            ['addr'] = 0x19,
            ['bit'] = 6,
            ['name'] = "Flight Pad"
        },
        ["1230812"] = {
            ['addr'] = 0x19,
            ['bit'] = 5,
            ['name'] = "Flap Flip"
        },
        ["1230813"] = {
            ['addr'] = 0x19,
            ['bit'] = 3,
            ['name'] = "Third Person Egg Shooting"
        },
        ["1230814"] = {
            ['addr'] = 0x1A,
            ['bit'] = 1,
            ['name'] = "Roll"
        },
        ["1230815"] = {
            ['addr'] = 0x1A,
            ['bit'] = 5,
            ['name'] = "Talon Trot"
        },
        ["1230816"] = {
            ['addr'] = 0x19,
            ['bit'] = 7,
            ['name'] = "Tall Jump"
        },
        ["1230817"] = {
            ['addr'] = 0x19,
            ['bit'] = 2,
            ['name'] = "Climb"
        },
        ["1230818"] = {
            ['addr'] = 0x19,
            ['bit'] = 4,
            ['name'] = "Flutter"
        },
        ["1230819"] = {
            ['addr'] = 0x1A,
            ['bit'] = 7,
            ['name'] = "Wonderwing"
        },
        ["1230820"] = {
            ['addr'] = 0x18,
            ['bit'] = 7,
            ['name'] = "Beak Buster"
        },
        ["1230821"] = {
            ['addr'] = 0x1A,
            ['bit'] = 6,
            ['name'] = "Turbo Trainers"
        },
        ["1230822"] = {
            ['addr'] = 0x1A,
            ['bit'] = 0,
            ['name'] = "Air Rat-a-tat Rap"
        },
        ["1230824"] = {
            ['addr'] = 0x19,
            ['bit'] = 1,
            ['name'] = "Ground Rat-a-tat Rap"
        },
        ["1230825"] = {
            ['addr'] = 0x18,
            ['bit'] = 5,
            ['name'] = "Beak Barge"
        },
        ["1230826"] = {
            ['addr'] = 0x1A,
            ['bit'] = 3,
            ['name'] = "Stilt Stride"
        },
        ["1230827"] = {
            ['addr'] = 0x18,
            ['bit'] = 6,
            ['name'] = "Beak Bomb"
        },

    },
    ["HONEYB"] = {
        ["1230997"] = {
            ['addr'] = 0x98,
            ['bit'] = 2,
            ['name'] = "IoH: Honey B's Reward 1"
        },
        ["1230998"] = {
            ['addr'] = 0x98,
            ['bit'] = 3,
            ['name'] = "IoH: Honey B's Reward 2"
        },
        ["1230999"] = {
            ['addr'] = 0x98,
            ['name'] = "IoH: Honey B's Reward 3"
        },
        ["1231000"] = {
            ['addr'] = 0x98,
            ['bit'] = 4,
            ['name'] = "IoH: Honey B's Reward 4"
        },
        ["1231001"] = {
            ['addr'] = 0x98,
            ['name'] = "IoH: Honey B's Reward 5"
        },
    },
    ["JCHUNKS"] = {
        ["1231002"] = {
            ['addr'] = 0x7D,
            ['bit'] = 0,
            ['name'] = "GGM: Crushing Shed Jiggy Chunk 1"
        },
        ["1231003"] = {
            ['addr'] = 0x7D,
            ['bit'] = 1,
            ['name'] = "GGM: Crushing Shed Jiggy Chunk 2"
        },
        ["1231004"] = {
            ['addr'] = 0x7D,
            ['bit'] = 2,
            ['name'] = "GGM: Crushing Shed Jiggy Chunk 3"
        }
    },
    ["JIGGIES"] = {
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
        }
    },
    ['JINJOS'] = {
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

function hag1_phase_skips()
    local tmp_flg_pointer = 0x12C774
    local beginning_phase_offset = 0x09
    local ending_phase_offset = 0x0A

    local pointer_addr = BTRAMOBJ:dereferencePointer(tmp_flg_pointer)
    mainmemory.writebyte(pointer_addr + beginning_phase_offset, 255); -- Skips part 1
    mainmemory.writebyte(pointer_addr + ending_phase_offset, 31); -- Skips Part 2
end

---------------------------------- JIGGIES ---------------------------------

function init_JIGGIES(type) -- Initialize JIGGIES
    local checks = {}
    for locationId,v in pairs(NON_AGI_MAP["JIGGIES"])
    do
        if type == "BMM"
        then
            BMM_JIGGIES[locationId] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_JIGGY_BMM")
        elseif type == "AGI"
        then
            checks[locationId] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_JIGGY_AGI")
        end
    end
    return checks
end

function restore_BMM_JIGGIES() --Only run while unpausing 
    if BMM_BACKUP_JIGGY == true and AGI_JIGGY_SET == true
    then
        for locationId,v in pairs(NON_AGI_MAP["JIGGIES"]) do
            if BMM_JIGGIES[locationId] == true
            then
                BTRAMOBJ:setFlag(v['addr'], v['bit']);
            else
                BTRAMOBJ:clearFlag(v['addr'], v['bit']);
            end
        end
        BMM_BACKUP_JIGGY = false
        AGI_JIGGY_SET = false
    end
end

function set_AP_JIGGIES() -- Only run while Pausing or Transistion to certain maps
    if BMM_BACKUP_JIGGY == true and AGI_JIGGY_SET == false
    then
        for locationId, value in pairs(AGI_JIGGIES)
        do
            local get_addr = NON_AGI_MAP["JIGGIES"][locationId]
            if value == true
            then
                BTRAMOBJ:setFlag(get_addr['addr'], get_addr['bit']);
            else
                BTRAMOBJ:clearFlag(get_addr['addr'], get_addr['bit']);
            end
        end
        AGI_JIGGY_SET = true
    end
end

function obtained_AP_JIGGY()
    if DEBUG == true
    then
        print("Jiggy Obtained")
    end
    for locationId, value in pairs(AGI_JIGGIES)
    do
        if value == false
        then
            AGI_JIGGIES[locationId] = true;
            if AGI_JIGGY_SET == true
            then
                local get_addr = NON_AGI_MAP["JIGGIES"][tostring(locationId)]
                BTRAMOBJ:setFlag(get_addr['addr'], get_addr['bit']);
            end
            break
        end
    end
    JIGGY_COUNT = JIGGY_COUNT + 1
end

function jiggy_ui_update()
    local jiggy_amt = 0
    local ram_jiggy_count = mainmemory.read_u16_be(0x11B0BC)
    if ram_jiggy_count ~= JIGGY_COUNT
    then
        for locationId, value in pairs(AGI_JIGGIES)
        do
            if value == false
            then
                jiggy_amt = jiggy_amt + 1
            end
        end
        mainmemory.write_u16_be(0x11B0BC, jiggy_amt)
        JIGGY_COUNT = jiggy_amt
    end
end

function backup_BMM_JIGGIES()
    if BMM_BACKUP_JIGGY == false
    then
        for locationId,v in pairs(NON_AGI_MAP["JIGGIES"]) do
            if BTRAMOBJ:checkFlag(v['addr'], v['bit']) == true
            then
                BMM_JIGGIES[locationId] = true
            else
                BMM_JIGGIES[locationId] = false
            end
        end
        BMM_BACKUP_JIGGY = true
        set_AP_JIGGIES()
    end
end

function jiggy_check()
    local checks = {}
    if BMM_BACKUP_JIGGY == true
    then
        jiggy_ui_update()
        if DEBUG == true
        then
            print("Setting BMM Jiggies")
        end
        return BMM_JIGGIES
    end
    if ASSET_MAP_CHECK["AGI_ASSETS"][CURRENT_MAP] ~= nil
    then
        if ASSET_MAP_CHECK["AGI_ASSETS"][CURRENT_MAP]["JIGGIES"] ~= nil
        then
            for _,locationId in pairs(ASSET_MAP_CHECK["AGI_ASSETS"][CURRENT_MAP]["JIGGIES"])
            do
                checks[locationId] = BTRAMOBJ:checkFlag(NON_AGI_MAP["JIGGIES"][locationId]['addr'], NON_AGI_MAP["JIGGIES"][locationId]['bit'])
                if DEBUG == true
                then
                    print(NON_AGI_MAP["JIGGIES"][locationId]['bit']..":"..tostring(checks[locationId]))
                end
            end
        end
    end
    for _,locationId in pairs(ASSET_MAP_CHECK["AGI_ASSETS"]["ALL"]["JIGGIES"])
    do
        checks[locationId] = BTRAMOBJ:checkFlag(NON_AGI_MAP["JIGGIES"][locationId]['addr'], NON_AGI_MAP["JIGGIES"][locationId]['bit'])
        -- if DEBUG == true
        -- then
        --     print(NON_AGI_MAP["JIGGIES"][locationId]['name'] .. ":" .. tostring(checks[locationId]))
        -- end
    end
    return checks
end

function no_puzzle_skip()
    if MAP_TRANSITION == true and NEXT_MAP == 0x14F and BMM_BACKUP_JIGGY == false --Wooded Hollow
    then
        backup_BMM_JIGGIES()
    elseif MAP_TRANSITION == true and NEXT_MAP == 0x151 and BMM_BACKUP_JIGGY == false -- Jiggywiggy Temple
    then
        backup_BMM_JIGGIES()
    elseif MAP_TRANSITION == true and BMM_BACKUP_JIGGY == true and NEXT_MAP ~= 0x14F and NEXT_MAP ~= 0x151  --Exiting Wooded Hollow
    then
        restore_BMM_JIGGIES()
    end
end

function hag1_open()
    if GAME_LOADED == true
    then
        if GOAL_TYPE == 0
        then
            if OPEN_HAG1 == true and BTRAMOBJ:checkFlag(0x6E, 3, "HAG_1_OPEN") == false then
                BTRAMOBJ:setFlag(0x6E, 3);
                table.insert(AP_MESSAGES, "HAG 1 is now unlocked!")
                print("HAG 1 is now unlocked!")
            end
        elseif GOAL_TYPE == 4
        then
            local token_count = 0;
            for id, itemId in pairs(receive_map)
            do
                if itemId == "1230798"
                then
                    token_count = token_count + 1
                end
            end
            if token_count >= 32
            then
                if OPEN_HAG1 == true and BTRAMOBJ:checkFlag(0x6E, 3, "HAG_1_OPEN") == false then
                    BTRAMOBJ:setFlag(0x6E, 3);
                    table.insert(AP_MESSAGES, "HAG 1 is now unlocked!")
                    print("HAG 1 is now unlocked!")
                end
            end
        end
    end
end

function check_open_level(show_message)  -- See if entrance conditions for a level have been met    
    if DEBUG == true then
        print(JIGGY_COUNT)
    end
    for _, values in pairs(WORLD_ENTRANCE_MAP)
    do
        if values["opened"] == false
        then
            if JIGGY_COUNT >= values["defaultCost"]
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
                    if ENABLE_AP_WORLDS == false
                    then
                        table.insert(AP_MESSAGES, values["defaultName"] .. " is now unlocked!")
                        print(values["defaultName"] .. " is now unlocked!")
                    end
                end
            end
        else --Make sure its open regardless but no message
            if JIGGY_COUNT >= values["defaultCost"] and values["opened"] == true
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

--------------- Randomize Worlds with BK Moves ---------------------------

function init_world_silos()
    for worlds, tbl in pairs(WORLD_ENTRANCE_MAP)
    do
        if tbl["locationId"] == "1230944"
        then
            if tbl["defaultName"] == "Glitter Gulch Mine"
            then
                BTRAMOBJ:setFlag(0x60, 7)
            end
            if tbl["defaultName"] == "Witchyworld"
            then
                BTRAMOBJ:setFlag(0x61, 0)
            end
            if tbl["defaultName"] == "Cloud Cuckooland" or tbl["defaultName"] == "Terrydactyland"
            then
                BTRAMOBJ:setFlag(0x61, 2)
            end
            if tbl["defaultName"] == "Jolly Roger's Lagoon" or tbl["defaultName"] == "Hailfire Peaks" or tbl["defaultName"] == "Grunty Industries"
            then
                BTRAMOBJ:setFlag(0x61, 1)
            end
        end
    end
    archipelago_msg_box("Warp Silo to your first world is now open")
end

--------------------------------- Roysten --------------------------------

function init_roysten()
    for k,v in pairs(NON_AGI_MAP['ROYSTEN'])
    do
        ROYSTEN[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "CHECK_ROYSTEN")
    end
end

function check_freed_roysten()
    if CURRENT_MAP == 0xAF
    then
        for k,v in pairs(NON_AGI_MAP['ROYSTEN'])
        do
            if ROYSTEN[k] == false
            then
                ROYSTEN[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "CHECK_ROYSTEN")
            end
        end
        if DOUBLE_AIR == true and ROYSTEN["1230778"] == true then
            ROYSTEN["1230777"] = true
        end
        if BTRAMOBJ:checkFlag(0x1E, 5, "CHECK_SWIM") == true and FAST_SWIM == false
        then
            if DEBUG == true
            then
                print("Removing Fast Swimming")
            end
            BTRAMOBJ:clearFlag(0x1E, 5)
        end
        if BTRAMOBJ:checkFlag(0x32, 7, "CHECK_DAIR") == true and DOUBLE_AIR == false
        then
            if DEBUG == true
            then
                print("Removing Double Air")
            end
            BTRAMOBJ:clearFlag(0x32, 7)
        end
    end
end


function obtain_swimming()
    if (FAST_SWIM == false or DOUBLE_AIR == false)
    then
        for apid, itemId in pairs(receive_map)
        do
            if itemId == "1230777"
            then
                if DEBUG == true
                then
                    print("Found Fast Swimming")
                end
                BTRAMOBJ:setFlag(0x1E, 5)
                FAST_SWIM = true
            end
            if itemId == "1230778"
            then
                if DEBUG == true
                then
                    print("Found Double Air")
                end
                BTRAMOBJ:setFlag(0x32, 7)
                DOUBLE_AIR = true
            end
        end
    end
end

--------------------------------- AMAZE-O-GAZE ------------------------------------
function check_goggles()
    if CURRENT_MAP == 0x143
    then
        local gogglesflg = BTRAMOBJ:checkFlag(0x30, 1, "CHECK_GOOGLES")
        local goggles_found = false
        if gogglesflg == true then
            GOGGLES = true
            for apid, item in pairs(receive_map)
            do
                if "1230779" == item
                then
                    goggles_found = true
                    break
                end
            end
            if goggles_found == false
            then
                BTRAMOBJ:clearFlag(0x1E, 0, "CHECK_GOOGLES")
            end
        end
    end
end

function check_real_goggles()
    if BTRAMOBJ:checkFlag(0x1E, 0) == false
    then
        for apid, item in pairs(receive_map)
        do
            if "1230779" == item
            then
                BTRAMOBJ:setFlag(0x1E, 0, "CHECK_GOOGLES")
                break
            end
        end
    end
end

--------------------------------- CHEATO REWARDS ----------------------------------
function init_CHEATO_REWARDS()
    for k,v in pairs(NON_AGI_MAP['CHEATO'])
    do
        CHEATO_REWARDS[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "CHECK_CHEATO")
    end
end

function watchCheato()
    if CURRENT_MAP == 0xAD then
        for k,v in pairs(NON_AGI_MAP['CHEATO'])
        do
            if CHEATO_REWARDS[k] == false
            then
                CHEATO_REWARDS[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "CHECK_CHEATO")
            end
        end
    end
end

function cheato_math_check()
    BTCONSUMEOBJ:changeConsumable("CHEATO");
    local spent_counter = 0
    local res = BTRAMOBJ:checkFlag(0x08, 4, "Cheato1")
    if res == true then
        spent_counter = spent_counter + 1
    end
    local res = BTRAMOBJ:checkFlag(0x08, 5, "Cheato2")
    if res == true then
        spent_counter = spent_counter + 1
    end
    local res = BTRAMOBJ:checkFlag(0x08, 6, "Cheato3")
    if res == true then
        spent_counter = spent_counter + 1
    end
    local res = BTRAMOBJ:checkFlag(0x08, 7, "Cheato4")
    if res == true then
        spent_counter = spent_counter + 1
    end
    local res = BTRAMOBJ:checkFlag(0x09, 0, "Cheato5")
    if res == true then
        spent_counter = spent_counter + 1
    end
    local spent_pages = 5 * spent_counter
    local recv_pages = 0

    for ap_id, memlocation in pairs(receive_map)
    do
        if memlocation == "1230513" then
            recv_pages = recv_pages + 1
        end
    end
    recv_pages = recv_pages - spent_pages
    BTCONSUMEOBJ:setConsumable(recv_pages);
end

--------------------------------- HONEY B REWARDS -----------------------------------

function init_HONEYB_REWARDS()
    for k,v in pairs(NON_AGI_MAP['HONEYB'])
    do
        HONEYB_REWARDS[k] = false
    end
end

function watchHoneyB()
    if CURRENT_MAP == 0x153 then
        local base_location_id = 1230996
        local bit1 = 0
        local bit2 = 0
        local bit3 = 0
        local result = BTRAMOBJ:checkFlag(0x98, 2, "CHECK_HONEYB1")
        if result == true
        then
            bit1 = 1
        end
        local result = BTRAMOBJ:checkFlag(0x98, 3, "CHECK_HONEYB2")
        if result == true
        then
            bit2 = 2
        end
        local result = BTRAMOBJ:checkFlag(0x98, 4, "CHECK_HONEYB3")
        if result == true
        then
            bit3 = 4
        end
        
        local final_res = bit1 + bit2 + bit3

        for i = 1230997, final_res + base_location_id, 1 do
            HONEYB_REWARDS[tostring(i)] = true
        end
        --TODO: Loop through base_location_id UNTIL the end number
        -- if final_res >= 1
        -- then
        --     HONEY_REWARDS[]
        -- end
    end
end

function honeycomb_math_check()
    BTCONSUMEOBJ:changeConsumable("HONEYCOMB");
    local bit1 = 0
    local bit2 = 0
    local bit3 = 0
    local result = BTRAMOBJ:checkFlag(0x98, 2, "CHECK_HONEYB1")
    if result == true
    then
        bit1 = 1
    end
    local result = BTRAMOBJ:checkFlag(0x98, 3, "CHECK_HONEYB2")
    if result == true
    then
        bit2 = 2
    end
    local result = BTRAMOBJ:checkFlag(0x98, 4, "CHECK_HONEYB3")
    if result == true
    then
        bit3 = 4
    end
    local final_res = bit1 + bit2 + bit3

    local honeycount = 0

    for ap_id, memlocation in pairs(receive_map)
    do
        if memlocation == "1230512" then
            honeycount = honeycount + 1
        end
    end
    if final_res >= 1 then
        honeycount = honeycount - 1
    end
    if final_res >= 2 then
        honeycount = honeycount - 3
    end
    if final_res >= 3 then
        honeycount = honeycount - 5
    end
    if final_res >= 4 then
        honeycount = honeycount - 7
    end
    if final_res == 5 then
        honeycount = honeycount - 9
    end
    BTCONSUMEOBJ:setConsumable(honeycount);
end

--------------------------------- JIGGY CHUNKS ----------------------------------
function init_JIGGY_CHUNK()
    for k,v in pairs(NON_AGI_MAP['JCHUNKS'])
    do
        JIGGY_CHUNKS[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "CHECK_JCHUNKS")
    end
end

function watchJChunk()
    if CURRENT_MAP == 0xC7 then
        for k,v in pairs(NON_AGI_MAP['JCHUNKS'])
        do
            if JIGGY_CHUNKS[k] == false
            then
                JIGGY_CHUNKS[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "CHECK_JCHUNKS")
            end
        end
    end
end

--------------------------------- Dino Kids -------------------------------------------
function init_DINO_KIDS()
    DINO_KIDS["1231006"] = false
    DINO_KIDS["1231007"] = false
    DINO_KIDS["1231008"] = false

end

function watchDinoFlags()
    if CURRENT_MAP == 0x118 then
        local scrut = BTRAMOBJ:checkFlag(0x0C, 2)

        local scrat_healed = BTRAMOBJ:checkFlag(0x26, 6)
        local scrat_train = BTRAMOBJ:checkFlag(0x2C, 1)

        local scrit_grow = BTRAMOBJ:checkFlag(0x26, 7)

        if scrut == true
        then
            DINO_KIDS["1231006"] = true
        end
        if scrat_healed == true and scrat_train == false
        then
            DINO_KIDS["1231007"] = true
        end
        if scrit_grow == true
        then
            DINO_KIDS["1231008"] = true
        end
    end
end

--------------------------------- BK MOVES ----------------------------------------------
function obtain_bkmove()
    for itemId, data in pairs(NON_AGI_MAP["BKMOVES"])
    do
        local res = BTRAMOBJ:checkFlag(data['addr'], data['bit'], data['name'])
        if res == false
        then
            for apid, item in pairs(receive_map)
            do
                if itemId == item
                then
                    if DEBUG == true
                    then
                        print("Found ".. data['name'])
                    end
                    BTRAMOBJ:setFlag(data['addr'], data['bit'])
                end
            end
        end
    end
end

function check_progressive()
    local beak_bust = 0
    local eggs = 0
    local shoes = 0
    local swim = 0
    local location = ""
    for ap_id, memloc in pairs(receive_map)
    do
        if memloc == "1230828"
        then
            beak_bust = beak_bust + 1
        end
        if memloc == "1230829"
        then
            eggs = eggs + 1
        end
        if memloc == "1230830"
        then
                shoes = shoes + 1
        end
        if memloc == "1230831"
        then
            swim = swim + 1
        end
    end

    if beak_bust == 1 then
        BTRAMOBJ:setFlag(0x18, 7, "Beak Buster")
    elseif beak_bust == 2 then
        BTRAMOBJ:setFlag(0x18, 7, "Beak Buster")
        location = "1230757"
        AGI_MOVES[location] = true
        set_AGI_MOVES_checks()
    end

    if eggs == 1 then
        AGI_MOVES["1230756"] = true
        set_AGI_MOVES_checks()
    elseif eggs == 2 then
        AGI_MOVES["1230756"] = true
        AGI_MOVES["1230759"] = true
        set_AGI_MOVES_checks()
    elseif eggs == 3 then
        AGI_MOVES["1230756"] = true
        AGI_MOVES["1230759"] = true
        AGI_MOVES["1230763"] = true
        set_AGI_MOVES_checks()
    elseif eggs == 4 then
        AGI_MOVES["1230756"] = true
        AGI_MOVES["1230759"] = true
        AGI_MOVES["1230763"] = true
        AGI_MOVES["1230767"] = true
        set_AGI_MOVES_checks()
    end

    if shoes == 1 then
        BTRAMOBJ:setFlag(0x1A, 3, "Stilt Stride")
    elseif shoes == 2 then
        BTRAMOBJ:setFlag(0x1A, 3, "Stilt Stride")
        BTRAMOBJ:setFlag(0x1A, 6, "Turbo Trainers")
    elseif shoes == 3 then
        BTRAMOBJ:setFlag(0x1A, 3, "Stilt Stride")
        BTRAMOBJ:setFlag(0x1A, 6, "Turbo Trainers")
        AGI_MOVES["1230768"] = true
        set_AGI_MOVES_checks()
    elseif shoes == 4 then
        BTRAMOBJ:setFlag(0x1A, 3, "Stilt Stride")
        BTRAMOBJ:setFlag(0x1A, 6, "Turbo Trainers")
        AGI_MOVES["1230768"] = true
        AGI_MOVES["1230773"] = true
        set_AGI_MOVES_checks()
    end

    if swim == 1 then
        BTRAMOBJ:setFlag(0x1A, 4, "Dive")
    elseif swim == 2 then
        BTRAMOBJ:setFlag(0x1A, 4, "Dive")
        BTRAMOBJ:setFlag(0x32, 7, "Double Air")
        DOUBLE_AIR = true
    elseif swim == 3 then
        BTRAMOBJ:setFlag(0x1A, 4, "Dive")
        BTRAMOBJ:setFlag(0x32, 7, "Double Air")
        BTRAMOBJ:setFlag(0x1E, 5, "Fast Swimming")
        FAST_SWIM = true
        DOUBLE_AIR = true
    end
end

--------------------------------- Stop N Swap --------------------------------

function init_BKMYSTERY(type) -- Initialize BMK
    local checks = {}
    if type == "BKMYSTERY"
    then
        BKMYSTERY['REMOVE'] = {}
        for k,v in pairs(NON_AGI_MAP['STOPNSWAP'])
        do
            BKMYSTERY[k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_BMK")
            BKMYSTERY['REMOVE'][k] = BTRAMOBJ:checkFlag(v['addr'], v['bit'], "INIT_BMK")
        end
        BKMYSTERY["1230958"] = false -- Ice key
        BKMYSTERY['REMOVE']["1230958"] = false
    else
        checks["1230799"] = false -- Icekey
        checks["1230800"] = false -- Bregull Bash
        checks["1230801"] = false -- Nothing
        checks["1230802"] = false -- Homing Eggs
        checks["1230803"] = false -- Blue egg
        checks["1230804"] = false -- Pink egg
        return checks;
    end
end

function check_egg_mystery()
    if ASSET_MAP_CHECK["STOPNSWAP"][CURRENT_MAP] == nil --Happens when exiting map too quickly when entering a new map
    then
        if CURRENT_MAP == 0x150 or CURRENT_MAP == 0x14F -- on Heggy map / Wooded Hollow, if you have eggs, enable flags
        then
            if EGGS_CLEARED == true
            then
                EGGS_CLEARED = false
                if DEBUG == true
                then
                  print("On Heggy's or Wooded Hollow Map")
                end
                for itemId, value in pairs(AGI_MYSTERY)
                do
                    if itemId == "1230803"
                    then
                        if value == true
                        then
                            local hatched = NON_AGI_MAP['STOPNSWAP']["1230955"]
                            if BTRAMOBJ:checkFlag(hatched['addr'], hatched['bit']) == false -- Egg not hatched yet
                            then
                                if DEBUG == true
                                then
                                    print("Ready to hand in Blue Egg")
                                end
                                local eggTable = NON_AGI_MAP['STOPNSWAP']["1230957"]
                                BTRAMOBJ:setFlag(eggTable['addr'], eggTable['bit'])
                            end
                        else
                            if DEBUG == true
                            then
                                print("Unsetting Local Blue Egg Flag")
                            end
                            if BKMYSTERY["1230957"] == true
                            then
                                local eggTable = NON_AGI_MAP['STOPNSWAP']["1230957"]
                                BTRAMOBJ:clearFlag(eggTable['addr'], eggTable['bit'])
                            end
                        end
                    end
                    if itemId == "1230804"
                    then
                        if value == true
                        then
                            local hatched = NON_AGI_MAP['STOPNSWAP']["1230954"]
                            if BTRAMOBJ:checkFlag(hatched['addr'], hatched['bit']) == false -- Egg not hatched yet
                            then
                                if DEBUG == true
                                then
                                    print("Ready to hand in Pink Egg")
                                end
                                local eggTable = NON_AGI_MAP['STOPNSWAP']["1230956"]
                                BTRAMOBJ:setFlag(eggTable['addr'], eggTable['bit'])
                            end
                        else
                            if DEBUG == true
                            then
                                print("Unsetting Local Pink Egg Flag")
                            end
                            if BKMYSTERY["1230956"] == true
                            then
                                local eggTable = NON_AGI_MAP['STOPNSWAP']["1230956"]
                                BTRAMOBJ:clearFlag(eggTable['addr'], eggTable['bit'])
                            end
                        end
                    end
                end
            end
        else -- on a different map, clearFlags
            if EGGS_CLEARED == true
            then
                return
            end

            for itemId, value in pairs(AGI_MYSTERY)
            do
                if itemId == "1230803"
                then
                    if value == true
                    then
                        local hatched = NON_AGI_MAP['STOPNSWAP']["1230955"]
                        if BTRAMOBJ:checkFlag(hatched['addr'], hatched['bit']) == false -- Egg not hatched yet
                        then
                            local eggTable = NON_AGI_MAP['STOPNSWAP']["1230957"]
                            if BKMYSTERY["1230957"] == true
                            then
                                if DEBUG == true
                                then
                                    print("Setting Local Blue Egg")
                                end
                                BTRAMOBJ:setFlag(eggTable['addr'], eggTable['bit'])
                            else
                                if DEBUG == true
                                then
                                    print("Clearing Blue Egg")
                                end
                                BTRAMOBJ:clearFlag(eggTable['addr'], eggTable['bit'])
                            end
                        end
                    else
                        if DEBUG == true
                        then
                            print("setting back Local Blue Egg Flag")
                        end
                        if BKMYSTERY["1230957"] == true
                        then
                            local eggTable = NON_AGI_MAP['STOPNSWAP']["1230957"]
                            BTRAMOBJ:setFlag(eggTable['addr'], eggTable['bit'])
                        end
                    end
                elseif itemId == "1230804"
                then
                    if value == true
                    then
                        local hatched = NON_AGI_MAP['STOPNSWAP']["1230954"]
                        if BTRAMOBJ:checkFlag(hatched['addr'], hatched['bit']) == false -- Egg not hatched yet
                        then
                            local eggTable = NON_AGI_MAP['STOPNSWAP']["1230956"]
                            if BKMYSTERY["1230956"] == true
                            then
                                if DEBUG == true
                                then
                                    print("Setting Local Pink Egg")
                                end
                                BTRAMOBJ:setFlag(eggTable['addr'], eggTable['bit'])
                            else
                                if DEBUG == true
                                then
                                    print("Clearing Pink Egg")
                                end
                                BTRAMOBJ:clearFlag(eggTable['addr'], eggTable['bit'])
                            end
                        end
                    else
                        if DEBUG == true
                        then
                            print("Unsetting Local Pink Egg Flag")
                        end
                        if BKMYSTERY["1230956"] == true
                        then
                            local eggTable = NON_AGI_MAP['STOPNSWAP']["1230956"]
                            BTRAMOBJ:setFlag(eggTable['addr'], eggTable['bit'])
                        end
                    end
                end
            end
            EGGS_CLEARED = true
        end
        return
    end
    local eggLocId = ASSET_MAP_CHECK["STOPNSWAP"][CURRENT_MAP];
    local eggTable = NON_AGI_MAP['STOPNSWAP'][eggLocId]
    local got_egg = BTRAMOBJ:checkFlag(eggTable['addr'], eggTable['bit'])
    if BKMYSTERY[eggLocId] == false
    then
        local eggTable = NON_AGI_MAP['STOPNSWAP'][eggLocId]
        local got_egg = BTRAMOBJ:checkFlag(eggTable['addr'], eggTable['bit'])
        BTCONSUMEOBJ:changeConsumable("Eggs")
        local egg_amt = BTCONSUMEOBJ:getEggConsumable()
        if got_egg == true and egg_amt > 0 and  BKMYSTERY['REMOVE'][eggLocId] == false
        then
            if DEBUG == true
            then
                print("Got a Local Mystery Egg")
            end
            BTCONSUMEOBJ:setConsumable(egg_amt - 1)
            BKMYSTERY['REMOVE'][eggLocId] = true
            BKMYSTERY[eggLocId] = true
            savingBMM()
        end
    end
end

function check_hatched_mystery()
    if CURRENT_MAP == 0x150  -- on Heggy map, if you have eggs, enable flags
    then
        if WAIT_FOR_HATCH == false
        then
            if AGI_MYSTERY["1230800"] == true and BKMYSTERY["1230954"] == false -- BBASH
            then
                if DEBUG == true then
                    print("Remove Bregull Bash")
                end
                local tbl = NON_AGI_MAP["STOPNSWAP"]["1230954"]
                BTRAMOBJ:clearFlag(tbl['addr'], tbl['bit'])
                BTRAMOBJ:clearFlag(0x1E, 7)
            elseif BKMYSTERY["1230954"] == true
            then
                local tbl = NON_AGI_MAP["STOPNSWAP"]["1230954"]
                BTRAMOBJ:setFlag(tbl['addr'], tbl['bit'])
                BTRAMOBJ:clearFlag(0x77, 5)
            end
            if AGI_MYSTERY["1230801"] == true and BKMYSTERY["1230953"] == false -- nothing
            then
                if DEBUG == true then
                    print("Remove Yellow Jinjo")
                end
                local tbl = NON_AGI_MAP["STOPNSWAP"]["1230953"]
                BTRAMOBJ:clearFlag(tbl['addr'], tbl['bit'])
            elseif BKMYSTERY["1230953"] == true
            then
                local tbl = NON_AGI_MAP["STOPNSWAP"]["1230953"]
                BTRAMOBJ:setFlag(tbl['addr'], tbl['bit'])
            end
            if AGI_MYSTERY["1230802"] == true and BKMYSTERY["1230955"] == false -- homing eggs
            then
                if DEBUG == true then
                    print("Remove Homing Eggs")
                end
                local tbl = NON_AGI_MAP["STOPNSWAP"]["1230955"]
                BTRAMOBJ:clearFlag(tbl['addr'], tbl['bit'])
            elseif BKMYSTERY["1230955"] == true
            then
                local tbl = NON_AGI_MAP["STOPNSWAP"]["1230955"]
                BTRAMOBJ:clearFlag(0x77, 3)
                BTRAMOBJ:setFlag(tbl['addr'], tbl['bit'])
            end
            WAIT_FOR_HATCH = true
        else -- Watch if Eggs are hatched
            if BKMYSTERY["1230954"] == false
            then
                local tbl = NON_AGI_MAP["STOPNSWAP"]["1230954"]
                if BTRAMOBJ:checkFlag(tbl['addr'], tbl['bit']) == true
                then
                    BKMYSTERY["1230954"] = true
                    BTRAMOBJ:clearFlag(0x1E, 7)
                end
            end
            if BKMYSTERY["1230953"] == false
            then
                local tbl = NON_AGI_MAP["STOPNSWAP"]["1230953"]
                if BTRAMOBJ:checkFlag(tbl['addr'], tbl['bit']) == true
                then
                    BKMYSTERY["1230953"] = true
                end
            end
            if BKMYSTERY["1230955"] == false
            then
                local tbl = NON_AGI_MAP["STOPNSWAP"]["1230955"]
                if BTRAMOBJ:checkFlag(tbl['addr'], tbl['bit']) == true
                then
                    BKMYSTERY["1230955"] = true
                end
            end
        end
    elseif CURRENT_MAP == 0x14F -- Wooded Hollow
    then
        if BKMYSTERY["1230954"] == true
        then
            local tbl = NON_AGI_MAP["STOPNSWAP"]["1230954"]
            BTRAMOBJ:clearFlag(0x77, 5)
            BTRAMOBJ:setFlag(tbl['addr'], tbl['bit'])
        end
        if BKMYSTERY["1230953"] == true
        then
            local tbl = NON_AGI_MAP["STOPNSWAP"]["1230953"]
            BTRAMOBJ:setFlag(tbl['addr'], tbl['bit'])
        end
        if BKMYSTERY["1230955"] == true
        then
            local tbl = NON_AGI_MAP["STOPNSWAP"]["1230955"]
            BTRAMOBJ:clearFlag(0x77, 3)
            BTRAMOBJ:setFlag(tbl['addr'], tbl['bit'])
        end
    else
        if BKMYSTERY["1230956"] == false
        then
            -- if DEBUG == true then
            --     print("reverse Hatch flag, Pink egg not yet obtained")
            -- end
            local tbl = NON_AGI_MAP["STOPNSWAP"]["1230954"]
            BTRAMOBJ:clearFlag(tbl['addr'], tbl['bit'])
        end
        if AGI_MYSTERY["1230800"] == false
        then
            BTRAMOBJ:clearFlag(0x1E, 7)
        end
        if BKMYSTERY["1230957"] == false
        then
            -- if DEBUG == true then
            --     print("reverse Hatch flag, Blue egg not yet obtained")
            -- end
            local tbl = NON_AGI_MAP["STOPNSWAP"]["1230955"]
            BTRAMOBJ:clearFlag(tbl['addr'], tbl['bit'])
        end
        -- if AGI_MYSTERY["1230802"] == true
        -- then
        --     local tbl = NON_AGI_MAP["STOPNSWAP"]["1230953"]
        --     -- BTRAMOBJ:setFlag(tbl['addr'], tbl['bit'])
        -- end
        WAIT_FOR_HATCH = false
    end
end

function obtain_breegull_bash()
    if AGI_MYSTERY["1230800"] == true and CURRENT_MAP ~= 0x150
    then
        if DEBUG == true
        then
            print("Setting BBASH")
        end
        BTRAMOBJ:setFlag(0x1E, 7)
    end
end

function check_local_icekey()
    local keyLocId = ASSET_MAP_CHECK["ICEKEY"][CURRENT_MAP];
    if BKMYSTERY[keyLocId] == false
    then
        BTCONSUMEOBJ:changeConsumable("Ice Keys")
        local key_amt = BTCONSUMEOBJ:getConsumable()

        if KEY_DROPPED == false
        then
            BTMODELOBJ:changeName("Player", false)
            local player = BTMODELOBJ:checkModel();
            if player == false
            then
                return
            end
            BTMODELOBJ:changeName("Ice Key", false);
            local key_spawn = BTMODELOBJ:checkModel()
            if key_spawn == true
            then
                if DEBUG == true
                then
                    print("Key Spawned")
                end
                KEY_DROPPED = true
            end
        end

        if KEY_DROPPED == true and KEY_GRABBED == false
        then
            BTMODELOBJ:changeName("Ice Key", false);
            local key_spawn = BTMODELOBJ:checkModel()
            if key_spawn == false
            then
                if DEBUG == true
                then
                    print("Key grabbed")
                end
                KEY_GRABBED = true
            end
        end

        if key_amt > 0 and KEY_DROPPED == true and KEY_GRABBED == true and BKMYSTERY['REMOVE'][keyLocId] == false
        then
            if DEBUG == true
            then
                print("Got a Local Ice Key")
            end
            if AGI_MYSTERY["1230799"] == false
            then
                if DEBUG == true
                then
                    print("Removing Key as we don't have AGI key yet")
                end
                BTCONSUMEOBJ:changeConsumable("Ice Keys")
                BTCONSUMEOBJ:setConsumable(key_amt - 1)
            end
            BKMYSTERY['REMOVE'][keyLocId] = true
            BKMYSTERY[keyLocId] = true
            savingBMM()
        end
    end
end

function pause_show_AGI_key()
    if AGI_MYSTERY["1230799"] == true and BKMYSTERY["1230958"] == false
    then
        if DEBUG == true
        then
            print("Setting Key")
        end
        BTCONSUMEOBJ:changeConsumable("Ice Keys")
        BTCONSUMEOBJ:setConsumable(1)
    end
end

function unpause_hide_AGI_key()
    if AGI_MYSTERY["1230799"] == true and BKMYSTERY["1230958"] == false
    then
        if DEBUG == true
        then
            print("Unsetting Key")
        end
        BTCONSUMEOBJ:changeConsumable("Ice Keys")
        BTCONSUMEOBJ:setConsumable(0)
    end
end

function ap_icekey_glowbo_map()
    if AGI_MYSTERY["1230799"] == true and BKMYSTERY["1230958"] == false and CURRENT_MAP == 0x128 --Icy Side
    then
        if DEBUG == true
        then
            print("Setting Key")
        end
        BTCONSUMEOBJ:changeConsumable("Ice Keys")
        BTCONSUMEOBJ:setConsumable(1)
    end
end

function clearKey()
    if AGI_MYSTERY["1230799"] == true and BKMYSTERY["1230958"] == false and CURRENT_MAP ~= 0x128 --Icy Side
    then
        if DEBUG == true
        then
            print("Unsetting Key")
        end
        BTCONSUMEOBJ:changeConsumable("Ice Keys")
        BTCONSUMEOBJ:setConsumable(0)
    end
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
        BTRAMOBJ:setFlag(0x0D, 5, "Levitate")
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

---------------------------------- JamJars MOVES -----------------------------------

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

------------------ DEATH LINK ---------------

function minigameMaps()
    if CURRENT_MAP == 0xC6 or CURRENT_MAP == 0xC8 or CURRENT_MAP == 0xC9  -- MT Kickballs
    then
        return true
    elseif CURRENT_MAP == 0x16F or CURRENT_MAP == 0x170 --Canary GGM Race
    then
        return true
    -- elseif CURRENT_MAP == 0xE4 or CURRENT_MAP == 0xE5 --Crazy Castle Minigames
    -- then
    --     return true
    elseif CURRENT_MAP == 0xDE or CURRENT_MAP == 0xDF or CURRENT_MAP == 0xE0 -- Dodgems
    then
        return true
    elseif CURRENT_MAP == 0x124 or CURRENT_MAP == 0x141 or CURRENT_MAP == 0x13C -- Saucer of Peril
    then
        return true
    -- elseif CURRENT_MAP == 0x17D -- GI Packing Game
    -- then
    --     return true
    elseif CURRENT_MAP == 0x12E or CURRENT_MAP == 0x12F or CURRENT_MAP == 0x130  -- HFP Kickballs
    then
        return true
    elseif CURRENT_MAP == 0x161 -- Canary CC Race
    then
        return true
    elseif CURRENT_MAP == 0x15F -- ToT
    then
        return true
    end
    return false
end

function cutsceneMaps()
    if CURRENT_MAP == 0x197 or CURRENT_MAP == 0x199 or CURRENT_MAP == 0xA3 or CURRENT_MAP == 0x18F 
    or CURRENT_MAP == 0x195 or CURRENT_MAP == 0x195 or CURRENT_MAP == 0xAC or CURRENT_MAP == 0x192
    or CURRENT_MAP == 0x193 or CURRENT_MAP == 0x19D or CURRENT_MAP == 0xA9 or CURRENT_MAP == 0xA5
    or CURRENT_MAP == 0xA2 or CURRENT_MAP == 0xA6 or CURRENT_MAP == 0x18C or CURRENT_MAP == 0x190
    or CURRENT_MAP == 0x198 or CURRENT_MAP == 0x18D or CURRENT_MAP == 0x196 or CURRENT_MAP == 0x18E
    or CURRENT_MAP == 0xAA or CURRENT_MAP == 0xAB or CURRENT_MAP == 0x159 or CURRENT_MAP == 0xA8
    or CURRENT_MAP == 0xA4 or CURRENT_MAP == 0x19C or CURRENT_MAP == 0x191 or CURRENT_MAP == 0xA1
    or CURRENT_MAP == 0x17E or CURRENT_MAP == 0x158
    then
        return true
    end
    return false
end

function setCurrentHealth(value)
	local currentTransformation = mainmemory.readbyte(0x11B065);
    local health_table = {
        [0x01] = 0x11B644, -- Main
        [0x10] = 0x11B65F, -- Banjo (Solo)
        [0x11] = 0x11B668, -- Mumbo
        [0x2E] = 0x11B66E, -- Detonator
        [0x2F] = 0x11B665, -- Submarine
        [0x30] = 0x11B677, -- T. Rex
        [0x31] = 0x11B653, -- Bee
        [0x32] = 0x11B647, -- Snowball
        [0x36] = 0x11B656, -- Washing Machine
        [0x5F] = 0x11B662, -- Kazooie (Solo)
    }
	if type(health_table[currentTransformation]) == 'number' then
		value = value or 0;
		value = math.max(0x00, value);
		value = math.min(0xFF, value);
		mainmemory.write_u8(health_table[currentTransformation], value);
        return currentTransformation
	end
    return false
end

function killBT()
    if KILL_BANJO == true then
        CHECK_DEATH = true -- Avoid Death loops
        BTMODELOBJ:changeName("Player", false)
        local player = BTMODELOBJ:checkModel();
        if player == false
        then
            return
        end
        if minigameMaps() == false and cutsceneMaps() == false and GAME_LOADED == true
        then 
            tranformation = setCurrentHealth(0)
            if type(tranformation) == 'number' then
                mainmemory.write_u16_be(0x12b062, 0x0100)--max air and suffocation flag?
                mainmemory.write_u16_be(0x12b068, 0x800C)--max air and suffocation flag?
                mainmemory.write_u16_be(0x12b06A, 0xF734)--max air and suffocation flag?
                local kill_animation = 0x01 -- funny drowning death
                if tranformation ~= 0x01
                then
                    kill_animation = 0x02 -- Explode 
                end 
                mainmemory.write_u8(0x12b161, kill_animation)--max air and suffocation flag?
                local death_flg = mainmemory.read_u8(0x1354F9)
                if death_flg == 1
                then
                    KILL_BANJO = false
                end
            end
        end
    end
end

function getBanjoDeath()
    if DEATH_LINK == true and KILL_BANJO == false
    then
        local death_flg = mainmemory.read_u8(0x1354F9)
        BTMODELOBJ:changeName("Player", false)
        local check = BTMODELOBJ:checkModel();
        if death_flg  == 0 and CHECK_DEATH == true
        then
            CHECK_DEATH = false
            return
        end
        if CHECK_DEATH == false and death_flg == 1
        then
            DETECT_DEATH = true
        end
    end
end

---------------------- MAP HANDLING -------------------

function watchMapTransition()
    if mainmemory.read_u8(0x127642) == 1
    then
        if MAP_TRANSITION == false then
            NEXT_MAP = BTRAMOBJ:getMap(true)
            MAP_TRANSITION = true
            BKAssetFound();
        end
    else
        finishTransition()
        jiggy_ui_update()
    end
end

function finishTransition()
    BTMODELOBJ:changeName("Player", false)
    local player = BTMODELOBJ:checkModel();
    local mapaddr = BTRAMOBJ:getMap(false)
    if mainmemory.read_u8(0x127642) == 0 and MAP_TRANSITION == true and player == true and mapaddr == NEXT_MAP
    then
        MAP_TRANSITION = false
        local mapaddr = BTRAMOBJ:getMap(false)
        BKLogics(mapaddr)
        if mapaddr ~= CURRENT_MAP
        then
            PREVIOUS_MAP = CURRENT_MAP
            CURRENT_MAP = mapaddr
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
    if(current_map == 0x142 or current_map == 0xAF or current_map == 0x160)
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
            BKMYSTERY = json.decode(f:read("l"));
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
            init_roysten()
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
            if ENABLE_AP_CHEATO_REWARDS == true then
                init_CHEATO_REWARDS()
            end
            init_JIGGY_CHUNK()
            init_DINO_KIDS()
            hag1_open()
            hag1_phase_skips()
            GAME_LOADED = true;
            DEMO_MODE = false;
        end
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
    check_freed_roysten()
    obtain_swimming()
    if ENABLE_AP_BK_MOVES ~= 0
    then
        obtain_bkmove()
    end
    if ENABLE_AP_CHEATO_REWARDS == true
    then
        watchCheato()
    end
    if ENABLE_AP_HONEYB_REWARDS == true
    then
        watchHoneyB()
    end
    watchJChunk()
    check_goggles()
    watchDinoFlags()
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
    if ((CURRENT_MAP ~= mapaddr) or player == false)
    then
        set_checked_BKNOTES();
        TREBLE_WAIT_TIMER = 0
        CHECK_FOR_TREBLE = true
        set_checked_BKSTATIONS()
        STATION_BTN_TIMER = 0
        CHECK_FOR_STATIONBTN = true
        honeycomb_math_check()
        cheato_math_check()
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
        clearKey()
        check_progressive()
        obtain_breegull_bash()
        check_real_goggles()
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
    check_egg_mystery()
    check_hatched_mystery()
    check_local_icekey()
    ap_icekey_glowbo_map()
 -- ApWarp();

end



function locationControl()
    local mapaddr = BTRAMOBJ:getMap(false)
    if mapaddr == nil --We don't want this to process anything
    then
        DEMO_MODE = true
        return DEMO_MODE
    end
    if SolvingPuzzle(mapaddr) == true
    then
        DEMO_MODE = true
        return DEMO_MODE
    end

    if USE_BMM_TBL == true --Only used If Pausing
    then
        if BTRAMOBJ:checkFlag(0x1F, 0, "LocControl1") == true -- DEMO FILE
        then
            DEMO_MODE = true
            return DEMO_MODE
        end
        DEMO_MODE = false
        BKLogics(mapaddr)
        getAltar()
        if ENABLE_AP_WORLDS == true
        then
            nearDisiple()
        end
        CURRENT_MAP = mapaddr
        return all_location_checks("BMM");
    else
        if GAME_LOADED == false
        then
            loadGame(mapaddr)
            DEMO = true
            return DEMO
        else
            DEMO_MODE = false
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
        gui.use_surface("client")
        bgcolor = "#590000"
        fgcolor = "#ca0000"
        local ratio = client.screenwidth() / client.screenheight()
        if ratio > 1.35
        then
            textXpos = math.floor(client.screenwidth()*.41)
            textYpos = math.floor(client.screenheight()*.70)
            textSize = math.floor((client.screenheight()*.03)+.5)
        else
            textXpos = math.floor(client.screenwidth()*.41)
            textYpos = math.floor(client.screenheight()*.65)
            textSize = math.floor((client.screenheight()*.03)+.5)
        end

        if TEXT_START == false
        then
            if DISABLE_TEXT_OVERLAY == false then
                gui.drawText(textXpos, textYpos, msg, fgcolor, bgcolor, textSize, nil, nil, "center")
            end
            TEXT_START = true
        end
end

function clearText()
    if TEXT_TIMER > 0
    then
        TEXT_TIMER = TEXT_TIMER - 1
    else
        gui.clearGraphics()
        TEXT_TIMER = 3
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
            elseif(memlocation == 1230515) -- Jiggy
            then
                obtained_AP_JIGGY()
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
            elseif memlocation == 1230516 -- Treble Clef
            then
                obtained_AP_BKNOTE();
            elseif(1230790 <= memlocation and memlocation <= 1230795) -- Station Btns
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
            elseif(memlocation == 1230800)
            then
                if DEBUG == true
                then
                    print("Breegull Bash Obtained")
                end
                AGI_MYSTERY[tostring(memlocation)] = true
                obtain_breegull_bash()
            elseif(memlocation == 1230801)
            then
                if DEBUG == true
                then
                    print("Jinjo Multiplayer Obtained")
                end
                AGI_MYSTERY[tostring(memlocation)] = true
            elseif(memlocation == 1230802)
            then
                if DEBUG == true
                then
                    print("Homing Obtained")
                end
                AGI_MYSTERY[tostring(memlocation)] = true
            elseif(memlocation == 1230803)
            then
                if DEBUG == true
                then
                    print("Blue Egg Obtained")
                end
                AGI_MYSTERY[tostring(memlocation)] = true
                BTCONSUMEOBJ:changeConsumable("Eggs")
                local amt = BTCONSUMEOBJ:getEggConsumable()
                BTCONSUMEOBJ:setConsumable(amt + 1)
            elseif(memlocation == 1230804)
            then
                if DEBUG == true
                then
                    print("Pink Egg Obtained")
                end
                AGI_MYSTERY[tostring(memlocation)] = true
                BTCONSUMEOBJ:changeConsumable("Eggs")
                local amt = BTCONSUMEOBJ:getEggConsumable()
                BTCONSUMEOBJ:setConsumable(amt + 1)
            elseif(memlocation == 1230799)
            then
                if DEBUG == true
                then
                    print("Ice Key Obtained")
                end
                AGI_MYSTERY[tostring(memlocation)] = true
                if BKMYSTERY["1230958"] == true
                then
                    BTCONSUMEOBJ:changeConsumable("Ice Keys")
                    BTCONSUMEOBJ:setConsumable(1)
                end
            elseif(memlocation == 1230823)
            then
                BTRAMOBJ:setFlag(0x1E, 6, "Blue Eggs")
                BTCONSUMEOBJ:changeConsumable("BLUE EGGS")
                BTCONSUMEOBJ:setConsumable(100)
            elseif(memlocation == 1230828) -- Progressive Beak Bust
            then
                local progressive_count = 0
                for ap_id, memloc in pairs(receive_map)
                do
                    if memloc == "1230828"
                    then
                        progressive_count = progressive_count + 1
                    end
                end
                if progressive_count == 0 then
                    BTRAMOBJ:setFlag(0x18, 7, "Beak Buster")
                end
                if progressive_count == 1 then
                    local location = "1230757"
                    AGI_MOVES[location] = true
                    set_AGI_MOVES_checks()
                end
            elseif(memlocation == 1230829) -- Progressive Eggs
            then
                local progressive_count = 0
                for ap_id, memloc in pairs(receive_map)
                do
                    if memloc == "1230829"
                    then
                        progressive_count = progressive_count + 1
                    end
                end
                if progressive_count == 0 then
                    local location = "1230756"
                    AGI_MOVES[location] = true
                    set_AGI_MOVES_checks()
                    BTCONSUMEOBJ:changeConsumable("FIRE EGGS")
                    BTCONSUMEOBJ:setConsumable(50)
                end
                if progressive_count == 1 then
                    local location = "1230759"
                    AGI_MOVES[location] = true
                    set_AGI_MOVES_checks()
                    BTCONSUMEOBJ:changeConsumable("GRENADE EGGS")
                    BTCONSUMEOBJ:setConsumable(25)
                end
                if progressive_count == 2 then
                    local location = "1230763"
                    AGI_MOVES[location] = true
                    set_AGI_MOVES_checks()
                    BTCONSUMEOBJ:changeConsumable("ICE EGGS")
                    BTCONSUMEOBJ:setConsumable(50)
                end
                if progressive_count == 3 then
                    local location = "1230767"
                    AGI_MOVES[location] = true
                    set_AGI_MOVES_checks()
                    BTCONSUMEOBJ:changeConsumable("CWK EGGS")
                    BTCONSUMEOBJ:setConsumable(10)
                end
            elseif(memlocation == 1230830) -- Progressive Shoes
            then
                local progressive_count = 0
                for ap_id, memloc in pairs(receive_map)
                do
                    if memloc == "1230830"
                    then
                        progressive_count = progressive_count + 1
                    end
                end
                if progressive_count == 0 then
                    BTRAMOBJ:setFlag(0x1A, 3, "Stilt Stride")
                end
                if progressive_count == 1 then
                    BTRAMOBJ:setFlag(0x1A, 6, "Turbo Trainers")
                end
                if progressive_count == 2 then
                    local location = "1230768"
                    AGI_MOVES[location] = true
                    set_AGI_MOVES_checks()
                end
                if progressive_count == 3 then
                    local location = "1230773"
                    AGI_MOVES[location] = true
                    set_AGI_MOVES_checks()
                end
            elseif(memlocation == 1230831) -- Progressive Water Training
            then
                local progressive_count = 0
                for ap_id, memloc in pairs(receive_map)
                do
                    if memloc == "1230831"
                    then
                        progressive_count = progressive_count + 1
                    end
                end
                if progressive_count == 0 then
                    BTRAMOBJ:setFlag(0x1A, 4, "Dive")
                end
                if progressive_count == 1 then
                    BTRAMOBJ:setFlag(0x32, 7, "Double Air")
                    DOUBLE_AIR = true
                end
                if progressive_count == 2 then
                    BTRAMOBJ:setFlag(0x1E, 5, "Fast Swimming")
                    FAST_SWIM = true
                end
            elseif(memlocation == 1230832) -- Progressive Bash Attack
            then
                local progressive_count = 0
                for ap_id, memloc in pairs(receive_map)
                do
                    if memloc == "1230832"
                    then
                        progressive_count = progressive_count + 1
                    end
                end
                if progressive_count == 0 then
                    BTRAMOBJ:setFlag(0x19, 1, "GRAT")
                end
                if progressive_count == 1 then
                    AGI_MYSTERY["1230800"] = true
                    obtain_breegull_bash()
                end
            elseif(memlocation == 1230779) --amaze-o-gaze
            then
                BTRAMOBJ:setFlag(0x1E, 0, "AMAZE-O-GAZE")
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
    if next(block['items']) ~= nil and INIT_COMPLETE
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
    if block['triggerDeath'] == true
    then
        KILL_BANJO = true;
    end

    if DEBUGLVL3 == true then
        print(block)
    end
end

function SendToBTClient()
    local retTable = {}
    retTable["scriptVersion"] = SCRIPT_VERSION;
    retTable["playerName"] = PLAYER;
    retTable["deathlinkActive"] = DEATH_LINK;
    --retTable['locations'] = locationControl()
    retTable["jiggies"] = jiggy_check()
    retTable['unlocked_moves'] = BKM;
    retTable['treble'] = BKNOTES;
    retTable['stations'] = BKSTATIONS;
    retTable['chuffy'] = BKCHUFFY;
    retTable["isDead"] = DETECT_DEATH;
    retTable["jinjofam"] = BKJINJOFAM;
    retTable["worlds"] = UNLOCKED_WORLDS;
    retTable["mystery"] = BKMYSTERY;
    retTable["roysten"] = ROYSTEN;
    retTable["cheato_rewards"] = CHEATO_REWARDS;
    retTable["honeyb_rewards"] = HONEYB_REWARDS;
    retTable["jiggy_chunks"] = JIGGY_CHUNKS;
    retTable["goggles"] = GOGGLES;
    retTable["dino_kids"] = DINO_KIDS;
    retTable["DEMO"] = DEMO_MODE;
    
    if CURRENT_MAP == nil
    then
        retTable["banjo_map"] = 0x0;
    else
        retTable["banjo_map"] = CURRENT_MAP;
    end 
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
        PRINT_GOAL = true;
        CUR_STATE = STATE_OK
    end
    if DETECT_DEATH == true
    then
        DETECT_DEATH = false
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
        backup_BMM_JIGGIES()
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
        if SKIP_PUZZLES == false then
            if CURRENT_MAP ~= 0x14F and CURRENT_MAP ~= 0x151  -- Don't want to restore while in WH zone
            then
                print(CURRENT_MAP)
                restore_BMM_JIGGIES()
                BMMRestore()
            end
        end
        
        unpause_hide_AGI_key()
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
        
        -- Object and Items 
        total = mainmemory.readbyte(0x123A88);
        if total == 1 and OBJ_TOTALS_MENU == false
        then
            OBJ_TOTALS_MENU = true
            pause_show_AGI_key()
        elseif total ~= 1 and OBJ_TOTALS_MENU == true
        then
            OBJ_TOTALS_MENU = false
            unpause_hide_AGI_key()
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
            if ENABLE_AP_BK_MOVES ~= 0 
            then
                for locationId, table in pairs(NON_AGI_MAP["BKMOVES"])
                do
                    if BTRAMOBJ:checkFlag(table['addr'], table['bit']) == true
                    then
                        print(table['name'])
                    end
                end
            end
            for locationId, values in pairs(NON_AGI_MAP["MOVES"])
            do             
                if AGI_MOVES[locationId] == true
                then
                    print(values['name'])
                end
            end
            if AGI_MYSTERY["1230800"] == true
            then
                print("Breegull Bash");
            end
            if FAST_SWIM == true
            then
                print("Fast Swimming")
            end
            if DOUBLE_AIR == true
            then
                print("Double Air")
            end
            print(" ")
            print(" ")
            print("Unlocked Worlds")
            for world, table in pairs(WORLD_ENTRANCE_MAP)
            do
                if table["opened"] == true
                then
                    print(table["defaultName"])
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
            if GOAL_TYPE ~= 0
            then
                local token_count = 0;
                for id, itemId in pairs(receive_map)
                do
                    if itemId == "1230798"
                    then
                        token_count = token_count + 1
                    end
                end
                print(" ")
			    print("Collected Mumbo Tokens: "..token_count)
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
            if ENABLE_AP_MYSTERY == true
            then
                if AGI_MYSTERY["1230802"] == true
                then
                    BTRAMOBJ:setFlag(0xAF, 3, "Aim Assist")
                    AIMASSIST = true
                    print(" ")
                    print("Aim Assist Enabled")
                else
                    print("Homing Eggs not found")
                end
            else
                BTRAMOBJ:setFlag(0xAF, 3, "Aim Assist")
                AIMASSIST = true
                print(" ")
                print("Aim Assist Enabled")
            end
        elseif check_controls ~= nil and check_controls['P1 DPad L'] == true and check_controls['P1 L'] == true and AIMASSIST == true
        then
            BTRAMOBJ:clearFlag(0xAF, 3)
            AIMASSIST = false
            print(" ")
            print("Aim Assist Disabled")
        end
		
		if check_controls ~= nil and check_controls['P1 DPad D'] == true and check_controls['P1 L'] == true and REGEN == false
        and DEATH_LINK == false
        then
           BTRAMOBJ:setFlag(0xA1, 7, "Automatic Energy Regain")
           REGEN = true
           print(" ")
           print("Automatic Energy Regain Enabled")
        elseif check_controls ~= nil and check_controls['P1 DPad D'] == true and check_controls['P1 L'] == true and REGEN == true
        and DEATH_LINK == false
        then
            BTRAMOBJ:clearFlag(0xA1, 7)
            REGEN = false
            print(" ")
            print("Automatic Energy Regain Disabled")
        end

        if check_controls ~= nil and check_controls['P1 L'] == true and check_controls['P1 Start'] == true and FPS == false
        then
            mainmemory.write_u8(0x07913F, 1)
            print("Smooth Banjo Enabled")
            FPS = true
        elseif check_controls ~= nil and check_controls['P1 L'] == true and check_controls['P1 Start'] == true and FPS == true
        then
            mainmemory.write_u8(0x07913F, 2)
            print("Smooth Banjo Disabled")
            FPS = false
        end
    end
end

function savingAGI()
    local f = io.open("BT" .. PLAYER .. "_" .. SEED .. ".AGI", "w") --generate #BTplayer_seed.AGI
    if DEBUGLVL2 == true
    then
        print("Writing AGI File from Saving");
        print(AGI)
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
        print("Writing MYSTERY");
    end
    f:write(json.encode(AGI_MYSTERY) .. "\n");
    -- if DEBUGLVL2 == true
    -- then
    --     print("Writing Traps");
    -- end
    -- f:write(json.encode(AGI_TRAPS) .. "\n");
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
        if next(AGI_MYSTERY) == nil then
            AGI_MYSTERY = init_BKMYSTERY("AGI");
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
        f:write(json.encode(AGI_MYSTERY) .. "\n");
     -- f:write(json.encode(AGI_TRAPS) .. "\n");
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
        AGI_MYSTERY = json.decode(f:read("l"));
     -- AGI_TRAPS = json.decode(f:read("l"));
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
    f:write(json.encode(BKJINJOFAM) .. "\n");
    f:write(json.encode(BKMYSTERY));
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
        print("slot_data")
        print(block)
        print("EO_slot_data")
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
    if block['slot_disable_text'] ~= nil and block['slot_disable_text'] ~= "false"
    then
        DISABLE_TEXT_OVERLAY = true
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
    if block['slot_bkmoves'] ~= nil and block['slot_bkmoves'] ~= "false"
    then
        ENABLE_AP_BK_MOVES = block['slot_bkmoves']
    end
    if block['slot_cheatorewards'] ~= nil and block['slot_cheatorewards'] ~= "false"
    then
        ENABLE_AP_CHEATO_REWARDS = true
    end
    if block['slot_honeybrewards'] ~= nil and block['slot_honeybrewards'] ~= "false"
    then
        ENABLE_AP_HONEYB_REWARDS = true
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
    if block['slot_skip_klungo'] ~= nil and block['slot_skip_klungo'] ~= "false"
    then
        SKIP_KLUNGO = true
    end
    if block['slot_skip_king'] ~= nil and block['slot_skip_king'] ~= "false"
    then
        SKIP_KING = true
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
    if block['slot_mystery'] ~= nil and block['slot_mystery'] ~= "false"
    then
        ENABLE_AP_MYSTERY = true
    end
    if block['slot_goal_type'] ~= nil and block['slot_goal_type'] ~= ""
    then
        GOAL_TYPE = block['slot_goal_type']
    end
    if block['slot_minigame_hunt_length'] ~= nil and block['slot_minigame_hunt_length'] ~= ""
    then
        MGH_LENGTH = block['slot_minigame_hunt_length']
    end
    if block['slot_boss_hunt_length'] ~= nil and block['slot_boss_hunt_length'] ~= ""
    then
        BH_LENGTH = block['slot_boss_hunt_length']
    end
    if block['slot_jinjo_family_rescue_length'] ~= nil and block['slot_jinjo_family_rescue_length'] ~= ""
    then
        JFR_LENGTH = block['slot_jinjo_family_rescue_length']
    end
    if block['slot_token_hunt_length'] ~= nil and block['slot_token_hunt_length'] ~= ""
    then
        TH_LENGTH = block['slot_token_hunt_length']
    end
    -- if block['slot_warp_traps'] ~= nil and block['slot_warp_traps'] ~= ""
    -- then
    --     WARP_TRAP_LOGIC = block['slot_warp_traps']
    -- end
    if block['slot_world_order'] ~= nil
    then
        for level, jiggy_amt in pairs(block['slot_world_order'])
        do
            local locationId = block['slot_keys'][level]
            if level == "Outside Grunty's Industries"
            then
                level = "Grunty Industries"
            elseif  level == "Jolly Roger's Lagoon - Town Center"
            then
                level = "Jolly Roger's Lagoon"
            end
            for worlds, t in pairs(WORLD_ENTRANCE_MAP)
            do
                if t['defaultName'] == level
                then
                    WORLD_ENTRANCE_MAP[worlds]["defaultCost"] = jiggy_amt
                    WORLD_ENTRANCE_MAP[worlds]["locationId"] = tostring(locationId)
                end
            end
        end
    end
    if block['slot_version'] ~= nil and block['slot_version'] ~= ""
    then
        CLIENT_VERSION = block['slot_version']
        if CLIENT_VERSION ~= BT_VERSION
        then
            VERROR = true
            return false
        end
    end
    printGoalInfo();
    if SEED ~= 0
    then
        loadAGI()
    else
        return false
    end
    return true
end


function printGoalInfo()
    local randomEncouragment = ENCOURAGEMENT[math.random(1, #ENCOURAGEMENT)]["message"]
    if GOAL_TYPE ~= nil and MGH_LENGTH ~= nil and BH_LENGTH ~= nil and 
    JFR_LENGTH ~= nil and TH_LENGTH ~= nil then
        local message = ""
        if GOAL_TYPE == 0 then
            message = "You need to hunt down Grunty in her HAG1 \nand put her back in the ground!"..randomEncouragment;
        elseif GOAL_TYPE == 1 and MGH_LENGTH == 15 then
            message = "You are hunting down all 15 of the Mumbo Tokens \nfound in Grunty's dastardly minigames! Good luck and"..randomEncouragment;
        elseif GOAL_TYPE == 1 and MGH_LENGTH < 15 then
            message = "You are hunting for "..MGH_LENGTH.." Mumbo Tokens from \nGrunty's dastardly minigames! Good Luck and"..randomEncouragment;
        elseif GOAL_TYPE == 2 and BH_LENGTH == 8 then
            message = "You are hunting down all 8 Mumbo Tokens from \neach world boss! Good Luck and"..randomEncouragment;
        elseif GOAL_TYPE == 2 and BH_LENGTH < 8 then
            message = "You are hunting for "..BH_LENGTH.." Mumbo Tokens from \nthe 8 world bosses! Good Luck and"..randomEncouragment;
        elseif GOAL_TYPE == 3 and JFR_LENGTH == 9 then
            message ="You are trying to rescue all 9 Jinjo families and \nretrieve their Mumbo Tokens! Good Luck and"..randomEncouragment;
        elseif GOAL_TYPE == 3 and JFR_LENGTH < 9 then
            message = "You are trying to rescue "..JFR_LENGTH.." of the 9 Jinjo families \nand retrieve their Mumbo Tokens! Good Luck and"..randomEncouragment;
        elseif GOAL_TYPE == 4 then
            message ="You absolute mad lad! You're doing the Wonder Wing Challenge! Good Luck and"..randomEncouragment;
        elseif GOAL_TYPE == 5 and TH_LENGTH == 15 then
            message ="You are trying to find all 15 of Mumbo's Tokens scattered \nthroughout the Isle of Hags! Good Luck and"..randomEncouragment;
        elseif GOAL_TYPE == 5 and TH_LENGTH < 15 then
            message = "You are trying to find "..TH_LENGTH.." of the 15 of Mumbo Tokens \nscattered throughout the Isle of Hags! Good Luck and"..randomEncouragment;
        end
        print(message)
        table.insert(AP_MESSAGES, message);
    end
end


function initializeFlags()
	-- Use Cutscene: "2 Years Have Passed..." to check for fresh save
	local current_map = BTRAMOBJ:getMap(false);
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
        DEMO_MODE = false
        init_BMK("BKM");
        init_BKNOTES("BKNOTES");
        init_BKSTATIONS("BKSTATIONS");
        init_CHUFFY("BKCHUFFY");
        init_JinjoFam();
        init_BKMYSTERY("BKMYSTERY")
        init_roysten()
        init_DINO_KIDS()
        init_JIGGIES("BMM")
        AGI_MOVES = init_BMK("AGI");
        AGI_NOTES = init_BKNOTES("AGI");
        AGI_MYSTERY = init_BKMYSTERY("AGI");
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
        hag1_open()

        if ENABLE_AP_JINJO == true then
            -- 129 is 1000 0001
            -- 2 is   0000 0010
            if DEBUG == true
            then
                print("Setting Jinjo Pattern")
            end
            BTRAMOBJ:setMultipleFlags(0x6A, 129, 2)
        end
        if SKIP_KLUNGO == true then
            --{byte=0x5E, bit=0, name="Klungo 1 Defeated", type="Progress"},
	        --{byte=0x5E, bit=1, name="Klungo 2 Defeated", type="Progress"},
            BTRAMOBJ:setFlag(0x5E, 0, "Klungo 1 Defeated")
            BTRAMOBJ:setFlag(0x5E, 1, "Klungo 2 Defeated")
        end
        if ENABLE_AP_BK_MOVES ~= 0 then
            BTRAMOBJ:clearFlag(0x1A, 4) -- Dive
            BTRAMOBJ:clearFlag(0x19, 6) -- Fly pad
            BTRAMOBJ:clearFlag(0x19, 5) -- Flap Flip
            BTRAMOBJ:clearFlag(0x19, 3) -- Can't Shoot or Poop Eggs
            BTRAMOBJ:clearFlag(0x1A, 1) -- Roll

            BTRAMOBJ:clearFlag(0x1A, 0) -- Air Rat-atat-rap
            BTRAMOBJ:clearFlag(0x1A, 6) -- Turbo Trainers
            BTRAMOBJ:clearFlag(0x18, 7) -- Beak Buster
            if ENABLE_AP_BK_MOVES == 2 then
                BTRAMOBJ:clearFlag(0x1A, 5) -- Talon Trot
                BTRAMOBJ:clearFlag(0x19, 7) -- Full Jump
            end
            BTRAMOBJ:clearFlag(0x19, 2) -- Climb
            BTRAMOBJ:clearFlag(0x19, 4) -- Feather Flap
            BTRAMOBJ:clearFlag(0x1A, 7) -- Full Jump
            BTRAMOBJ:clearFlag(0x1E, 6) -- Blue Eggs
            BTRAMOBJ:clearFlag(0x19, 1) -- Ground Rat-a-tat rap
            BTRAMOBJ:clearFlag(0x18, 5) -- Beak Barge
            BTRAMOBJ:clearFlag(0x1A, 3) -- Stilt Stride
            BTRAMOBJ:clearFlag(0x18, 6) -- Beak Bomb

            if ENABLE_AP_WORLDS == true then -- Randomize Worlds - SILOS!!!
                init_world_silos()
            end
        end
        if ENABLE_AP_CHEATO_REWARDS == true then
            init_CHEATO_REWARDS()
        end
        if ENABLE_AP_HONEYB_REWARDS == true then
            init_HONEYB_REWARDS()
        end
        init_JIGGY_CHUNK()
        BTCONSUMEOBJ:changeConsumable("Eggs")
        BTCONSUMEOBJ:setConsumable(0)
        BTCONSUMEOBJ:changeConsumable("Ice Keys")
        BTCONSUMEOBJ:setConsumable(0)
        BTRAMOBJ:setFlag(0x60, 3) --sets prison compound code to sun, moon, star,moon, sun 

        if SKIP_KING == true
        then
            BTRAMOBJ:setFlag(0xA7, 1)
            BTRAMOBJ:setFlag(0x2F, 5)
            BTRAMOBJ:setFlag(0x53, 6)
            BTRAMOBJ:setFlag(0x50, 1)
            BTRAMOBJ:setFlag(0x67, 0)

        end
        hag1_phase_skips()
        
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
    mainmemory.writebyte(0x12C78D, 64); -- Skips Intro waiting
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
            if (FRAME % 30 == 1) then
                BTRAM:banjoPTR()
                receive();
                if VERROR == true
                then
                    print("ERROR: Banjo_Tooie_connector Mismatch. Please obtain the correct version")
                    print("Connector Version: " .. BT_VERSION)
                    print("Client Version: " .. CLIENT_VERSION)
                    return
                end
                if SKIP_TOT == "true" and CURRENT_MAP == 0x15E then
					setToTComplete();
				end
                if SAVE_GAME == true
                then
                    saveGame();
                end
                BKCheckAssetLogic()
                gameSaving();
                hag1_open()
                if TEXT_START == true then
                    clearText()
                elseif TEXT_START == false then
                    processMessages()
                end
                getBanjoDeath()
                killBT()
            elseif (FRAME % 5 == 1)
            then
                watchMapTransition()
                if SKIP_PUZZLES == false
                then
                    no_puzzle_skip()
                end
                checkPause();
                checkTotalMenu();
                if not (INIT_COMPLETE) or CURRENT_MAP == 0x158 then
					initializeFlags();
				end
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
