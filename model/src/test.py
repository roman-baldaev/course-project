import DataModel
import PlotModel
from ProcessSimulation import Distribution
import numpy as np
import matplotlib.pyplot as plt


if __name__=='__main__':

    model = DataModel.DataModel(0)
    for i in range(10000000):
        model.add_time(i-1)
        model.add_value(i+1)
    print("Finish")
    # plot = PlotModel.PlotModel(model)
    # plot.show_hist()

    # model.print()
    # print(np.count_nonzero((times > 0) & (times < 1)))

    # Normal = Distribution('normal', (0, 0.001))
    # a = []
    # for i in range(100000):
    #     a.append(Normal.get_value())
    # data = np.array(a)
    # plt.hist(data, bins=100)
    # plt.show()
