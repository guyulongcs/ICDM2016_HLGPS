__author__ = 'guyulong'

from Tool import  FormatTool
from Tool.FormatTool import *
from Location import *
from Tool.TimeTool import *

class Rating():
    def __init__(self):
        self.user_id = ""
        self.venue_id = 0
        self.score = 0
        #add
        self.latitude = 0.0
        self.longitude = 0.0

    def SetValue(self, list):
        uid = list[0]
        vid = list[1]
        score = list[2]
        self.user_id = uid
        self.venue_id = FormatTool.intStrToInt(vid)
        self.score = FormatTool.intStrToInt(score)

    @classmethod
    def loadRatingFromFile(cls, file):
        listRating = []
        lines = FileTool.FileTool.ReadLineListFromFile(file)

        for line in lines:
            list = line.split("\t")

            if(len(list) != Config.fileRatingColNum):
                continue

            rating = Rating()
            rating.SetValue(list)

            listRating.append(rating)

        return listRating

    @classmethod
    def format_list_rating_to_location(cls, ratingList):
        locList = []
        for checkIn in ratingList:
            loc = Rating.format_rating_to_location(checkIn)
            locList.append(loc)
        return locList

    @classmethod
    def format_rating_to_location(cls, rating):
        loc = Location()
        loc.latitude = rating.latitude
        loc.longitude = rating.longitude
        return loc