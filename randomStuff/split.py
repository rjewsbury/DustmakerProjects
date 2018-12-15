from dustmaker import *

f1 = 'wraeclasta'
x1 = 472
y1 = 322

BASE = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/'
with open(BASE + f1, "rb") as f:
    m1 = read_map(f.read())

m2 = Map()
m2.name(m1.name() + '_modified')

for tile in m1.tiles:
    print(tile, m1.tiles[tile])
    if(tile[1] <= x1 and tile[2] <= y1):
        m2.add_tile(*tile,m1.get_tile(*tile))

for prop in m1.props:
    print(prop, m1.props[prop])
    if (m1.props[prop][1] <= x1 and m1.props[prop][2] <= y1):
        m2.add_prop(*m1.props[prop])

for entity in m1.entities:
    print(entity, m1.entities[entity])
    if (m1.entities[entity][0] <= x1 and m1.entities[entity][1] <= y1):
        m2.add_entity(*m1.entities[entity],entity)

with open(BASE + f1 + "_modified", "wb") as f:
    f.write(write_map(m2))