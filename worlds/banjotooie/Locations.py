from BaseClasses import Location
import typing
from .Names import locationName


class BanjoTooieLocation(Location):
    game: str = "Banjo Tooie"
    
class LocationData(typing.NamedTuple):
    #BAD 12C780 pointer (1230720) increment
    #12C770 pointer instead (1230704)
    btid: int = 0
    # Save + mem addr
    memaddr: int = 0
    # some items have bitmasks. if bitmask>0 bitor to give item else
    bitmask: int = 0

SMLoc_table = {
    locationName.CHEATOSM1: LocationData(1230752, 0x59, 3),
    locationName.JINJOIH5: LocationData(1230595, 0x3F, 0)
}

JVLoc_table = {
    locationName.JIGGYIH1:  LocationData(1230676, 0x4F, 0),
    locationName.JIGGYIH2:  LocationData(1230677, 0x4F, 1),
    locationName.JIGGYIH3:  LocationData(1230678, 0x4F, 2),
    locationName.JIGGYIH4:  LocationData(1230679, 0x4F, 3),
    locationName.JIGGYIH5:  LocationData(1230680, 0x4F, 4),
    locationName.JIGGYIH6:  LocationData(1230681, 0x4F, 5),
    locationName.JIGGYIH7:  LocationData(1230682, 0x4F, 6),
    locationName.JIGGYIH8:  LocationData(1230683, 0x4F, 7),
    locationName.JIGGYIH9:  LocationData(1230684, 0x50, 0),
    locationName.JIGGYIH10: LocationData(1230685, 0x50, 1)
}

MTLoc_Table = {
    locationName.JINJOMT1: LocationData(1230551, 0x39, 4), 
    locationName.JINJOMT2: LocationData(1230552, 0x39, 5),
    locationName.JINJOMT3: LocationData(1230553, 0x39, 6),
    locationName.JINJOMT4: LocationData(1230554, 0x39, 7),
    locationName.JINJOMT5: LocationData(1230555, 0x3A, 0),
    locationName.JIGGYMT1:  LocationData(1230596, 0x45, 0),
    locationName.JIGGYMT2:  LocationData(1230597, 0x45, 1),
    locationName.JIGGYMT3:  LocationData(1230598, 0x45, 2),
    locationName.JIGGYMT4:  LocationData(1230599, 0x45, 3),
    locationName.JIGGYMT5:  LocationData(1230600, 0x45, 4),
    locationName.JIGGYMT6:  LocationData(1230601, 0x45, 5),
    locationName.JIGGYMT7:  LocationData(1230602, 0x45, 6),
    locationName.JIGGYMT8:  LocationData(1230603, 0x45, 7),
    locationName.JIGGYMT9:  LocationData(1230604, 0x46, 0),
    locationName.JIGGYMT10: LocationData(1230605, 0x46, 1),
    locationName.GLOWBOMT1: LocationData(1230686, 0x42, 7),
    locationName.GLOWBOMT2: LocationData(1230687, 0x43, 0),
    locationName.HONEYCMT1: LocationData(1230703, 0x3F, 2),
    locationName.HONEYCMT2: LocationData(1230704, 0x3F, 3),
    locationName.HONEYCMT3: LocationData(1230705, 0x3F, 4),
    locationName.CHEATOMT1: LocationData(1230728, 0x56, 3),
    locationName.CHEATOMT2: LocationData(1230729, 0x56, 4),
    locationName.CHEATOMT3: LocationData(1230730, 0x56, 5),
}

IHPLLoc_table = {
    locationName.JINJOIH4: LocationData(1230594, 0x3E, 7),
    locationName.HONEYCIH1: LocationData(1230727, 0x42, 2)
}

