# The MIT License (MIT)
#
# Copyright (c) 2019 Seon "Unexpected Maker" Rozenblum
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`tinypico-playshield-snake` - Snake Game for the TinyPICO Play Shield
=====================================================================
* Author(s): Seon Rozenblum
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/unexpectedmaker/tinypico"

from machine import I2C, Pin, Timer, PWM
import tinypico as TinyPICO
import time, random, ssd1306, framebuf, bitmaps, math, notes
from micropython import const

# Turn off the power to the DotStar
TinyPICO.set_dotstar_power( False )

class Snake:

    def reset(self, x, y, len, dir):
        self._moves = 0
        self._dead = False
        self._length = len
        self._dir = 0
        self._speed = 0.12
        self._score = 0
        self._fruit = []

        # set snake head position
        self._list = [ [x,y] ]
        # dynamically create snake body based on starting position
        for i in range( self._length-1 ):

            if self._dir == 0:
                y += 2
            elif self._dir == 1:
                x -= 2
            elif self._dir == 2:
                y -= 2
            elif self._dir == 3:
                x += 2
            
            self._list.append( [x,y] )
        
        self.add_fruit()

    def __init__(self, x, y, len, dir):
        self.reset( x, y, len, dir )

    def set_dir(self, dir):
        # Chnage directiom
        self._dir += dir

        # Wrap direction
        if self._dir < 0:
            self._dir = 3
        elif self._dir > 3:
            self. _dir = 0

    def move(self):
        # Increase snake length every 10 moves
        # self._moves += 1
        # if self._moves == 10:
        #     self._moves = 0
        #     self._length += 1

        remove_tail = [0,0,0,0]

        if len( self._list ) == self._length:
            x,y = self._list[ self._length-1 ]
            remove_tail[0] = x
            remove_tail[1] = y
            del self._list[ self._length-1 ]

        # Grab the x,y of the head
        x, y = self._list[0]

        # move the head based on the current direction
        if self._dir == 0:
            y -= 2
        elif self._dir == 1:
            x += 2
        elif self._dir == 2:
            y += 2
        elif self._dir == 3:
            x -= 2

        # Did we hit the outer bounds of the level?
        hit_bounds = x < 1 or y < 1 or x > 125 or y > 61

        # Is the x,y position already in the list? If so, we hit ourselves and died - we also died if we hit the edge of the level 
        self._dead = self._list.count( [x,y] ) > 0 or hit_bounds

        # Add the next position as the head of the snake
        self._list.insert( 0, [x,y] )

        # Did we eat any fruit?
        for f in self._fruit:
            fx,fy = f

            if x >= fx-2 and x <= fx+1 and y >= fy-2 and y <= fy+1:
                remove_tail[2] = fx
                remove_tail[3] = fy
                self.eat_food()
                self._fruit.remove( f )
                self.add_fruit()

        return remove_tail

    def is_dead(self):
        return self._dead

    def get_positions(self):
        return self._list

    def get_speed(self):
        return self._speed

    def get_score(self):
        return self._score

    def eat_food(self):
        self._score += 1
        self._length += 2
        # reduce the speed time delay, burt clamped between 0.05 and 0.12
        self._speed = max(0.01, min( self._speed - 0.01, 0.12))

        # print("Score {}, Speed {}".format( self._score, self._speed))

    def add_fruit(self):
        x = random.randrange(2,60) * 2
        y = random.randrange(2,30) * 2
        self._fruit.append( (x,y) )

    def get_fruit_positions(self):
        return self._fruit


# Globals

game_state = -1 #0 = menu, 1 = playing, 2 = pause, 3 = gameover
game_state_changed = False
fruit_interval = 10
fruit_next = 0


# Sound
def play_boot_music():
    speaker = PWM(Pin(25), freq=20000, duty=512)
    boot_sound = [notes.D4, 0, notes.G4, 0, notes.D4, 0, notes.A4, 0]
    for i in boot_sound:
        if i == 0:
            speaker.freq(0)
            time.sleep_ms(50)
            pass
        else:
            speaker.freq(i)
            time.sleep_ms(250)

    speaker.freq(0)
    speaker.deinit()

def play_death():
    speaker = PWM(Pin(25), freq=20000, duty=512)
    speaker.freq(notes.D4)
    time.sleep_ms(200)
    speaker.freq(0)
    time.sleep_ms(25)
    speaker.freq(notes.A2)
    time.sleep_ms(400)
    speaker.freq(0)
    speaker.deinit()

def play_sound( note, duration ):
    speaker = PWM(Pin(25), freq=20000, duty=512)
    speaker.freq(note)
    time.sleep_ms(duration)
    speaker.freq(0)
    speaker.deinit()

# Create an instance of Snake
snake = Snake( x=62, y=30, len=6, dir=0 )

def switch_state( new_state ):
    global game_state, game_state_changed
    if game_state == new_state:
        pass
    else:
       game_state = new_state
       game_state_changed = True

def player_turn(dir):
    global snake
    snake.set_dir(dir)

# Helpers

