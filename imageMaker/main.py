from dustmaker import *
import imageMaker.PropImage as _PropImage
from imageMaker.BetterFogTrigger import BetterFogTrigger
import imageMaker.Images as img

map_file = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/CustomMapRace52'

# load map
with open(map_file, "rb") as f:
    map = read_map(f.read())
map.level_type(LevelType.DUSTMOD)

for id in map.entities:
    if map.get_entity(id).type == 'fog_trigger':
        print(id,map.get_entity_xposition(id),map.get_prop_yposition(id),map.get_entity(id))

# loads the image

# creates the fog trigger
floor_1_fog = BetterFogTrigger(map.get_entity(24014))
floor_2_fog = BetterFogTrigger(map.get_entity(24008))
floor_3_fog = BetterFogTrigger(map.get_entity(24009))
credits_fog = BetterFogTrigger(map.get_entity(24020))

map.add_entity(5, -10, floor_1_fog)
map.add_entity(5, -40, floor_2_fog)
map.add_entity(5, -70, floor_3_fog)
map.add_entity(-360,-24, credits_fog)

# create and place props
#Credits---------------------------------------------------------------
'''
#OVERWRITING CONSTANTS OH JEEZ
old_spacing = _PropImage.SPACING
_PropImage.SPACING = 6/48
_PropImage.PROPS[1][0][2].scale = 0.1
#MAKING IMAGES ON BACKGROUND LAYERS IS HARD
img.foreground_mario.compress(_PropImage._outline)
img.foreground_mario.x = -441.95 #-166.95
img.foreground_mario.y = -44 #-40
img.foreground_mario.build_image(map, credits_fog,19,15)

img.background_mario.compress(_PropImage._outline)
img.background_mario.x = -441.95 #-166.95
img.background_mario.y = -44 #-40
img.background_mario.build_image(map, credits_fog,17,0)
#STOP THIS NONSENSE
_PropImage.SPACING = old_spacing
_PropImage.PROPS[1][0][2].scale = _PropImage.SCALE

# img.font.x = -100
# img.font.y = 0
# img.font.build_image(map, credits_fog, 17, 15)
''''''

#First Floor---------------------------------------------------------------
''''''
img.shovel_knight.compress()
img.shovel_knight.x = 10.08
img.shovel_knight.y = -20.8
img.shovel_knight.build_image(map, floor_1_fog, 13, 0)

img.kirby.compress()
img.kirby.x = -15.08
img.kirby.y = -20.08
img.kirby.build_image(map, floor_1_fog, 13, 11)

img.mario.compress()
img.mario.x = 1#-5.75 #THIS PAINTING SHOULD GO AT -5.75 BUT THERES A ROUNDING ERROR ACROSS THE AXIS
img.mario.y = -12.25
img.mario.build_image(map, floor_1_fog, 15, 0)
''''''

#Second Floor---------------------------------------------------------------

''''''
#OVERWRITING CONSTANTS OH JEEZ
old_spacing = _PropImage.SPACING
_PropImage.SPACING = 0.5
_PropImage.PROPS[1][0][2].scale = 0.05
#MAKING IMAGES ON BACKGROUND LAYERS IS HARD
img.islands.compress(_PropImage._outline)
img.islands.x = -100
img.islands.y = -30
img.islands.build_image(map, floor_2_fog,5,1)
#STOP THIS NONSENSE
_PropImage.SPACING = old_spacing
_PropImage.PROPS[1][0][2].scale = _PropImage.SCALE
''''''
# img.metroid.compress()
# img.metroid.x = -3
# img.metroid.y = -40
# img.metroid.build_image(map, floor_2_fog, 6, 0)

img.wide_cloud.compress()
img.wide_cloud.x = 8
img.wide_cloud.y = -51
img.wide_cloud.build_image(map, floor_2_fog, 10, 0)

img.small_cloud.compress()
img.small_cloud.x = 22
img.small_cloud.y = -38
img.small_cloud.build_image(map, floor_2_fog, 10, 0)
img.small_cloud.x = -22
img.small_cloud.y = -38
img.small_cloud.build_image(map, floor_2_fog, 10, 0)

img.big_cloud.compress()
img.big_cloud.x = 20
img.big_cloud.y = -44
img.big_cloud.build_image(map, floor_2_fog, 8, 0)
img.big_cloud.x = -20
img.big_cloud.y = -50
img.big_cloud.build_image(map, floor_2_fog, 8, 0)

img.vines.compress()
img.vines.x = -21
img.vines.y = -50
img.vines.build_image(map, floor_2_fog, 12, 0)

img.sonic.compress()
img.sonic.x = -19
img.sonic.y = -33.3
img.sonic.build_image(map, floor_2_fog, 13, 0)

img.megaman.compress()
img.megaman.x = 9
img.megaman.y = -40
img.megaman.build_image(map, floor_2_fog, 13, 12)

# img.link.compress()
# img.link.x = 19
# img.link.y = -33
# img.link.build_image(map, floor_2_fog, 14, 4)

img.fez.compress()
img.fez.x = 16.5
img.fez.y = -47.1
img.fez.build_image(map, floor_2_fog, 14,2)

img.liliac.compress()
img.liliac.x = -13
img.liliac.y = -43
img.liliac.build_image(map, floor_2_fog, 19, 14)

# img.dark_pine.compress()
# img.dark_pine.x = 18.5
# img.dark_pine.y = -35.8
# img.dark_pine.build_image(map, floor_2_fog, 14, 9)
# 
# img.oak.compress()
# img.oak.x = -13
# img.oak.y = -34.6
# img.oak.build_image(map, floor_2_fog, 14, 22)
''''''

#Third Floor---------------------------------------------------------
''''''
img.dustman.compress()
img.dustman.x = -35
img.dustman.y = -81
img.dustman.build_image(map, floor_3_fog, 9, 14, transparency=(0,0,0))

img.leafsprite.compress()
img.leafsprite.x = 10
img.leafsprite.y = -81
img.leafsprite.build_image(map, floor_3_fog, 9, 0, transparency=(255,255,255))

img.dustgirl.compress()
img.dustgirl.x = -25
img.dustgirl.y = -81
img.dustgirl.build_image(map, floor_3_fog, 7, 12, transparency=(0,0,0))

img.dustwraith.compress()
img.dustwraith.x = 0
img.dustwraith.y = -81
img.dustwraith.build_image(map, floor_3_fog, 7, 0, transparency=(0,0,0))
'''

print('total props:',len(map.props))
# save map
map.name(map.name() + '_modified')
with open(map_file + "_modified", "wb") as f:
    f.write(write_map(map))
