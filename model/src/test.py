import DataModel
import PlotModel
from ProcessSimulation import ProcessSimulation, Distribution
import numpy as np

import matplotlib.pyplot as plt
import time

if __name__ == '__main__':

    process_1 = ProcessSimulation(10000000, 100, 5, 3, 4, 5, 1, 1)
    process_2 = ProcessSimulation(10000000, 100, 5, 3, 4, 5, 1, 1)

    start = time.clock()
    process_1.start_simulation()
    process_2.start_simulation()

    plot_1 = PlotModel.PlotModel(process_1)
    plot_2 = PlotModel.PlotModel(process_2)
    plot_1.show_pdf_with_threshold(100)
    plot_1.show_pdf_without_threshold(100)
    plot_1.show_cdf(100)
    plot_2.show_cdf(100)
    end = time.clock() - start
    print(end)
    plot_1.kolmogorov_distance(plot_2)
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
