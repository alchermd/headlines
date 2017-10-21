import requests
from flask import Flask, render_template

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("appconfig.py")

sources = {
    "bbc": "bbc-news",
    "cnn": "cnn",
    "hackernews": "hacker-news"
}

def create_link(source):
    if source in sources.keys():
        return f"https://newsapi.org/v1/articles?source={sources[source]}&sortBy=top&apiKey={app.config['API_KEY']}"
    

@app.route("/")
@app.route("/<source>")
def index(source="bbc"):
    r = requests.get(create_link(source))
    return render_template("index.html", articles=r.json().get("articles"), source=source)


if __name__ == "__main__":
    app.run()