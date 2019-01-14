import csv
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

top, users, list_of_cells, header = 500, [], [], []
req = Request("https://socialblade.com/twitter/top/" + str(top) + "/followers", headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(urlopen(req).read(), "lxml")
[header.append(re.sub(r'[^\w]', '', cell.text)) for cell in soup.findAll("div", {"class": "table-header"})]
table = soup.find("div", {"class": "content-module-wide"})
cells = table.findAll("div", {"class": "table-cell"})
cells_in_row = len(cells) / top

for i, cell in enumerate(cells):
    if i is not 0 and i % cells_in_row == 0:
        users.append(list_of_cells)
        list_of_cells = []  # reset list of cells
    list_of_cells.append(cell.text)

with open("output.csv", "w", newline='') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(cell for cell in header)
    writer.writerows(users)
