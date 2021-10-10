from raindropio import *
from rdfunctions import *
from rdsettings import *
import sys, time

while True:
    # Get URL and tags for new bookmark
    urls = []
    text = "placeholder"
    while text != "":
        text = input("Enter a URL: ")
        urls.append(text)
    urls.pop()
    tagmessage = ""
    for tag in tags:
        tagmessage = tagmessage + "\n" + str(tags.index(tag)) + ". " + tag
    bookmarktaggs = [tags[int(x)] for x in input(tagmessage + "\nEnter numbers in to add tags: ").split()]
    #add bookmark, then wait
    for link in urls:
        print(addBookmark(url=link, bookmarktags=bookmarktaggs))
        time.sleep(0.5)
