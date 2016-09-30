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
from HLIClustering import *
import random

class HLITrust():
    def __init__(self, hliData):
        self.hliData = hliData
        self.hliData.init_predict_data()

        pass

    def home_loc_identify_predict_trust(self):
        resList = self.home_loc_identify_method_trust()
        fileHomeLoc = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.methodTrust + Config.fileHomeLoc)
        FileTool.WriteStrListToFileWithNewLine(resList, fileHomeLoc)

    def home_loc_identify_method_trust(self):
        InOut.console_func_begin("home_loc_identify_method_trust")

        predictList = []

        #initial

        #self.init_user_home_location()
        self.init_predict_data()

        #iteration
        iterOutMax = Config.trust_iterOutMax
        iterInnerMax = Config.trust_iterInnerMax
        iterOut = 0
        iterInner = 0

        self.hliData.m_iteration_number = 0
        #outter iteration
        iterCnt = 0
        while(True):
            print "outter iteration..."
            diffAvgInfUser = self.update_influence_user()
            diffAvgInfVenue = self.update_influence_venue()

            #innter iteration
            iterInner = 0

            while(True):
                print "innter iteration..."
                iterCnt += 1
                print "\niterOut: %d, iterInner: %d" % (iterOut, iterInner)

                self.hliData.setLocationBroadKnowUserNew = set()
                self.hliData.m_iteration_number += 1

                self.update_trust()
                self.cal_loc_new_user()

                print "old broad: ", len(self.hliData.setLocationBroadKnowUser)
                self.hliData.setLocationBroadKnowUser = self.hliData.setLocationBroadKnowUser | self.hliData.setLocationBroadKnowUserNew

                print "new broad: ", len(self.hliData.setLocationBroadKnowUserNew)
                print "all broad: ", len(self.hliData.setLocationBroadKnowUser)
                disAvg = self.update_loc_new_user()
                iterInner += 1

                print "diffAvgInfUser: %f, diffAvgInfVenue: %f, disAvg: %f" % (diffAvgInfUser, diffAvgInfVenue, disAvg)

                #if(iterInner >= iterInnerMax and self.is_converage_loc(disAvg)):
                if(iterInner >= iterInnerMax):
                    break

            #
            #self.update_loc_new_user()
            iterOut += 1
            #if(iterOut >= iterOutMax and self.is_converage_inf_user(diffAvgInfUser)):
            if(iterOut >= iterOutMax):
                break

        #get result
        resList = self.home_loc_identify_method_get_result()
        return resList


    def update_trust(self):
        for user_id in self.hliData.dictUser:
            #self.hliData.dictTrustUser[user_id] *= Config.r_trust_iteration_alpha
            alpha = Config.r_trust_iteration_alpha
            iter = self.hliData.dictIteratorUser[user_id]
            self.hliData.dictTrustUser[user_id] = alpha ** iter
            self.hliData.dictTrustUser[user_id] = 1
        pass

    def home_loc_identify_method_get_result(self):
        resList = []
        for user_id in self.hliData.setUserNotKnowHome:
            user = self.hliData.dictUserRes[user_id]
            loc = Location(user.latitude, user.longitude)
            line = user_id + "\t" + str(loc.latitude) + "\t" + str(loc.longitude)
            resList.append(line)
        return resList

    def init_predict_data(self):
        InOut.console_func_begin("init_predict_data")
        self.init_user_home_loc()
        self.init_venue_userList()
        self.init_trust()
        InOut.console_func_end("init_predict_data")

    def init_user_home_loc(self):
        InOut.console_func_begin("init_user_home_loc")
        self.hliData.setLocationBroadKnowUser = set()
        self.hliData.dictIteratorUser = {}

        for user_id in self.hliData.dictUser:
            self.hliData.dictIteratorUser[user_id] = 0

        for user_id in self.hliData.setUserKnowHome:
            self.hliData.setLocationBroadKnowUser.add(user_id)

        for user_id in self.hliData.setUserNotKnowHome:
            loc = Location()
            flag = False
            if(user_id in self.hliData.dictUserCheckin):
                if(Config.flag_method_trust_update_loc_user_has_checkin_use_rating == False):
                    (flag, loc) = HLIClustering.get_loc_cluster_from_user_checkinList(self.hliData, user_id)
                else:
                    (flag, loc) = HLIClustering.get_loc_cluster_from_user_checkinList_ratingList(self.hliData, user_id)
                #print "user_id:", user_id
                #print flag
                #print loc.toString()
            if(Config.flag_method_trust_init_rating_user_loc and (user_id not in self.hliData.dictUserCheckin) and (user_id in self.hliData.dictUserRating)):
                (flag, loc) = HLIClustering.get_loc_cluster_from_user_checkinList_ratingList(self.hliData, user_id)
            #if(flag == False):
            #    (flag, loc) = HLIAvg.get_loc_avg_from_user_friend(self.hliData, user_id)
            if(flag == False):
                loc = Location.get_loc_random()
            self.hliData.dictUserRes[user_id] = User(user_id, loc.latitude, loc.longitude)
            self.hliData.dictUserResNew[user_id] = User(user_id, loc.latitude, loc.longitude)



    def init_trust(self):
        InOut.console_func_begin("init_trust")
        #self.init_trust_friend()
        self.init_trust_user()
        InOut.console_func_end("init_trust")

    def init_trust_friend(self):
        InOut.console_func_begin("init_trust_friend")
        self.hliData.dictTrustCfriend = {}
        for user_id in self.hliData.dictFriend:
            #if(user_id in self.hliData.dictTrustCfriend):
            #    continue
            friend_id_set = self.hliData.dictFriend[user_id]
            for friend_id in friend_id_set:
                if(friend_id in self.hliData.dictFriend):
                    f_set = self.hliData.dictFriend[friend_id]
                    coef = self.cal_set_jaccard(friend_id_set, f_set)
                    ProcessTool.dictStrDictStrValue_add_str_str_str( self.hliData.dictTrustCfriend, user_id, friend_id, coef)
                    #ProcessTool.dictStrDictStrValue_add_str_str_str( self.hliData.dictTrustCfriend, friend_id, user_id, coef)
        InOut.console_func_end("init_trust_friend")
        pass

    def get_trust_friend(self, user_id1, user_id2):
        coef = 1
        if(Config.flag_method_trust_coef):
            #return self.hliData.dictTrustCfriend[user_id1][user_id2]
            set1 = self.hliData.dictFriend[user_id1]
            set2 = self.hliData.dictFriend[user_id2]
            if(Config.flag_method_trust_coef_jaccard):
                coef = self.cal_set_jaccard(set1, set2)
            if(Config.flag_method_trust_coef_sigmoid):
                coef = self.cal_set_sigmoid(set1 & set2)
        return coef

    def cal_set_sigmoid(self, set):
        n = len(set)
        res = ProcessTool.sigmoid(n)
        return res



    def init_trust_user(self):
        InOut.console_func_begin("init_trust_user")
        self.hliData.dictTrustUser = {}

        for user_id in self.hliData.dictUser:
            self.hliData.dictTrustUser[user_id] = 1

        InOut.console_func_end("init_trust_user")

    def cal_set_jaccard(self, set1, set2):
        res = 0
        sjoin = set1 & set2
        sunion = set1 | set2
        res = (len(sjoin)+1) / (float)(len(sunion)+1)
        return res

    def is_converage_loc(self, disAvg):
        return disAvg <= Config.threshold_coverage_disAvg

    def is_converage_inf_user(self, diffInfUser):
        return diffInfUser <= Config.threshold_coverage_diffInfUser

    def init_venue_userList(self):
        self.hliData.dictVenueUserset = {}
        for user_id in self.hliData.dictUserCheckin:
            checkin_list = self.hliData.dictUserCheckin[user_id]
            for checkin in checkin_list:
                ProcessTool.dictStrListStr_add_str_str(self.hliData.dictVenueUserlist, checkin.venue_id, user_id)
                ProcessTool.dictStrListStr_add_str_str(self.hliData.dictVenueUserlistCheck, checkin.venue_id, user_id)

        if(Config.flag_trust_use_rating):
            for user_id in self.hliData.dictUserRating:
                rating_list = self.hliData.dictUserRating[user_id]
                for rating in rating_list:
                    ProcessTool.dictStrListStr_add_str_str(self.hliData.dictVenueUserlist, rating.venue_id, user_id)
                    ProcessTool.dictStrListStr_add_str_str(self.hliData.dictVenueUserlistRating, rating.venue_id, user_id)
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
                #(flag, loc) = HLIAvg.get_loc_avg_from_user_checkinList(self.hliData, user_id)
                (flag, loc) = HLIClustering.get_loc_cluster_from_user_checkinList(self.hliData, user_id)

            #if(flag == False):
            #    (flag, loc) = HLIAvg.get_loc_avg_from_user_friend(self.hliData, user_id)
            if(flag == False):
                loc = Location.get_loc_random()
            self.hliData.dictUserNotKnowHomeLoc[user_id] = loc

    def update_influence_user(self):
        InOut.console_func_begin("update_influence_user")
        count = 0
        sumDiff = 0.0
        avgDiff = 0.0
        list = self.hliData.dictUserRes.keys()
        if(Config.flag_method_trust_broadcast):
            list = self.hliData.setLocationBroadKnowUser
        for user_id in list:
            sum = 0.0
            if(user_id in self.hliData.dictFriend):
                friend_id_list = self.hliData.dictFriend[user_id]
                friend_id_list = self.filt_user_by_broadknowhome_userset(friend_id_list)

                if(len(friend_id_list) > 0):
                    for friend_id in friend_id_list:
                        dis = self.cal_user_distance_euclidean(user_id, friend_id)
                        #trust1 = self.hliData.dictTrustCfriend[user_id][friend_id]
                        trust1 = self.get_trust_friend(user_id, friend_id)
                        trust = trust1 * self.hliData.dictTrustUser[friend_id]

                        #dis = trust * dis
                        #print "trust: ", trust
                        #print "dis: ", dis

                        sum += dis
                    influence = sum / (2*len(friend_id_list))

                    count += 1
                    sumDiff += self.cal_influcence_diff(self.hliData.dictUserRes[user_id].influence, influence)
                    self.hliData.dictUserRes[user_id].influence = influence

        avgDiff = 0
        if(count > 0):
            avgDiff = sumDiff / (float)(count)

        print "avgDiff: ", avgDiff

        InOut.console_func_end("update_influence_user")
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
        InOut.console_func_begin("update_influence_venue")
        count = 0
        sumDiff = 0.0
        avgDiff = 0.0
        for venue_id in self.hliData.dictVenueUserlist:
            sum = 0.0

            userlist = self.hliData.dictVenueUserlist[venue_id]
            userlist = self.filt_user_by_broadknowhome_userset(userlist)

            if(len(userlist) > 0):
                #check in
                if(venue_id in self.hliData.dictVenueUserlistCheck):
                    userlistCheck = self.hliData.dictVenueUserlistCheck[venue_id]
                    userlistCheck = self.filt_user_by_broadknowhome_userset(userlistCheck)
                    for user_id in userlistCheck:
                        dis = self.cal_user_venue_distance(user_id, venue_id)
                        sum += Config.weight_checkin * dis

                #rating


                if(venue_id in self.hliData.dictVenueUserlistRating):
                    userlistRating = self.hliData.dictVenueUserlistRating[venue_id]
                    userlistRating = self.filt_user_by_broadknowhome_userset(userlistRating)
                    for user_id in userlistRating:
                        dis = self.cal_user_venue_distance(user_id, venue_id)
                        sum += Config.weight_rating * dis


                influence = sum / 2*(Config.weight_checkin*len(userlistCheck) + Config.weight_rating*len(userlistRating))

                count += 1
                sumDiff += self.cal_influcence_diff(self.hliData.dictVenueRes[venue_id].influence, influence)
                self.hliData.dictVenueRes[venue_id].influence = influence

        avgDiff = sumDiff / (float)(count)

        InOut.console_func_end("update_influence_venue")
        return avgDiff
        pass

    def isValidNumerator(self, num):
        threshold = 0.0001
        return (num >= threshold)


    def filt_user_by_broadknowhome_userset(self, friend_id_list):
        res = friend_id_list
        #print type(res)
        #print type(self.hliData.setLocationBroadKnowUser)
        if(Config.flag_method_trust_broadcast):
            res = ProcessTool.filt_liststr_by_set(res, self.hliData.setLocationBroadKnowUser)
        return res

    def filt_checkinuser_by_checkin_userset(self, user_id, friend_id_list):
        res = friend_id_list
        #print type(res)
        #print type(self.hliData.setLocationBroadKnowUser)
        if(Config.flag_method_trust_not_update_loc_user_has_checkin == False):
            if(user_id in self.hliData.setUserHasCheckin):
                res = []
                #res = ProcessTool.filt_liststr_by_set(res, self.hliData.setUserHasCheckin)
        return res


    def cal_loc_new_user(self):
        InOut.console_func_begin("cal_loc_new_user")

        disSum = 0.0
        disCnt = 0
        disAvg = 0.0
        for user_id in self.hliData.setUserNotKnowHome:
            if(Config.flag_method_trust_not_update_loc_user_has_checkin and (user_id in self.hliData.dictUserCheckin)):
                self.hliData.dictUserResNew[user_id].latitude = self.hliData.dictUserRes[user_id].latitude
                self.hliData.dictUserResNew[user_id].longitude = self.hliData.dictUserRes[user_id].longitude
                continue

            sum1_lat = 0.0
            sum1_lon = 0.0
            influence1 = 0.0

            sum3_lat = 0.0
            sum3_lon = 0.0
            influence3 = 0.0

            sum4_lat = 0.0
            sum4_lon = 0.0
            influence4 = 0.0

            flag = user_id in self.hliData.dictFriend
            if(flag):
                if((user_id in self.hliData.setUserHasCheckin) and (Config.flag_method_trust_update_loc_user_has_checkin_use_friend == False)):
                    flag = False
            if(flag):
                friend_id_list = self.hliData.dictFriend[user_id]
                friend_id_list = self.filt_user_by_broadknowhome_userset(friend_id_list)
                friend_id_list = self.filt_checkinuser_by_checkin_userset(user_id,friend_id_list)

                if(len(friend_id_list) > 0):
                    #if(self.hliData.dictIteratorUser[user_id] == 0):
                    #    self.hliData.dictIteratorUser[user_id] += 1
                    for friend_id in friend_id_list:
                        user = self.hliData.dictUserRes[friend_id]
                        if(self.isValidNumerator(user.influence)):
                            trust1 = self.get_trust_friend(user_id, friend_id)
                            #trust1 = self.hliData.dictTrustCfriend[user_id][friend_id]
                            trust = trust1 * self.hliData.dictTrustUser[friend_id]
                            #print "trust:", trust
                            influence = user.influence
                            #influence = influence * trust
                            sum1_lat += Config.weight_friend * user.latitude * trust / influence
                            sum1_lon += Config.weight_friend * user.longitude * trust / influence

                            influence1 += (Config.weight_friend * trust / user.influence)

            if(user_id in self.hliData.dictUserCheckin):
                checkin_list = self.hliData.dictUserCheckin[user_id]

                if(len(checkin_list) > 0):
                    for checkin in checkin_list:
                        venue_id = checkin.venue_id
                        venue = self.hliData.dictVenueRes[venue_id]
                        lat = venue.latitude
                        lon = venue.longitude

                        if(Config.flag_method_trust_use_checkin_loc_real):
                            lat = checkin.latitude
                            lon = checkin.longitude

                        if(self.isValidNumerator(venue.influence)):
                            sum3_lat += Config.weight_checkin * lat / venue.influence
                            sum3_lon += Config.weight_checkin * lon / venue.influence

                            influence3 += (Config.weight_checkin * 1 / venue.influence)

            if(Config.flag_trust_use_rating):
                if(user_id in self.hliData.dictUserRating):
                    rating_list = self.hliData.dictUserRating[user_id]
                    if(len(rating_list) > 0):
                        for rating in rating_list:
                            venue_id = rating.venue_id
                            venue = self.hliData.dictVenueRes[venue_id]
                            if(self.isValidNumerator(venue.influence)):
                                sum4_lat += Config.weight_rating * venue.latitude / venue.influence
                                sum4_lon += Config.weight_rating * venue.longitude / venue.influence

                                influence4 += (Config.weight_rating * 1 / venue.influence)

            frac_lat = sum1_lat + sum3_lat + sum4_lat
            frac_lon = sum1_lon + sum3_lon + sum4_lon
            numerator = influence1 + influence3 + influence4


            if(self.isValidNumerator(numerator)):
                latNew = frac_lat / numerator
                lonNew = frac_lon / numerator
                user = self.hliData.dictUserRes[user_id]
                self.hliData.dictUserResNew[user_id].latitude = latNew
                self.hliData.dictUserResNew[user_id].longitude = lonNew

                dis = User.cal_user_distance(self.hliData.dictUserRes[user_id], self.hliData.dictUserResNew[user_id])
                disSum += dis
                disCnt += 1


                if(user_id not in self.hliData.setLocationBroadKnowUser):
                    #print "user not in broard"
                    self.hliData.setLocationBroadKnowUserNew.add(user_id)
                    self.hliData.dictIteratorUser[user_id] = self.hliData.m_iteration_number
            else:
                self.hliData.dictUserResNew[user_id].latitude =  self.hliData.dictUserRes[user_id].latitude
                self.hliData.dictUserResNew[user_id].longitude = self.hliData.dictUserRes[user_id].longitude

        disAvg = 0
        if(disCnt > 0):
            disAvg = disSum /disCnt
        print "disAvg: ", disAvg

        InOut.console_func_end("cal_loc_new_user")
        pass

    def update_loc_new_user(self):
        InOut.console_func_begin("update_loc_new_user")
        disSum = 0
        for user_id in self.hliData.dictUserResNew:
            u1 = self.hliData.dictUserRes[user_id]
            u2 = self.hliData.dictUserResNew[user_id]
            #print "u1: ", u1.latitude, "\t", u1.longitude
            #print "u2: ", u2.latitude, "\t", u2.longitude
            dis = User.cal_user_distance(self.hliData.dictUserRes[user_id], self.hliData.dictUserResNew[user_id])
            #print "dis:", dis
            disSum += dis
            self.hliData.dictUserRes[user_id].latitude = self.hliData.dictUserResNew[user_id].latitude
            self.hliData.dictUserRes[user_id].longitude = self.hliData.dictUserResNew[user_id].longitude
        disAvg = disSum / (float)(len(self.hliData.dictUserResNew))
        return disAvg
        pass

    @classmethod
    def load_data_home_loc(cls):
        fileHomeLoc = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.folderRatio,  Config.methodTrust + Config.fileHomeLoc)
        dictUser = User.loadDictUserFromFile(fileHomeLoc)
        return dictUser
