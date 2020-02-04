import sys
import random

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSizePolicy, QPushButton, QTextEdit, QWidget,
)
from PyQt5.QtGui import QTextOption

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from configuration_manager import ConfigurationManager
from logger import Logger
from main_layout import CustomLayout
from axes_controller import AxesController, AxesTypes
from menubar import MenuBar
from serial_reader import SerialReaderThread
from data_controller import DataController


class App(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'untitled'
        self.readers_initialized = True
        self.curr_layout = None         # to be initialized in init_ui
        self.controller_layout = None   # ...
        self.menu_bar = None            # ...
        self.logger_proxy = None        # ...
        self.serial_readers = {}        # ...
        self.plot_widget = self.init_plot()
        self.data_controller = DataController(self)
        self.config_manager = ConfigurationManager()
        self.init()
        self.init_signals()

    def init_signals(self):
        def test_plot():
            selected = self.controller_layout.get_selected_plot()
            e = AxesTypes[selected]
            self.plot_widget.plot(
                [random.random() for _ in range(10)],
                [random.random() for _ in range(10)],
                e
            )
            self.logger_proxy.log('Clicked test plot for plot {}'.format(e.name))

        def test_clear():
            selected = self.controller_layout.get_selected_plot()
            e = AxesTypes[selected]
            self.plot_widget.clear(e)
            self.logger_proxy.log('Clicked clear plot for plot {}'.format(e.name))

        def test_update():
            selected = self.controller_layout.get_selected_plot()
            e = AxesTypes[selected]
            self.plot_widget.update_plot(
                [random.random() for x in range(5)],
                [random.random() for x in range(5)],
                e
            )

        self.controller_layout.test_plot_button.pressed.connect(test_plot)
        self.controller_layout.clear_plot_button.pressed.connect(test_clear)
        self.controller_layout.update_plot_button.pressed.connect(test_update)
        self.controller_layout.start_reader_button.pressed.connect(self.create_reader_thread)

        self.menu_bar.action_save.triggered.connect(self.data_controller.save_data)
        self.menu_bar.action_clear_buffer.triggered.connect(lambda: Logger.clear_buffer())
        self.menu_bar.action_connect.triggered.connect(self.start_reading)
        self.menu_bar.action_close.triggered.connect(self.close)
        self.menu_bar.action_disconnect.triggered.connect(self.stop_reading)
        self.menu_bar.action_pause_reading.triggered.connect(self.pause_reading)
        self.menu_bar.action_create.triggered.connect(lambda: self.config_manager.show())

        self.controller_layout.serial_connector.ready_to_start_reading_signal.connect(self.found_serial)

    def init_readers(self):
        for tp in AxesTypes.get_entries():
            self.serial_readers[tp] = SerialReaderThread(tp)
            self.serial_readers[tp].got_data_signal.connect(self.process_read_data)

    def found_serial(self, ax_type, path):
        if ax_type == AxesTypes.ALL:
            Logger.log('All devices were found')
            self.menu_bar.action_connect.setEnabled(True)
        else:
            Logger.log('Found device at %s' % path)
            self.serial_readers[ax_type].set_read_path(path)

    def start_reading(self):
        if ...:
            return
        if not self.readers_initialized:
            self.init_readers()
        for reader in self.serial_readers.values():
            #TODO: Test
            if reader.ax_type == AxesTypes.VAC:
                continue
            #endtest
            reader.start()
        self.menu_bar.action_disconnect.setEnabled(True)
        self.menu_bar.action_connect.setEnabled(False)

    def pause_reading(self):
        Logger.warn('Tasking all reader threads to pause')
        for reader in self.serial_readers.values():
            reader.requestInterruption()

    def stop_reading(self):
        for reader in self.serial_readers.values():
            reader.terminate()
        self.menu_bar.action_disconnect.setEnabled(False)
        self.menu_bar.action_connect.setEnabled(True)

    def close(self):
        self.readers_initialized = False
        self.serial_readers = {}
        self.plot_widget.clear(AxesTypes.ALL)

    def create_reader_thread(self):
        selected = self.controller_layout.get_selected_plot()
        tp = AxesTypes[selected]
        self.serial_readers[tp].start()

    def init_layout(self, info, plots):
        w = QWidget()
        layout = CustomLayout(info=info, plots=plots)
        w.setLayout(layout)
        self.setCentralWidget(w)
        return layout

    def init_plot(self):
        return PlotCanvas(self)

    def init(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 1024, 768)

        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)

        info_output = QTextEdit(self)
        info_output.setReadOnly(True)
        info_output.setWordWrapMode(QTextOption.WrapAnywhere)
        self.logger_proxy = Logger(lambda text: info_output.setHtml(text))

        self.curr_layout = self.init_layout(info=info_output, plots=self.plot_widget)
        self.controller_layout = self.curr_layout.controller_layout

        self.init_readers()
        self.show()

    def process_read_data(self, x_data, y_data, aux_data, ax_type):
        if ax_type == AxesTypes.LAC:
            self.plot_widget.try_plot(x_data, y_data, AxesTypes.LAC)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(hspace=0.25)
        super().__init__(fig)
        self.axes_controller = AxesController(fig)

        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.draw()

    def plot(self, data_x, data_y, axes_type):
        self.axes_controller.plot_data(data_x, data_y, axes_type)
        self.draw()

    def clear(self, axes_type):
        self.axes_controller.clear(axes_type)
        self.draw()

    def update_plot(self, data_x, data_y, axes_types):
        self.axes_controller.update_plot(data_x, data_y, axes_types)
        self.draw()

    def handle_new_data(self, data, ax_type):
        self.try_plot(data, data, ax_type)

    def try_plot(self, data_x, data_y, ax_type):
        self.axes_controller.try_plot(data_x, data_y, ax_type)
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
