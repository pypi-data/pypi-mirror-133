.. _cli:

Configuration options
=====================

When run through CLI, pyfingerd exposes a number of configuration options using
its own code. Each configuration option is configurable through three
cumulative means:

 * A UNIX-style command-line option.
 * An environment variable set directly.
 * An environment variable set through a dotenv file (``.env``).

When a configuration option is given through multiple means, the resolution
order of such the value is the one given above.

Binding
-------

As for all network servers, pyfingerd will bind one or more network ports and
answer to queries from all of the bound ports. These network ports are
defined through the following option:

 * The ``-b`` or ``--binds`` CLI option.
 * The ``BIND`` or ``BINDS`` environment variable.

This option must be defined one way or another, and must contain the list
of ports to bind separated with commas (``,``). Each port must have one of
the following formats:

``example.com``
	Bind on all addresses that ``example.com`` resolve as (IPv4 and IPv6),
	port 79.

``example.com:1234``
	Bind on all addresses that ``example.com`` resolve as (IPv4 and IPv6),
	port 1234.

``1.2.3.4`` or ``[1.2.3.4]``
	Bind on ``1.2.3.4`` (IPv4), port 79.

``1.2.3.4:1234`` or ``[1.2.3.4]:1234``
	Bind on ``1.2.3.4`` (IPv4), port 1234.

``::1:2:3:4`` or ``[::1:2:3:4]``
	Bind on ``::1:2:3:4`` (IPv6) port 79.

``[::1:2:3:4]:1234``
	Bind on ``::1:2:3:4`` (IPv6) port 1234.

Here are some examples:

.. code-block:: bash

	# On modern platforms, binds on 127.0.0.1:79 (IPv4)
	# and [::1]:79 (IPv6).
	BIND=localhost

	# Binds on 1.2.3.4:3331 and [2001:41d0:302:2200::3b2]:79.
	BIND="1.2.3.4:3331,[2001:41d0:302:2200::3b2]:79"
	BIND="1.2.3.4:3331,2001:41d0:302:2200::3b2"

Setting the hostname
--------------------

The pyfingerd server answers queries with a given hostname to identify itself.
This hostname can be configured through the following option:

 * The ``-H`` or ``--hostname`` CLI option.
 * The ``FINGER_HOST`` environment variable.

It is optional and defined to ``LOCALHOST`` by default.

Defining the server type
------------------------

For answering queries, the information provided by the server can come from
different sources. The server type represents the source of the information,
and can be configured through the following option:

 * The ``-t`` or ``--type`` CLI option.
 * The ``FINGER_TYPE`` environment variable.

The possible values for this option are the following:

``DUMMY``
	There is no data (no users, no sessions).

``NATIVE``
	The data is gathered from the system.

``SCENARIO``
	The data is gathered from a scenario (see :ref:`cli-scenario` below).

By default, the interface type is ``NATIVE``. If an invalid server type is
provided, the server is considered a dummy server.

.. _cli-scenario:

Defining the scenario
---------------------

When the server is a scenario server, the path to a scenario in the TOML
format must be provided. This path must then be configured through the
following option:

 * The ``-s`` or ``--scenario`` CLI option.
 * The ``FINGER_ACTIONS`` environment variable.

The destination file must be a TOML file representing a scenario;
see :ref:`scenario-files` for more information.
