# Imports
from machine import ADC, Pin, PWM
import time

# Set up the potentiometer on ADC pin 27
potentiometer = ADC(Pin(27))

# Set up the LED pins
leds = [
    Pin(20, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(18, Pin.OUT),
]

pwm_leds = [
    PWM(Pin(20)),
    PWM(Pin(19)),
    PWM(Pin(18))
]

# Create a variable for our reading
reading = 0
on = 40_000
fade = 1_000
off = 100

def reset_leds():
    # for led in leds:
    #     led.value(0)

    for pwm_led in pwm_leds:
        pwm_led.freq(1000)


reset_leds()
while True: # Run forever
    
    reading = potentiometer.read_u16() # Read the potentiometer value and set this as our reading variable value
    delay = 0.1 + (reading / 65535) * 0.9
    
    l = len(pwm_leds)
    for i in range(l):
        print(f"{(i+2)%l=} {fade=}, {(i+1)%l=} {off=}, {i=} {on=} {delay}")
        pwm_leds[(i+1)%l].duty_u16(off)
        pwm_leds[(i+2)%l].duty_u16(fade)
        pwm_leds[i].duty_u16(on)
        time.sleep(delay) # short delay

