from dustmaker import *
import copy

def find_apples(map):
    apples = []
    for key in map.entities:
        if map.entities[key][2].type == 'hittable_apple':
            apples.append(map.entities[key])
    return apples

if __name__ == '__main__':
    map_file = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/Midnight-Temple-8057'

    with open(map_file, "rb") as f:
        map = read_map(f.read())

    print(find_apples(map))
