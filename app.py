import json
import requests
from flask import Flask, render_template, request
from urllib.request import quote, urlopen

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("appconfig.py")

sources = {
    "bbc": "bbc-news",
    "cnn": "cnn",
    "hackernews": "hacker-news"
}

DEFAULTS = {
    "source": "bbc",
    "city": "Malolos"
}


def get_news(source):
    if source is None or source not in sources.keys():
        source = DEFAULTS["source"]
    else:
        source = source.lower()

    r = requests.get(f"https://newsapi.org/v1/articles?source={sources[source]}&sortBy=top&apiKey={app.config['NEWS_API_KEY']}")
    return r.json().get("articles")


def get_weather(city):
    city = quote(city)
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={app.config['WEATHER_API_KEY']}"
    data = urlopen(api_url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {
                    "description": parsed["weather"][0]["description"],
                    "temperature": parsed["main"]["temp"],
                    "city": parsed["name"]
                  }
    return weather


@app.route("/")
def index():
    # Get customized news headlines.
    source = request.args.get("source")
    if source is None or source.lower() not in sources.keys():
        source = DEFAULTS["source"]
    else:
        source = source.lower()
    articles = get_news(source)

    # Get customized weather info.
    city = request.args.get("city")
    if city is None:
        city = DEFAULTS["city"]
    weather = get_weather(city)

    return render_template("index.html", articles=articles,
                           source=source, weather=weather)


if __name__ == "__main__":
    app.run()