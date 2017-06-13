# -*- coding: utf-8 -*-

"""Main module."""

import requests


class Relay(object):
    def __init__(self, url_base, relay_number):
        self.url_base = url_base
        self.relay_number = relay_number
        self.is_on = False

    def turn_on(self):
        requests.get('{}/{:02d}'.format(self.url_base, 2 * self.relay_number + 1))
        self.is_on = True

    def turn_off(self):
        requests.get('{}/{:02d}'.format(self.url_base, 2 * self.relay_number))
        self.is_on = False

    def toggle(self):
        return self.turn_off() if self.is_on else self.turn_on()


class WebRelay(object):
    def __init__(self, url_base, num_relays):
        if not (num_relays == 8 or num_relays == 16):
            raise ValueError('num_relays should be either 8 or 16')
        self.url_base = url_base
        self.relays = [Relay(url_base, x) for x in range(num_relays)]

    def toggle(self, relay_number):
        self.relays[relay_number].toggle()

    def turn_on(self, relay_number):
        self.relays[relay_number].turn_on()

    def turn_off(self, relay_number):
        self.relays[relay_number].turn_off()

    def all_on(self):
        requests.get('{}/45'.format(self.url_base))

    def all_off(self):
        requests.get('{}/44'.format(self.url_base))
    