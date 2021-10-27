# TinyPICO Audio Shield DAC Example
# https://www.tinypico.com/add-ons

# Amplifier power can be toggled with with:
# TinyPICO = IO4
# TinyS2 = IO4

# Gain trim pot:
# clockwise = louder
# anti-clockwise = quieter

from machine import Pin, DAC

amp = Pin(4, Pin.OUT, value=0)  # amp off (no sound)
amp.value(1)  # amp on (lots of sound)

dac = DAC(Pin(25))


# ----------------------
# example 1: simple buzz

# play a simple buzzing sound for a few seconds
for _ in range(100):
    for i in range(255):
        dac.write(i)
        dac.write(255-i)


# --------------------
# example 2: sine wave

import math

# create a buffer
buf = bytearray(100)

# fill it with a sine wave
for i in range(len(buf)):
    buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / len(buf)))

# play the sine wave for a few seconds
for _ in range(500):
    for i in range(len(buf)):
        dac.write(buf[i])
