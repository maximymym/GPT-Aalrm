import datetime
from alarm import AlarmClock


def test_add_alarm(qtbot):
    """Ensure alarms can be added to the list."""
    widget = AlarmClock()
    qtbot.addWidget(widget)
    target_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).time()
    widget.time_edit.setTime(target_time)
    widget.add_alarm()
    assert len(widget.alarms) == 1
    alarm = widget.alarms[0]
    assert alarm["time"].strftime("%H:%M") == target_time.strftime("%H:%M")
    assert alarm["enabled"] is True
