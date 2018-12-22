import urllib.request as url
import ssl
import re
import json

_default_dir = "C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/%s"

# currently a dead link
stats_url = "https://dustkid.com/backend8/dustmod_getstats.php?user=%d"

_default_user_id = 76378

# html page that I can kind of parse
stats_custom_url = "https://dustkid.com/profilecustom/%d/"
stats_apple_url = "https://dustkid.com/profilecustom/%d//apple"

_default_custom = _default_dir % "_custom_stats.html"
_default_apple = _default_dir % "_apple_stats.html"

config_file = './_config.json'
try:
    with open(config_file, 'r') as f:
        config_dict = json.load(f)
except FileNotFoundError:
    config_dict = {}
custom_file = config_dict.get('rank_file', _default_custom)
apple_file = config_dict.get('apple_rank_file', _default_apple)


def download_stat_files(**kwargs):
    user_id = kwargs.get('user_id', _default_user_id)
    load_custom = kwargs.get('generate_rank_file', True)
    load_apples = kwargs.get('generate_apple_rank_file', True)

    if load_custom:
        data = url.urlopen(stats_custom_url % user_id, context=ssl._create_unverified_context())
        with open(custom_file, 'w+') as f:
            f.write(data.read().decode('utf-8'))
    if load_apples:
        data = url.urlopen(stats_apple_url % user_id, context=ssl._create_unverified_context())
        with open(apple_file, 'w+') as f:
            f.write(data.read().decode('utf-8'))


def get_rank(level_name):
    with open(custom_file, 'r') as f:
        data = f.read()
        m = re.search(r"<tr><td><a href='/level/"+level_name+r".*?</tr>", data, re.IGNORECASE)
        line = m.group(0)
    if 'N/A' in line:
        return None
    rank = ''.join(re.search(r'score score(.).*?score score(.)', line).groups())

    return rank


def get_apple_rank(level_name):
    with open(apple_file, 'r') as f:
        data = f.read()
        m = re.search(r"<tr><td><a href='/level/" + level_name + r".*?</td>", data, flags=re.IGNORECASE)
        line = m.group(0)
    if 'N/A' in line:
        return None, None
    rank = ''.join(re.search(r'score score(.).*?score score(.)', line).groups())

    apple_m = re.search(r"<img src='/static/iconApple.png' style='height: 1em;'/> x(\S+)", line)
    if apple_m is not None:
        apple_count = int(apple_m.group(1))
    else:
        apple_count = re.findall(r"<img src='/static/iconApple.png' style='height: 1em;'/>", line)
        apple_count = len(apple_count)

    return rank, apple_count


if __name__ == '__main__':
    # this is an expensive call. avoid updating when possible
    # download_stat_files()

    #test output
    print(get_rank('Dustless-Realm-4864'))
    print(get_apple_rank('Dustless-Realm-4864'))
    print()
    print(get_rank('Dont-Think-About-It-8832'))
    print(get_apple_rank('Dont-Think-About-It-8832'))
    print()
    print(get_rank('appletainment-7294'))
    print(get_apple_rank('appletainment-7294'))
    print()
    print(get_rank('Traksu-Lita-0061-3665'))
    print(get_apple_rank('Traksu-Lita-0061-3665'))