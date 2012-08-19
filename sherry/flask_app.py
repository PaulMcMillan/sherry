from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
app.config.from_object('sherry.default_settings')
#app.config.from_envvar('SHERRY_SETTINGS')

systems_to_install = {'mac_addr': {'release':123, 'kernel_opts':'foobar'}}

@app.route('/')
def foo():
    return "%s\n%s" % (app.config['SERVER_NAME'], systems_to_install)

@app.route('/pxe/chain.pxe', methods=['GET'])
def chain_pxe():
    return render_template('chain.pxe')

@app.route('/pxe/<mac_address>', methods=['GET'])
def sort_system(mac_address):
    if mac_address not in systems_to_install:
        return render_template('boot.pxe')
    system_info = systems_to_install[mac_address]
    return render_template('install.pxe', **system_info)

# This allows both methods for convenience. Bookmark reimage ftw!
@app.route('/install', methods=['GET', 'POST'])
def install():
    # ipmi_address
    # mac_address
    # release
    # kernel_opts
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=24602)
