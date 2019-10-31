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
from HLIAvg import *
import random

class HLIInfluenceGlobal():
    def __init__(self, hliData):
        self.hliData = hliData
        self.hliData.init_predict_data()

        pass

    def home_loc_identify_predict_influenceGlobal(self):
        resList = self.home_loc_identify_method_influenceGlobal()
        fileHomeLoc = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.methodInfluenceGlobal + Config.fileHomeLoc)
        FileTool.WriteStrListToFileWithNewLine(resList, fileHomeLoc)

    def home_loc_identify_method_influenceGlobal(self):
        InOut.console_func_begin("home_loc_identify_method_influenceGlobal")

        predictList = []

        #initial

        #self.init_user_home_location()
        self.init_predict_data()


        #iteration
        iterOutMax = 3
        iterInnerMax = 3
        iterOut = 0
        iterInner = 0

        #outter iteration
        while(True):
            diffAvgInfUser = self.update_influence_user()
            diffAvgInfVenue = self.update_influence_venue()

            #innter iteration
            iterInner = 0
            while(True):
                self.cal_loc_new_user()
                disAvg = self.update_loc_new_user()
                iterInner += 1

                print "\niterOut: %d, iterInner: %d" % (iterOut, iterInner)
                print "diffAvgInfUser: %f, diffAvgInfVenue: %f, disAvg: %f" % (diffAvgInfUser, diffAvgInfVenue, disAvg)

                if(iterInner >= iterInnerMax and self.is_converage_loc(disAvg)):
                #if(iterInner >= iterInnerMax):
                    break
            #
            #self.update_loc_new_user()
            iterOut += 1
            #if(iterOut >= iterOutMax and self.is_converage_inf_user(diffAvgInfUser)):
            if(iterOut >= iterOutMax):
                break

        #


        #get result
        resList = self.home_loc_identify_method_influenceGlobal_get_result()
        return resList

    def home_loc_identify_method_influenceGlobal_get_result(self):
        resList = []
        for user_id in self.hliData.setUserNotKnowHome:
            user = self.hliData.dictUserRes[user_id]
            loc = Location(user.latitude, user.longitude)
            line = user_id + "\t" + str(loc.latitude) + "\t" + str(loc.longitude)
            resList.append(line)
        return resList

    def init_predict_data(self):
        self.init_user_home_loc()
        self.init_venue_userList()

    def init_user_home_loc(self):
        for user_id in self.hliData.setUserNotKnowHome:
            loc = Location()
            flag = False
            if(user_id in self.hliData.dictUserCheckin):
                (flag, loc) = HLIAvg.get_loc_avg_from_user_checkinList(self.hliData, user_id)
            if(flag == False):
                (flag, loc) = HLIAvg.get_loc_avg_from_user_friend(self.hliData, user_id)
            if(flag == False):
                loc = Location.get_loc_random()
            self.hliData.dictUserRes[user_id] = User(user_id, loc.latitude, loc.longitude)
            self.hliData.dictUserResNew[user_id] = User(user_id, loc.latitude, loc.longitude)

    def is_converage_loc(self, disAvg):

        return disAvg <= Config.threshold_coverage_disAvg

    def is_converage_inf_user(self, diffInfUser):

        return diffInfUser <= Config.threshold_coverage_diffInfUser


    def init_venue_userList(self):
        self.hliData.dictVenueUserset = {}
        for user_id in self.hliData.dictUserCheckinUseVenueLoc:
            checkin_list = self.hliData.dictUserCheckinUseVenueLoc[user_id]
            for checkin in checkin_list:
                ProcessTool.dictStrListStr_add_str_str(self.hliData.dictVenueUserlist, checkin.venue_id, user_id)

        pass

    def init_user_home_location(self):
        self.hliData.dictUserKnowHomeLoc = {}
        self.dictUserNotKnowHomeLoc = {}
        self.init_user_know_home_location()
        self.init_user_not_know_home_location()

    def init_user_know_home_location(self):
        for user_id in self.hliData.setUserKnowHome:
            self.hliData.dictUserKnowHomeLoc[user_id] = self.hliData.dictUserLoc[user_id]

    def init_user_not_know_home_location(self):
        for user_id in self.hliData.setUserNotKnowHome:
            loc = Location()
            flag = False
            if(user_id in self.hliData.dictUserCheckin):
                (flag, loc) = HLIAvg.get_loc_avg_from_user_checkinList(self.hliData, user_id)
            if(flag == False):
                (flag, loc) = HLIAvg.get_loc_avg_from_user_friend(self.hliData, user_id)
            if(flag == False):
                loc = Location.get_loc_random()
            self.hliData.dictUserNotKnowHomeLoc[user_id] = loc

    def update_influence_user(self):
        count = 0
        sumDiff = 0.0
        avgDiff = 0.0
        for user_id in self.hliData.dictUserRes:
            sum = 0.0
            if(user_id in self.hliData.dictFriend):
                friend_id_list = self.hliData.dictFriend[user_id]

                if(len(friend_id_list) > 0):
                    for friend_id in friend_id_list:
                        dis = self.cal_user_distance_euclidean(user_id, friend_id)
                        sum += dis
                    influence = sum / (2*len(friend_id_list))

                    count += 1
                    sumDiff += self.cal_influcence_diff(self.hliData.dictUserRes[user_id].influence, influence)
                    self.hliData.dictUserRes[user_id].influence = influence

        avgDiff = sumDiff / (float)(count)
        return avgDiff

        pass

    def cal_influcence_diff(self, inf1, inf2):
        return math.fabs(inf1-inf2)

    def cal_user_distance_euclidean(self, user_id1, user_id2):
        user1 = self.hliData.dictUserRes[user_id1]
        user2 = self.hliData.dictUserRes[user_id2]
        dis = User.cal_loc_distance_euclidean(user1, user2)
        return dis

    def cal_user_venue_distance(self, user_id1, venue_id1):
        user1 = self.hliData.dictUserRes[user_id1]
        venue1 = self.hliData.dictVenueRes[venue_id1]
        loc1 = Location(user1.latitude, user1.longitude)
        loc2 = Location(venue1.latitude, venue1.longitude)
        dis = Location.cal_loc_distance_euclidean(loc1, loc2)
        return dis



    def update_influence_venue(self):
        count = 0
        sumDiff = 0.0
        avgDiff = 0.0
        for venue_id in self.hliData.dictVenueUserlist:
            sum = 0.0
            userlist = self.hliData.dictVenueUserlist[venue_id]
            if(len(userlist) > 0):
                for user_id in userlist:
                    dis = self.cal_user_venue_distance(user_id, venue_id)
                    sum += dis
                influence = sum / (2*len(userlist))

                count += 1
                sumDiff += self.cal_influcence_diff(self.hliData.dictVenueRes[venue_id].influence, influence)
                self.hliData.dictVenueRes[venue_id].influence = influence

        avgDiff = sumDiff / (float)(count)
        return avgDiff
        pass

    def isValidNumerator(self, num):
        threshold = 0.0001
        return (num >= threshold)



    def cal_loc_new_user(self):
        for user_id in self.hliData.setUserNotKnowHome:

            sum1_lat = 0.0
            sum1_lon = 0.0
            influence1 = 0.0
            sum3_lat = 0.0
            sum3_lon = 0.0
            influence3 = 0.0



            if(user_id in self.hliData.dictFriend):
                friend_id_list = self.hliData.dictFriend[user_id]

                if(len(friend_id_list) > 0):
                    for friend_id in friend_id_list:
                        user = self.hliData.dictUserRes[friend_id]
                        if(self.isValidNumerator(user.influence)):
                            sum1_lat += user.latitude / user.influence
                            sum1_lon += user.longitude / user.influence

                            influence1 += (1 / user.influence)

            if(user_id in self.hliData.dictUserCheckinUseVenueLoc):
                checkin_list = self.hliData.dictUserCheckinUseVenueLoc[user_id]

                if(len(checkin_list) > 0):
                    for checkin in checkin_list:
                        venue_id = checkin.venue_id
                        venue = self.hliData.dictVenueRes[venue_id]

                        if(self.isValidNumerator(venue.influence)):
                            sum3_lat += venue.latitude / venue.influence
                            sum3_lon += venue.longitude / venue.influence

                            influence3 += (1 / venue.influence)


            frac_lat = sum1_lat + sum3_lat
            frac_lon = sum1_lon + sum3_lon
            numerator = influence1 + influence3


            if(self.isValidNumerator(numerator)):
                latNew = frac_lat / numerator
                lonNew = frac_lon / numerator
                user = self.hliData.dictUserRes[user_id]
                self.hliData.dictUserResNew[user_id].latitude = latNew
                self.hliData.dictUserResNew[user_id].longitude = lonNew
        pass


    def update_loc_new_user(self):
        disSum = 0
        for user_id in self.hliData.dictUserResNew:
            dis = User.cal_user_distance(self.hliData.dictUserRes[user_id], self.hliData.dictUserResNew[user_id])
            disSum += dis
            self.hliData.dictUserRes[user_id].latitude = self.hliData.dictUserResNew[user_id].latitude
            self.hliData.dictUserRes[user_id].longitude = self.hliData.dictUserResNew[user_id].longitude
        disAvg = disSum / (float)(len(self.hliData.dictUserResNew))
        return disAvg
        pass

    @classmethod
    def load_data_home_loc_influenceGlobal(cls):
        fileHomeLoc = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.folderRatio,  Config.methodInfluenceGlobal + Config.fileHomeLoc)
        dictUser = User.loadDictUserFromFile(fileHomeLoc)
        return dictUser