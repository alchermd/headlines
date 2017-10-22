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
    "city": "Malolos",
    "currency_from": "USD",
    "currency_to": "PHP"
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
                    "city": parsed["name"],
                    "country": parsed["sys"]["country"]
                  }
    return weather


def get_rate(frm, to):
    # Load rate data.
    api_url = f"https://openexchangerates.org/api/latest.json?app_id={app.config['RATES_API_KEY']}"
    all_currency = urlopen(api_url).read()
    parsed = json.loads(all_currency).get("rates")
    
    # Get the appropriate conversion.
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


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

    # Get customized rate info.
    currency_from = request.args.get("currency_from") or DEFAULTS["currency_from"]
    currency_to = request.args.get("currency_to") or DEFAULTS["currency_to"]
    rate, currencies = get_rate(currency_from, currency_to)

    return render_template("index.html", articles=articles,
                           source=source, weather=weather,
                           currency_from=currency_from, currency_to=currency_to,
                           rate=rate, currencies=currencies)


if __name__ == "__main__":
    app.run()