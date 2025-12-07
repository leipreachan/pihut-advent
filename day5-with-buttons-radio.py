# Play melody with buttons to start/stop (day 3 + day 5), every button works as a stop/play toggle
# The potentiometer is used to "change the radio station"
# If the station is changed while playing, the playback stops with white noise
# Pressing any button also stops the playback with a kick sound

import re
from machine import Pin, PWM, ADC
import time
import urandom

# Set up the Buzzer pin as PWM
buzzer = PWM(Pin(13))  # Set the buzzer to PWM mode
potentiometer = ADC(Pin(27))
onboardLED = Pin(25, Pin.OUT)

A = 440
As = 466
B = 494
C = 261
Cs = 277
D = 293
Ds = 311
E = 330
F = 349
Fs = 370
G = 392
Gs = 415

notes = {
    "A": A,
    "AS": As,
    "B": B,
    "C": C,
    "CS": Cs,
    "D": D,
    "DS": Ds,
    "E": E,
    "F": F,
    "FS": Fs,
    "G": G,
    "GS": Gs,
}

note_to_led = [["A", "AS", "B", "C", "CS"], ["D", "DS", "E"], ["F", "FS", "G", "GS"]]

leds = [Pin(20, Pin.OUT), Pin(19, Pin.OUT), Pin(18, Pin.OUT)]

buttons = [
    Pin(12, Pin.IN, Pin.PULL_DOWN),
    Pin(8, Pin.IN, Pin.PULL_DOWN),
    Pin(3, Pin.IN, Pin.PULL_DOWN),
]

max = 65500
min = 0

led_on = 40_000
led_fade = 1_000
led_off = 100

button_state = False

