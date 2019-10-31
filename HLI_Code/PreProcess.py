from os import listdir
from os.path import isfile, join
from Tool import  ConfigTool, InOut
#import Tool.FileTool
#import Tool.MySQLTool
#import Tool.ConfigTool
#import Tool.InOut
#from Tool.ConfigTool import *
#from Tool.MySQLTool import *
#from Tool.FileTool import *
#from Tool.InOut import *

import Tool.TypeTool
from Tool.TypeTool import *
from Config import *
from Venue import *
import numpy as np

class PreProcess():
    def __init__(self):
        #self.db = MySQLTool.MySQLTool()
        #self.db.connect(host=Config.host, user=Config.user, pwd=Config.pwd, db=Config.database)
        self.listVenue = []

        pass

    def start(self):
        InOut.console_func_begin("PreProcess")
        #self.proDbCheckInNoLatLon()

        #self.processFileFormat()
        #self.processNoLatLon()

        #self.filtByLatLon()

        InOut.console_func_end("PreProcess")
        pass

    def processNoLatLon(self):
        self.processFileUserNoLatLon()
        self.processFileVenueNoLatLon()
        self.processFileCheckInNoLatLon()

    #filt in area
    def filtByLatLon(self):
        InOut.console_func_begin("filtByLatLon")
        self.filt_by_lat_lon_user()
        #self.filt_by_lat_lon_venue()

        #self.filt_by_lat_lon_socialgraph()
        #self.filt_by_lat_lon_checkin()
        #self.filt_by_lat_lon_rating()
        pass

    def load_filt_user_set(self):
        filtUser = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileUser)

        listUser = np.loadtxt(filtUser,dtype="int", usecols=(0,))

        setUser = set(listUser)
        return setUser

    def load_filt_venue_set(self):
        filtVenue = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileVenue)

        listVenue = np.loadtxt(filtVenue, dtype="int", usecols=(0,))

        setVenue = set(listVenue)
        return setVenue

    def filt_by_lat_lon_socialgraph(self):
        InOut.console_func_begin("filt_by_lat_lon_socialgraph")
        setUser = self.load_filt_user_set()
        fileSocialgraph = join(Config.folderData, Config.folderDataParsed, Config.fileSocialGraph)
        filtSocialgraph = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileSocialGraph)
        lineList = FileTool.FileTool.ReadLineListFromFile(fileSocialgraph)
        lineListNew = []

        index=0
        for line in lineList:
            index = index+1
            list = line.split("\t")
            if(len(list) == 2):
                u1 = Venue.intStrToInt(list[0])
                u2 = Venue.intStrToInt(list[1])
                #print "u1:$%s$, u2:$%s$" % (u1, u2)
                if((u1 in setUser) and (u2 in setUser)):
                    lineListNew.append(line)
            if(index % 10000 == 0):
                str = "%s/%s" % (index, len(lineList))
                print str
        FileTool.FileTool.WriteStrListToFileWithNewLine(lineListNew, filtSocialgraph)
        pass

    def filt_by_lat_lon_checkin(self):
        InOut.console_func_begin("filt_by_lat_lon_checkin")
        setUser = self.load_filt_user_set()
        setVenue = self.load_filt_venue_set()
        file = join(Config.folderData, Config.folderDataParsed, Config.fileNorm + Config.fileCheckin)
        filtFile = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileCheckin)
        lineList = FileTool.FileTool.ReadLineListFromFile(file)
        lineListNew = []

        for line in lineList:
            list = line.split("\t")
            uid = Venue.floatStrToInt(list[1])
            vid= Venue.floatStrToInt(list[2])
            if((uid in setUser) and (vid in setVenue)):
                lineListNew.append((line))
        FileTool.FileTool.WriteStrListToFileWithNewLine(lineListNew, filtFile)
        pass

    def filt_by_lat_lon_rating(self):
        InOut.console_func_begin("filt_by_lat_lon_rating")

        setUser = self.load_filt_user_set()
        setVenue = self.load_filt_venue_set()
        file = join(Config.folderData, Config.folderDataParsed,   Config.fileRating)
        filtFile = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileRating)
        lineList = FileTool.FileTool.ReadLineListFromFile(file)
        lineListNew = []

        for line in lineList:
            list = line.split("\t")
            if(len(list) < 2):
                continue
            uid = Venue.floatStrToInt(list[0])
            vid= Venue.floatStrToInt(list[1])
            if((uid in setUser) and (vid in setVenue)):
                lineListNew.append((line))
        FileTool.FileTool.WriteStrListToFileWithNewLine(lineListNew, filtFile)
        pass

    def filt_by_lat_lon_file(self, file, latCol, lonCol):
        InOut.console_func_begin("filt_by_lat_lon_file " + file)
        fileNorm = join(Config.folderData, Config.folderDataParsed, Config.fileNorm + file)
        fileFilt = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + file)
        lineList = FileTool.FileTool.ReadLineListFromFile(fileNorm)

        lineListNew = []
        for line in lineList:
            #print "line:$%s$" % line
            list = line.split("\t")
            lat = list[latCol]
            lon = list[lonCol]
            #print "lat:$%s$" % lat
            #print "lon:$%s$" % lon

            if(Venue.isInFiltArea(Config.filtCountry, lat, lon) == True):
                lineListNew.append(line)

            #break

        FileTool.FileTool.WriteStrListToFileWithNewLine(lineListNew, fileFilt)
        pass

    def filt_by_lat_lon_user(self):
        self.filt_by_lat_lon_file(Config.fileUser, 1, 2)

    def filt_by_lat_lon_venue(self):
        self.filt_by_lat_lon_file(Config.fileVenue, 1, 2)



    #func: db format to csv format
    def processFileFormat(self):
        InOut.console_func_begin("processFileFormat")
        srcFolder = join(Config.folderData, Config.folderDataOri)
        dstFolder = join(Config.folderData, Config.folderDataParsed)
        for file in listdir(srcFolder):
            print "Process %s..." % file
            if(len(file) > 0 and file[0]=='.'):
                continue
            fileName = join(srcFolder, file)
            lineList = FileTool.ReadLineListFromFile(fileName, 2)
            fileNew = join(dstFolder,file)
            lineListNew = FileTool.ReplaceLineListSplitNorm(lineList, "|", "\t")

            FileTool.WriteStrListToFileWithNewLine(lineListNew, fileNew)
            #break;

        pass;

    def processFileCheckInNoLatLon(self):
        InOut.console_func_begin("processFileCheckInNoLatLon")
        dictVenue = Venue.loadDictVenueFromNormFile()
        folder = join(Config.folderData, Config.folderDataParsed)
        fileCheckIn = join(folder, Config.fileCheckin)
        fileCheckinNorm = join(folder, Config.fileNorm + Config.fileCheckin)

        lines=[]
        with(open(fileCheckIn,"r")) as fin:
            lines=fin.readlines()

        lineListNew = []
        for line in lines:
            line = line.strip("\n")
            list = line.split("\t")
            if(len(list) != Config.fileCheckinColNum):
                continue

            venueId = int(list[2])
            if(dictVenue.has_key(venueId) == False):
                continue;

            lat = list[3]
            lon = list[4]
            if(self.isNoLatLon(lat, lon)):
                list[3] = "%f" % dictVenue[venueId].latitude
                list[4] = "%f" % dictVenue[venueId].longitude
            lineNew = "\t".join(list)
            lineListNew.append(lineNew)

            #break;


        FileTool.FileTool.WriteStrListToFileWithNewLine(lineListNew, fileCheckinNorm)


    def isNoLatLon(self, lat, lon):
        #print lat


        lat =  TypeTool.str_to_float(lat)
        lon =  TypeTool.str_to_float(lon)

        lat = abs(lat)
        lon = abs(lon)

        thres = 0.01

        flag = False
        if(lat < thres and lon < thres ):
            flag = True

        return flag



    def processFileNoLatLon(self, folder, file, fileColCnt, fileNorm):
        InOut.console_func_begin("processFileNoLatLon")


        fileUser = file
        fileUserNorm = fileNorm

        lines=[]
        with(open(fileUser,"r")) as fin:
            lines=fin.readlines()

        lineListNew = []
        for line in lines:
            line = line.strip("\n")
            list = line.split("\t")
            if(len(list) != fileColCnt):
                continue

            userId = int(list[0])
            lat = list[1]
            lon = list[2]

            if(self.isNoLatLon(lat, lon)):
                continue

            lineListNew.append(line)

        FileTool.FileTool.WriteStrListToFileWithNewLine(lineListNew, fileUserNorm)

    def processFileUserNoLatLon(self):
        InOut.console_func_begin("processFileUserNoLatLon")

        folder = join(Config.folderData, Config.folderDataParsed)
        fileUser = join(folder, Config.fileUser )
        fileUserNorm = join(folder, Config.fileNorm + Config.fileUser)
        self.processFileNoLatLon(folder, fileUser, Config.fileUserColNum, fileUserNorm)

    def processFileVenueNoLatLon(self):
        InOut.console_func_begin("processFileVenueNoLatLon")

        folder = join(Config.folderData, Config.folderDataParsed)
        fileVenue = join(folder, Config.fileVenue )
        fileVenueNorm = join(folder,  Config.fileNorm + Config.fileVenue)
        self.processFileNoLatLon(folder, fileVenue, Config.fileVenueColNum, fileVenueNorm)








    def proCheckInNoLatLon(self):
        #srcFolder = self.conf.get("folderFile", "folderData")
        srcFolder = Config.folderData
        print srcFolder


    def proDbCheckInNoLatLon(self):


        sqlStr="select * from checkins where latitude < 0.01 and longitude < 0.01 limit 0,10"
        print "sql:" + sqlStr
        (line, cur) = self.db.execute(sqlStr)
        #(line, cur) = db.execute(sqlStr, None, MySQLTool.DICTCURSOR_MODE)
        result = self.db.fetch_executeresult(cur,MySQLTool.MySQLTool.FETCH_ALL)

        print result

    def loadDBVenue(self):
        sqlStr = "select * from venues";
        (line, cur) = self.db.execute(sqlStr)
        result = self.db.fetch_executeresult(cur,MySQLTool.MySQLTool.FETCH_ALL)
        print result

        pass;