 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from os.path import join
from Config import *
from Tool import FileTool, InOut, GeoCoder



class Resource():
    def start(self):
        self.preProcess()

    def preProcess(self):
        self.processCityByPopulation()
        pass

    def processCityByPopulation(self):
        fileCityByPop = join(Config.folderData, Config.folderResourse, Config.fileCityByPopulation)
        fileCityByPopNorm = join(Config.folderData, Config.folderResourse, Config.fileNorm + Config.fileCityByPopulation)
        lineList = FileTool.FileTool.ReadLineListFromFile(fileCityByPop)

        lineListNew = []
        lineCnt = len(lineList)
        for i in range(0, lineCnt, 3):
            try:
                line1 = lineList[i]
                line2 = lineList[i+1]
                line3 = lineList[i+2]

                lineNew = line1+line2+line3

                lineNewNorm = ""
                lineNewNorm = self.processCityByPopulationNormLine(lineNew)
                lineListNew.append(lineNewNorm)
                #break

            except:
                InOut.InOut.except_info("processCityByPopulation")

        FileTool.FileTool.WriteStrListToFileWithNewLine(lineListNew, fileCityByPopNorm)
        pass

    def processCityByPopulationNormLine(self, str):
        InOut.InOut.console_func_begin("processCityByPopulationNormLine")
        strNorm = ""

        try:
            strList = str.split("\t")
            if(len(strList) == 9):
                cityNo = strList[0]
                cityName = strList[1]
                cityState = strList[2]
                cityPopulation = strList[4]
                cityLandArea = strList[6]
                cityPopdensity = strList[7]
                cityLatLon = strList[8]

                #

                cityName = cityName.partition("[")[0]
                cityPopulation = cityPopulation.replace(",","")
                cityLandArea = cityLandArea.partition("sq mi")[2].partition(" km2")[0].replace(",","")
                cityPopdensity = cityPopdensity.partition("per sq mi")[2].partition(" km")[0].replace(",","")
                cityLat = cityLatLon.partition("°N")[0]
                cityLon = "-"+cityLatLon.partition("°N ")[2].partition("°W")[0]

                #print cityName
                boundBox = None

                #print cityLat, cityLon

                #no, name, state, population, landarea, popdensity, lat, lon, swlat, swlon, nelt, nelon
                listNew = []
                listNew.append(cityNo)
                listNew.append(cityName)
                listNew.append(cityState)
                listNew.append(cityPopulation)
                listNew.append(cityLandArea)
                listNew.append(cityPopdensity)
                listNew.append(cityLat)
                listNew.append(cityLon)

                placeName = "%s,%s" % (cityName, cityState)
                try:

                    boundBox = GeoCoder.GeoCoder.get_place_bound_box(placeName)
                except:
                    boundBox = None
                    print "except boundbox %s" % placeName

                if(boundBox != None):
                    swlat = "%f" % boundBox.swlat
                    swlon = "%f" % boundBox.swlon
                    nelat = "%f" % boundBox.nelat
                    nelon = "%f" % boundBox.nelon

                    listNew.append(swlat)
                    listNew.append(swlon)
                    listNew.append(nelat)
                    listNew.append(nelon)


                #print listNew
                strNorm = "\t".join(listNew)

        except:
            InOut.InOut.except_info("processCityByPopulationNormLine")

        return strNorm







