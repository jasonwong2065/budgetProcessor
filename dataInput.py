#!/usr/bin/python
import string
import csv
import re
import sys
import os

def processDate(string):
    date = re.match("(\d+)\/(\d+)",string[0])
    if(date):
        day = date.group(1)
        month = date.group(2)
        format = day + "/" + month
        return format
def is_number(s): #Code from pythoncentral.io
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

try:
    sys.argv[1]
except:
    print("Usage: ./dataInput.py file1 file2 etc.")
    sys.exit(0)

files = sys.argv[1:]
for file in files:
    fileName = os.path.splitext(file)[0]
    spreadsheet = csv.writer(open(fileName + ".csv", 'wb'), delimiter=',')
    f = open(file, "r") #Opens budget file

    sum = 0
    items = []
    firstDateIterated = 0 #has the first date been iterated

    print("Skipped lines in file: {}".format(file))
    for line in f:
        string = line.strip().split(" ",1)
        date = processDate(string)
        if(date):
            if(not firstDateIterated):
                firstDateIterated = 1
            else:
                items = ','.join(item for item in items if item)
                spreadsheet.writerow([sum, items])
                spreadsheet.writerow(string)
                sum = 0
                items = []
        elif is_number(string[0]):
            sum += int(string[0])
            items.append(' '.join(string[1:]))
        elif(string[0]):
            print(string)
    items = ','.join(item for item in items if item)
    spreadsheet.writerow([sum, items]) #Writes the final line

    f.close()
