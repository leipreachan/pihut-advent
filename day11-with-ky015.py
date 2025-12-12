# Imports
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from ky015 import DHT11, InvalidPulseCount
import time

# Set up I2C and the pins we're using for it
i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
button = Pin(8, Pin.IN, Pin.PULL_DOWN)
lightsensor = ADC(Pin(26))
th_sensor = DHT11(Pin(27, Pin.OUT, Pin.PULL_DOWN))
onboardLED = Pin(25, Pin.OUT)

onboardLED.value(1)
# Short delay to stop I2C falling over
time.sleep(1)

# Define the display and size (128x32)
display = SSD1306_I2C(128, 32, i2c)

enable_display = True
last_press = 0
debounce_ms = 1000   

def swap_display_state():
    global enable_display
    print(f"swap screen to {enable_display}")
    if enable_display:
        onboardLED.value(0)
        display.poweron()
    else:
        onboardLED.value(1)
        display.poweroff()

def button_handle(p):
    global enable_display
    global last_press
    now = time.ticks_ms()
    
    print("", end="\r")

    if time.ticks_diff(now, last_press) < debounce_ms:
        return  # debounce

    last_press = now
    enable_display = not enable_display
    swap_display_state()

def main():
    prev_light = 0
    prev_temp = 0
    prev_hum = 0

    button.irq(lambda p:button_handle(p), Pin.PULL_DOWN)        
    
    while True:
        # Delay
        if prev_light != 0 or prev_temp != 0 or prev_hum != 0:
            time.sleep(2)
        else:
            onboardLED.value(0)
        
        light = round((lightsensor.read_u16())/65535*100,1)
        
        try:
            t = th_sensor.temperature
            h = th_sensor.humidity
        except InvalidPulseCount:
            print("Couldn't connect to the temperature sensor - InvalidPulseCount")
            t = 0
            h = 0
        
        if abs(prev_light - light) < 0.3 and abs(prev_temp - t) < 0.5 and abs(prev_hum - h) < 0.5:
            continue
        
        prev_light = light
        prev_hum = h
        prev_temp = t
        # Print the light reading percentage
        print(light)
        
        if not enable_display:
            continue
        
        # Clear the display
        display.fill(0)
        
        # Write two lines to the display
        # The line turns our light variable into a string, and adds '%' to the end
        display.text(f"light {light}%", 0, 0)
        display.text(f"temperature {t}", 0, 12)
        display.text(f"humitidy {h}%", 0, 24)

        # Update the display
        display.show()
        
        
main()