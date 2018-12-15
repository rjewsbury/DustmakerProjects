from dustmaker import *
import os

BASE = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/'

for map_name in os.listdir(BASE+'flag/'):
    with open(BASE + 'flag/' + map_name, "rb") as f:
        main_map = read_map(f.read())

    apple = 0
    for key in main_map.entities:
        if (main_map.entities[key][2].type == 'hittable_apple'):
            apple += 1
            break

    if(apple == 0):
        print('__',map_name)
    else:
        print('%02d'%apple, map_name)
        os.rename(BASE + 'flag/' + map_name, BASE + 'apple/' + map_name)