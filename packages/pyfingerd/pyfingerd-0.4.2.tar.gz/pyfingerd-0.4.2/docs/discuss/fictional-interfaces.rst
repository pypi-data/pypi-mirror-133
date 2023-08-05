.. _fictional-interfaces:

Fictional interfaces
====================

One of the goals of pyfingerd was to be able to play a fiction and present
scripted fake data.

Imagine a scene in a theater. On this scene, you can distinctly see actions
happening, making the scene go from one state to the other. Fictional
interfaces in pyfingerd function the same way.

The interface managing the scene is the
:py:class:`pyfingerd.fiction.FingerFictionInterface`.
It starts with an empty scene, i.e. no users and no sessions.
From there, two things can happen:

* One or more actions can be applied to the scene to make it evolve,
  using :py:meth:`pyfingerd.fiction.FingerFictionInterface.apply`.
* The scene can be reset to the initial state (no users, no sessions);
  for example, this can happen when a scene repeats itself or starts
  a completely different story. This is accomplished by using
  :py:meth:`pyfingerd.fiction.FingerFictionInterface.reset`.

This base class doesn't do anything by itself, it is a canvas which
other classes can subclass to manage the scene by calling these two
methods.

Note that any class subclassing the fiction interface can also make the
server shut down by simply exiting using ``exit(0)``.
For example, a story could include the server itself, with a technician
making the server crash at some point.

.. _scenario-interface:

Scenario interface
------------------

One of the applications of the fiction interface is the scenario interface.
The idea is to make use of a scenario, i.e. a set of actions accompanied by
the ending type and time.

This application is implemented using the
:py:class:`pyfingerd.fiction.FingerScenarioInterface` class.
This function has a function that gets executed every second that
updates the scene according to the scenario.

See :ref:`scenarios` for more information.

Live interface
--------------

Another potential application of the fiction interface would be to read
the actions from a live source, e.g. by having an intermediate server
listening on localhost for scripts to push actions through HTTP POSt
requests and making them available for the finger server to pull.

Note that this usage is not yet implemented.
