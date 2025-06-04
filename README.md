# GPT-Aalrm

A minimal alarm clock application for Windows inspired by the look of the iPhone clock.

## Features
- Simple black theme with large digital clock
- Wheel style time selector
- Multiple alarms with optional custom music
- Small fade animation when an alarm goes off
- Multiple countdown timers

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

## Building a Windows executable
To create a standalone `exe` you can use [PyInstaller](https://www.pyinstaller.org/) on a
Windows machine:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed alarm.py
```

The resulting executable will be placed in the `dist` folder. Building a Windows
binary from Linux is not officially supported, so perform these steps on
a Windows system.

## Pixel Runner Game
A simple platformer with a short storyline. Use the arrow keys to move and
press Space to jump. Reach the blue crystal to advance through the two short
levels.

Run it with:
```bash
python pixel_runner.py
```
