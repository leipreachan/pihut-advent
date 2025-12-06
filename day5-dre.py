# Imports
import re
from machine import Pin, PWM, ADC
import time

# Set up the Buzzer pin as PWM
buzzer = PWM(Pin(13)) # Set the buzzer to PWM mode
potentiometer = ADC(Pin(27))

# Create our library of tone variables for "Jingle Bells"

A = 430
As = 467
B = 494
C = 525
Cs = 557
D = 590
Ds = 625
E = 659
F = 698
Fs = 740
G = 784
Gs = 830

notes = {
    "A": A,
    "A#": As,
    "AS": As,
    "B": B,
    "C": C,
    "C#": Cs,
    "CS": Cs,
    "D": D,
    "D#": Ds,
    "DS": Ds,
    "E": E,
    "F": F,
    "F#": Fs,
    "FS": Fs,
    "G": G,
    "GS": Gs,
    "G#": Gs
}

red = ["A", "A#", "AS", "B", "C", "C#", "CS"]
green = ["D", "D#", "DS", "E"]
amber = ["F", "F#", "FS", "G", "G#", "GS"]

leds = [
    Pin(20, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(18, Pin.OUT)
]

# Create volume variable (Duty cycle)
max = 65000
min = 1000

led_on = 40_000
led_fade = 1_000
led_off = 100

def reset_leds():
    for led in leds:
        led.value(0)
    # for pwm_led in pwm_leds:
    #     pwm_led.freq(1000)
        
def volume() -> int:
    reading = potentiometer.read_u16() # Read the potentiometer value and store it in our 'reading' variable
    return reading

def get_led(note: str) -> Pin:
    if note in red:
        return leds[0]
    elif note in green:
        return leds[1]
    else:
        return leds[2]
     
        
def turn_led_by_freq(note: str, val: int):
    if note in red:
        print(f"Red LED {val}")
        leds[0].value(1)
        # pwm_leds[0].duty_u16(val)
    elif note in green:
        print(f"Green LED {val}")
        leds[1].value(1)
        # pwm_leds[1].duty_u16(val)
    elif note in amber:
        print(f"Amber LED {val}")
        leds[2].value(1)
        # pwm_leds[2].duty_u16(val)
    
def get_freq_by_note(note: str) -> int:
    return notes[note]

# Create our function with arguments
def playtone(note: str|None, vol: int, delay1: str|None, delay2: str|None) -> None:
    print(f"{note=} {vol=} {delay1=} {delay2=}")
    if note and note != "REST":
        freq = get_freq_by_note(note)
        led = get_led(note)
        led.value(1)
        buzzer.duty_u16(vol)
        buzzer.freq(freq)
        
    delay = 1/float(delay1) if delay1 else 0.05
    time.sleep(delay)
    
    if note and note != "REST":
        led.value(0)
    buzzer.duty_u16(0)
    
    delay = 1/float(delay2) if delay2 else 0.25
    time.sleep(delay)
    
def playmelody(melody: str):
    list_of_notes = melody.split("-")
    for note in list_of_notes:
        vol = volume()
        
        clean_note = note.strip()
        v = re.match("((\d+):)?([A-z]+)(:(\d+))?", clean_note)
        [_, delay1, name, _, delay2] = v.groups() if v else [None, None, None, None, None]
        playtone(name, vol, delay1, delay2)
        

# dre_riff()
dre = "C - D - A - C - D - A - D - B - D - A - B - D - G - D - C - D - A - C - D - A - D - D - B - D - A - B - D - G - D - C - D - A - C - D - A - D - B - D - A - B - D - G - D - C - D - A - C - D - A - D - B - D - A - B - D - G - D" 
mario = "E - E - E - E - C - E - G - G - C - G - E - C - E - E - E - C - E - G"
got = "8:G - 8:C - 16:DS - 16:F - 8:G - 8:C - 16:DS - 16:F - 8:G - 8:C - 16:DS - 16:F - 8:G - 8:C - 16:DS - 16:F - 8:G - 8:C - 16:E - 16:F - 8:G - 8:C - 16:E - 16:F - 8:G - 8:C - 16:E - 16:F - 8:G - 8:C - 16:E - 16:F - 4:G - 4:C - 16:DS4 - 16:F4 - 4:G4 - 4:C4 - 16:DS4 - 16:F4 - 1:D4 - 4:F4 - 4:AS3 - 16:DS4 - 16:D4 - 4:F4 - 4:AS3 - 16:DS4 - 16:D4 - 1:C4 - 4:G4 - 4:C4 - 16:DS4 - 16:F4 - 4:G4 - 4:C4 - 16:DS4 - 16:F4 - 1:D4 - 4:F4 - 4:AS3 - 16:DS4 - 16:D4 - 4:F4 - 4:AS3 - 16:DS4 - 16:D4 - 1:C4 - 4:G4 - 4:C4 - 16:DS4 - 16:F4 - 4:G4 - 4:C4 - 16:DS4 - 16:F4 - 2:D4 - 4:F4 - 4:AS3 - 8:D4 - 8:DS4 - 8:D4 - 8:AS3 - 1:C4 - 2:C5 - 2:AS4 - 2:C4 - 2:G4 - 2:DS4 - 4:DS4 - 4:F4 - 1:G4 - 2:C5 - 2:AS4 - 2:C4 - 2:G4 - 2:DS4 - 4:DS4 - 4:D4 - 8:C5 - 8:G4 - 16:GS4 - 16:AS4 - 8:C5 - 8:G4 - 16:GS4 - 16:AS4 - 8:C5 - 8:G4 - 16:GS4 - 16:AS4 - 8:C5 - 8:G4 - 16:GS4 - 16:AS4 - 4:REST - 16:GS5 - 16:AS5 - 8:C6 - 8:G5 - 16:GS5 - 16:AS5 - 8:C6 - 16:G5 - 16:GS5 - 16:AS5 - 8:C6 - 8:G5 - 16:GS5 - 16:AS5"
tokyo_drift = "4:AS4 - 4:REST - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:F5 - 4:REST - 4:F5 - 4:REST - 3:GS5 - 3:FS5 - 4:F5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:GS5 - 3:FS5 - 4:F5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST"
pink_panter = "2:REST - 4:REST - 8:REST - 8:DS4 - 4:E4 - 8:REST - 8:FS4 - 4:G4 - 8:REST - 8:DS4 - 8:E4 - 8:FS4 - 8:G4 - 8:C5 - 8:B4 - 8:E4 - 8:G4 - 8:B4 - 2:AS4 - 16:A4 - 16:G4 - 16:E4 - 16:D4 - 2:E4 - 4:REST - 8:REST - 4:DS4 - 4:E4 - 8:REST - 8:FS4 - 4:G4 - 8:REST - 8:DS4 - 8:E4 - 8:FS4 - 8:G4 - 8:C5 - 8:B4 - 8:G4 - 8:B4 - 8:E5 - 1:DS5 - 2:D5 - 4:REST - 8:REST - 8:DS4 - 4:E4 - 8:REST - 8:FS4 - 4:G4 - 8:REST - 8:DS4 - 8:E4 - 8:FS4 - 8:G4 - 8:C5 - 8:B4 - 8:E4 - 8:G4 - 8:B4 - 2:AS4 - 16:A4 - 16:G4 - 16:E4 - 16:D4 - 4:E4 - 4:REST - 4:REST - 8:E5 - 8:D5 - 8:B4 - 8:A4 - 8:G4 - 8:E4 - 16:AS4 - 8:A4 - 16:AS4 - 8:A4 - 16:AS4 - 8:A4 - 16:AS4 - 8:A4 - 16:G4 - 16:E4 - 16:D4 - 16:E4 - 16:E4 - 2:E4"
  
def main(melody: str):
    reset_leds()
    time.sleep(1)
    playmelody(melody)
    reset_leds()

main(pink_panter)