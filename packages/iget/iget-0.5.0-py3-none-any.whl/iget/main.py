"""iget 0.5.0

Usage:
  iget <name> <limit> [options]

Options:
  -c            China
  -j            Japan
  -u            USA

"""

from docopt import docopt
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode
from sys import argv,exit
from os import path
import json

def get():
    arguments = docopt(__doc__)
    # name
    if arguments['<name>'] != "":
        term = arguments['<name>']
    
    # limit
    if arguments['<limit>'] != "":
        limit = arguments['<limit>']
    else:
        limit = "10"

    # country
    if arguments['-c'] == True:
        country = 'cn'
    elif arguments['-j'] == True:
        country = 'jp'
    elif arguments['-u'] == True:
        country = 'us'
    else:
        country = 'cn'

    base_url = 'https://itunes.apple.com/search?'
    parmas = {'term': term,
              'country': country,
              'media': 'software',
              'entity': 'software',
              'limit': limit}
    url = base_url + urlencode(parmas)
    response = urlopen(url)
    jsonObj = json.load(response)
    count = jsonObj["resultCount"]

    if count == 0:
        print("查无此项")
    else:
        for index, item in enumerate(jsonObj['results']):
            print("{} : {}".format(index, item["trackCensoredName"]))
        select_num = input("请输入要查找的项目(0到{}): ".format(index))
        size = ["60x60", "100x100", "512x512"]
        for index, item in enumerate(size):
            print("{} : {}".format(index, item))
        select_size = input("请选择要下载的大小(0到{}): ".format(index))
        image_link = jsonObj['results'][int(select_num)]["artworkUrl{}".format(size[int(select_size)].split("x")[0])]
        image_name = jsonObj['results'][int(select_num)]["trackCensoredName"]
        dir_desktop = path.expandvars('$HOME') + "/Desktop/"
        filename = "{}{}-{}.jpg".format(dir_desktop, image_name, size[int(select_size)])
        urlretrieve(image_link, filename=filename)
        print("🍺 下载完成")

def main():
    try:
        get()
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    main()