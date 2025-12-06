# Imports
from machine import Pin
import time

#Set up our LED names and GPIO pin numbers
red = Pin(18, Pin.OUT)
amber = Pin(19, Pin.OUT)
green = Pin(20, Pin.OUT)

def traffic_light_sequence(redState: int, amberState: int, greenState: int):
    red.value(redState)
    amber.value(amberState)
    green.value(greenState)


counter = 1 # Set the counter to 1

traffic_light_sequence(0, 0, 0) # Turn all lights OFF

while counter < 11: # While count is less than 11
    
    print(counter) # Print the current counter
    
    traffic_light_sequence(1, 0, 0)
    time.sleep(0.5) # Wait half a second
    traffic_light_sequence(0, 1, 0)
    time.sleep(0.5) # Wait half a second
    traffic_light_sequence(0, 0, 1)
    time.sleep(0.5) # Wait half a second
    
    counter += 1 # Add 1 to our counter

traffic_light_sequence(0, 0, 0) # Turn all lights OFF