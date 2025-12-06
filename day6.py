# Imports
from machine import ADC, Pin
import time

# Set up the LED pins
red = Pin(18, Pin.OUT)
amber = Pin(19, Pin.OUT)
green = Pin(20, Pin.OUT)

# Define pin for our sensor
lightsensor = ADC(Pin(26))

while True: # Run forever
    
    # Read sensor value and store it in a variable called 'light'
    light = lightsensor.read_u16()

    # Use the round function to limit the decimal places to 1
    lightpercent = round(light/65535*100,1)

    # Print our reading percentage with % symbol
    print(f"{light=} {lightpercent}%")
    
    # 1 second delay between readings
    time.sleep(1)

    if lightpercent <= 30: # If percentage is less than or equal to 30
        
        red.value(1) # Red LED on
        amber.value(0)
        green.value(0)

    elif 30 < lightpercent < 60: # If percentage is between 30 and 60
        
        red.value(0)
        amber.value(1) # Amber LED on
        green.value(0)

    elif lightpercent >= 60: # If percentage is greater than or equal to 60
        
        red.value(0)
        amber.value(0)
        green.value(1) # Green LED on