def text_horiz_centred(fb, text, y, char_width=8):
    fb.text(text, (fb.width - len(text) * char_width) // 2, y)

# Buttons
BUT_1 = Pin(26, Pin.IN )
BUT_2 = Pin(27, Pin.IN )
BUT_3 = Pin(15, Pin.IN )
BUT_4 = Pin(14, Pin.IN )

last_button_press_time = 0

def process_button_1():
    if game_state == 1:
        player_turn(1)

def process_button_2():
    if game_state == 0:
        switch_state(1)
    elif game_state == 3:
        switch_state(0)

def process_button_3():
    if game_state == 1:
        player_turn(-1)

def process_button_4():
    print("Pressed Button 4")

button_handlers = { str(BUT_1): process_button_1, str(BUT_2): process_button_2, str(BUT_3):process_button_3, str(BUT_4): process_button_4 }

def button_press_callback(pin):
    global last_button_press_time
    # block button press as software debounce
    if last_button_press_time < time.ticks_ms():
        
        # add 150ms delay between button presses... might be too much, we'll see!
        last_button_press_time = time.ticks_ms() + 150

        # If the pin is in the callback handler dictionary, call the appropriate function 
        if str(pin) in button_handlers:
            button_handlers[str(pin)]()
    # else:
    #     # print a debug message if button presses were too quick or a dounce happened
    #     print("Button Bounce - {}ms".format( ( last_button_press_time - time.ticks_ms() ) ) )

# Create all of the triggers for each button pointing to the single callback handler
BUT_1.irq(trigger=Pin.IRQ_FALLING, handler=button_press_callback)
BUT_2.irq(trigger=Pin.IRQ_FALLING, handler=button_press_callback)
BUT_3.irq(trigger=Pin.IRQ_FALLING, handler=button_press_callback)
BUT_4.irq(trigger=Pin.IRQ_FALLING, handler=button_press_callback)

# create timer for flashing UI
flasher = Timer(0)
flash_state = False
def flasher_update(timer):
    global flash_state
    flash_state = not flash_state

flasher.init(period=500, mode=Timer.PERIODIC, callback=flasher_update)

def flash_text(x,y,text):
    global flash_state
    if flash_state:
        oled.text(text, x, y, 2)
    else:
        oled.fill_rect( 1, y, 126, 12, 0)


# Begin

# Turn off the power to the DotStar
TinyPICO.set_dotstar_power( False )

# Configure I2C for controlling anything on the I2C bus
# Software I2C only for this example but the next version of MicroPython for the ESP32 supports hardware I2C too
i2c = I2C(scl=Pin(22), sda=Pin(21))

# Initialise the OLED screen
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Add the TP logo to a frameBuf buffer and show it for 2 seconds
fbuf = framebuf.FrameBuffer(bytearray(bitmaps.icon_tinypico), 128, 30, framebuf.MONO_HLSB)
oled.blit(fbuf, 0, 2)
text_horiz_centred( oled, "PLAY SHIELD", 35)
text_horiz_centred( oled, "INTEL NOT INSIDE", 50)

oled.show()
play_boot_music()
time.sleep(2)

# show the menu on start
switch_state(0)

def show_menu():
    # clear the display
    oled.fill(0)
    # Show welcome message
    text_horiz_centred( oled, "TINY SNAKE", 0 )
    text_horiz_centred( oled, "3-Left  1-Right", 50 )
    oled.line(0, 12, 127, 12,1 )
    # oled.text("TINY SNAKE", 25, 0, 2)
    # oled.text("3-Left  1-Right", 4, 50, 2)
    oled.show()

def draw_snake():
    global snake, fruit_next, fruit_interval
    # Move the snake and return if we need to clear the tail or if the snake grew
    result = snake.move()

    # The snake tail position is stored in result index 0,1 if it needs to be removed
    # If x or y are > 0 then we reove that pos from the screen
    if result[0] > 0 or result[1] > 0:
        oled.fill_rect(result[0], result[1], 2, 2, 0)

    # The last eaten fruit position is stored in indexs 2,3 if it needs to be removed
    # If x or y are > 0 then we reove that pos from the screen
    if result[2] > 0 or result[3] > 0:
        oled.fill_rect(result[2]-1, result[3]-1, 3, 3, 0)
        play_sound(notes.C4,100)

    # Go through the snake positions and draw them
    for pos in snake.get_positions():
        oled.fill_rect(pos[0], pos[1], 2, 2, 1)

    # Redraw all fruit
    for pos in snake.get_fruit_positions():
        oled.fill_rect(pos[0]-1, pos[1]-1, 3, 3, 1)

    # Update the OLED
    oled.show()
    time.sleep( snake.get_speed() )

    # If the snake died in that move, end the game
    if snake.is_dead():
        play_death()
        switch_state( 3 )

def setup_new_game():
    oled.fill(0)
    oled.rect(0, 0, 128, 64, 1)
    # oled.rect(1, 1, 127, 63, 1)
    oled.show()

    #reset variables
    global snake, fruit_next, fruit_interval
    snake.reset( x=62, y=30, len=3, dir=0 )

    fruit_next = time.time() + fruit_interval

    draw_snake()

def show_gameover():
    global snake
    oled.fill(0)
    text_horiz_centred( oled, "YOU SCORED " + str( snake.get_score() ), 10 )
    text_horiz_centred( oled, "2 - Continue", 50 )
    # oled.text("YOU SCORED " + str( snake.get_score() ), 10, 10, 2)
    # oled.text("2 - Continue", 15, 50, 2)
    oled.show()



while True:
    if game_state_changed:
        game_state_changed = False

        if game_state == 0:
            show_menu()
        elif game_state == 1:
            setup_new_game()
        elif game_state == 3:
            show_gameover()

    # menu
    if game_state == 0:
        flash_text( 0, 30, "Press 2 to start")
        oled.show()
        time.sleep(.001)

    elif game_state == 1:
        draw_snake()

    elif game_state == 3:
        flash_text( 24, 30, "GAME OVER")
        oled.show()
        time.sleep(.001)

    
    





