__author__ = 'guyulong'


import Tool.FileTool
import Tool.InOut
from Tool import ProcessTool
from Tool import Evaluation
from Tool.InOut import *
from Tool.FileTool import *
from Tool.ProcessTool import *
from Tool.Evaluation import *
from Config import *
from Venue import *
from Checkin import *
from Rating import *
from User import *
from Location import *

from AnalyseCheckin import *
from Edge import *

class LoadData():
    def __init__(self):
        pass

    @classmethod
    def load_set_alluser(cls, flagExp=True, flagRatio = True):
        res = []
        if(flagExp):
            file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileUserSet)
            if(flagRatio == True):
                file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileUserSet)
            res = FileTool.ReadFileColumnSet(file)

        return res

    @classmethod
    def load_set_user(cls):
        res = set()
        file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileUserSet)
        fileFriend = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileSocialGraph)
        res1 = FileTool.ReadFileColumnSet(file)
        res2 = FileTool.ReadFileColumnSet(fileFriend)
        res = res2
        return res


    @classmethod
    def load_set_userKnowHome(cls):
        file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileKnowHome + Config.fileUserSet)
        res = FileTool.ReadFileColumnSet(file)
        return res

    @classmethod
    def load_set_userNotKnowHome(cls):
        file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileNot + Config.fileKnowHome + Config.fileUserSet)
        res = FileTool.ReadFileColumnSet(file)
        return res

    @classmethod
    def load_set_userHasCheckin(cls):
        file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileHasCheckin + Config.fileUserSet)
        res = FileTool.ReadFileColumnSet(file)
        return res


    @classmethod
    def load_set_checkuser(cls, flagExp = True):
        res = []
        if(flagExp):
            file = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.fileFlagCheck + Config.fileUserSet)
            res = FileTool.ReadFileColumnSet(file)
        return res

    @classmethod
    def load_dict_filt_user(cls):
        res = {}
        res = {}

        file = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileUser)
        res = User.loadDictUserFromFile(file)
        return res

    @classmethod
    def load_dict_checkuser(cls, flagExp = True):
        InOut.console_func_begin("load_dict_checkuser")
        res = {}
        if(flagExp):
            file = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.fileFlagCheck + Config.fileUser)
            res = User.loadDictUserFromFile(file)
        return res

    @classmethod
    def load_dict_user(cls):
        InOut.console_func_begin("load_dict_user")

        #dict user: user_id => user
        res = {}
        file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileUser)
        res = User.loadDictUserFromFile(file)
        return res

    @classmethod
    def load_dict_user_loc(cls):
        InOut.console_func_begin("load_dict_user_loc")

        res = LoadData.load_dict_user()

        #dict user location: user_id => location
        res2 = {}
        for user_id in res:
            user = res[user_id]
            loc = Location(user.latitude, user.longitude)
            res2[user_id] = loc

        return res2


    @classmethod
    def load_dict_friend(cls, flagExp = True, flagAsc = False):
        InOut.console_func_begin("load_dict_friend")
        res = {}
        file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileSocialGraph)
        res = LoadData.load_dict_friend_file(file, flagAsc)
        return res

    @classmethod
    def load_dict_filt_friend(cls, flagExp = True, flagAsc=False):
        res = {}
        if(flagExp):
            file = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileSocialGraph)

            res = LoadData.load_dict_friend_file(file, flagAsc)
        return res


    @classmethod
    def load_dict_friend_file(cls, file, flagAsc=False):
        #res = Edge.loadDictEdgeFromFile(file)
        #res = Edge.dictEdge_undirected_remove_duplicate(res)

        res = Edge.loadDictEdgeFromFile(file, flagAsc)
        return res



    @classmethod
    def load_dict_user_city(cls, flagExp = True, flagRatio=True):
        InOut.console_func_begin("load_dict_user_city")
        dictUserCity = {}
        if(flagExp):
            file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileUserCity)
            if(flagRatio):
                file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileUserCity)
            dictUserCity = FileTool.ReadFileDictStrStr(file, 0, 1)
        return dictUserCity

    @classmethod
    def load_dict_user_checkin(cls, dictVenue, flagCheckinLocUseVenueLoc=False, flagExp=True):
        InOut.console_func_begin("load_dict_user_checkin")
        dictUserCheckin = {}
        fileCheckin = ""

        fileCheckin = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileCheckin)
        listCheckin = Checkin.loadCheckinFromFile(fileCheckin)

        print "listCheckin:", len(listCheckin)

        if(flagCheckinLocUseVenueLoc):
            listCheckin = LoadData.replace_checkin_loc_use_venue(listCheckin, dictVenue)


        for checkin in listCheckin:
            uid = checkin.user_id
            if(uid not in dictUserCheckin):
                dictUserCheckin[uid] = []
            dictUserCheckin[uid].append(checkin)

        return dictUserCheckin

    @classmethod
    def load_dict_user_rating(cls, dictVenue, flagExp=True):
        InOut.console_func_begin("load_dict_user_rating")
        dictUserRating = {}

        fileRating = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileRating)
        listRating = Rating.loadRatingFromFile(fileRating)

        print "listRating:", len(listRating)

        for rating in listRating:
            uid = rating.user_id
            vid = rating.venue_id
            if(vid not in dictVenue):
                continue
            if(uid not in dictUserRating):
                dictUserRating[uid] = []
            rating.latitude = dictVenue[vid].latitude
            rating.longitude = dictVenue[vid].longitude
            dictUserRating[uid].append(rating)

        return dictUserRating

    @classmethod
    def load_dict_venue(cls, flagExp = True, flagRatio=True):
        InOut.console_func_begin("load_dict_venue")
        fileVenue = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileVenue)
        dictVenue = Venue.loadDictVenueFromNormFile(fileVenue)
        return dictVenue

    @classmethod
    #use lat, lon in venue for checkin
    def replace_checkin_loc_use_venue(cls, listCheckin, dictVenue):
        fileVenue = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileVenue)
        #dictVenue = Venue.loadDictVenueFromNormFile(fileVenue)

        resList = []
        for checkin in listCheckin:
            venueid = checkin.venue_id
            if(venueid in dictVenue):
                checkin.latitude = dictVenue[venueid].latitude
                checkin.longitude = dictVenue[venueid].longitude
            resList.append(checkin)

        return resList
