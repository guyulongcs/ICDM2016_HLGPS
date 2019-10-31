from os.path import join
from Config import *
from Tool import FormatTool
from Tool import GeoLoc
from Tool import Clustering

from Tool.FormatTool import *
from Tool.GeoLoc import *
from Tool.Clustering import *
from User import *
from GeoMap import *
from Location import *
from Checkin import *
from Tool.InOut import *

class AnalyseLoc():
    def __init__(self):
        self.dictCity = GeoMap.load_city_dict()
        pass

    @classmethod
    def clustering_loc(cls, locList, clustering_method):

        loc = Location()
        N = len(locList)
        if(N == 0):
            return loc

        if(N == 1):
            return locList[0]

        geoLocList = Location.format_list_location_to_geoloc(locList)

        if(clustering_method == Config.clustering_Singlepass):
            loc = AnalyseLoc.clustering_geoloc_Singlepass(geoLocList)

        elif(clustering_method == Config.clustering_Kmeans):
            loc = AnalyseLoc.clustering_geoloc_Kmeans(geoLocList)

        return loc
        pass

    @classmethod
    def clustering_geoloc_Singlepass(cls, geoLocList):
        InOut.console_func_begin("clustering_loc_Singlepass")

        loc = Location()
        loc = Clustering.cluster_Singlepass_loc(geoLocList, Config.dictParamsClustering[Config.clustering_Singlepass]["threshold_dis_max"])
        return loc
        pass

    @classmethod
    def clustering_geoloc_Kmeans(cls, geoLocList):
        print "clustering_geoloc_Kmeans..."

        loc = Location()
        loc = Clustering.cluster_Kmeans_loc(geoLocList, Config.dictParamsClustering[Config.clustering_Kmeans]["K"], Config.dictParamsClustering[Config.clustering_Kmeans]["Round"])
        return loc
        pass

