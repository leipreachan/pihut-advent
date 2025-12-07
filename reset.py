from machine import Pin, PWM

onboardLED = Pin(25, Pin.OUT)

leds = [
    Pin(18, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(20, Pin.OUT)
]

# Set up the Buzzer pin as PWM
buzzer = PWM(Pin(13))

    
def main():
    for led in leds:
        led.value(0)
        
    onboardLED.value(0)
    
    buzzer.duty_u16(0)


main()