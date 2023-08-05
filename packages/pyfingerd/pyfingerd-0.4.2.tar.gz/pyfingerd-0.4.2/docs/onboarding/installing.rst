Installing pyfingerd
====================

In order to run and tweak pyfingerd, you must first install it; this section
will cover the need.

Installing pyfingerd using pip
------------------------------

To install pyfingerd, you can use pip with the following command:

.. code-block:: sh

	python -m pip install pyfingerd

Some notes on this command:

* On most Linux distributions, you can directly call ``pip`` (or ``pip3``
  on those where Python 2.x is still the default); I personnally prefer
  to call it through Python as a module.
* On Linux and other UNIX-like distributions where Python 2.x is still the
  default, when Python 3.x is installed, you must usually call it using
  ``python3`` instead of ``python``.
* On Microsoft Windows, the Python executable, when added to the PATH,
  goes by the name ``py`` instead of ``python``.

Installing pyfingerd from source
--------------------------------

To install pyfingerd from source, you can use the following commands:

.. code-block:: sh

    python -m pip install -r requirements.txt
    python ./setup.py install --system # or --user

.. _toml: https://pypi.org/project/toml/
.. _click: https://pypi.org/project/click/
