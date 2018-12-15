import os
import urllib.request as url
from dustmaker import *
import ssl

BASE = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/'
read_sub = 'flag+visible/apple/'

website = 'https://dustkid.com/json/level/%s/apple/all'

for map_name in os.listdir(BASE+read_sub):
    if(map_name == 'appleSS_complete' or map_name == 'appleSS_impossible'):
        continue

    #print(website%(map_name))
    try:
        data = url.urlopen(website%(map_name.replace(' ','%20')), context=ssl._create_unverified_context())
    except:
        print('-----------------------------------------------------------',map_name)
        continue

    stats = {}
    exec("stats = " + data.read().decode('utf-8'))

    hit_apples = 0
    for key in (key for key in stats['scores'] if stats['scores'][key]['user'] == 76378):
        if(stats['scores'][key]['score_completion']==5 and stats['scores'][key]['score_finesse']==5):
            hit_apples = stats['scores'][key]['apples']

    with open(BASE + read_sub + map_name, "rb") as f:
        main_map = read_map(f.read())

    apples = 0
    for key in main_map.entities:
        if (main_map.entities[key][2].type == 'hittable_apple'):
            apples += 1

    print(map_name, apples, hit_apples)
    if(hit_apples == apples):
        print('DONE!')
        os.rename(BASE + read_sub + map_name, BASE + read_sub + 'appleSS_complete/' + map_name)
    else:
        print('NO')