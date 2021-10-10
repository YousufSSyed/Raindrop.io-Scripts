from raindropio import *
from rdsettings import *
import sys, time, datetime
from datetime import datetime
api = API(APIKey)

def addBookmark(url: str, bookmarktags: list, createdtime=None, overwrite=False):
    if url == "about:blank":
        return "Invalid URL"
    createdtime = datetime.utcfromtimestamp(createdtime).strftime('%Y-%m-%d %H:%M:%S') if createdtime is not None else None
    createdtime2 = datetime.utcfromtimestamp(createdtime).strftime("%b %d %Y %-I:%M %p") if createdtime is not None else None
    bookmarks = []
    # Search for if there are existing links
    try:
        bookmarks = Raindrop.search(api, page=0, collection=CollectionRef({"$id": 0}), word=url, perpage=sys.maxsize)
    except:
        api = API(APIKey)
        bookmarks = Raindrop.search(api, page=0, collection=CollectionRef({"$id": 0}), word=url, perpage=sys.maxsize)
    # Make a list of duplicate links if they exist
    bookmarks = [bookmark for bookmark in bookmarks if bookmark.link == url or bookmark.link == "https://" + url or bookmark.link == "http://" + url]
    print("URL: " + url + ". New Tags: " + str(bookmarktags) + ". Time Added: " + (createdtime2 if createdtime2 is not None else "none") + ". Current time: " + datetime.now().strftime("%b %d %Y %I:%M %p"))
    # if existing bookmarks exist, delete extra ones and update the last one.
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
        return "Existing Bookmark found. Bookmark updated."
    else:
        newbookmark = Raindrop.create(api, link=url, tags=bookmarktags, created=createdtime)
        return "New bookmark created."

# sleep for 1 second (for the sake of the 120 requests per minute limit)
def rest():
    time.sleep(1)
