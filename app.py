import requests
from flask import Flask, render_template

app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
API_KEY = "c4002216fa5446d582b5f31d73959d36"

@app.route("/")
def index():
    r = requests.get(
        f"https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey={API_KEY}"
    )
    return render_template("index.html", articles=r.json().get("articles"))


if __name__ == "__main__":
    app.run()