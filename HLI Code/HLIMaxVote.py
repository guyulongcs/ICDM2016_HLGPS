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

class HLIMaxVote():
    def __init__(self, hliData):
        self.hliData = hliData
        pass


    def home_loc_identify_predict_maxVote(self):
        predictListMaxVote = self.home_loc_identify_method_max_vote()
        fileHomeLocVote = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.methodVote + Config.fileHomeLoc)
        FileTool.WriteStrListToFileWithNewLine(predictListMaxVote, fileHomeLocVote)


    #get cityid of userlist
    def home_loc_identify_method_max_vote(self):
        InOut.console_func_begin("home_loc_identify_method_max_vote")
        totalCnt = len(self.hliData.userList)

        predictList = []

        processCnt = 0
        totalCnt = len(self.hliData.userList)

        resList = []

        self.hliData.timerTool.start()
        for user_id in self.hliData.userList:
            print "user_id: %s" %user_id
            if(self.hliData.dictUserCheckin.has_key(user_id) == False):
                #print "not has check in"
                city = "-1"
            else:
                checkInList = self.hliData.dictUserCheckin[user_id]
                if(len(checkInList) == 0):
                    continue
                #user_checkin_cityList = self.dictUserCheckinCity[user_id]

                #print "user_id: %s" % user_id
                print "checkInList: %s " % len(checkInList)
                user_checkin_cityList = self.hliData.analyseCheckIn.trans_listCheckin_to_listCityId(checkInList, Config.flag_maxvote_nearCity)
                city = self.get_city_from_citylist_max_vote(user_checkin_cityList)

                latRes = 0.0
                lonRes = 0.0
                if(city != "-1" and (city in self.hliData.analyseCheckIn.dictCity)):
                    cityItem = self.hliData.analyseCheckIn.dictCity[city]
                    latRes = cityItem.lat
                    lonRes = cityItem.lon

                    s = user_id + "\t" + str(latRes) + "\t" + str(lonRes)
                    resList.append(s)

            print "city: %s" % city
            predictList.append(city)

            processCnt += 1
            time_info_str = self.hliData.timerTool.time_info(processCnt, totalCnt)
            if(processCnt % 10 == 0):
                s = "\nProcess %s / %s, %s" % (str(processCnt), str(totalCnt), time_info_str)
                print s

        #return predictList
        return resList

    #get cityid from citylist
    def get_city_from_citylist_max_vote(self, cityList):

        #InOut.console_func_begin("get_city_method_max_vote")
        cityId = "-1"

        if(len(cityList) == 0):
            return cityId


        print cityList
        dictCityCnt = {}

        for city in cityList:
            if(city == "-1"):
                continue
            if(dictCityCnt.has_key(city) == False):
                dictCityCnt[city] = 0
            dictCityCnt[city] = dictCityCnt[city] + 1

        if(len(dictCityCnt) == 0):
            cityId = "-1"
        else:
            dictCityCntList = Tool.Process.Process.dict_sort(dictCityCnt, True)
            cityId = dictCityCntList[0][0]
        #print cityId

        #print "get_city_method_max_vote... cityId:%s" % cityId

        return cityId

    @classmethod
    def load_data_home_loc_vote(cls):
        fileHomeLoc = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.methodVote + Config.fileHomeLoc)
        #homeLocVoteList = FileTool.ReadFileColumnList(fileHomeLocVote)
        #return homeLocVoteList
        dictUser = User.loadDictUserFromFile(fileHomeLoc)
        return dictUser