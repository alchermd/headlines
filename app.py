import requests
from flask import Flask, render_template

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("appconfig.py")

BBC_id= "bbc-news"

@app.route("/")
def index():
    r = requests.get(
        f"https://newsapi.org/v1/articles?source={BBC_id}&sortBy=top&apiKey={app.config['API_KEY']}"
    )
    return render_template("index.html", articles=r.json().get("articles"))


if __name__ == "__main__":
    app.run()