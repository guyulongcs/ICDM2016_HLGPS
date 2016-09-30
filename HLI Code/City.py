__author__ = 'guyulong'

from os.path import join
import  numpy as np
from Config import *
from Tool import FileTool, FormatTool
from Tool.FormatTool import *

class City():
    def __init__(self, id="", name ="", state="", population=0.0, landarea=0.0, popdensity=0.0, lat=0.0, lon = 0.0, swlat=0.0, swlon=0.0, nelat=0.0, nelon=0.0):
         #no, name, state, population, landarea, popdensity, lat, lon, swlat, swlon, nelat, nelon
        self.id = id
        self.name = name
        self.state = state
        self.population = population
        self.landarea = landarea
        self.popdensity = popdensity
        self.lat = lat
        self.lon = lon
        self.swlat = swlat
        self.swlon = swlon
        self.nelat = nelat
        self.nelon = nelon


    def set_value(self, list):
        if(len(list) != 12):
            return
        self.id = list[0]
        self.name = list[1]
        self.state = list[2]
        self.population = FormatTool.float_str_to_float(list[3])
        self.landarea = FormatTool.float_str_to_float(list[4])
        self.popdensity = FormatTool.float_str_to_float(list[5])
        self.lat = FormatTool.float_str_to_float(list[6])
        self.lon = FormatTool.float_str_to_float(list[7])
        self.swlat = FormatTool.float_str_to_float(list[8])
        self.swlon = FormatTool.float_str_to_float(list[9])
        self.nelat = FormatTool.float_str_to_float(list[10])
        self.nelon = FormatTool.float_str_to_float(list[11])

        pass

    def start(self):
        City.load_city_data()

    @classmethod
    def load_city_data2(cls):
        fileUS = join(Config.folderData, Config.folderResourse, Config.fileUS)
        (name, lat, lon, city) = np.loadtxt(fileUS, dtype="string", delimiter="\t",usecols=(1,4,5,17),unpack=True )


    @classmethod
    def load_city_data(cls):
        fileUS = join(Config.folderData, Config.folderResourse, Config.fileUS)
        fileUSCity = join(Config.folderData, Config.folderResourse, Config.fileUSCity)

        lineList = FileTool.FileTool.ReadLineListFromFile(fileUS)

        dictLenCnt={}

        venueList = []
        latList = []
        lonList = []
        cityList = []

        for i in range(len(lineList)):
            line = lineList[i]
            itemList = line.split("\t")
            n = len(itemList)
            if(dictLenCnt.has_key(n) == False):
                dictLenCnt[n]=0
            dictLenCnt[n] = dictLenCnt[n] + 1

            venue = itemList[1]
            lat = itemList[4]
            lon = itemList[5]
            city = itemList[17]

            venueList.append(venue)
            latList.append(lat)
            lonList.append(lon)
            cityList.append(city)






        #print dictLenCnt

        citySet = set(cityList)
        print len(citySet)
        print citySet

        cityListNew = list(citySet)
        FileTool.FileTool.WriteStrListToFileWithNewLine(cityListNew, fileUSCity)



