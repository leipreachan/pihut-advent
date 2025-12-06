from machine import Pin
from time import sleep

onboardLED = Pin(25, Pin.OUT)
for i in range(11):
    print(i%2)
    sleep(1)
    onboardLED.value(i % 2)