dre = "8:G4:8 - 8:C5:8 - 8:D#5:8 - 8:F5:8 - 8:G4:8 - 8:C5:8 - 8:D#5:8 - 8:F5:8 - 8:G4:8 - 8:C5:8 - 8:D#5:8 - 8:F5:8 - 8:G4:8 - 8:C5:8 - 8:D#5:8 - 8:F5:8 - 8:REST:8 "
mario = "16:E5:16 - 16:E5:16 - 16:E5:8 - 8:REST:8 - 16:C5:16 - 16:E5:16 - 8:G5:8 - 8:REST:8 - 8:G4:8 - 8:REST:8 - 16:C5:16 - 16:G4:16 - 16:E4:16 - 16:A4:16 - 16:B4:16 - 16:A4:16 - 16:G4:16 - 16:E5:16 - 16:G5:16 - 16:A5:8 - 8:REST:8 - 16:F5:16 - 16:G5:16 - 16:F5:16 - 16:E5:16 - 16:D5:16 - 16:E5:16 - 16:C5:16 - 16:D5:16 - 8:B4:8 "
got = "8:G - 8:C - 16:DS - 16:F - 8:G - 8:C - 16:DS - 16:F - 8:G - 8:C - 16:DS - 16:F - 8:G - 8:C - 16:DS - 16:F - 8:G - 8:C - 16:E - 16:F - 8:G - 8:C - 16:E - 16:F - 8:G - 8:C - 16:E - 16:F - 8:G - 8:C - 16:E - 16:F - 4:G - 4:C - 16:DS4 - 16:F4 - 4:G4 - 4:C4 - 16:DS4 - 16:F4 - 1:D4 - 4:F4 - 4:AS3 - 16:DS4 - 16:D4 - 4:F4 - 4:AS3 - 16:DS4 - 16:D4 - 1:C4 - 4:G4 - 4:C4 - 16:DS4 - 16:F4 - 4:G4 - 4:C4 - 16:DS4 - 16:F4 - 1:D4 - 4:F4 - 4:AS3 - 16:DS4 - 16:D4 - 4:F4 - 4:AS3 - 16:DS4 - 16:D4 - 1:C4 - 4:G4 - 4:C4 - 16:DS4 - 16:F4 - 4:G4 - 4:C4 - 16:DS4 - 16:F4 - 2:D4 - 4:F4 - 4:AS3 - 8:D4 - 8:DS4 - 8:D4 - 8:AS3 - 1:C4 - 2:C5 - 2:AS4 - 2:C4 - 2:G4 - 2:DS4 - 4:DS4 - 4:F4 - 1:G4 - 2:C5 - 2:AS4 - 2:C4 - 2:G4 - 2:DS4 - 4:DS4 - 4:D4 - 8:C5 - 8:G4 - 16:GS4 - 16:AS4 - 8:C5 - 8:G4 - 16:GS4 - 16:AS4 - 8:C5 - 8:G4 - 16:GS4 - 16:AS4 - 8:C5 - 8:G4 - 16:GS4 - 16:AS4 - 4:REST - 16:GS5 - 16:AS5 - 8:C6 - 8:G5 - 16:GS5 - 16:AS5 - 8:C6 - 16:G5 - 16:GS5 - 16:AS5 - 8:C6 - 8:G5 - 16:GS5 - 16:AS5"
tokyo_drift = "4:AS4 - 4:REST - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:F5 - 4:REST - 4:F5 - 4:REST - 3:GS5 - 3:FS5 - 4:F5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:GS5 - 3:FS5 - 4:F5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST - 3:AS4 - 3:B4 - 4:DS5 - 4:AS4 - 4:REST - 4:AS4 - 4:REST"
pink_panter = "2:REST - 4:REST - 8:REST - 8:DS4 - 4:E4 - 8:REST - 8:FS4 - 4:G4 - 8:REST - 8:DS4 - 8:E4 - 8:FS4 - 8:G4 - 8:C5 - 8:B4 - 8:E4 - 8:G4 - 8:B4 - 2:AS4 - 16:A4 - 16:G4 - 16:E4 - 16:D4 - 2:E4 - 4:REST - 8:REST - 4:DS4 - 4:E4 - 8:REST - 8:FS4 - 4:G4 - 8:REST - 8:DS4 - 8:E4 - 8:FS4 - 8:G4 - 8:C5 - 8:B4 - 8:G4 - 8:B4 - 8:E5 - 1:DS5 - 2:D5 - 4:REST - 8:REST - 8:DS4 - 4:E4 - 8:REST - 8:FS4 - 4:G4 - 8:REST - 8:DS4 - 8:E4 - 8:FS4 - 8:G4 - 8:C5 - 8:B4 - 8:E4 - 8:G4 - 8:B4 - 2:AS4 - 16:A4 - 16:G4 - 16:E4 - 16:D4 - 4:E4 - 4:REST - 4:REST - 8:E5 - 8:D5 - 8:B4 - 8:A4 - 8:G4 - 8:E4 - 16:AS4 - 8:A4 - 16:AS4 - 8:A4 - 16:AS4 - 8:A4 - 16:AS4 - 8:A4 - 16:G4 - 16:E4 - 16:D4 - 16:E4 - 16:E4 - 2:E4"
brigada = "4:G4:4 - 8:A4:8 - 8:A#4:8 - 4:A4:4 - 4:G4:4 - 4:F4:4 - 4:E4:4 - 8:F4:8 - 8:G4:8 - 4:D4:4 - 4:E4:4 - 2:G4:4"

radio_stations = {
    dre: "Doctor DRE",
    mario: "Mario",
    got: "Game Of Thrones",
    tokyo_drift: "Teriyaki Boys",
    pink_panter: "Pink Panter",
    brigada: "Brigada",
}

prev_station_id = None

def set_leds(value: int = 0):
    for led in leds:
        led.value(value)


def blink_all(times: int, delay: float):
    for _ in range(times):
        set_leds(1)
        time.sleep(delay)
        set_leds(0)
        time.sleep(delay)


def get_led_by_note(note: str) -> Pin:
    for i in range(len(note_to_led)):
        if note in note_to_led[i]:
            return leds[i]

    return leds[0]


def turn_led_by_note_name(note: str, val: int):
    get_led_by_note(note).value(val)


def get_radio_station() -> int:
    reading = (
        potentiometer.read_u16()
    )  # Read the potentiometer value and store it in our 'reading' variable

    if reading <= min:
        reading = min + 1
    if reading >= max:
        reading = max - 1

    return int((reading - min) / (max - min) * len(list(radio_stations.keys())))


def volume() -> int:
    # reading = potentiometer.read_u16() # Read the potentiometer value and store it in our 'reading' variable
    reading = 15_000
    return reading


def get_freq_by_note(note: str, oct: str | None) -> int:
    """Get note frequency by its name and octave"""
    if not oct:
        oct = "4"
    return notes[note.replace("#", "S").upper()] * 2 ** (int(oct) - 4)


