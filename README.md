## Breadboard Layout (Fritzing)

### Day 5 - Radio with several stations

- Click any button to play/stop
- Use potentiometer to change radio
- Onboard LED displays the running state of the project
- Color LEDs show different notes played
- Color LEDs blink when a button is pressed
- "Pshhht" sound when "radio station" is changed
- [Code: day5-with-button-radio.py](day5-with-button-radio.py)
- [Fzz file](docs/day5-radio.fzz)

![Schematics for 'radio'](docs/day5-radio_bb.svg) 


### Day 7 - Alarm (Proximity Sensor) with code

- Wait for PIR to get ready
- Click any button to set the alarm, wait for 3 seconds and play "start" jingle
- If the motion is detected, play alarm sound
- While playing alarm sound allow user to enter code using sequence of the buttons
- If code is correct, play "stop" jingle and de-activate alarm
- If code is wrong or more than 5 seconds passed since first button press, play "wrong code" jingle
- If alarm is de-activated, user can press any button to set alarm again
- Minor change in schematics comparing to day 5 (the potentiometer central pin is in a different place)
- [Code: day7-alaram-with-volume-and-code.py](day7-alaram-with-volume-and-code.py)
- [Fzz file](docs/day7-alarm-with-buttons.fzz)
![Day 7](docs/day7-alarm-with-buttons_bb.svg)