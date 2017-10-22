# -*- coding: utf-8 -*-
"""
    headlines 
    ~~~~~~~~~

    A Flask powered news aggregation web app.
    
    :copyright: (c) 2017, John Alcher
    :license: MIT, see LICENSE for more info.
"""
from flask import Flask


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("appconfig.py")

SOURCES = {
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

from . import views