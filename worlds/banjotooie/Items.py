from BaseClasses import Item
import typing
from .Names import itemName, locationName


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
    locationName.JIGGYIH1:  ItemData(1230676, 1, "progress"),
    locationName.JIGGYIH2:  ItemData(1230677, 1, "progress"),
    locationName.JIGGYIH3:  ItemData(1230678, 1, "progress"),
    locationName.JIGGYIH4:  ItemData(1230679, 1, "progress"),
    locationName.JIGGYIH5:  ItemData(1230680, 1, "progress"),
    locationName.JIGGYIH6:  ItemData(1230681, 1, "progress"),
    locationName.JIGGYIH7:  ItemData(1230682, 1, "progress"),
    locationName.JIGGYIH8:  ItemData(1230683, 1, "progress"),
    locationName.JIGGYIH9:  ItemData(1230684, 1, "progress"),
    locationName.JIGGYIH10: ItemData(1230685, 1, "progress"),
    locationName.JIGGYMT1:  ItemData(1230596, 1, "progress"),
    locationName.JIGGYMT2:  ItemData(1230597, 1, "progress"),
    locationName.JIGGYMT3:  ItemData(1230598, 1, "progress"),
    locationName.JIGGYMT4:  ItemData(1230599, 1, "progress"),
    locationName.JIGGYMT5:  ItemData(1230600, 1, "progress"),
    locationName.JIGGYMT6:  ItemData(1230601, 1, "progress"),
    locationName.JIGGYMT7:  ItemData(1230602, 1, "progress"),
    locationName.JIGGYMT8:  ItemData(1230603, 1, "progress"),
    locationName.JIGGYMT9:  ItemData(1230604, 1, "progress"),
    locationName.JIGGYMT10: ItemData(1230605, 1, "progress"),
    locationName.JIGGYGM1:  ItemData(1230606, 1, "progress"),
    locationName.JIGGYGM2:  ItemData(1230607, 1, "progress"),
    locationName.JIGGYGM3:  ItemData(1230608, 1, "progress"),
    locationName.JIGGYGM4:  ItemData(1230609, 1, "progress"),
    locationName.JIGGYGM5:  ItemData(1230610, 1, "progress"),
    locationName.JIGGYGM6:  ItemData(1230611, 1, "progress"),
    locationName.JIGGYGM7:  ItemData(1230612, 1, "progress"),
    locationName.JIGGYGM8:  ItemData(1230613, 1, "progress"),
    locationName.JIGGYGM9:  ItemData(1230614, 1, "progress"),
    locationName.JIGGYGM10: ItemData(1230615, 1, "progress"),
    locationName.JIGGYWW1:  ItemData(1230616, 1, "progress"),
    locationName.JIGGYWW2:  ItemData(1230617, 1, "progress"),
    locationName.JIGGYWW3:  ItemData(1230618, 1, "progress"),
    locationName.JIGGYWW4:  ItemData(1230619, 1, "progress"),
    locationName.JIGGYWW5:  ItemData(1230620, 1, "progress"),
    locationName.JIGGYWW6:  ItemData(1230621, 1, "progress"),
    locationName.JIGGYWW7:  ItemData(1230622, 1, "progress"),
    locationName.JIGGYWW8:  ItemData(1230623, 1, "progress"),
    locationName.JIGGYWW9:  ItemData(1230624, 1, "progress"),
    locationName.JIGGYWW10: ItemData(1230625, 1, "progress"),
    locationName.JIGGYJR1:  ItemData(1230626, 1, "progress"),
    locationName.JIGGYJR2:  ItemData(1230627, 1, "progress"),
    locationName.JIGGYJR3:  ItemData(1230628, 1, "progress"),
    locationName.JIGGYJR4:  ItemData(1230629, 1, "progress"),
    locationName.JIGGYJR5:  ItemData(1230630, 1, "progress"),
    locationName.JIGGYJR6:  ItemData(1230631, 1, "progress"),
    locationName.JIGGYJR7:  ItemData(1230632, 1, "progress"),
    locationName.JIGGYJR8:  ItemData(1230633, 1, "progress"),
    locationName.JIGGYJR9:  ItemData(1230634, 1, "progress"),
    locationName.JIGGYJR10: ItemData(1230635, 1, "progress"),
    locationName.JIGGYTD1:  ItemData(1230636, 1, "progress"),
    locationName.JIGGYTD2:  ItemData(1230637, 1, "progress"),
    locationName.JIGGYTD3:  ItemData(1230638, 1, "progress"),
    locationName.JIGGYTD4:  ItemData(1230639, 1, "progress"),
    locationName.JIGGYTD5:  ItemData(1230640, 1, "progress"),
    locationName.JIGGYTD6:  ItemData(1230641, 1, "progress"),
    locationName.JIGGYTD7:  ItemData(1230642, 1, "progress"),
    locationName.JIGGYTD8:  ItemData(1230643, 1, "progress"),
    locationName.JIGGYTD9:  ItemData(1230644, 1, "progress"),
    locationName.JIGGYTD10: ItemData(1230645, 1, "progress"),
    locationName.JIGGYGI1:  ItemData(1230646, 1, "progress"),
    locationName.JIGGYGI2:  ItemData(1230647, 1, "progress"),
    locationName.JIGGYGI3:  ItemData(1230648, 1, "progress"),
    locationName.JIGGYGI4:  ItemData(1230649, 1, "progress"),
    locationName.JIGGYGI5:  ItemData(1230650, 1, "progress"),
    locationName.JIGGYGI6:  ItemData(1230651, 1, "progress"),
    locationName.JIGGYGI7:  ItemData(1230652, 1, "progress"),
    locationName.JIGGYGI8:  ItemData(1230653, 1, "progress"),
    locationName.JIGGYGI9:  ItemData(1230654, 1, "progress"),
    locationName.JIGGYGI10: ItemData(1230655, 1, "progress"),
    locationName.JIGGYHP1:  ItemData(1230656, 1, "progress"),
    locationName.JIGGYHP2:  ItemData(1230657, 1, "progress"),
    locationName.JIGGYHP3:  ItemData(1230658, 1, "progress"),
    locationName.JIGGYHP4:  ItemData(1230659, 1, "progress"),
    locationName.JIGGYHP5:  ItemData(1230660, 1, "progress"),
    locationName.JIGGYHP6:  ItemData(1230661, 1, "progress"),
    locationName.JIGGYHP7:  ItemData(1230662, 1, "progress"),
    locationName.JIGGYHP8:  ItemData(1230663, 1, "progress"),
    locationName.JIGGYHP9:  ItemData(1230664, 1, "progress"),
    locationName.JIGGYHP10: ItemData(1230665, 1, "progress"),
    locationName.JIGGYCC1:  ItemData(1230666, 1, "progress"),
    locationName.JIGGYCC2:  ItemData(1230667, 1, "progress"),
    locationName.JIGGYCC3:  ItemData(1230668, 1, "progress"),
    locationName.JIGGYCC4:  ItemData(1230669, 1, "progress"),
    locationName.JIGGYCC5:  ItemData(1230670, 1, "progress"),
    locationName.JIGGYCC6:  ItemData(1230671, 1, "progress"),
    locationName.JIGGYCC7:  ItemData(1230672, 1, "progress"),
    locationName.JIGGYCC8:  ItemData(1230673, 1, "progress"),
    locationName.JIGGYCC9:  ItemData(1230674, 1, "progress"),
    locationName.JIGGYCC10: ItemData(1230675, 1, "progress"),
}

level_progress_table = {
    itemName.GLOWBO:        ItemData(1230511, 17, "progress"),
}

misc_collectable_table = {
    itemName.HONEY:         ItemData(1230512, 25, "useful"),
    itemName.PAGES:         ItemData(1230513, 25, "useful"),
    itemName.DOUBLOON:      ItemData(1230514, 30, "useful")
}



all_item_table = {
    **jinjo_table,
    **level_progress_table,
    **misc_collectable_table,
    **jiggy_table
}

all_group_table = {
    'jiggy' : jiggy_table,
    'jinjo' : jinjo_table,
    'misc' : misc_collectable_table
}