GMLoc_table = {
    locationName.JINJOGM1: LocationData(1230556, 0x3A, 1),
    locationName.JINJOGM2: LocationData(1230557, 0x3A, 2),
    locationName.JINJOGM3: LocationData(1230558, 0x3A, 3),
    locationName.JINJOGM4: LocationData(1230559, 0x3A, 4),
    locationName.JINJOGM5: LocationData(1230560, 0x3A, 5),
    locationName.JIGGYGM1:  LocationData(1230606, 0x46, 2),
    locationName.JIGGYGM2:  LocationData(1230607, 0x46, 3),
    locationName.JIGGYGM3:  LocationData(1230608, 0x46, 4),
    locationName.JIGGYGM4:  LocationData(1230609, 0x46, 5),
    locationName.JIGGYGM5:  LocationData(1230610, 0x46, 6),
    locationName.JIGGYGM6:  LocationData(1230611, 0x46, 7),
    locationName.JIGGYGM7:  LocationData(1230612, 0x47, 0),
    locationName.JIGGYGM8:  LocationData(1230613, 0x47, 1),
    locationName.JIGGYGM9:  LocationData(1230614, 0x47, 2),
    locationName.JIGGYGM10: LocationData(1230615, 0x47, 3),
    locationName.GLOWBOGM1: LocationData(1230688, 0x43, 1),
    locationName.GLOWBOGM2: LocationData(1230689, 0x43, 2),
    locationName.HONEYCGM1: LocationData(1230706, 0x3F, 5),
    locationName.HONEYCGM2: LocationData(1230707, 0x3F, 6),
    locationName.HONEYCGM3: LocationData(1230708, 0x3F, 7),
    locationName.CHEATOGM1: LocationData(1230731, 0x56, 6),
    locationName.CHEATOGM2: LocationData(1230732, 0x56, 7),
    locationName.CHEATOGM3: LocationData(1230733, 0x57, 0),
}

WWLoc_table = {
    locationName.JINJOWW1: LocationData(1230561, 0x3A, 6),
    locationName.JINJOWW2: LocationData(1230562, 0x3A, 7),
    locationName.JINJOWW3: LocationData(1230563, 0x3B, 0),
    locationName.JINJOWW4: LocationData(1230564, 0x3B, 1),
    locationName.JINJOWW5: LocationData(1230565, 0x3B, 2),
    locationName.JIGGYWW1:  LocationData(1230616, 0x47, 4),
    locationName.JIGGYWW2:  LocationData(1230617, 0x47, 5),
    locationName.JIGGYWW3:  LocationData(1230618, 0x47, 6),
    locationName.JIGGYWW4:  LocationData(1230619, 0x47, 7),
    locationName.JIGGYWW5:  LocationData(1230620, 0x48, 0),
    locationName.JIGGYWW6:  LocationData(1230621, 0x48, 1),
    locationName.JIGGYWW7:  LocationData(1230622, 0x48, 2),
    locationName.JIGGYWW8:  LocationData(1230623, 0x48, 3),
    locationName.JIGGYWW9:  LocationData(1230624, 0x48, 4),
    locationName.JIGGYWW10: LocationData(1230625, 0x48, 5),
    locationName.GLOWBOWW1: LocationData(1230690, 0x43, 3),
    locationName.GLOWBOWW2: LocationData(1230691, 0x43, 4),
    locationName.HONEYCWW1: LocationData(1230709, 0x40, 0),
    locationName.HONEYCWW2: LocationData(1230710, 0x40, 1),
    locationName.HONEYCWW3: LocationData(1230711, 0x40, 2),
    locationName.CHEATOWW1: LocationData(1230734, 0x57, 1),
    locationName.CHEATOWW2: LocationData(1230735, 0x57, 2),
    locationName.CHEATOWW3: LocationData(1230736, 0x57, 3)
}

