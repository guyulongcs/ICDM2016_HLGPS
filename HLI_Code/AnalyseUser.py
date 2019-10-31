from os.path import join
from Config import *
from Tool import FormatTool
from Tool.FormatTool import *

from Tool.FileTool import *

from User import *
from GeoMap import *
from Location import *
from Checkin import *

class AnalyseUser():
    def __init__(self):
        pass

    def start(self):
        self.dictCity = GeoMap.load_city_dict()
        self.checkUserInDictCity()
        self.checkUserInDictCityFull()
        #self.checkCheckinInDictCity()

    def checkUserInDictCity(self):

        self.listUser = self.loadUserFromFileFilt()
        fileUserCity = join(Config.folderData, Config.folderDataParsed, Config.fileCity + Config.fileUser)

        cntNo=0
        cnt = 0

        index=0
        totalCnt = len(self.listUser)
        lineUserCityList = []
        for user in self.listUser:
            cnt = cnt + 1
            #print len(self.dictCity)
            #print (user.id, user.latitude, user.longitude)
            loc = Location(user.latitude, user.longitude)
            city = Location.getLocCity(loc, self.dictCity)

            cityId = -1
            if(city == None):
                #print (user.latitude, user.longitude)
                cntNo = cntNo + 1
            else:
                cityId = city.id

            tmpList=[]
            tmpList.append(str(user.id))
            tmpList.append(str(user.latitude))
            tmpList.append(str(user.longitude))
            tmpList.append(str(cityId))

            lineUserCity = "\t".join(tmpList)
            lineUserCityList.append(lineUserCity)
            index = index + 1
            if(index % 1000 == 0):
                print "%s/%s\tNo:%s/%s" % (index, totalCnt, cntNo, cnt)
                #break

        print "No: %s/%s" % (cntNo, cnt)
        FileTool.FileTool.WriteStrListToFileWithNewLine(lineUserCityList, fileUserCity)

    def checkUserInDictCityFull(self):

        self.listUser = self.loadUserFromFileFilt()
        fileUserCity = join(Config.folderData, Config.folderDataParsed, Config.fileCity + Config.fileFull + Config.fileUser)

        cntNo=0
        cnt = 0

        index=0
        totalCnt = len(self.listUser)
        lineUserCityList = []
        for user in self.listUser:
            cnt = cnt + 1
            #print len(self.dictCity)
            #print (user.id, user.latitude, user.longitude)
            loc = Location(user.latitude, user.longitude)
            city = Location.getLocCity(loc, self.dictCity)
            if(city == None):
                #print (user.latitude, user.longitude)
                cntNo = cntNo + 1
            else:
                tmpList=[]
                tmpList.append(str(user.id))
                tmpList.append(str(user.latitude))
                tmpList.append(str(user.longitude))
                tmpList.append(str(city.id))
                tmpList.append(city.name)
                tmpList.append(city.state)

                lineUserCity = "\t".join(tmpList)
                lineUserCityList.append(lineUserCity)
            index = index + 1
            if(index % 1000 == 0):
                print "%s/%s\tNo:%s/%s" % (index, totalCnt, cntNo, cnt)
                #break

        print "No: %s/%s" % (cntNo, cnt)
        FileTool.FileTool.WriteStrListToFileWithNewLine(lineUserCityList, fileUserCity)



    def loadUserFromFileFilt(self):
        listUser = []
        file = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileUser)
        return self.loadUserFromFile(file)



    def loadUserFromFile(self, file):
        dictUser = {}
        listUser = []

        lines = []
        with(open(file, "r")) as fin:
            lines = fin.readlines()


        for line in lines:

            line = line.strip("\n")
            list = line.split("\t")
            #print list
            #print list
            if(len(list) != Config.fileUserColNum):
                continue
            uId = int(list[0])
            lat = FormatTool.float_str_to_float(list[1])
            lon = FormatTool.float_str_to_float(list[2])
            #print lat, lon
            user = User(uId, lat, lon)
            listUser.append(user)
            if(dictUser.has_key(uId) == False):
                dictUser[uId] = user

            #break
        #return  dictVenue
        return listUser

    @classmethod
    #user have loc and in area and in city
    def load_user_set_in_select_city_list(cls):
        fileCityFullUser = join(Config.folderData, Config.folderDataParsed, Config.fileCity + Config.fileFull + Config.fileUser)
        userSet = FileTool.FileTool.GetFileColumnSet(fileCityFullUser, '\t', 0)
        return userSet

    @classmethod
    #user in area and has checkin
    def load_user_set_has_check_in(cls):
        fileFiltCheckin = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileCheckin)
        userSet = FileTool.FileTool.GetFileColumnSet(fileFiltCheckin, '\t', 1)
        return userSet
        pass
