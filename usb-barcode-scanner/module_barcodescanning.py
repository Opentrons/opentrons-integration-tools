#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from IPython.display import HTML, clear_output, display
import string

deck_slot = input("Deck slot location for the plate or rack? answer must be 1-11: ")
print("Deck Slot", deck_slot, "\n")

by_row = input("Perform scans in row-wise order? (left to right A1, A2, A3...) (answer y or n) ")
clear_output()
print("Scan in Row Order? ", by_row, "\n")

numrows = int(input("Number of rows in the rack or plate?: "))
clear_output()
print("Number of Rows", numrows, "\n")

numcols = int(input("Number of columns in the rack or plate?: "))
clear_output()
print("Number of Columns", numcols, "\n")

rows = [*string.ascii_uppercase][:numrows]
cols = [str(num+1) for num in range(numcols)]
wellsbyrow = [row+col for row in rows for col in cols]
wellsbycol = [row+col for col in cols for row in rows]

# keyboard characters
hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e',
        9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j',
        14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o',
        19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't',
        24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
        29: 'z', 30: '1', 31: '2', 32: '3', 33: '4',
        34: '5', 35: '6', 36: '7', 37: '8', 38: '9',
        39: '0', 44: ' ', 45: '-', 46: '=', 47: '[',
        48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~',
        54: ',', 55: '.', 56: '/'  }

# shifted keyboard characters
hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F',
         10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K',
         15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P',
         20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U',
         25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z',
         30: '!', 31: '@', 32: '#', 33: '$', 34: '%',
         35: '^', 36: '&', 37: '*', 38: '(', 39: ')',
         44: ' ', 45: '_', 46: '+', 47: '{', 48: '}',
         49: '|', 51: ':' , 52: '"', 53: '~', 54: '<',
         55: '>', 56: '?'  }

stop_scanning = "AX002VRRIOR"
scan_count = 0

# HTML display
data = [wellsbyrow[i:i+numcols] for i in range(0, len(wellsbyrow), numcols)]
html = "<h1 style='color: #056608; font-family: arial narrow;'> Deck Slot {} </h1>".format(deck_slot) + "<table>"
for row in data:
    html += "<tr style='color: #800000; font-family: arial narrow; font-size: 16px;'>"
    for field in row:
        html +="<td style='border: 1px solid black;'><h4>{}</h4></td>".format(field)
    html += "</tr>"
html += "</table>" + "<p style= 'font-family: arial narrow;'> Start Scanning... </p>"
clear_output()
display(HTML(html))

def scanorder():
    yield from wellsbyrow if by_row == "y" else wellsbycol
    
wellname = scanorder()
current = next(wellname)

display(HTML("<h1 style='color: #056608; font-family: arial narrow;'> Scanning {}... </h1>".format(current)))

with open('/dev/hidraw0', 'rb') as fp:
    ss= ""
    shift = False
    while True:
        if ss == stop_scanning:
            break
        if scan_count == numcols*numrows:
            finished = input("Scan Samples in Another Deck Slot? type y or n: ")
            if finished == 'n':
                display(HTML("<h1> Finished Scanning </h1>"))
                break
            else:
                deck_slot = input("Deck slot location for the plate or rack? answer must be 1-11: ")
                clear_output()
                print("Deck Slot", deck_slot, "\n")

                by_row = input("Scanning will be performed in row-wise order (left to right A1, A2, A3...)? (answer y or n) ")
                clear_output()
                print("Scan in Row Order? ", by_row, "\n")

                numrows = int(input("Number of rows in the rack or plate?: "))
                clear_output()
                print("Number of Rows", numrows, "\n")

                numcols = int(input("Number of columns in the rack or plate?: "))
                clear_output()
                print("Number of Columns", numcols, "\n")
                
                rows = [*string.ascii_uppercase][:numrows]
                cols = [str(num+1) for num in range(numcols)]
                wellsbyrow = [row+col for row in rows for col in cols]
                wellsbycol = [row+col for col in cols for row in rows]
            
                scan_count = 0
                
                wellname = scanorder()
                current = next(wellname)
                
                # HTML display
                data = [wellsbyrow[i:i+numcols] for i in range(0, len(wellsbyrow), numcols)]
                html = "<h1 style='color: #056608; font-family: arial narrow;'> Deck Slot {} </h1>".format(deck_slot) + "<table>"
                for row in data:
                    html += "<tr style='color: #800000; font-family: arial narrow; font-size:16px;'>"
                    for field in row:
                        html +="<td style='border: 1px solid black;'><h4>{}</h4></td>".format(field)
                    html += "</tr>"
                html += "</table>" + "<p style='font-family: arial narrow;'> Start Scanning... </p>"
                clear_output()
                display(HTML(html))
                display(HTML("<h1 style='color: #056608; font-family: arial narrow;'> Scanning {}... </h1>".format(current)))
                
        buffer = fp.read(8) # read device input buffer
        for c in buffer:
            if c > 0:
                if c == 40: # 40 CR complete scan string read
                    fp.flush()
                    print(ss, "\n")
                    answer = input("Keep this scan? type y or n: ")
                    if answer == 'y':
                        print("Writing ", ss," to scans.csv", "\n")
                        file = 'scans.csv'
                        with open(file, 'a') as outfile:
                            outfile.write(deck_slot + ',' + current + ',' + ss + '\n')  # write scan string to csv
                        scan_count += 1
                        for i, row in enumerate(data):
                            for j, well in enumerate(row):
                                if well == current:
                                    data[i][j] = ss
                        clear_output()
                        html = "<h1 style='color: #056608; font-family: arial narrow;'> Deck Slot {} </h1>".format(deck_slot) + "<table>"
                        for row in data:
                            html += "<tr style='color: #800000; font-family: arial narrow; font-size:16px;'>"
                            for field in row:
                                html +="<td style='border: 1px solid black;'><h4>{}</h4></td>".format(field)
                            html += "</tr>"
                        html += "</table>"
                        clear_output()
                        display(HTML(html))
                        if scan_count < numrows*numcols:
                            current = next(wellname)
                            display(HTML("<h1 style='color: #056608; font-family: arial narrow;'> Scanning {}... </h1>".format(current)))
                    else:
                        print("Discarding this scan ", ss, "\n")
                    ss = ""
                    shift = False
                    continue
                if shift:
                    if c == 2 : # 2 shift
                        shift = True
                    else:
                        ss += hid2[c]  # append shifted character to scan string
                        shift = False
                else:
                    if c == 2 :  # 2 shift
                        shift = True
                    else:
                        ss += hid[c]  # append character to scan string

