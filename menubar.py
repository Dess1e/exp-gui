from PyQt5.QtWidgets import QMenuBar


class MenuBar(QMenuBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action_save = None
        self.action_load = None
        self.action_close = None
        self.action_quit = None
        self.action_connect = None
        self.action_disconnect = None
        self.init()

    def init(self):
        file_menu = self.addMenu('File')
        self.action_save = file_menu.addAction('Save')
        self.action_load = file_menu.addAction('Load')
        self.action_close = file_menu.addAction('Close')
        self.action_quit = file_menu.addAction('Quit')

        serial_menu = self.addMenu('Serial')
        self.action_connect = serial_menu.addAction('Connect')
        self.action_disconnect = serial_menu.addAction('Disconnect')
