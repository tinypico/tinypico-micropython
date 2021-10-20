# TinyPICO Audio Shield DAC Example
# https://www.tinypico.com/add-ons

# Amplifier power can be toggled with with:
# TinyPICO = IO4
# TinyS2 = IO4

# Gain trim pot:
# clockwise = louder
# anti-clockwise = quieter

# machine.PWM docs:
# https://docs.micropython.org/en/latest/esp32/quickref.html#pwm-pulse-width-modulation

from machine import Pin, PWM
import time

amp = Pin(4, Pin.OUT, value=0)  # amp off (no sound)
amp.value(1)  # amp on (lots of sound)

buzzer = PWM(Pin(25), freq=550, duty=0)


# ---------------------------
# example 1: oscillating buzz

def example1(duty1, duty2, pause=50):
    try:
        amp.value(1)
        while True:
            buzzer.duty(duty1)
            time.sleep_ms(pause)
            buzzer.duty(duty2)
            time.sleep_ms(pause)
        amp.value(0)
    except KeyboardInterrupt:
        buzzer.duty(0)
        amp.value(0)

example1(30,100)
# ctrl+c to stop


# -------------------------
# example 2: a dripping tap

buzzer.freq(2) # two droplets per second
buzzer.duty(30)

buzzer.freq(4) # four droplets per second

buzzer.duty(0) # someone turned off the tap
