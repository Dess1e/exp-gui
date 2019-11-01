from enum import Enum

from matplotlib.figure import Figure, Axes
from matplotlib.lines import Line2D


class AxesTypes(Enum):

    ALL = 0
    TBD1 = 'Plot 1 name'
    TBD2 = 'Plot 2 name'
    TBD3 = 'Plot 3 name'
    TBD4 = 'Plot 4 name'

    @staticmethod
    def get_names():
        return [AxesTypes[x].name for x in AxesTypes.__members__]

    @staticmethod
    def get_entries_to_skip():
        return AxesTypes.ALL,

    @staticmethod
    def get_entries():
        return (e for e in AxesTypes if e not in AxesTypes.get_entries_to_skip())


class AxesController:
    def __init__(self, figure: Figure):
        self.axes_map = {}
        self.data_map = {k: [] for k in AxesTypes}
        for indx, tp in enumerate(AxesTypes.get_entries(), 1):
            ax: Axes = figure.add_subplot(220 + indx)
            ax.set_title(tp.value)
            self.axes_map[tp] = ax

    def _plot_wrapper(self, data_x, data_y, type):
        ax = self.axes_map[type]
        line, = ax.plot(data_x, data_y, '.')
        self.data_map[type].append(line)

    def _clear_wrapper(self, type):
        plots = self.data_map[type]
        for plot in plots:
            plot.remove()
        self.data_map[type] = []

    def _update_wrapper(self, data_x, data_y, type):
        lst = self.data_map[type]
        if not len(lst):
            # TODO: log this event
            return
        line = lst[-1]
        line.set_xdata(data_x)
        line.set_ydata(data_y)

    def plot_data(self, data_x, data_y, axes_type):
        if axes_type == AxesTypes.ALL:
            for tp in AxesTypes.get_entries():
                self._plot_wrapper(data_x, data_y, tp)
        else:
            self._plot_wrapper(data_x, data_y, axes_type)

    def clear(self, axes_type):
        if axes_type == AxesTypes.ALL:
            for tp in AxesTypes.get_entries():
                self._clear_wrapper(tp)
        else:
            self._clear_wrapper(axes_type)

    def update_plot(self, data_x, data_y, axes_type):
        if axes_type == AxesTypes.ALL:
            for tp in AxesTypes.get_entries():
                self._update_wrapper(data_x, data_y, tp)
        else:
            self._update_wrapper(data_x, data_y, axes_type)
