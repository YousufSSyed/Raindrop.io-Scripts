import sys, time, datetime, os, pickle, io, argparse, copy, asyncio
from datetime import datetime
from raindropio import *
from rdsettings import *
from dateutil import tz
from ratelimit import *
from colorama import *

api = API(APIKey); clear = lambda: Style.RESET_ALL
ordinal = lambda n: "%d%s" % (int(n),"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

@sleep_and_retry
@limits(calls=120, period=60)
def raindropio(function):
    try: return function()
    except: api = API(APIKey); print(f"{Fore.GREEN}Refreshing API access.{clear()}"); return function()

def addBookmarks(urls, bookmarktags, overwrite=False, createdtime=None):
    plural = 's' if len(urls) > 1 else ''
    print(f"{Fore.BLUE}Adding bookmark{plural} {f'with the {Fore.CYAN}{bookmarktags}{Fore.BLUE} tag{plural}' if len(bookmarktags) > 0 else 'with no tags'} ...{clear()}")
    time = lambda t, format='%-I:%M%:%S%p': t.astimezone(tz.tzlocal()).strftime(format)
    bookmarkText = lambda bookmark, updated=False, count=0, customTime=False: f"bookmark for {Fore.GREEN}{bookmark.link[:os.get_terminal_size().columns * 2]}{f'{Fore.RED}...' if len(bookmark.link) > os.get_terminal_size().columns * 2 else ''}{clear()}{f' with the {Fore.CYAN}{bookmark.tags}{clear()} tag{plural}' if len(bookmarktags) > 0 and bookmark.tags != bookmarktags else ''} {f'with the timestamp of ' if customTime else (f'{Fore.MAGENTA}created at' if updated else 'at')} {Fore.MAGENTA}{time(bookmark.created)}{' on ' + time(bookmark.created, f'%b {ordinal(bookmark.created.day)} %Y') if bookmark.created.astimezone(tz.tzlocal()).day != datetime.now().day else ''}" + (f"{Fore.CYAN} and {f'merged {count} bookmarks' if count > 1 else 'updated'} at {Fore.MAGENTA}{time(bookmark.lastUpdate)}" if updated else '') + clear()
    def background(f):
        def wrapped(*args, **kwargs): return loop.run_in_executor(None, f, *args, **kwargs)
        return wrapped
    @background
    def checkBookmark(url, index):
        nonlocal bookmarktags; nonlocal createdtime
        if "about:blank" in url: print("Invalid URL"); return
        bookmarks = searchBookmarks(url)
        if len(bookmarks) != 0:
            if not overwrite:
                for bookmark in bookmarks: bookmarktags = list(set(bookmarktags + bookmark.tags))
            collections = [bookmark.collection for bookmark in bookmarks]
            finalcollection = max(set(collections), key = collections.count)
            if len(bookmarks) > 1:
                for i in range(len(bookmarks) - 1): raindropio(lambda: Raindrop.remove(api, id=bookmarks[i + 1].id))
            bookmark = raindropio(lambda: Raindrop.update(api, id=bookmarks[0].id, tags=bookmarktags, collection=finalcollection, created=createdtime))
            print(f"{Fore.RED}Updated {bookmarkText(bookmark, True, len(bookmarks))}.")
        else: return url
    loop = asyncio.get_event_loop()
    links = loop.run_until_complete(asyncio.gather(*[checkBookmark(url, index) for index, url in enumerate(urls)]))
    if len(links := list(filter(None, links))) > 0:
        bookmarks = raindropio(lambda: Raindrop.createMany(api, links=links, tags=bookmarktags, created=createdtime))
        for bookmark in bookmarks: print(f"Created {bookmarkText(bookmark)}.")
    message = lambda color, count, new: f"{color}{count} bookmark{'s' if count > 1 else ''} {'created' if new else 'updated'}. {clear()}" if count > 0 else ""
    print(f"{message(Fore.CYAN, len(links), True)}{message(Fore.RED, len(urls) - len(links), False)}")

def searchBookmarks(url):
    bookmarks = raindropio(lambda: Raindrop.search(api, page=0, collection=CollectionRef({"$id": 0}), word=url, perpage=50))
    return [bookmark for bookmark in bookmarks if bookmark.link == url or bookmark.link in [f"{prefix}{bookmark.link}" for prefix in ["http://", "https://"]]]

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
