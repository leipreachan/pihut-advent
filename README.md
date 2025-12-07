# Raspberry Pi Pico - 12 days of hacking / coding

https://thepihut.com/advent

## Day 1 - OnBoard LED

- Blink with onboard LED

[Code: day1.py](day1.py)

## Day 2 - Color LEDs

- Traffic light sequence (Red, Amber, Green LEDs)

[Code: day2.py](day2.py)

## Day 3 - Buttons

- Print ID of the pressed button

[Code: day3.py](day3.py)

## Day 4 - Potentiometer

- Read value from potentiometer
- Print the value
- Depending on the value, turn on either red, or amber, or green light

[Code: day4.py](day4.py)

### Traffic Lights

- Turn on red, amber, green lights one by one
- Read value from potentiometer
- Depending on the value, speed up or slow down the sequence

[Code: day4-glow.py](day4-glow.py)

### 'Brightness'

- Depending on the value from potentiometer, change brightness of the green LED

[Code: day4-pwm.py](day4-pwm.py)

## Day 5 - Buzzer

- Play "Jingle Bells"

[Code: day5.py](day5.py)

### Radio with several stations

- Click any button to play/stop
- Use potentiometer to change radio
- Onboard LED displays the running state of the project
- Color LEDs show different notes played
- Color LEDs blink when a button is pressed
- "Pshhht" sound when "radio station" is changed

[Code: day5-with-button-radio.py](day5-with-button-radio.py)
    
[![docs/day5-radio.fzz](docs/day5-radio_bb.svg)](docs/day5-radio.fzz)

## Day 6 - Light sensor

- Read light sensor value
- Depending on the value, turn on either red, or amber, or green LED

[Code: day6.py](day6.py)

## Day 7 - Proximity Sensor

- Warm up PIR (Passive Infra-Red Sensor)
- If proximity sensor sends a signal, turn on alarm (1 cycle)

[Code: day7.py](day7.py)

### Project: Alarm (Proximity Sensor) with security code

- Wait for PIR to get ready
- Click any button to set the alarm, wait for 3 seconds and play "start" jingle
- If the motion is detected, play alarm sound
- While playing alarm sound allow user to enter code using sequence of the buttons
- If code is correct, play "stop" jingle and de-activate alarm
- If code is wrong or more than 5 seconds passed since first button press, play "wrong code" jingle
- If alarm is de-activated, user can press any button to set alarm again
- Minor change in schematics comparing to day 5 (the potentiometer central pin is in a different place)

[Code: day7-alaram-with-volume-and-code.py](day7-alaram-with-volume-and-code.py)

[![docs/day7-alarm-with-buttons.fzz](docs/day7-alarm-with-buttons_bb.svg)](docs/day7-alarm-with-buttons.fzz)