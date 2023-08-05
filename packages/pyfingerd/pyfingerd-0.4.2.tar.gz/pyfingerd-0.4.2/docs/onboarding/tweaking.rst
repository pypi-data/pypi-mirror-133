Tweaking pyfingerd
==================

In order to start tweaking pyfingerd using Python instead of the CLI, you
can import utilities from the module. The minimal code for running the
server is the following:

.. code-block:: python

	from pyfingerd import FingerServer

	server = FingerServer()
	server.serve_forever()

For more information, please consult the discussion topics and API reference
on the current documentation.
