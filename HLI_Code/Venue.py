__author__ = 'guyulong'

import sys
from os.path import join
from Config import *
from Tool import InOut, FileTool, GeoCoder
from Tool.InOut import *
from Tool.GeoCoder import *

class Venue():
    def __init__(self, id=0, lat=0.0, lon=0.0, inf=0.0):
        self.venueId=id;
        self.latitude=lat;
        self.longitude=lon;
        self.influence = inf

    @classmethod
    def floatStrToInt(cls, str):
        #n = 0
        if(str == ""):
            str = "0"

        n = int(round(float(str)))
        #try:
        #    n = int(round(float(str)))
            #print "str: %s" % str
            #print "n: %d" % n
        #except:
        #    print "str is not digit: $%s$" % str

        return n

    @classmethod
    def intStrToInt(cls, str):
        if(str == ""):
            str="0"

        n=int(str)
        return n

    @classmethod
    def isInFiltArea(cls, filtCountry, lat, lon):
        flag = False
        latMin = Config.dictCountry[filtCountry]["latMin"]
        latMax = Config.dictCountry[filtCountry]["latMax"]
        lonMin = Config.dictCountry[filtCountry]["lonMin"]
        lonMax = Config.dictCountry[filtCountry]["lonMax"]

        #print "lat:$%s$" % lat
        #print "lon:$%s$" % lon
        lat = Venue.floatStrToInt(lat)
        lon = Venue.floatStrToInt(lon)
        if( lat >= latMin and lat <= latMax and lon >= lonMin and lon <= lonMax):
            flag = True

        return flag

    @classmethod
    def isVenueInBoundbox(cls, venue, boundbox):
        flag = False
        lat = venue.latitude
        lon = venue.longitude
        latMin = boundbox.swlat
        latMax = boundbox.nelat
        lonMin = boundbox.swlon
        lonMax = boundbox.nelon
        if( lat >= latMin and lat <= latMax and lon >= lonMin and lon <= lonMax):
            flag = True

        return flag

    @classmethod
    def isVenueInCity(cls, venue, city):
        #print "isVenueInCity"

        boundbox = GeoBoundBox(city.swlat, city.swlon, city.nelat, city.nelon)

        #print (venue.latitude, venue.longitude)

        #print (boundbox.swlat, boundbox.swlon, boundbox.nelat, boundbox.nelon)

        return Venue.isVenueInBoundbox(venue, boundbox)


    @classmethod
    def getVenueLocCity(cls, venue, dictCity):
        #InOut.console_func_begin("getVenueLocCity")
        listCityCandidate = []
        listCityCandidate = Venue.getVenueLocCityCandidate(venue, dictCity)

        minDis = sys.float_info.max

        cityRes = None
        for city in listCityCandidate:
            dis = GeoCoder.cal_point_distance(venue.latitude, venue.longitude, city.lat, city.lon)
            if (dis < minDis):
                minDis = dis
                cityRes = city

        return cityRes


    @classmethod
    def getVenueLocCityCandidate(cls, venue, dictCity):
        #InOut.console_func_begin("getVenueLocCityCandidate")
        #print venue.latitude, venue.longitude
        #print len(dictCity)
        listCityCandidate = []
        for cityId in dictCity.keys():
            city = dictCity[cityId]
            if(Venue.isVenueInCity(venue, city)):
                listCityCandidate.append(city)
        return listCityCandidate


    @classmethod
    def loadDictVenueFromNormFile(cls, file=""):
        InOut.console_func_begin("Venue loadDictVenueFromNormFile")

        if(file == ""):
            file = join(Config.folderData, Config.folderDataParsed, Config.fileNorm + Config.fileVenue)

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
            lat = float(list[1])
            lon = float(list[2])
            #print lat, lon
            venue = Venue(venueId, lat, lon)
            listVenue.append(venue)
            if(dictVenue.has_key(venueId) == False):
                dictVenue[venueId] = venue
        return  dictVenue
        #return listVenue
