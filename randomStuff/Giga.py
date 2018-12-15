from dustmaker import *

f1 = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/1000 Giga Walls'

with open(f1, "rb") as f:
    map = read_map(f.read())

print(list(map.entities.values()))

tiles = map.tiles.copy()
entities = list(map.entities.copy().values())

for i in range(1,1000):
    for layer, x, y in tiles:
        tile = map.tiles.get((layer, x, y))
        map.add_tile(layer, x+7*i, y, tile)
    for x, y, entity in entities:
        map.add_entity(x+i*7,y,entity)

map.name(map.name() + '_modified')
with open(f1 + "_modified", "wb") as f:
    f.write(write_map(map))