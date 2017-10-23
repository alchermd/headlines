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


from .helpers import get_sources

SOURCES = {source:source for source in get_sources()}

DEFAULTS = {
    "source": "bbc-news",
    "city": "Malolos",
    "currency_from": "USD",
    "currency_to": "PHP"
}

from . import views