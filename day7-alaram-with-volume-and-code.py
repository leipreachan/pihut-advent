# PIR sensor with alarm, volume control via potentiometer, and LED indicators
# Press any button to START the alarm
# Press buttons in the correct sequence to STOP the alarm

from machine import Pin, PWM, ADC
import time

CODE_MAX_LENGTH = 10
DEACTIVATION_CODE = [1, 2, 0]

onboardLED = Pin(25, Pin.OUT)
potentiometer = ADC(Pin(27))

leds = [Pin(20, Pin.OUT), Pin(19, Pin.OUT), Pin(18, Pin.OUT)]

# Set up the Buzzer pin as PWM
buzzer = PWM(Pin(13))

# Set PWM duty to 0% at program start
buzzer.duty_u16(0)

# Set up PIR pin with pull down
pir = Pin(26, Pin.IN, Pin.PULL_DOWN)

onboardLED.value(1)  # Turn onboard LED ON to show program is running

buttons = [
    Pin(12, Pin.IN, Pin.PULL_DOWN),
    Pin(8, Pin.IN, Pin.PULL_DOWN),
    Pin(3, Pin.IN, Pin.PULL_DOWN),
]

jingles = {
    "start": [(523, 0.12), (659, 0.12), (784, 0.20)],
    "stop": [(784, 0.12), (659, 0.12), (523, 0.20)],
    "bad_code": [(900, 0.08), (700, 0.08), (500, 0.12)],
}

alarm_active = False


def is_button_pressed() -> bool:
    """Check if any of the buttones pressed to play/stop melody"""
    for button in buttons:
        if button.value() == 1:
            return True
    return False


def read_button_code() -> int:
    """Read which button is pressed and return its index"""
    for index, button in enumerate(buttons):
        if button.value() == 1:
            print(f"Button {index} pressed")
            # Wait for button release
            while button.value() == 1:
                time.sleep(0.1)
            return index
    return -1


def verify_code(max_code_enter_time: int = 5) -> bool:
    """Verify if the entered code matches the deactivation code"""
    entered_code = []
    start = time.time()
    print("Enter deactivation code:")
    for _ in range(CODE_MAX_LENGTH):
        while not is_button_pressed():
            time.sleep(0.1)
            if time.time() > start + max_code_enter_time:
                return False
        
        button_index = read_button_code()
        entered_code.append(button_index)
        if entered_code == DEACTIVATION_CODE:
            print(f"Entered code: {entered_code}")
            return True
        

    return entered_code == DEACTIVATION_CODE


def play_track(track):
    set_volume()
    for freq, delay in track:
        buzzer.freq(freq)  # Higher pitch
        time.sleep(delay)
    set_volume(0)

def is_alarm_active() -> bool:
    return alarm_active

def enable_alarm():
    play_track(jingles["start"])

    global alarm_active
    alarm_active = True


def disable_alarm():
    play_track(jingles["stop"])
    global alarm_active
    alarm_active = False


def check_code() -> bool:
    if is_button_pressed():
        if verify_code():
            print("Entered correct code. Alarm deactivated.")
            return True
        else:
            print("Wrong code")
            play_track(jingles["bad_code"])
    return False


def set_leds(value: int):
    for led in leds:
        led.value(value)


def set_volume(vol: int | None = None):
    volume = potentiometer.read_u16()
    buzzer.duty_u16(vol if vol is not None else volume)


def alarm(repeat: int = 3) -> bool:  # Our alarm function
    result = False
    # Set PWM duty (volume up)
    for _ in range(repeat):  # Run this 3 times
        # Read potentiometer value for volume control
        set_volume()

        buzzer.freq(1000)  # Higher pitch
        set_leds(1)
        time.sleep(0.5)
        if result := check_code():
            break

        buzzer.freq(500)  # Lower pitch
        set_leds(0)
        time.sleep(0.5)
        if result := check_code():
            break

    # turn off leds
    set_leds(0)
    # Set PWM duty (volume off)
    set_volume(0)
    return result


def set_alarm():
    print("Activate alarm by pressing any button")
    while True:  # Run forever
        time.sleep(0.01)  # Delay to stop unnecessary program speed

        if not is_alarm_active() and is_button_pressed():
            delay = 3
            print(f"Alarm will be activated in {delay} seconds...")
            time.sleep(delay)  # Delay to avoid immediate activation
            enable_alarm()
            print("... Alarm is now active!")
            continue

        if is_alarm_active() and pir.value() == 1:  # If PIR detects movement
            print("I SEE YOU!")

            if alarm(10):  # Call our function
                print("Press any button to activate the alarm")
                disable_alarm()
                continue

            print("Sensor active")  # Let us know that the sensor is active again


def warm_up_pir(delay: int = 5):
    # Warm up/settle PIR sensor
    print("Warming up...")
    time.sleep(delay)  # Delay to allow the sensor to settle
    print("Sensor ready!")


def main():
    warm_up_pir()
    set_alarm()


main()
