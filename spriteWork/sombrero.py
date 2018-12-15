from PIL import Image
import os

dir_name = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/content_src/sprites/player/dustman/wallrun'
add_on_path = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/content_src/sprites/player/Sombrero-clip-art-3.png'
add_on = Image.open(add_on_path)

for file in os.listdir(dir_name):
    if file.endswith(".png"):
        base = Image.open(dir_name+'/'+file)
        base.paste(add_on,(75,85),add_on)
        base.save(dir_name+'/'+file)