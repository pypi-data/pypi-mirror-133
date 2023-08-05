#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" Tests for the pyfingerd server. """

import socket

from datetime import timedelta
from time import sleep

from pyfingerd.core import *  # NOQA
from pyfingerd.fiction import *  # NOQA

import pytest


class TestFingerConnection:
    """ Test basic finger connections. """

    @pytest.fixture(autouse=True)
    def fingerserver(self):
        """ Start a finger server.

            A fixture starting a finger server on ``localhost:3099``
            and stopping it after the test.
        """

        scenario = FingerScenario()
        scenario.ending_type = 'freeze'
        scenario.duration = timedelta(seconds=5)
        scenario.add(
            FingerUserCreationAction(
                login='john',
                name='John Doe',
                home='/home/john',
                shell='/bin/bash',  # NOQA
                office='84.6',
            ),
            timedelta(seconds=-5))
        scenario.add(
            FingerUserLoginAction(
                login='john',
                line='tty1',
            ),
            timedelta(seconds=0))
        scenario.add(
            FingerUserLogoutAction(
                login='john',
            ),
            timedelta(seconds=1))

        class TestFormatter(FingerFormatter):
            """ Test formatter, uncomplicated to test. """

            def _format_users(self, users):
                result = f'{len(users)}\n'
                for user in users:
                    result += (
                        f'{user.login}|{user.name}|{user.home}|'
                        f'{user.shell}|{user.office or ""}|'
                        f'{len(user.sessions)}\n'
                    )
                    for session in user.sessions:
                        result += (
                            f'{session.line or ""}|{session.host or ""}\n'
                        )

                return result

            def format_query_error(self, hostname, raw_query):
                return f'{hostname}\n{raw_query}\nerror\n'

            def format_short(self, hostname, raw_query, users):
                return (
                    f'{hostname}\n{raw_query}\nshort\n'
                    + self._format_users(users)
                )

            def format_long(self, hostname, raw_query, users):
                return (
                    f'{hostname}\n{raw_query}\nlong\n'
                    + self._format_users(users)
                )

        server = FingerServer(
            'localhost:3099',
            hostname='example.org',
            interface=FingerScenarioInterface(scenario),
            formatter=TestFormatter(),
        )
        server.start()

        sleep(.1)
        yield

        server.stop()

    def _send_command(self, command):
        conn = socket.create_connection(('localhost', 3099), 1)
        conn.send(command.encode('ascii') + b'\r\n')

        result = tuple(
            conn.recv(1024).decode('ascii')
            .rstrip('\r\n').split('\r\n')
        )

        assert result[:2] == (
            'EXAMPLE.ORG',
            command,
        )
        return result[2:]

    # ---
    # Tests.
    # ---

    def test_no_user_list(self):
        """ Test if an unknown user returns an empty result. """

        assert self._send_command('user') == ('long', '0')

    def test_existing_user_list(self):
        """ Test the user list before and after the cron is executed. """

        assert self._send_command('') == (
            'short', '1',
            'john|John Doe|/home/john|/bin/bash|84.6|1',
            'tty1|',
        )

        sleep(2)

        assert self._send_command('') == ('short', '0')

# End of file.
