import datetime
from . import SOURCES, app
from .helpers import *
from flask import render_template, make_response


@app.route("/")
def index():
    """ The index page. """
    # Get customized news headlines.
    source = get_value("source")
    articles = get_news(source)

    # Get customized weather info. 
    city = get_value("city")
    weather = get_weather(city)

    # Get customized rate info.
    currency_from, currency_to = get_value("currency_from"), get_value("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    # Set cookies.
    response = make_response(render_template("index.html", articles=articles,
                           source=source, weather=weather,
                           currency_from=currency_from, currency_to=currency_to,
                           rate=rate, currencies=currencies,
                           SOURCES=SOURCES))

    expires= datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("source", source, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)

    return response


@app.route("/code")
def code():
    """ The code page. """
    return render_template("code.html")
