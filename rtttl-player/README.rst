Ring Tone Text Transfer Language Parser
=======================================

This library can parse RTTTL text lines and delivers the frequency and duration for each note.

This library was originally designed by Dave Hylands: https://github.com/dhylands/upy-rtttl


A typical RTTTL string looks like this:
```
Entertainer:d=4,o=5,b=140:8d,8d#,8e,c6,8e,c6,8e,2c.6,8c6,8d6,8d#6,8e6,8c6,8d6,e6,8b,d6,2c6,p,8d,8d#,8e,c6,8e,c6,8e,2c.6,8p,8a,8g,8f#,8a,8c6,e6,8d6,8c6,8a,2d6
```

You can find many more sample ring tones here: http://www.picaxe.com/RTTTL-Ringtones-for-Tune-Command/

You can find a description of RTTTL here: https://en.wikipedia.org/wiki/Ring_Tone_Transfer_Language

# Using RTTTL on the TinyPICO & Audio or Play shield

.. code-block:: python

    # play songs from songs.py
    play_song('Entertainer')

    # play songs directly
    play_song('Bond')

    # play songs by passing RTTTL data directly
    play( RTTTL('Monty Python:d=8,o=5,b=180:d#6,d6,4c6,b,4a#,a,4g#,g,f,g,g#,4g,f,2a#,p,a#,g,p,g,g,f#,g,d#6,p,a#,a#,p,g,g#,p,g#,g#,p,a#,2c6,p,g#,f,p,f,f,e,f,d6,p,c6,c6,p,g#,g,p,g,g,p,g#,2a#,p,a#,g,p,g,g,f#,g,g6,p,d#6,d#6,p,a#,a,p,f6,f6,p,f6,2f6,p,d#6,4d6,f6,f6,e6,f6,4c6,f6,f6,e6,f6,a#,p,a,a#,p,a,2a#') )
..

Files:
- rtttl_player.py: Playing RTTTL's on the TinyPICO or any other ESP32 board
- rtttl.py: RTTTL decoding library.
- songs.py: Optional collection of RTTTL songs to test the library.
