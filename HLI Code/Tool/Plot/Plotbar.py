import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class Plotbar():
    def __init__(self):
        #x
        self.xlabels = []
        self.xcolor = []
        self.xwidth = 0.5
        self.xwidth_base = 1.2
        #y
        self.y = []
        self.yaxis = []
        self.ylabel = ""
        self.title = ""
        self.alpha=0.6
        self.grid = False
        self.file = ""



        pass

    def plot_bar(self):
        #plot setting
        ymin = self.yaxis[0]
        ymax = self.yaxis[1]
        ytick = self.yaxis[2]
        N=len(self.y)
        ind = np.arange(N)
        yt=np.arange(ymin, ymax, ytick)

        #plot
        pp = PdfPages(self.file)
        plt.figure(1)
        plt.grid(self.grid)
        p = plt.bar(ind, self.y, color = self.xcolor, alpha=self.alpha)
        plt.title(self.title)
        plt.xticks(ind + self.xwidth/self.xwidth_base, self.xlabels)
        plt.yticks(yt)
        plt.ylabel(self.ylabel)
        plt.ylim(ymin,ymax)

        pp.savefig()
        pp.close()
        plt.close()



    @classmethod
    def demo(cls):
        plotBar = Plotbar()
        plotBar.xlabels = ["HLIA", "Maxvote", "ClusterHier", "Avg"]
        plotBar.file = "pic.pdf"
        plotBar.xcolor = ['red','green','blue','orange']
        plotBar.xwidth = 0.5
        plotBar.y = [92.3, 91.9, 91.6, 88.8]
        plotBar.yaxis = [86, 93.5, 1]
        plotBar.ylabel = "ACC"
        plotBar.title = "Performance of methods for users who have check-in data"
        plotBar.alpha=0.6
        plotBar.grid = False

        plotBar.plot()