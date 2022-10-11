from html.parser import HTMLParser
from io import StringIO
import requests
import re
'''import feedparser
NewsFeed = feedparser.parse("feed:https://us6.campaign-archive.com/feed?u=a55e641e3e&id=8b3c7488d6")
entry = NewsFeed.entries[1]

print(entry.published)
print("******")
print(entry.summary)
print("------News Link--------")
print(entry.link)

'''
from bs4 import BeautifulSoup

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def getNames():
	soup = BeautifulSoup(requests.get('https://us6.campaign-archive.com/home/?u=a55e641e3e&id=8b3c7488d6').text, "html.parser")

	for i in soup.find_all("li"):
		if "eNews" in i.text:
			date = i.text.split('for ')
			link = i.a['href']
			message = BeautifulSoup(requests.get(link).text, "html.parser")
			raw = requests.get(link).text
			raw = strip_tags(raw)
			roster = raw[raw.find("Preaching Roster") + 50: raw.find("Preaching Roster") + 300].split("\n")
			nameWithTitle = roster[0].split("\xa0 ")[2].split(" - ")
			name = nameWithTitle[0]
			sermonTitle = nameWithTitle[1]
			print("Weekly Sermon Recognized! Person: " + name + " | TItle: " + sermonTitle)
			return(name, sermonTitle)
			break
