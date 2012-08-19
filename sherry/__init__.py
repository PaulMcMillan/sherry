from flask import Flask

app = Flask(__name__)
app.config.from_object('sherry.default_settings')

import sherry.views
