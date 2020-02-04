from PyQt5.QtWidgets import QWidget, QVBoxLayout


class ConfigurationManager(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setFixedWidth(200)
        self.setFixedHeight(200)
        # init layout
        # init all buttons and place them on layout
        ...

    def save_config(self):
        ...

    def load_config(self):
        ...