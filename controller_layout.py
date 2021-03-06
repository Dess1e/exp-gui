from PyQt5.QtWidgets import QGridLayout, QComboBox, QPushButton
from axes_controller import AxesTypes


class ControllerLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ax_selector = None         # to be initialized in init()
        self.test_plot_button = None    # ..
        self.clear_plot_button = None   # ..
        self.update_plot_button = None  # ..
        self.init()

    def init(self):
        ax_selector = QComboBox()
        self.ax_selector = ax_selector
        names = AxesTypes.get_names()
        ax_selector.addItems(names)

        self.test_plot_button = QPushButton('Test plot')
        self.clear_plot_button = QPushButton('Test clear data')
        self.update_plot_button = QPushButton('Test update plot')
        self.addWidget(ax_selector, 0, 0)
        self.addWidget(self.test_plot_button, 1, 0)
        self.addWidget(self.clear_plot_button, 1, 1)
        self.addWidget(self.update_plot_button, 2, 0)

    def get_selected_plot(self):
        return self.ax_selector.currentText()
