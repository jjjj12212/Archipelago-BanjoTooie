from BaseClasses import Item
import typing
from .Names import itemName
from .Names import locationName


class BanjoTooieItem(Item):
    game: str = "Banjo Tooie"
class ItemData(typing.NamedTuple):
    btid: int = 0
    qty: int = 0
    type: str = ""
    defualt_location: None | str = "" 



jinjo_table = {
    itemName.WJINJO:        ItemData(1230501, 1, "progress", None),
    itemName.OJINJO:        ItemData(1230502, 2, "progress", None),
    itemName.YJINJO:        ItemData(1230503, 3, "progress", None),
    itemName.BRJINJO:       ItemData(1230504, 4, "progress", None),
    itemName.GJINJO:        ItemData(1230505, 5, "progress", None),
    itemName.RJINJO:        ItemData(1230506, 6, "progress", None),
    itemName.BLJINJO:       ItemData(1230507, 7, "progress", None),
    itemName.PJINJO:        ItemData(1230508, 8, "progress", None),
    itemName.BKJINJO:       ItemData(1230509, 9, "progress", None)
}

jiggy_table = {
    itemName.JIGGYIH1:  ItemData(1230676, 1, "filler", None),
    itemName.JIGGYIH2:  ItemData(1230677, 1, "filler", None),
    itemName.JIGGYIH3:  ItemData(1230678, 1, "filler", None),
    itemName.JIGGYIH4:  ItemData(1230679, 1, "filler", None),
    itemName.JIGGYIH5:  ItemData(1230680, 1, "filler", None),
    itemName.JIGGYIH6:  ItemData(1230681, 1, "filler", None),
    itemName.JIGGYIH7:  ItemData(1230682, 1, "filler", None),
    itemName.JIGGYIH8:  ItemData(1230683, 1, "filler", None),
    itemName.JIGGYIH9:  ItemData(1230684, 1, "filler", None),
    itemName.JIGGYIH10: ItemData(1230685, 1, "progress", None),
    itemName.JIGGYMT1:  ItemData(1230596, 1, "progress", None),
    itemName.JIGGYMT2:  ItemData(1230597, 1, "progress", None),
    itemName.JIGGYMT3:  ItemData(1230598, 1, "progress", None),
    itemName.JIGGYMT4:  ItemData(1230599, 1, "progress", None),
    itemName.JIGGYMT5:  ItemData(1230600, 1, "progress", None),
    itemName.JIGGYMT6:  ItemData(1230601, 1, "progress", None),
    itemName.JIGGYMT7:  ItemData(1230602, 1, "progress", None),
    itemName.JIGGYMT8:  ItemData(1230603, 1, "progress", None),
    itemName.JIGGYMT9:  ItemData(1230604, 1, "progress", None),
    itemName.JIGGYMT10: ItemData(1230605, 1, "progress", None),
    itemName.JIGGYGM1:  ItemData(1230606, 1, "progress", None),
    itemName.JIGGYGM2:  ItemData(1230607, 1, "progress", None),
    itemName.JIGGYGM3:  ItemData(1230608, 1, "progress", None),
    itemName.JIGGYGM4:  ItemData(1230609, 1, "progress", None),
    itemName.JIGGYGM5:  ItemData(1230610, 1, "progress", None),
    itemName.JIGGYGM6:  ItemData(1230611, 1, "progress", None),
    itemName.JIGGYGM7:  ItemData(1230612, 1, "progress", None),
    itemName.JIGGYGM8:  ItemData(1230613, 1, "progress", None),
    itemName.JIGGYGM9:  ItemData(1230614, 1, "progress", None),
    itemName.JIGGYGM10: ItemData(1230615, 1, "progress", None),
    itemName.JIGGYWW1:  ItemData(1230616, 1, "progress", None),
    itemName.JIGGYWW2:  ItemData(1230617, 1, "progress", None),
    itemName.JIGGYWW3:  ItemData(1230618, 1, "progress", None),
    itemName.JIGGYWW4:  ItemData(1230619, 1, "progress", None),
    itemName.JIGGYWW5:  ItemData(1230620, 1, "progress", None),
    itemName.JIGGYWW6:  ItemData(1230621, 1, "progress", None),
    itemName.JIGGYWW7:  ItemData(1230622, 1, "progress", None),
    itemName.JIGGYWW8:  ItemData(1230623, 1, "progress", None),
    itemName.JIGGYWW9:  ItemData(1230624, 1, "progress", None),
    itemName.JIGGYWW10: ItemData(1230625, 1, "progress", None),
    itemName.JIGGYJR1:  ItemData(1230626, 1, "progress", None),
    itemName.JIGGYJR2:  ItemData(1230627, 1, "progress", None),
    itemName.JIGGYJR3:  ItemData(1230628, 1, "progress", None),
    itemName.JIGGYJR4:  ItemData(1230629, 1, "progress", None),
    itemName.JIGGYJR5:  ItemData(1230630, 1, "progress", None),
    itemName.JIGGYJR6:  ItemData(1230631, 1, "progress", None),
    itemName.JIGGYJR7:  ItemData(1230632, 1, "progress", None),
    itemName.JIGGYJR8:  ItemData(1230633, 1, "progress", None),
    itemName.JIGGYJR9:  ItemData(1230634, 1, "progress", None),
    itemName.JIGGYJR10: ItemData(1230635, 1, "progress", None),
    itemName.JIGGYTD1:  ItemData(1230636, 1, "progress", None),
    itemName.JIGGYTD2:  ItemData(1230637, 1, "progress", None),
    itemName.JIGGYTD3:  ItemData(1230638, 1, "progress", None),
    itemName.JIGGYTD4:  ItemData(1230639, 1, "progress", None),
    itemName.JIGGYTD5:  ItemData(1230640, 1, "progress", None),
    itemName.JIGGYTD6:  ItemData(1230641, 1, "progress", None),
    itemName.JIGGYTD7:  ItemData(1230642, 1, "progress", None),
    itemName.JIGGYTD8:  ItemData(1230643, 1, "progress", None),
    itemName.JIGGYTD9:  ItemData(1230644, 1, "progress", None),
    itemName.JIGGYTD10: ItemData(1230645, 1, "progress", None),
    itemName.JIGGYGI1:  ItemData(1230646, 1, "progress", None),
    itemName.JIGGYGI2:  ItemData(1230647, 1, "progress", None),
    itemName.JIGGYGI3:  ItemData(1230648, 1, "progress", None),
    itemName.JIGGYGI4:  ItemData(1230649, 1, "progress", None),
    itemName.JIGGYGI5:  ItemData(1230650, 1, "progress", None),
    itemName.JIGGYGI6:  ItemData(1230651, 1, "progress", None),
    itemName.JIGGYGI7:  ItemData(1230652, 1, "progress", None),
    itemName.JIGGYGI8:  ItemData(1230653, 1, "progress", None),
    itemName.JIGGYGI9:  ItemData(1230654, 1, "progress", None),
    itemName.JIGGYGI10: ItemData(1230655, 1, "progress", None),
    itemName.JIGGYHP1:  ItemData(1230656, 1, "progress", None),
    itemName.JIGGYHP2:  ItemData(1230657, 1, "progress", None),
    itemName.JIGGYHP3:  ItemData(1230658, 1, "progress", None),
    itemName.JIGGYHP4:  ItemData(1230659, 1, "progress", None),
    itemName.JIGGYHP5:  ItemData(1230660, 1, "progress", None),
    itemName.JIGGYHP6:  ItemData(1230661, 1, "progress", None),
    itemName.JIGGYHP7:  ItemData(1230662, 1, "progress", None),
    itemName.JIGGYHP8:  ItemData(1230663, 1, "progress", None),
    itemName.JIGGYHP9:  ItemData(1230664, 1, "progress", None),
    itemName.JIGGYHP10: ItemData(1230665, 1, "progress", None),
    itemName.JIGGYCC1:  ItemData(1230666, 1, "progress", None),
    itemName.JIGGYCC2:  ItemData(1230667, 1, "progress", None),
    itemName.JIGGYCC3:  ItemData(1230668, 1, "progress", None),
    itemName.JIGGYCC4:  ItemData(1230669, 1, "progress", None),
    itemName.JIGGYCC5:  ItemData(1230670, 1, "progress", None),
    itemName.JIGGYCC6:  ItemData(1230671, 1, "progress", None),
    itemName.JIGGYCC7:  ItemData(1230672, 1, "progress", None),
    itemName.JIGGYCC8:  ItemData(1230673, 1, "progress", None),
    itemName.JIGGYCC9:  ItemData(1230674, 1, "progress", None),
    itemName.JIGGYCC10: ItemData(1230675, 1, "progress", None),
}

