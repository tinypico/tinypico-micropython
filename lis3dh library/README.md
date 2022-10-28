# MicroPython-LIS3DH
MicroPython library for the LIS3DH IMU

This is the IMU IC used on the [TinyPICO Play shield](https://www.tinypico.com/add-ons).

## Currently under development
Proper interrupt support

## Example usage

```python
import lis3dh, time
from machine import Pin, I2C

i2c = I2C(sda=Pin(21), scl=Pin(22)) # Correct I2C pins for TinyPICO
imu = lis3dh.LIS3DH_I2C(i2c)

# If we have found the LIS3DH
if imu.device_check():
    # Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
    imu.range = lis3dh.RANGE_2_G

    # Loop forever printing accelerometer values
    while True:
        # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
        # z axis values.  Divide them by 9.806 to convert to Gs.
        x, y, z = [value / lis3dh.STANDARD_GRAVITY for value in imu.acceleration]
        print("x = %0.3f G, y = %0.3f G, z = %0.3f G" % (x, y, z))
        # Small delay to keep things responsive but give time for interrupt processing.
        time.sleep(0.1)
```
