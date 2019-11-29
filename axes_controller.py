from enum import Enum

from matplotlib.figure import Figure, Axes
from matplotlib.lines import Line2D


class AxesTypes(Enum):

    ALL = 0
    VAC = 'VAC'  # 'Volt-Ampere Characteristic'
    LAC = 'LAC'  # 'Lumen-Ampere Characteristic'

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
            ax.autoscale(enable=True, tight=True)
            ax.set_title(tp.value)
            self.axes_map[tp] = ax

    def _plot_wrapper(self, data_x, data_y, type):
        ax = self.axes_map[type]
        line, *rest = ax.plot(data_x, data_y, '.')
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
        ax = self.axes_map[type]
        ax.autoscale_view()

    def plot_data(self, data_x, data_y, axes_type):
        if axes_type == AxesTypes.ALL:
            for tp in AxesTypes.get_entries():
                self._plot_wrapper(data_x, data_y, tp)
        else:
            self._plot_wrapper(data_x, data_y, axes_type)

    def try_plot(self, data_x, data_y, ax_type):
        if len(self.data_map[ax_type]):
            self._update_wrapper(data_x, data_y, ax_type)
        else:
            self._plot_wrapper(data_x, data_y, ax_type)

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
