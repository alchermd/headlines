import datetime
import json
import requests
from flask import Flask, render_template, request, make_response
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


def get_value(key):
    if request.args.get(key):
        return request.args.get(key)
    else:
        return request.cookies.get(key) or DEFAULTS[key]


@app.route("/")
def index():
    # Get customized news headlines.
    source = get_value("source")
    articles = get_news(source)

    # Get customized weather info. 
    city = get_value("city")
    print("City is " + str(city))
    weather = get_weather(city)

    # Get customized rate info.
    currency_from, currency_to = get_value("currency_from"), get_value("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    # Set cookies.
    response = make_response(render_template("index.html", articles=articles,
                           source=source, weather=weather,
                           currency_from=currency_from, currency_to=currency_to,
                           rate=rate, currencies=currencies))

    expires= datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("source", source, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)

    return response


if __name__ == "__main__":
    app.run()