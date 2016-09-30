__author__ = 'guyulong'


from Tool.InOut import *
from Tool.FileTool import *
from Tool.ProcessTool import *
from Tool.Evaluation import *
from Config import *
from Venue import *
from Checkin import *
from User import *
from Location import *
from AnalyseCheckin import *
from LoadData import *
from Tool.MLTool import *
from Tool.TimerTool import *
from HLIData import *
from HLIAvg import *
from HLIMaxVote import *
from HLIClustering import *
from HLIInfluenceGlobal import *
from HLITrust import *
from HLIEvaluation import *

class HomeLocIdentify():
    def __init__(self):
        self.hliData = HLIData()
        pass

    def start(self):
        InOut.console_func_begin("start")

        if(Config.flag_home_loc_identify):
            self.home_loc_identify()
            pass

        self.load_data_home_loc()
        self.home_loc_identify_evaluation()
        #self.analyse_exp_result()
        pass

    def load_data(self):
        self.hliData.load_data()
        self.hliData.home_loc_identify_get_exp_data()

    def home_loc_identify(self):
        InOut.console_func_begin("home_loc_identify")
        self.load_data()
        self.home_loc_identify_predict()


    def home_loc_identify_predict(self):
        InOut.console_func_begin("home_loc_identify_predict")
        if(Config.flag_method_avg):
            self.home_loc_identify_predict_avg()
        if(Config.flag_method_maxVote):
            self.home_loc_identify_predict_maxVote()
        if(Config.flag_method_clustering):
            self.home_loc_identify_predict_clustering()
        if(Config.flag_method_influenceGlobal):
            self.home_loc_identify_predict_influenceGlobal()
        if(Config.flag_method_trust):
            self.home_loc_identify_predict_trust()


    def analyse_exp_result(self):
        InOut.console_func_begin("analyse_exp_result")
        self.analyse_exp_result_errdis()
        self.analyse_exp_result_errcdf()


    def analyse_exp_result_errdis(self):
        InOut.console_func_begin("analyse_exp_result_errdis")

        la = [0, 1]
        la.extend(range(10, 100, 10))
        la.extend(range(100,1000,100))
        la.extend(range(1000,3500,500))

        threshold_predict_err_mile = la

        resList = []
        for mile in threshold_predict_err_mile:
            Config.threshold_predict_err_km = mile * Config.const_mile_km
            (accuracy1, recall1) = HLIEvaluation.metrics_true_predict(self.homeLocTrue, self.homeLocInfluenceGlobal)
            (accuracy2, recall2) = HLIEvaluation.metrics_true_predict(self.homeLocTrue, self.homeLocTrust)

            line = "%s\t%s\t%s" % (str(mile), str(accuracy1), str(accuracy2))
            print line

            resList.append(line)

        file = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.file_exp_result_mile_accuracy)
        FileTool.WriteStrListToFileWithNewLine(resList, file)

    def analyse_exp_result_errcdf(self):
        InOut.console_func_begin("analyse_exp_result_errcdf")
        self.analyse_exp_result_errcdf_method_type(Config.methodTrust)
        self.analyse_exp_result_errcdf_method_type(Config.methodInfluenceGlobal)
        self.analyse_exp_result_errcdf_method_type(Config.methodAvg)
        self.analyse_exp_result_errcdf_method_type(Config.methodVote)
        self.analyse_exp_result_errcdf_method_type(Config.clustering_Hierarchical)


    @classmethod
    def get_file_true_homeloc(cls):
        folder =  join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio)
        file = join(folder, Config.fileTrue + Config.fileHomeLoc )
        return file
    @classmethod
    def get_file_name_errdis(cls, method_type):
        folder =  join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio)
        file = join(folder,  method_type + Config.file_exp_result_errdis )
        return file
    def analyse_exp_result_errcdf_method_type(self, method_type):
        print "method_type:", method_type
        resList = []
        file = ""
        homeLoc = None
        if(method_type == Config.methodTrust):
            homeLoc = self.homeLocTrust
        elif(method_type == Config.methodAvg):
            homeLoc = self.homeLocAvg
        elif(method_type == Config.methodVote):
            homeLoc = self.homeLocMaxVote
        elif(method_type == Config.methodInfluenceGlobal):
            homeLoc = self.homeLocInfluenceGlobal
        elif(method_type == Config.clustering_Hierarchical):
            homeLoc = self.homeLocHierarchy

        resList = HLIEvaluation.metrics_err_list(self.homeLocTrue, homeLoc)
        file = HomeLocIdentify.get_file_name_errdis(method_type)
        print "file:", file


        FileTool.WriteStrListToFileWithNewLine(resList, file)




    def home_loc_identify_evaluation(self):
        InOut.console_func_begin("home_loc_identify_evaluation")


        print "\navg"
        HLIEvaluation.metrics_true_predict(self.homeLocTrue, self.homeLocAvg)

        print "\nvote: "
        HLIEvaluation.metrics_true_predict(self.homeLocTrue, self.homeLocMaxVote)

        print "\nInfluenceGlobal"
        HLIEvaluation.metrics_true_predict(self.homeLocTrue, self.homeLocInfluenceGlobal)

        print "\ntrust"
        HLIEvaluation.metrics_true_predict(self.homeLocTrue, self.homeLocTrust)


        print "\nclustering: "

        for clusteringMethod in Config.clusteringMethods:
            print "\n"
            print clusteringMethod

            self.homeLocClustering = HLIClustering.load_data_home_loc_clustering(clusteringMethod)

            HLIEvaluation.metrics_true_predict(self.homeLocTrue, self.homeLocClustering)




    def load_data_home_loc(self):
        self.homeLocTrue = self.load_data_home_loc_true()
        self.homeLocInfluenceGlobal = HLIInfluenceGlobal.load_data_home_loc_influenceGlobal()
        self.homeLocAvg = HLIAvg.load_data_home_loc_avg()
        self.homeLocTrust = HLITrust.load_data_home_loc()
        self.homeLocMaxVote = HLIMaxVote.load_data_home_loc_vote()

        self.homeLocHierarchy = HLIClustering.load_data_home_loc_clustering(Config.clustering_Hierarchical)

        print "true list:", len(self.homeLocTrue)
        print "avg list:", len(self.homeLocAvg)
        #print "vote list:", len(self.homeLocVoteList)
        print "influenceGlobal list:", len(self.homeLocInfluenceGlobal)
        print "trust list:", len(self.homeLocTrust)


        #self.load_data_home_loc_clustering()

    def load_data_home_loc_true(self):
        fileHomeLoc = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderRatio, Config.fileTrue + Config.fileHomeLoc)
        dictUser = User.loadDictUserFromFile(fileHomeLoc)
        return dictUser
        #homeLocTrueList = FileTool.ReadFileColumnList(fileHomeLocTrue)
        #return homeLocTrueList



    def home_loc_identify_predict_maxVote(self):
        hliMaxVote = HLIMaxVote(self.hliData)
        hliMaxVote.home_loc_identify_predict_maxVote()

    def home_loc_identify_predict_avg(self):
        hliAvg = HLIAvg(self.hliData)
        hliAvg.home_loc_identify_predict_avg()

    def home_loc_identify_predict_clustering(self):
        hliClustering = HLIClustering(self.hliData)
        hliClustering.home_loc_identify_predict_clustering()


    def home_loc_identify_predict_influenceGlobal(self):
        hliInfluenceGlobal = HLIInfluenceGlobal(self.hliData)
        hliInfluenceGlobal.home_loc_identify_predict_influenceGlobal()

    def home_loc_identify_predict_trust(self):
        hliTrust = HLITrust(self.hliData)
        hliTrust.home_loc_identify_predict_trust()
    