__author__ = 'guyulong'


import time
import datetime


class TimeTool():

    @classmethod
    def get_time_from_seconds(cls, n):
        n = int(n)
        timeUnit = TimeUnit(n)
        return timeUnit

    @classmethod
    def get_datetime_from_str(cls, s):
        t = time.strptime(s, "%Y-%m-%d %H:%M:%S")
        dt = datetime.datetime.fromtimestamp(time.mktime(t))
        return dt

class TimeUnit():
    def __init__(self, n=0):
        self.h=0
        self.m=0
        self.s=0

        self.setValue(n)

    def toString(self):
        s = "%s H %s M %s S" % (str(self.h), str(self.m), str(self.s))
        return s

    def setValue(self, n):
        n = int(n)
        self.s = n
        if(self.s > 60):
            self.m = self.s / 60
            self.s = self.s % 60
        if(self.m > 60):
            self.h = self.m / 60
            self.m = self.m % 60

