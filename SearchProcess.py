from raindropio import *
import time, sys, os, pickle, io
api = API('e4588190-ab7d-43d3-b488-3716aac0272d')

oldtags = ["Miscellaneous"]
newtags = ["Google Search"]

searchfile = open('search.pkl', 'rb')
bookmarks = pickle.load(searchfile)
print("Loaded data file.")

def update():
  searchfile.close()
  searchfile = open('search.pkl', 'wb')
  pickle.dump(bookmarks, searchfile, pickle.HIGHEST_PROTOCOL)
  searchfile.close()
  searchfile = open('search.pkl', 'rb')

for index, bookmark in enumerate(bookmarks):
  print("Bookmark #" + str(index) + ". URL: " + bookmark.link + ". Title: " + bookmark.title + ". Tags: " + str(bookmark.tags))
  if len([tag for tag in bookmark.tags if tag in newtags]) != 0 or bookmark is None:
    bookmarks[index] = None
    continue
  bookmarktags = newtags
  for index2, bookmark2 in enumaterate(bookmarks[index + 1:]):
    if bookmark.link == bookmark2.link and index1 != index2:
      bookmarktags += bookmark2.tags + bookmark1.tags
      bookmarktags = [tag for tag in bookmarktags if tag not in oldtags]
      bookmarks[index] = None
      remove = Raindrop.remove(api, id=bookmark.id)
      newbookmark = Raindrop.update(api, id=bookmark2.id, tags=bookmarktags)
      update()
      break
  bookmarktags += [tag for tag in bookmark.tags if tag not in oldtags]
  newbookmark = Raindrop.update(api, id=bookmark.id, tags=bookmarktags)
  bookmarks[index] = None
  update()
