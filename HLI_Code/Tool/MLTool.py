__author__ = 'guyulong'


import sklearn
from sklearn.metrics import *

class MLTool():
    def __init__(self):
        pass

    @classmethod
    def metrics_true_predict(cls, trueList, predictList):
        accuracy =  accuracy_score(trueList, predictList)
        #precision = precision_score(trueList, predictList,  average='micro')
        #f1 = f1_score(trueList, predictList)

        print "accuracy:", accuracy
        #print "precision: ", precision
        #print "f1: ", f1
        pass
