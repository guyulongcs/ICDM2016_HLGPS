import gmplot

from Tool.GeoPlot.gmplot.gmplot import *
from Config import *
from os.path import *
from Checkin import *
from Tool.ProcessTool import *
from Tool.InOut import *

from GeoMap import *
import matplotlib.pyplot as plt

class PlotTest():
    def __init__(self):
        pass

    def start(self):

        plt.rcdefaults()


        # Example data
        people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
        y_pos = np.arange(len(people))
        performance = 3 + 10 * np.random.rand(len(people))
        error = np.random.rand(len(people))

        plt.bar(y_pos, performance, align='center', alpha=0.4)
        plt.yticks(y_pos, people)
        plt.xlabel('Performance')
        plt.title('How fast do you want to go today?')

        plt.show()