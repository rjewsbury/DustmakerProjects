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


def get_level_candidates(level_dict, **kwargs):
    has_end = kwargs.get('has_end', True)
    completed = kwargs.get('completed', None)
    ss = kwargs.get('ss', None)
    playable_type = kwargs.get('playable_type', True)
    ssable = kwargs.get('ssable', True)
    ss_difficult = kwargs.get('ss_difficult', None)
    name_search = kwargs.get('name_search', None)
    has_apples = kwargs.get('has_apples', None)
    apple_completed = kwargs.get('apple_completed', None)
    apple_ss = kwargs.get('apple_ss', None)
    apple_ssable = kwargs.get('apple_ssable', None)
    apple_ss_difficult = kwargs.get('apple_ss_difficult', None)
    
    candidates = []
    for key in level_dict:
        info = level_dict[key]
        valid = True
        valid = valid and (has_end is None or has_end == info.get('has_end', False))
        valid = valid and (completed is None or completed == (info.get('rank', None) is not None))
        valid = valid and (name_search is None or (name_search.lower() in info['filename'].lower()))
        valid = valid and valid_published_status(info.get('published', Published.UNKNOWN), **kwargs)
        valid = valid and (ss is None or ss == (info.get('rank', None) == 'SS'))
        valid = valid and (ssable is None or ssable == (info.get('has_end', False) and 'ss_impossible' not in info))
        valid = valid and (ss_difficult is None or ss_difficult == ('ss_difficult' in info))
        valid = valid and (playable_type is None or playable_type ==
                           (info.get('level_type', LevelType.NEXUS) in (LevelType.NORMAL, LevelType.DUSTMOD)))
        valid = valid and (has_apples is None or has_apples == (info.get('apples', 0) != 0))
        valid = valid and (apple_completed is None or apple_completed == (info.get('apple_rank', None) is not None))
        valid = valid and (apple_ss is None or apple_ss == has_apple_ss(info))
        valid = valid and (apple_ssable is None or apple_ssable ==
                           (info.get('has_end', False) and info.get('apples', 0) != 0
                            and 'ss_impossible' not in info and 'apple_ss_impossible' not in info))
        valid = valid and (apple_ss_difficult is None or apple_ss_difficult ==
                           ('ss_difficult' in info or 'apple_ss_difficult' in info))
        if valid:
            candidates.append(key)
    return candidates


def pick_level(candidates=None, **kwargs):
    choose_newest = kwargs.get('choose_newest', False)
    if candidates is None and kwargs is None:
        return None
    try:
        if candidates is None:
            candidates = get_level_candidates(**kwargs)
        if choose_newest:
            candidates.sort(key=lambda x: int(x))
            return candidates[-1]
        else:
            return random.choice(candidates)
    except IndexError:
        return None


def valid_published_status(status, **kwargs):
    valid = False
    valid = valid or (kwargs.get('allow_hidden', False) and status == Published.HIDDEN)
    valid = valid or (kwargs.get('allow_unpublished', False) and status == Published.UNPUBLISHED)
    valid = valid or (kwargs.get('allow_unknown', False) and status == Published.UNKNOWN)
    valid = valid or (kwargs.get('allow_visible', True) and status == Published.VISIBLE)
    return valid


def has_apple_ss(info):
    apples = info.get('apples', 0)
    rank = info.get('apple_rank', None)
    count = info.get('hit_apples', 0)
    # Refresh-7946 has infinite apples, so the count is higher than the actual number
    return (rank == 'SS') and apples <= count


def launch(filename):
    if filename is None:
        return
    name, num = filename.rsplit('-', 1)
    webbrowser.open('dustforce://installPlay/%s/%s' % (num, name))


def dustkid_link(filename):
    return dustkid % filename.replace(' ', '%20')


def atlas_link(filename):
    name, num = filename.rsplit('-', 1)
    return atlas % (num, name)


class Result(IntEnum):
    EXIT = 0,
    NEXT = 1,
    SS = 2,
    SS_DIFFICULT = 3,
    SS_IMPOSSIBLE = 4,
    APPLE_SS = 5,
    APPLE_SS_DIFFICULT = 6,
    APPLE_SS_IMPOSSIBLE = 7,


def process_command(command, info, reason=None):
    if command == Result.SS:
        info['rank'] = 'SS'
    elif command == Result.SS_DIFFICULT:
        if 'ss_impossible' in info:
            del info['ss_impossible']
        if reason is None: reason = input('Reason?: ')
        info['ss_difficult'] = reason
    elif command == Result.SS_IMPOSSIBLE:
        if 'ss_difficult' in info:
            del info['ss_difficult']
        if reason is None: reason = input('Reason?: ')
        info['ss_impossible'] = reason
    elif command == Result.APPLE_SS:
        info['rank'] = 'SS'
        info['apple_rank'] = 'SS'
        info['hit_apples'] = info.get('apples', 0)
    elif command == Result.APPLE_SS_DIFFICULT:
        if 'apple_ss_impossible' in info:
            del info['apple_ss_impossible']
        if reason is None: reason = input('Reason?: ')
        info['apple_ss_difficult'] = reason
    elif command == Result.APPLE_SS_IMPOSSIBLE:
        if 'apple_ss_difficult' in info:
            del info['apple_ss_difficult']
        if reason is None: reason = input('Reason?: ')
        info['apple_ss_impossible'] = reason
    return info


def main(**kwargs):
    auto_launch = kwargs.get('auto_launch', False)
    with open(dest_dir % index_file, 'r') as f:
        level_dict = json.load(f)
    command = 1
    candidates = get_level_candidates(level_dict, **kwargs)
    while command != 0:
        key = pick_level(candidates, **kwargs)

        if key is None:
            print('No level matches this criteria')
            command = 0
        else:
            info = level_dict[key]
            candidates.remove(key)
            for data in info:
                print('%s: %s' % (data, str(info[data])))
            print(dustkid_link(info['filename']))
            if auto_launch:
                launch(info['filename'])
            print()
            for res in Result:
                print(int(res), '=', res.name)
            command = -1
            while command < 0:
                try: command = int(input('Result?: '))
                except Exception: pass
            info = process_command(command, info)
            level_dict[key] = info
    with open(dest_dir % index_file, 'w') as f:
        json.dump(level_dict, f, indent=4)


if __name__ == '__main__':
    SS_search = {
        'ss': False,
        'ssable': True,
        'choose_newest': True,
        'ss_difficult': False}
    appleSS = {
        'ss': True,
        'apple_ssable': True,
        'apple_ss': False,
        'choose_newest': True,
        'apple_ss_difficult': False
    }
    impossible = {
        'has_end': True,
        'ssable': False,
        'choose_newest': True
    }
    impossible_apple = {
        'has_end': True,
        'has_apples': True,
        'apple_ssable': False,
        'choose_newest': True
    }
    main(**appleSS)
