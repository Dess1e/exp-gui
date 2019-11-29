from time import time, sleep
from functools import partial

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel

from utils import serial_like_data_generator, find_device_path
from axes_controller import AxesTypes


class SerialConnector(QWidget):
    ready_to_start_reading_signal = pyqtSignal(AxesTypes, str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.searcher_thread = SerialSearcher()
        self.found = {ax_type: False for ax_type in SerialSearcher.SERIAL_LOOKUP_PATH.keys()}
        self.info = QLabel(self)
        self.init()

    def init(self):
        self.searcher_thread.found_serial_signal.connect(self.found_serial)
        self.update_info()
        self.searcher_thread.start()

    def update_info(self):
        bool_to_str = lambda b: 'available' if b is True else 'not available'
        info = ['{} reader: {}'.format(ax_type.value, bool_to_str(found)) for ax_type, found in self.found.items()]
        full_info = '\n'.join(info)
        self.info.setText(full_info)

    def found_serial(self, ax_type: AxesTypes, path: str):
        if ax_type == AxesTypes.ALL:
            self.ready_to_start_reading_signal.emit(ax_type, '')
        else:
            self.found[ax_type] = True
            self.ready_to_start_reading_signal.emit(ax_type, path)
        self.update_info()


class SerialReaderThread(QThread):
    got_data_signal = pyqtSignal(list, list, AxesTypes)

    def __init__(self, ax_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x_data = []
        self.y_data = []
        self.ax_type = ax_type
        self.device_path = None

    def set_read_path(self, path):
        self.device_path = path

    def run(self) -> None:
        t = time()
        while True:
            if self.isInterruptionRequested():
                sleep(0.5)
                continue
            x_data = serial_like_data_generator()
            y_data = serial_like_data_generator()
            self.x_data += x_data
            self.y_data += y_data
            if time() - t > 0.5:
                self.got_data_signal.emit(self.x_data, self.y_data, self.ax_type)
                t = time()


class SerialSearcher(QThread):
    found_serial_signal = pyqtSignal(AxesTypes, str)
    SERIAL_LOOKUP_PATH = {
        # TODO: testing
        # AxesTypes.VAC: partial(find_device_path, 'STMicroelectronics'),
        AxesTypes.LAC: partial(find_device_path, 'Arduino'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.found = {k: False for k in AxesTypes.get_entries()}
        # TODO: testing
        self.found.pop(AxesTypes.VAC)

    def is_all_found(self):
        return all(self.found.values())

    def run(self) -> None:
        while True:
            sleep(0.5)
            if self.is_all_found():
                self.found_serial_signal.emit(AxesTypes.ALL, '')
                self.terminate()
            for tp, finder in self.SERIAL_LOOKUP_PATH.items():
                if self.found[tp] is True:
                    continue
                path = finder()
                if path is None:
                    continue
                else:
                    self.found[tp] = True
                    self.found_serial_signal.emit(tp, path)
