from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt


class StatusMonitor(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_label = QLabel(self)
        self.init()

    def init(self):
        self.status_label.setTextFormat(Qt.RichText)

    def update_status_monitor(self, info: str):
        self.status_label.setText(info)