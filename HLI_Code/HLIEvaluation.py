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


class HLIEvaluation():
    def __init__(self):
        pass

    @classmethod
    def metrics_true_predict(cls, dictUserTrue, dictUserPredict):
        (accuracy, recall) = HLIEvaluation.cal_metrics(dictUserTrue, dictUserPredict)
        print "accuracy: %f, recall: %f" % (accuracy, recall)
        return (accuracy, recall)

    @classmethod
    def metrics_err_list(cls, dictUserTrue, dictUserPredict):
        res = []
        for user_id in dictUserPredict:
            userPredict = dictUserPredict[user_id]
            userTrue = dictUserTrue[user_id]
            dis = User.cal_user_distance(userTrue, userPredict)
            res.append(dis)
        return res





    @classmethod
    def cal_metrics(cls, dictUserTrue, dictUserPredict):
        recall = HLIEvaluation.cal_metrics_recall(dictUserTrue, dictUserPredict)
        accuracy = HLIEvaluation.cal_metrics_accuracy(dictUserTrue, dictUserPredict)
        return (accuracy, recall)

    @classmethod
    def cal_metrics_recall(cls, dictUserTrue, dictUserPredict):
        total = len(dictUserTrue)
        predict = len(dictUserPredict)
        recall = 0
        if(total > 0):
            recall = predict / (float)(total)
        return recall


    @classmethod
    def cal_metrics_accuracy(cls, dictUserTrue, dictUserPredict):

        totalCnt = 0
        trueCnt = 0
        for user_id in dictUserTrue:
            userTrue = dictUserTrue[user_id]
            if(user_id in dictUserPredict):
                totalCnt += 1
                userPredict = dictUserPredict[user_id]
                dis = User.cal_user_distance(userTrue, userPredict)
                if(HLIEvaluation.is_dis_predict_true(dis)):
                    trueCnt += 1

        accuracy = trueCnt / (float)(totalCnt)
        return accuracy


    @classmethod
    def is_dis_predict_true(cls, dis):
        return (dis < Config.threshold_predict_err_km)