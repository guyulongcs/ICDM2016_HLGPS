import gmplot

from Tool.GeoPlot.gmplot.gmplot import *
from PlotCity import *
from PlotTest import *
from PlotExpRes import *

class Plot():
    def __init__(self):
        pass

    def start(self):
        #pl = PlotCity()
        #pl.start()

        pl = PlotTest()
        #pl.start()

        pl = PlotExpRes()
        pl.start()
