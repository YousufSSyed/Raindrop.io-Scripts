from rdfunctions import *

# downloads all or as many bookmarks possible matching the search crtiera into a PKL file
# The search() function in python-raindropio only takes one search term

searchterm = ""
searchtags = []
# Gets the searh tags based on the numbers typed in
searchtags = [tags[int(x)] for x in searchtags]
#Do you want bookmarks with only those tags or not?
onlyThoseTags = True

searchfile = open('search.pkl', 'wb')
bookmarks = []
page = 0
newbookmarks = Raindrop.search(api, page=page, tag=searchtags, collection=CollectionRef({"$id": 0}), word=searchterm, perpage=50)

while (len(newbookmarks) != 0):
  bookmarks = bookmarks + newbookmarks
  print("Added bookmarks from page " + str(page) + ". Total bookmarks: " + str(len(bookmarks)))
  page += 1
  try:
    newbookmarks = Raindrop.search(api, page=page, tag=searchtags, collection=CollectionRef({"$id": 0}), word=searchterm, perpage=50)
  except:
    print("Search limit reached.")
    break
print(len(bookmarks))
pickle.dump(bookmarks, searchfile, pickle.HIGHEST_PROTOCOL)
print("Created data file.")
searchfile.close()