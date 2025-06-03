import datetime
from alarm import AlarmClock
from PyQt5 import QtWidgets

# Basic test to ensure the widget initializes and sets alarm times correctly.
def test_alarm_set(qtbot):
    widget = AlarmClock()
    qtbot.addWidget(widget)
    target_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).time()
    widget.time_edit.setTime(target_time)
    widget.set_alarm()
    assert widget.alarm_time.strftime("%H:%M") == target_time.strftime("%H:%M")
