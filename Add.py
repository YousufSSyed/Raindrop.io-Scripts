from rdfunctions import *

parser = argparse.ArgumentParser("A CLI Script to add raindrop.io bookmarks and specify tags.")
parser.add_argument("-r", 
help="A flag so that if a new bookmarks are added with the same URL as exisiting bookmark(s), the existing ones would be deleted.", action="store_true")
parser.add_argument("-o", help="A flag to add bookmark(s) only once then quit the script immediately.", action="store_true")
parser.add_argument('-b', help="Specify one bookmark, or multiple delimited by spaces. This will skip the add bookmarks prompt the first time.", nargs='+')
parser.add_argument("-s", help="A flag to show all of your tags when adding bookmarks", action="store_true")
parser.add_argument("-t", help="Only show all the bookmark tags and nothing else.", action="store_true")
args = parser.parse_args()

if args.t:
    [print(f"{str(tags.index(tag))}. {tag}" ) for tag in tags]
    quit()

while True:
    # Get URL and tags for new bookmark
    urls = []
    if args.b is not None: urls = args.b
    else:
        text = "placeholder"
        print("Add bookmarks to your collection. Enter URL(s) in: ")
        while text != "":
            text = input()
            urls.append(text)
        urls.pop()
    [print(f"{str(tags.index(tag))}. {tag}" ) for tag in tags]
    bookmarktaggs = [tags[int(x)] for x in input("Enter numbers in: ").split()]
    #add bookmark, then wait
    for link in urls:
        addBookmark(url=link, bookmarktags=bookmarktaggs, overwrite=args.r)
    if (args.b is not None) or args.o:
        break
