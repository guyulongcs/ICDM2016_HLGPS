import sys
import random
from GeoLoc import *
from ClusterLoc import *
from GeoCoder import *
from Process import *


class ClusteringSinglePass():
    def __init__(self):
        pass

    @classmethod
    def cluster_Singlepass_loc(cls, geolocList, threshold_dis_max):

        clusterList = []
        for loc in geolocList:
            clusterIndex = ClusteringSinglePass.cluster_single_pass_get_loc_cluster(loc, clusterList, threshold_dis_max)
            if(clusterIndex == -1):
                clusterLoc = ClusterLoc()
                clusterLoc.locList.append(loc)
                clusterLoc.centerLoc = loc
                clusterList.append(clusterLoc)
                pass
            else:
                clusterList[clusterIndex].locList.append(loc)
                ClusteringSinglePass.update_cluster_center(clusterList, clusterIndex)
                pass

            pass

        resLoc = ClusteringSinglePass.cluster_single_pass_get_max_cluster_loc(clusterList)
        return resLoc

        pass

    @classmethod
    def update_cluster_center(cls, clusterList, clusterIndex):
        clusterList[clusterIndex].centerLoc = GeoLoc.get_geo_loc_list_center(clusterList[clusterIndex].locList)

    @classmethod
    def cluster_single_pass_get_max_cluster_loc(cls, clusterList):
        maxCnt = -1
        index = -1
        for i in range(len(clusterList)):
            cluster = clusterList[i]
            cnt = len(cluster.locList)
            if(cnt > maxCnt):
                maxCnt = cnt
                index = i

        resLoc = GeoLoc
        if(index != -1):
            resLoc = clusterList[index].centerLoc
        return resLoc
        pass

    @classmethod
    def cluster_single_pass_get_loc_cluster(cls, loc, clusterList, threshold_dis_max):

        minDis = sys.float_info.max
        minIndex = -1

        for i in range(len(clusterList)):
            clusterLoc = clusterList[i]
            dis = GeoCoder.cal_loc_distance(loc, clusterLoc.centerLoc)
            if(dis < minDis):
                minDis = dis
                minIndex = i

        if(minDis > threshold_dis_max):
            minIndex = -1

        return minIndex

        pass

