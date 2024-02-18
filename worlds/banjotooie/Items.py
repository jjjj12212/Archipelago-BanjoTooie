from BaseClasses import Item
import typing
from .Names import itemName


class BanjoTooieItem(Item):
    game: str = "Banjo Tooie"
class ItemData(typing.NamedTuple):
    btid: int = 0
    qty: int = 0
    type: str = ""



jinjo_table = {
    itemName.WJINJO:        ItemData(1230501, 1, "progress"),
    itemName.OJINJO:        ItemData(1230502, 2, "progress"),
    itemName.YJINJO:        ItemData(1230503, 3, "progress"),
    itemName.BRJINJO:       ItemData(1230504, 4, "progress"),
    itemName.GJINJO:        ItemData(1230505, 5, "progress"),
    itemName.RJINJO:        ItemData(1230506, 6, "progress"),
    itemName.BLJINJO:       ItemData(1230507, 7, "progress"),
    itemName.PJINJO:        ItemData(1230508, 8, "progress"),
    itemName.BKJINJO:       ItemData(1230509, 9, "progress")
}

jiggy_table = {
    itemName.JIGGYIH1:  ItemData(1230676, 1, "progress"),
    itemName.JIGGYIH2:  ItemData(1230677, 1, "progress"),
    itemName.JIGGYIH3:  ItemData(1230678, 1, "progress"),
    itemName.JIGGYIH4:  ItemData(1230679, 1, "progress"),
    itemName.JIGGYIH5:  ItemData(1230680, 1, "progress"),
    itemName.JIGGYIH6:  ItemData(1230681, 1, "progress"),
    itemName.JIGGYIH7:  ItemData(1230682, 1, "progress"),
    itemName.JIGGYIH8:  ItemData(1230683, 1, "progress"),
    itemName.JIGGYIH9:  ItemData(1230684, 1, "progress"),
    itemName.JIGGYIH10: ItemData(1230685, 1, "progress"),
    itemName.JIGGYMT1:  ItemData(1230596, 1, "progress"),
    itemName.JIGGYMT2:  ItemData(1230597, 1, "progress"),
    itemName.JIGGYMT3:  ItemData(1230598, 1, "progress"),
    itemName.JIGGYMT4:  ItemData(1230599, 1, "progress"),
    itemName.JIGGYMT5:  ItemData(1230600, 1, "progress"),
    itemName.JIGGYMT6:  ItemData(1230601, 1, "progress"),
    itemName.JIGGYMT7:  ItemData(1230602, 1, "progress"),
    itemName.JIGGYMT8:  ItemData(1230603, 1, "progress"),
    itemName.JIGGYMT9:  ItemData(1230604, 1, "progress"),
    itemName.JIGGYMT10: ItemData(1230605, 1, "progress"),
    itemName.JIGGYGM1:  ItemData(1230606, 1, "progress"),
    itemName.JIGGYGM2:  ItemData(1230607, 1, "progress"),
    itemName.JIGGYGM3:  ItemData(1230608, 1, "progress"),
    itemName.JIGGYGM4:  ItemData(1230609, 1, "progress"),
    itemName.JIGGYGM5:  ItemData(1230610, 1, "progress"),
    itemName.JIGGYGM6:  ItemData(1230611, 1, "progress"),
    itemName.JIGGYGM7:  ItemData(1230612, 1, "progress"),
    itemName.JIGGYGM8:  ItemData(1230613, 1, "progress"),
    itemName.JIGGYGM9:  ItemData(1230614, 1, "progress"),
    itemName.JIGGYGM10: ItemData(1230615, 1, "progress"),
    itemName.JIGGYWW1:  ItemData(1230616, 1, "progress"),
    itemName.JIGGYWW2:  ItemData(1230617, 1, "progress"),
    itemName.JIGGYWW3:  ItemData(1230618, 1, "progress"),
    itemName.JIGGYWW4:  ItemData(1230619, 1, "progress"),
    itemName.JIGGYWW5:  ItemData(1230620, 1, "progress"),
    itemName.JIGGYWW6:  ItemData(1230621, 1, "progress"),
    itemName.JIGGYWW7:  ItemData(1230622, 1, "progress"),
    itemName.JIGGYWW8:  ItemData(1230623, 1, "progress"),
    itemName.JIGGYWW9:  ItemData(1230624, 1, "progress"),
    itemName.JIGGYWW10: ItemData(1230625, 1, "progress"),
    itemName.JIGGYJR1:  ItemData(1230626, 1, "progress"),
    itemName.JIGGYJR2:  ItemData(1230627, 1, "progress"),
    itemName.JIGGYJR3:  ItemData(1230628, 1, "progress"),
    itemName.JIGGYJR4:  ItemData(1230629, 1, "progress"),
    itemName.JIGGYJR5:  ItemData(1230630, 1, "progress"),
    itemName.JIGGYJR6:  ItemData(1230631, 1, "progress"),
    itemName.JIGGYJR7:  ItemData(1230632, 1, "progress"),
    itemName.JIGGYJR8:  ItemData(1230633, 1, "progress"),
    itemName.JIGGYJR9:  ItemData(1230634, 1, "progress"),
    itemName.JIGGYJR10: ItemData(1230635, 1, "progress"),
    itemName.JIGGYTD1:  ItemData(1230636, 1, "progress"),
    itemName.JIGGYTD2:  ItemData(1230637, 1, "progress"),
    itemName.JIGGYTD3:  ItemData(1230638, 1, "progress"),
    itemName.JIGGYTD4:  ItemData(1230639, 1, "progress"),
    itemName.JIGGYTD5:  ItemData(1230640, 1, "progress"),
    itemName.JIGGYTD6:  ItemData(1230641, 1, "progress"),
    itemName.JIGGYTD7:  ItemData(1230642, 1, "progress"),
    itemName.JIGGYTD8:  ItemData(1230643, 1, "progress"),
    itemName.JIGGYTD9:  ItemData(1230644, 1, "progress"),
    itemName.JIGGYTD10: ItemData(1230645, 1, "progress"),
    itemName.JIGGYGI1:  ItemData(1230646, 1, "progress"),
    itemName.JIGGYGI2:  ItemData(1230647, 1, "progress"),
    itemName.JIGGYGI3:  ItemData(1230648, 1, "progress"),
    itemName.JIGGYGI4:  ItemData(1230649, 1, "progress"),
    itemName.JIGGYGI5:  ItemData(1230650, 1, "progress"),
    itemName.JIGGYGI6:  ItemData(1230651, 1, "progress"),
    itemName.JIGGYGI7:  ItemData(1230652, 1, "progress"),
    itemName.JIGGYGI8:  ItemData(1230653, 1, "progress"),
    itemName.JIGGYGI9:  ItemData(1230654, 1, "progress"),
    itemName.JIGGYGI10: ItemData(1230655, 1, "progress"),
    itemName.JIGGYHP1:  ItemData(1230656, 1, "progress"),
    itemName.JIGGYHP2:  ItemData(1230657, 1, "progress"),
    itemName.JIGGYHP3:  ItemData(1230658, 1, "progress"),
    itemName.JIGGYHP4:  ItemData(1230659, 1, "progress"),
    itemName.JIGGYHP5:  ItemData(1230660, 1, "progress"),
    itemName.JIGGYHP6:  ItemData(1230661, 1, "progress"),
    itemName.JIGGYHP7:  ItemData(1230662, 1, "progress"),
    itemName.JIGGYHP8:  ItemData(1230663, 1, "progress"),
    itemName.JIGGYHP9:  ItemData(1230664, 1, "progress"),
    itemName.JIGGYHP10: ItemData(1230665, 1, "progress"),
    itemName.JIGGYCC1:  ItemData(1230666, 1, "progress"),
    itemName.JIGGYCC2:  ItemData(1230667, 1, "progress"),
    itemName.JIGGYCC3:  ItemData(1230668, 1, "progress"),
    itemName.JIGGYCC4:  ItemData(1230669, 1, "progress"),
    itemName.JIGGYCC5:  ItemData(1230670, 1, "progress"),
    itemName.JIGGYCC6:  ItemData(1230671, 1, "progress"),
    itemName.JIGGYCC7:  ItemData(1230672, 1, "progress"),
    itemName.JIGGYCC8:  ItemData(1230673, 1, "progress"),
    itemName.JIGGYCC9:  ItemData(1230674, 1, "progress"),
    itemName.JIGGYCC10: ItemData(1230675, 1, "progress"),
}

