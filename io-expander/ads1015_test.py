# Examples using the ADS1015 12-bit ADC

from tinypico_io_expander import *

# value = adc.read([rate, [channel1[, channel2]]])
ads.read(5,0)
ads.read(5,1)
ads.read(5,2)
ads.read(5,3)
ads.read(5,0,1)
ads.read(5,2,3)

ads.alert_start(rate=5, channel1=0, threshold_high=700, threshold_low=500, latched=True)
value = ads.alert_read()

from machine import Pin

p26 = Pin(26, Pin.IN, Pin.PULL_UP)

def _handler(p):
    print('ALERT')
    value = ads.alert_read()
    print(value)

p26.irq(trigger=Pin.IRQ_FALLING, handler=_handler)
p26.irq(None)
