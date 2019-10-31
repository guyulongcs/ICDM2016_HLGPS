from os.path import join
from Config import *
from Tool import FormatTool
from Tool import GeoLoc
from Tool import Clustering

from Tool.FormatTool import *
from Tool.GeoLoc import *
from Tool.Clustering import *
from User import *
from GeoMap import *
from Location import *
from Checkin import *
from Tool.InOut import *
from AnalyseLoc import *

class AnalyseCheckin():
    def __init__(self):
        self.dictCity = GeoMap.load_city_dict()
        pass

    def start(self):

        self.checkCheckinInDictCity()

    def loadCheckinFromFileFilt(self):
        listCheckin = []
        file = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileCheckin)
        return Checkin.loadCheckinFromFile(file)

    def trans_checkin_to_cityId(self, checkin, flagNearCity=False):
        loc = Location(checkin.latitude, checkin.longitude)
        city = Location.getLocCity(loc, self.dictCity, flagNearCity)

        cityId = -1
        if(city != None):
            cityId = city.id

        return cityId

    def trans_listCheckin_to_listCityId(self, listCheckin, flagNearCity=False):
        resList = []
        for checkin in listCheckin:
            cityId = self.trans_checkin_to_cityId(checkin, flagNearCity)
            resList.append(cityId)
        return resList

    def checkCheckinInDictCity(self):
        InOut.console_func_begin("checkCheckinInDictCity start")
        self.listCheckin = Checkin.loadCheckinFromFileFilt()
        fileCheckinCity = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileCheckinCity)

        cntNo=0
        cnt = 0

        index=0
        totalCnt = len(self.listCheckin)
        lineCheckinCityList = []
        for checkin in self.listCheckin:
            cnt = cnt + 1
            #print len(self.dictCity)
            #print (user.id, user.latitude, user.longitude)
            loc = Location(checkin.latitude, checkin.longitude)
            city = Location.getLocCity(loc, self.dictCity)

            cityId = -1
            if(city == None):
                #print (user.latitude, user.longitude)
                cntNo = cntNo + 1
            else:
                cityId = city.id

            tmpList=[]
            tmpList.append(str(checkin.id))
            tmpList.append(str(checkin.user_id))
            tmpList.append(str(checkin.venue_id))
            tmpList.append(str(checkin.latitude))
            tmpList.append(str(checkin.longitude))
            tmpList.append(str(checkin.created_at))
            tmpList.append(str(cityId))

            lineCheckinCity = "\t".join(tmpList)
            lineCheckinCityList.append(lineCheckinCity)
            index = index + 1
            if(index % 1000 == 0):
                print "%s/%s\tNo:%s/%s" % (index, totalCnt, cntNo, cnt)
                #break

        print "No: %s/%s" % (cntNo, cnt)
        FileTool.FileTool.WriteStrListToFileWithNewLine(lineCheckinCityList, fileCheckinCity)



    @classmethod
    def clustering(cls, checkInList, clustering_method):

        loc = Location()
        N = len(checkInList)
        if(N == 0):
            return loc
        if(N == 1):
            return Checkin.format_checkin_to_location(checkInList[0])

        if(clustering_method == Config.clustering_Singlepass):
            loc = AnalyseCheckin.clustering_Singlepass(checkInList)

        elif(clustering_method == Config.clustering_Kmeans):
            loc = AnalyseCheckin.clustering_Kmeans(checkInList)

        elif (clustering_method == Config.clustering_Hierarchical):
            loc = AnalyseCheckin.clustering_Hierarchical(checkInList)
        return loc
        pass





    @classmethod
    def clustering_Singlepass(cls, checkInList):
        InOut.console_func_begin("clustering_Singlepass")
        geoLocList = Checkin.format_list_checkin_to_geoLoc(checkInList)
        return AnalyseLoc.clustering_geoloc_Singlepass(geoLocList)


    @classmethod
    def clustering_Kmeans(cls, checkInList):
        InOut.console_func_begin("clustering_Kmeans")
        geoLocList = Checkin.format_list_checkin_to_geoLoc(checkInList)
        return AnalyseLoc.clustering_geoloc_Kmeans(geoLocList)

    @classmethod
    def clustering_Hierarchical(cls, checkInList):
        InOut.console_func_begin("clustering_Hierarchical")

        flagFilt = Config.dictParamsClustering[Config.clustering_Hierarchical]["flagFiltTimeInNight"]
        if(flagFilt):
            checkInListNew = Checkin.filt_checkin_in_night(checkInList)
            if(len(checkInListNew) > 0):
                checkInList = checkInListNew


        geoLocList = Checkin.format_list_checkin_to_geoLoc(checkInList)


        loc = Location()
        loc = Clustering.cluster_Hierarchical_loc(geoLocList, Config.dictParamsClustering[Config.clustering_Hierarchical]["n_clusters"])
        return loc
