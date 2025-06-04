# GPT-Aalrm

A minimal alarm clock application for Windows inspired by the look of the iPhone clock.

## Features
- Simple black theme with large digital clock
- Wheel style time selector
- Multiple alarms with optional custom music
- Toggle switch to enable or disable each alarm
- Styled buttons and iPhone-like fonts
- Small fade animation when an alarm goes off

## Usage
Install requirements first:
```bash
pip install -r requirements.txt
```
Then run the app:
```bash
python alarm.py
```

## Testing
Run the tests with:
```bash
pytest -v
```
If you see a `libpulse-mainloop-glib.so.0` error, your system is missing the
Qt multimedia libraries required by PyQt.