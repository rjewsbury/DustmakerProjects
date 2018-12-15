from dustmaker import *

f0 = 'apple tutorial'
f1 = 'apple tutorial'
x1 = 100
y1 = 0
f2 = 'apple tutorial'
x2 = 200
y2 = 0

BASE = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/'
with open(BASE + f0, "rb") as f:
    main_map = read_map(f.read())
with open(BASE + f1, "rb") as f:
    m1 = read_map(f.read())
with open(BASE + f2, "rb") as f:
    m2 = read_map(f.read())

m1.transform([[1,0,x1],[0,1,y1]])
m2.transform([[1,0,x2],[0,1,y2]])

main_map.merge_map(m1)
main_map.merge_map(m2)

main_map.name(main_map.name() + '_modified')
with open(BASE + f0 + "_modified", "wb") as f:
    f.write(write_map(main_map))