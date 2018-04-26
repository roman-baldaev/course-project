import numpy as np
import pandas as pd

class DataModel:
    """
    This class implements a data model - values at time points and provides methods for working with these data.
    """

    def __init__(self, n=0, values=None, times=None):
        """
        A constructor that takes values and a time point.

        :param values: Array of values process
        :param times: Array of a time points
        """
        if (values is None) or (times is None):
            self._times = np.zeros((n, ))
            self._values = np.zeros((n, ))
        else:
            if len(values) != len(times):
                print("Different size of values and times")
            else:
                self._times = np.array(times, dtype=float)
                self._values = np.array(values, dtype=float)

    def print(self, n=None):
        if n is not None:
            _n = n
        elif self._times.shape:
                _n = self._times.shape[0]
        for i in range(_n):
            print("Time: {}___Value: {}".format(self._times[i], self._values[i]))

    def get_values_mean(self):
        return self._times.mean()

    def get_values(self):
        return self._values

    def get_times(self):
        return self._times

    def add_value(self, value, index):
        # self._values.__add__(value)
        self._values[index] = value

    def add_time(self, time, index):
        # self._times.__add__(time)
        self._times[index] = time

    def get_value(self, index):
        return self._values[index]

    def get_time(self, index):
        return self._times[index]