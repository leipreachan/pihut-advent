# Imports
import time
import random
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from neopixel import NeoPixel

NUMBER_OF_LEDS = 15
# Define the strip pin number (28) and number of LEDs (15)
strip = NeoPixel(Pin(28), NUMBER_OF_LEDS)
button = Pin(15, Pin.IN, Pin.PULL_DOWN)
# Set up the potentiometer on ADC pin 26
potentiometer = ADC(Pin(26))
# Set up I2C and the pins we're using for it
i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
# Define the display and size (128x32)
display = SSD1306_I2C(128, 32, i2c)

black = (0, 0, 0)
counter = 0

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

def set_brightness(color, brightness):
    (red, green, blue) = color
    return (int(red * brightness), int(green * brightness), int(blue * brightness))
    
def fade_in(seconds, pixels, color, steps = 30):
    prev_pattern = current_pattern
    for i in range(steps):
        if prev_pattern != current_pattern:
            break
        for pixel in pixels:
            strip[pixel] = set_brightness(color, i/steps)
        time.sleep(seconds/steps)
        strip.write()
        
def fade_out(seconds, pixels, color, steps = 30):
    prev_pattern = current_pattern
    for i in range(steps+1):
        if prev_pattern != current_pattern:
            break
        for pixel in pixels:
            brightness = 0 if steps == i else (steps-i)/steps
            strip[pixel] = set_brightness(color, brightness)
        time.sleep(seconds/steps)
        strip.write()

def run_lights_from_list(map, color):
    for i in map:
        mydelay = get_delay()
        # Set the next LED in the range to light with a colour
        strip[i] = color
        # Delay - the speed of the chaser
        time.sleep(mydelay)

        # Send the data to the strip
        strip.write()

def fade_in_out_lights_from_list(map, color):
    mydelay = get_delay()
    for j in range(NUMBER_OF_LEDS):
        strip[j] = black
    strip.write()
    fade_in(1, map, color)
    fade_out(1, map, color)
    time.sleep(mydelay)

def pattern_dots(color):
    map = create_map()
    run_lights_from_list(map, color)


def pattern_sequence(color):
    map = range(NUMBER_OF_LEDS)
    run_lights_from_list(map, color)


def pattern_reverse_sequence(color):
    map = reversed(range(NUMBER_OF_LEDS))
    run_lights_from_list(map, color)


def pattern_wave_from_center(color):
    center = int(NUMBER_OF_LEDS / 2)
    map = []
    for i in range(int(NUMBER_OF_LEDS / 2) + 1):
        map.append(center + i)
        map.append(center - i)

    run_lights_from_list(map, color)
    
def pattern_dots_with_gaps(color):
    one_or_zero = counter % 2
    for i in range(NUMBER_OF_LEDS):
        mydelay = get_delay()
        if i % 2 == one_or_zero:
            strip[i] = color
        else:
            strip[i] = black
        strip.write()
        time.sleep(mydelay)

def pattern_dots_on_black(color):
    map = create_map()
    mydelay = get_delay()
    for i in map:
        for j in range(NUMBER_OF_LEDS):
            strip[j] = black
        strip[i] = color
        strip.write()
        time.sleep(mydelay)
       
def pattern_progressive_wave(color):
    center = int(NUMBER_OF_LEDS / 2)
    mydelay = get_delay()
    for j in range(center + 2):
        map = []
        for i in range(j):
            if i == 0:
                map.append(center)
            else:
                map.append(center + i)
                map.append(center - i)
        
        print(f"{map=}")
        for i in map:
            # strip[i] = set_brightness(color, center abs(center - i)/center)
            print(f"{i=} {strip[i]=}")
        
        strip.write()
        time.sleep(0.5)
        time.sleep(mydelay)

    
def pattern_fade_all(color):
    map = list(range(NUMBER_OF_LEDS))
    fade_in(1.5, map, color)
    fade_out(2, map, color)
    
def pattern_fade_dots_on_black(color):
    map = create_map()
    for i in map:
        mydelay = get_delay()
        for j in range(NUMBER_OF_LEDS):
            strip[j] = black
        strip.write()
        fade_in(0.5, [i], color)
        fade_out(0.5, [i], color)
        time.sleep(mydelay)
    
def pattern_fade_group_from_black(color):
    map = []
    for i in range(NUMBER_OF_LEDS):
        if random.randint(0, 1):
            map.append(i)
    if len(map) == 0:
        map.append(random.choice(list(range(NUMBER_OF_LEDS)))) # type: ignore
    fade_in_out_lights_from_list(map, color)
    
         
def pattern_turning_off_dots(color):
    map = create_map()
    mydelay = get_delay()
    run_lights_from_list(map, black)
    time.sleep(mydelay)
    for i in range(NUMBER_OF_LEDS):
        strip[i] = color
    strip.write()
        
    

def all_black():
    for i in range(NUMBER_OF_LEDS):
        strip[i] = black
    strip.write()
    time.sleep(1000)


current_pattern = 0
patterns = [
    # pattern_progressive_wave,
    pattern_fade_group_from_black,
    pattern_fade_dots_on_black,
    pattern_fade_all,
    pattern_wave_from_center,
    pattern_dots,
    pattern_sequence,
    pattern_reverse_sequence,
    pattern_dots_with_gaps,
    pattern_dots_on_black,
    pattern_turning_off_dots
]
last_press = 0
debounce_ms = 1000

def display_pattern_name():
    display.fill(0)
    text = f"{patterns[current_pattern].__name__.replace('_', ' ').replace('pattern ', '')}"
    chunk_size = 15
    chunks = [text[i:i + chunk_size].strip() for i in range(0, len(text), chunk_size)]
    line_num = 0
    for chunk in chunks:
        display.text(chunk, 0, line_num)
        line_num += 12
        
    display.show()

def button_handle(p):
    global current_pattern
    global last_press
    now = time.ticks_ms()

    if time.ticks_diff(now, last_press) < debounce_ms:
        return  # debounce

    last_press = now
    current_pattern = (current_pattern + 1) % len(patterns)
    print(f"New pattern: {current_pattern}")
    display_pattern_name()


button.irq(lambda p: button_handle(p), Pin.PULL_DOWN)

current_pattern = -1
button_handle(0)
while color := random_color():  # Run forever
    patterns[current_pattern](color)
    time.sleep(0.5)
