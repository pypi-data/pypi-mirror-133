#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" Tests for the pyfingerd server. """

import socket

from pyfingerd.binds import FingerBindsDecoder, FingerTCPv4Bind
import pytest


class TestFingerDecoder:
    """ Test binds. """

    @pytest.fixture
    def decoder(self):
        return FingerBindsDecoder(proto='finger')

    def test_no_binds(self, decoder):
        assert decoder.decode('') == ()

    @pytest.mark.parametrize('raw,cls,params', (
        ('127.0.0.1:79', FingerTCPv4Bind, (
            socket.AF_INET,
            '127.0.0.1',
            79,
        )),
        ('127.0.2.3', FingerTCPv4Bind, (
            socket.AF_INET,
            '127.0.2.3',
            79,
        )),
    ))
    def test_binds(self, decoder, raw, cls, params):
        binds = decoder.decode(raw)
        assert len(binds) == 1

        bind = binds[0]
        assert isinstance(bind, cls)
        assert bind.runserver_params == params

# End of file.
