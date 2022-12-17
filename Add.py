from rdfunctions import *

parser = argparse.ArgumentParser("A CLI Script to add raindrop.io bookmarks and specify tags from a list using numbers")
parser.add_argument('-b', help="Specify one bookmark, or multiple delimited by spaces, with or without quotes. The script quits after adding them.", nargs='+')
parser.add_argument("-t", help="Numbers corresponding to tags to add to bookmarks specificed with -b. Requires -b.", type=int, nargs='+')
parser.add_argument("-nt", help="Include no tags when adding bookmarks with -b. Requires -b", action="store_true")
parser.add_argument("-r", help="A flag so that if a new bookmarks are added with the same URL as exisiting bookmark(s), the existing ones would be deleted.", action="store_true")
parser.add_argument("-up", help="Use the URLs or tags previous used in the script session. Works inside the script only.", action="store_true")
parser.add_argument("-p", help="Show the previous tags or numbers in the script depending on where you enter it. Works inside the script only.", action="store_true")
parser.add_argument("-c", help="Show the current tags or numbers in the script depending on where you enter it. Works inside the script only.", action="store_true")
parser.add_argument("-s", help="Show all tags and the corresponding numbers when adding bookmarks", action="store_true")
parser.add_argument("-st", help="Shows all the bookmark tags and quits immediately.", action="store_true")
args = parser.parse_args()
if args.t and args.nt: parser.error("-t and -nt are mutually exclusive.")
parser.exit_on_error=False

printOverwrite = lambda : print(f"{Fore.RED}Bookmark overwriting {'enabled' if overwrite else f'{Fore.GREEN}disabled'}{clear()}.")
def showTags(): [print(f"{Fore.GREEN}{str(tags.index(tag))}. {tag}{clear()}") for tag in tags]
if args.st: showTags(); quit()
overwrite = args.r

values = {
    "PreviousURLs": [],
    "URLs": [],
    "PreviousTags": [],
    "Tags": []
}

def getInput(num=True):
        text = input(f"{Fore.GREEN}Enter {'URLs' if num else 'numbers'} and or arguments in: {clear()}")
        while text != "" or len(urls) == 0:
            if (arg := parseBookmarkArgs(text, num)): values[argType := "URLs" if ]urls.extend(arg)
            text = input()

def parseBookmarkArgs(inputArgs, num=True):
    print(num)
    global overwrite; bArgs = None
    try: bArgs = parser.parse_args(f"-t {inputArgs}".split() if num else f"-b {inputArgs}".split())
    except:
        try: bArgs = parser.parse_args(inputArgs.split())
        except: return
    print(bArgs)
    if any([arg for arg in vars(bArgs) if vars(bArgs)[arg] and arg not in ["s", "r", "b", "t"]]) or (bArgs.b and num) or (bArgs.t and not num):
        print("Only -s and -r are allowed in the URL and tag inputs."); return
    if bArgs.s and not args.s: showTags()
    if bArgs.r: overwrite = not overwrite
    if overwrite: printOverwrite()
    printArgs(previous=False, addPrevious=False)
    if bArgs.c:
        print(f"{Fore.GREEN}Current {'tags' if num else 'URLs'}:{clear()}")
        if num: print(values["Tags"])
        else: [print(URL) for URL in values["URLs"]]
    if bArgs.p:
        print(f"{Fore.GREEN}Previous {'tags' if num else 'URLs'}:{clear()}")
        if num: print(values["PreviousTags"])
        else: [print(URL) for URL in values["PreviousURLs"]]
    argValues = list(bArgs.t if num else bArgs.b)
    if bArgs.up:
        print(f"{Fore.GREEN}Added previous {'tags' if num else 'URLs'}.{clear()}")
        if num: print(values["PreviousTags"])
        else: [print(URL) for URL in values["PreviousURLs"]]
    if bArgs.b or bargs.t:
        if num: return bArgs.t
        else: return bArgs.b
    else: return

while True:
    urls = []
    if args.b is not None: urls = args.b
    else:
      print(f"{Fore.GREEN}Add bookmarks to your collection{clear()}")

    if args.s: showTags()
    bookmarktags = []
    overwrite = args.r
    if not args.nt:
        if args.t: bookmarktags = args.t
        else:
            text = input(f"{Fore.GREEN}Enter numbers and or arguments in: {clear()}")
            while text != "":
                if (arg := parseBookmarkArgs(text, str)): urls.extend(arg)

        bookmarktags = list(set([tags[int(x)] for x in bookmarktags]))
    else:
        if args.nt: continue
        
        

            bookmarkArgs = input(f"{Fore.GREEN}Enter numbers and or arguments in: {clear()}") if args.t is None else " ".join(map(str, args.t))
        
    else
        overwrite: printOverwrite()
    for link in urls: addBookmark(url=link, bookmarktags=bookmarktags, overwrite=overwrite)
    if args.b is not None: break
