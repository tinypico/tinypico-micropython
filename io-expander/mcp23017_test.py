# Examples using the MCP23017 16-bit I/O Expander

from tinypico_io_expander import *

# -----------
# Simple IO

# set pin 0 as input with pull-up
mcp.pin(0, mode=1, pullup=1)
print(mcp.pin(0))

# set pin 1 as output low
mcp.pin(1, mode=0, value=0)

# set pin 2 as output high
mcp.pin(2, mode=0, value=1)

# -----------
# Push button receive LED

# Connect a momentary push button between Pin 0 and GND
# Connect a LED anode (long leg) to Pin 1, cathode (short leg) through a 180ohm resistor to GND
# When the LED on Pin 1 goes HIGH it will source current and illuminate the LED

# When the button is pushed, Pin 0 will go LOW, triggering an interrupt
# On interrupt, read the value of Pin 0 and set Pin 1 HIGH or LOW
# The polarity of the input pin is inverted so that it can be passed directly to the output pin

# set button pin 0 as input with pull-up
mcp.pin(0, mode=1, pullup=1, interrupt_enable=1, polarity=1)

# set LED pin 1 as output low, LED off
mcp.pin(1, mode=0, value=0)

# connect IntA to Pin4
p4 = Pin(4, Pin.IN)

def _handler(p):
    # if pin 7 caused the INT
    if mcp.porta.interrupt_flag & 1:
        # get the value of the GPIO at the time of interrupt
        val = mcp.porta.interrupt_captured & 1
        # if button pressed, val will be 1
        mcp.pin(0, value=val)

# fire interrupt when button is pushed
p4.irq(trigger=Pin.IRQ_FALLING, handler=_handler)

# turn off interrupt handler
p4.irq(None)
