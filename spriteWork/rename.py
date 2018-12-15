import os

path = 'C:/Users/Ryley/Documents/Ryleys Documents/Games/Dustforce/Skins/pixelSprites/area'

def rewrite(directory, count = 0):
    list = os.listdir(directory)
    for file in list:
        if file.endswith('.png'):
            print(directory+'/'+file)
            os.rename(directory+'/'+file, directory+'/'+file.split('.')[0]+'_src.png')
            count += 1
        elif '.' in file:
            print('FOUND '+file)
        else:
            count += rewrite(directory+'/'+file)
    return count

print(rewrite(path))