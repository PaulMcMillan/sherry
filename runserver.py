#!/usr/bin/env python
from sherry import app

# Load debug config
app.config.from_pyfile('../sherry.conf', silent=False)

app.run(host='0.0.0.0', port=5000, debug=True)

