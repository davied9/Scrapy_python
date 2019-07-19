#-*-coding:utf-8-*-
import requests
import re
from lxml import etree
from lxml import html
try:
    from StringIO import StringIO # python 2
except ImportError:
    from io import StringIO # python 3



def routine_00():
    print("routine_00")
    req = requests.get("http://quotes.toscrape.com/page/1/")
    with open('out_quotes.txt', 'wb') as f: # not recommend write as characters, may cause problems
        f.write(req._content)
    # r = etree.XML(req.text) # XML can't parse correctly, use html instead
    # r = etree.parse('out_quotes.txt')
    res = html.fromstring(req.text) # use html instead of XML, cause there is syntax problem
    tar = res.xpath('//div[@class="quote"]/span[@class="text"]/text()') # for quote
    with open('res_quotes.txt', 'wb') as f:
        for t in tar:
            f.write((t + '\n').encode('utf-8')) # encode before write to binary file

    req = requests.get("https://book.douban.com/#")
    with open('out_douban.txt', 'wb') as f:
        f.write(req._content)
    res = html.fromstring(req.text)
    # titles = res.xpath('//div[@class="section books-express "]//div[@class="info"]/div[@class="cover"]/@title')
    titles = res.xpath('//div[@class="section books-express "]//div[@class="info"]/div[@class="title"]/a/text()')
    authors = res.xpath('//div[@class="section books-express "]//div[@class="info"]/div[@class="author"]/text()')
    with open('res_douban.txt', 'wb') as f:
        f.write('{:60}{}\n'.format('author', 'book').encode('utf-8'))
        for i in range(len(titles)):
            author = authors[i].strip()
            f.write('{:60}'.format(author).encode('utf-8'))
            title = titles[i].strip()
            f.write('{}'.format(title).encode('utf-8'))
            f.write('\n'.encode('utf-8'))

def routine_01():
    print("routine_01")
    with open('out.txt', 'rb') as f:
        bin = f.read()
        content = bin.decode('utf-8')
    print('re-loaded :\n', content[0:100])
    #res = re.findall(r'')
    # <div class="section books-express ">
    # </div>

def routine_02():
    print("routine_02")
    content = '''
<html>
    <body>
        <div class = "entry">
            <a href="/login">Login</a>
        </div>
        <div class = "quote">
            <title>Quotes to Scrape</title>
        </div>
    </body>
</html>
'''
    f = StringIO(content) # manipulate string as file stream
    tree = etree.parse(f) # etree.parse used to parse xml file/stream
    r = tree.xpath('/html/body/div') # got 2 nodes named div
    r = tree.xpath('/html/body/div/@class') # got node div's attribute 'class' := ['entry', 'quote']
    r = tree.xpath('/html/body/div[@class="quote"]') # got node div whose attribute 'class' have value "quote"
    r = tree.xpath('/html/body/div/title')
    print(r)

def routine_03():
    print("routine_03")
    content = '''
<html>
    <body>
        <div class = "entry">
            <a href="/login">Login</a>
        </div>
        <div class = "quote">
            <title>Quotes to Scrape</title>
        </div>
    </body>
</html>
'''
    tree = etree.XML(content) # create xml from string
    r = tree.xpath('/html/body/div/title/text()') # get title's text := "Quotes to Scrape"
    r = tree.xpath('/html/body/div/para()')
    print(r)

def shell_entry():
    print("first_try shell_entry")
    routine_00()

