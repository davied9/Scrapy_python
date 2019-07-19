import requests
import re
from lxml import html


def routine_00():
    print("routine_00")
    req = requests.get("http://www.gamersky.com/")

    with open("gamersky.txt", "wb") as f:
        f.write(req._content)

def shell_entry():
    print("gamersky_pictures shell_entry")
    routine_00()
