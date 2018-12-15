import urllib, urllib.request as urllib2, time, re

url_raw = "http://atlas.dustforce.com/gi/downloader.php?id=%d"

for i in range(6913 ,8245): #6913
    url = url_raw % i
    url_data = urllib2.urlopen(url_raw % i)
    headers = url_data.info()
    content = url_data.read()
    if content:
        name = re.search("filename=\"(.*?)\"", headers["content-disposition"])
        if name:
            name = name.group(1)
            map = urllib2.URLopener()
            map.retrieve(url_raw % i, "maps/%s" % name)
            print(i, name)
        else:
            print("error:\n", content.read())
    time.sleep(1)