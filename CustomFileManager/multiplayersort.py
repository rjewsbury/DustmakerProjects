import os
import urllib.request as url
from dustmaker import *

BASE = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/'
read_sub = 'noflag/visible/non-multiplayer'
website = 'https://atlas.dustforce.com/%s/%s'

for map_name in os.listdir(BASE+read_sub):
    if('-' not in map_name):
        print(map_name, '---------------------------------------------------------------')
        continue
    try:
        name_split = list(map_name[::-1].split('-',1))
        name = name_split[1][::-1]
        num = name_split[0][::-1]
        #print(name,num)
    except:
        print(map_name, '---------------------------------------------------------------')
        continue

    with open(BASE + read_sub + map_name, "rb") as f:
        main_map = read_map(f.read())

    print(map_name,main_map.level_type())
