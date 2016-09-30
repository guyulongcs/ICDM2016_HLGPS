__author__ = 'guyulong'

import time

from TimeTool import *

class TimerTool():
    def __init__(self):
        self.begin = 0
        self.end = 0

        self.start()

        pass

    def start(self):
        self.begin = time.time()


    def time_info(self, processCnt=0, totalCnt=0):

        self.end = time.time()
        t_s = self.end - self.begin
        t_s = int(t_s)
        t_s_need = 0
        if(processCnt > 0):
            t_s_need = (t_s*(totalCnt-processCnt)) / (float)(processCnt)

        t_past = TimeUnit(t_s)
        t_need = TimeUnit(t_s_need)

        str = "Time: %s, Remain: %s" % (t_past.toString(), t_need.toString())

        return str

