Fictional interfaces API
========================

.. py:module:: pyfingerd.fiction

For more information about this section, consult :ref:`fictional-interfaces`.

Fictional representations
-------------------------

These classes are compatible with the ones from the core for use by the
server, but implements existing and/or new properties more suited for fiction.

.. autoclass:: FictionalFingerUser
	:members: login, name, shell, home, office, plan

.. autoclass:: FictionalFingerSession
	:members: name, start, idle, idle_since, active_since, line, host

.. _actions-api:

Fictional action representations
--------------------------------

.. autoclass:: FingerAction

.. autoclass:: FingerUserCreationAction
	:members: login, name, shell, home, office, plan

.. autoclass:: FingerUserEditionAction
	:members: login, name, shell, home, office, plan

.. autoclass:: FingerUserDeletionAction
	:members: login

.. autoclass:: FingerUserLoginAction
	:members: login, session_name, line, host

.. autoclass:: FingerUserSessionChangeAction
	:members: login, session_name, idle

.. autoclass:: FingerUserLogoutAction
	:members: login, session_name

Playing fictions
----------------

.. autoclass:: FingerFictionInterface
	:members: reset, apply

Playing scenarios
-----------------

.. autoclass:: FingerScenario
	:members: verify, load, get, add, ending_type, duration, EndingType

.. autoclass:: FingerScenarioInterface

