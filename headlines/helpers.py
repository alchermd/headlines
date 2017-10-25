import json
import requests
import smtplib
from . import app
from flask import request
from urllib.request import quote, urlopen


def get_news(source) -> list:
    """ Fetches articles from the news API.
    
    Args:
        source (str): The name of the news source to use.

    Returns:
        list: A list of news articles.
    """
    from . import DEFAULTS, SOURCES

    # Determine fallback values.
    if source is None or source not in SOURCES.keys():
        source = DEFAULTS["source"]
    else:
        source = source.lower()

    # Fetch data from the API.
    r = requests.get(f"https://newsapi.org/v1/articles?source={SOURCES[source]}&sortBy=top&apiKey={app.config['NEWS_API_KEY']}")
    
    return r.json().get("articles")


def get_weather(city) -> dict:
    """ Fetches weather info from the OpenWeatherMap API.
    
    Args:
        city (str): The city in which to fetch info on.  

    Returns:
        dict: A dictionary containing the fetched weather info.
    """
    # Fetch weather data from API.
    city = quote(city)
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={app.config['WEATHER_API_KEY']}"
    data = urlopen(api_url).read()

    # Parse json data.
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


def get_rate(frm, to) -> tuple:
    """ Fetches forex rate from the OpenExchangeRates API.
    
    Args:
        frm (str): Currency to exchange from.
        to (str): Currency to exchange to.  

    Returns:
        tuple: Contains the conversion rate and the currencies
            available from the API.
    """
    # Load rate data.
    api_url = f"https://openexchangerates.org/api/latest.json?app_id={app.config['RATES_API_KEY']}"
    all_currency = urlopen(api_url).read()
    parsed = json.loads(all_currency).get("rates")
    
    # Get the appropriate conversion.
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())

    return (to_rate / frm_rate, parsed.keys())


def get_value(key) -> str:
    """ Determines the value to be used.
    The GET variables, cookies, and DEFAULTS dictionary are
    prioritized in that order.

    Args:
        key (str): The string to search as key.

    Returns:
        str: The determined result to be used.
    """
    from . import DEFAULTS

    if request.args.get(key):
        return request.args.get(key)
    else:
        return request.cookies.get(key) or DEFAULTS[key]


def get_sources() -> dict:
    """ Loads and parses all the news sources provided by
    the NewsAPI.org API.

    Returns:
        dict: A dictionary of all the news sources where the
            key and value are the same.
    """
    # Load sources data.
    api_url = f"https://newsapi.org/v1/sources"
    all_sources = urlopen(api_url).read()
    parsed = json.loads(all_sources).get("sources")

    # Parse sources.
    sources = {source["id"]:source["id"] for source in parsed}
    return sources


def send_email(reply_to: str, message: str):
    """ Sends an email to the configured recepient.

    Args:
        reply_to: the email address to reply to.
        message: the message of the email to be sent.
    """
    body = "\r\n".join([
        f"From: {reply_to}",
        f"To: {app.config['MY_EMAIL']}",
        "Subject: Headlines App Message",
        "",
        f"From:{reply_to} \n{message}"
    ])

    # Start an SMPT server and connect it to Gmail.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()

    # Start a TSL session to login email credentials.
    mail.starttls()
    mail.login(app.config['MY_EMAIL'], app.config['MY_EMAIL_PASSWORD'])

    # Send the message and close the server.
    mail.sendmail(app.config['MY_EMAIL'], app.config['MY_EMAIL'], body)
    mail.close()