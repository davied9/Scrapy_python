import requests
import re


def routine_00():
    print("routine_00")
    # r = requests.get("https://book.douban.com/#")
    r = requests.get("http://quotes.toscrape.com/page/1/")

    content = r._content.decode('utf-8')
    #print('r :\n', content[0:10])

    with open('out.txt', 'wb') as f:
        f.write(r._content)

def routine_01():
    print("routine_01")
    with open('out.txt', 'rb') as f:
        bin = f.read()
        content = bin.decode('utf-8')
    print('re-loaded :\n', content[0:100])
    #res = re.findall(r'')
    # <div class="section books-express ">
    # </div>

def shell_entry():
    print("first_try shell_entry")
    routine_00()

