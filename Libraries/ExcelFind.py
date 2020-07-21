from openpyxl import load_workbook
from openpyxl import utils
from datetime import datetime
import sys

# Finds a given field in an Excel file, based on finding a given value within the same row.
# requires 3 arguments: 
# 1 The full path name of the file (ie c:/folder/file.xlsx)
# 2 The column to search for the given value
# 3 The value to search for
# Returns the row in which the value was found

def OpenXLSX(inputPath):
    book = load_workbook(inputPath)
    sheet = book.active
    return sheet

def padString(name):
    jn = name.zfill(4)
    return jn

def findValue(sheet, searchColumn, searchValue, killColumn, dateColumn):
    foundRows=list()
    for row in sheet:
        found = False
        for cell in row:
            # print(cell.column_letter)
            if cell.column_letter == str(searchColumn):
                # print(sheet[killColumn+str(cell.row)].value)
                if padString(str(searchValue)) in padString(str(cell.value).split('-')[0]) and sheet[killColumn+str(cell.row)].value == None:
                    # print(type(sheet[dateColumn+str(cell.row)].value))
                    # print(str(cell.row))
                    found = True
        if found == True:
            foundRows.append(row)
    if len(foundRows) == 1:
        colNumber = utils.cell.column_index_from_string(searchColumn)
        print(foundRows[0][colNumber].row)
    if len(foundRows) > 1:
        colNumber = utils.cell.column_index_from_string(dateColumn)-1
        for foundRow in foundRows:
            foundRow[colNumber].value = datetime.strptime(foundRow[colNumber].value, '%m/%d/%Y')
            # print(foundRow[colNumber].value)
        foundRows.sort(key=lambda x: x[colNumber].value)
        print(foundRows[0][0].row)

"""     if found == False:
        print(searchColumn)
        print(searchValue)
        print("Not Found") """

def OpenTable(path):
    return OpenXLSX(path)

#findValue(OpenTable('BVM_Jobs.xlsx'), 'B', '327', 'C', 'J')

# sheet = OpenTable("Backing/SplitterJobList/5588.xlsx")
# print(Find(sheet,"A","L3054"))
# WriteCSV(table, 0, "Backing/SplitterJobList")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(len(sys.argv))
        print(sys.argv[1])
        print(sys.argv[2])
        print(sys.argv[3])

        print("Arguments: 'File', 'Search Column', 'Search Value', 'Kill Column', 'Date Column' are required")
    else:
        findValue(OpenTable(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])