import sys
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia

class AlarmClock(QtWidgets.QWidget):
    """Simple multi-alarm clock with iPhone like look."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alarm")
        self.resize(320, 480)
        self.setStyleSheet("background-color: black; color: white;")

        main_layout = QtWidgets.QVBoxLayout(self)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(
            "QTabBar::tab {background: #444; color: white;}"
            "QTabBar::tab:selected {background: black; color: white;}"
        )
        main_layout.addWidget(self.tabs)

        self.alarm_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.alarm_tab, "Alarm")
        alarm_layout = QtWidgets.QVBoxLayout(self.alarm_tab)

        self.time_display = QtWidgets.QLabel("00:00:00")
        time_font = QtGui.QFont("Helvetica", 36, QtGui.QFont.Bold)
        self.time_display.setFont(time_font)
        self.time_display.setAlignment(QtCore.Qt.AlignCenter)
        alarm_layout.addWidget(self.time_display)

        # Wheel style time selector
        selector_layout = QtWidgets.QHBoxLayout()
        self.time_edit = QtWidgets.QTimeEdit(datetime.datetime.now().time())
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setFont(QtGui.QFont("Helvetica", 24))
        self.time_edit.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        selector_layout.addWidget(self.time_edit)

        self.choose_sound = QtWidgets.QPushButton("Music…")
        self.choose_sound.clicked.connect(self.pick_sound)
        selector_layout.addWidget(self.choose_sound)

        alarm_layout.addLayout(selector_layout)

        self.add_alarm_button = QtWidgets.QPushButton("Add Alarm")
        self.add_alarm_button.clicked.connect(self.add_alarm)
        alarm_layout.addWidget(self.add_alarm_button)

        self.alarms_view = QtWidgets.QListWidget()
        alarm_layout.addWidget(self.alarms_view)

        # Timer tab
        self.timer_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.timer_tab, "Timer")
        timer_layout = QtWidgets.QVBoxLayout(self.timer_tab)

        timer_selector = QtWidgets.QHBoxLayout()
        self.timer_edit = QtWidgets.QTimeEdit(QtCore.QTime(0, 1, 0))
        self.timer_edit.setDisplayFormat("HH:mm:ss")
        self.timer_edit.setFont(QtGui.QFont("Helvetica", 24))
        self.timer_edit.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        timer_selector.addWidget(self.timer_edit)

        self.add_timer_button = QtWidgets.QPushButton("Add Timer")
        self.add_timer_button.clicked.connect(self.add_timer)
        timer_selector.addWidget(self.add_timer_button)

        timer_layout.addLayout(timer_selector)

        self.timers_view = QtWidgets.QListWidget()
        timer_layout.addWidget(self.timers_view)

        self.alarms = []
        self.selected_sound = None

        self.timers = []

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

    def pick_sound(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Alarm Sound", "", "Audio Files (*.wav *.mp3)")
        if path:
            self.selected_sound = path
            self.choose_sound.setText(QtCore.QFileInfo(path).fileName())

    def add_alarm(self):
        alarm_time = self.time_edit.time().toPyTime()
        sound = self.selected_sound
        self.alarms.append({"time": alarm_time, "sound": sound, "triggered": False})
        display = alarm_time.strftime("%H:%M")
        if sound:
            display += f" - {QtCore.QFileInfo(sound).fileName()}"
        self.alarms_view.addItem(display)

    def add_timer(self):
        t = self.timer_edit.time()
        remaining = t.hour() * 3600 + t.minute() * 60 + t.second()
        if remaining == 0:
            return
        self.timers.append(remaining)
        h = remaining // 3600
        m = (remaining % 3600) // 60
        s = remaining % 60
        self.timers_view.addItem(f"{h:02d}:{m:02d}:{s:02d}")

    def update_clock(self):
        now = datetime.datetime.now().time()
        self.time_display.setText(now.strftime("%H:%M:%S"))

        for alarm in self.alarms:
            if not alarm["triggered"] and now >= alarm["time"]:
                alarm["triggered"] = True
                self.trigger_alarm(alarm)

        for i in reversed(range(len(self.timers))):
            self.timers[i] -= 1
            if self.timers[i] <= 0:
                self.timers.pop(i)
                self.timers_view.takeItem(i)
                QtWidgets.QMessageBox.information(self, "Timer", "Time's up!")
            else:
                remaining = self.timers[i]
                h = remaining // 3600
                m = (remaining % 3600) // 60
                s = remaining % 60
                self.timers_view.item(i).setText(f"{h:02d}:{m:02d}:{s:02d}")

    def trigger_alarm(self, alarm):
        animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(1000)
        animation.setStartValue(1.0)
        animation.setKeyValueAt(0.5, 0.0)
        animation.setEndValue(1.0)
        animation.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

        if alarm.get("sound"):
            url = QtCore.QUrl.fromLocalFile(alarm["sound"])
            content = QtMultimedia.QMediaContent(url)
            player = QtMultimedia.QMediaPlayer()
            player.setMedia(content)
            player.play()
        QtWidgets.QMessageBox.information(self, "Alarm", "Wake up!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = AlarmClock()
    w.show()
    sys.exit(app.exec_())