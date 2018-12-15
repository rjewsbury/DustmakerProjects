import os
from dustmaker import *

folder = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/'
for file in os.listdir(folder):
    if not file.endswith('CCW'):
        continue

    with open(folder+file,'rb') as f:
        level = read_map(f.read())

    level.rotate(3)
    level.name(level.name()+' CCW')

    keys = list(level.entities.keys())
    for key in keys:
        if level.entities[key][2].type == 'camera_node':
            level.entities.pop(key)

    level.remap_ids()

    level.vars['key_get_type'].value = 0
    print('done',level.name())

    with open(folder+file,'wb') as f:
        f.write(write_map(level))