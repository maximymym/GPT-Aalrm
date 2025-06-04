# GPT-Aalrm

A minimal alarm clock application for Windows inspired by the look of the iPhone clock.

## Features
- Simple black theme with large digital clock
- Toggle switch to enable or disable each alarm
- Styled buttons and iPhone-like fonts

If you see a `libpulse-mainloop-glib.so.0` error, your system is missing the
Qt multimedia libraries required by PyQt.
- Wheel style time selector
- Multiple alarms with optional custom music
- Small fade animation when an alarm goes off
=======
- Set a daily alarm
- Small fade animation when the alarm goes off


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
