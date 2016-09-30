__author__ = 'guyulong'

from LoadData import *
from Config import *
from Tool.TimerTool import *

class AnalyseFriend():
    def __init__(self):
        self.flagExp = Config.flagExp
        pass

    def load_data(self):

        #check user
        self.dictUser = LoadData.load_dict_checkuser(self.flagExp)
        self.dictEdge = LoadData.load_dict_friend(self.flagExp)

        #filt all user
        #self.dictUser = LoadData.load_dict_filt_user()
        #self.dictEdge = LoadData.load_dict_filt_friend()

    def start(self):
        self.load_data()
        self.analyse_friend_distance()
        pass

    def get_friend_distance_list(self):
        resList = []

        processCnt = 0
        totalCnt = len(self.dictUser)

        timerTool = TimerTool()
        for start in self.dictUser:
            for end in self.dictUser:
                print "start: %s, end: %s" % (start, end)
                print timerTool.time_info(processCnt, totalCnt)
                istart = int(start)
                iend = int(end)
                if(istart >= iend):
                    continue

                ustart = self.dictUser[start]
                uend = self.dictUser[end]
                dis = User.cal_user_distance(ustart, uend)
                hasEdge = 0
                if(start in self.dictEdge and end in self.dictEdge[start]):
                    hasEdge = 1
                line = str(dis) + "\t" + str(hasEdge)
                resList.append(line)
            processCnt += 1
        return resList



    def get_friend_distance_list_old(self):
        resList = []
        for start in self.dictEdge:
            for end in self.dictEdge[start]:
                if(start in self.dictUser and end in self.dictUser):
                    ustart = self.dictUser[start]
                    uend = self.dictUser[end]
                    dis = User.cal_user_distance(ustart, uend)
                    dis = int(dis)
                    resList.append(dis)
        return resList

    def get_friend_distance_dict_cnt(self, list):
        dict = {}
        for dis in list:
            ProcessTool.dictStrInt_add_key(dict, dis)
        return dict

    def get_friend_distance_dict_ratio(self, dictCnt):
        dict = {}
        N = len(self.dictUser)

        CN = N*(N-1)/2

        CN = sum(dictCnt.values())

        for key in dictCnt:
            cnt = dictCnt[key]
            ratio = cnt / float(CN)
            dict[key] = ratio
        return dict

    def analyse_friend_distance(self):
        InOut.console_func_begin("analyse_friend_distance")
        list = self.get_friend_distance_list()

        file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileFriendDistance)
        FileTool.WriteStrListToFileWithNewLine(list, file)
        return


        fileRatio = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileFriendDistance + Config.fileRatio)

        dictCnt = self.get_friend_distance_dict_cnt(list)
        dict = self.get_friend_distance_dict_ratio(dictCnt)
        resList = ProcessTool.dictStrStr_to_listStr(dict)
        FileTool.WriteStrListToFileWithNewLine(resList, fileRatio)