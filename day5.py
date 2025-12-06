# Imports
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

# Create volume variable (Duty cycle)
volume = potentiometer.read_u16()  # Read the potentiometer value and store it in our 'volume' variable

# Create our function with arguments
def playtone(note,vol,delay1,delay2):
    buzzer.duty_u16(vol)
    buzzer.freq(note)
    time.sleep(delay1)
    buzzer.duty_u16(0)
    time.sleep(delay2)
    
# Play the tune
# playtone(E,volume,0.1,0.2)
# playtone(E,volume,0.1,0.2)
playtone(A,volume,4,0.5) #Longer second delay

# playtone(E,volume,0.1,0.2)
# playtone(E,volume,0.1,0.2)
# playtone(E,volume,0.1,0.5) #Longer second delay

# playtone(E,volume,0.1,0.2)
# playtone(G,volume,0.1,0.2)
# playtone(C,volume,0.1,0.2)
# playtone(D,volume,0.1,0.2)
# playtone(E,volume,0.1,0.2)

# Duty to 0 to turn the buzzer off
buzzer.duty_u16(0)
