.. _scenarios:

Scenarios and actions
=====================

A scenario defines how a scene evolves through time; see
:ref:`fictional-interfaces` for more information about scenes.
In order to achieve this goal, it is composed of three elements:

* An ending time, which defines at which time the scenario ends.
* An ending type, which defines how the scene should behave once the
  scenario ends.
* A set of actions, each accompagnied with a time relative to the start
  of the play.

In the scope of this project, such a scenario is represented using
the :py:class:`pyfingerd.fiction.FingerScenario` class. This class can load
its data using two methods: programatically, or using a scenario file.

Note that this section doesn't cover how to write scenarios, only a definition
of scenarios; see :ref:`writing-scenarios` for this use.

Loading a scenario programatically
----------------------------------

For defining a scenario using code, you are to use the
:py:meth:`pyfingerd.fiction.FingerScenario.add` method with actions
as defined in :ref:`actions-api`, and define both the
:py:meth:`pyfingerd.fiction.FingerScenario.ending_type` and
:py:meth:`pyfingerd.fiction.FingerScenario.duration` properties.

For example:

.. code-block:: python

    from datetime import timedelta
    from pyfingerd.fiction import *

    scenario = FingerScenario()
    scenario.ending_type = FingerScenario.EndingType.FREEZE
    scenario.duration = 60

    scenario.add(
        FingerUserCreationAction(
            login="root",
            home="/home/root",
        ),
        '-1m',
    )

    scenario.add(
        FingerUserLoginAction(
            login="root",
        ),
        timedelta(seconds=5),
    )

.. _scenario-files:

Scenario files
--------------

Scenarios can also be defined as TOML files, loaded using the
:py:meth:`pyfingerd.fiction.FingerScenario.load` static method which
produce :py:class:`pyfingerd.fiction.FingerScenario` instances.

These files describe actions as point in times where something happen.
Every action has a time offset, using a TOML array section (``[[something]]``),
and properties describing what's happening. Endings are represented as
specific actions.

Time offsets are represented the following way:

::

	-?(<weeks>w)?(<days>[jd])?(<hours>h)?(<minutes>m)?(<seconds>s)?

Where negative times, starting with a dash (``-``), are the initial situation,
what is supposed to have happened before the beginning.

For example, ``-1w5d2h`` means “1 week, 5 days and 2 hours before the
origin” and ``2j`` means “2 days after the origin”. So if we want to make
an action that takes place 5 seconds after the origin, the first line of the
action will be the following one:

::

	[[5s]]

All actions have a type represented by the ``type`` property, and other
properties depending on the type. The actions are described in the
subsections below.

Flow-related actions
~~~~~~~~~~~~~~~~~~~~

The following are related to the action flow:

``interrupt`` or ``freeze``
	The server freezes on the latest situation.

``stop``
	The server stops on the event.

``repeat``
	The server repeats everything starting from the beginning.

All the actions after the time of any of these will be ignored.

User-related actions
~~~~~~~~~~~~~~~~~~~~

User-related actions' types can be of the following:

``create``
	A user has been created.

``update``
	A user has been updated.

``delete``
	A user has been deleted.

As all of these actions are about users, they all take an additional
``login`` argument which is the affected user's name, e.g. ``rinehart``.

The ``create`` and ``update`` event takes some more arguments:

``name``
	The user full name, e.g. “Mark J. Rinehart”.

``shell``
	The selected login shell.

``home``
	The home directory.

``office``
	The user's office name, e.g. “B121 on second floor”.

``plan``
	The plan path.

For an ``update`` action, setting properties to ``false`` will erase their
previous value without setting a new one.

Session-related actions
~~~~~~~~~~~~~~~~~~~~~~~

Session-related actions' types can be of the following:

``login``
	A user has logged in and is active.

``logout``
	A user has logged out.

``idle``
	A user is now idle (not typing on the keyboard anymore).

``active``
	A user is now active (typing every now and then).

These actions take an additional argument ``login`` which is the user to
which the session belongs, and an optional other ``session`` argument to
identify the session for which the event is in the case of multiple sessions
for the user.

The ``login`` operation takes the information about the originating shell:

``line``
	The physical line on which the user is connected.

``host``
	The remote host from which the physical line is opened, if any.
