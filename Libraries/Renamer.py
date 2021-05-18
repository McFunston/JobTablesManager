import csv
import sys
import os

def OpenCSV(inputPath):
    rows = []
    with open(inputPath, encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter =',')
        for row in csv_reader:
            rows.append(row)
    return rows

def WriteCSV(table, outputPath):

    with open(outputPath, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(table)

def jobNumberPadder(number):
    if number!='':
        prefix = number[0]
        number = number[1:]
        number = number.rjust(4, '0')
        number = prefix+number
    return number

def pdfRenamer(fileName, jobsList, codeColumn, jNColumn):
    table = OpenCSV(jobsList)
    newTable = []
    catch=False

    if '-' in fileName[:5]:
        fileNameNumbers = [s.rjust(4, '0') for s in fileName.split('-') if s.isdigit()]
    elif '_' in fileName[:5]:
        fileNameNumbers = [s.rjust(4, '0') for s in fileName.split('_') if s.isdigit()]
    else:
        fileNameNumbers = [s.rjust(4, '0') for s in fileName.split() if s.isdigit()]

    if len(fileNameNumbers) == 0:
        return

    for row in table:
        code = row[int(codeColumn)].rjust(4, '0')


        if (
            row[int(codeColumn)] != ''
            and code == fileNameNumbers[0]
            and not catch
        ):
            newFileName = jobNumberPadder(row[int(jNColumn)])+'_'+fileName
            os.rename(fileName, 'Renamed/'+newFileName)
            catch=True
        elif row[0] != '': 
            newTable.append(row)
    WriteCSV(newTable, jobsList)

# pdfRenamer('488-24 Pager 1 2.pdf','BVM_Open_Jobs.csv', 6, 0)

if __name__ == "__main__":
    if len(sys.argv) != 5:

        print("Arguments: 'PDF File', 'CSV File', 'Code Column', and 'ID Column' are required")
    else:
        pdfRenamer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
