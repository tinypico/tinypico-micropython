TinyPICO MicroPython Helper
===========================

This library adds some helper functions and useful pin assignments to make coding with TinyPICO & MicroPython easier

TinyPICO Hardware Pin Assignments
---------------
.. code-block:: python

    # Battery
    BAT_VOLTAGE = const(35)
    BAT_CHARGE = const(34)

    # APA102 Dotstar pins for production boards
    DOTSTAR_CLK = const(12)
    DOTSTAR_DATA = const(2)
    DOTSTAR_PWR = const(13)

    # SPI
    SPI_MOSI = const(23)
    SPI_CLK = const(18)
    SPI_MISO = const(19)

    #I2C
    I2C_SDA = const(21)
    I2C_SCL = const(22)

    #DAC
    DAC1 = const(25)
    DAC2 = const(26)
..

Helper functions
----------------
.. code-block:: python

    # Get a *rough* estimate of the current battery voltage
    # If the battery is not present, the charge IC will still report it's trying to charge at X voltage
    # so it will still show a voltage.
    def get_battery_voltage()

    # Return the current charge state of the battery - we need to read the value multiple times
    # to eliminate false negatives due to the charge IC not knowing the difference between no battery
    # and a full battery not charging - This is why the charge LED flashes
    def get_battery_charging()

    # Return the internal PICO-D4 temperature in Fahrenheit
    def get_internal_temp_F()

    # Return the internal PICO-D4 temperature in Celsius
    def get_internal_temp_C()

    # Power to the on-board Dotstar is controlled by a PNP transistor, so low is ON and high is OFF
    # We also need to set the Dotstar clock and data pins to be inputs to prevent power leakage when power is off
    # This might be improved at a future date
    # The reason we have power control for the Dotstar is that it has a quiescent current of around 1mA, so we
    # need to be able to cut power to it to minimise power consumption during deep sleep or with general battery powered use
    # to minimise unneeded battery drain
    def set_dotstar_power( state )

    # Dotstar rainbow colour wheel
    def dotstar_color_wheel( wheel_pos )

    # Go into deep sleep but shut down the APA first to save power
    # Use this  if you want lowest deep  sleep current
    def go_deepsleep( t )
..

Example Usage
-------------
.. code-block:: python

    from machine import SPI, Pin
    import tinypico as TinyPICO
    from micropython_dotstar import DotStar
    import time, random, micropython

    # Configure SPI for controlling the DotStar
    # Internally we are using software SPI for this as the pins being used are not hardware SPI pins
    spi = SPI(sck=Pin( TinyPICO.DOTSTAR_CLK ), mosi=Pin( TinyPICO.DOTSTAR_DATA ), miso=Pin( TinyPICO.SPI_MISO) )
    # Create a DotStar instance
    dotstar = DotStar(spi, 1, brightness = 0.5 ) # Just one DotStar, half brightness
    # Turn on the power to the DotStar
    TinyPICO.set_dotstar_power( True )

    # Say hello
    print("\nHello from TinyPICO!")
    print("--------------------\n")

    # Show some info on boot
    print("Battery Voltage is {}V".format( TinyPICO.get_battery_voltage() ) )
    print("Battery Charge State is {}\n".format( TinyPICO.get_battery_charging() ) )

    # Show available memory
    print("Memory Info - micropython.mem_info()")
    print("------------------------------------")
    micropython.mem_info()

    # Read the data every 15 seconds
    update_interval = 5
    # Make sure it fires immediately by starting it in the past
    update_temp_time = time.time() - 10

    def print_temp():
        global update_interval
        global update_temp_time

        # We only run the contents of this function every 5 seconds
        if update_temp_time < time.time():
            update_temp_time = time.time() + update_interval

            # Grab the temperatures and print them
            print("\nInternal PICO-D4 Temp: {}°F {:.2f}°C".format( TinyPICO.get_internal_temp_F(), TinyPICO.get_internal_temp_C() ) )


    # Create a colour wheel index int
    color_index = 0

    # Rainbow colours on the Dotstar
    while True:
        # Get the R,G,B values of the next colour
        r,g,b = TinyPICO.dotstar_color_wheel( color_index )
        # Set the colour on the dotstar
        dotstar[0] = ( r, g, b, 0.5)
        # Increase the wheel index
        color_index += 1
        # Sleep for 20ms so the colour cycle isn't too fast
        time.sleep_ms(20)

        # Print the internal PICO-D4 temperature in F and C
        print_temp()
..
