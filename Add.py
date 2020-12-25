tags = ["Amazon Inc",
"Android Platform",
"App Related",
"Apple Inc",
"Bullshit",
"Cambridge MA",
"Chrome OS Platform",
"Cognition Related",
"Particularly Enjoyable",
"Culture Related",
"Definitions",
"Design (Non Visual)",
"Design (Visual)",
"Desktop Computing",
"Education Related",
"Enterprise Related",
"Good Reads",
"Good Thoughts",
"Google Inc",
"Hardware Component Related",
"Hardware Related",
"Humor",
"Interesting",
"Life Pro Tips",
"Entertainment Related",
"Memes & Meme Culture Related",
"Meme Content",
"Microsoft Corporation",
"Miscellaneous Reads",
"Mobile Device Related",
"Opinionated",
"Partially Read",
"Personal Reads",
"Power Rangers & Super Sentai",
"Relatable",
"Roblox Related",
"Samsung",
"School Related",
"Shazam",
"Skimmed / Partially Read",
"Software Related",
"Technical & Hardware Related",
"Technical & Software Related",
"Technology Related",
"Timely Matters",
"Unread",
"Web Related",
"Windows OS",
"Kamen Rider",
"Hilarious",
"Google Searches",
"Yu-Gi-Oh! Related"]

from raindropio import *
from rdfunctions import *
import sys
import time

api = API('e4588190-ab7d-43d3-b488-3716aac0272d')

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
    bookmarktags = [tags[int(x)] for x in input(tagmessage + "\nEnter numbers in to add tags: ").split()]
    #add bookmark, then wait
    for url in urls:
        print(addBookmark(url, bookmarktags))
    rest()
