=====
Usage
=====

To use sainsmart in a project::

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
    assert not any(relay.relays)

To use EthernetRelay with a different IP address::

    import sainsmart

    relay = sainsmart.EthernetRelay('http://192.168.44.100/30000')

