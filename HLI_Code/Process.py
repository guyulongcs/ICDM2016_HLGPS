import Tool.InOut
from Tool.InOut import *
from PreProcess import *
from HomeLocIdentify import *
from Analyse import *
from City import *
from Resource import *
from GetExpData import *
from GetExpRatioData import *
from Tool.InOut import *
from Tool.Clustering import *
from Test import *
from Plot.Plot import *

class Process():
    @classmethod
    def start(cls):
        InOut.console_func_begin("Process")

        prePro = PreProcess()
        #prePro.start()
        #return

        pl = Plot()
        pl.start()
        return


        city = City()
        #city.start()

        resource = Resource()
        #resource.start()


        if(Config.flag_exp_generate_exp_data):
            getExpData = GetExpData()
            getExpData.start()

        if(Config.flag_exp_generate_ratio_data):
            getExpRatioData = GetExpRatioData()
            getExpRatioData.start()

        #return


        analyse = Analyse()
        #analyse.start()
        #return


        #Test.test()
        #return

        hli = HomeLocIdentify()
        hli.start()

        InOut.console_func_end("Process")


if __name__ == "__main__":
    Process.start()

