import sys, time, datetime, os, pickle, io, argparse, copy, asyncio, tomllib
from datetime import datetime
from raindropio import *
from dateutil import tz
from ratelimit import *
from colorama import *

settings = tomllib.load(open("rdsettings.toml", "rb"))
api = API(settings["APIKey"]); clear = lambda: Style.RESET_ALL
ordinal = lambda n: "%d%s" % (int(n),"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

@sleep_and_retry
@limits(calls=120, period=60)
def raindropio(function):
    try: return function()
    except: api = API(settings["APIKey"]); print(f"{Fore.GREEN}Refreshing API access.{clear()}"); return function()

def addBookmarks(urls, bookmarktags, overwrite=False, createdtime=None):
    plural = lambda s=urls: 's' if len(s) > 1 else ''
    print(f"{Fore.BLUE}Adding bookmark{plural()} {f'with the {Fore.CYAN}{bookmarktags}{Fore.BLUE} tag{plural(bookmarktags)}' if len(bookmarktags) > 0 else 'with no tags'} ...{clear()}")
    def bookmarkText(bookmark, updated=False, count=0, customTime=False):
        time = lambda t, format='%-I:%M%:%S%p': t.astimezone(tz.tzlocal()).strftime(format)
        link = f"{Fore.GREEN}{bookmark.link[:(tWidth := os.get_terminal_size().columns * 2)]}{f'{Fore.RED}...{clear()}' if len(bookmark.link) > tWidth else ''}"
        tags = f"{f' with the {Fore.CYAN}{bookmark.tags}{clear()} tag{plural(bookmarktags)}' if len(bookmarktags) > 0 and bookmark.tags != bookmarktags else ''}"
        timeText = f'{Fore.MAGENTA}with the timestamp' if customTime else (f'{Fore.RED}created' if updated else 'at')
        createdDate = f" on {Fore.MAGENTA}{time(bookmark.created, f'%b {ordinal(bookmark.created.day)} %Y')}" if customTime or (updated and bookmark.created.astimezone(tz.tzlocal()).day != datetime.now().day) else (' at' if updated else '')
        timestamp = f"{Fore.MAGENTA}{time(bookmark.created)}"
        updatedTime = f"{Fore.CYAN}{f'and merged {count} bookmarks' if count > 1 else ''} at {Fore.MAGENTA}{time(bookmark.lastUpdate)}" if updated else ''
        return f"{link}{tags} bookmark {timeText}{createdDate} {timestamp}{updatedTime}{clear()}"
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
            print(f"{bookmarkText(bookmark, True, len(bookmarks))}.")
        else: return url
    loop = asyncio.get_event_loop()
    links = loop.run_until_complete(asyncio.gather(*[checkBookmark(url, index) for index, url in enumerate(urls)]))
    if len(links := list(filter(None, links))) > 0:
        bookmarks = raindropio(lambda: Raindrop.createMany(api, links=links, tags=bookmarktags, created=createdtime))
        for bookmark in bookmarks: print(f"{bookmarkText(bookmark)}.")
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