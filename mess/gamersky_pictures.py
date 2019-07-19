#-*-coding:utf-8-*-
import requests
import re
import time
from lxml import html


def routine_00():
    print("routine_00")
    game_zone = "thewitcher3"
    encoding  = 'utf-8'
    save_dir = ''
    if True:
        proxies = {
            "http" : "socks5h://127.0.0.1:1080",
            "https" : "socks5h://127.0.0.1:1080"
        }
    else:
        proxies = {}

    # check coding
    time.sleep(0.5)
    req = requests.get("https://www.gamersky.com/z/{}/".format(game_zone), proxies=proxies, verify=False)
    # with open("gamersky.txt", "wb") as f:
    #     f.write(req._content)
    tree = html.fromstring(req._content.decode(encoding))
    meta = tree.xpath("//head/meta[contains(@content, 'charset')]/@content")[0]
    charset_match = re.findall(r'charset=[\w\-]+', meta)[0]
    web_encoding = charset_match[len('charset='):]
    print("  default request encoding : {}".format(req.encoding))
    print("  parsing encoding : {}".format(encoding))
    print("  website encoding : {}".format(web_encoding))
    if encoding != web_encoding:
        print("  encoding check failed.")
        return

    # find 图库
    node = tree.xpath("//body/div[@class='center']//ul[@class='nav']/li/a[text()='图库']")[0]
    picture_library_url = node.xpath("@href")[0]
    print("  图库 {}".format(picture_library_url))

    # find 壁纸
    time.sleep(0.5)
    req = requests.get(picture_library_url, proxies=proxies, verify=False)
    tree = html.fromstring(req._content.decode(encoding))
    # with open("gamersky.txt", "wb") as f:
    #     f.write(req._content)
    node = tree.xpath("//body//div[@class='topnav']/a/b[text()='壁纸']")[0]
    wallpaper_url = node.xpath("../@href")[0]
    print("  壁纸 {}".format(wallpaper_url))

    # save all wallpapers
    time.sleep(0.5)
    req = requests.get(wallpaper_url, proxies=proxies, verify=False)
    with open("gamersky.txt", "wb") as f:
        f.write(req._content)



def shell_entry():
    print("gamersky_pictures shell_entry")
    routine_00()
