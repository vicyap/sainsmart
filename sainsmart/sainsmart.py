# -*- coding: utf-8 -*-

"""SainSmart Module."""

import re
import requests

from typing import List


class EthernetRelay(object):
    """SainSmart Ethernet Relay.

    <https://www.sainsmart.com/sainsmart-ethernet-control-module-lan-wan-web-server-control-with-rj45-port.html>
    """

    def __init__(self, url_base: str ='http://192.168.1.4/30000') -> None:
        """Initalize the class.

        Kwargs:
            url_base (str): The base url of the ethernet relay.

        Attributes:
            url_base (str): The base url of the ethernet relay.
            relays (:obj:`list` of :obj:`bool`): A list of the on/off state of each relay.
        """
        self.url_base = url_base
        self.relays = self.get_state()

    def _check_index(self, relay_index: int) -> None:
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
        elif relay_index >= len(self.relays):
            raise IndexError('relay_index={} cannot be greater than {}'.format(
                relay_index, len(self.relays)))

    def get_state(self) -> List[bool]:
        """Get the state of the relays.

        Raises:
            RuntimeError: If there was a problem with requesting the url or
                parsing the response.
        """
        r = requests.get('{}/99'.format(self.url_base))
        if r.status_code == 200:
            match = re.search(r'<a.*>(?P<state_bits>[01]+)</a>', r.content.decode('ascii'))
            if match:
                state_bits_str = match.groupdict()['state_bits']
                return [s == '1' for s in state_bits_str]
            else:
                raise RuntimeError("Could not parse the response from the ethernet relay.")
        else:
            raise RuntimeError('The ethernet relay did not respond with status code 200.')

    def verify_state(self) -> None:
        """Verify the state of the relays matches this class instance's state.

        Raises:
            ValueError: If this class instance's state does not match the state
                of the relays.
        """
        state = self.get_state()
        index = 0
        for i, j in zip(self.relays, state):
            if i != j:
                raise ValueError('Relay at index={} did not match state={}'.format(index, j))
            index += 1

    def toggle(self, relay_index: int) -> None:
        """Toggle the state of a relay.

        Args:
            relay_index (int): the relay index to toggle.
        """
        self._check_index(relay_index)
        if self.relays[relay_index]:
            self.turn_off(relay_index)
        else:
            self.turn_on(relay_index)

    def turn_on(self, relay_index: int) -> None:
        """Turn a relay on.

        Args:
            relay_index (int): the relay index to turn on.
        """
        self._check_index(relay_index)
        requests.get('{}/{:02d}'.format(self.url_base, 2 * relay_index + 1))
        self.relays[relay_index] = True
        self.verify_state()

    def turn_off(self, relay_index: int) -> None:
        """Turn a relay off.

        Args:
            relay_index (int): the relay index to turn off.
        """
        self._check_index(relay_index)
        requests.get('{}/{:02d}'.format(self.url_base, 2 * relay_index))
        self.relays[relay_index] = False
        self.verify_state()

    def all_on(self) -> None:
        """Turn all relays on."""
        requests.get('{}/45'.format(self.url_base))
        self.relays = [True for r in self.relays]
        self.verify_state()

    def all_off(self) -> None:
        """Turn all relays off."""
        requests.get('{}/44'.format(self.url_base))
        self.relays = [False for r in self.relays]
        self.verify_state()
