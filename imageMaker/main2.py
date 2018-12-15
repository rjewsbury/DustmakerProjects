from dustmaker import *
import imageMaker.PropImage as _constants
from imageMaker.PropImage import PropImage
from imageMaker.BetterFogTrigger import BetterFogTrigger
import imageMaker.PropConstants as Group

map_file = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/Testing'

#Proper size: 134 x 76

with open(map_file, "rb") as f:
    map = read_map(f.read())
map.level_type(LevelType.DUSTMOD)

for id in map.entities:
    if map.get_entity(id).type == 'fog_trigger':
        print(id,map.get_entity_xposition(id),map.get_prop_yposition(id),map.get_entity(id))

fog = BetterFogTrigger()

map.add_entity(0,0,fog)

FOLDER = 'C:/Users/Ryley/Documents/Ryleys Documents/Games/Dustforce/Mapmaking/testImages/'
img = PropImage(FOLDER+'starry3.png')
print('original:', 'size =',img.size, '\tcolors =',len(img.colors), 'props =',len(img._pixel_data))
#img.compress()
#print('compressed:','size =',img.size, '\tcolors =',len(img.colors), 'props =',len(img._pixel_data))

#MODIFYING CONSTANTS

_constants.PROPS[1][0] = (0,0,Prop(0, 0, True, True, 1, *Group.MACHINERY, 19, 0))
_constants.SPACING = 18/48 # 18/48 is the max for dots

#END MADNESS

img.x=-28.8
img.y=-20.1
img.build_image(map, fog, 13, 0)

print('total props:',len(map.props))
# save map
map.name(map.name() + '_modified')
with open(map_file + "_modified", "wb") as f:
    f.write(write_map(map))