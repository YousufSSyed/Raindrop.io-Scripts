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
try:
  while (True):
    bookmarks = bookmarks + Raindrop.search(api, page=page, collection=CollectionRef({"$id": 0}), word=searchterm, perpage=50, tag=searchtag)
    print("Added bookmarks from page " + str(page))
    page += 1
except:
  pickle.dump(bookmarks, searchfile, pickle.HIGHEST_PROTOCOL)
  print("Created data file.")
  searchfile.close()