honeycomb_table = {
    itemName.HONEYCMT1:     ItemData(1230703, 1, "useful"),
    itemName.HONEYCMT2:     ItemData(1230704, 1, "useful"),
    itemName.HONEYCMT3:     ItemData(1230705, 1, "useful"),
    itemName.HONEYCGM1:     ItemData(1230706, 1, "useful"),
    itemName.HONEYCGM2:     ItemData(1230707, 1, "useful"),
    itemName.HONEYCGM3:     ItemData(1230708, 1, "useful"),
    itemName.HONEYCWW1:     ItemData(1230709, 1, "useful"),
    itemName.HONEYCWW2:     ItemData(1230710, 1, "useful"),
    itemName.HONEYCWW3:     ItemData(1230711, 1, "useful"),
    itemName.HONEYCJR1:     ItemData(1230712, 1, "useful"),
    itemName.HONEYCJR2:     ItemData(1230713, 1, "useful"),
    itemName.HONEYCJR3:     ItemData(1230714, 1, "useful"),
    itemName.HONEYCTL1:     ItemData(1230715, 1, "useful"),
    itemName.HONEYCTL2:     ItemData(1230716, 1, "useful"),
    itemName.HONEYCTL3:     ItemData(1230717, 1, "useful"),
    itemName.HONEYCGI1:     ItemData(1230718, 1, "useful"),
    itemName.HONEYCGI2:     ItemData(1230719, 1, "useful"),
    itemName.HONEYCGI3:     ItemData(1230720, 1, "useful"),
    itemName.HONEYCHP1:     ItemData(1230721, 1, "useful"),
    itemName.HONEYCHP2:     ItemData(1230722, 1, "useful"),
    itemName.HONEYCHP3:     ItemData(1230723, 1, "useful"),
    itemName.HONEYCCC1:     ItemData(1230724, 1, "useful"),
    itemName.HONEYCCC2:     ItemData(1230725, 1, "useful"),
    itemName.HONEYCCC3:     ItemData(1230726, 1, "useful"),
    itemName.HONEYCIH1:     ItemData(1230727, 1, "useful"),
}

level_progress_table = {
    itemName.GLOWBO:        ItemData(1230511, 17, "progress"),
}

misc_collectable_table = {
    itemName.PAGES:         ItemData(1230513, 25, "useful"),
    itemName.DOUBLOON:      ItemData(1230514, 30, "useful")
}



all_item_table = {
    **jinjo_table,
    **level_progress_table,
    **misc_collectable_table,
    **jiggy_table,
    **honeycomb_table
}

all_group_table = {
    'jiggy' : jiggy_table,
    'honeycombs' : honeycomb_table,
    'jinjo' : jinjo_table,
    'misc' : misc_collectable_table
}



