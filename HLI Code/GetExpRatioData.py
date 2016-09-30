from os.path import join
from Config import *

from Tool import FileTool
from Tool.FileTool import *
from Tool.InOut import *

from AnalyseUser import *
from LoadData import *

class GetExpRatioData():
    def __init__(self):
        #config
        self.flagExp = Config.flagExp
        self.flagCheckinLocUseVenueLoc = Config.flagCheckinLocUseVenueLoc

        pass

    def start(self):
        self.get_exp_ratio_data()

        pass

    def get_exp_ratio_data(self):
        self.get_exp_ratio_user_set()
        self.get_exp_ratio_data_filt()


    def get_exp_ratio_user_set(self):
        #self.setUser = LoadData.load_set_alluser(self.flagExp, False)
        self.setUser = LoadData.load_set_user()
        self.setCheckUser = LoadData.load_set_checkuser(self.flagExp)
        #user list
        self.userList = list(self.setUser)
        if(Config.flag_exp_only_check_user):
            self.userList = list(self.setCheckUser)
        maxUserCnt = Config.maxUserCnt
        self.userList = ProcessTool.get_list_str_sub_n(self.userList, maxUserCnt)
        self.userSet = ProcessTool.list_to_set(self.userList)

        (self.userKnowHomeList, self.userNotKnowHomeList) = ProcessTool.splitListByRatio(self.userList, Config.r_user_hasHomeLocation)

        print "userList:", len(self.userList)
        print "userKnowHomeList:", len(self.userKnowHomeList)
        print "userNotKnowHomeList:", len(self.userNotKnowHomeList)
        #(self.userHasCheckinList, self.userNotHasCheckinList) = ProcessTool.splitListByRatio(self.userList, Config.r_user_hasCheckin)


        #write file
        fileUser = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileUserSet)
        FileTool.WriteStrListToFileWithNewLine(self.userList, fileUser)

        fileUserKnowHome = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileKnowHome + Config.fileUserSet)
        fileUserNotKnowHome = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileNot + Config.fileKnowHome + Config.fileUserSet)
        FileTool.WriteStrListToFileWithNewLine(self.userKnowHomeList, fileUserKnowHome)
        FileTool.WriteStrListToFileWithNewLine(self.userNotKnowHomeList, fileUserNotKnowHome)

        fileUserHasCheckin = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileHasCheckin + Config.fileUserSet)
        fileUserNotHasCheckin = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileNot + Config.fileHasCheckin + Config.fileUserSet)
        #FileTool.WriteStrListToFileWithNewLine(self.userHasCheckinList, fileUserHasCheckin)
        #FileTool.WriteStrListToFileWithNewLine(self.userNotHasCheckinList, fileUserNotHasCheckin)


    def get_exp_ratio_data_filt(self):
        InOut.console_func_begin("get_exp_ratio_data_filt")
        self.get_exp_ratio_user()
        self.get_exp_ratio_userCity()
        self.get_exp_ratio_checkin()
        self.get_exp_ratio_rating()
        self.get_exp_ratio_venue()

        self.get_exp_ratio_social()
        InOut.console_func_end("get_exp_ratio_data_filt")

    def get_exp_ratio_user(self):
        InOut.console_func_begin("get_exp_ratio_user")
        fileSrc = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileUser)
        fileDst = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileUser)

        colIndex = 0
        FileTool.FiltFileByColInSet(fileSrc, fileDst, colIndex, self.userSet)

    def get_exp_ratio_userCity(self):
        InOut.console_func_begin("get_exp_ratio_userCity")
        fileSrc = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileUserCity)
        fileDst = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileUserCity)

        colIndex = 0
        FileTool.FiltFileByColInSet(fileSrc, fileDst, colIndex, self.userSet)

    def get_exp_ratio_checkin(self):
        InOut.console_func_begin("get_exp_ratio_checkin")
        print "userSet:", len(self.userSet)
        fileSrc = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileCheckin)
        fileDst = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileCheckin)
        colIndex = 1
        FileTool.FiltFileByColInSet(fileSrc, fileDst, colIndex, self.userSet)

        pass

    def get_exp_ratio_checkin_venue_set(self):
        fileDst = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileCheckin)
        res = FileTool.ReadFileColumnSet(fileDst, '\t', 2)
        return res

    def get_exp_ratio_rating_venue_set(self):
        fileDst = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileRating)
        res = FileTool.ReadFileColumnSet(fileDst, '\t', 1)
        return res

    def get_exp_ratio_venue_set(self):
        setVenueCheckin = self.get_exp_ratio_checkin_venue_set()
        setVenueRating = self.get_exp_ratio_rating_venue_set()
        setVenue = setVenueCheckin | setVenueRating
        return setVenue

    def get_exp_ratio_venue(self):
        InOut.console_func_begin("get_exp_ratio_venue")

        setVenue = self.get_exp_ratio_venue_set()
        fileExpVenue = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.fileVenue)
        fileExpVenueCity = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.fileVenueCity)

        fileDstVenue = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.folderRatio, Config.fileVenue)
        fileDstVenueCity = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileVenueCity)

        #FileTool.CopyFile(fileExpVenue, fileDstVenue)
        #FileTool.CopyFile(fileExpVenueCity, fileDstVenueCity)

        FileTool.FiltFileByColInSet(fileExpVenue, fileDstVenue, 0, setVenue)
        FileTool.FiltFileByColInSet(fileExpVenueCity, fileDstVenueCity, 0, setVenue)

        pass

    def get_exp_ratio_rating(self):
        InOut.console_func_begin("get_exp_ratio_rating")
        print "userSet:", len(self.userSet)

        fileExp = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileRating)
        fileDst = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileRating)

        colIndex = 0
        FileTool.FiltFileByColInSet(fileExp, fileDst, colIndex, self.userSet)
        pass

    def get_exp_ratio_social(self):
        InOut.console_func_begin("get_exp_ratio_social")
        fileExpSocial = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileSocialGraph)
        fileDstSocial = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileSocialGraph)
        #FileTool.FiltFileByTwoColAtleastOneInSet(fileExpSocial, fileDstSocial, 0, 1, self.userSet)
        FileTool.FiltFileByTwoColAllInSet(fileExpSocial, fileDstSocial, 0, 1, self.userSet)

