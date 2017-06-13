#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sainsmart` package."""


import unittest
import httmock
import re

from sainsmart import sainsmart


_MOCK = None
_99 = ' <small><a href="http://192.168.1.4/30000"></a></small><a href="http://192.168.1.4/30000/{}">{}</a><p>'


class EthernetRelayMock(object):
    def __init__(self, num_relays=16, init_state=None):
        self.relays = [False] * num_relays
        if init_state:
            assert len(init_state) == num_relays
            self.relays = [s == '1' for s in init_state]

    def get_state_str(self):
        state = ''
        for r in self.relays:
            if r:
                state += '1'
            else:
                state += '0'
        return state

    def toggle(self, relay_index):
        self.relays[relay_index] = not self.relays[relay_index]

    def turn_on(self, relay_index):
        self.relays[relay_index] = True

    def turn_off(self, relay_index):
        self.relays[relay_index] = False

    def all_on(self):
        self.relays = [True] * len(self.relays)

    def all_off(self):
        self.relays = [False] * len(self.relays)


@httmock.all_requests
def mock_relay(url, request):
    """Mocks requests.

    if port is 30000, act normal.

    if port is 20000, return status_code=200 but bad content

    if port is 40000, return status_code=404
    """
    status_code = 200
    content = None
    match = re.match(r'http://192\.168\.1\.4/(?P<port>\d+)/(?P<num>\d*)', request.url)
    port = int(match.groupdict()['port'])
    num = int(match.groupdict()['num'])
    if port == 30000:
        if num == 99:
            content = _99.format(_MOCK.get_state_str(), _MOCK.get_state_str()).encode('ascii')
        elif num == 44:
            _MOCK.all_off()
        elif num == 45:
            _MOCK.all_on()
        elif num < 40:
            if num % 2 == 1:
                _MOCK.turn_on(int(num / 2))
            else:
                _MOCK.turn_off(int(num / 2))
    elif port == 40000:
        status_code = 404
    elif port == 20000:
        content = 'garbage'.encode('ascii')
    return {'status_code': status_code,
            'content': content}


class TestSainsmart(unittest.TestCase):
    """Tests for `sainsmart` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        global _MOCK
        assert _MOCK is None
        _MOCK = EthernetRelayMock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        global _MOCK
        _MOCK = None

    def test_000(self):
        """Test init."""
        with httmock.HTTMock(mock_relay):
            sainsmart.EthernetRelay()

    def test_001(self):
        """Test all on."""
        with httmock.HTTMock(mock_relay):
            relay = sainsmart.EthernetRelay()
            relay.all_off()
            relay.all_on()
            self.assertTrue(all(relay.state()))

    def test_002(self):
        """Test all off."""
        with httmock.HTTMock(mock_relay):
            relay = sainsmart.EthernetRelay()
            relay.all_on()
            relay.all_off()
            self.assertFalse(any(relay.state()))

    def test_003(self):
        """Test turn on and turn off."""
        with httmock.HTTMock(mock_relay):
            relay = sainsmart.EthernetRelay()
            for i in range(len(relay.state())):
                relay.turn_on(i)
            self.assertTrue(all(relay.state()))
            for i in range(len(relay.state())):
                relay.turn_off(i)
            self.assertFalse(any(relay.state()))

    def test_004(self):
        """Test toggle."""
        with httmock.HTTMock(mock_relay):
            relay = sainsmart.EthernetRelay()
            for i in range(len(relay.state())):
                relay.toggle(i)
            self.assertTrue(all(relay.state()))
            for i in range(len(relay.state())):
                relay.toggle(i)
            self.assertFalse(any(relay.state()))

    def test_005(self):
        """Non-zero init."""
        global _MOCK
        _MOCK = EthernetRelayMock(num_relays=16, init_state='1010101010101010')
        with httmock.HTTMock(mock_relay):
            relay = sainsmart.EthernetRelay()
            self.assertEqual(sum(relay.state()), 8)

    def test_006(self):
        """Test verify."""
        with httmock.HTTMock(mock_relay):
            relay = sainsmart.EthernetRelay()
            relay._relays[0] = True  # this should be disallowed anyways
            with self.assertRaises(ValueError):
                relay.verify()

    def test_007(self):
        """Test check_index."""
        with httmock.HTTMock(mock_relay):
            relay = sainsmart.EthernetRelay()
            with self.assertRaises(IndexError):
                relay.check_index(-1)
            with self.assertRaises(IndexError):
                relay.check_index(16)

    def test_008(self):
        """Test bad status code."""
        with httmock.HTTMock(mock_relay):
            with self.assertRaises(RuntimeError):
                sainsmart.EthernetRelay(url_base='http://192.168.1.4/40000')

    def test_009(self):
        """Test unable to parse content."""
        with httmock.HTTMock(mock_relay):
            with self.assertRaises(RuntimeError):
                sainsmart.EthernetRelay(url_base='http://192.168.1.4/20000')
