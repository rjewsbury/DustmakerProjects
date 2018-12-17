import webbrowser
import json
import random
from enum import IntEnum

from CustomFileManager.publishedsort import Published
from dustmaker import LevelType

dest_dir = "C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/%s"
index_file = '_level_index.json'
atlas = 'https://atlas.dustforce.com/%s/%s'
dustkid = 'https://dustkid.com/level/%s/all/0'


def pick_level(level_dict, ss=None, playable_type=True, ssable=True, ss_difficult=None, name_search=None,
               allow_hidden=False, allow_unpublished=False, allow_unknown=False, allow_visible=True,
               has_apples=None, apple_ss=None, apple_ssable=None, apple_ss_difficult=None):
    candidates = []
    for key in level_dict:
        info = level_dict[key]
        valid = True
        valid = valid and (name_search is None or (name_search.lower() in info['filename'].lower()))
        valid = valid and valid_published_status(info.get('published', Published.UNKNOWN),
                                                 allow_hidden, allow_unpublished, allow_unknown, allow_visible)
        valid = valid and (ss is None or ss == (info.get('rank', 'DD') == 'SS'))
        valid = valid and (ssable is None or ssable == (info.get('has_end', False) and 'ss_impossible' not in info))
        valid = valid and (ss_difficult is None or ss_difficult == ('ss_difficult' in info))
        valid = valid and (playable_type is None or playable_type ==
                           (info.get('level_type', LevelType.NEXUS) in (LevelType.NORMAL, LevelType.DUSTMOD)))
        valid = valid and (has_apples is None or has_apples == (info.get('apples', 0) != 0))
        valid = valid and (apple_ss is None or apple_ss == has_apple_ss(info))
        valid = valid and (apple_ssable is None or apple_ssable ==
                           (info.get('has_end', False) and info.get('apples', 0) != 0
                            and 'ss_impossible' not in info and 'apple_ss_impossible' not in info))
        valid = valid and (apple_ss_difficult is None or apple_ss_difficult ==
                           ('ss_difficult' in info or 'apple_ss_difficult' in info))
        if valid:
            candidates.append(key)
    try:
        return random.choice(candidates)
    except IndexError:
        return None


def valid_published_status(status, allow_hidden=False, allow_unpublished=False,
                           allow_unknown=False, allow_visible=True):
    valid = False
    valid = valid or (allow_hidden and status == Published.HIDDEN)
    valid = valid or (allow_unpublished and status == Published.UNPUBLISHED)
    valid = valid or (allow_unknown and status == Published.UNKNOWN)
    valid = valid or (allow_visible and status == Published.VISIBLE)
    return valid


def has_apple_ss(info):
    apples = info.get('apples', 0)
    rank = info.get('apple_rank', 'DD')
    count = info.get('hit_apples', 0)
    return (rank == 'SS') and apples == count


def launch(filename):
    name, num = filename.rsplit('-', 1)
    webbrowser.open('dustforce://installPlay/%s/%s' % (num, name))


def dustkid_link(filename):
    return dustkid % filename


def atlas_link(filename):
    name, num = filename.rsplit('-', 1)
    return atlas % (num,name)


class Result(IntEnum):
    EXIT = 0,
    NEXT = 1,
    SS = 2,
    SS_DIFFICULT = 3,
    SS_IMPOSSIBLE = 4,
    APPLE_SS = 5,
    APPLE_SS_DIFFICULT = 6,
    APPLE_SS_IMPOSSIBLE = 7,


def process_command(command, info):
    if command == Result.SS:
        info['rank'] = 'SS'
    elif command == Result.SS_DIFFICULT:
        if 'ss_impossible' in info:
            del info['ss_impossible']
        info['ss_difficult'] = input('Reason?: ')
    elif command == Result.SS_IMPOSSIBLE:
        if 'ss_difficult' in info:
            del info['ss_difficult']
        info['ss_impossible'] = input('Reason?: ')
    elif command == Result.APPLE_SS:
        info['rank'] = 'SS'
        info['apple_rank'] = 'SS'
        info['hit_apples'] = info.get('apples', 0)
    elif command == Result.APPLE_SS_DIFFICULT:
        if 'apple_ss_impossible' in info:
            del info['apple_ss_impossible']
        info['apple_ss_difficult'] = input('Reason?: ')
    elif command == Result.APPLE_SS_IMPOSSIBLE:
        if 'apple_ss_difficult' in info:
            del info['apple_ss_difficult']
        info['apple_ss_impossible'] = input('Reason?: ')
    return info


def main(auto_launch=False):
    with open(dest_dir % index_file, 'r') as f:
        level_dict = json.load(f)
    command = 1
    while command != 0:
        key = pick_level(level_dict)
        info = level_dict[key]
        if info is None:
            print('No level matches this criteria')
        else:
            for data in info:
                print('%s: %s' % (data, str(info[data])))
            print(dustkid_link(info['filename']))
            if auto_launch:
                launch(info['filename'])
            print()
            for res in Result:
                print(int(res), '=', res.name)
            command = int(input('Result?: '))
            info = process_command(command, info)
            level_dict[key] = info
    with open(dest_dir % index_file, 'w') as f:
        json.dump(level_dict, f, indent=4)

if __name__ == '__main__':
    main(True)
