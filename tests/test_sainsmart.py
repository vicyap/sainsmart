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
    def __init__(self, num_relays, init_state=None):
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
    status_code = 200
    match = re.match(r'http://192\.168\.1\.4/30000/(?P<num>\d*)', request.url)
    num = int(match.groupdict()['num'])
    content = None
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
    return {'status_code': status_code,
            'content': content}


class TestSainsmart(unittest.TestCase):
    """Tests for `sainsmart` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        global _MOCK
        assert _MOCK is None
        _MOCK = EthernetRelayMock(16)

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
            self.assertTrue(all(relay.relays))

    def test_002(self):
        """Test all off."""
        with httmock.HTTMock(mock_relay):
            relay = sainsmart.EthernetRelay()
            relay.all_on()
            relay.all_off()
            self.assertFalse(any(relay.relays))

    def test_003(self):
        """Test turn on and turn off."""
        with httmock.HTTMock(mock_relay):
            relay = sainsmart.EthernetRelay()
            for i in range(len(relay.relays)):
                relay.turn_on(i)
            self.assertTrue(all(relay.relays))
            for i in range(len(relay.relays)):
                relay.turn_off(i)
            self.assertFalse(any(relay.relays))

    def test_004(self):
        """Test toggle."""
        with httmock.HTTMock(mock_relay):
            relay = sainsmart.EthernetRelay()
            for i in range(len(relay.relays)):
                relay.toggle(i)
            self.assertTrue(all(relay.relays))
            for i in range(len(relay.relays)):
                relay.toggle(i)
            self.assertFalse(any(relay.relays))

    def test_005(self):
        """Non-zero init."""
        global _MOCK
        _MOCK = EthernetRelayMock(16, '1010101010101010')
        with httmock.HTTMock(mock_relay):
            relay = sainsmart.EthernetRelay()
            self.assertEquals(sum(relay.relays), 8)
