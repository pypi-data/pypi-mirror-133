#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2017-2022 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" Binds decoder for the finger server. """

import socket as _socket

from typing import Sequence as _Sequence

from .errors import InvalidBindError as _InvalidBindError

__all__ = [
    'FingerBind', 'FingerBindsDecoder',
    'FingerTCPv4Bind', 'FingerTCPv6Bind',
]


class FingerBind:
    """ Bind address for pyfingerd. """

    @property
    def runserver_params(self):
        """ Return the data as ``_runserver`` arguments. """

        raise NotImplementedError


class FingerTCPv4Bind(FingerBind):
    """ IPv4 TCP Address. """

    def __init__(self, address, port):
        try:
            self._addr = _socket.inet_pton(_socket.AF_INET, address)
        except Exception:
            self._addr = address

        self._port = port

    @property
    def runserver_params(self):
        """ Return the data as `_runserver` parameters. """

        return (
            _socket.AF_INET,
            _socket.inet_ntop(_socket.AF_INET, self._addr),
            self._port,
        )


class FingerTCPv6Bind(FingerBind):
    """ IPv6 TCP Address. """

    def __init__(self, address, port):
        try:
            self._addr = _socket.inet_pton(_socket.AF_INET6, address)
        except Exception:
            self._addr = address

        self._port = port

    @property
    def runserver_params(self):
        """ Return the data as `_runserver` parameters. """

        return (
            _socket.AF_INET6,
            _socket.inet_ntop(_socket.AF_INET6, self._addr),
            self._port,
        )


class FingerBindsDecoder:
    """ Binds decoder for pyfingerd. """

    def __init__(self, proto: str = 'finger'):
        proto = proto.casefold()
        if proto not in ('finger',):
            raise ValueError(f'unsupported protocol {proto!r}')

        self._proto = proto

    def decode(self, raw: str) -> _Sequence[FingerBind]:
        """ Get binds for the server, using a given string. """

        binds = set()

        for addr in map(lambda x: x.strip(), raw.split(',')):
            if not addr:
                continue

            # Try to find a scheme.

            scheme, *rest = addr.split(':/')
            if not rest:
                # No scheme found, let's just guess the scheme based on
                # the situation.

                raw = scheme
                scheme = {'finger': 'tcp'}[self._proto]
            else:
                # just don't add the ':' of ':/' again
                raw = '/' + ':/'.join(rest)

            if (
                (self._proto == 'finger' and scheme != 'tcp')
                or scheme not in ('tcp',)
            ):
                raise _InvalidBindError(
                    addr,
                    f'Unsupported scheme {scheme!r} for '
                    f'protocol {self._proto!r}',
                )

            # Decode the address data.

            if scheme == 'tcp':
                binds.update(self._decode_tcp_host(raw))

        return tuple(binds)

    def __repr__(self):
        return f'{self._class__.__name__}()'

    def _decode_tcp_host(self, x):
        """ Decode suitable hosts for a TCP bind. """

        addrs = ()
        addr = x

        # TODO: manage the '*' case.
        # TODO: decode hosts without the default host.

        # Get the host part first, we'll decode it later.

        if x[0] == '[':
            # The host part is an IPv6, look for the closing ']' and
            # decode it later.

            to = x.find(']')
            if to < 0:
                raise _InvalidBindError(
                    addr, "Expected closing ']'")

            host = x[1:to]
            x = x[to + 1:]

            is_ipv6 = True
        else:
            # The host part is either an IPv4 or a host name, look for
            # the ':' and decode it later.

            host, *x = x.split(':')
            x = ':' + ':'.join(x)

            is_ipv6 = False

        # Decode the port part.

        if x in ('', ':'):
            port = 79
        elif x[0] == ':':
            try:
                port = int(x[1:])
            except ValueError:
                try:
                    if x[1:] != '':
                        raise AssertionError('Expected a port number')
                    port = _socket.getservbyname(x[1:])
                except Exception:
                    raise _InvalidBindError(
                        addr,
                        'Expected a valid port number or name '
                        f'(got {x[1:]!r})',
                    ) from None
        else:
            raise _InvalidBindError(
                addr, 'Garbage found after the host',
            )

        # Decode the host part and get the addresses.

        addrs = ()
        if is_ipv6:
            # Decode the IPv6 address (validate it using `_socket.inet_pton`).

            ip6 = host
            _socket.inet_pton(_socket.AF_INET6, host)
            addrs += (FingerTCPv6Bind(ip6, port),)
        else:
            # Decode the host (try IPv4, otherwise, resolve domain).

            try:
                ip = host.split('.')
                if len(ip) < 2 or len(ip) > 4:
                    raise AssertionError('2 <= len(ip) <= 4')

                ip = list(map(int, ip))
                if not all(lambda x: 0 <= x < 256, ip):
                    raise AssertionError('non-8-bit component')

                if len(ip) == 2:
                    ip = [ip[0], 0, 0, ip[1]]
                elif len(ip) == 3:
                    ip = [ip[0], 0, ip[1], ip[2]]

                addrs += (FingerTCPv4Bind(ip, port),)
            except Exception:
                entries = _socket.getaddrinfo(
                    host, port,
                    proto=_socket.IPPROTO_TCP,
                    type=_socket.SOCK_STREAM)

                for ent in entries:
                    if (
                        ent[0] not in (_socket.AF_INET, _socket.AF_INET6)
                        or ent[1] not in (_socket.SOCK_STREAM,)
                    ):
                        continue

                    if ent[0] == _socket.AF_INET:
                        ip = ent[4][0]
                        _socket.inet_pton(_socket.AF_INET, ent[4][0])
                        addrs += (FingerTCPv4Bind(ip, port),)
                    else:
                        ip6 = ent[4][0]
                        _socket.inet_pton(_socket.AF_INET6, ent[4][0])
                        addrs += (FingerTCPv6Bind(ip6, port),)

        return addrs

# End of file.
