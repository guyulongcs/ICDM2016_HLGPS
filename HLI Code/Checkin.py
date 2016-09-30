__author__ = 'guyulong'

from Tool import  FormatTool
from Tool.FormatTool import *
from Location import *
from Tool.TimeTool import *

class Checkin():
    def __init__(self):
        self.id = 0
        self.user_id = ""
        self.venue_id = 0
        self.latitude = 0.0
        self.longitude = 0.0
        self.created_at = ""

    def SetValue(self, list):
        id = list[0]
        uid = list[1]
        vid = list[2]
        lat = list[3]
        lon = list[4]
        created_at = list[5]
        self.id = FormatTool.intStrToInt(id)
        #self.user_id = FormatTool.intStrToInt(uid)
        self.user_id = uid
        self.venue_id = FormatTool.intStrToInt(vid)
        self.latitude = FormatTool.float_str_to_float(lat)
        self.longitude = FormatTool.float_str_to_float(lon)
        self.created_at = created_at

    @classmethod
    def get_avg_loc(cls, checkInList):
        locList = Checkin.format_list_checkin_to_location(checkInList)
        loc = Location.get_avg_loc(locList)
        return loc


    @classmethod
    def format_checkin_to_location(cls, checkIn):
        loc = Location()
        loc.latitude = checkIn.latitude
        loc.longitude = checkIn.longitude
        return loc

    @classmethod
    def format_list_checkin_to_location(cls, checkInList):
        locList = []
        for checkIn in checkInList:
            loc = Checkin.format_checkin_to_location(checkIn)
            locList.append(loc)
        return locList

    @classmethod
    def format_list_checkin_to_geoLoc(cls, checkInList):
        locList = Checkin.format_list_checkin_to_location(checkInList)
        geoLocList = Location.format_list_location_to_geoloc(locList)
        return geoLocList

    def toString(self):
        res = ""
        res = "%f, %f" % (self.latitude, self.longitude)
        return res

    @classmethod
    def loadCheckinFromFile(cls, file):
        listCheckin = []
        lines = FileTool.FileTool.ReadLineListFromFile(file)

        for line in lines:
            list = line.split("\t")

            if(len(list) != Config.fileCheckinColNum):
                continue

            checkIn = Checkin()
            checkIn.SetValue(list)

            listCheckin.append(checkIn)

        return listCheckin

    @classmethod
    def filt_checkin_in_night(cls, checkinList):
        resList = []
        for checkin in checkinList:
            if(Checkin.is_checkin_in_night(checkin)):
                resList.append(checkin)
        return resList

    @classmethod
    def is_checkin_in_night(cls, checkin):
        flag = False
        t = checkin.created_at
        dt = TimeTool.get_datetime_from_str(t)
        hour = dt.hour
        if(hour >= 20 or hour < 8):
            flag = True

        return flag