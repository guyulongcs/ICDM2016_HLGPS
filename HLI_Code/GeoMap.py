from os.path import join
from Config import *
from Tool import FileTool, InOut
from Tool.InOut import *
from Tool.FileTool import *
from City import *
from Venue import *


class GeoMap():
    @classmethod
    def load_city_dict(cls):
        InOut.console_func_begin("load_city_dict")
        fileCity = join(Config.folderData, Config.folderResourse, Config.fileNorm + Config.fileCityByPopulation)
        lineList = FileTool.FileTool.ReadLineListFromFile(fileCity)

        print len(lineList)
        dictCity={}
        for line in lineList:
            #no, name, state, population, landarea, popdensity, lat, lon, swlat, swlon, nelt, nelon
            strList = line.split("\t")
            #print(len(strList))
            if(len(strList) != 12):
                print line
                continue
            city = City()
            city.set_value(strList)

            dictCity[city.id] = city

        return dictCity

