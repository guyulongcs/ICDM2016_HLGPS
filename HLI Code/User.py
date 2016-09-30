from os.path import join
from Config import *

from Tool import FileTool
from Tool.FileTool import *
from Tool.InOut import *


from Tool.GeoCoder import *
class User():

    userColCnt = 3
    def __init__(self, id="", lat=0, lon=0, inf=0):
        self.id = id
        self.latitude = lat
        self.longitude = lon
        self.influence = inf

    @classmethod
    def user_to_loc(cls, user):
        loc = GeoLoc(user.latitude, user.longitude)
        return loc

    @classmethod
    def cal_user_distance(cls, u1, u2):
        #InOut.console_func_begin("cal_user_distance")


        loc1 = User.user_to_loc(u1)
        loc2 = User.user_to_loc(u2)
        dis = GeoCoder.cal_loc_distance(loc1, loc2)
        return dis

    @classmethod
    def cal_loc_distance_euclidean(cls, u1, u2):
        loc1 = User.user_to_loc(u1)
        loc2 = User.user_to_loc(u2)
        dis = GeoCoder.cal_loc_distance_euclidean(loc1, loc2)
        return dis

    @classmethod
    def read_user_from_list(cls, list):
        user = None
        if(len(list) == User.userColCnt):
            id = list[0]
            latitude = TypeTool.str_to_float(list[1])
            longitude = TypeTool.str_to_float(list[2])
            user = User(id, latitude, longitude)
        return user


    @classmethod
    def loadDictUserFromFile(cls, file=""):
        InOut.console_func_begin("User loadDictUserFromFile")

        listLineList = FileTool.ReadListLineListFromFile(file)

        dict = {}
        for listLine in listLineList:
            user = User.read_user_from_list(listLine)
            if(user == None):
                continue
            dict[user.id] = user
        return dict



