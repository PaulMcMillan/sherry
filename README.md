Sherry
======

Sherry is a quick, easy-to-use, low-overhead server to deal with a
very specific PXE configuration:

 - machines always boot from pxe
 - pxe server tells machines to boot from disk
 - except when told to reimage with a specific image

This approach is especially useful in test and dev environments, with
machines that need to be conditionally rebuilt from time to time.

Sherry is designed to retain state for as little time as
possible. Store configuration information, mac addresses, OBM IPs, and
the like in the calling scripts, rather than the machine which does
the reimaging.

For more complicated setups, there's always Cobbler. But forking
Sherry might be faster than configuring Cobbler.

Installation
------------

Sherry depends on Flask, dnsmasq, and ipxe. Installing the deb will
install the sherry specific dnsmasq boot script, but you are responsible for
making dnsmasq serve dhcp and tftp.

You'll need to make sure your `/etc/dnsmasq.conf` contains these lines:

    enable-tftp
    tftp-root=/usr/lib/ipxe/ # or your equivalent
    conf-dir=/etc/dnsmasq.d

You will also need to configure your webserver of choice to serve
sherry at the URL specified during installation (in
`/etc/dnsmasq.d/sherry`). You must also serve your initrd and kernel,
and any additional files which may be required (e.g. by
initramfs-tools).


Sherry Cobbler
--------------
 - 4 oz dry Sherry
 - 3 slices orange
 - 2 bar-spoons sugar

Shake all ingredients hard with ice and pour, unstrained, in to a tall
glass. Garnish with fresh berries then add a straw.
