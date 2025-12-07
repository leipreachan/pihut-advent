# Imports
from machine import Pin, PWM
import time

onboardLED = Pin(25, Pin.OUT)

# Set up the LED pins
red = Pin(18, Pin.OUT)
amber = Pin(19, Pin.OUT)
green = Pin(20, Pin.OUT)

# Set up the Buzzer pin as PWM
buzzer = PWM(Pin(13))

# Set PWM duty to 0% at program start
buzzer.duty_u16(0)
 
# Set up PIR pin with pull down
pir = Pin(26, Pin.IN, Pin.PULL_DOWN)

onboardLED.value(1) # Turn onboard LED ON to show program is running

# Warm up/settle PIR sensor
print("Warming up...")
time.sleep(10) # Delay to allow the sensor to settle
print("Sensor ready!")

def alarm(): # Our alarm function
    # Set PWM duty (volume up)
    buzzer.duty_u16(10000)
    for _ in range(1): # Run this 5 times
        buzzer.freq(1000) # Higher pitch
        
        red.value(1) # Red ON
        amber.value(1) # Amber ON
        green.value(1) # Green ON
        
        time.sleep(0.5)
        
        buzzer.freq(500) # Lower pitch
        
        red.value(0) # Red OFF
        amber.value(0) # Amber OFF
        green.value(0) # Green OFF
        
        time.sleep(0.5)

    # Set PWM duty (volume off)
    buzzer.duty_u16(0)
        
while True: # Run forever
    
    time.sleep(0.01) # Delay to stop unnecessary program speed
    
    if pir.value() == 1: # If PIR detects movement
        
        print("I SEE YOU!")
    
        alarm() # Call our function
        
        print("Sensor active") # Let us know that the sensor is active again

