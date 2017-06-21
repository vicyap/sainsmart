# -*- coding: utf-8 -*-

"""Devices Module."""

import re
import requests

from typing import List  # noqa: F401


class EthernetRelay(object):
    """SainSmart Ethernet Relay.

    <https://www.sainsmart.com/sainsmart-ethernet-control-module-lan-wan-web-server-control-with-rj45-port.html>
    """

    def __init__(self, url_base='http://192.168.1.4/30000'):
        # type: (str) -> None
        """Initalize the class.

        Kwargs:
            url_base (str): The base url of the ethernet relay.

        Attributes:
            url_base (str): The base url of the ethernet relay.
            relays (:obj:`list` of :obj:`bool`): A list of the on/off state of each relay.
        """
        self.url_base = url_base
        self._relays = self.state()

    def check_index(self, relay_index):
        # type: (int) -> None
        """Check that relay_index is valid.

        This method raises an IndexError if `relay_index` is negative or if
        `relay_index` is greater than or equal to the number of relay.

        Args:
            relay_index (int): the relay index.

        Raises:
            IndexError: If `relay_index` is negative or greater than the
                number of relays.
        """
        if relay_index < 0:
            raise IndexError('relay_index={} cannot be negative'.format(relay_index))
        elif relay_index >= len(self._relays):
            raise IndexError('relay_index={} cannot be greater than {}'.format(
                relay_index, len(self._relays)))

    def state(self):
        # type: () -> List[bool]
        """Get the state of the relays.

        Raises:
            RuntimeError: If there was a problem with requesting the url or
                parsing the response.
        """
        r = requests.get('{}/99'.format(self.url_base))
        if r.status_code == 200:
            content = r.content.decode('ascii')
            re.sub('192.168\.\d+\.\d+', '', content)
            regex = re.compile(
                r'''
                <a.*>
                (?P<state_bits>[01]+)
                .*</a>
                ''',
                re.VERBOSE)
            match = regex.search(content)
            if match:
                state_bits_str = match.groupdict()['state_bits']
                return [s == '1' for s in state_bits_str]
            else:
                raise RuntimeError("Could not parse the response from the ethernet relay.")
        else:
            raise RuntimeError('The ethernet relay did not respond with status code 200.')

    def verify(self):
        # type: () -> None
        """Verify the state of the relays matches this class instance's state.

        Raises:
            RuntimeError: :func:`EthernetRelay.state()`
            ValueError: If this class instance's state does not match the state
                of the relays.
        """
        state = self.state()
        index = 0
        for i, j in zip(self._relays, state):
            if i != j:
                raise ValueError('Relay at index={} did not match state={}'.format(index, j))
            index += 1

    def toggle(self, relay_index):
        # type: (int) -> None
        """Toggle the state of a relay.

        Args:
            relay_index (int): the relay index to toggle.

        Raises:
            IndexError: :func:`EthernetRelay.check_index`
        """
        self.check_index(relay_index)
        if self._relays[relay_index]:
            self.turn_off(relay_index)
        else:
            self.turn_on(relay_index)

    def turn_on(self, relay_index):
        # type: (int) -> None
        """Turn a relay on.

        Args:
            relay_index (int): the relay index to turn on.

        Raises:
            IndexError: :func:`EthernetRelay.check_index`
        """
        self.check_index(relay_index)
        requests.get('{}/{:02d}'.format(self.url_base, 2 * relay_index + 1))
        self._relays[relay_index] = True
        self.verify()

    def turn_off(self, relay_index):
        # type: (int) -> None
        """Turn a relay off.

        Args:
            relay_index (int): the relay index to turn off.

        Raises:
            IndexError: :func:`EthernetRelay.check_index`
        """
        self.check_index(relay_index)
        requests.get('{}/{:02d}'.format(self.url_base, 2 * relay_index))
        self._relays[relay_index] = False
        self.verify()

    def all_on(self):
        # type: () -> None
        """Turn all relays on."""
        requests.get('{}/45'.format(self.url_base))
        self._relays = [True for r in self._relays]
        self.verify()

    def all_off(self):
        # type: () -> None
        """Turn all relays off."""
        requests.get('{}/44'.format(self.url_base))
        self._relays = [False for r in self._relays]
        self.verify()
