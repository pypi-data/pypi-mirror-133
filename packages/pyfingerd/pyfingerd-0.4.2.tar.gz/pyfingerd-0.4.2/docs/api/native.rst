Native API
==========

For native integration of pyfingerd, the project provides interfaces for
reading system information in order to expose it through the server.

Note that the relevant native interface for the host system (or the dummy
interface if none are relevant) is accessible through
:py:class:`pyfingerd.native.FingerNativeInterface`.

.. py:module:: pyfingerd.posix

.. autoclass:: FingerPOSIXInterface
    :members: search_users
