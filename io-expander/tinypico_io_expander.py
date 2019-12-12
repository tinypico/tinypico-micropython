# tinypico_io_expander

from machine import Pin, I2C
i2c = I2C(scl=Pin(22), sda=Pin(21))

# if there is no ads_address set or mcp_address set
print('Scanning for devices...')
found = i2c.scan()
for i in range(32,40):
    if i in found:
        print('Found MCP23017 at I2C address {} {}'.format(i, hex(i)))
        mcp_address = i
        break
for i in range(72,74):
    if i in found:
        print('Found ADS1015 at I2C address {} {}'.format(i, hex(i)))
        ads_address = i
        break
del found

# adc
import ads1015
ads = ads1015.ADS1015(i2c, ads_address, gain=1)

# mcp23017
import mcp23017
mcp = mcp23017.MCP23017(i2c, mcp_address)

# sd card
import uos as os
from machine import SDCard
sd = SDCard(slot=2)
sd_cd = Pin(33, Pin.IN)

# if sd card detect pin is LOW, a card is inserted
if sd_cd.value() == 0:
    try:
        print('Found SD card {}'.format(sd.info()))
        os.mount(sd, '/sd')
        print('Mounted SD card at /sd')
    except OSError:
        print('Failed to mount SD card')
else:
    print('SD card not inserted')

# deinit sd with
# os.umount('/sd')
# sd.deinit()
