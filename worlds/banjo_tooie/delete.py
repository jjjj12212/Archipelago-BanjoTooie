string = """
    itemName.SILOIOHJV:           ItemData(1230870,   1, "progress"),
    itemName.SILOIOHWH:           ItemData(1230871,   1, "progress"),
    itemName.SILOIOHPL:           ItemData(1230872,   1, "progress"),
    itemName.SILOIOHPG:           ItemData(1230873,   1, "progress"),
    itemName.SILOIOHCT:           ItemData(1230874,   1, "progress"),
    itemName.SILOIOHWL:           ItemData(1230875,   1, "progress"),
    itemName.SILOIOHQM:           ItemData(1230876,   1, "progress"),
}

warp_pad_table = {
    itemName.WARPMT1:           ItemData(1230877,   1, "progress"),
    itemName.WARPMT2:           ItemData(1230878,   1, "progress"),
    itemName.WARPMT3:           ItemData(1230879,   1, "progress"),
    itemName.WARPMT4:           ItemData(1230880,   1, "progress"),
    itemName.WARPMT5:           ItemData(1230881,   1, "progress"),
    itemName.WARPGM1:           ItemData(1230882,   1, "progress"),
    itemName.WARPGM2:           ItemData(1230883,   1, "progress"),
    itemName.WARPGM3:           ItemData(1230884,   1, "progress"),
    itemName.WARPGM4:           ItemData(1230885,   1, "progress"),
    itemName.WARPGM5:           ItemData(1230886,   1, "progress"),
    itemName.WARPWW1:           ItemData(1230887,   1, "progress"),
    itemName.WARPWW2:           ItemData(1230888,   1, "progress"),
    itemName.WARPWW3:           ItemData(1230889,   1, "progress"),
    itemName.WARPWW4:           ItemData(1230890,   1, "progress"),
    itemName.WARPWW5:           ItemData(1230891,   1, "progress"),
    itemName.WARPJR1:           ItemData(1230892,   1, "progress"),
    itemName.WARPJR2:           ItemData(1230893,   1, "progress"),
    itemName.WARPJR3:           ItemData(1230894,   1, "progress"),
    itemName.WARPJR4:           ItemData(1230895,   1, "progress"),
    itemName.WARPJR5:           ItemData(1230896,   1, "progress"),
    itemName.WARPTL1:           ItemData(1230897,   1, "progress"),
    itemName.WARPTL2:           ItemData(1230898,   1, "progress"),
    itemName.WARPTL3:           ItemData(1230899,   1, "progress"),
    itemName.WARPTL4:           ItemData(1230900,   1, "progress"),
    itemName.WARPTL5:           ItemData(1230901,   1, "progress"),
    itemName.WARPGI1:           ItemData(1230902,   1, "progress"),
    itemName.WARPGI2:           ItemData(1230903,   1, "progress"),
    itemName.WARPGI3:           ItemData(1230904,   1, "progress"),
    itemName.WARPGI4:           ItemData(1230905,   1, "progress"),
    itemName.WARPGI5:           ItemData(1230906,   1, "progress"),
    itemName.WARPHP1:           ItemData(1230907,   1, "progress"),
    itemName.WARPHP2:           ItemData(1230908,   1, "progress"),
    itemName.WARPHP3:           ItemData(1230909,   1, "progress"),
    itemName.WARPHP4:           ItemData(1230910,   1, "progress"),
    itemName.WARPHP5:           ItemData(1230911,   1, "progress"),
    itemName.WARPCC1:           ItemData(1230912,   1, "progress"),
    itemName.WARPCC2:           ItemData(1230913,   1, "progress"),
    itemName.WARPCK1:           ItemData(1230914,   1, "progress"),
    itemName.WARPCK2:           ItemData(1230915,   1, "progress"),
"""

start_index = 1230870
print(string)
for line in string.split("\n"):
    if len(line) < 20:
        continue
    item = line[line.index(".")+1:line.index(":")]
    print(line[:line.rindex("\"")+1] + ", locationName.{}),".format(item))
    #print("itemName.{}:           ItemData({},   1, \"progress\"),".format(line[:line.find("=")-1], start_index))
    start_index += 1
