"""
Flask views and routes for controlling pxe booting.
"""

import logging
import jinja2

from flask import render_template
from flask import request

from sherry import app
from sherry import converters

log = app.logger

# This stores the list of servers that need to be imaged
reimage_queue = {}


@app.route('/')
def index():
    return render_template('index.html', reimage_queue=reimage_queue)


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
    - location
    - kernel_opts
    """
    request_values = request.values.to_dict()
    if len(request_values) == 0:
        return render_template('reimage.html', message='')

    # Eventually we should use better form handling here. Django?
    try:
        obm_address = request_values.pop('obm_address')
        mac_address = converters.strip_mac(request_values.pop('mac_address'))
        # Render the template to make sure that no values are missing
        render_template('install.pxe', **request_values)
    except (KeyError,jinja2.exceptions.UndefinedError):
        message = ('Could not reimage. Incorrect or missing arguments. '
                   'Args: %s' % request.values.to_dict())
        log.warning(message)
        return render_template('reimage.html', message=message)

    # store the rest of the parameters to render the template
    reimage_queue[mac_address] = request_values

    powerdriver = app.config['POWER_DRIVER'](obm_address,
                                             app.config['OBM_USERNAME'],
                                             app.config['OBM_PASSWORD'])
    power_results = powerdriver.reboot()

    message = ("Reimaging {mac_address} at {obm_address}. "
               "Power command results: {power_results}".format(**locals()))
    log.info(message)
    return render_template('reimage.html', message=message)


@app.route('/log')
def display_log():
    """ Display the last 50 lines of log messages """
    with open(app.logger.handlers[1].baseFilename) as f:
        log = f.readlines()
    return render_template('log.html', log=log[-50:])

