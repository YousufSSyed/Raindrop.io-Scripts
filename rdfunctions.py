from raindropio import *
from rdsettings import *
import sys, time, datetime, os, pickle, io, argparse
from datetime import datetime
api = API(APIKey)

def addBookmark(url: str, bookmarktags: list, createdtime=None, overwrite=False):
    if "about:blank" in url: print("Invalid URL"); return
    createdtime = datetime.utcfromtimestamp(createdtime).strftime('%Y-%m-%d %H:%M:%S') if createdtime is not None else None
    createdtime2 = datetime.utcfromtimestamp(createdtime).strftime("%b %d %Y %-I:%M %p") if createdtime is not None else None
    print(f"Adding URL \"{url}\"{', ' + str(bookmarktags) + ' tags included' if len(bookmarktags) == 0 else ''}{f', and with the custom timestamp: {createdtime2}' if createdtime2 is not None else ''}, at {datetime.now().strftime('%I:%M%p')}.")
    bookmarks = searchBookmarks(url)
    if len(bookmarks) != 0:
        if overwrite == False:
            for bookmark in bookmarks: bookmarktags = bookmarktags + bookmark.tags
        collections = [bookmark.collection for bookmark in bookmarks]
        finalcollection = max(set(collections), key = collections.count)
        if len(bookmarks) > 1:
            for i in range(len(bookmarks) - 1): Raindrop.remove(api, id=bookmarks[i + 1].id)
        Raindrop.update(api, id=bookmarks[0].id, tags=bookmarktags, collection=finalcollection, created=createdtime)
        print("Existing Bookmark(s) found, merged, and updated." if overwrite == False else "Bookmark updated.")
    else:
        try: Raindrop.create(api, link=url, tags=bookmarktags, created=createdtime)
        except: apiRefresh(); Raindrop.create(api, link=url, tags=bookmarktags, created=createdtime)
        print("New bookmark created.")
    rest()

def searchBookmarks(url: str):
    bookmarks = []
    try: bookmarks = Raindrop.search(api, page=0, collection=CollectionRef({"$id": 0}), word=url, perpage=50)
    except: apiRefresh(); bookmarks = Raindrop.search(api, page=0, collection=CollectionRef({"$id": 0}), word=url, perpage=50)
    bookmarks = [bookmark for bookmark in bookmarks if bookmark.link == url or bookmark.link in [f"{prefix}{bookmark.link}" for prefix in ["http://", "https://"]]]  
    rest(); return bookmarks

def deleteBookmark(url: str):
    print("URL: " + url)
    bookmarks = searchBookmarks(url)
    if len(bookmarks) <= 0: print("Bookmark does not exist."); return
    count = len(bookmarks)
    for bookmark in bookmarks:
        try: Raindrop.remove(api, id=bookmark.id)
        except: apiRefresh(); Raindrop.remove(api, id=bookmark.id)
    print(f"{str(count)} 'bookmark'{'s' if count > 1 else ''} deleted.")
    rest()

def apiRefresh(): api = API(APIKey)

# sleep for 0.5 seconds (for the sake of the 120 requests per minute limit)
def rest(): time.sleep(0.5)
