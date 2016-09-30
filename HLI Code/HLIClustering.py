__author__ = 'guyulong'

from Tool.InOut import *
from Tool.FileTool import *
from Tool.ProcessTool import *
from Tool.Evaluation import *
from Config import *
from Venue import *
from Checkin import *
from User import *
from Location import *
from AnalyseCheckin import *
from LoadData import *
from Tool.MLTool import *
from Tool.TimerTool import *
from HLIData import *

class HLIClustering():
    def __init__(self, hliData):
        self.hliData = hliData
        pass

    def home_loc_identify_predict_clustering(self):
        clusteringMethods = Config.dictParamsClustering.keys()

        clusteringMethods = Config.clusteringMethods


        for clusteringMethod in clusteringMethods:
            self.home_loc_identify_predict_clustering_method(clusteringMethod)

    def home_loc_identify_predict_clustering_method(self, clusteringMethod):
        predictList = self.home_loc_identify_method_clustering( clusteringMethod)
        fileHomeLocCluster = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.folderRatio, clusteringMethod + Config.fileHomeLoc)
        FileTool.WriteStrListToFileWithNewLine(predictList, fileHomeLocCluster)

    def home_loc_identify_method_clustering(self, clusteringMethod):
        InOut.console_func_begin("home_loc_identify_method_clustering")

        totalCnt = len(self.hliData.userList)
        allCnt = totalCnt

        predictList = []
        resList = []

        processCnt = 0

        #for user_id in self.hliData.userList:
        for user_id in self.hliData.setUserNotKnowHome:
            city = "-1"
            if(self.hliData.dictUserCheckin.has_key(user_id) == False):
                city = "-1"
                continue


            user_checkin_List = self.hliData.dictUserCheckin[user_id]

            print "user_id: %s" %user_id
            print "user_checkin_List: %s " % len(user_checkin_List)

            (flag, loc) = self.get_loc_method_clustering(user_checkin_List, clusteringMethod)

            if(flag):
                s = user_id + "\t" + str(loc.latitude) + "\t" + str(loc.longitude)
                resList.append(s)

            processCnt += 1
            time_info_str = self.hliData.timerTool.time_info(processCnt, totalCnt)
            if(processCnt % 10 == 0):
                s = "\nProcess %s / %s, %s" % (str(processCnt), str(totalCnt), time_info_str)
                print s
            else:
                print "not in dict"
                print self.hliData.analyseCheckIn.dictCity.keys()

        #return predictList
        return resList

    def get_loc_method_clustering(self, checkInList, clusteringMethod):

        flag = False
        locRes = Location()
        if(len(checkInList) == 0):
            return (flag, locRes)

        flag = True
        dictCityCnt = {}

        print "get_city_method_clustering..."
        print clusteringMethod
        print "checkInList:"
        for checkIn in checkInList:
            print "checkIn:%s" % checkIn.toString()


        locRes = AnalyseCheckin.clustering(checkInList, clusteringMethod)

        return (flag, locRes)

    def get_city_method_clustering(self, checkInList, clusteringMethod):
        cityId = "-1"

        if(len(checkInList) == 0):
            return cityId

        dictCityCnt = {}

        print "get_city_method_clustering..."
        print clusteringMethod
        print "checkInList:"
        for checkIn in checkInList:
            print "checkIn:%s" % checkIn.toString()

        loc = AnalyseCheckin.clustering(checkInList, clusteringMethod)
        cityId = Location.getLocCityId(loc, self.hliData.analyseCheckIn.dictCity, Config.flag_clustering_nearCity)

        print "loc:%s" % loc.toString()
        print "cityId:%s" % cityId

        return cityId

    @classmethod
    def load_data_home_loc_clustering(cls, clusteringMethod):

        fileHomeLoc = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, clusteringMethod + Config.fileHomeLoc)
        #homeLocClusteringList = FileTool.ReadFileColumnList(fileHomeLoc)
        #return homeLocClusteringList
        dictUser = User.loadDictUserFromFile(fileHomeLoc)
        return dictUser

    @classmethod
    def get_loc_cluster_from_user_checkinList(cls, hliData, user_id):
        flag = True
        loc = Location()
        clusteringMethod = Config.clustering_Singlepass
        if(user_id in hliData.dictUserCheckin):
            flag = True
            checkInList = hliData.dictUserCheckin[user_id]
            loc = AnalyseCheckin.clustering(checkInList, clusteringMethod)
            if(len(checkInList) == 0):
                flag = False
        return (flag, loc)

    @classmethod
    def get_loc_cluster_from_user_checkinList_ratingList(cls, hliData, user_id):
        flag = True
        loc = Location()
        clusteringMethod = Config.clustering_Singlepass
        if(user_id in hliData.dictUserCheckin):
            flag = True
            locList = HLIClustering.merge_loc_list_from_checkin_rating_of_user(hliData, user_id)
            loc = AnalyseLoc.clustering_loc(locList, clusteringMethod)
            if(len(locList) == 0):
                flag = False
        return (flag, loc)

    @classmethod
    def merge_loc_list_from_checkin_rating_of_user(cls, hliData, user_id):
        checkInList = hliData.dictUserCheckin[user_id]
        ratingList = hliData.dictUserRating[user_id]
        locList = HLIClustering.merge_loc_list_from_checkinList_ratingList(checkInList, ratingList)
        return locList

    @classmethod
    def merge_loc_list_from_checkinList_ratingList(cls, checkInList, ratingList):
        locList = []
        locListCheckin = Checkin.format_list_checkin_to_location(checkInList)
        locListRating  = Rating.format_list_rating_to_location(ratingList)
        locList.extend(locListCheckin)
        locList.extend(locListRating)
        return locList

