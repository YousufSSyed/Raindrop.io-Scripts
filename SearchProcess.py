from raindropio import *
import time, sys, os, pickle, io
api = API('e4588190-ab7d-43d3-b488-3716aac0272d')

oldtags = ["Miscellaneous Reads"]
newtags = ["Miscellaneous Articles"]

searchfile = open('search.pkl', 'rb')
bookmarks = pickle.load(searchfile)
print("Loaded data file.")

for index, bookmark in enumerate(bookmarks):
  if bookmark is None:
    print("Bookmark #" + str(index + 1) + ": already processed.")
    continue
  print("Bookmark #" + str(index + 1) + ". URL: " + bookmark.link + ". Title: " + bookmark.title + ". Tags: " + str(bookmark.tags))
  bookmarktags = newtags[:]
  duplicate = False
  for index2, bookmark2 in enumerate(bookmarks[index + 1:]):
    if bookmark.link == bookmark2.link and index != index2:
      duplicate = True
      bookmarktags += bookmark2.tags + bookmark.tags
      bookmarktags = [tag for tag in bookmarktags if tag not in oldtags]
      bookmarks[index] = None
      try:
        remove = Raindrop.remove(api, id=bookmark.id)
      except:
        remove = None
      newbookmark = Raindrop.update(api, id=bookmark2.id, tags=bookmarktags, collection=bookmark2.collection, created=bookmark2.created)
      searchfile.close()
      searchfile = open('search.pkl', 'wb')
      pickle.dump(bookmarks, searchfile, pickle.HIGHEST_PROTOCOL)
      searchfile.close()
      searchfile = open('search.pkl', 'rb')
      print("Bookmark #" + str(index + 1) + ": Duplicate bookmark found. Bookmarks combined and updated. tags: " + str(bookmarktags))
      break
  if duplicate:
    continue
  bookmarktags += [tag for tag in bookmark.tags if tag not in oldtags]
  bookmarks[index] = None
  newbookmark = Raindrop.update(api, id=bookmark.id, tags=bookmarktags, collection=bookmark.collection, created=bookmark.created)
  searchfile.close()
  searchfile = open('search.pkl', 'wb')
  pickle.dump(bookmarks, searchfile, pickle.HIGHEST_PROTOCOL)
  searchfile.close()
  searchfile = open('search.pkl', 'rb')
  print("Bookmark #" + str(index + 1) + " updated. New tags: " + str(bookmarktags))
  bookmarktags = []
  time.sleep(0.5)
