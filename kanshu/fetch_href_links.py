from bs4 import BeautifulSoup # a package for webstie data analysis

import urllib.request
from urllib.parse import urljoin
from urllib.parse import urlparse
import requests

import re # 正则表达式包，for cutting the punctuations
import time 
import random


# html_page=urllib.request.urlopen('./source.html')
# How to write the output to html file with Python BeautifulSoup
# 请求地址

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def countchn(string):
    pattern = re.compile(u'[\u1100-\uFFFDh]+?')
    result = pattern.findall(string)
    chnnum = len(result)            #list的长度即是中文的字数
    possible = chnnum/len(str(string))         #possible = 中文字数/总字数
    return (chnnum, possible)


def findtext(part):    
    length = 50000000
    l = []
    for paragraph in part:
        chnstatus = countchn(str(paragraph))
        possible = chnstatus[1]
        if possible > 0.65:         # 剔除标题行，描述行，还有上下翻页
            l.append(paragraph)
    l_t = l[:]
    #这里需要复制一下表，在新表中再次筛选，要不然会出问题，跟Python的内存机制有关
    for elements in l_t:
        chnstatus = countchn(str(elements))
        chnnum2 = chnstatus[0]
        if chnnum2 < 300:    
        #最终测试结果表明300字是一个比较靠谱的标准，低于300字的正文咱也不想要了对不
            l.remove(elements)
        elif len(str(elements))<length:
            length = len(str(elements))
            paragraph_f = elements
            return paragraph_f


def fetch_url_content(chapterUrl):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    try:
        request = urllib.request.Request(
            chapterUrl, headers=headers)
        response = urllib.request.urlopen(request, timeout=180)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    html = response.read().decode('gbk')
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')

   
    # Convert <br> to end line
    for br in soup.find_all("br"):
        br.replace_with("\n")


    # replace or remove HTML entities like “&nbsp;” using BeautifulSoup
    # replace the non-breaking space unicode with a normal space
    # https://stackoverflow.com/questions/15138406/how-can-i-replace-or-remove-html-entities-like-nbsp-using-beautifulsoup-4
    soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' '))

    # General case:
    # https://zhuanlan.zhihu.com/p/26192335 如何从任意HTML页面里提取正文？(Python3)
    # https://blog.csdn.net/robert_chen1988/article/details/105149263
    part = soup.select('div')
    div_box = findtext(part) # for predetect the div, contenxt > 300 words

    # Special case:  
    # only for the one website
    # specify the div which include the main content
    # div_box = soup.find('div', attrs={'class': 'DivPM6 Size14 BookReadconn'})


    #  Remove tags: <div>, <script>,  get the text part beneath a tag
    #  <div> hello </div> =>  hello
    divText= div_box.get_text().strip()

    return divText


def save_txt(title, content):
    filePath = './output_txt_files/'
    fileName = title

    # soup = BeautifulSoup(content, "lxml")  # 解析网页返回内容，lxml 是一个解码方式，效率比较快，被推荐使用
    # chapter_content = soup.select('.wenzhangziti')[0].get_text(separator="\n")  # select(.类名) 查找网页中的类，因为返回的是列表，所以跟 [0]
    # # chapter_content2 = soup.find_all('div', class_ = 'chapter_content')[0].text
    # chapter_content = chapter_content.lstrip()  # 去除左边的空格
    # chapter_content = chapter_content.rstrip()  # 去除右边的空格

    f  = open(filePath + fileName + '.txt', 'w', encoding='utf-8')
    f.write(str(content))
    f.close()



def main():
    soup = BeautifulSoup(open('./source.html'), "html.parser")
    chapterDict = {}

    for link in soup.findAll('a'):
        title = link.get('title')
        addr = link.get('href')
        chapterDict[title] = addr
        # print(title, addr)

    chapter_num = len(chapterDict)
    print('total chapters: ', chapter_num)

    # download chapter, save to txt file
    index = 0
    for key in chapterDict:
        index = index + 1
        try: 
            chapterTitle = key
            chapterUrl = chapterDict[key]
            chapterName = str(index) + '.' + chapterTitle
            print(chapterName,  '->', chapterUrl)

            chapterContent = fetch_url_content(chapterUrl)
            
            if chapterContent != None: 
                save_txt(chapterName, chapterContent)
            time.sleep(random.random() * 2)
        except AttributeError as e:
            print(e)
            break
        



if __name__ == '__main__':
    main()
    # testUrl = 'http://www.wakbook.com/Article/1x0000000004/109330x39269/STANZA_13.html'
    # content = fetch_url_content(testUrl)
    # print('content ', content)

'''
    html = response.read().decode('gbk')

    pattern = re.compile(
        '<table cellspacing="0" cellpadding="0"><tr><td class="t_msgfont" id="(.*?)"><font size="5">(.*?)</font></td></tr></table>', re.S)
    section_content = re.findall(pattern, html)

    # down txt
    try:
        fp = open('output.txt', 'w')
    except IOError as e:
        pattern = re.compile(
            '<font size="5">(.*?)</font><br />', re.S)
        # chapterTitle = re.findall(pattern, chapterTitle)
        # fp = open(section_name[0]+'.txt', 'w')
    print('start download')
    cleanTxt = cleanhtml(str(section_content))
    fp.write(cleanTxt)
    print('down finish\n')
    fp.close()

'''