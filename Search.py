from raindropio import *
import time, sys, os, pickle
api = API('e4588190-ab7d-43d3-b488-3716aac0272d')

searchterm = "https://www.google.com/search?client=firefox"

searchfile = open('search.pkl', 'wb')
page = 0
bookmarks = []
limit = True
pagelimit = 19
if limit:
  while page <= pagelimit:
    bookmarks = bookmarks + Raindrop.search(api, page=page, collection=CollectionRef({"$id": 0}), word=searchterm, perpage=sys.maxsize)
    print("Added bookmarks from page" + str(page))
    page += 1
else:
  while (items:=Raindrop.search(api, page=page, collection=CollectionRef({"$id": 0}), word=searchterm, perpage=sys.maxsize)):
    bookmarks = bookmarks + items
    print("Added bookmarks from page" + str(page))
    page += 1
pickle.dump(bookmarks, searchfile, pickle.HIGHEST_PROTOCOL)
print("Created data file.")
searchfile.close()
