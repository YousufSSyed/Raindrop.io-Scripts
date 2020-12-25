from raindropio import *
from rdfunctions import *
import sys
import time
api = API('e4588190-ab7d-43d3-b488-3716aac0272d')

bookmarktags = ["Web Related"]
overwrite = False

with open('rd.txt') as f:
    for line in f:
        createdtime = None
        if line.find(" ") != -1:
            url = line[:line.find(" ")]
            createdtime = int(line[line.find(" ") + 1:])
        else:
            url = line
        print(addBookmark(url, bookmarktags, createdtime, overwrite))
        rest()
