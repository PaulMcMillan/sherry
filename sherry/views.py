"""
Flask views and routes for controlling pxe booting.
"""

import logging

from flask import render_template
from flask import request

from sherry import app
from sherry import converters

log = logging.getLogger(__name__)

# This stores the list of servers that need to be imaged
reimage_queue = {}


@app.route('/')
def index():
    return "%s\n%s" % (app.config['SERVER_NAME'], reimage_queue)


@app.route('/pxe/chain.pxe', methods=['GET'])
def chain_pxe():
    return render_template('chain.pxe')


@app.route('/pxe/<mac:mac_address>', methods=['GET'])
def boot_or_reimage(mac_address):
    if mac_address not in reimage_queue:
        log.info('Served {} boot.pxe'.format(mac_address))
        return render_template('boot.pxe')
    # Remove the system from the queue
    system_info = reimage_queue.pop(mac_address)
    log.info('Served {} install.pxe with info {!s}'.format(
            mac_address, system_info))
    return render_template('install.pxe', **system_info)


# allows both HTTP methods for convenience. Bookmark reimage ftw!
@app.route('/reimage', methods=['GET', 'POST'])
def reimage():
    """ Initiate a reimage of the target system.
    Parameters:
    - obm_address
    - mac_address
    - release
    - kernel
    """
    request_values = request.values.to_dict()
    obm_address = request_values.pop('obm_address')
    mac_address = converters.strip_mac(request_values.pop('mac_address'))

    # Render the template to make sure that no values are missing
    render_template('install.pxe', **request_values)

    # store the rest of the parameters to render the template
    reimage_queue[mac_address] = request_values

    powerdriver = app.config['POWER_DRIVER'](obm_address,
                                             app.config['OBM_USERNAME'],
                                             app.config['OBM_PASSWORD'])
    power_results = powerdriver.reboot()
    return ("Reimaging {mac_address} at {obm_address}. \n"
            "Power command results: {power_results}".format(**locals()))
