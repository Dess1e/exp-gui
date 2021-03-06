import sys
import random

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSizePolicy, QPushButton, QTextEdit, QWidget,
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from logger_proxy import LoggerProxy
from main_layout import CustomLayout
from axes_controller import AxesController, AxesTypes
from menubar import MenuBar

Logger = None


class App(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'untitled'
        self.curr_layout = None         # to be initialized in init_ui
        self.controller_layout = None   # ...
        self.menu_bar = None            # ...
        self.logger_proxy = None        # ...
        self.plot_widget = self.init_plot()
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
        self.logger_proxy = LoggerProxy(info_output)
        global Logger
        Logger = self.logger_proxy

        self.curr_layout = self.init_layout(info=info_output, plots=self.plot_widget)
        self.controller_layout = self.curr_layout.controller_layout

        self.show()


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
