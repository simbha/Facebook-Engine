import urllib
import re

import sys
sys.path.insert(0, '/gspread')
import gspread


mail = raw_input("E-mail: ")
passw = raw_input("Password: ")
spreadsheet_name = raw_input("Name of the spreadsheet: ")

sites = [line.strip() for line in open('sites.txt')]

def writeInfo():
    pass

def getInfo(url):
    ''' function to get the info from facebook '''
    content = urllib.urlopen("https://api.facebook.com/restserver.php?method=links.getStats&urls=" + url).read()
    content = str(content)

    share_count = int(re.search(r"<share_count>([0-9]+)</share_count>", content).groups()[0])
    like_count = int(re.search(r"<like_count>([0-9]+)</like_count>", content).groups()[0])
    comment_count = int(re.search(r"<comment_count>([0-9]+)</comment_count>", content).groups()[0])
    total_count = int(re.search(r"<total_count>([0-9]+)</total_count>", content).groups()[0])

    return (share_count, like_count, comment_count, total_count)

def updateLine(data, line, w):
    ''' Function to update a row in the google spreadsheet with the list provided '''
    cols = 'ABCDEFGHIJKLMNOPQRSTWXYZ'
    # defines the range to update
    cell_list = w.range("A" + str(line) + ":" + cols[len(data)-1] + str(line))
    # sets the value for each cell in the range
    for c, cell in enumerate(cell_list):
        cell.value = data[c]
    # updates the range/row
    w.update_cells(cell_list)

# gets the info about each site
dataList = []
for site in sites:
    dataList.append(getInfo(site))

# functions to interact with google spreadsheet
g = gspread.login(mail, passw)
w = g.open(spreadsheet_name).sheet1

# adds the header
header = ("Site", "Shares", "Likes", "Comments", "Total")
updateLine(header, 1, w)

# adds the rows with the results
for line, site in enumerate(sites):
    data = dataList[line]
    data = [site] + list(data)
    updateLine(data, line+2, w)