JRLoc_table = {
    locationName.JRLDB1: LocationData(1230521, 0x22, 7),
    locationName.JRLDB2: LocationData(1230522, 0x23, 0),
    locationName.JRLDB3: LocationData(1230523, 0x23, 1),
    locationName.JRLDB4: LocationData(1230524, 0x23, 2),
    locationName.JRLDB5: LocationData(1230525, 0x23, 3),
    locationName.JRLDB6: LocationData(1230526, 0x23, 4),
    locationName.JRLDB7: LocationData(1230527, 0x23, 5),
    locationName.JRLDB8: LocationData(1230528, 0x23, 6),
    locationName.JRLDB9: LocationData(1230529, 0x23, 7),
    locationName.JRLDB10: LocationData(1230530, 0x24, 0),
    locationName.JRLDB11: LocationData(1230531, 0x24, 1),
    locationName.JRLDB12: LocationData(1230532, 0x24, 2),
    locationName.JRLDB13: LocationData(1230533, 0x24, 3),
    locationName.JRLDB14: LocationData(1230534, 0x24, 4),
    locationName.JRLDB15: LocationData(1230535, 0x24, 5),
    locationName.JRLDB16: LocationData(1230536, 0x24, 6),
    locationName.JRLDB17: LocationData(1230537, 0x24, 7),
    locationName.JRLDB18: LocationData(1230538, 0x25, 0),
    locationName.JRLDB19: LocationData(1230539, 0x25, 1),
    locationName.JRLDB20: LocationData(1230540, 0x25, 2),
    locationName.JRLDB21: LocationData(1230541, 0x25, 3),
    locationName.JRLDB22: LocationData(1230542, 0x25, 4),
    locationName.JRLDB23: LocationData(1230543, 0x25, 5),
    locationName.JRLDB24: LocationData(1230544, 0x25, 6),
    locationName.JRLDB25: LocationData(1230545, 0x25, 7),
    locationName.JRLDB26: LocationData(1230546, 0x26, 0),
    locationName.JRLDB27: LocationData(1230547, 0x26, 1),
    locationName.JRLDB28: LocationData(1230548, 0x26, 2),
    locationName.JRLDB29: LocationData(1230549, 0x26, 3),
    locationName.JRLDB30: LocationData(1230550, 0x26, 4),
    locationName.JINJOJR1:  LocationData(1230566, 0x3B, 3),
    locationName.JINJOJR2:  LocationData(1230567, 0x3B, 4),
    locationName.JINJOJR3:  LocationData(1230568, 0x3B, 5),
    locationName.JINJOJR4:  LocationData(1230569, 0x3B, 6),
    locationName.JINJOJR5:  LocationData(1230570, 0x3B, 7),
    locationName.JIGGYJR1:  LocationData(1230626, 0x48, 6),
    locationName.JIGGYJR2:  LocationData(1230627, 0x48, 7),
    locationName.JIGGYJR3:  LocationData(1230628, 0x49, 0),
    locationName.JIGGYJR4:  LocationData(1230629, 0x49, 1),
    locationName.JIGGYJR5:  LocationData(1230630, 0x49, 2),
    locationName.JIGGYJR6:  LocationData(1230631, 0x49, 3),
    locationName.JIGGYJR7:  LocationData(1230632, 0x49, 4),
    locationName.JIGGYJR8:  LocationData(1230633, 0x49, 5),
    locationName.JIGGYJR9:  LocationData(1230634, 0x49, 6),
    locationName.JIGGYJR10: LocationData(1230635, 0x49, 7),
    locationName.GLOWBOJR1: LocationData(1230692, 0x43, 5),
    locationName.GLOWBOJR2: LocationData(1230693, 0x43, 6),
    locationName.HONEYCJR1: LocationData(1230712, 0x40, 3),
    locationName.HONEYCJR2: LocationData(1230713, 0x40, 4),
    locationName.HONEYCJR3: LocationData(1230714, 0x40, 5),
    locationName.CHEATOJR1: LocationData(1230737, 0x57, 4),
    locationName.CHEATOJR2: LocationData(1230738, 0x57, 5),
    locationName.CHEATOJR3: LocationData(1230739, 0x57, 6)
}

