import numpy as np
import DataModel


class Distribution:
    """
    An additional class for realizing the values of a particular distribution
    (since the number of distribution parameters is unknown with using getattr).
    """

    def __init__(self, distribution_name, parameters):

        #_distribution its function implements distribution 'distribution_name' from np.random object
        self._distribution = self._get_distribution_function(distribution_name)

        #tuple with parameters
        self._parameters = parameters

        if len(parameters) == 1:
            self.get_value = self.get_value_from_one_parameter_distribution

        else:
            self.get_value = self.get_value_from_two_parameters_distribution

    @staticmethod
    def _get_distribution_function(distribution):
        """
        A function that returns a function from a packet np.random.

        :return:
        The return function implements this distribution.
        """
        distribution = getattr(np.random, distribution)

        return distribution

    def get_value_from_one_parameter_distribution(self):
        return self._distribution(self._parameters[0])

    def get_value_from_two_parameters_distribution(self):
        return self._distribution(self._parameters[0], self._parameters[1])



#show getattr function for replacement "switch" of different distributions

class ProcessSimulation:

    _distributions_with_one_parameter = ('exponential',)
    _distributions_with_two_parameters = ('normal',)

    def __init__(
            self, n=100000, border_value=1.5,
            input_parameters_below_border=(1,),
            input_parameters_above_border=(0.5,),
            output_parameters_below_border=(0.5,),
            output_parameters_above_border=(1,),
            input_intensity=(0.5,),
            output_intensity=(1,),
            input_distribution="exponential",
            output_distribution="exponential",
            input_time_distribution="exponential",
            output_time_distribution="exponential",
            ):

        # distribution law of volumes of receipt of the resource
        self._input_distribution = input_distribution

        # distribution law of volumes of resource loss
        self._output_distribution = output_distribution

        # distribution law of lengths of time intervals
        self._input_time_distribution = input_time_distribution
        self._output_time_distribution = output_time_distribution

        # parameters of distribution law of volumes of receipt of the resource (below and above S-border)
        self._input_parameters_below_border = input_parameters_below_border
        self._input_parameters_above_border = input_parameters_above_border

        # parameters of distribution law of volumes of resource loss (below and above S-border)
        self._output_parameters_below_border = output_parameters_below_border
        self._output_parameters_above_border = output_parameters_above_border

        # parameters of distribution law of lengths of time intervals
        self._input_intensity = input_intensity
        self._output_intensity = output_intensity

        # number of iterations
        self._n = n

        self._border_value = border_value

        self._data = DataModel.DataModel(n)

    def start_simulation(self):

        # distributions for input resource
        input_below_border = Distribution(self._input_distribution, (self._input_parameters_below_border, ))
        input_above_border = Distribution(self._input_distribution, (self._input_parameters_above_border, ))

        # distributions for output resource
        output_below_border = Distribution(self._output_distribution, (self._output_parameters_below_border, ))
        output_above_border = Distribution(self._output_distribution, (self._output_parameters_above_border, ))

        input_intensity = Distribution(self._input_time_distribution, (self._input_intensity, ))
        output_intensity = Distribution(self._output_time_distribution, (self._output_intensity, ))

        time_input = input_intensity.get_value()
        time_output = output_intensity.get_value()

        if time_input < time_output:
            self._data.add_value(input_below_border.get_value(), 0)
            self._data.add_time(time_input, 0)
        else:
            self._data.add_value(output_below_border.get_value()*-1, 0)
            self._data.add_time(time_output, 0)

        time_input = self._data.get_time(0) + input_intensity.get_value()
        time_output = self._data.get_time(0) + output_intensity.get_value()
        i = 1
        while i < self._n:


            # up to the first loss of resources there may be several requests for replenishment
            # therefore a 'while' is used
            while time_input <= time_output and i < self._n:
                last_value = self._data.get_value(i-1)
                if last_value < self._border_value:
                    self._data.add_value(last_value + input_below_border.get_value(), i)
                else:
                    self._data.add_value(last_value + input_above_border.get_value(), i)

                self._data.add_time(time_input, i)
                time_input = self._data.get_time(i) + input_intensity.get_value()
                i += 1

            while time_input > time_output and i < self._n:
                last_value = self._data.get_value(i-1)
                if last_value < self._border_value:
                    self._data.add_value(last_value - output_below_border.get_value(), i)
                else:
                    self._data.add_value(last_value - output_above_border.get_value(), i)

                self._data.add_time(time_output, i)
                time_output = self._data.get_time(i) + output_intensity.get_value()
                i += 1

    def get_data(self):
        return self._data

    def get_threshold(self):
        return self._border_value