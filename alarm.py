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

        self.time_display = QtWidgets.QLabel("00:00:00")
        time_font = QtGui.QFont("Helvetica", 36, QtGui.QFont.Bold)
        self.time_display.setFont(time_font)
        self.time_display.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.time_display)

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

        main_layout.addLayout(selector_layout)

        self.add_alarm_button = QtWidgets.QPushButton("Add Alarm")
        self.add_alarm_button.clicked.connect(self.add_alarm)
        main_layout.addWidget(self.add_alarm_button)

        self.alarms_view = QtWidgets.QListWidget()
        main_layout.addWidget(self.alarms_view)

        self.alarms = []
        self.selected_sound = None

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

    def update_clock(self):
        now = datetime.datetime.now().time()
        self.time_display.setText(now.strftime("%H:%M:%S"))

        for alarm in self.alarms:
            if not alarm["triggered"] and now >= alarm["time"]:
                alarm["triggered"] = True
                self.trigger_alarm(alarm)

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