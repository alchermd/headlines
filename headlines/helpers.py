import json
import requests
from . import SOURCES, DEFAULTS, app
from flask import request
from urllib.request import quote, urlopen


def get_news(source):
    if source is None or source not in SOURCES.keys():
        source = DEFAULTS["source"]
    else:
        source = source.lower()

    r = requests.get(f"https://newsapi.org/v1/articles?source={SOURCES[source]}&sortBy=top&apiKey={app.config['NEWS_API_KEY']}")
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
