import feedparser
from flask import Flask, render_template

app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"

@app.route("/")
def index():
    feed = feedparser.parse(BBC_FEED)
    return render_template("index.html", feed=feed.get('entries'))


if __name__ == "__main__":
    app.run()