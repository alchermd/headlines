# -*- coding: utf-8 -*-
"""
    headlines 
    ~~~~~~~~~

    A Flask powered news aggregation web app.
    
    :copyright: (c) 2017, John Alcher
    :license: MIT, see LICENSE for more info.
"""
from flask import Flask

# Instantiate a new Flask application.
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("appconfig.py")

# Circular imports.
# TODO: Look for better ways to refactor this bit.
from .helpers import get_sources

# Set global values.
# TODO: Find a way to somehow place these in the Flask.g object 
SOURCES = get_sources()

DEFAULTS = {
    "source": "bbc-news",
    "city": "Malolos",
    "currency_from": "USD",
    "currency_to": "PHP"
}

# Another ciruclar import.
from . import views