import pprint
from pandas import read_csv
from os import rename, remove
import sys

def fix_csv(path):
    fixed = []
    needed_fixing = False
    file_name=path.split("/")[-1].split("\\")[-1].split(".")[0]
    file_ext = path.split(".")[-1]
    new_path = path.replace(file_name, file_name+"-fixed")
    with open(path, 'r') as f:
        for line in f:
            length = len(line)
            i=0
            open_quote=False
            while i < length:
                prev = ""
                #print(open_quote)
                if line[i]=='"':
                    open_quote=not open_quote

                if i > 1:
                    prev=line[i-1]
                    cur=line[i]

                    if (
                        cur != '"'
                        and cur != ','
                        and cur != '\n'
                        and cur != ' '
                        and not open_quote
                    ):
                        if prev!=',':
                            print("In "+ file_name + " there is a field missing both quote and comma in this line: \n"+line)
                            line = line[:i] + ',"' + line[i:]
                            i += 2
                        else:
                            print("In "+ file_name + " there is a field with no opening quotation mark in this line: \n"+line)
                            line = line[:i] + '"' + line[i:]
                            i += 1
                        needed_fixing = True
                        open_quote= not open_quote
                    if line[i] == "," and open_quote:
                        needed_fixing = True
                        print("In "+ file_name + " there is a field with no closing quotation mark in this line: \n"+line)
                        line = line[:i] + '"' + line[i:]
                        open_quote=not open_quote
                        #print(line)                        

                    if line[i] == " " and prev == ',':
                        needed_fixing = True
                        print("In "+ file_name + " there is a floating space found in this line: \n"+line)
                        line = line[:i] + line[i+1:]
                        i -= 1
                        length -= 1

                i += 1
            fixed.append(line)
    if needed_fixing:
        with open(new_path, 'w') as nf:
            nf.writelines(fixed)
    else:
        new_path=path
    try:
        x = read_csv(new_path)
        if new_path!=path: 
            remove(path)
    except:
        print(file_name + " is broken, and I cannot fix it")
        if needed_fixing:
            remove(new_path)

        broke_name = path.replace("."+file_ext, "-broken."+file_ext)
        rename(path, broke_name)

# fix_csv("Test_Data/Bad_txt/3358 West of Winnipeg #3358.txt")

if __name__ == "__main__":
    fix_csv(sys.argv[1])