
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QPushButton, QVBoxLayout, QWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import random


class App(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'untitled'
        self.init_layout()
        self.init_ui()

    def init_layout(self):
        w = QWidget()
        w.

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 640, 480)

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('Example button')
        button.resize(140, 100)

        self.layout().addItem(
            PlotCanvas(self, width=5, height=4)
        )

        self.show()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        super().__init__(fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [random.random() for _ in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, '*')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())