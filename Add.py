from rdfunctions import *

parser = argparse.ArgumentParser("A CLI Script to add raindrop.io bookmarks and specify tags from a list using numbers")
parser.add_argument('-b', help="Specify one bookmark, or multiple delimited by spaces, with or without quotes. The script quits after adding them.", nargs='+')
parser.add_argument("-t", help="Numbers corresponding to tags to add to bookmarks specificed with -b. Requires -b.", type=int, nargs='+')
parser.add_argument("-nt", help="Include no tags when adding bookmarks with -b. Requires -b", action="store_true")
parser.add_argument("-r", help="A flag so that if a new bookmarks are added with the same URL as exisiting bookmark(s), the existing ones would be deleted.", action="store_true")
parser.add_argument("-s", help="Show all tags and the corresponding numbers when adding bookmarks", action="store_true")
parser.add_argument("-st", help="Shows all the bookmark tags and quits immediately.", action="store_true")
args = parser.parse_args()
if (args.t or args.nt) and args.b is None: parser.error("-t and -nt requires -b.")
if args.t and args.nt: parser.error("-t and -nt are mutually exclusive.")

def showTags(): [print(f"{str(tags.index(tag))}. {tag}") for tag in tags]
if args.st: showTags(); quit()

while True:
    urls = []
    if args.b is not None: urls = args.b
    else:
        text = input(f"{Fore.GREEN}Add bookmarks to your collection. Enter URLs and or arguments in: {clear()}"); urls.append(text)
        while text != "": text = input(); urls.append(text)
        urls.pop()
    printOverwrite = lambda : print(f"{Fore.RED}Bookmark overwriting enabled.{clear()}")
    if args.s: showTags()
    bookmarktags = []
    overwrite = args.r
    if args.t is None or not args.nt:
        bookmarkArgparse = argparse.ArgumentParser("Bookmark specific arguments")
        bookmarkArgparse.add_argument("-s", help="Show all numbers and their corresponding tags.", action="store_true")
        bookmarkArgparse.add_argument("-r", help="Reverses the overwrite option for these specific bookmarks. If overwriting is enabled, they won't be for those bookmarks, and vice versa.", action="store_true")
        bookmarkArgparse.add_argument("-t", type=int, nargs='+')
        while True:
            bookmarkArgs = input(f"{Fore.GREEN}Enter numbers and or arguments in: {clear()}") if args.t is None else " ".join(map(str, args.t))
            bookmarkArgs = f"-t {bookmarkArgs}" if any(str(n) in bookmarkArgs for n in [n for n in range(10)]) else bookmarkArgs
            try: bookmarkArgs = bookmarkArgparse.parse_args([bookmarkArgs])
            except: continue
            if bookmarkArgs.s and not args.s: showTags()
            if bookmarkArgs.r: overwrite = not overwrite
            if overwrite: printOverwrite()
            if bookmarkArgs.s or bookmarkArgs.r: continue
            args.t = bookmarkArgs.t; break
        bookmarktags = list(set([tags[int(x)] for x in args.t]))
    elif overwrite: printOverwrite()
    for link in urls: addBookmark(url=link, bookmarktags=bookmarktags, overwrite=overwrite)
    if args.b is not None: break
