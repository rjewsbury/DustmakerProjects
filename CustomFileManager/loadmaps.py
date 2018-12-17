import urllib, urllib.request as urllib2, time, re

url_raw = "http://atlas.dustforce.com/gi/downloader.php?id=%d"
dest_dir = "C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/%s"


def download_map(id, dir=dest_dir, debug=False):
    url = url_raw % id
    url_data = urllib2.urlopen(url)
    headers = url_data.info()
    if debug: print(headers)
    content = url_data.read()
    if debug: print(content)
    if content:
        name = re.search("filename=\"(.*?)\"", headers["content-disposition"])
        if name:
            name = name.group(1)
            map = urllib2.URLopener()
            map.retrieve(url, dir % name)
            if debug: print(id, name)
            return name
        else:
            if debug: print("error:\n", content.read())
    return None


def download_all(start, end=1000000, debug=False):
    blank_count = 0
    MAX_BLANKS = 5
    for i in range(start, end):
        success = download_map(i, debug=debug)
        if not success:
            # apparently, there are some IDs that do not have maps
            # the only thing I can do to know that I've reached the end
            # is to find enough empty IDs in a row
            blank_count += 1
            if blank_count > MAX_BLANKS:
                break
        else:
            blank_count = 0

if __name__ == '__main__':
    download_all(8315, debug=True)