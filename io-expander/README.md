# TinyPICO IO Expander Shield

MicroPython library for the [TinyPICO IO Expander Shield](https://www.tinypico.com/add-ons).

The shield combines several components:

* MCP23017 - 16-port I/O expander, I2C interface
* ADS1015 - Analog to Digital converter (ADC), I2C interface
* SD Card - MicroSD, SDIO interface
* TXB0104 - 4-bit bidirectional voltage level translator for 5V logic


## Example usage

```python
from tinypico_io_expander import *
```


# ADS1015 ADC

Connects using I2C interface:

* SDA GPIO21
* SCL GPIO22

Address selection via pads on bottom.
Pulled down by default. Bridge to connect ADDR pin to 3V3.

There are two other I2C addresses the ADS1015 supports, by connecting ADDR to SCL or SDA, but this board does not support these configurations.

ADDR  | Address
----- | --------------------------------
GND   | 0b1001000 - 0x48 - 72  (default)
3V3   | 0b1001001 - 0x49 - 73

ALERT pin has an onboard pull up resistor.

Features:

* Resolution: 12 bits
* Max sample rate: 3300 sps
* Inputs: 2 differential or 4 single ended
* Programmable gain amplifier: Yes
* Comparator: Yes

```python
ads.read(5,0)  # read channel 0 (A1)
ads.read(5,1)  # read channel 1 (A2)
ads.read(5,2)  # read channel 2 (A3)
ads.read(5,3)  # read channel 3 (A4)

ads.read(5,0,1)  # read difference between channels 0 and 1 (A1, A2)
ads.read(5,2,3)  # read difference between channels 2 and 3 (A3, A4)
```


# MCP23017 16 port IO expander

Connects using I2C interface:

* SDA GPIO21
* SCL GPIO22

Address selection via pads on bottom.
Each are pulled down by default. Bridge to pull up to 3V3.

A0  | A1  | A2  | Address
--- | --- |---- | -------------------------------
LO  | LO  | LO  | 0100 0000 - 0x20 - 32 (default)
HI  | LO  | LO  | 0100 0001 - 0x21 - 33
LO  | HI  | LO  | 0100 0010 - 0x22 - 34
HI  | HI  | LO  | 0100 0011 - 0x23 - 35
LO  | LO  | HI  | 0100 0100 - 0x24 - 36
HI  | LO  | HI  | 0100 0101 - 0x25 - 37
LO  | HI  | HI  | 0100 0110 - 0x26 - 38
HI  | HI  | HI  | 0100 0111 - 0x27 - 39

```python
# set pin 0 as input with pull-up
mcp.pin(0, mode=1, pullup=1)
print(mcp.pin(0))

# set pin 1 as output low
mcp.pin(1, mode=0, value=0)

# set pin 2 as output high
mcp.pin(2, mode=0, value=1)
```


# SD Card

Connects using SPI interface:

* MOSI GPIO23 (hw pull down)
* MISO GPIO19
* SCK  GPIO18
* CS   GPIO5 (hw pull up)
* CD   GPIO33

You can detect if a card is inserted by reading CD (card detect) GPIO33.

```python
import machine
import uos

# initialise sd card
sd = machine.SDCard(slot=2)

# get card size
sd.info()

# mount
uos.mount(sd, '/sd')

# list files in directory
uos.listdir('/sd')

# write file
f = open('/sd/test.py', 'w')
f.write('print(\'hello\')\n')
f.close()

# read file
f = open('/sd/test.py', 'r')
print(f.read())
f.close()

# append to file
f = open('/sd/test.py', 'a')
f.write('print(\'hello again\')\n')
f.close()

# remove file
uos.remove('/sd/test.py')

# unmount
uos.umount('/sd')

# deinitialise sd card
sd.deinit()
```

# TXB0104 5V IO

TXB0104 4-bit bidirectional voltage level translator.

There are 3 pins which stepped up from 3.3V to 5V.

* GPIO14
* GPIO15
* GPIO27

If the board is powered by USB (5V), the OE (output enable) pin of the TXB0104 is pulled up and 5V output is enabled.

```python
from machine import Pin
p27 = Pin(27, Pin.OUT, value=0)

p27 = Pin(27, Pin.IN, Pin.PULL_UP)
print(p27())
```


# Unused pins

The following pins are not used by the IO Expander Shield and are free to use:

* GPIO25
* GPIO26
* GPIO4
* GPIO32
