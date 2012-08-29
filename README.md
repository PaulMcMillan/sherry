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

Sherry depends on Flask, gunicorn, dnsmasq, and iPXE. Installing the
deb will install the sherry specific dnsmasq boot script, and
configure dnsmasq to serve tftp, but you are responsible for making
dnsmasq serve dhcp.

You'll need to make sure your `/etc/dnsmasq.conf` contains this line:

    conf-dir=/etc/dnsmasq.d

Sherry installs and configures nginx to serve the sherry app, as well
as the image files.

Usage
-----
Control flow with Sherry is roughly like this:

 - Client PXE Boots, gets DHCP from dnsmasq
 - Client downloads and boots iPXE
 - iPXE downloads `/pxe/<mac_address>`
 - Server sends
   - `boot.pxe` if the mac is unknown.
   - `install.pxe` if mac is known. Server removes mac from list.
 - Client boots from disk or via provided initrd, kernel, and kernel
   parameters.

In normal use, clients always get redirected to boot from disk. When a
client needs to be reimaged, make a request (GET or POST) to
`/reimage` with these parameters:

 - `mac_address`
 - `obm_address`
 - `release`
 - `kernel_opts`

Sherry will use the `obm_address` (and configured obm credentials) to
reboot the client. When it restarts, it will boot using

 - `kernel http://{SERVER_NAME}/releases/{release}/vmlinuz {kernel_opts}`
 - `initrd http://{SERVER_NAME}/releases/{release}/initrd.img`

Security
--------

Sherry deliberately has no security mechanisms. Don't expose it to a
public network.

Sherry Cobbler
--------------
 - 4 oz dry Sherry
 - 3 slices orange
 - 2 bar-spoons sugar

Shake all ingredients hard with ice and pour, unstrained, in to a tall
glass. Garnish with fresh berries then add a straw.
