import copy
from PIL import Image
import collections
from dustmaker import *
import PropUtils
from imageMaker import PropConstants

a = 'testImages/blackRook.png'      #test for RGBA png
b = 'testImages/whiteKnight.png'    #test for RGBA png
c = 'testImages/linkSprite.gif'     #test for P gif
d = 'testImages/skyhawk33.jpg'      #test for RBG jpeg
e = 'testImages/GreatWave.png'      #test for 150 paletted png
f = 'testImages/MonaLisa.png'       #test for 150 paletted png

"""to create a 150 paletted PNG,
-   Find any image and Ctrl+Shift+V into Gimp
-   Colors... to improve contrast (optional)
-   Image > Mode > Indexed > Generate Optimum Palette, max colors 150
-   Image > Scale Image, to a reasonable size
"""

import imageMaker.PropConstants as Group
SCALE = 0.06
SPACING = 4 / 48
MAX_SIZE = 128
ARGS = (0, 0, True, True)
PROPS = [None for i in range(129)]
PROPS[1] = [(0, 0, Prop(*ARGS, SCALE, *Group.STORAGE, 4, 0))]
PROPS[2] = [(-2 / 48, -3 / 48, Prop(*ARGS, 0.141, *Group.STORAGE, 4, 0))]
PROPS[4] = [(-6 / 48, -9 / 48, Prop(*ARGS, 0.271, *Group.STORAGE, 4, 0))]
PROPS[8] = [(-14 / 48, -22 / 48, Prop(*ARGS, 0.521, *Group.STORAGE, 4, 0))]
PROPS[16] = [(-30 / 48, -46 / 48, Prop(*ARGS, 1.000, *Group.STORAGE, 4, 0))]

PROPS[32] = [(-55 / 48, 11 / 48, Prop(*ARGS, 0.442, *Group.BACKDROP, 6, 0)),
             (-55 / 48, -29 / 48, Prop(*ARGS, 0.442, *Group.BACKDROP, 6, 0)),
             (-55 / 48, -57 / 48, Prop(*ARGS, 0.442, *Group.BACKDROP, 6, 0))]

PROPS[64] = [(-168 / 48, -159 / 48, Prop(*ARGS, 0.721, *Group.BACKDROP2, 7, 0)),
             (-168 / 48, -35 / 48, Prop(*ARGS, 0.721, *Group.BACKDROP2, 7, 0))]

PROPS[128] = [(-823 / 48, -558 / 48, Prop(*ARGS, 1.919, *Group.MACHINERY, 14, 0)),
              (-275 / 48, -58 / 48, Prop(*ARGS, 1.177, *Group.BACKDROP2, 7, 0)),
              (-275 / 48, -269 / 48, Prop(*ARGS, 1.177, *Group.BACKDROP2, 7, 0)),
              (-275 / 48, -358 / 48, Prop(*ARGS, 1.177, *Group.BACKDROP2, 7, 0))]

im = Image.open(e)
im = im.convert("RGB")
data = list(im.getdata())
print(data)
x,y,width,height = im.getbbox()
print(width,height)
counter = collections.Counter(data)
colors = sorted(list(counter),key=counter.get, reverse=True)
print(colors)


map_file = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/lisa'
# load map
with open(map_file, "rb") as f:
    map = read_map(f.read())
map.level_type(LevelType.DUSTMOD)

size = 0.06
prop = Prop(0, 0, True, True, size, 1, 11, 4, 0)
marker = Prop(0,0,True,True,1,*PropConstants.MACHINERY,19,0)
utils = PropUtils.PropUtils('C:/Users/Ryley/PycharmProjects/PropUtils-master/sprite-data',True)

print('---------------------------------------')
for prop in map.props:
    if map.get_prop_layer(prop) is 20:
        thing = map.get_prop(prop)
        print(thing.prop_set, thing.prop_group, thing.prop_index, thing.palette)

for dx, dy, base_prop in PROPS[128]:
    print(dx, dy, base_prop)
    prop = copy.deepcopy(base_prop)
    prop.layer_sub = 0
    map.add_prop(20, dx, dy, prop)
'''
for i in range(5,39000):
    if PropUtils.get_prop_scale(i / 1   000) > PropUtils.get_prop_scale((i - 1) / 1000):
        print(i/1000," - ",end="")
    if PropUtils.get_prop_scale(i/1000) < PropUtils.get_prop_scale((i+1)/1000) or i == 38999:
        print(i/1000,">",PropUtils.get_prop_scale(i/1000))
        new_prop = copy.deepcopy(prop)
        new_prop.scale = i/1000
        map.add_prop(12, *utils.set_prop_location(i/100, 0, new_prop, PropUtils.Pivot.BOTTOM_LEFT), new_prop)
        map.add_prop(13, i / 100, 0, copy.deepcopy(prop))
        map.add_prop(13, i / 100 + new_prop.scale*1.4917, 0, copy.deepcopy(prop))
        map.add_prop(13, i / 100, 0 - new_prop.scale*1.4375, copy.deepcopy(prop))
        map.add_prop(13, i / 100 + new_prop.scale*1.4917, 0 - new_prop.scale*1.4375, copy.deepcopy(prop))
        blx,bly = utils.get_prop_offset(new_prop,PropUtils.Pivot.BOTTOM_LEFT)
        print(blx/PropUtils.get_prop_scale(i/1000), bly/PropUtils.get_prop_scale(i/1000))
'''

map.name(map.name() + '_modified')
with open(map_file + "_modified", "wb") as f:
    f.write(write_map(map))