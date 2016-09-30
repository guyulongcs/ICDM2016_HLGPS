import sys
import random
from GeoLoc import *
from ClusterLoc import *
from GeoCoder import *
from Process import *
from ClusteringSinglePass import *
from ClusteringKmeans import *
from ClusteringHierarchical import *


class Clustering():
    def __init__(self):
        pass

    @classmethod
    def cluster_Singlepass_loc(cls, geolocList, threshold_dis_max):
        return ClusteringSinglePass.cluster_Singlepass_loc(geolocList, threshold_dis_max)


    @classmethod
    def cluster_Kmeans_loc(cls, geolocList, K, MaxRound):
        return ClusteringKmeans.cluster_Kmeans_loc(geolocList, K, MaxRound)

    @classmethod
    def cluster_Hierarchical_loc(cls, geolocList, n_clusters):
        return ClusteringHierarchical.cluster_Hierarchical_loc(geolocList, n_clusters)

    @classmethod
    def test(cls):
        ClusteringHierarchical.test()