from raindropio import *
import time, sys, os, pickle, io
api = API('e4588190-ab7d-43d3-b488-3716aac0272d')

oldtags = ["Miscellaneous"]
newtags = ["Google Searches"]

searchfile = open('search.pkl', 'rb')
bookmarks = pickle.load(searchfile)
print("Loaded data file.")

for index, bookmark in enumerate(bookmarks):
  if bookmark is None:
    print("Bookmark #" + str(index) + ": already processed.")
    continue
  print("Bookmark #" + str(index) + ". URL: " + bookmark.link + ". Title: " + bookmark.title + ". Tags: " + str(bookmark.tags))
  bookmarktags = newtags
  for index2, bookmark2 in enumerate(bookmarks[index + 1:]):
    if bookmark.link == bookmark2.link and index != index2:
      bookmarktags += bookmark2.tags + bookmark.tags
      bookmarktags = [tag for tag in bookmarktags if tag not in oldtags]
      bookmarks[index] = None
      remove = Raindrop.remove(api, id=bookmark.id)
      newbookmark = Raindrop.update(api, id=bookmark2.id, tags=bookmarktags, collection=bookmark2.collection, created=bookmark2.created)
      searchfile.close()
      searchfile = open('search.pkl', 'wb')
      pickle.dump(bookmarks, searchfile, pickle.HIGHEST_PROTOCOL)
      searchfile.close()
      searchfile = open('search.pkl', 'rb')
      print("Bookmark #" + str(index) + ": Duplicate bookmark found. Bookmarks combined and updated.")
      break
  bookmarktags += [tag for tag in bookmark.tags if tag not in oldtags]
  print(str(bookmarktags))
  newbookmark = Raindrop.update(api, id=bookmark.id, tags=bookmarktags, collection=bookmark.collection, created=bookmark.created)
  bookmarks[index] = None
  searchfile.close()
  searchfile = open('search.pkl', 'wb')
  pickle.dump(bookmarks, searchfile, pickle.HIGHEST_PROTOCOL)
  searchfile.close()
  searchfile = open('search.pkl', 'rb')
  print("Bookmark #" + str(index) + " updated.")
