from GeoCoder import *

import numpy as np

class GeoLoc():
    def __init__(self, lat=0.0, lon=0.0):
        self.latitude=lat;
        self.longitude=lon;

    @classmethod
    def get_geo_loc_list_center(cls, geoLocList):
        cnt = 0
        avgLoc = GeoLoc()
        for i in range(len(geoLocList)):
            oldSum = avgLoc.latitude * cnt
            newSum = oldSum + geoLocList[i].latitude
            newCnt = cnt + 1
            avgLoc.latitude = newSum / float(newCnt)
            oldSum = avgLoc.longitude * cnt
            newSum = oldSum + geoLocList[i].longitude
            avgLoc.longitude = newSum / float(newCnt)

            cnt = newCnt

        return avgLoc
        pass

    @classmethod
    def trans_geoloclist_to_array(cls, geolocList):
        X = np.array([[geoloc.latitude, geoloc.longitude] for geoloc in geolocList])
        return X

    @classmethod
    def trans_array_to_geolocList(cls, X):
        l = [GeoLoc(x[0], x[1]) for x in X]
        return l


    def toString(self):
        res = ""
        res = "lat: %f, lon: %f" % (self.latitude, self.longitude)
        return res