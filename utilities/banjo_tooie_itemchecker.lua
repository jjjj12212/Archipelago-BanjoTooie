local RAM_FLG = {}
local FRAME = 0

string.lpad = function(str, len, char)
	if type(str) ~= "str" then
		str = tostring(str);
	end
	if char == nil then char = ' ' end
	return string.rep(char, len - #str)..str;
end

function toHexString(value, desiredLength, prefix)
	value = string.format("%X", value or 0);
	value = string.lpad(value, desiredLength or string.len(value), '0');
	return (prefix or "0x")..value;
end

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
        [59] = {key=0x8FBF, name="Ice Keys"}, -- Stop'n'Swop -- to write, use id 19
        [20] = {key=0x1461, name="MEGA GLOWBO",max=1},
        [21] = {key=0x7680, name="???1"},
        [22] = {key=0x0DE3, name="???2"},
        [23] = {key=0x5E79, name="???3"},
        [24] = {key=0x5E79, name="???4"},
        [25] = {key=0x5E79, name="???5"},
        [26] = {key=0x5E79, name="???6"},
        [27] = {key=0x5E79, name="???7"},
		[29] = {key=0x5E79, name="Green Idols"},

    };
    consumeIndex = nil;
    consumeKey = nil;
    consumeName = nil;
}

function BTConsumable:new(BTRAM)
    setmetatable({}, self)
    self.__index = self
    self.banjoRAM = BTRAM;
   return self
end

function BTConsumable:getConsumable(index)
    local amount = mainmemory.read_u16_be(self.CONSUME_IDX + index * 0x0C);
	return amount;
end

function BTConsumable:setConsumable(index, value)
    key = self.consumeTable[index]["key"]
    local addr = self.banjoRAM:dereferencePointer(self.CONSUME_PTR);
    if index == 59
    then
        mainmemory.write_u16_be(addr + 19 * 2, value ~ key);
    else
        mainmemory.write_u16_be(addr + index * 2, value ~ key);

    end
    mainmemory.write_u16_be(self.CONSUME_IDX + index * 0x0C, value);

end

function BTConsumable:getTable()
    return self.consumeTable
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

RAM_CONSUME = {}

function initConsumeTable(BTCONSUME)
    table = BTCONSUME:getTable()
    for key, item_table in pairs(table) do
        RAM_CONSUME[item_table['name']] = {
            ['key'] = key,
            ['amt'] = 0
        }
    end
end

function checkconsumableAmts(BTCONSUME)
    for item, table in pairs(RAM_CONSUME)
    do
        amt = BTCONSUME:getConsumable(table['key'])
        if amt ~= table['amt']
        then
            print("Picked up: " .. item .. " new count: " .. tostring(amt))
            RAM_CONSUME[item]['amt'] = amt
        end
        -- Uncomment to set Consumables
        -- if table['key'] == 59 or table['key'] == 18 or table['key'] == 15 then
        --     BTCONSUME:setConsumable(table['key'], 9999)
        -- end
    end
end

function main()
    BTRAMOBJ = BTRAM:new(nil);
    BTCONSUME = BTConsumable:new(BTRAMOBJ)
    initConsumeTable(BTCONSUME)
    while true do
        FRAME = FRAME + 1
        if (FRAME % 60 == 1) then
            checkconsumableAmts(BTCONSUME)
        end
        emu.frameadvance()
    end
end

main()
