#!/usr/bin/env python

import csv # csv helper
import sys, getopt # used for command line args



# Parse command line arguments.



helpString = 'Expected usage is "python csv2ris.py -i <yourInputFileName>.csv". For example, "python csv2ris.py -i Example.csv". Also note the python file should be located in the same folder as your csv file.'

fileName = "filename.csv" # default

try:
    # read in and parse command line args
    args = sys.argv[1:] # get rid of the first argument (which will be 'csv2ris.py')
    opts, _ = getopt.getopt(args, "hi:") # "hi means h and i arguments are supported"
except getopt.GetoptError:
    # occurs if there is unknown argument
    print(helpString)
    exit(2)
for opt, arg in opts:
    # help option
    if opt == '-h':
        print(helpString)
        exit()
    # specifying input file
    elif opt == "-i":
        fileName = arg

if fileName == "filename.csv":
    print("Attempting to read in data from filename.csv. If you wish to specify your own file name, please use the following format.")
    print(helpString)





# Load files and data



infile = open(fileName, mode='r', encoding='utf-8-sig', errors='ignore') #Open input csv file—replace 'filename' with the name of your csv file.


# Load csv parsing library. This will give us our data in the format [{keyName: keyValue}] where each item in the list is a row (with the keyName being the column header and keyValue being the row's value in that column)
dataDicts = csv.DictReader(infile)

# These are the valid fields accepted in the ris format
all_fields = ['TY', 'TI', 'AB', 'A1', 'A2', 'A3', 'A4', 'AD', 'AN', 'AU', 'AV', 'BT', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'CA', 'CN', 'CP', 'CT', 'CY', 'DA', 'DB', 'DO', 'DP', 'ED', 'EP', 'ET', 'ID', 'IS', 'J1', 'J2', 'JA', 'JF', 'JO', 'KW', 'L1', 'L2', 'L3', 'L4', 'LA', 'LB', 'LK', 'M1', 'M2', 'M3', 'N1', 'N2', 'NV', 'OP', 'PB', 'PP', 'PY', 'RI', 'RN', 'RP', 'SE', 'SN', 'SP', 'ST', 'T1', 'T2', 'T3', 'TA', 'TT', 'U1', 'U2', 'U3', 'U4', 'U5', 'UR', 'VL', 'VO', 'Y1', 'Y2', 'ER']

# Get name of file to write to - split on . so the first part will be the intended name (and second part will be '.csv' which we discard)
outFileName = fileName.split('.')[0]+'.ris'
outfile = open(outFileName, "w", encoding='utf-8', errors='replace') # Create output txt (ris) file—replace 'filename' with the desired name of your txt/ris file

output = [] # Construct output in a list of characters and convert it to string when finished



seenCols = set()

# Actual logic

for row in dataDicts:
    if 'TY' not in row:
        err = "ERROR: Your csv file must have a TY column. See valid TY values at https://en.wikipedia.org/wiki/RIS_(file_format)"
        print(err)
        raise Exception(err)
    for header in row:
        if header == 'AU' or header == 'KW': #Authors and keywords will have multiple values, delimited by '; '. Need to split these up. 
            collection = row[header].split('; ')
            for item in collection:
                # Pair each value for author/keyword with its heading, put each on a new line.
                line = header + '  - ' + item + '\n' 

                # Convert our line into a list of characters which can add to our existing output character list
                output.extend(list(line)) 
        elif header in all_fields:
            line = header + '  - ' + row[header] + '\n' # For all fields besides author/keyword, pair the value with its heading, put each on a new line.
            output.extend(list(line))
        elif header not in seenCols:
            print(f"WARNING: Column {header} contained within csv that is not a valid RIS tag. See valid RIS tags at https://en.wikipedia.org/wiki/RIS_(file_format)")
            seenCols.add(header)

    output.extend(list('ER  - \n\n')) # Puts an empty "ER" (End of Reference) tag at the end of each record, along with an extra new line for readability



# Conversion done - now write to file


# convert our list of characters to a string
stringOutput = ''.join(output)

# and finally write it to a file
outfile.write(stringOutput)

# We did it - yay!
infile.close()
outfile.close()

print("File successfully converted")
