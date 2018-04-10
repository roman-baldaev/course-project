import DataModel
import PlotModel
from ProcessSimulation import ProcessSimulation, Distribution
import numpy as np

import matplotlib.pyplot as plt
import time

if __name__ == '__main__':

    process = ProcessSimulation(1000000, 1000, 5, 0.5, 4, 5, 1, 1)
    start = time.clock()
    process.start_simulation()

    plot = PlotModel.PlotModel(process)
    # process.get_data().print()
    plot.show_cdf(50)
    end = time.clock() - start
    print(end)
    # plot.show_realization(0,10000)

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
