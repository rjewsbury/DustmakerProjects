from dustmaker import *

path = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/appleNonsense'
map = Map()
map.name("appleNonsense")
for i in range(1000):
    apple = Apple()
    map.add_entity(0,0,apple)

with open(path, "wb") as f:
    f.write(write_map(map))