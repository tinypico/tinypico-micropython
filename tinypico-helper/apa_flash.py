from machine import SoftSPI, Pin
import tinypico as TinyPICO
from micropython_dotstar import DotStar
import time, random

# Configure SPI for controlling the DotStar
# Internally we are using software SPI for this as the pins being used are not hardware SPI pins
spi = SoftSPI(sck=Pin( TinyPICO.DOTSTAR_CLK ), mosi=Pin( TinyPICO.DOTSTAR_DATA ), miso=Pin( TinyPICO.SPI_MISO) ) 
# Create a DotStar instance
dotstar = DotStar(spi, 1, brightness = 0.5 ) # Just one DotStar, half brightness
# Turn on the power to the DotStar
TinyPICO.set_dotstar_power( True )

# On and Off times in ms
wait_on = 500
wait_off = 500

# Flash the Dotstar a random colour every second
while True:
    # Pick a random colour from the colour wheel
    r,g,b = TinyPICO.dotstar_color_wheel( int(random.random() * 255) )
    # Display the colour for wait_on time then clear for wait_off time
    dotstar[0] = ( r, g, b, 1)
    time.sleep_ms(wait_on)
    dotstar[0] = ( 0, 0, 0, 1)
    time.sleep_ms(wait_off)
