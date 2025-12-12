from machine import Pin
from ky015 import DHT11
import time

onboardLED = Pin(25, Pin.OUT)


while True:
    onboardLED.value(1)
    time.sleep(3)
    pin = Pin(27, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)
    t = sensor.temperature
    h = sensor.humidity
    print(f"Temperature: {sensor.temperature}; Humidity: {sensor.humidity}     ", end="\r")
    time.sleep(1)
