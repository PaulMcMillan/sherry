from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
app.config.from_object('sherry.default_settings')
#app.config.from_envvar('SHERRY_SETTINGS')

reimage_queue = {'mac_addr': {'release':123, 'kernel_opts':'foobar'}}

@app.route('/')
def foo():
    return "%s\n%s" % (app.config['SERVER_NAME'], reimage_queue)

@app.route('/pxe/chain.pxe', methods=['GET'])
def chain_pxe():
    return render_template('chain.pxe')

@app.route('/pxe/<mac_address>', methods=['GET'])
def boot_or_reimage(mac_address):
    # TODO (PaulM): regularize the mac address
    if mac_address not in reimage_queue:
        return render_template('boot.pxe')
    # Remove the system from the queue
    system_info = reimage_queue.pop(mac_address)
    return render_template('install.pxe', **system_info)

# allows both HTTP methods for convenience. Bookmark reimage ftw!
@app.route('/reimage', methods=['GET', 'POST'])
def reimage():
    """ Initiate a reimage of the target system.
    Parameters:
    - ipmi_address
    - mac_address
    - release
    - kernel
    """
    req_vals = request.values.to_dict()
    ipmi_address = req_vals.pop('ipmi_address')
    mac_address = req_vals.pop('mac_address')
    # store the rest of the parameters to render the template
    reimage_queue[mac_address] = req_vals
    # TODO (PaulM): pre-render the template(s) with these values here
    powerdriver = app.config['POWER_DRIVER'](ipmi_address, 'user', 'pass')
    powerdriver.reboot()
    return "it might have worked..."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=24602)
