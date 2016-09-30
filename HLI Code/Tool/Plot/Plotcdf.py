import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from bisect import bisect_left


class Plotcdf():
    def __init__(self):
        self.data = None
        self.xa = None
        self.ya = None
        self.file = ""


        pass

    def plot_cdf(self):
        #plot
        pp = PdfPages(self.file)
        plt.figure(1)

        plt.plot(self.xa, self.ya)


        pp.savefig()
        pp.close()
        plt.close()



    def plot_cdf2(self):
        #plot setting

        cdf = discrete_cdf(self.data)
        xvalues = range(0, int(max(self.data)))
        yvalues = [cdf(point) for point in xvalues]


        #plot
        pp = PdfPages(self.file)

        plt.figure(1)

        #plt.plot(xvalues, yvalues)

        n, bins, patches = plt.hist(self.data, 100, normed=1, facecolor='green', alpha=0.75)


        pp.savefig()
        pp.close()
        plt.close()


class discrete_cdf():
    def __init__(self, data):
        self._data = data # must be sorted
        self._data_len = float(len(data))

    def __call__(self, point):
        return (len(self._data[:bisect_left(self._data, point)]) /
                self._data_len)