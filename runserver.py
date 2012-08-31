#!/usr/bin/env python
import os

# Load debug config
os.environ['SHERRY_SETTINGS_PATH'] = os.path.join(os.getcwd(), 'sherry.conf')

from sherry import app

app.run(host='0.0.0.0', port=5000, debug=True)
