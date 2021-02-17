from raindropio import *
from rdfunctions import *
import time, datetime
api = API('e4588190-ab7d-43d3-b488-3716aac0272d')

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

overwrite = False
with open('bookmarks.csv') as f:
    for line in f:
        createdtime = time.mktime(datetime.datetime.strptime(line[:line.find(",")], "%m/%d/%Y %H:%M:%S").timetuple())
        url = line[line.find(",") + 1:find_nth(line, ",", 2)]
        tags = []
        try:
            if line[find_nth(line, ",", 2) + 1:].index("\"") != -1:
                tags = line[find_nth(line, ",", 2) + 1:line.rfind("\"")].split(sep=", ")
        except:
            tags.append(line[find_nth(line, ",", 2) + 1:])
        print(addBookmark(url, tags, createdtime, overwrite))
        rest()
