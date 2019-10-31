from os.path import join
from Config import *

from Tool import FileTool
from Tool.FileTool import *
from Tool.InOut import *

from AnalyseUser import *

class GetExpData():
    def __init__(self):
        self.allUserSet = set()
        self.checkUserSet = set()
        pass

    def start(self):
        #self.get_exp_user_set()
        self.load_exp_user_set()

        self.get_exp_data()
        pass

    def get_exp_user_set(self):
        InOut.console_func_begin("get_exp_user")
        ula = AnalyseUser.load_user_set_in_select_city_list()
        uc = AnalyseUser.load_user_set_has_check_in()

        print "ula: ", len(ula)
        print "uc: ", len(uc)

        ulac = ula & uc
        ulanc = ula - ulac

        print "ulac: ", len(ulac)
        print "ulanc: ", len(ulanc)


        fileUser = join(Config.folderData, Config.folderDataParsed, Config.folderExp,Config.fileUserSet)
        fileCheckUser = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileFlagCheck + Config.fileUserSet)

        FileTool.FileTool.WriteStrListToFileWithNewLine(list(ula), fileUser)
        FileTool.FileTool.WriteStrListToFileWithNewLine(list(ulac), fileCheckUser)

        #return ulac
        pass


    def load_exp_user_set(self):
        self.allUserSet = self.load_exp_all_user_set()
        self.checkUserSet = self.load_exp_check_user_set()

    def load_exp_all_user_set(self):
        InOut.console_func_begin("load_exp_all_user_set")
        fileUser = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileUserSet)
        userSet = FileTool.FileTool.ReadFileColumnSet(fileUser)
        return userSet

    def load_exp_check_user_set(self):
        InOut.console_func_begin("load_exp_check_user_set")
        fileUser = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileFlagCheck + Config.fileUserSet)
        userSet = FileTool.FileTool.ReadFileColumnSet(fileUser)
        return userSet


    def get_exp_data(self):
        InOut.console_func_begin("get_exp_data")

        self.get_exp_user()
        self.get_exp_checkin()
        self.get_exp_venue()
        self.get_exp_rating()
        self.get_exp_social()


    def get_exp_user(self):
        InOut.console_func_begin("get_exp_user")

        self.get_check_user_data()
        #self.get_exp_cityfulluser()
        #self.split_exp_cityfulluser()

    def get_check_user_data(self):
        InOut.console_func_begin("get_check_user_data")
        fileUser = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileUser)
        fileCheckUser = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileFlagCheck + Config.fileUser)

        colIndex = 0
        FileTool.FileTool.FiltFileByColInSet(fileUser, fileCheckUser, colIndex, self.checkUserSet)




    def get_exp_checkin(self):
        InOut.console_func_begin("get_exp_checkin")

        fileFiltCheckin = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileCheckin)
        fileExpCheckin = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileCheckin)

        colIndex = 1
        FileTool.FileTool.FiltFileByColInSet(fileFiltCheckin, fileExpCheckin, colIndex, self.checkUserSet)
        pass


    def get_exp_venue(self):
        InOut.console_func_begin("get_exp_venue")
        #self.get_exp_city_venue()
        self.split_exp_city_venue()

    def get_exp_city_venue(self):

        fileCityVenue = join(Config.folderData, Config.folderDataParsed, Config.fileCity + Config.fileVenue)
        fileExp = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.fileCity + Config.fileVenue)

        FileTool.FileTool.CopyFile(fileCityVenue, fileExp)

    def split_exp_city_venue(self):
        colIndex = 0
        fileExp = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.fileCity + Config.fileVenue)
        listLineList = FileTool.FileTool.ReadListLineListFromFile(fileExp)

        fileExpVenue = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.fileVenue)
        fileExpVenueCity = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.fileVenueCity)

        listVenueLoc = []
        listVenueCity = []


        for listLine in listLineList:
            venueId = listLine[0]
            lat = listLine[1]
            lon = listLine[2]
            cityId = listLine[3]

            lineVenueLoc = venueId + "\t" + lat + "\t" + lon
            lineVenueCity = venueId + "\t" + cityId

            listVenueLoc.append(lineVenueLoc)
            listVenueCity.append(lineVenueCity)

        FileTool.FileTool.WriteStrListToFileWithNewLine(listVenueLoc, fileExpVenue)
        FileTool.FileTool.WriteStrListToFileWithNewLine(listVenueCity, fileExpVenueCity)
        pass

    def get_exp_rating(self):
        InOut.console_func_begin("get_exp_rating")

        fileFilt = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileRating)
        fileExp = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileRating)

        colIndex = 0
        #FileTool.FileTool.FiltFileByColInSet(fileFilt, fileExp, colIndex, self.checkUserSet)
        FileTool.FileTool.FiltFileByColInSet(fileFilt, fileExp, colIndex, self.allUserSet)

        pass

    def get_exp_social(self):
        InOut.console_func_begin("get_exp_social")

        fileFiltSocial = join(Config.folderData, Config.folderDataParsed, Config.fileFilt + Config.fileSocialGraph)
        fileExpSocial = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileSocialGraph)


        #FileTool.FileTool.FiltFileByTwoColAtleastOneInSet(fileFiltSocial, fileExpSocial, 0, 1, self.checkUserSet)

        FileTool.FileTool.FiltFileByTwoColAllInSet(fileFiltSocial, fileExpSocial, 0, 1, self.allUserSet)



        pass

    def get_exp_cityfulluser(self):
        InOut.console_func_begin("get_exp_cityfulluser")

        fileCityFullUser = join(Config.folderData, Config.folderDataParsed, Config.fileCity + Config.fileFull + Config.fileUser)
        fileExpUser = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileCity + Config.fileFull + Config.fileUser)

        colIndex = 0
        FileTool.FileTool.FiltFileByColInSet(fileCityFullUser, fileExpUser, colIndex, self.allUserSet)
        pass

    def split_exp_cityfulluser(self):
        InOut.console_func_begin("split_exp_cityfulluser")
        fileExpCityUser = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileCity + Config.fileFull + Config.fileUser)
        fileExpUser = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.fileUser)
        fileExpUserCity = join(Config.folderData, Config.folderDataParsed, Config.folderExp,  Config.fileUserCity)

        listLineList = FileTool.FileTool.ReadListLineListFromFile(fileExpCityUser)

        listUser = []
        listUserCity = []
        for listLine in listLineList:
            uid = listLine[0]
            lat = listLine[1]
            lon = listLine[2]
            cityId = listLine[3]

            lineUser = uid + "\t" + lat + "\t" + lon
            lineUserCity = uid + "\t" + cityId

            listUser.append(lineUser)
            listUserCity.append(lineUserCity)

        FileTool.FileTool.WriteStrListToFileWithNewLine(listUser, fileExpUser)
        FileTool.FileTool.WriteStrListToFileWithNewLine(listUserCity, fileExpUserCity)


