import urllib.request as url
import ssl
import re

dest_dir = "C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/%s"

# currently a dead link
stats_url = "https://dustkid.com/backend8/dustmod_getstats.php?user=%d"

user_id = 76378

# html page that I can kind of parse
stats_custom_url = "https://dustkid.com/profilecustom/%d/"%user_id
stats_apple_url = "https://dustkid.com/profilecustom/%d//apple"%user_id

dest_custom = "_custom_stats.html"
dest_apple = "_apple_stats.html"


def download_stat_files():
    data = url.urlopen(stats_custom_url, context=ssl._create_unverified_context())
    with open(dest_dir % dest_custom, 'w+') as f:
        f.write(data.read().decode('utf-8'))
    data = url.urlopen(stats_apple_url, context=ssl._create_unverified_context())
    with open(dest_dir % dest_apple, 'w+') as f:
        f.write(data.read().decode('utf-8'))


def get_rank(level_name):
    with open(dest_dir % dest_custom, 'r') as f:
        data = f.read()
        m = re.search(r"<tr><td><a href='/level/"+level_name+r".*?</tr>", data, re.IGNORECASE)
        line = m.group(0)
    if 'N/A' in line:
        return None
    rank = ''.join(re.search(r'score score(.).*score score(.)', line).groups())

    return rank

def get_apple_rank(level_name):
    with open(dest_dir % dest_apple, 'r') as f:
        data = f.read()
        m = re.search(r"<tr><td><a href='/level/" + level_name + r".*?</td>", data, flags=re.IGNORECASE)
        line = m.group(0)
    if 'N/A' in line:
        return None, None
    rank = ''.join(re.search(r'score score(.).*score score(.)', line).groups())

    apple_m = re.search(r"<img src='/static/iconApple.png' style='height: 1em;'/> x(.)", line)
    if apple_m is not None:
        apple_count = int(apple_m.group(1))
    else:
        apple_count = re.findall(r"<img src='/static/iconApple.png' style='height: 1em;'/>", line)
        apple_count = len(apple_count)

    return rank, apple_count



if __name__ == '__main__':
    # this is an expensive call. avoid updating when possible
    download_stat_files()

    #test output
    print(get_rank('Dustless-Realm-4864'))
    print(get_apple_rank('Dustless-Realm-4864'))
    print()
    print(get_rank('Contrast-161'))
    print(get_apple_rank('Contrast-161'))
    print()
    print(get_rank('zen-5241'))
    print(get_apple_rank('zen-5241'))
    print()
    print(get_rank('Traksu-Lita-0061-3665'))
    print(get_apple_rank('Traksu-Lita-0061-3665'))