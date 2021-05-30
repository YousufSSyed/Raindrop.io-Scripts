from raindropio import *
from rdfunctions import *
import time, sys, os, pickle
api = API('e4588190-ab7d-43d3-b488-3716aac0272d')

# Both values are strings
searchterm = ""
searchtag = "Miscellaneous Reads"

newbookmarks = Raindrop.search(api, page=0, tag=searchtag, collection=CollectionRef({"$id": 0}), word=searchterm, perpage=50)
searchfile = open('search.pkl', 'wb')
bookmarks = []
page = 0

while (len(newbookmarks) != 0):
  bookmarks = bookmarks + newbookmarks
  print("Added bookmarks from page " + str(page) + ". total bookmarks: " + str(len(bookmarks)))
  page += 1
  try:
    newbookmarks = Raindrop.search(api, page=page, tag=searchtag, collection=CollectionRef({"$id": 0}), word=searchterm, perpage=50)
  except:
    print("Search limit reached.")
    break
pickle.dump(bookmarks, searchfile, pickle.HIGHEST_PROTOCOL)
print("Created data file.")
searchfile.close()
