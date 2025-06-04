import datetime
import pytest

try:
    from alarm import AlarmClock
except Exception as e:  # pragma: no cover - skip if dependencies missing
    pytest.skip(f"AlarmClock cannot be imported: {e}", allow_module_level=True)


def test_add_alarm(qtbot):
    """Ensure alarms can be added to the list."""
    widget = AlarmClock()
    qtbot.addWidget(widget)
    target_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).time()
    widget.time_edit.setTime(target_time)
    widget.add_alarm()
    assert len(widget.alarms) == 1
    assert widget.alarms[0]["time"].strftime("%H:%M") == target_time.strftime("%H:%M")

