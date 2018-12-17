import os
import urllib.request as url
from enum import IntEnum

BASE = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/'
read_sub = '' #'noflag/'
website = 'https://atlas.dustforce.com/%s/%s'

class Published(IntEnum):
    UNKNOWN = 0
    UNPUBLISHED = 1
    HIDDEN = 2
    VISIBLE = 3

def get_published_status(map_name, dir=BASE):
    name_split = list(map_name.rsplit('-',1))
    name = name_split[0]
    num = name_split[1]
    try:
        data = url.urlopen(website%(num,name))
        # There's no definite way to tell if a map is published,
        # but if the name is not visible, that probably means the map is not visible
        if r'<meta property="og:title" content=" - a Dustforce map" >' in str(data.read()):
            return Published.HIDDEN
        else:
            return Published.VISIBLE
    except:
        return Published.UNPUBLISHED

if __name__ == '__main__':
    for map_name in os.listdir(BASE+read_sub):
        try:
            status = get_published_status(map_name)
            print(map_name, Published(status).name)
        except:
            print(map_name, '---------------------------------------------------------------')
            continue
        if status == Published.HIDDEN:
            os.rename(BASE + read_sub + map_name, BASE + 'hidden/' + map_name)
        elif status == Published.UNPUBLISHED:
            os.rename(BASE + read_sub + map_name, BASE + 'nonpublished/' + map_name)
