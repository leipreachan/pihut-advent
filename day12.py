# Imports
import time
import random
from machine import Pin, ADC
from neopixel import NeoPixel

NUMBER_OF_LEDS = 15
# Define the strip pin number (28) and number of LEDs (15)
strip = NeoPixel(Pin(28), NUMBER_OF_LEDS)
button = Pin(15, Pin.IN, Pin.PULL_DOWN)

# Set up the potentiometer on ADC pin 26
potentiometer = ADC(Pin(26))


def random_bit():
    return random.randint(0, 255)


def random_color():
    return random_bit(), random_bit(), random_bit()


def get_delay():
    return potentiometer.read_u16() / 50000


def create_map():
    result = []
    seq = list(range(NUMBER_OF_LEDS))
    for _ in range(NUMBER_OF_LEDS):
        new_val = random.choice(seq)  # type: ignore
        result.append(new_val)
        seq.remove(new_val)  # type: ignore

    return result


def run_ligths_from_list(map, color):
    for i in map:
        mydelay = get_delay()
        # Set the next LED in the range to light with a colour
        strip[i] = color
        # Delay - the speed of the chaser
        time.sleep(mydelay)

        # Send the data to the strip
        strip.write()

def pattern_map(color):
    map = create_map()
    run_ligths_from_list(map, color)

def pattern_sequence(color):
    map = range(NUMBER_OF_LEDS)
    run_ligths_from_list(map, color)

def pattern_reverse_sequence(color):
    map = reversed(range(NUMBER_OF_LEDS))
    run_ligths_from_list(map, color)

def pattern_from_center(color):
    center = int(NUMBER_OF_LEDS/2)
    map = []
    for i in range(int(NUMBER_OF_LEDS/2)):
        map.append(center + i)
        map.append(center - i)
    
    run_ligths_from_list(map, color)
    

current_pattern = 0
patterns = [pattern_from_center, pattern_map, pattern_sequence, pattern_reverse_sequence]
last_press = 0
debounce_ms = 1000


def button_handle(p):
    global current_pattern
    global last_press
    now = time.ticks_ms()

    if time.ticks_diff(now, last_press) < debounce_ms:
        return  # debounce

    last_press = now
    current_pattern = (current_pattern + 1) % len(patterns)
    print(f"New pattern: {current_pattern}")


button.irq(lambda p: button_handle(p), Pin.PULL_DOWN)

while color := random_color():  # Run forever
    patterns[current_pattern](color)
    time.sleep(0.5)
