import os

BASE = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/'
read_sub = 'flag/visible/apple/appleSS_complete/'

count = 0

for map_name in os.listdir(BASE+read_sub):
    if('-' not in map_name):
        continue
    pass
    try:
        name_split = list(map_name[::-1].split('-',1))
        name = name_split[1][::-1]
        num = name_split[0][::-1]
        #print(name,num)
    except:
        break

    if(7107<=int(num)<=8200):
        print(map_name)
        count+=1

print()
print(count)