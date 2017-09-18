from flask import Flask, jsonify, Response
import feedparser
from html.parser import HTMLParser
import dateutil.parser
import datetime
import logging
import json

ARXIV_ASTROPH_URL = "http://arxiv.org/rss/astro-ph?version=2.0"

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.recording_p = 0
        self.authors = []
        self.summary = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.recording += 1
        if tag == 'p':
            self.recording_p += 1

    def handle_endtag(self, tag):
        if tag == 'a':
            self.recording -= 1
        if tag == 'p':
            self.recording_p -= 1

    def handle_data(self, data):
        if self.recording==1:
            self.data = data
            self.authors.append(data)
        if self.recording==0 and self.recording_p==1:
            self.summary = data

class ArticleEntry:
    """
        a class for an article entry
    """
    Nauthor_display = 3 # only show the first three authors

    def __init__(self, entry, updateDate_str):
        self.entry = entry
        self.id = self.entry['id']
        self.title = self.entry['title'].split(' (arXiv')[0]
        self.link = self.entry['link']
        self.updateDate = self.generate_updateDate(updateDate_str)

        self.parser = Parser()
        self.parser.feed(self.entry['summary'])
        self.summary = self.process_summary(self.parser.summary)

        self.generate_author_list()
        self.maintext = self.generate_mainText_from_summary()

    def generate_updateDate(self, updateDate_str):
        updateDate_datetime = dateutil.parser.parse(updateDate_str)
        updateDate_datetime += datetime.timedelta(seconds=int(self.id.split('.')[-1]))

        return updateDate_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def generate_author_list(self):
        self.author_list_full = list(self.parser.authors)
        self.Nauthor = len(self.author_list_full)

        na_short = min(self.Nauthor, self.Nauthor_display) # show 3 or less authors
        self.author_list_short = []
        for i in range(na_short):
            self.author_list_short.append(self.author_list_full[i])

        if na_short < self.Nauthor:
            self.author_list_short.append("et al")
    
    def generate_mainText_from_summary(self):
        """
            convert the "summary" from arxiv rss (v2) into mainText format.
        """
        
        maintext = self.title + "by " + ", ".join(self.author_list_short) + ". " \
            + self.summary

        return maintext

    def process_summary(self, raw_summary):
        return raw_summary.replace("$"," ") \
            .replace("Msun", " solar masses") \
            .replace("<", "less than") \
            .replace(">", "greater than") \
            .replace("\n", " ") \
            .replace("~", " about ")

def construct_alexa_dict(entry, updateDate_str):
    """
        1st version without author names..
        
        Example
    """
    this = ArticleEntry(entry, updateDate_str)
    data_dict = {}
    data_dict["uid"] = this.id
    data_dict["updateDate"] = this.updateDate
    data_dict["titleText"] = this.title
    data_dict["redirectionUrl"] = this.link
    data_dict["mainText"] = this.maintext
    
    return data_dict


logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route("/")
def main():
    feed = feedparser.parse(ARXIV_ASTROPH_URL)
    entrylist = []
    for ent in feed["entries"]:
        entrylist.append(ent)

    json_list = [ construct_alexa_dict(entrylist[i], feed['updated']) for i in range(5)]
    output = json.dumps(json_list)

# https://stackoverflow.com/questions/11945523/forcing-application-json-mime-type-in-a-view-flask
    resp = Response(response=output, status=200, mimetype="application/json")
    
    return resp

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


# https://github.com/alecxe/PlanetPythonSkill/blob/master/app.py