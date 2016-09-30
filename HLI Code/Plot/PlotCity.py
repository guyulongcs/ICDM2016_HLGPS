import gmplot

from Tool.GeoPlot.gmplot.gmplot import *
from Config import *
from os.path import *
from Checkin import *
from Tool.ProcessTool import *
from Tool.InOut import *

from GeoMap import *

class PlotCity():
    def __init__(self):
        self.path = '/Users/guyulong/Documents/'
        self.fileName = 'map.html'
        self.dictCity = GeoMap.load_city_dict()
        pass

    def start(self):
        file = join(self.path, self.fileName)
        (checkLatList, checkLonList) = self.get_check_in_plot_list()

        #GoogleMapPlotter.demo(file)
        #return

        mymap = GoogleMapPlotter(37.428, -110.145, 4.5)
        #mymap = GoogleMapPlotter.from_geocode("America", 4.5)


        latList = []
        lonList = []
        for cityId in self.dictCity:
            city = self.dictCity[cityId]
            lat = city.lat
            lon = city.lon
            latList.append(lat)
            lonList.append(lon)

            #mymap.marker(lat, lon, "green")
            mymap.circle(lat, lon, 20000, "b", ew=2)
            #mymap.polygon(path3[0], path3[1], edge_color="cyan", edge_width=5, face_color="blue", face_alpha=0.1)

        #mymap.heatmap(latList, lonList, threshold=10, radius=20)
        mymap.heatmap(checkLatList, checkLonList, threshold=10, radius=40)

        #mymap.heatmap(latList, lonList, threshold=10, radius=20)
       # mymap.scatter(latList, lonList, c='r', marker=True)





        #mymap.marker(37.427, -122.145, "yellow")

        mymap.draw(file)
        pass

    def load_check_in_list(self):
        InOut.console_func_begin("load_check_in_list")
        file_checkin = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileCheckin)
        file_checkin = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileCheckin)

        checkInList = Checkin.loadCheckinFromFile(file_checkin)
        print "checkInList", len(checkInList)
        checkInList = ProcessTool.sampleListByRatio(checkInList, 1)
        return checkInList

    def get_check_in_plot_list(self):
        InOut.console_func_begin("get_check_in_plot_list")
        checkInList = self.load_check_in_list()
        latList = []
        lonList = []
        for checkin in checkInList:
            latList.append(checkin.latitude)
            lonList.append(checkin.longitude)
        print "len:", len(latList), len(lonList)
        return (latList, lonList)




def __main__():
    pl = PlotCity()
    pl.start()