moves_table = {
    itemName.GGRAB:         ItemData(1230753, 1, "progress", None),
    itemName.BBLASTER:      ItemData(1230754, 1, "progress", None),
    itemName.EGGAIM:        ItemData(1230755, 1, "progress", None),

    itemName.FEGGS:         ItemData(1230756, 1, "progress", None),

    itemName.BDRILL:        ItemData(1230757, 1, "progress", None),
    itemName.BBAYONET:      ItemData(1230758, 1, "progress", None),

    itemName.GEGGS:         ItemData(1230759, 1, "progress", None),

    itemName.AIREAIM:       ItemData(1230760, 1, "progress", None),
    itemName.SPLITUP:       ItemData(1230761, 1, "progress", None),
    itemName.PACKWH:        ItemData(1230762, 1, "progress", None),
    
    itemName.IEGGS:         ItemData(1230763, 1, "progress", None),

    itemName.WWHACK:        ItemData(1230764, 1, "progress", None),
    itemName.TTORP:         ItemData(1230765, 1, "progress", None),
    itemName.AUQAIM:        ItemData(1230766, 1, "progress", None),

    itemName.CEGGS:         ItemData(1230767, 1, "progress", None),

    itemName.SPRINGB:       ItemData(1230768, 1, "progress", None),
    itemName.TAXPACK:       ItemData(1230769, 1, "progress", None),
    itemName.HATCH:         ItemData(1230770, 1, "progress", None),

    itemName.SNPACK:        ItemData(1230771, 1, "progress", None),
    itemName.LSPRING:       ItemData(1230772, 1, "progress", None),
    itemName.CLAWBTS:       ItemData(1230773, 1, "progress", None),

    itemName.SHPACK:        ItemData(1230774, 1, "progress", None),
    itemName.GLIDE:         ItemData(1230775, 1, "progress", None),

    itemName.SAPACK:        ItemData(1230776, 1, "progress", None),

 #   itemName.FSWIM:         ItemData(1230777, 1, "progress", None),
}

