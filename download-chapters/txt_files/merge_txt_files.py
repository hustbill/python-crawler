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
    merge_txt_files()


if __name__ == '__main__':
    main()
