from dustmaker import *
import os

BASE = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/'
sub_folder = ""

for map_name in os.listdir(BASE):
    if(map_name == 'error' or map_name == 'flag' or map_name == 'noflag' or map_name == 'apple'):
        continue

    try:
        with open(BASE + map_name, "rb") as f:
            main_map = read_map(f.read())
    except:
        print('error/', map_name)
        os.rename(BASE + map_name, BASE + 'error/' + map_name)
        continue

    sub_folder = ''

    for key in main_map.entities:
        if (main_map.entities[key][2].type == 'level_end' or main_map.entities[key][2].type == 'level_end_prox'):
            sub_folder = 'flag/'
            break

    if(sub_folder == ''):
        sub_folder = 'noflag/'

    print(sub_folder, map_name)
    os.rename(BASE + map_name, BASE + sub_folder + map_name)