level_progress_table = {
    itemName.MUMBOMT:        ItemData(1230855, 1, "progress", locationName.GLOWBOMT1),
    itemName.MUMBOGM:        ItemData(1230856, 1, "progress", locationName.GLOWBOGM1),
    itemName.MUMBOWW:        ItemData(1230857, 1, "progress", locationName.GLOWBOWW1),
    itemName.MUMBOJR:        ItemData(1230858, 1, "progress", locationName.GLOWBOJR1),
    itemName.MUMBOTD:        ItemData(1230859, 1, "progress", locationName.GLOWBOTL1),
    itemName.MUMBOGI:        ItemData(1230860, 1, "progress", locationName.GLOWBOGI1),
    itemName.MUMBOHP:        ItemData(1230861, 1, "progress", locationName.GLOWBOHP1),
    itemName.MUMBOCC:        ItemData(1230862, 1, "progress", locationName.GLOWBOCC1),
    itemName.MUMBOIH:        ItemData(1230863, 1, "progress", locationName.GLOWBOIH1),

    itemName.HUMBAMT:        ItemData(1230174, 1, "progress", locationName.GLOWBOMT2),
    itemName.HUMBAGM:        ItemData(1230175, 1, "progress", locationName.GLOWBOGM2),
    itemName.HUMBAWW:        ItemData(1230176, 1, "progress", locationName.GLOWBOWW2),
    itemName.HUMBAJR:        ItemData(1230177, 1, "progress", locationName.GLOWBOJR2),
    itemName.HUMBATD:        ItemData(1230178, 1, "progress", locationName.GLOWBOTL2),
    itemName.HUMBAGI:        ItemData(1230179, 1, "progress", locationName.GLOWBOGI2),
    itemName.HUMBAHP:        ItemData(1230180, 1, "progress", locationName.GLOWBOHP2),
    itemName.HUMBACC:        ItemData(1230181, 1, "progress", locationName.GLOWBOCC2),
    itemName.HUMBAIH:        ItemData(1230182, 1, "progress", locationName.GLOWBOMEG),
}

misc_collectable_table = {
    itemName.HONEY:         ItemData(1230512, 25, "useful", None),
    itemName.PAGES:         ItemData(1230513, 25, "useful", None),
    itemName.DOUBLOON:      ItemData(1230514, 30, "useful", None)
}



all_item_table = {
    **jinjo_table,
    **level_progress_table,
    **misc_collectable_table,
    **jiggy_table,
    **moves_table
}

all_group_table = {
    'jiggy' : jiggy_table,
    'jinjo' : jinjo_table,
    'misc' : misc_collectable_table,
    'moves': moves_table,
    "magic": level_progress_table
}



