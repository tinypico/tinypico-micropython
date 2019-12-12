# Examples using the MicroSD Card

import machine
import uos as os

# no sd card mounted
os.listdir()
['boot.py', 'main.py']

sd = machine.SDCard(slot=2)
# I (1090900) gpio: GPIO[5]| InputEn: 0| OutputEn: 1| OpenDrain: 0| Pullup: 0| Pulldown: 0| Intr:0

sd.info()
#(7948206080, 512)

# mount
os.mount(sd, '/sd')

os.listdir()
#['sd', 'boot.py', 'main.py']

os.listdir('/sd')
# ['hello.py']

# write
f = open('/sd/test.py', 'w')
f.write('print(\'hello\')\n')
f.close()

# read
f = open('/sd/test.py', 'r')
print(f.read())
f.close()

# append
f = open('/sd/test.py', 'a')
f.write('print(\'hello again\')\n')
f.close()

# read again
f = open('/sd/test.py', 'r')
print(f.read())
f.close()

# remove the file
os.remove('/sd/test.py')

# unmount
os.umount('/sd')

# yep, it's gone
os.listdir()
# ['boot.py', 'main.py']

sd.deinit()
# I (1199930) gpio: GPIO[23]| InputEn: 0| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0
# I (1199930) gpio: GPIO[19]| InputEn: 0| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0
# I (1199940) gpio: GPIO[18]| InputEn: 0| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0

sd.info()
# (7948206080, 512)
# (7948206080/1024/1024/1024 = 7.4GB) - 8GB SanDisk MicroSD card

# mount (fail)
os.mount(sd, '/sd')
# E (1278440) sdmmc_cmd: sdmmc_read_sectors_dma: sdmmc_send_cmd returned 0x103
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# OSError: [Errno 19] ENODEV

# reinit
sd = machine.SDCard(slot=2)

# mount (works!)
os.mount(sd, '/sd')
