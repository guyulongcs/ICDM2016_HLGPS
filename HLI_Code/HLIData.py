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
import numpy as np
import random

class HLIData():
    def __init__(self):
        #data
        self.folder = Config.folderDataParsed
        self.dictCheckinUserCheckinList = {}
        self.dictUser = {}
        self.dictUserCity = {}
        self.dictUserCheckinCity = {}
        self.dictUserCheckin = {}
        #self.dictCity = GeoMap.load_city_dict()
        self.analyseCheckIn = AnalyseCheckin()

        #config

        self.flagExp = Config.flagExp
        self.flagRatio = Config.flagRatio
        self.flagCheckinLocUseVenueLoc = Config.flagCheckinLocUseVenueLoc

        #exp data
        self.userList = []
        self.userKnowHomeList = []
        self.userNotKnowHomeList = []

        #procedure
        self.setLocationBroadKnowUser = set()
        self.dictIteratorUser = {}

        #res
        self.dictUserKnowHomeLoc = {}
        self.dictUserNotKnowHomeLoc = {}
        self.dictUserRes = {}
        self.dictUserResNew = {}
        self.dictVenueUserlist = {}
        self.dictVenueUserlistCheck = {}
        self.dictVenueUserlistRating = {}



        self.timerTool = TimerTool()
        pass

    def load_data(self):
        InOut.console_func_begin("load_data")
        self.load_data_user_info()
        self.dictVenue = LoadData.load_dict_venue()
        self.dictUserCheckin = LoadData.load_dict_user_checkin(self.dictVenue, False, self.flagExp)
        self.dictUserCheckinUseVenueLoc = LoadData.load_dict_user_checkin(self.dictVenue, True, self.flagExp)
        self.dictUserRating = LoadData.load_dict_user_rating(self.dictVenue, self.flagExp)
        self.dictFriend = LoadData.load_dict_friend(self.flagExp, False)

        print "dictUserCheckin:", len(self.dictUserCheckin)
        print "dictUserRating:", len(self.dictUserRating)

        self.setUserHasCheckin = set(self.dictUserCheckin.keys())
        self.setUserNotHasCheckin = self.setUser - self.setUserHasCheckin

        print "setUser:", len(self.setUser)
        print "setUserKnowHome:", len(self.setUserKnowHome)
        print "setUserNotKnowHome:", len(self.setUserNotKnowHome)

        print "setUserHasCheckin:", len(self.setUserHasCheckin)
        print "setUserNotHasCheckin:", len(self.setUserNotHasCheckin)

        self.setUserNotKnowHomeHasCheckin = self.setUserNotKnowHome & self.setUserHasCheckin
        print "setUserNotKnowHomeHasCheckin:", len(self.setUserNotKnowHomeHasCheckin)

        self.setUserHasRating = set(self.dictUserRating.keys())
        print "setUserHasRating:", len(self.setUserHasRating)
        self.setUserNotKnowHomeHasRating = self.setUserNotKnowHome & self.setUserHasRating
        print "setUserNotKnowHomeHasRating:", len(self.setUserNotKnowHomeHasRating)

        self.setUserNotHasCheckinHasRating = self.setUserHasRating - self.setUserHasCheckin
        print "setUserNotHasCheckinHasRating:", len(self.setUserNotHasCheckinHasRating)

        ratio = len(self.setUserNotKnowHomeHasCheckin) / (float)(len(self.setUserNotKnowHome))
        print "ratio:", ratio

        print "dictUser:", len(self.dictUser)
        print "dictUserCity:", len(self.dictUserCity)
        print "dictUserCheckin:", len(self.dictUserCheckin)
        print "dictUserCheckinUseVenueLoc:", len(self.dictUserCheckinUseVenueLoc)
        print "dictUserRating:", len(self.dictUserRating)
        print "dictFriend:", len(self.dictFriend)

    def init_predict_data(self):
        #user
        self.dictUserRes = {}
        for user_id in self.setUserKnowHome:
            self.dictUserRes[user_id] = self.dictUser[user_id]
        for user_id in self.setUserNotKnowHome:
            self.dictUserRes[user_id] = User(user_id)


        #venue
        self.dictVenueRes = {}
        for venue_id in self.dictVenue:
            self.dictVenueRes[venue_id] = self.dictVenue[venue_id]

    def load_data_user_info(self):
        self.load_data_user_set()
        self.load_data_userCity()
        self.load_data_user()

    def load_data_user_set(self):
        self.setUser = LoadData.load_set_alluser(self.flagExp, self.flagRatio)
        self.setUserKnowHome = LoadData.load_set_userKnowHome()
        self.setUserNotKnowHome = self.setUser - self.setUserKnowHome
        #self.setUserHasCheckin = LoadData.load_set_userHasCheckin()


        #self.setUserNotHasCheckin = self.setUser - self.setUserHasCheckin


    def load_data_userCity(self):
         self.dictUserCity = LoadData.load_dict_user_city(self.flagExp, self.flagRatio)

    def load_data_user(self):
        self.dictUser = LoadData.load_dict_user()

    def load_data_userLoc(self):
        self.dictUserLoc = LoadData.load_dict_user_loc()
        self.load_data_user_know_home_Loc()

    def load_data_user_know_home_Loc(self):
        for user_id in self.setUserKnowHome:
            self.dictUserKnowHomeLoc[user_id] = self.dictUserLoc[user_id]



    def home_loc_identify_get_exp_data(self):
        self.home_loc_write_true_loc_list()
        #self.userList = self.dictUserCheckin.keys()
        self.userList = self.setUserNotKnowHome
        return

        #user list
        #self.userList = list(self.setUserHasCheckin)
        #maxUserCnt = 100
        #self.userList = ProcessTool.get_list_str_sub_n(self.userList, maxUserCnt)
        #self.userSet = ProcessTool.list_to_set(self.userList)


        self.homeLocTrueList = self.home_loc_get_true_list(self.userList)
        print "homeLocTrueList:", len(self.homeLocTrueList)

        fileHomeLocTrue = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.folderRatio, Config.fileTrue + Config.fileHomeLoc)
        FileTool.WriteStrListToFileWithNewLine(self.homeLocTrueList, fileHomeLocTrue)

        #filt data

    def home_loc_write_true_loc_list(self):
        resList = self.home_loc_get_true_loc_list()
        fileHomeLocTrue = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.folderRatio, Config.fileTrue + Config.fileHomeLoc)
        FileTool.WriteStrListToFileWithNewLine(resList, fileHomeLocTrue)


    def home_loc_get_true_loc_list(self):
        resList = []
        for user_id in self.setUserNotKnowHome:
            user = self.dictUser[user_id]
            loc = Location(user.latitude, user.longitude)
            line = user_id + "\t" + str(loc.latitude) + "\t" + str(loc.longitude)
            resList.append(line)
        return resList

        pass

    #get ture home loc of user
    def home_loc_get_true_list(self, userList):
        list = []
        for user in userList:
            cityId = "-1"
            if(self.dictUserCity.has_key(user)):
                cityId = self.dictUserCity[user]
            else:
                InOut.except_info("dictUserCity not has user")
            list.append(cityId)
        return list
