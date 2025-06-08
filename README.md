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
Then run the PyQt demo app:
```bash
python alarm.py
```

### Flet alarm manager
An alternative implementation built with [Flet](https://flet.dev) and SQLite is
provided in `flet_alarm.py`.

Run it with:
```bash
python flet_alarm.py
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
A minimal pixel platformer built with Pygame.

Run it with:
```bash
python pixel_runner.py
```
