Running pyfingerd
=================

Once installed, you can directly run pyfingerd with its default options
through the following command, **as root**:

.. code-block:: sh

	python3 -m pyfingerd

By default, this will run a finger server on TCP port 79 for both Internet
protocols (IPv4 and IPv6) if available, returning native information if
implemented or dummy information (no users) if not.

Setting up your finger client
-----------------------------

If you haven't already, you should get a client for testing your finger
server. It is recommended to use the original, finger client from BSD,
by using one of the following packages:

* Debian and derivatives: run ``sudo apt-get install finger``.
* Fedora and derivatives: install ``dnf install finger``.
* Archlinux and derivatives: install ``netkit-bsd-finger`` or
  ``netkit-bsd-finger-ipv6`` (both AUR packages) using your favourite
  pacman frontend.

Once installed and your server is running, you should be able to run
``finger`` on the command-line. The default syntax doesn't query any server;
the syntaxes are the following:

.. code-block:: sh

    # List connected users.
    finger @localhost

    # List connected users in the 'long' format.
    finger -l @localhost

    # Search for a given user.
    finger user@localhost

    # Ask for request forwarding.
    finger user@example.org@localhost

Other options exist; for example, the Castor_ browser allows `finger URLs`_
for querying finger servers.

Finger being a simple protocol, you can also use any raw TCP utility for
making requests; Socat_ is a renown one. Example commands using Socat_ are
the following:

.. code-block:: sh

    # List connected users.
    echo | socat - tcp:localhost:79

    # List connected users in the 'long' format.
    echo '/W' | socat - tcp:localhost:79

    # Search for a given user.
    echo 'user' | socat - tcp:localhost:79

    # Ask for request forwarding
    echo 'user@example.org' | socat - tcp:localhost:79

If you choose this option, you might want to familiarize yourself
with `RFC 1288`_, since you're doing the requests yourself.

Using a different port
----------------------

Due to historical reasons, on UNIX-like systems, by default, TCP ports below
1024 are considered "privileged ports", which means a program needs to be
run as root (uid 0) to bind that port. Although on Linux, this is configurable
(see `ip_unprivileged_port_start`_), it is rarely done in practice.

However, running a network server program in root is considered a bad security
practice. Usually, application servers are run on a custom unprivileged port
(usually 3000, 5000 or 8000 in my experience) and a load balancer, usually
Apache or nginx for HTTP and HTTPS services, redirects traffic to that custom
port.

Although pyfingerd seems harmless, it is recommended to run it as an
unprivileged user that only can access the required data,
usually session information from the host in its default configuration.
In order for it to still be able to listen to requests and answer on TCP
port 79, one possibility is to attribute a custom port to it, such as 3999,
and redirect all inbound traffic on port 79 to that custom port using
iptables. This can be done by appending a rule to the NAT table using a
command such as the following:

.. code-block:: sh

	iptables -t nat -A OUTPUT -p tcp [-s <source ip>] [-d <destination ip>] --dport 79 -j DNAT --to '<ip:port>'

For example, if the pyfingerd server is running on port 3999, we can use both
these commands to redirect traffic to that server:

.. code-block:: sh

	iptables -t nat -A OUTPUT -p tcp -d 127.0.0.1 --dport 79 -j DNAT --to 127.0.0.1:3999
	ip6tables -t nat -A OUTPUT -p tcp -d ::1 --dport 79 -j DNAT --to '[::1]:3999'

Or, if you only want to accept request from localhost, you can also make use of
the ``-s`` option to only accept traffic from localhost:

.. code-block:: sh

	iptables -t nat -A OUTPUT -p tcp -s 127.0.0.1 -d 127.0.0.1 --dport 79 -j DNAT --to 127.0.0.1:3999
	ip6tables -t nat -A OUTPUT -p tcp -s ::1 -d ::1 --dport 79 -j DNAT --to '[::1]:3999'

However, you must think of listening on port 3999 on the command-line, by
using the following command-line option:

.. code-block:: sh

	python3 -m pyfingerd -b localhost:3999
	# OR
	BIND=localhost:3999 python3 -m pyfingerd

See :ref:`cli` for more information.

Setting the hostname
--------------------

By default, pyfingerd uses the hostname ``localhost`` when answering to
requests. Say you want the server to answer with the ``EXAMPLE.ORG``
hostname. You can do so using the following command-line option:

.. code-block:: sh

	python3 -m pyfingerd -H example.org
	# OR
	FINGER_HOST=example.org python3 -m pyfingerd

.. _Castor: https://sr.ht/~julienxx/Castor/
.. _finger URLs: http://tools.ietf.org/html/draft-ietf-uri-url-finger
.. _Socat: https://sectools.org/tool/socat/
.. _`ip_unprivileged_port_start`: https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt
.. _RFC 1288: https://datatracker.ietf.org/doc/html/rfc1288
