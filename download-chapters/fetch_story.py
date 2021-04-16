# coding=utf-8
import urllib
import re
import os
import glob
import urllib.request


from urllib.parse import urljoin
from urllib.parse import urlparse

import re


# Ref: https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from https://stackoverflow.com/a/12643073/190597
    '''
    return [atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def fetch_section(webroot):
    print("fetch_section")
    for page in range(1, 2):
        print('正在下载第'+str(page)+'页小说')

        url = 'http://www.cangshubao.net/forum-915-'+str(page)+'.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=180)
            #print (response.read().decode('gbk'))
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)

        html = response.read().decode('gbk')
        # print html
        # pattern = re.compile(u'<a href="thread-1453325-1-3.html">第205章行内人的密报</a>')
        #  pattern = re.compile(u'<span id="(.*?)"><a href="(.*?)"></a></span>')
        pattern = re.compile(
            u'<span id="(.*?)"><a href="(.*?)">第(.*?)</a></span>')
        items = re.findall(pattern, html)
        # print (items)

        for item in items:
            try:
                section_thread = item[0].encode('gbk')
                section_link = item[1]
                section_name = item[2]
                section_full_link = urljoin(webroot, section_link)   # 构建书的绝对地址

                # 请求地址
                try:
                    request = urllib.request.Request(
                        section_full_link, headers=headers)
                    response = urllib.request.urlopen(request, timeout=180)
                except urllib.error.URLError as e:
                    if hasattr(e, "code"):
                        print(e.code)
                    if hasattr(e, "reason"):
                        print(e.reason)
                html = response.read().decode('gbk')

                pattern = re.compile(
                    '<table cellspacing="0" cellpadding="0"><tr><td class="t_msgfont" id="(.*?)"><font size="5">(.*?)</font></td></tr></table>', re.S)
                section_content = re.findall(pattern, html)

                # down txt
                try:
                    fp = open(section_name+'.txt', 'w')
                except IOError as e:
                    pattern = re.compile(
                        '<font size="5">(.*?)</font><br />', re.S)
                    section_name = re.findall(pattern, section_name)
                    fp = open(section_name[0]+'.txt', 'w')
                print('start download')
                cleanTxt = cleanhtml(str(section_content[0][1]))
                fp.write(cleanTxt)
                print('down finish\n')
                fp.close()
            except Exception as e:
                print('该条目解析出现错误，忽略')
                print(e)
                print('')
                fp = open('error.log', 'a')
                fp.write('page:'+str(page)+'\n')
                print(item)
                
                # fp.write(item[4].encode('gbk'))
                fp.write('\nThere is an error in parsing process.\n\n')
                fp.close()


def merge_txt_files():
    print("merge_txt_files: ")
    read_files = glob.glob("*.txt")
    # sorted_files = sorted(read_files)
    # correctly sort a string with a number inside
    read_files.sort(key=natural_keys)
    # print (read_files[1:20])
    # sub_files = read_files[1:20]
    sub_files = read_files
    with open("result.txt", "wb") as outfile:
        for f in sub_files:
            with open(f, "rb") as infile:
                print(f)
                # outfile.write(f.encode('gbk'))
                # outfile.write(f)
                base = os.path.basename(f)
                file_name = os.path.splitext(base)[0]

                section_name = ('\n\n\n### ' + file_name + " \n\n\n").encode()
                outfile.write(section_name)

                outfile.write(infile.read())


def main():
    # 获取排行榜首页内容
    webroot = 'http://www.cangshubao.net/'
    
    fetch_section(webroot)

    # sort string by number inside
    alist = [
        "something1",
        "something2",
        "something1.0",
        "something1.25",
        "something1.105"]

    alist.sort(key=natural_keys)
    # print(alist)
    # merge sections into one file
    # merge_txt_files()


if __name__ == '__main__':
    main()
