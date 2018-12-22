import os
import time
import json
import traceback
from timeit import default_timer
from dustmaker.MapReader import read_map
from dustmaker import LevelType
from CustomFileManager.loadmaps import download_map
from CustomFileManager.level_stats import get_rank, get_apple_rank
from CustomFileManager.publishedsort import Published, get_published_status

_default_dir = "C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/"
_default_index = _default_dir + '_level_index.json'

config_file = './_config.json'
try:
    with open(config_file, 'r') as f:
        config_dict = json.load(f)
except FileNotFoundError:
    config_dict = {}
dest_dir = config_dict.get('level_dir', _default_dir) + '/%s'
index_file = config_dict.get('index_file', _default_index)


def level_id(name):
    try:
        return int(name.split('-')[-1])
    except Exception:
        return -1


def get_name_list(**kwargs):
    load_extended = kwargs.get('load_extended', False)
    load_missing = kwargs.get('load_missing', False)
    reload_existing = kwargs.get('reload_existing', False)
    lower_bound = kwargs.get('lower_bound', 0)
    upper_bound = kwargs.get('upper_bound', 1000000000)
    min_missing_id = kwargs.get('min_missing_id', 93)
    # level IDs 0 - 92 do not exist on atlas

    existing = list(os.listdir(dest_dir % ''))

    existing.sort(key=level_id)
    max_id = level_id(existing[-1])
    existing_index = 0
    while level_id(existing[existing_index]) < lower_bound:
        existing_index += 1

    # insert None's so that level IDs match with index
    levels = [None]*(max_id+1)
    for i in range(lower_bound, min(upper_bound,max_id+1)):
        existing_id = level_id(existing[existing_index])
        if (min_missing_id <= i < existing_id) and load_missing:
            level_name = download_map(i,dest_dir)
            print('Missing map id %d. Loaded = %s' % (i, str(level_name)))
            levels[i] = level_name
            time.sleep(1)
        elif i == existing_id:
            if reload_existing:
                level_name = download_map(i,dest_dir)
                print('Reloading map id %d. Loaded = %s' % (i, str(level_name)))
                time.sleep(1)
                if level_name is not None and level_name != existing[existing_index]:
                    existing[existing_index].insert(existing_index, level_name)

            levels[i] = existing[existing_index]

            prev_id = existing_id
            existing_index += 1
            if existing_index < len(existing):
                existing_id = level_id(existing[existing_index])
                while prev_id == existing_id:
                    print('Error: matching level ID [%s] [%s]'%(existing[existing_index-1], existing[existing_index]))
                    existing_index += 1
                    existing_id = level_id(existing[existing_index])

    #check for new maps after the last ID
    if load_extended and upper_bound > max_id+1:
        blank_count = 0
        MAX_BLANKS = 5
        for i in range(max_id+1,upper_bound):
            name = download_map(i)
            if not name:
                levels.append(None)
                blank_count += 1
                if blank_count > MAX_BLANKS:
                    break
            else:
                levels.append(name)
                blank_count = 0

    # remove trailing None's
    while levels[-1] is None:
        del levels[-1]

    return levels


def get_info(filename, **kwargs):
    info = {'filename': filename}
    return add_info(info, **kwargs)


def add_info(info, **kwargs):
    add_map = kwargs.get('add_map', True)
    add_ranks = kwargs.get('add_ranks', True)
    add_apple_ranks = kwargs.get('add_apple_ranks', False)
    add_published = kwargs.get('add_published', False)
    debug = kwargs.get('debug', False)

    if debug:
        start = default_timer()

    filename = info['filename']
    if debug: print(filename)

    # if the map is not even readable, there's no point in looking at the rest of the data
    # checks before map info just in case info has been generated before
    if not info.get('readable', True):
        return info

    if add_map:
        add_map_info(info, debug)

    # double check if its readable after the map info is generated
    if not info.get('readable', True):
        return info

    if add_published:
        add_published_info(info, debug)

    if add_ranks:
        add_rank_info(info, add_apple_ranks, debug)

    if debug:
        end = default_timer()
        print('\tprocess time =%.2f'%(end-start))

    return info


def add_map_info(info, debug=False):
    filename = info['filename']
    try:
        with open(dest_dir % filename, "rb") as f:
            map = read_map(f.read())
        info['readable'] = True
    except:
        print('Error: could not read', filename)
        info['readable'] = False
        return info

    info['level_type'] = map.level_type()
    if debug: print('\tlevelType:',LevelType(info['level_type']).name)

    info['has_end'] = False
    info['apples'] = 0
    for key in map.entities:
        if map.entities[key][2].type in ('level_end', 'level_end_prox'):
            info['has_end'] = True
        if map.entities[key][2].type == 'hittable_apple':
            info['apples'] += 1
    if debug: print('\thasEnd:', info['has_end'])
    if debug: print('\tnumApples:', info['apples'])
    return info


def add_rank_info(info, add_apple_rank=True, debug=False):
    filename = info['filename']
    if info.get('has_end', False):
        try:
            info['rank'] = get_rank(filename)
            if debug: print('\trank:', info['rank'])

            if add_apple_rank and (info.get('apples', 0) > 0):
                apple_rank, apple_count = get_apple_rank(filename)
                info['apple_rank'] = apple_rank
                info['hit_apples'] = apple_count
                if debug: print('\tappleRank:', info['apple_rank'], info['hit_apples'])
        except Exception:
            print('Error: could not load ranks for',filename)
    return info


# this is separated because it's an expensive operation
def add_published_info(info, debug=False):
    info['published'] = get_published_status(info['filename'])
    if debug: print('\tpublished:', Published(info['published']).name)
    return info


def create_complete_index():
    levels = get_name_list(load_extended=True, load_missing=True)
    level_dict = {}
    for i, name in enumerate(levels):
        if name is not None:
            try:
                level_dict[i] = get_info(name, add_published=True)
            except Exception as err:
                print('Error: could not process level', levels[i])
                print(traceback.format_exc())
                print()
        if i % 100 == 0:
            print('\tprocessed', i, name)

    with open(index_file, 'w+') as f:
        json.dump(level_dict, f, indent=4)


def update_index(already_indexed_args={}, **kwargs):
    min_id = kwargs.get('lower_bound', 0)
    max_id = kwargs.get('upper_bound', 1000000000)

    try:
        with open(index_file, 'r') as f:
            level_dict = json.load(f)
    except FileNotFoundError:
        level_dict = {}

    levels = get_name_list(**kwargs)
    for i in range(min_id, min(max_id, len(levels))):
        if levels[i] is not None:
            try:
                if str(i) not in level_dict:
                    level_dict[str(i)] = get_info(levels[i], **kwargs)
                else:
                    level_dict[str(i)] = add_info(level_dict[str(i)], **already_indexed_args)
            except Exception as err:
                print('Error: could not process level', levels[i])
                print(traceback.format_exc())
                print()

        if i % 100 == 0:
            print('\tprocessed', i, levels[i])

    with open(index_file, 'w+') as f:
        json.dump(level_dict, f, indent=4)

if __name__ == '__main__':
    kwargs = {
        'load_extended': True,
        'load_missing': True,
        'add_published': True
    }
    already_indexed_args = {
        'add_map': False
    }
    update_index(already_indexed_args, **kwargs)
