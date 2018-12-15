import os
import urllib.request as url

BASE = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/'
read_sub = 'noflag/'
website = 'https://atlas.dustforce.com/%s/%s'

for map_name in os.listdir(BASE+read_sub):
    pass
    try:
        name_split = list(map_name[::-1].split('-',1))
        name = name_split[1][::-1]
        num = name_split[0][::-1]
        print(name,num)
    except:
        print(map_name, '---------------------------------------------------------------')
        continue

    try:
        data = url.urlopen(website%(num,name))
        if('Undefined' in str(data.read())):
            print('HIDDEN')
            os.rename(BASE + read_sub + map_name, BASE + 'hidden/' + map_name)
        else:
            print("OK")
    except:
        print('UNPUBLISHED')
        os.rename(BASE + read_sub + map_name, BASE + 'nonpublished/' + map_name)
