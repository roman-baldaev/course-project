import DataModel
import matplotlib.pyplot as plt

class PlotModel:
    """
    This class implements methods for visualizing the DateModel model.
    """

    def __init__(self, new_model):

        self._model = new_model

    def show_hist(self):

        plt.hist(self._model.get_times())
        plt.show()