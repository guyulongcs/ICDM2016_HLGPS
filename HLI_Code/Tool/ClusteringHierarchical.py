__author__ = 'guyulong'

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from GeoLoc import *
from GeoCoder import *

from collections import Counter
from ProcessTool import *

class ClusteringHierarchical():
    @classmethod
    def test(cls):
        X = [
            [4,50],
            [4,51],
            [10,50],
            [12,50],
            [11, 50]
        ]
        n_clusters = 2
        geoLocList = GeoLoc.trans_array_to_geolocList(X)
        resLoc = ClusteringHierarchical.cluster_Hierarchical_loc(geoLocList, n_clusters)
        print resLoc.toString()

    @classmethod
    def cluster_Hierarchical_loc(cls, geolocList, n_clusters=2):

        #threshold_dis_max = 10
        InOut.console_func_begin("cluster_Hierarchical_loc")
        print "geolocList:", len(geolocList)

        resLoc = GeoLoc()

        N= len(geolocList)
        if(N == 0):
            return resLoc
        if(N == 1):
            resLoc = geolocList[0]
            return resLoc

        X = GeoLoc.trans_geoloclist_to_array(geolocList)
        clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='average', affinity=ClusteringHierarchical.affinity_geoloc).fit(X)
        clusteringLabels = clustering.labels_

        #print clusteringLabels

        label_most_common = ProcessTool.get_list_most_common(clusteringLabels)
        index = (clusteringLabels==label_most_common)
        locList = X[index]

        locList = GeoLoc.trans_array_to_geolocList(locList)

        resLoc = GeoLoc.get_geo_loc_list_center(locList)

        #print resLoc.toString()

        return resLoc


    @classmethod
    def affinity_geoloc(cls, M):
        return np.array([[ClusteringHierarchical.metric_geoloc(a, b) for a in M] for b in M])

    @classmethod
    def metric_geoloc(cls, a, b):
        loc1 = GeoLoc(a[0], a[1])
        loc2 = GeoLoc(b[0], b[1])
        res = GeoCoder.cal_loc_distance(loc1, loc2)

        return res