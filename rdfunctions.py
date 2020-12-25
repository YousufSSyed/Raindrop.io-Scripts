from raindropio import *
import sys
import time
import datetime
from datetime import datetime
api = API('e4588190-ab7d-43d3-b488-3716aac0272d')

#Search for existing bookmarks, if they exist, get all the tags from all bookmarks, and update the first bookmark to be in the most frequent collection, and delete all others. Otherwise, create new bookmark
def addBookmark(url: str, bookmarktags: list, createdtime=None, overwrite=False):
    if url == "about:blank":
        return "Invalid URL"
    createdtime2 = datetime.strftime("%b %d %Y %-I:%M %p") if createdtime is not None else None
    createdtime = datetime.utcfromtimestamp(createdtime).strftime('%Y-%m-%d %H:%M:%S') if createdtime is not None else None
    bookmarks = Raindrop.search(api, page=0, collection=CollectionRef({"$id": 0}), word=url, perpage=sys.maxsize)
    bookmarks = [bookmark for bookmark in bookmarks if bookmark.link == url or bookmark.link == "https://" + url or bookmark.link == "http://" + url]
    print("URL: " + url + ". New Tags: " + str(bookmarktags) + ". Time Added: " + (createdtime2 if createdtime2 is not None else "none") + ". Current time: " + datetime.now().strftime("%b %d %Y %-I:%M %p"))
    if len(bookmarks) != 0:
        if overwrite == False:
            for bookmark in bookmarks:
                bookmarktags = bookmarktags + bookmark.tags
        collections = [bookmark.collection for bookmark in bookmarks]
        finalcollection = max(set(collections), key = collections.count)
        if len(bookmarks) > 1:
            for i in range(len(bookmarks) - 1):
                remove = Raindrop.remove(api, id=bookmarks[i + 1].id)
        updatedbookmark = Raindrop.update(api, id=bookmarks[0].id, tags=bookmarktags, collection=finalcollection, created=createdtime)
        return "Existing Bookmark(s) found, tags from existing bookmarks put into new bookmark, and other existing bookmarks have been deleted."
    else:
        newbookmark = Raindrop.create(api, link=url, tags=bookmarktags, created=createdtime)
        return "New bookmark created."

# sleep for 2 seconds (for the sake of the 120 requests per minute)
def rest():
    time.sleep(1)
