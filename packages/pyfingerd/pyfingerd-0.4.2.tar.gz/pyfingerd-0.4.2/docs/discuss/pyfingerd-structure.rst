pyfingerd structure
===================

pyfingerd's conception is centered around the server class,
:py:class:`pyfingerd.core.FingerServer`, which itself makes use of
two other objects: an interface and a formatter.

.. _discuss-interfaces:

Interfaces
----------

An interface provides the data presented by the server to the client.

Interfaces in pyfingerd are subclasses of
:py:class:`pyfingerd.core.FingerInterface`. Interfaces must override
the methods from this class, mostly the one to search for users, in
order to provide data from their source.

Usable interfaces throughout pyfingerd are the following:

:py:class:`pyfingerd.core.FingerInterface`

	Base class and dummy interface, doesn't transmit nor yield any user
	results.

:py:class:`pyfingerd.fiction.FingerScenarioInterface`

	Interface following a scenario; see :ref:`fictional-interfaces` for
	more information.

:py:class:`pyfingerd.posix.FingerPOSIXInterface`

    Interface using the POSIX user accounting databases.

:py:class:`pyfingerd.native.FingerNativeInterface`

    Interface bound to the one using native system interface:

    * :py:class:`pyfingerd.posix.FingerPOSIXInterface` if on Linux or \*BSD.
    * :py:class:`pyfingerd.core.FingerInterface` by default.

.. _discuss-formatters:

Formatters
----------

A formatter takes data obtained by the server for a given request through
its interface, and presents it using text.

Formatters in pyfingerd are subclasses of
:py:class:`pyfingerd.core.FingerFormatter`. Existing formatters
throughout pyfingerd are the following:

:py:class:`pyfingerd.core.FingerFormatter`

	Base class, outputs similarly to RFC 1288.
