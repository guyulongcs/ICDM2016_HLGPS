__author__ = 'guyulong'

class TypeTool():
    def __init__(self):
        pass

    @classmethod
    def str_to_float(cls, s):
        try:
            res = float(s)
        except:
            res = 0

        return res

    @classmethod
    def str_to_int(cls, s):
        try:
            res = int(s)
        except:
            res = 0

        return res


    @classmethod
    def listLineList_to_linelist(cls, listLineList, connStr="\t"):
        resList = []
        for listLine in listLineList:
            line = connStr.join(listLine)
            resList.append(line)
        return resList

    @classmethod
    def setstr_to_setint(cls, setstr):
        res = set()
        for s in setstr:
            n = TypeTool.str_to_int(s)
            res.add(n)
        return res

    @classmethod
    def liststr_to_listfloat(cls, liststr):
        res = []
        for s in liststr:
            n = TypeTool.str_to_float(s)
            res.append(n)
        return res