TLLoc_table = {
    locationName.JINJOTL1:  LocationData(1230571, 0x3C, 0),
    locationName.JINJOTL2:  LocationData(1230572, 0x3C, 1),
    locationName.JINJOTL3:  LocationData(1230573, 0x3C, 2),
    locationName.JINJOTL4:  LocationData(1230574, 0x3C, 3),
    locationName.JINJOTL5:  LocationData(1230575, 0x3C, 4),
    locationName.JIGGYTD1:  LocationData(1230636, 0x4A, 0),
    locationName.JIGGYTD2:  LocationData(1230637, 0x4A, 1),
    locationName.JIGGYTD3:  LocationData(1230638, 0x4A, 2),
    locationName.JIGGYTD4:  LocationData(1230639, 0x4A, 3),
    locationName.JIGGYTD5:  LocationData(1230640, 0x4A, 4),
    locationName.JIGGYTD6:  LocationData(1230641, 0x4A, 5),
    locationName.JIGGYTD7:  LocationData(1230642, 0x4A, 6),
    locationName.JIGGYTD8:  LocationData(1230643, 0x4A, 7),
    locationName.JIGGYTD9:  LocationData(1230644, 0x4B, 0),
    locationName.JIGGYTD10: LocationData(1230645, 0x4B, 1),
    locationName.GLOWBOTL1: LocationData(1230694, 0x43, 7),
    locationName.GLOWBOTL2: LocationData(1230695, 0x44, 0),
    locationName.HONEYCTL1: LocationData(1230715, 0x40, 6),
    locationName.HONEYCTL2: LocationData(1230716, 0x40, 7),
    locationName.HONEYCTL3: LocationData(1230717, 0x41, 0),
    locationName.CHEATOTL1: LocationData(1230740, 0x57, 7),
    locationName.CHEATOTL2: LocationData(1230741, 0x58, 0),
    locationName.CHEATOTL3: LocationData(1230742, 0x58, 1)
}

GILoc_table = {
    locationName.JINJOGI1:  LocationData(1230576, 0x3C, 5),
    locationName.JINJOGI2:  LocationData(1230577, 0x3C, 6),
    locationName.JINJOGI3:  LocationData(1230578, 0x3C, 7),
    locationName.JINJOGI4:  LocationData(1230579, 0x3D, 0),
    locationName.JINJOGI5:  LocationData(1230580, 0x3D, 1),
    locationName.JIGGYGI1:  LocationData(1230646, 0x4B, 2),
    locationName.JIGGYGI2:  LocationData(1230647, 0x4B, 3),
    locationName.JIGGYGI3:  LocationData(1230648, 0x4B, 4),
    locationName.JIGGYGI4:  LocationData(1230649, 0x4B, 5),
    locationName.JIGGYGI5:  LocationData(1230650, 0x4B, 6),
    locationName.JIGGYGI6:  LocationData(1230651, 0x4B, 7),
    locationName.JIGGYGI7:  LocationData(1230652, 0x4C, 0),
    locationName.JIGGYGI8:  LocationData(1230653, 0x4C, 1),
    locationName.JIGGYGI9:  LocationData(1230654, 0x4C, 2),
    locationName.JIGGYGI10: LocationData(1230655, 0x4C, 3),
    locationName.GLOWBOGI1: LocationData(1230696, 0x44, 1),
    locationName.GLOWBOGI2: LocationData(1230697, 0x44, 2),
    locationName.HONEYCGI1: LocationData(1230718, 0x41, 1),
    locationName.HONEYCGI2: LocationData(1230719, 0x41, 2),
    locationName.HONEYCGI3: LocationData(1230720, 0x41, 3),
    locationName.CHEATOGI1: LocationData(1230743, 0x58, 2),
    locationName.CHEATOGI2: LocationData(1230744, 0x58, 3),
    locationName.CHEATOGI3: LocationData(1230745, 0x58, 4)
}

