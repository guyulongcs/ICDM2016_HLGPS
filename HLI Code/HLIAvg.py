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

class HLIAvg():
    def __init__(self, hliData):
        self.hliData = hliData
        pass


    def home_loc_identify_predict_avg(self):
        predictList = self.home_loc_identify_method_avg()
        fileHomeLoc = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.folderRatio, Config.methodAvg + Config.fileHomeLoc)
        FileTool.WriteStrListToFileWithNewLine(predictList, fileHomeLoc)


    #get cityid of userlist

    def home_loc_identify_method_avg(self):
        InOut.console_func_begin("home_loc_identify_method_avg")

        resList = []
        totalCnt = len(self.hliData.userList)

        predictList = []

        processCnt = 0
        totalCnt = len(self.hliData.userList)

        self.hliData.timerTool.start()
        for user_id in self.hliData.userList:
            print "user_id: %s" %user_id
            if(self.hliData.dictUserCheckin.has_key(user_id) == False):
                #print "not has check in"
                city = "-1"
            else:
                checkInList = self.hliData.dictUserCheckin[user_id]
                #user_checkin_cityList = self.dictUserCheckinCity[user_id]

                #print "user_id: %s" % user_id
                print "checkInList: %s " % len(checkInList)
                (flag, loc) = HLIAvg.get_loc_method_avg(checkInList)
                if(flag):
                    s = user_id + "\t" + str(loc.latitude) + "\t" + str(loc.longitude)
                    resList.append(s)
                #city = self.get_city_method_avg(checkInList)

            #print "city: %s" % city
            #predictList.append(city)

            processCnt += 1
            time_info_str = self.hliData.timerTool.time_info(processCnt, totalCnt)
            if(processCnt % 10 == 0):
                s = "\nProcess %s / %s, %s" % (str(processCnt), str(totalCnt), time_info_str)
                print s

        return resList

    @classmethod
    def get_loc_avg_from_user_checkinList(cls, hliData, user_id):
        flag = False
        loc = Location()
        if(user_id in hliData.dictUserCheckin):
            flag = True
            checkInList = hliData.dictUserCheckin[user_id]
            (flag, loc) = HLIAvg.get_loc_method_avg(checkInList)
        return (flag, loc)


    @classmethod
    def get_loc_avg_from_user_friend(cls, hliData, user_id):
        flag = False
        loc = Location()
        locList = []
        checkInList = []
        if(user_id in hliData.dictFriend):
            friendList = hliData.dictFriend[user_id]
            for f in friendList:
                if(f in hliData.dictUserKnowHomeLoc):
                    user = hliData.dictUserKnowHomeLoc[f]
                    locList.append(Location(user.latitude, user.longitude))
            if(len(locList) > 0):
                flag = True
                loc = Location.get_avg_loc(locList)
        return (flag, loc)


    @classmethod
    def get_loc_method_avg(cls, checkInList):
        flag = False
        loc = Location()

        if(len(checkInList) == 0):
            return (flag, loc)

        flag = True


        print "get_loc_method_avg..."
        print "checkInList:"
        for checkIn in checkInList:
            print "checkIn:%s" % checkIn.toString()

        loc = Checkin.get_avg_loc(checkInList)
        return (flag, loc)

    def get_city_method_avg(self, checkInList):
        cityId = "-1"

        if(len(checkInList) == 0):
            return cityId

        dictCityCnt = {}

        print "get_city_method_avg..."
        print "checkInList:"
        for checkIn in checkInList:
            print "checkIn:%s" % checkIn.toString()

        loc = Checkin.get_avg_loc(checkInList)
        cityId = Location.getLocCityId(loc, self.hliData.analyseCheckIn.dictCity)

        print "loc:%s" % loc.toString()
        print "cityId:%s" % cityId

        return cityId

    @classmethod
    def load_data_home_loc_avg(cls):
        fileHomeLoc = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.folderRatio, Config.methodAvg + Config.fileHomeLoc)
        #homeLocAvgList = FileTool.ReadFileColumnList(fileHomeLoc)
        #return homeLocAvgList
        dictUser = User.loadDictUserFromFile(fileHomeLoc)
        return dictUser