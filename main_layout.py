from math import sqrt

from PyQt5.QtWidgets import QGridLayout

from controller_layout import ControllerLayout


class CustomLayout(QGridLayout):

    def __init__(self, plots, info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRowStretch(0, 5)
        self.setRowStretch(1, 1)
        self.used_plot_slots = 0
        self.plots_widget = plots
        self.info_widget = info
        self.controller_layout = ControllerLayout()
        self.init_layouts()

    def init_layouts(self):
        self.addWidget(
            self.plots_widget,
            0, 0
        )
        self.addLayout(
            self.controller_layout,
            0, 1
        )
        self.addWidget(
            self.info_widget,
            1, 0
        )
