from dustmaker import *
from PIL import Image
import binascii
import io

map_file = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/TwoNewCards'
img_path = 'C:/Users/Ryley/Documents/Ryleys Documents/Games/Dustforce/Mapmaking/Images/thumbtest2.png'

#Proper size: 134 x 76

with open(map_file, "rb") as f:
    map = read_map(f.read())
map.level_type(LevelType.DUSTMOD)

print(map.sshot)

with open(img_path,"rb") as f:
    bytes = f.read()
    print(type(bytes))
    print(bytes)
    map.sshot = bytes

    stream2 = io.BytesIO(bytes)
    img2 = Image.open(stream2)

stream = io.BytesIO(map.sshot)
img = Image.open(stream)


print(type(img), img.getbands(), img.getbbox())
print()
print(type(img2), img2.getbands(), img2.getbbox())
print()

#img.save("C:/Users/Ryley/Documents/Ryleys Documents/Games/Dustforce/Mapmaking/Images/thumbtest.png","PNG")

# save map
map.name(map.name() + '_modified')
with open(map_file + "_modified", "wb") as f:
    f.write(write_map(map))

