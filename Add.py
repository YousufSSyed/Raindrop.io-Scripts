from rdfunctions import *

parser = argparse.ArgumentParser("A CLI Script to add raindrop.io bookmarks and specify tags from a list using numbers")
parser.add_argument('-b', help="Specify one bookmark, or multiple delimited by spaces, with or without quotes. The script quits after adding them.", nargs='+')
parser.add_argument("-t", help="Numbers corresponding to tags to add to bookmarks specificed with -b. Requires -b.", type=int, nargs='+')
parser.add_argument("-nt", help="Include no tags when adding bookmarks with -b. Requires -b", action="store_true")
parser.add_argument("-r", help="A flag so that if a new bookmarks are added with the same URL as exisiting bookmark(s), the existing ones would be deleted.", action="store_true")
parser.add_argument("-s", help="Show all tags and the corresponding numbers when adding bookmarks", action="store_true")
parser.add_argument("-st", help="Shows all the bookmark tags and quits immediately.", action="store_true")
args = parser.parse_args()
if args.t and args.nt: parser.error("-t and -nt are mutually exclusive.")
parser.exit_on_error=False

print(f"{Fore.GREEN}Add bookmarks to your collection{clear()}")
printOverwrite = lambda : print(f"{Fore.RED}Bookmark overwriting enabled.{clear()}")
def showTags(): [print(f"{Fore.GREEN}{str(tags.index(tag))}. {tag}{clear()}") for tag in tags]
if args.st: showTags(); quit()
overwrite = args.r

def parseBookmarkArgs(inputArgs, dataType=int):
    print(dataType)
    global overwrite; bArgs = None
    try: bArgs = parser.parse_args(f"-t {inputArgs}".split() if dataType == int else f"-b {inputArgs}".split())
    except:
        try: bArgs = parser.parse_args(inputArgs.split())
        except: return
    print(bArgs)
    if any([arg for arg in vars(bArgs) if vars(bArgs)[arg] and arg not in ["s", "r", "b", "t"]]) or (args.b and datatype == int) or (args.t and dataType != int): 
        print("Only -s and -r are allowed in the URL and tag inputs."); return
    if bArgs.s and not args.s: showTags()
    if bArgs.r: overwrite = not overwrite
    if overwrite: printOverwrite()
    if bArgs.s or bArgs.r: return
    if bArgs.b or args.t:
        if dataType == int: return bArgs.t
        else: return bArgs.b
    else: return

while True:
    urls = []
    if args.b is not None: urls = args.b
    else:
        text = input(f"{Fore.GREEN}Enter URLs and or arguments in: {clear()}")
        while text != "" or len(urls) == 0: 
            arg = parseBookmarkArgs(text, str)
            if (arg): urls.extend(arg)
            print("arg" + str(arg))
            print(urls)
            text = input()
    print(urls)
