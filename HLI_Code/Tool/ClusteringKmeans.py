import sys
import random
from GeoLoc import *
from ClusterLoc import *
from GeoCoder import *
from Process import *


class ClusteringKmeans():
    def __init__(self):
        pass

    @classmethod
    def cluster_Kmeans_loc(cls, geolocList, K, MaxRound):
        clusterList = []

        #init
        indexList = Process.get_random_list(0, len(geolocList)-1, K)
        for index in indexList:
            loc = geolocList[index]
            clusterLoc = ClusterLoc()
            #clusterLoc.locList.append(loc)
            clusterLoc.centerLoc = loc
            clusterList.append(clusterLoc)

        #kmeans
        iteration = 0
        while(True):
            ClusteringKmeans.cluster_Kmeans_clear_cluster_loc(clusterList)

            for geoloc in geolocList:
                index = ClusteringKmeans.cluster_Kmeans_loc_get_loc_cluster_index(geoloc, clusterList)
                ClusteringKmeans.cluster_Kmeans_loc_add_loc_to_cluster_index(geoloc, clusterList, index)
            ClusteringKmeans.cluster_Kmeans_update_cluster_center(clusterList)

            iteration = iteration + 1
            if(iteration >= MaxRound):
                break

            pass

        #get largest cluster
        maxCnt = -1
        maxCluster = ClusterLoc()
        for cluster in clusterList:
            cnt = len(cluster.locList)
            if(cnt > maxCnt):
                maxCnt = cnt
                maxCluster = cluster

        resLoc = maxCluster.centerLoc
        print resLoc.toString()
        return resLoc

        pass

    @classmethod
    def cluster_Kmeans_loc_get_loc_cluster_index(cls, geoloc, clusterList):
        index = -1
        minDis = sys.float_info.max

        for i in range(len(clusterList)):
            clusterLoc = clusterList[i]
            dis = GeoCoder.cal_loc_distance(geoloc, clusterLoc.centerLoc)
            if(dis < minDis):
                minDis = dis
                index = i

        return index

    @classmethod
    def cluster_Kmeans_loc_add_loc_to_cluster_index(cls, geoloc, clusterList, index):
        clusterList[index].locList.append(geoloc)
        pass

    @classmethod
    def cluster_Kmeans_update_cluster_center(cls, clusterList):
        for i in range(len(clusterList)):
            cluster = clusterList[i]
            clusterList[i].centerLoc = GeoLoc.get_geo_loc_list_center(clusterList[i].locList)
        pass

    @classmethod
    def cluster_Kmeans_clear_cluster_loc(cls, clusterList):
        for i in range(len(clusterList)):
            cluster = clusterList[i]
            clusterList[i].locList = []
        pass
