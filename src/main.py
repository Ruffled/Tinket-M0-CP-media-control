"""
A CircuitPython 'multimedia' dial demo
Uses a Trinket M0 + Rotary Encoder -> HID consumer_control out
"""

import time
from digitalio import DigitalInOut, Direction, Pull
from board import D2, D3, D4
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Encoder button is a digital input with pullup on D2
button = DigitalInOut(D2)
button.direction = Direction.INPUT
button.pull = Pull.UP

# Rotary encoder inputs with pullup on D3 & D4
rot_a = DigitalInOut(D3)
rot_a.direction = Direction.INPUT
rot_a.pull = Pull.UP
rot_b = DigitalInOut(D4)
rot_b.direction = Direction.INPUT
rot_b.pull = Pull.UP

# Used to do HID output, see below
doing_keyboard = True

if doing_keyboard:
    cc = ConsumerControl(usb_hid.devices)

######################### MAIN LOOP ##############################

# the counter counts up and down, it can roll over! 16-bit value
encoder_counter = 0
# direction tells you the last tick which way it went
encoder_direction = 0

# constants to help us track what edge is what
A_POSITION = 0
B_POSITION = 1
UNKNOWN_POSITION = -1  # initial state so we know if something went wrong

rising_edge = falling_edge = UNKNOWN_POSITION

# get initial/prev state and store at beginning
last_button = button.value
current_button = last_button
rotary_prev_state = [rot_a.value, rot_b.value]
button_pressed = 0.0
double_click = False
double_pending = False
long_press = False
double_click_thresh = 0.50
long_click_thresh = 0.80

while True:
    # reset encoder and wait for the next turn
    encoder_direction = 0

    # take a 'snapshot' of the rotary encoder state at this time
    rotary_curr_state = [rot_a.value, rot_b.value]
    current_button = button.value

    if rotary_curr_state != rotary_prev_state:
        # print("Changed")
        if rotary_prev_state == [True, True]:
            # we caught the first falling edge!
            if not rotary_curr_state[A_POSITION]:
                # print("Falling A")
                falling_edge = A_POSITION
            elif not rotary_curr_state[B_POSITION]:
                # print("Falling B")
                falling_edge = B_POSITION
            else:
                # uhh something went deeply wrong, lets start over
                continue

        if rotary_curr_state == [True, True]:
            # Ok we hit the final rising edge
            if not rotary_prev_state[B_POSITION]:
                rising_edge = B_POSITION
                # print("Rising B")
            elif not rotary_prev_state[A_POSITION]:
                rising_edge = A_POSITION
                # print("Rising A")
            else:
                # uhh something went deeply wrong, lets start over
                continue

            # check first and last edge
            if (rising_edge == A_POSITION) and (falling_edge == B_POSITION):
                encoder_counter -= 1
                encoder_direction = -1
                print("%d dec" % encoder_counter)
            elif (rising_edge == B_POSITION) and (falling_edge == A_POSITION):
                encoder_counter += 1
                encoder_direction = 1
                print("%d inc" % encoder_counter)
            else:
                # (shrug) something didn't work out, oh well!
                encoder_direction = 0

            # reset our edge tracking
            rising_edge = falling_edge = UNKNOWN_POSITION

    rotary_prev_state = rotary_curr_state

    # Check if rotary encoder went up
    if doing_keyboard:
        if encoder_direction == 1:
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)

        # Check if rotary encoder went down
        if encoder_direction == -1:
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)

    # Button was 'just pressed'
    if current_button != last_button:
        if current_button:
            button_released = time.monotonic()
            button_delta = button_released - button_pressed
            if button_delta < double_click_thresh:
                if double_pending:
                    double_click = True
                    double_pending = False
                else:
                    double_click = False
                    double_pending = True
                long_press = False
            elif button_delta > long_click_thresh:
                double_click = False
                double_pending = False
                long_press = True
            else:
                double_click = False
                double_pending = False
                long_press = False

            print("Button Released, time", str(button_delta), "double",
                str(double_click), "long", str(long_press), sep=" ")

            if doing_keyboard:
                if long_press:
                    cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
                    long_press = False
                elif double_click:
                    cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
                    double_click = False
                else:
                    cc.send(ConsumerControlCode.PLAY_PAUSE)
        else:
            if double_pending:
                button_delta = time.monotonic() - button_pressed
                if button_delta > double_click_thresh:
                    double_pending = False
                    button_pressed = time.monotonic()
            else:
                button_pressed = time.monotonic()

            # print("Button Pressed")

    last_button = current_button