HPLoc_table = {
    locationName.JINJOHP1:  LocationData(1230581, 0x3D, 2),
    locationName.JINJOHP2:  LocationData(1230582, 0x3D, 3),
    locationName.JINJOHP3:  LocationData(1230583, 0x3D, 4),
    locationName.JINJOHP4:  LocationData(1230584, 0x3D, 5),
    locationName.JINJOHP5:  LocationData(1230585, 0x3D, 6),
    locationName.JIGGYHP1:  LocationData(1230656, 0x4C, 4),
    locationName.JIGGYHP2:  LocationData(1230657, 0x4C, 5),
    locationName.JIGGYHP3:  LocationData(1230658, 0x4C, 6),
    locationName.JIGGYHP4:  LocationData(1230659, 0x4C, 7),
    locationName.JIGGYHP5:  LocationData(1230660, 0x4D, 0),
    locationName.JIGGYHP6:  LocationData(1230661, 0x4D, 1),
    locationName.JIGGYHP7:  LocationData(1230662, 0x4D, 2),
    locationName.JIGGYHP8:  LocationData(1230663, 0x4D, 3),
    locationName.JIGGYHP9:  LocationData(1230664, 0x4D, 4),
    locationName.JIGGYHP10: LocationData(1230665, 0x4D, 5),
    locationName.GLOWBOHP1: LocationData(1230698, 0x44, 3),
    locationName.GLOWBOHP2: LocationData(1230699, 0x44, 4),
    locationName.HONEYCHP1: LocationData(1230721, 0x41, 4),
    locationName.HONEYCHP2: LocationData(1230722, 0x41, 5),
    locationName.HONEYCHP3: LocationData(1230723, 0x41, 6),
    locationName.CHEATOHP1: LocationData(1230746, 0x58, 5),
    locationName.CHEATOHP2: LocationData(1230747, 0x58, 6),
    locationName.CHEATOHP3: LocationData(1230748, 0x58, 7)
}

CCLoc_table = {
    locationName.JINJOCC1:  LocationData(1230586, 0x3D, 7),
    locationName.JINJOCC2:  LocationData(1230587, 0x3E, 0),
    locationName.JINJOCC3:  LocationData(1230588, 0x3E, 1),
    locationName.JINJOCC4:  LocationData(1230589, 0x3E, 2),
    locationName.JINJOCC5:  LocationData(1230590, 0x3E, 3),
    locationName.JIGGYCC1:  LocationData(1230666, 0x4D, 6),
    locationName.JIGGYCC2:  LocationData(1230667, 0x4D, 7),
    locationName.JIGGYCC3:  LocationData(1230668, 0x4E, 0),
    locationName.JIGGYCC4:  LocationData(1230669, 0x4E, 1),
    locationName.JIGGYCC5:  LocationData(1230670, 0x4E, 2),
    locationName.JIGGYCC6:  LocationData(1230671, 0x4E, 3),
    locationName.JIGGYCC7:  LocationData(1230672, 0x4E, 4),
    locationName.JIGGYCC8:  LocationData(1230673, 0x4E, 5),
    locationName.JIGGYCC9:  LocationData(1230674, 0x4E, 6),
    locationName.JIGGYCC10: LocationData(1230675, 0x4E, 7),
    locationName.GLOWBOCC1: LocationData(1230700, 0x44, 5),
    locationName.GLOWBOCC2: LocationData(1230701, 0x44, 6),
    locationName.HONEYCCC1: LocationData(1230724, 0x41, 7),
    locationName.HONEYCCC2: LocationData(1230725, 0x42, 0),
    locationName.HONEYCCC3: LocationData(1230726, 0x42, 1),
    locationName.CHEATOCC1: LocationData(1230749, 0x59, 0),
    locationName.CHEATOCC2: LocationData(1230750, 0x59, 1),
    locationName.CHEATOCC3: LocationData(1230751, 0x59, 2)
}

IHWHLoc_table = {
    locationName.JINJOIH1: LocationData(1230591, 0x3E, 4)
}

IHWLLoc_table = {
    locationName.JINJOIH2: LocationData(1230592, 0x3E, 5)
}

IHCTLoc_table = {
    locationName.JINJOIH3: LocationData(1230593, 0x3E, 6),
    locationName.GLOWBOIH1: LocationData(1230702, 0x44, 7)

}

boss_table = {
    locationName.HAG1:      LocationData(1230027, 0x03, 3)
}


all_location_table = {
    **SMLoc_table,
    **JVLoc_table,
    **IHWHLoc_table,
    **MTLoc_Table,
    **IHPLLoc_table,
    **GMLoc_table,
    **WWLoc_table,
    **IHCTLoc_table,
    **JRLoc_table,
    **IHWLLoc_table,
    **TLLoc_table,
    **GILoc_table,
    **HPLoc_table,
    **CCLoc_table,
    **boss_table
}

