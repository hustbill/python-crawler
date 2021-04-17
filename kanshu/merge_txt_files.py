
import os
import glob
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

def merge_txt_files(txtPath,outputFile):
    print("merge_txt_files: ")
    read_files = glob.glob(txtPath + "/*.txt")
    # sorted_files = sorted(read_files)
    # correctly sort a string with a number inside
    read_files.sort(key=natural_keys)
    # print (read_files[1:20])
    # sub_files = read_files[1:20]
    sub_files = read_files
    with open(outputFile, "wb") as outfile:
        for f in sub_files:
            with open(f, "rb") as infile:
                print(f)
                # outfile.write(f.encode('gbk'))
                # outfile.write(f)
                base = os.path.basename(f)
                file_name = os.path.splitext(base)[0]

                section_name = ('\n\n ' + file_name + ' \n\n').encode()
                outfile.write(section_name)

                outfile.write(infile.read())


if __name__ == "__main__":
    outputFile = "冷枪-中日两支特种小分队生死对决-吴超著.txt"
    merge_txt_files("./txt_files", outputFile)