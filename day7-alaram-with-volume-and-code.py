# PIR sensor with alarm, volume control via potentiometer, and LED indicators
# Press any button to START the alarm
# Press buttons in the correct sequence to STOP the alarm

from machine import Pin, PWM, ADC
import time

DEACTIVATION_CODE = [1, 2, 0]

onboardLED = Pin(25, Pin.OUT)
potentiometer = ADC(Pin(27))

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

onboardLED.value(1)  # Turn onboard LED ON to show program is running

buttons = [
    Pin(12, Pin.IN, Pin.PULL_DOWN),
    Pin(8, Pin.IN, Pin.PULL_DOWN),
    Pin(3, Pin.IN, Pin.PULL_DOWN),
]

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


def verify_code() -> bool:
    """Verify if the entered code matches the deactivation code"""
    entered_code = []
    print("Enter deactivation code:")
    for _ in range(len(DEACTIVATION_CODE)):
        while not is_button_pressed():
            time.sleep(0.1)
        button_index = read_button_code()
        entered_code.append(button_index)

    print(f"Entered code: {entered_code}")
    return entered_code == DEACTIVATION_CODE


def is_alarm_active() -> bool:
    return alarm_active


def enable_alarm():
    global alarm_active
    alarm_active = True


def disable_alarm():
    global alarm_active
    alarm_active = False


def alarm(repeat: int = 3) -> bool:  # Our alarm function
    result = False
    # Set PWM duty (volume up)
    for _ in range(repeat):  # Run this 3 times
        # Read potentiometer value for volume control
        volume = potentiometer.read_u16()
        buzzer.duty_u16(volume)

        buzzer.freq(1000)  # Higher pitch

        red.value(1)  # Red ON
        amber.value(1)  # Amber ON
        green.value(1)  # Green ON

        time.sleep(0.5)

        buzzer.freq(500)  # Lower pitch

        red.value(0)  # Red OFF
        amber.value(0)  # Amber OFF
        green.value(0)  # Green OFF

        time.sleep(0.5)
        if is_button_pressed() and verify_code():
            print("Entered correct code. Alarm deactivated.")
            result = True
            break

    # Set PWM duty (volume off)
    buzzer.duty_u16(0)
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
