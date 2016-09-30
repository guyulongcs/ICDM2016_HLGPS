__author__ = 'guyulong'

import math
import geocoder
import geopy
from geopy.distance import *

from InOut import *
from GeoBoundBox import *
from GeoLoc import *

class GeoCoder():
    @classmethod
    def get_place_bound_box(cls, place):
        print place
        boundBox = None

        try:
            #print place
            g = geocoder.osm(place)

            box = g.bbox

            #print box
            swlat = box["southwest"][0]
            swlon = box["southwest"][1]
            nelat = box["northeast"][0]
            nelon = box["northeast"][1]

            #print swlat, swlon, nelat, nelon
            boundBox = GeoBoundBox(swlat, swlon, nelat, nelon)

        except:
            InOut.except_info("get_place_bound_box")
            boundBox = None

        return boundBox

    @classmethod
    def cal_point_distance(cls, lat1, long1, lat2, long2):
        dis=0.0
        #dis = GeoCoder.distance_on_unit_sphere(lat1, long1, lat2, long2)
        dis = GeoCoder.distance_geopy(lat1, long1, lat2, long2)
        return dis

    @classmethod
    def cal_loc_distance(cls, loc1, loc2):
        return GeoCoder.cal_point_distance(loc1.latitude, loc1.longitude, loc2.latitude, loc2.longitude)

    @classmethod
    def cal_loc_distance_euclidean(cls, loc1, loc2):
        dis = (loc1.latitude - loc2.latitude) ** 2 + (loc1.longitude - loc2.longitude) ** 2
        return dis

    @classmethod
    def distance_geopy(cls, lat1, long1, lat2, long2):
        p1 = (lat1, long1)
        p2= (lat2, long2)
        dis = vincenty(p1, p2).kilometers
        return dis

    @classmethod
    def distance_on_unit_sphere(cls, lat1, long1, lat2, long2):
        earth_radius = 6371
        # Convert latitude and longitude to
        # spherical coordinates in radians.
        degrees_to_radians = math.pi/180.0

        # phi = 90 - latitude
        phi1 = (90.0 - lat1)*degrees_to_radians
        phi2 = (90.0 - lat2)*degrees_to_radians

        # theta = longitude
        theta1 = long1*degrees_to_radians
        theta2 = long2*degrees_to_radians

        # Compute spherical distance from spherical coordinates.

        # For two locations in spherical coordinates
        # (1, theta, phi) and (1, theta, phi)
        # cosine( arc length ) =
        #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
        # distance = rho * arc length

        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
               math.cos(phi1)*math.cos(phi2))
        arc = math.acos( cos )

        # Remember to multiply arc by the radius of the earth
        # in your favorite set of units to get length.

        dis = earth_radius * arc
        return dis

    @classmethod
    def test(cls):
        dis = GeoCoder.cal_point_distance(52.2296756,21.0122287,52.406374,16.9251681)
        dis = GeoCoder.cal_point_distance(42, 31, 45, 32)


        dis2 = GeoCoder.distance_geopy(42, 31, 45, 32)

        print dis, dis2


if __name__=="__main__":
    GeoCoder.test()
