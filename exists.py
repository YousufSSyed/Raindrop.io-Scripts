from rdfunctions import *

parser = argparse.ArgumentParser("A CLI Script to check if bookmarks exist in raindrop.io.")
parser.add_argument('-b', help="Specify one bookmark, or multiple delimited by spaces. This will skip the add bookmarks prompt the first time.", nargs='+')
args = parser.parse_args()

while True:
    urls = []
    if args.b is not None: urls = args.b
    else:
        print(f"{Fore.GREEN}Check if bookmarks exist. Enter URL(s) in: {clear()}")
        text = "placeholder"
        while text != "": text = input(); urls.append(text)
        urls.pop(); 
    print(f"{Fore.GREEN}non-exsitant URLs: {clear()}")
    for url in urls:
        if len(searchBookmarks(url)) == 0: print(url)
    if (args.b is not None): break