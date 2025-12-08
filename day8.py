# Imports
import onewire
import ds18x20
import time
from machine import Pin, PWM, ADC

onboardLED = Pin(25, Pin.OUT)

# Set up the LED pins
leds = {
"red" : Pin(20, Pin.OUT),
"amber" : Pin(19, Pin.OUT),
"green" : Pin(18, Pin.OUT)
}
 
# Set the data pin for the sensor
SensorPin = Pin(26, Pin.IN)
 
# Tell MicroPython that we're using a DS18B20 sensor, and which pin it's on
sensor = ds18x20.DS18X20(onewire.OneWire(SensorPin))

# Buzzer
buzzer = PWM(Pin(13))

# Potentiometer
potentiometer = ADC(Pin(27))

# Look for DS18B20 sensors (each contains a unique rom code)
roms = sensor.scan()

# Start PWM duty to 0% at program start
buzzer.duty_u16(0)

prev_temperature = None   
prev_grade = None 

def turn_on_led(led_color: str|None = None):
    for led in leds:
        if led == led_color:
            leds[led].value(1)
        else:
            leds[led].value(0)

def switch_and_blink(led_color: str):
    for _ in range(3):
        turn_on_led()
        time.sleep(0.2)
        turn_on_led(led_color)
        time.sleep(0.2)

def beep():
    volume = potentiometer.read_u16()
    buzzer.duty_u16(volume if volume else 6_000)
    buzzer.freq(500) # low pitch
    time.sleep(0.2)
    buzzer.duty_u16(0) # turn off

def get_grade_by_reading(reading: int) -> str:
    if reading <= 18: # If reading is less than or equal to 18
        return "red"
    elif 18 < reading < 22: # If reading is between 18 and 22
        return "amber"
    return "green"

def alarm(): # Our alarm function
    
    buzzer.duty_u16(10000) # Buzzer duty (volume) up

    for i in range(5): # Run this 5 times
        
        buzzer.freq(5000) # Higher pitch
        
        # LEDs ON
        leds["red"].value(1)
        leds["amber"].value(1)
        leds["green"].value(1)
        
        time.sleep(0.2) # wait 1 second
        
        buzzer.freq(1000) # Lower pitch
        
        # LEDs OFF
        leds["red"].value(0)
        leds["amber"].value(0)
        leds["green"].value(0)       
        
        time.sleep(0.2) # wait 1 second

    buzzer.duty_u16(0) # Buzzer duty (volume) off 


turn_on_led()    
onboardLED.value(1)
while True: # Run forever

    time.sleep(5) # Wait 5 seconds between readings
    sensor.convert_temp() # Convert the sensor units to centigrade

    for rom in roms: # For each sensor found (just 1 in our case)
    
        time.sleep(1) # Always wait 1 second after converting
    
        reading = sensor.read_temp(rom)
        if prev_temperature is None or abs(prev_temperature - reading) >= 0.05:
            onboardLED.value(0)
            print(f"{sensor.read_temp(rom)}°C        ", end = "\r") # Print the temperature reading with °C after it
            prev_temperature = reading
            
            grade = get_grade_by_reading(reading)
            if  prev_grade != grade:
                # alarm()
                beep()
                switch_and_blink(grade)
                prev_grade = grade
                
