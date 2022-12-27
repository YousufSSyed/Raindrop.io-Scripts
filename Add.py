from rdfunctions import *

parser = argparse.ArgumentParser("A CLI Script to add raindrop.io bookmarks and specify tags from a list using numbers")
parser.add_argument('-b', help="Specify one bookmark, or multiple delimited by spaces, with or without quotes. The script quits after adding them.", nargs='+')
parser.add_argument("-t", help="Numbers corresponding to tags to add to bookmarks specificed with -b. Requires -b.", type=int, nargs='+')
parser.add_argument("-nt", help="Include no tags when adding bookmarks with -b. Requires -b", action="store_true")
parser.add_argument("-r", help="A flag so that if a new bookmarks are added with the same URL as exisiting bookmark(s), the existing ones would be deleted.", action="store_true")
parser.add_argument("-up", help="Use the URLs or tags previous used in the script session. Works inside the script only.", action="store_true")
parser.add_argument("-p", help="Show the previous tags or numbers in the script depending on where you enter it. Works inside the script only.", action="store_true")
parser.add_argument("-c", help="Show the current tags. Works inside the script's bookmark dialogue only.", action="store_true")
parser.add_argument("-s", help="Show all tags and the corresponding numbers when adding bookmarks", action="store_true")
parser.add_argument("-st", help="Shows all the bookmark tags and quits immediately.", action="store_true")
args = parser.parse_args()
if args.t and args.nt: parser.error("-t and -nt are mutually exclusive.")
parser.exit_on_error=False

printOverwrite = lambda : print(f"{Fore.RED}Bookmark overwriting {'enabled' if overwrite else f'{Fore.GREEN}disabled'}{clear()}.")
bookmarktags = lambda tagNums: list(set([tags[int(x)] for x in tagNums]))
def showTags(): [print(f"{Fore.GREEN}{str(tags.index(tag))}. {tag}{clear()}") for tag in tags]
if args.st: showTags(); quit()
bArgs, overwrite = None, args.r

values = {
    "PreviousURLs": [],
    "URLs": [],
    "PreviousTags": [],
    "Tags": []
}

def getInput(num=True):
    global values, overwrite
    if num and overwrite: printOverwrite()
    text = input(f"{Fore.GREEN}Enter {Fore.BLUE}{'numbers' if num else 'URLs'} {Fore.GREEN}and arguments in: {clear()}" + ('' if num else '\n'))
    while text != "" or len(values['Tags' if num else 'URLs']) == 0:
        if text == "" and num: break
        if (arg := parseBookmarkArgs(text, num)):
            values['Tags' if num else 'URLs'].extend(arg)
            if num and not bArgs.up: break
        text = input()

def parseBookmarkArgs(inputArgs, num=True):
    global overwrite, values, bArgs
    try: bArgs = parser.parse_args(f"{'-t' if num else f'-b'} {inputArgs}".split())
    except:
        try: bArgs = parser.parse_args(inputArgs.split())
        except: return
    if any([arg for arg in vars(bArgs) if vars(bArgs)[arg] and arg not in ["c", "p", "up", "s", "r", "b", "t"]]) or (bArgs.b and num) or (bArgs.t and not num):
        print("Only the following arguments are allowed in the URL and tag inputs: -s -r -c -p -up."); return
    argValues = bArgs.t if num else bArgs.b
    def printArgs(previous=False, addPrevious=False):
        nonlocal argValues
        key = 'Tags' if num else 'URLs'
        previousValue = "Previous" if previous else ""
        if len(values[f"{previousValue if previous else ''}{key}"]) == 0:
            print(f"{Fore.RED}There are no {f'previous' if previous else 'current'} {key}.{clear()}"); return 
        urlLength = len(values[f'{previousValue}URLs'])
        print(f"{Fore.GREEN}{'Added ' if addPrevious else ''}{'Previous' if previous else 'Current'} {key}:{clear()} {values[f'{previousValue}Tags'] if num else ''}{values[f'{previousValue}URLs'] if urlLength == 1 and not num else ''}")
        if urlLength > 1: [print(URL) for URL in values[f"{previousValue}URLs"]]
        if addPrevious:
            if argValues is None: argValues = values[f"Previous{key}"]
            else: argsValues.extend(values[f"Previous{key}"])
    if bArgs.c:
        if num: print(f"{Fore.RED}-c is for bookmarks only.{clear()}")
        else: printArgs()
    if bArgs.p: printArgs(True)
    if bArgs.up: printArgs(True, True)
    if bArgs.s: showTags()
    if bArgs.r: overwrite = not overwrite; printOverwrite()
    return argValues

if not args.b: print(f"{Fore.GREEN}Add bookmarks to your collection. {clear()}", end="")
while True:
    if args.b: values["URLs"] = args.b
    else: getInput(False)
    if args.s: showTags()
    overwrite = args.r
    if not args.nt:
        if args.t: values["Tags"] = args.t
        else: getInput(True)
    if args.b and overwrite: printOverwrite()
    addBookmarks(values["URLs"], bookmarktags(values["Tags"]), overwrite=overwrite)
    if args.b: break
    values["PreviousURLs"], values["PreviousTags"] = values["URLs"], values["Tags"]
    values["URLs"], values["Tags"] = [], []
