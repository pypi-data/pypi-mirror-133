Welcome to pyfingerd's documentation!
=====================================

finger is both a protocol and a utility to get the information and status
from a user on a distant machine. It was standardized in `RFC 742`_
in 1977, then in `RFC 1288`_ in 1991, and has been abandoned since.

pyfingerd is an implementation for this protocol, which allows you to:

* Run a finger server using system information on Linux and \*BSD systems.
* Run a finger server using a scenario for animating alternate reality games
  or confusing potential attackers.
* Implement your own finger server in Python using sensible defaults.

For more information, you can consult:

* The project homepage at `pyfingerd.touhey.pro`_.
* The PyPI project page at `pypi.org`_.
* The source at `forge.touhey.org`_.

The documentation contents is the following:

.. toctree::
    :maxdepth: 3

    onboarding
    guides
    discuss
    cli
    api

.. _RFC 742: https://tools.ietf.org/html/rfc742
.. _RFC 1288: https://tools.ietf.org/html/rfc1288
.. _`pyfingerd.touhey.pro`: https://pyfingerd.touhey.pro/
.. _`pypi.org`: https://pypi.org/project/pyfingerd/
.. _`forge.touhey.org`: https://forge.touhey.org/pyfingerd.git/
