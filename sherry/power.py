"""
Drivers for OBM power on/off handling
"""

import subprocess


class PowerDriver(object):
    """Abstraction for powering on/off nodes"""

    def __init__(self, address, user, password, extra_data):
        self.address = address
        self.user = user
        self.password = password
        self.extra_data = extra_data

    def power_on(self):
        """Power the node on"""
        raise NotImplementedError()

    def power_off(self):
        """Power the node off"""
        raise NotImplementedError()

    def reboot(self):
        """Reboot the node"""
        self.power_off()
        self.power_on()


class IPMIDriver(PowerDriver):
    """Power on/off using ipmitool"""

    def _call_ipmitool(self, action):
        """Helper to call ipmitool"""
        subprocess.call(['/usr/bin/ipmitool',
                         '-H', str(self.address),
                         '-U', str(self.user),
                         '-P', str(self.password),
                         'power', str(action)])

    def power_on(self):
        self._call_ipmitool('on')

    def power_off(self):
        self._call_ipmitool('off')

    def reboot(self):
        self._call_ipmitool('cycle')


class QemuDriver(PowerDriver):
    """Power on/off Qemu/KVM virtual machines using virsh"""

    def _call_virsh(self, action):
        """Helper to call virsh"""
        instance_name = self.extra_data

        # XXX: requires libvirt to be configured for password-less operation
        subprocess.call(['/usr/bin/virsh'
                         '--connect',
                         'qemu://{0}@{1}/system'
                         .format(self.user, self.address),
                         str(action),
                         str(instance_name)])

    def power_on(self):
        self._call_virsh('on')

    def power_off(self):
        self._call_virsh('off')
