"""
Drivers for OBM power on/off handling
"""

import logging
import subprocess

# FIXME (PaulM): I'm not entirely happy with this
from sherry import app
log = app.logger


class PowerDriver(object):
    """Abstraction for powering on/off nodes"""

    def __init__(self, address, user, password):
        self.address = address
        self.user = user
        self.password = password

    def power_on(self):
        """Power the node on"""
        raise NotImplementedError()

    def power_off(self):
        """Power the node off"""
        raise NotImplementedError()

    def status(self):
        """Get node power status"""
        raise NotImplementedError()

    def reboot(self):
        """Reboot the node"""
        off = self.power_off()
        on = self.power_on()
        return "%s\n%s" % (off, on)


class MockPowerDriver(PowerDriver):
    """A power driver that does nothing but log the requests"""

    def power_on(self):
        log.debug('Powering on at {0}@{1}, passwd: %{2}'
                  .format(self.user, self.address, self.password))

    def power_off(self):
        log.debug('Powering off at {0}@{1}, passwd: %{2}'
                  .format(self.user, self.address, self.password))

    def reboot(self):
        log.debug('Rebooting at {0}@{1}, passwd: %{2}'
                  .format(self.user, self.address, self.password))


class IPMIDriver(PowerDriver):
    """Power on/off using ipmitool"""

    IPMITOOL_PATH = '/usr/bin/ipmitool'

    def _call_ipmitool(self, action):
        """Helper to call ipmitool"""
        log.info('IPMI power {action}. {self.user}@{self.address}'.format(
                action=action, self=self))
        return subprocess.check_output([self.IPMITOOL_PATH,
                                        '-H', str(self.address),
                                        '-U', str(self.user),
                                        '-P', str(self.password),
                                        'power', str(action)])

    def power_on(self):
        return self._call_ipmitool('on')

    def power_off(self):
        return self._call_ipmitool('off')

    def status(self):
        return self._call_ipmitool('status')

    def reboot(self):
        # not all devices can cycle from 'off'
        try:
            return self._call_ipmitool('cycle')
        except subprocess.CalledProcessError:
            return self.power_on()


class QemuDriver(PowerDriver):
    """Power on/off Qemu/KVM virtual machines using virsh"""

    def _call_virsh(self, action):
        """Helper to call virsh"""
        log.info('Qemu power {action}. {self.user}@{self.address}'.format(
                action=action, self=self))
        # XXX: requires libvirt to be configured for password-less operation
        return subprocess.check_output([
                '/usr/bin/virsh'
                '--connect',
                'qemu://127.0.0.1@{1}/system'.format(self.user),
                str(action),
                str(self.address)])

    def power_on(self):
        return self._call_virsh('on')

    def power_off(self):
        return self._call_virsh('off')
