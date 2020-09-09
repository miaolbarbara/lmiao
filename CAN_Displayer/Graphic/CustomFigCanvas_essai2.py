from datetime import datetime

import matplotlib as mpl
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
import matplotlib.animation as animation
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker
import gc


class DemoFigureCanvas_essai(FigureCanvas):
    flag_get_DBC = 0

    def __init__(self, figure) -> None:
        self.figure = figure
        self.canvas = FigureCanvas(self.figure)
        super().__init__(self.figure)
        # initialise empty dictionaries for different objects in figure
        self.ax = {}
        self.line = {}
        self.y_ticks_value = {}
        self.index = 1
        self.index = 1

    def set_xaxis_format(self, axe):
        # set axis format as 'hour:min:sec'.
        axe.xaxis_date()
        dateFormat = DateFormatter('%H:%M:%S')
        axe.xaxis.set_major_formatter(ticker.FuncFormatter(dateFormat))
        axe.tick_params(labelrotation=0)

    def creat_lines(self, SignalName, color, length):
        if self.index <= length:
            self.ax[SignalName] = self.figure.add_subplot(length, 1, self.index)
            self.line[SignalName], = self.ax[SignalName].plot([], [], label=SignalName, color=color)
            self.line[SignalName].set_data([], [])
            self.y_ticks_value[SignalName] = []
            self.set_xaxis_format(self.ax[SignalName])
            self.index = self.index + 1

    def init(self, SignalName):
        '''
        :param SignalName
        :return: return a line2D object
                to be noticed: don't forget , at the end
        '''
        self.line[SignalName].set_data([], [])
        return self.line[SignalName],

    def animate_data(self, data_time, data_value, data_time_min=None, data_time_max=None, y_tickers=None,
                     y_ticklabels=None, SignalName=None):
        '''
        :param data_time: list
        :param data_value: list
        :param data_time_min: the minimal timestamp
        :param data_time_max: the maximal timestamp
        :param y_tickers: values
        :param y_ticklabels: texts corresponding to values
        :param SignalName: string
        :return: return a line2D object
                to be noticed, don't forget , at the end
        '''
        x_values = [datetime.fromtimestamp(d) for d in data_time]
        if y_tickers is None:
            self.line[SignalName].set_xdata(x_values)
            self.line[SignalName].set_ydata(data_value)
        else:
            self.y_ticks_value = []
            for value in data_value:
                self.y_ticks_value.append(y_ticklabels.index(value))
            self.ax[SignalName].set_yticks(y_tickers)
            self.ax[SignalName].set_yticklabels(y_ticklabels)
            self.line[SignalName].set_xdata(x_values)

            self.line[SignalName].set_ydata(self.y_ticks_value)

        self.ax[SignalName].set_xlim(min(data_time) - 1, max(data_time) + 1)
        # update range of axis x
        if data_time_min:
            self.ax[SignalName].set_xlim(data_time_min, data_time_max)
        # update legend
        self.ax[SignalName].legend(loc='upper left')
        return self.line[SignalName],

    def clean_canvas(self):
        self.figure.clear()
        self.figure.clf()
        gc.collect()
