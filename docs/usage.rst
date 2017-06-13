=====
Usage
=====

To use EthernetRelay in a project::

    import sainsmart

    relay = sainsmart.EthernetRelay()

    # Access the state of the relays
    # relay.state() is a list of bools
    relay_state = relay.state()

    # Turn on the relay at index 0.
    relay.turn_on(0)

    # Turn off the relay at index 0.
    relay.turn_off(0)

    # Toggle the state of relay 0.
    relay.toggle(0)

    # Turn on all relays.
    relay.all_on()

    # Turn off all relays.
    relay.all_off()

The SainSmart Ethernet Relay defaults ip address: 192.168.1.4/30000.
This can be changed through their web interface.

To use EthernetRelay with a different IP address::

    import sainsmart

    relay = sainsmart.EthernetRelay('http://192.168.44.100/30000')

