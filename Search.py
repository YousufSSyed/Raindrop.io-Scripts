from raindropio import *
from rdfunctions import *
import time, sys, os, pickle
api = API('e4588190-ab7d-43d3-b488-3716aac0272d')

searchterm = "reddit.com"
searchtag = "Miscellaneous Reads"
limit = True

searchfile = open('search.pkl', 'wb')
page = 0
bookmarks = []
count = 0
if limit:
  while (items:=Raindrop.search(api, page=page, collection=CollectionRef({"$id": 0}), word=searchterm, perpage=50, tag=searchtag)) and page < 19:
    bookmarks = bookmarks + items
    print("Added bookmarks from page " + str(page))
    page += 1
else:
    while (items:=Raindrop.search(api, page=page, collection=CollectionRef({"$id": 0}), perpage=50)):
      for item in items:
        if searchterm in item.link and searchtag in item.tags:
          bookmarks.append(item)
          count += 1
          print("Bookmark #" + str(count) + " added. URL: " + item.link + ". Title: " + item.title + ". Tags: " + str(item.tags)) 
        print("Added bookmarks from page " + str(page))
        page += 1
pickle.dump(bookmarks, searchfile, pickle.HIGHEST_PROTOCOL)
print("Created data file.")
searchfile.close()
