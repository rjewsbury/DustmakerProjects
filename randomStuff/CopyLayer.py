from dustmaker import *
import copy
map_file = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/virttest'

with open(map_file, "rb") as f:
    map = read_map(f.read())

tiles = {}
for key in map.tiles:
    if key[0] == 6:
        tiles[(10,key[1],key[2])] = copy.deepcopy(map.tiles[key])
    tiles[key] = map.tiles[key]
map.tiles = tiles
for prop in map.props:
    if prop[0] == 6:
        map.add_prop(*copy.deepcopy(prop))

# save map
map.name(map.name() + '_modified')
with open(map_file + "_modified", "wb") as f:
    f.write(write_map(map))