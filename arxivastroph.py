from flask import Flask, jsonify, Response
import feedparser
from html.parser import HTMLParser
import dateutil.parser

ARXIV_ASTROPH_URL = "http://arxiv.org/rss/astro-ph?version=2.0"

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.recording_p = 0
        self.authors = set()
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
            self.authors.add(data)
        if self.recording==0 and self.recording_p==1:
            self.summary = data

def generate_mainText_from_summary(entry_summary_html):
    """
        convert the "summary" from arxiv rss (v2) into mainText format.
    """
    parser = Parser()
    parser.feed(entry_summary_html)
    author_list = list(parser.authors)
    title = entry['title'].split(' (arXiv')[0]
    summary = parser.summary
    Nauthor = len(author_list)
    
    return summary


def construct_alexa_dict(entry, updateDate):
    """
        1st version without author names..
        
        Example
    """
    data_dict = {}
    data_dict["uid"] = entry['id']
    data_dict["updateDate"] = updateDate
    data_dict["titleText"] = entry['title'].split(' (arXiv')[0]
    data_dict["redirectionUrl"] = entry['link']
    data_dict["mainText"] = generate_mainText_from_summary(entry['summary'])
    
    return data_dict

import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route("/")
def main():
    feed = feedparser.parse(ARXIV_ASTROPH_URL)
    entrylist = []
    for ent in feed["entries"]:
        entrylist.append(ent)

    json_list = [ construct_alexa_dict(entrylist[i], dateutil.parser.parse(feed['updated']).strftime("%Y-%m-%dT%H:%M:%S.%fZ")) for i in range(5)]
    output = json.dumps(json_list)

# https://stackoverflow.com/questions/11945523/forcing-application-json-mime-type-in-a-view-flask
    resp = Response(response=output, status=200, mimetype="application/json")
    
    return resp

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


# https://github.com/alecxe/PlanetPythonSkill/blob/master/app.py