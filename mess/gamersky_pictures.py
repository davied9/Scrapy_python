#-*-coding:utf-8-*-
import requests
import os
import re
import time
from lxml import html
from lxml import etree
# from selenium.webdriver.common.touch_actions import TouchActions
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common import desired_capabilities
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
from selenium import webdriver


def routine_00():
    print("routine_00")
    game_zone = "watchdogs2" # "thewitcher3"
    encoding  = 'utf-8'
    save_dir = 'test'
    print("starting download wallpapers for game zone {}".format(game_zone))
    if False:
        proxies = {
            "http" : "socks5h://127.0.0.1:1080",
            "https" : "socks5h://127.0.0.1:1080"
        }
        print("using proxy {}".format(proxies))
    else:
        proxies = {}


    # check coding
    time.sleep(0.5)
    req = requests.get("https://www.gamersky.com/z/{}/".format(game_zone), proxies=proxies, verify=False)
    # with open("gamersky.txt", "wb") as f:
    #     f.write(req._content)
    tree = html.fromstring(req._content.decode(encoding))
    req.close()
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
    print("  found 图库 at {}".format(picture_library_url))

    # find 壁纸
    time.sleep(0.5)
    req = requests.get(picture_library_url, proxies=proxies, verify=False)
    tree = html.fromstring(req._content.decode(encoding))
    req.close()
    # with open("gamersky.txt", "wb") as f:
    #     f.write(req._content)
    node = tree.xpath("//body//div[@class='topnav']/a/b[text()='壁纸']")[0]
    wallpaper_url = node.xpath("../@href")[0]
    print("  found 壁纸 at {}".format(wallpaper_url))

    # save all wallpapers
    time.sleep(0.5)
    # req = requests.get(wallpaper_url, proxies=proxies, verify=False)
    # with open("gamersky.txt", "wb") as f:
    #     f.write(req._content)

    browser = webdriver.Chrome()
    browser.implicitly_wait(2)

    browser.get(wallpaper_url)
    last_figure_count = -1
    figure_count = 0
    get_out_counter = 0

    while get_out_counter < 3:
        if figure_count == last_figure_count:
            get_out_counter += 1
        else:
            get_out_counter = 0
        last_figure_count = figure_count
        time.sleep(0.2)

        # action.scroll(0, 5) # this will not take effect for PC
        browser.execute_script("window.scrollBy(0, 3000)") # scroll with javascript

        # # we can find nodes with xpath, but this can not continue the interactive within browser
        # # innerHTML = browser.execute_script("return document.body.innerHTML") # get page source with javascript
        # innerHTML = browser.page_source
        # req = html.fromstring(innerHTML)
        # nodes = req.xpath("//a[@class='picbtn']")

        # so we use selenium for the searching, xpath or class name is OK
        # nodes = browser.find_elements_by_class_name("picbtn") # we can find all elements with just class name specified
        buttons = browser.find_elements_by_xpath("//a[@class='picbtn']") # or with xpath

        figure_count = len(buttons)
        print("\r  [{}] found {} images ...".format(get_out_counter, figure_count), end="", flush=True)

    # with open("gamersky.txt", "wb") as f:
    #     f.write(innerHTML.encode('utf-8'))

    if figure_count > 0:
        print("  found {} images, start saving ...".format(figure_count))
        image_root = os.path.join(save_dir, game_zone)
        if not os.path.exists(image_root):
            os.makedirs(image_root)
        image_index = 0
        for button in buttons:
            browser.switch_to.window(window_name=browser.window_handles[0])
            button.click()
            browser.switch_to.window(window_name=browser.window_handles[-1])
            innerHTML = browser.page_source
            browser.close()

            tree = html.fromstring(innerHTML)
            image_full_url = tree.xpath("//div[@class='Bimg']/div[@class='li block']/a/@href")[0]
            image_clean_url = re.findall(r"(?<=shtml\?).*", image_full_url)[0]
            image_format_postfix = re.findall(r"\.\w+$", image_clean_url)[0][1:]

            req = requests.get(image_clean_url, stream=True)
            image_path = os.path.join(image_root, 'image_{:03}.{}'.format(image_index, image_format_postfix))
            print("    saving {}".format(image_clean_url))
            print("        to {}".format(image_path))
            with open(image_path, 'wb') as f:
                for chunk in req:
                    f.write(chunk)

            image_index += 1
            time.sleep(0.2)

    browser.switch_to.window(window_name=browser.window_handles[0])
    browser.close()

def routine_01(): # console print test
    print("routine_01 : console print test")
    print("first test message", end=" ")
    print("third test message", end="", flush=True)
    print("second test message", end="\n")
    for i in range(20):
        print("\r", end="")
        occ = i % 5
        left = 4 - occ
        print("[", end="")
        for j in range(occ):
            print("=", end="")
        for j in range(left):
            print(" ", end="")
        print("] this is high", end="", flush=True)
        time.sleep(0.5)

def shell_entry():
    print("gamersky_pictures shell_entry")
    routine_00()
