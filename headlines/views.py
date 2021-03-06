import datetime
from . import SOURCES, app
from .forms import EmailForm
from .helpers import *
from flask import flash, make_response, redirect, render_template, url_for


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


@app.route("/code", methods=["GET", "POST"])
def code():
    """ The code page. """
    form = EmailForm()
    form_errors = None
    if form.validate_on_submit():
        # Send the email.
        send_email(form.reply_to.data, form.message.data)

        # Redirect to the same endpoint.
        flash("Email Sent!", "success")
        return redirect(url_for('code'))
    
    else:
        form_errors = form.errors
    
    return render_template("code.html", form=form, form_errors=form_errors)
