import DataModel
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from math import floor

class PlotModel:
    """
    This class implements methods for visualizing the DateModel model.
    """

    def __init__(self, process):
        """

        :param process: Instance of a class "ProcessSimulation"
        _pdf its a result of calculate PDF
        _cdf its a result of calculate CDF
        """
        self._process = process
        self._pdf = None
        self._cdf = None

    def show_realization(self, start=0, end=100):
        """
        A method showing the implementation of a process in the range from
        "start" to "end"
        :param start: left border of interval
        :param end: right border of interval
        :return: just show plot
        """
        n = end - start

        old_values = self._process.get_data().get_times()[start:end]
        old_times = self._process.get_data().get_values()[start:end]
        values = np.zeros((n*2,))
        times = np.zeros((n*2,))
        values = []
        times = []

        for i in range(0, n):
            values.append(old_values[i])
            values.append(old_values[i])

        times.append(old_times[0])
        for i in range(1, n):
            times.append(old_times[i])
            times.append(old_times[i])
        times.append(old_times[-1])
        threshold_time_interval = [old_times[0], times[-1]]
        plt.plot(values, times)
        plt.plot(threshold_time_interval, [self._process.get_threshold()] * 2)
        print(old_times[end-1])
        plt.show()

    def calculate_pdf(self, number_of_splits):

        times = pd.Series(self._process.get_data().get_times())
        values = pd.Series(self._process.get_data().get_values())


        sum_of_time_intervals = pd.Series(np.zeros((number_of_splits, )))
        steps = np.zeros((number_of_splits, ))

        max_value = np.max(values)
        min_value = np.min(values)
        diff = max_value - min_value
        step = diff / number_of_splits

        lengths_of_time_intervals = pd.Series(
            np.array([times[i] - times[i-1] for i in range(1, len(times))], dtype=float)
        )
        # for i in range(len(lenghts_of_time_intervals)):
        #     sum_of_time_intervals[floor(values[i] / number_of_splits)] += lenghts_of_time_intervals[i]
        steps[0] = min_value
        for i in range(1, number_of_splits):
            steps[i] = steps[i-1] + step
        steps[number_of_splits-1] = max_value
        pdf = pd.DataFrame({'volume': values[0:-1], 'interval': lengths_of_time_intervals})

        for i in range(1, len(steps)-1):
            sum_of_time_intervals[i] = pd.Series.sum(pdf[(pdf.volume > steps[i]) & (pdf.volume <= steps[i+1])].interval)


        sum_of_time_intervals.values[-1] = pd.Series.sum(pdf[pdf.values >= steps[-1]].interval)
        sum_of_time_intervals.values[0] = times.values[-1] - pd.Series.sum(sum_of_time_intervals)
        # steps = steps / 2

        sum_of_time_intervals = sum_of_time_intervals / times.values[-1]
        # print("Sum density: {}".format(pd.Series.sum(sum_of_time_intervals)))

        self._pdf = (steps, sum_of_time_intervals)

    def calculate_pdf_one_step(self):

        times = pd.Series(self._process.get_data().get_times())
        values = pd.Series(self._process.get_data().get_values())

        max_value = math.floor(np.max(values))
        min_value = math.ceil(np.min(values))

        number_of_splits = max_value - min_value

        sum_of_time_intervals = pd.Series(np.zeros((number_of_splits, )))
        steps = np.zeros((number_of_splits, ))

        steps[0] = min_value
        for i in range(1, number_of_splits):
            steps[i] = steps[i-1] + 1

        lengths_of_time_intervals = pd.Series(
            np.array([times[i] - times[i-1] for i in range(1, len(times))], dtype=float)
        )

        pdf = pd.DataFrame({'volume': values[0:-1], 'interval': lengths_of_time_intervals})

        for i in range(1, len(steps)-1):
            sum = pd.Series.sum(pdf[(pdf.volume > steps[i]) & (pdf.volume <= steps[i+1])].interval)
            if sum is not np.NaN:
                sum_of_time_intervals[i] = sum
            else:
                sum_of_time_intervals[i] = 0

        sum_of_time_intervals.values[-1] = pd.Series.sum(pdf[pdf.values >= steps[-1]].interval)
        sum_of_time_intervals.values[0] = times.values[-1] - pd.Series.sum(sum_of_time_intervals)
        # steps = steps / 2
        print(sum_of_time_intervals)

        sum_of_time_intervals = sum_of_time_intervals / times.values[-1]


        self._pdf = (steps, sum_of_time_intervals)

    def show_scale_pdf(self, number_for_primary_partition, number_of_splits, start, end):

        times = self._process.get_data().get_times()
        values = self._process.get_data().get_values()

        sum_of_time_intervals = np.zeros((number_of_splits, ), dtype='float64')
        steps = np.zeros((number_for_primary_partition, ), dtype='float64')

        lengths_of_time_intervals = np.array(
            [times[i] - times[i-1] for i in range(1, len(times))], dtype='float64'
        )

        # for i in range(len(lenghts_of_time_intervals)):
        #     sum_of_time_intervals[floor(values[i] / number_of_splits)] += lenghts_of_time_intervals[i]
        steps = np.zeros((number_of_splits, ), dtype='float64')

        max_value = np.max(values)
        min_value = np.min(values)
        diff = max_value - min_value
        step = diff / number_of_splits

        for i in range(1, number_of_splits):
            steps[i] = steps[i-1] + step
        steps[number_of_splits - 1] = max_value

        pdf = pd.DataFrame({
            'values': values[0:-1],
            'interval': lengths_of_time_intervals
            })
        data_with_the_highest_number_of_requests = pdf[(pdf.values > start) & (pdf.values < end)]

        max_requests = 0

        # for i in range(1, len(steps)-1):
        #     _pdf = pdf[(pdf.values >= steps[i]) & (pdf.values < steps[i+1])]
        #     print(_pdf.size)
        #     if _pdf.size > max_requests:
        #         data_with_the_highest_number_of_requests = _pdf
        #         max_requests = _pdf.size

        max_value = np.max(data_with_the_highest_number_of_requests.values)
        min_value = np.min(data_with_the_highest_number_of_requests.values)
        diff = max_value - min_value
        step = diff / number_of_splits
        print(step)
        steps[0] = min_value
        for i in range(1, number_of_splits):
            steps[i] = steps[i-1] + step
        steps[number_of_splits - 1] = max_value
        print(steps)
        for i in range(1, len(steps)-1):
            sum_of_time_intervals[i] = np.sum(
                data_with_the_highest_number_of_requests[
                    (data_with_the_highest_number_of_requests.values >= steps[i])
                    & (data_with_the_highest_number_of_requests.values < steps[i+1])].interval
            )
        sum_of_time_intervals[-1] = np.sum(
            data_with_the_highest_number_of_requests[
                data_with_the_highest_number_of_requests.values >= steps[-1]
            ].interval
        )
        sum_of_time_intervals[0] = times[-1] - np.sum(sum_of_time_intervals)
        # steps = steps / 2

        sum_of_time_intervals = sum_of_time_intervals / times[-1]

        plt.plot(steps, sum_of_time_intervals)
        plt.show()

    def calculate_cdf(self, number_of_splits):
        """
        calculate CDF based on PDF
        :param number_of_splits:
        :return:
        """

        # if self._pdf is not None, parameter 'number_of_splits' will be ignored
        if self._pdf is None:
            self.calculate_pdf_one_step()

        n = self._pdf[0].shape[0]
        print(n)
        probabilities = np.zeros((n, ), dtype='float64')
        pdf_probabilities = self._pdf[1]
        probabilities[0] = pdf_probabilities[0]
        values = self._pdf[0]

        for i in range(1, n):
            if pdf_probabilities[i] is not None:
                probabilities[i] = probabilities[i-1] + pdf_probabilities[i]
            else:
                probabilities[i] = probabilities[i - 1] + 0

        # self._cdf = (values, probabilities)
        self._cdf = [values, probabilities]


    def kolmogorov_distance(self, second_plot):

        diff_start = np.int(np.absolute(self._cdf[0][0] - second_plot._cdf[0][0]))
        diff_end = np.int(np.absolute(self._cdf[0][-1] - second_plot._cdf[0][-1]))
        zeros = np.zeros((diff_start, ))
        if self._cdf[0][0] > second_plot._cdf[0][0]:
            values = [i for i in range(int(second_plot._cdf[0][0]), int(self._cdf[0][0]))]
            self._cdf[1] = np.concatenate([zeros, self._cdf[1]])
            self._cdf[0] = np.concatenate([values, self._cdf[0]])
        else:
            values = [i for i in range(int(self._cdf[0][0]), int(second_plot._cdf[0][0]))]
            second_plot._cdf[1] = np.concatenate([zeros, second_plot._cdf[1]])
            second_plot._cdf[0] = np.concatenate([values, second_plot._cdf[0]])

        ones = np.ones((diff_end, ))
        if self._cdf[0][-1] < second_plot._cdf[0][-1]:
            values = [i for i in range(int(self._cdf[0][-1]), int(second_plot._cdf[0][-1]))]
            self._cdf[1] = np.concatenate([self._cdf[1], ones])
            self._cdf[0] = np.concatenate([self._cdf[0], values])
        else:
            values = [i for i in range(int(second_plot._cdf[0][-1]), int(self._cdf[0][-1]))]
            second_plot._cdf[1] = np.concatenate([second_plot._cdf[1], ones])
            second_plot._cdf[0] = np.concatenate([second_plot._cdf[0], values])

        array_distance = np.absolute(self._cdf[1] - second_plot._cdf[1])

        print("Kolmogorov distance: {}".format(np.max(array_distance)))

    def show_two_cdf(self, second_plot):
        plt.plot(self._cdf[0], self._cdf[1])
        plt.plot(second_plot._cdf[0], second_plot._cdf[1], color='red')
        plt.show()

    def show_pdf_with_threshold(self, number_of_splits):
        if self._pdf is not None:
            pass

        else:
            self.calculate_pdf_one_step()
        x = [self._process.get_threshold(), self._process.get_threshold()]
        y = [np.min(self._pdf[1]), np.max(self._pdf[1])]
        plt.plot(self._pdf[0], self._pdf[1])
        plt.plot(x, y, color='r', linewidth=1)
        plt.show()

    def show_pdf_without_threshold(self, number_of_splits):
        if self._pdf is not None:
            pass

        else:
            self.calculate_pdf(number_of_splits)
        x = [self._process.get_threshold(), self._process.get_threshold()]
        y = [np.min(self._pdf[1]), np.max(self._pdf[1])]
        plt.plot(self._pdf[0], self._pdf[1])
        plt.show()

    def show_cdf(self, number_of_splits):
        if self._cdf is not None:
            pass

        else:
            self.calculate_cdf(number_of_splits)
        plt.plot(self._cdf[0], self._cdf[1])
        plt.show()

    def show_hist(self):

        plt.hist(self._process.get_data().get_times())
        plt.show()