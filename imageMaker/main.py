from dustmaker import *
from imageMaker.PropImage import PropImage
from imageMaker.BetterFogTrigger import BetterFogTrigger

map_file = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/lisa'
img_1 = 'testImages/MonaLisa_5_M.png'
img_2 = 'testImages/MonaLisa_20_M.png'
img_3 = 'testImages/MonaLisa_50_M.png'

# load map
with open(map_file, "rb") as f:
    map = read_map(f.read())
map.level_type(LevelType.DUSTMOD)

# loads the image
prop_img_1 = PropImage(img_1)
prop_img_1.x = 5
prop_img_1.y = -20
prop_img_1.prop_size = 0.1

# loads the image
prop_img_2 = PropImage(img_2)
prop_img_2.x = 35
prop_img_2.y = -20
prop_img_2.prop_size = 1

# loads the image
prop_img_3 = PropImage(img_3)
prop_img_3.x = 100
prop_img_3.y = -20
prop_img_3.prop_size = 1

print(prop_img_1.size)

# creates the fog trigger
fog = BetterFogTrigger()
fog.set_gradient(
    (0x97, 0xcc, 0xf1),
    (0x8a, 0xc6, 0xef),
    (0x7e, 0xc0, 0xee))
map.add_entity(0, 0, fog)

# create and place props

prop_img_1.build_image(map, fog, 12, 5)
prop_num = len(map.props)
print(prop_num)

prop_img_1.compress()
prop_img_1.x -= 20
prop_img_1.build_image(map, fog, 12, 5)

#gets the relative percentage of props in the compressed image
print((len(map.props)-prop_num)/prop_num*100,'%')

#prop_img_2.build_image(map, fog, 12, 11)
#prop_img_3.build_image(map, fog, 13, 7)



# save map
map.name(map.name() + '_modified')
with open(map_file + "_modified", "wb") as f:
    f.write(write_map(map))
