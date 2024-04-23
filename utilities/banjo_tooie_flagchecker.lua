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


local RAM_FLG = {}

function initRamFlags(BTRAMOBJ)
    local starting_hex = 0x00
    local end_hex = 0xB0
    for hex = starting_hex, end_hex, 1
    do
        RAM_FLG[hex] = {}
        local first_bit = 0
        local last_bit = 7
        for bit = first_bit, last_bit, 1
        do
            RAM_FLG[hex][bit] = false
        end
    end
end

function checkRamFlags(BTRAMOBJ)
    local starting_hex = 0x00
    local end_hex = 0xB0
    for hex = starting_hex, end_hex, 1
    do
        local first_bit = 0
        local last_bit = 7
        for bit = first_bit, last_bit, 1
        do
            if RAM_FLG[hex][bit] == false
            then
                local check = BTRAMOBJ:checkFlag(hex, bit)
                if check == true
                then
                    print("Flag Hex number: " .. toHexString(hex) .. " bit:" .. tostring(bit) .. " Is now set")
                    RAM_FLG[hex][bit] = true
                end
            end
        end
    end
end

function main()
    BTRAMOBJ = BTRAM:new(nil);
    initRamFlags(BTRAMOBJ)
    while true do
        FRAME = FRAME + 1
        if (FRAME % 60 == 1) then
            checkRamFlags(BTRAMOBJ)
        end
        emu.frameadvance()
    end
end

main()
