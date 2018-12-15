import os
from PIL import Image

path = 'C:/Users/Ryley/Documents/Ryleys Documents/Games/Dustforce/Skins/OutlineTest/player'

air_hitbox_path = 'C:/Users/Ryley/Documents/Ryleys Documents/Games/Dustforce/Skins/OutlineTest/air_hitbox.png'
ceiling_hitbox_path = 'C:/Users/Ryley/Documents/Ryleys Documents/Games/Dustforce/Skins/OutlineTest/ceiling_hitbox.png'
grounded_hitbox_path = 'C:/Users/Ryley/Documents/Ryleys Documents/Games/Dustforce/Skins/OutlineTest/grounded_hitbox.png'
wall_hitbox_path = 'C:/Users/Ryley/Documents/Ryleys Documents/Games/Dustforce/Skins/OutlineTest/wall_hitbox.png'

hitbox = [
    Image.open(air_hitbox_path),        #0
    Image.open(ceiling_hitbox_path),    #1
    Image.open(grounded_hitbox_path),   #2
    Image.open(wall_hitbox_path)        #3
]

types = {}

def make_hitbox(directory, count = 0):

    if directory.endswith('fx'):
        return 0

    list = os.listdir(directory)
    file_groups = {}
    for file in list:
        if file.endswith('.png'):
            file_groups[file[:-8]] = 1 + file_groups.get(file[:-8],0)
        elif '.' in file:
            print('FOUND '+file)
        else:
            count += make_hitbox(directory+'/'+file)

    for group in file_groups:
        if group in types:
            type = types[group]
        else:
            type = -1
            while type < 0:
                try:
                    type = int(input(group))
                except:
                    pass
            types[group] = type
        count += 1
        for i in range(file_groups[group]):
            base = Image.open(directory + '/' + group + ('%04d'%(i+1)) + '.png')
            base.paste(hitbox[type], mask=hitbox[type])
            base.save(directory + '/' + group + ('%04d'%(i+1)) + '.png')

    return count

print(make_hitbox(path))