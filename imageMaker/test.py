from PIL import Image
import collections
from dustmaker import *

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

size = 6
prop = Prop(0, 0, True, True, size, 1, 11, 4, 0)
for x in range(-50,50,15):
    for y in range(-50,50,15):
        map.add_tile(19,x,y,Tile(0))
        map.add_prop(12,x,y,prop)

map.name(map.name() + '_modified')
with open(map_file + "_modified", "wb") as f:
    f.write(write_map(map))