def playdelay(delay1: float, delay2) -> None:
    """Play delay with two parts"""
    time.sleep(delay1)
    time.sleep(delay2)


def playtone(
    freq: int,
    vol: int,
    delay1: float,
    delay2: float,
    led: Pin | None = None,
) -> None:
    """Play tone with given frequency, volume and delays, optionally light up LED"""
    if led:
        led.value(1)
    buzzer.duty_u16(vol)
    buzzer.freq(freq)
    time.sleep(delay1)
    if led:
        led.value(0)
    buzzer.duty_u16(0)
    time.sleep(delay2)


def kick(vol: int | None = None):
    """Play kick sound effect"""
    kick_vol = vol if vol else volume()
    set_leds(1)
    playtone(160, kick_vol, 0.05, 0)
    playtone(240, kick_vol, 0.05, 0)
    playtone(400, kick_vol, 0.005, 0.01)
    set_leds(0)


def white_noise(duration: float = 0.5):
    """Play white noise sound effect"""
    t = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t) < duration * 1000:
        freq = urandom.getrandbits(12) % 800 + 300  # 3000–8000 Гц
        playtone(freq, volume(), 0.001, 0)


def playnote(
    note: str | None, vol: int, oct: str | None, length: str | None, pause: str | None
) -> None:
    """Play single note (letter!) with given parameters"""
    # print(f"{note=} {vol=} {length=} {pause=}")
    if note:
        # prevent division by zero
        delay_note = 0 if length == "0" else 1 / float(length) if length else 0.05
        pause_after = 0 if pause == "0" else 1 / float(pause) if pause else 0.25
        # handle REST and 'RESTKICK'
        if note == "REST":
            playdelay(delay_note, pause_after)
        elif note == "RESTKICK":
            kick(vol)
        else:
            freq = int(get_freq_by_note(note, oct))
            playtone(freq, vol, delay_note, pause_after, get_led_by_note(note))

def swap_state(blink: int = 1):
    """Swap play/stop state and blink LEDs accordingly"""
    global button_state
    button_state = not button_state
    blink_all(blink if button_state else 2, 0.2)

def stop_playing():
    """Switch playing state to 'False'"""
    if is_playing():
        swap_state()
        print("Stopped playing")


def is_button_pressed() -> bool:
    """Check if any of the buttones pressed to play/stop melody"""
    for button in buttons:
        if button.value() == 1:
            return True
    return False


def has_station_changed() -> bool:
    """Check if the radio station has changed"""
    global prev_station_id
    return get_radio_station() != prev_station_id


def is_playing() -> bool:
    """Check if any of the buttones pressed to play/stop melody"""
    return button_state


def get_note_params(note: str):
    """Parse note string and return its parameters
    For example, 4:AS4:8 returns ('AS', '4', '4', '8')
    """
    # remove spaces
    clean_note = note.strip()
    v = re.match("((\d+):)?([A-z]+)(\d)?(:(\d+))?", clean_note)
    [_, delay1, name, oct, _, delay2] = (
        v.groups() if v else [None, None, None, None, None, None]
    )
    return (name, oct, delay1, delay2)


def playmelody(melody: str):
    """Play melody until stopped or station changed"""
    list_of_notes = melody.split("-")
    for note in list_of_notes:
        if has_station_changed():
            white_noise()
            stop_playing()
            break
        
        if is_button_pressed():
            kick()
            stop_playing()
            break

        if not is_playing():
            break

        (name, oct, delay1, delay2) = get_note_params(note)
        playnote(name, volume(), oct, delay1, delay2)

    # Ensure to stop playing if still in playing state
    stop_playing()


def main():
    set_leds(0)
    onboardLED.value(0)  # LED off by default

    while True:
        time.sleep(0.2)  # Short delay

        # prepare "radio station"
        station_id = get_radio_station()
        if has_station_changed():
            print(
                f"Radio Station: {list(radio_stations.values())[station_id]}"
            )
            global prev_station_id
            if prev_station_id is not None and is_playing():
                white_noise()
                stop_playing()
            prev_station_id = station_id

        # check for play/stop button press
        if is_button_pressed():
            swap_state()

        # update onboard LED status
        onboardLED.value(0 if is_playing() else 1)

        # play melody from the current "radio station"
        if is_playing():
            global prev_station_id
            prev_station_id = station_id
            print("Playing music...")
            playmelody(list(radio_stations.keys())[station_id])


main()
