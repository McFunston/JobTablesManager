import pprint
from pandas import read_csv, read_excel
from os import name, rename, remove
from itertools import chain
import sys

def fix_csv(path, breakdown_path):
    csv_sum=0
    file_name=path.split("/")[-1].split("\\")[-1].split(".")[0]
    file_ext = path.split(".")[-1]
    new_path = path.replace(file_name, file_name+"-fixed")
    pub_num = get_pub_num(file_name)
    
    breakdown_count = check_breakdown(breakdown_path, pub_num)
    fixed=list()
    needed_fixing = False

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

                    if cur != '"' and cur != ',' and cur != '\n' and cur != ' ' and open_quote==False:
                        if prev!=',':
                            needed_fixing = True
                            print("In "+ file_name + " there is a field missing both quote and comma in this line: \n"+line)
                            line = line[:i] + ',"' + line[i:]
                            i=i+2
                            open_quote= not open_quote
                        else:
                            needed_fixing = True
                            print("In "+ file_name + " there is a field with no opening quotation mark in this line: \n"+line)
                            line = line[:i] + '"' + line[i:]
                            i=i+1
                            open_quote= not open_quote

                    if line[i] == "," and open_quote==True:
                        needed_fixing = True
                        print("In "+ file_name + " there is a field with no closing quotation mark in this line: \n"+line)
                        line = line[:i] + '"' + line[i:]
                        open_quote=not open_quote
                        #print(line)                        
                        
                    if line[i] == " " and prev == ',':
                        needed_fixing = True
                        print("In "+ file_name + " there is a floating space found in this line: \n"+line)
                        line = line[:i] + line[i+1:]
                        i=i-1
                        length=length-1
                
                i=i+1
            fixed.append(line)
    if needed_fixing == True:
        with open(new_path, 'w') as nf:
            nf.writelines(fixed)
    else:
        new_path=path
    try:
        x = read_csv(new_path, header=None)
        csv_sum=x[4].values.sum()+x[5].values.sum()+x[6].values.sum()
        if new_path!=path: 
            remove(path)
    except:
        print(file_name + " is broken, and I cannot fix it")
        if needed_fixing == True:
            remove(new_path)
            
        broke_name = path.replace("."+file_ext, "-broken."+file_ext)
        rename(path, broke_name)
    if csv_sum != breakdown_count:
        print("In " +file_name+" the count(" + str(csv_sum) +") does not match the Excel file that you sent ("+str(breakdown_count)+")\n")

def get_pub_num(name):
    num = str()
    found=False
    for letter in name:
        if not letter.isnumeric() and found==True:
            return num

        if letter.isnumeric():
            found = True
            num += str(letter)
    return num

def find_largest_number(df, sheet_name):
    largest_number = 0
    cell_list = df[sheet_name].values.tolist()
    single_cell_list = chain.from_iterable(cell_list)
    for cell in single_cell_list:
        try:
            cell = int(cell)
            if cell> largest_number:
                largest_number=cell
        except:
            pass
    return largest_number
    

def check_breakdown(path, pub_num):
    df = read_excel(path, sheet_name=None, header=None)
    totals=dict()
    if "Learn More" in df.keys():
        df.pop("Learn More")
    name_list = list(df.keys())
    for name in name_list:
        pub_number=get_pub_num(name)
        df[pub_number]=df.pop(name)
        totals[pub_number]=find_largest_number(df, pub_number)
    return(find_largest_number(df, pub_num))

fix_csv("763 Neighbours of Wascana The Creeks #763.txt", "Test_Data/Canada Mag Break Down September Issue 2020.xlsx")

# if __name__ == "__main__":
#     fix_csv(sys.argv[1], sys.argv[2])