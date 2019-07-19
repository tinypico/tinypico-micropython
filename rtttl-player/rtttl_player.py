# TinyPICO RTTTL Player
# This should also work with any ESP32  

from rtttl import RTTTL
import songs, time
from machine import Pin, PWM

# Setup a PWM reference to GPIO25 which is DAC1
buz = PWM(Pin(25), freq=550, duty=0)

# Change this to adjust the volume
pwm = 50

def play_tone(freq, msec):
    print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    if freq > 0:
        buz.freq( int(freq) )
        buz.duty( int(pwm) )
    time.sleep_ms( int(msec * 0.9 ) )
    buz.duty(0)
    time.sleep_ms( int(msec * 0.1 ) )

def play(tune):
    try:
        for freq, msec in tune.notes():
            play_tone(freq, msec)
    except KeyboardInterrupt:
        play_tone(0, 0)

def play_song(search):
    play(RTTTL(songs.find(search)))

# play songs from songs.py
# play_song('Entertainer')

# play songs directly
play_song('Bond')

# play songs by passing RTTTL data directly
#play( RTTTL('Monty Python:d=8,o=5,b=180:d#6,d6,4c6,b,4a#,a,4g#,g,f,g,g#,4g,f,2a#,p,a#,g,p,g,g,f#,g,d#6,p,a#,a#,p,g,g#,p,g#,g#,p,a#,2c6,p,g#,f,p,f,f,e,f,d6,p,c6,c6,p,g#,g,p,g,g,p,g#,2a#,p,a#,g,p,g,g,f#,g,g6,p,d#6,d#6,p,a#,a,p,f6,f6,p,f6,2f6,p,d#6,4d6,f6,f6,e6,f6,4c6,f6,f6,e6,f6,a#,p,a,a#,p,a,2a#') )

