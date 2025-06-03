import sys
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

class AlarmClock(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alarm")
        self.resize(300, 150)
        self.setStyleSheet("background-color: black; color: white;")

        layout = QtWidgets.QVBoxLayout(self)
        self.time_display = QtWidgets.QLabel("00:00:00")
        font = QtGui.QFont("Helvetica", 36, QtGui.QFont.Bold)
        self.time_display.setFont(font)
        self.time_display.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.time_display)

        self.time_edit = QtWidgets.QTimeEdit(datetime.datetime.now().time())
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setFont(QtGui.QFont("Helvetica", 20))
        layout.addWidget(self.time_edit)

        self.set_alarm_button = QtWidgets.QPushButton("Set Alarm")
        layout.addWidget(self.set_alarm_button)
        self.set_alarm_button.clicked.connect(self.set_alarm)

        self.alarm_time = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

    def update_clock(self):
        now = datetime.datetime.now().time()
        self.time_display.setText(now.strftime("%H:%M:%S"))
        if self.alarm_time and now >= self.alarm_time:
            self.trigger_alarm()

    def set_alarm(self):
        self.alarm_time = self.time_edit.time().toPyTime()
        self.set_alarm_button.setText("Alarm Set: " + self.alarm_time.strftime("%H:%M"))

    def trigger_alarm(self):
        self.alarm_time = None
        self.set_alarm_button.setText("Set Alarm")
        animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(1000)
        animation.setStartValue(1.0)
        animation.setKeyValueAt(0.5, 0.0)
        animation.setEndValue(1.0)
        animation.start(QtCore.QAbstractAnimation.DeleteWhenStopped)
        QtWidgets.QMessageBox.information(self, "Alarm", "Wake up!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = AlarmClock()
    w.show()
    sys.exit(app.exec_())
