import os
import imageio

path = 'C:/Users/Ryley/Documents/Ryleys Documents/Games/Dustforce/Skins/pixelSprites/area'

def make_gif(directory, count = 0):
    list = os.listdir(directory)
    file_groups = {}
    for file in list:
        if file.endswith('_src.png'):
            file_groups[file[:-12]] = 1 + file_groups.get(file[:-12],0)
        elif '.' in file:
            print('FOUND '+file)
        else:
            count += make_gif(directory+'/'+file)

    for group in file_groups:
        count += 1
        if file_groups[group] > 1 and not str(group).startswith('npc_3_1') and not str(group).startswith('intro'):
            print(directory+'/'+group)
            images = []
            for i in range(1,file_groups[group]+1):
                images.append(imageio.imread(directory+'/'+group+'%04d_src.png'%i))
            imageio.mimsave(directory+'/'+group+'_src.gif',images)

    return count

print(make_gif(path))