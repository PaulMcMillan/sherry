import jinja2
from flask import Flask
from sherry import converters

app = Flask(__name__)
app.config.from_object('sherry.default_settings')
app.url_map.converters['mac'] = converters.MacConverter
app.jinja_env.undefined = jinja2.StrictUndefined

import sherry.views
