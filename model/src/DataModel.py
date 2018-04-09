import numpy as np


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

    def print(self):
        if self._times.shape:
            for i in range(self._times.shape[0]):
                print("Time: {}___Value: {}".format(self._times[i], self._values[i]))
        else:
            print("Empty")
    def get_values_mean(self):
        return self._times.mean()

    def get_values(self):
        return self._values

    def get_times(self):
        return self._times

    def add_value(self, value):
        self._values.__add__(value)
        # self._values = np.append(self._values, value)

    def add_time(self, time):
        self._times.__add__(time)
        # self._times = np.append(self._values, time)