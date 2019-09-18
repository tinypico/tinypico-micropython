# TinyPICO Play Shield MicroPython Starting Template
# 2019 Seon Rozenblum
#
# Project home:
#   https://github.com/TinyPICO
#
# 2019-July-20 - v1.0 - Initial Release

"""
`tinypico play` - MicroPython TinyPICO Play Shield Template
===========================================================

* Author(s): Seon Rozenblum
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/TinyPICO/tinypico-micropython"

# Import required libraries
import tinypico as TinyPICO
from micropython import const
from machine import I2C, Pin

# Hardware Pin Assignments

# Buttons
BUT_1 = Pin( 26, Pin.IN )
BUT_2 = Pin( 27, Pin.IN )
BUT_3 = Pin( 15, Pin.IN )
BUT_4 = Pin( 14, Pin.IN )

# Light  Sensor
LIGHT_SENS = Pin( 32, Pin.IN )

# Speaker
SPEAKER = Pin( 25, Pin.OUT )

# Blue LED
LED = Pin( 4, Pin.OUT )

# Setup

# Turn off the power to the DotStar
TinyPICO.set_dotstar_power( False )

# Configure I2C for controlling anything on the I2C bus
# Software I2C only for this example but the next version of MicroPython for the ESP32 supports hardware I2C too
i2c = I2C(scl=Pin(22), sda=Pin(21))

# Example initialisers for the  OLED and IMU

# Initialise the LIS3HD 3-Axis IC
# imu = lis3dh.LIS3DH_I2C(i2c)

# Initialise the OLED screen
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)
