# TinyPICO I2S Audio Shield Example
# Play .wav files from SD card

# Based on easy_wav_player example by Mike Teachman
# https://github.com/miketeachman/micropython-i2s-examples/blob/master/examples/easy_wav_player.py

# The MIT License (MIT)
# Copyright (c) 2021 Mike Teachman
# https://opensource.org/licenses/MIT

# machine.I2S docs:
# https://docs.micropython.org/en/latest/library/machine.I2S.html

# Free tool to convert mp3 to wav:
# https://audio.online-convert.com/convert-to-wav

# Drum loop from Zapsplat.com:
# https://www.zapsplat.com/sound-effect-category/loops/

# Setup:
# copy wavplayer.py to your filesystem
# copy .wav files to a SD card

import os
import time
from machine import Pin
from wavplayer import WavPlayer

# configure and mount SD card
from machine import SDCard
sd = SDCard(slot=2) # sck=18, mosi=23, miso=19, cs=5
os.mount(sd, "/sd")

# list files to your SD card
os.listdir('/sd')
# ['fart.wav', 'drum_loop_1.wav', 'drum_loop_3.wav', 'drum_loop_3.wav']

# adjust the gain (volume)
# gain = Pin(14)
# gain.init(Pin.IN, pull=Pin.PULL_DOWN) # gain 5: louder
# gain.init(Pin.OUT, value=0)           # gain 4: loud
# gain.init(Pin.IN, pull=None)          # gain 3: middle
# gain.init(Pin.OUT, value=1)           # gain 2: quiet
# gain.init(Pin.IN, pull=Pin.PULL_UP)   # gain 1: quieter

# init WavPlayer
wp = WavPlayer(id=0, sck_pin=Pin(27), ws_pin=Pin(26), sd_pin=Pin(25), ibuf=40000)

# play once
wp.play("fart.wav", loop=False)

# loop forever
wp.play("drum_loop_1.wav", loop=True)
# wp.play("drum_loop_2.wav", loop=True)
# wp.play("drum_loop_3.wav", loop=True)

if wp.isplaying():
    print('yes drum loop is playing')

# pause the drum loop
wp.pause()

# resume from where it was paused
wp.resume()

# stop playing
wp.stop()

# eject SD card
# os.umount("/sd")
