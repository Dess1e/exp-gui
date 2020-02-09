from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtCore import pyqtSignal
from logger import Logger


class MenuBar(QMenuBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action_save = None
        self.action_load = None
        self.action_close = None
        self.action_quit = None
        self.action_connect = None
        self.action_disconnect = None
        self.action_clear_buffer = None
        self.action_pause_reading = None
        self.action_create = None
        self.action_calibrate_temp = None
        self.action_calibrate_curr = None
        self.init()

    def init(self):
        file_menu = self.addMenu('File')
        self.action_load = file_menu.addAction('Load configuration')
        self.action_save = file_menu.addAction('Save configuration')
        self.action_create = file_menu.addAction('Create configuration')
        self.action_close = file_menu.addAction('Close')
        self.action_quit = file_menu.addAction('Quit')
        self.action_clear_buffer = file_menu.addAction('Clear logging window')

        serial_menu = self.addMenu('Serial')
        self.action_connect = serial_menu.addAction('Connect')
        self.action_disconnect = serial_menu.addAction('Disconnect')
        self.action_connect.setEnabled(False)
        self.action_disconnect.setEnabled(False)

        exp_menu = self.addMenu('Experimental')
        self.action_pause_reading = exp_menu.addAction('Pause connection')
        self.action_pause_reading.setEnabled(False)

        calibrate = self.addMenu('Calibrate')
        self.action_calibrate_temp = calibrate.addAction('Cal. temperature')
        self.action_calibrate_temp.setEnabled(False)
        self.action_calibrate_curr = calibrate.addAction('Cal. current')
        self.action_calibrate_curr.setEnabled(False)