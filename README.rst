=========
sainsmart
=========


.. image:: https://img.shields.io/pypi/v/sainsmart.svg
        :target: https://pypi.python.org/pypi/sainsmart

.. image:: https://img.shields.io/travis/vicyap/sainsmart.svg
        :target: https://travis-ci.org/vicyap/sainsmart

.. image:: https://readthedocs.org/projects/sainsmart/badge/?version=latest
        :target: https://sainsmart.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/vicyap/sainsmart/shield.svg
     :target: https://pyup.io/repos/github/vicyap/sainsmart/
     :alt: Updates


sainsmart contains code for working with sainsmart products.

Usage
-----
To use EthernetRelay in a project::

    import sainsmart

    relay = sainsmart.EthernetRelay()

    # Access the state of the relays
    # relay.relays is a list of bools
    relay_states = relay.relays

    # Turn on the relay at index 0.
    relay.turn_on(0)
    assert relay.relays[0]

    # Turn off the relay at index 0.
    relay.turn_off(0)
    assert relay.relays[0] == False

    # Toggle the state of relay 0.
    relay.toggle(0)
    assert relay.relays[0]
    relay.toggle(0)
    assert relay.relays[0] == False

    # Turn on all relays.
    relay.all_on()
    assert all(relay.relays)

    # Turn off all relays.
    relay.all_off()

To use EthernetRelay with a different IP address::

    import sainsmart

    relay = sainsmart.EthernetRelay('http://192.168.44.100/30000')


* Free software: MIT license
* Documentation: https://sainsmart.readthedocs.io.


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

