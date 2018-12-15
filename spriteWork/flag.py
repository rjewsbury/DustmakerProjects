from PIL import Image, ImageOps
import os

dir_name = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/content_src/sprites/player/dustworth/jump'
add_on_path = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/content_src/sprites/entities/mansion/flag/'

for i,file in enumerate(os.listdir(dir_name)):
    if file.endswith(".png"):
        base = Image.open(add_on_path+'cleansed1%04d.png'%(((int(file[-7:-4])-1)%7)+1))
        #base = ImageOps.flip(base)
        base.save(dir_name+'/'+file)