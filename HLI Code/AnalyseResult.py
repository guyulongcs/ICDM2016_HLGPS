
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
from os.path import *
from HomeLocIdentify import *
from Tool.FileTool import *
from Tool.TypeTool import *
class AnalyseResult():
    def __init__(self):
        pass

    @classmethod
    def load_errdis_method(cls, method_type):
        file = HomeLocIdentify.get_file_name_errdis(method_type)
        resList = FileTool.ReadFileColumnList(file)
        resList = TypeTool.liststr_to_listfloat(resList)

        return resList
    @classmethod
    def load_homeloc_cnt(cls):
        file = HomeLocIdentify.get_file_true_homeloc()
        resList = FileTool.ReadFileColumnList(file)
        N = len(resList)
        return N


    @classmethod
    def load_err_dis_cp_method(cls, method_type):
        errList = AnalyseResult.load_errdis_method(method_type)
        data = np.sort(errList)
        N = AnalyseResult.load_homeloc_cnt()
        maxvalue = 101
        step = 1
        maxvalue = min(maxvalue, len(data))

        print "data:", len(data)
        print "maxvalue:", maxvalue
        xvalues = np.arange(0, maxvalue, step)
        xa = []
        ya = []
        for x in xvalues:
            count = ProcessTool.get_count_asc_list_l_value(data, x)
            xa.append(x)
            ya.append(count)
        ya = ProcessTool.list_div_value(ya, N)

        res  = [xa, ya]
        return res







