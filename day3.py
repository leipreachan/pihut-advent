# Imports
from machine import Pin
from time import sleep

# Set up our LED names and GPIO pin numbers
red = Pin(20, Pin.OUT)
amber = Pin(19, Pin.OUT)
green = Pin(18, Pin.OUT)

# Set up our button names and GPIO pin numbers
# Also set pins as inputs and use pull downs
buttons = [
    (Pin(13, Pin.IN, Pin.PULL_DOWN), red),
    (Pin(8, Pin.IN, Pin.PULL_DOWN), green),
    (Pin(3, Pin.IN, Pin.PULL_DOWN), amber)
]


while True: # Loop forever

    sleep(0.4) # Short delay
          
    i = 0
    for button, led in buttons:
        i += 1
        if button.value() == 1: # If button is pressed
            print(f"Button on pin {i} pressed")
            led.toggle() # Toggle corresponding LED on/off  
        
        
