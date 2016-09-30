__author__ = 'guyulong'

from os import listdir
from os.path import isfile, join
from Tool import FileTool, InOut
from Tool.InOut import *
from Tool.FileTool import *
from Config import *
from Venue import *
from GeoMap import *
from Location import *

class AnalyseVenue():
    def __init__(self):
        self.listVenue = []
        self.dictLatdictLonCnt = {}
        self.dictCity = {}
        self.fileAnalyseVenue = Config.folderData + Config.folderDataParsed + Config.fileAnalyseVenue

    def start(self):
        InOut.console_func_begin("AnalyseVenue start")
        self.dictCity = GeoMap.load_city_dict()
        #self.listVenue = self.loadVenueFromFileNorm()
        #self.statisVenue()
        #print "debug"
        self.checkVenueInDictCity()


    def checkVenueInDictCity(self):
        #print "debug 2"
        InOut.console_func_begin("checkVenueInDictCity")

        self.listVenue = self.loadVenueFromFileFilt()
        fileVenueCity = join(Config.folderData, Config.folderDataParsed, Config.fileCity + Config.fileVenue)

        cntNo=0
        cnt = 0

        index=0
        totalCnt = len(self.listVenue)
        lineVenueCityList = []
        for venue in self.listVenue:
            cnt = cnt + 1
            #print len(self.dictCity)
            #print (user.id, user.latitude, user.longitude)
            loc = Location(venue.latitude, venue.longitude)
            city = Location.getLocCity(loc, self.dictCity)

            cityId = -1
            if(city == None):
                #print (user.latitude, user.longitude)
                cntNo = cntNo + 1
            else:
                cityId = city.id

            tmpList=[]
            tmpList.append(str(venue.venueId))
            tmpList.append(str(venue.latitude))
            tmpList.append(str(venue.longitude))
            tmpList.append(str(cityId))


            lineVenueCity = "\t".join(tmpList)
            lineVenueCityList.append(lineVenueCity)
            index = index + 1
            if(index % 1000 == 0):
                print "%s/%s\tNo:%s/%s" % (index, totalCnt, cntNo, cnt)
                #break



        print "No: %s/%s" % (cntNo, cnt)
        FileTool.FileTool.WriteStrListToFileWithNewLine(lineVenueCityList, fileVenueCity)

    def checkVenueInDictCityOld(self):
        self.dictCity = GeoMap.load_city_dict()
        self.listVenue = self.loadVenueFromFileFilt()

        cntNo=0
        cnt = 0

        index=0
        totalCnt = len(self.listVenue)
        for venue in self.listVenue:
            cnt = cnt + 1
            #print len(self.dictCity)
            loc = Location(venue.latitude, venue.longitude)
            city = Location.getLocCity(loc, self.dictCity)
            if(city == None):
                #print (venue.latitude, venue.longitude)
                cntNo = cntNo + 1

            index = index + 1
            if(index % 1000 == 0):
                print "%s/%s\tNo:%s/%s" % (index, totalCnt, cntNo, cnt)
            #    break




        print "No: %s/%s" % (cntNo, cnt)



    def loadVenueFromFileNorm(self):
        file = join(Config.folderData, Config.folderDataParsed, Config.fileNorm + Config.fileVenue)
        return self.loadVenueFromFile(file)

    def loadVenueFromFileFilt(self):
        listVenue = []
        file = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileVenue)
        return self.loadVenueFromFile(file)


    def loadVenueFromFile(self, file):
        dictVenue = {}
        listVenue = []

        lines = []
        with(open(file, "r")) as fin:
            lines = fin.readlines()


        for line in lines:
            line = line.strip("\n")
            list = line.split("\t")
            #print list
            if(len(list) != Config.fileVenueColNum):
                continue
            venueId = int(list[0])
            lat = FormatTool.float_str_to_float(list[1])
            lon = FormatTool.float_str_to_float(list[2])
            #print lat, lon
            venue = Venue(venueId, lat, lon)
            listVenue.append(venue)
            if(dictVenue.has_key(venueId) == False):
                dictVenue[venueId] = venue
        #return  dictVenue
        return listVenue


    def statisVenue(self):
        for venue in self.listVenue:
            dlat = venue.latitude
            dlon = venue.longitude
            lat = Venue.floatStrToInt(dlat)
            lon =  Venue.floatStrToInt(dlon)
            if(lat == None or lon == None):
                continue
            if(self.dictLatdictLonCnt.has_key(lat) == False):
                self.dictLatdictLonCnt[lat]={}
            if(self.dictLatdictLonCnt[lat].has_key(lon) == False):
                self.dictLatdictLonCnt[lat][lon] = 0
            self.dictLatdictLonCnt[lat][lon] = self.dictLatdictLonCnt[lat][lon] + 1

        resList = []
        latList = self.dictLatdictLonCnt.keys()
        #print latList
        for lat in latList:
            for lon in self.dictLatdictLonCnt[lat].keys():
                cnt = self.dictLatdictLonCnt[lat][lon]
                str = "%s\t%s\t%s" % (lat, lon, cnt)
                resList.append(str)

        FileTool.FileTool.WriteStrListToFileWithNewLine(resList, self.fileAnalyseVenue)

