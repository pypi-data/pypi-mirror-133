Core API
========

.. py:module:: pyfingerd.core

These classes constitute the core of the pyfingerd module.

Base representations
--------------------

The following classes are objects used by other classes to represent users and
sessions.

.. autoclass:: FingerUser
	:members: login, name, last_login, home, shell, office, plan,
	          sessions

.. autoclass:: FingerSession
	:members: start, line, host, idle

The base interface class
------------------------

The following class is subclassed for making server interface classes.
For more information, consult :ref:`discuss-interfaces`.

.. autoclass:: FingerInterface
	:members: transmit_query, search_users

The base formatter class
------------------------

The following class is subclassed for making formatter classes.
For more information, consult :ref:`discuss-formatters`.

.. autoclass:: FingerFormatter
	:members: format_query_error, format_short, format_long,
	          _format_header, _format_footer

The server object
-----------------

.. autoclass:: FingerServer
	:members: start, stop, serve_forever
