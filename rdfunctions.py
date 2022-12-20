import sys, time, datetime, os, pickle, io, argparse, copy
from datetime import datetime
from ratelimit import limits
from raindropio import *
from rdsettings import *
from colorama import *

api = API(APIKey); clear = lambda : Style.RESET_ALL
bookmarkText = lambda url, bookmarktags=None, createdtime2=None : f"{Fore.GREEN}{url}{clear()}{f' with the {Fore.CYAN}{bookmarktags}{clear()} tags' if len(bookmarktags) > 0 else ''}{f' and with the custom timestamp - {Fore.BLUE}{createdtime2}{clear()}' if createdtime2 else ''} at {Fore.MAGENTA}{datetime.now().strftime('%-I:%M%:%S %p')}{clear()}"

# in the future, make it so that overflow runs in the background
@limits(calls=120, period=60)
def raindropio(function):
    try: return function()
    except: api = API(APIKey); print(f"{Fore.GREEN}Refreshing API access.{clear()}"); return function()

def addBookmark(url, bookmarktags, overwrite=False, createdtime=None):
    if "about:blank" in url: print("Invalid URL"); return
    createdtime = datetime.utcfromtimestamp(createdtime).strftime('%Y-%m-%d %H:%M:%S') if createdtime else None
    createdtime2 = datetime.utcfromtimestamp(createdtime).strftime("%b %d %Y %-I:%M %p") if createdtime else None    
    bookmarks = searchBookmarks(url)
    if len(bookmarks) != 0:
        if overwrite == False:
            for bookmark in bookmarks: bookmarktags = list(set(bookmarktags + bookmark.tags))
        collections = [bookmark.collection for bookmark in bookmarks]
        finalcollection = max(set(collections), key = collections.count)
        if len(bookmarks) > 1:
            for i in range(len(bookmarks) - 1): raindropio(lambda : Raindrop.remove(api, id=bookmarks[i + 1].id))
        raindropio(lambda : Raindrop.update(api, id=bookmarks[0].id, tags=bookmarktags, collection=finalcollection, created=createdtime))
        pluralText = "bookmarks merged" if len(bookmarks) > 1 else "bookmark updated"
        print(f"{Fore.RED}Updated bookmark{clear()} {bookmarkText(url, bookmarktags, createdtime2)} {Fore.RED}with {len(bookmarks)} {pluralText}{clear()}.")
    else:
        raindropio(lambda : Raindrop.create(api, link=url, tags=bookmarktags, created=createdtime))
        print(f"{bookmarkText(url, bookmarktags, createdtime2)}.")

def searchBookmarks(url):
    bookmarks = raindropio(lambda: Raindrop.search(api, page=0, collection=CollectionRef({"$id": 0}), word=url, perpage=50))
    bookmarks = [bookmark for bookmark in bookmarks if bookmark.link == url or bookmark.link in [f"{prefix}{bookmark.link}" for prefix in ["http://", "https://"]]]
    return bookmarks

def deleteBookmark(url):
    bookmarks = searchBookmarks(url)
    if len(bookmarks) <= 0: print(f"{Fore.RED}The bookmark {Fore.GREEN}{url}{clear()}{Fore.RED} does not exist.{clear()}"); return
    count = len(bookmarks)
    for bookmark in bookmarks: raindropio(lambda: Raindrop.remove(api, id=bookmark.id))
    print(f"{Fore.RED}{str(count)} 'bookmark'{'s' if count > 1 else ''} for {Fore.GREEN}{url}{clear()}{Fore.RED} deleted.{clear()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-sb', help="Search a URL.", required=True)
    url = parser.parse_args().sb
    print(f"Searching for {Fore.GREEN}{url}{clear()}.")
    bookmarks = searchBookmarks(url)
    if len(bookmarks) == 0: print(f"{Fore.RED}No results found.{clear()}"); exit()
    else:
        print(f"{Fore.GREEN}{len(bookmarks)}{clear()} result{'s' if len(bookmarks) > 1 else ''} found:")
        for bookmark in bookmarks: print(bookmark.link)
