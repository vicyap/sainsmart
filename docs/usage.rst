=====
Usage
=====
To use EthernetRelay in a project::

    from sainsmart import devices

    relay = devices.EthernetRelay()

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

    from sainsmart import devices

    relay = devices.EthernetRelay('http://192.168.44.100/30000')


Example
-------
Here is an example with a real device::

   >>> from sainsmart import devices
   >>> relay = devices.EthernetRelay()
   >>> relay.state()
   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
   >>> relay.turn_on(0)
   >>> relay.state()
   [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
   >>> relay.toggle(0)
   >>> relay.state()
   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
   >>> relay.all_on()
   >>> relay.state()
   [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
   >>> relay.turn_off(0)
   >>> relay.state()
   [False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
   >>> relay.all_off()
   >>> relay.state()
   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False] 

