__author__ = 'guyulong'

import sys
from os.path import join
from Config import *
from Tool import InOut, FileTool, GeoCoder, FormatTool, GeoLoc
from Tool.InOut import *
from Tool.GeoCoder import *
from Tool.FormatTool import *
from Tool.GeoLoc import *
import random

class Location():
    def __init__(self, lat=0.0, lon=0.0):
        self.latitude=lat;
        self.longitude=lon;


    @classmethod
    def GeoLocToLocation(cls, geoLoc):
        loc = Location(geoLoc.latitude, geoLoc.longitude)
        return loc

    @classmethod
    def LocationToGeoLoc(cls, loc):
        geoLoc = GeoLoc(loc.latitude, loc.longitude)
        return geoLoc

    @classmethod
    def cal_loc_distance_euclidean(cls, loc1, loc2):
        geoLoc1 = Location.LocationToGeoLoc(loc1)
        geoLoc2 = Location.LocationToGeoLoc(loc2)
        dis = GeoCoder.cal_loc_distance_euclidean(geoLoc1, geoLoc2)
        return dis

    @classmethod
    def get_avg_loc(cls, locationList):
        geoLocList = Location.format_list_location_to_geoloc(locationList)
        geoLoc = GeoLoc.get_geo_loc_list_center(geoLocList)
        loc = Location.GeoLocToLocation(geoLoc)
        return loc

    @classmethod
    def get_loc_random(cls):
        filtCountry = Config.filtCountry
        latMin = Config.dictCountry[filtCountry]["latMin"]
        latMax = Config.dictCountry[filtCountry]["latMax"]
        lonMin = Config.dictCountry[filtCountry]["lonMin"]
        lonMax = Config.dictCountry[filtCountry]["lonMax"]

        latRandom = random.uniform(latMin, latMax)
        lonRandom = random.uniform(lonMin, lonMax)

        loc = Location(latRandom, lonRandom)
        return loc

    @classmethod
    def isInFiltArea(cls, filtCountry, lat, lon):
        flag = False
        latMin = Config.dictCountry[filtCountry]["latMin"]
        latMax = Config.dictCountry[filtCountry]["latMax"]
        lonMin = Config.dictCountry[filtCountry]["lonMin"]
        lonMax = Config.dictCountry[filtCountry]["lonMax"]

        #print "lat:$%s$" % lat
        #print "lon:$%s$" % lon
        lat = FormatTool.floatStrToInt(lat)
        lon = FormatTool.floatStrToInt(lon)
        if( lat >= latMin and lat <= latMax and lon >= lonMin and lon <= lonMax):
            flag = True

        return flag

    @classmethod
    def isLocInBoundbox(cls, loc, boundbox):
        flag = False
        #print loc
        lat = loc.latitude
        lon = loc.longitude
        latMin = boundbox.swlat
        latMax = boundbox.nelat
        lonMin = boundbox.swlon
        lonMax = boundbox.nelon
        if( lat >= latMin and lat <= latMax and lon >= lonMin and lon <= lonMax):
            flag = True

        return flag

    @classmethod
    def isLocInCity(cls, loc, city):
        #print "isVenueInCity"

        boundbox = GeoBoundBox(city.swlat, city.swlon, city.nelat, city.nelon)

        #print (venue.latitude, venue.longitude)

        #print (boundbox.swlat, boundbox.swlon, boundbox.nelat, boundbox.nelon)

        return Location.isLocInBoundbox(loc, boundbox)


    @classmethod
    def getLocCity(cls, loc, dictCity, flagNearCity=False):

        #InOut.console_func_begin("getVenueLocCity")
        listCityCandidate = []
        listCityCandidate = Location.getLocCityCandidate(loc, dictCity)

        minDis = sys.float_info.max

        cityRes = None
        for city in listCityCandidate:
            dis = GeoCoder.cal_point_distance(loc.latitude, loc.longitude, city.lat, city.lon)
            if (dis < minDis):
                minDis = dis
                cityRes = city

        if(cityRes == None and flagNearCity):
            cityRes = Location.getLocNearCity(loc, dictCity)
        return cityRes

    @classmethod
    def getLocNearCity(cls, loc, dictCity):


        minDis = sys.float_info.max

        cityRes = None
        for cityId in dictCity:
            city = dictCity[cityId]
            dis = GeoCoder.cal_point_distance(loc.latitude, loc.longitude, city.lat, city.lon)
            if (dis < minDis):
                minDis = dis
                cityRes = city

        return cityRes


    @classmethod
    def getLocCityId(cls, loc, dictCity, flagNearCity=False):
        city = Location.getLocCity(loc, dictCity, flagNearCity)

        cityId = -1
        if(city == None):
            #print (user.latitude, user.longitude)
            #cntNo = cntNo + 1
            pass
        else:
                cityId = city.id

        cityId = int(cityId)
        return cityId


    @classmethod
    def getLocCityCandidate(cls, loc, dictCity):
        #InOut.console_func_begin("getVenueLocCityCandidate")
        #print venue.latitude, venue.longitude
        #print len(dictCity)
        listCityCandidate = []
        for cityId in dictCity.keys():
            city = dictCity[cityId]
            if(Location.isLocInCity(loc, city)):
                listCityCandidate.append(city)
        return listCityCandidate


    @classmethod
    def format_location_to_geoloc(cls, loc):
        geoLoc = GeoLoc()
        geoLoc.latitude = loc.latitude
        geoLoc.longitude = loc.longitude
        return geoLoc

    @classmethod
    def format_list_location_to_geoloc(cls, locList):
        geoLocList = []
        for loc in locList:
            geoLoc = Location.format_location_to_geoloc(loc)
            geoLocList.append(geoLoc)
        return geoLocList


    def toString(self):
        res = ""
        res = "%f, %f" % (self.latitude, self.longitude)
        return res