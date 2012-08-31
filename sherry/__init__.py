import jinja2
from flask import Flask
from sherry import converters
import os

app = Flask(__name__)
app.config.from_object('sherry.settings_default')
# Load from the environment variable if defined
app.config.from_envvar('SHERRY_SETTINGS_PATH', silent=True)

app.url_map.converters['mac'] = converters.MacConverter
app.jinja_env.undefined = jinja2.StrictUndefined

app.logger.addHandler(app.config['LOG_HANDLER'])
import sherry.views
