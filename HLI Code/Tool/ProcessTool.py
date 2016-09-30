__author__ = 'guyulong'

import random
import math

from collections import Counter

class ProcessTool():
    def __init__(self):
        pass

    @classmethod
    def dict_sort(cls, a, descend = False):
        a = sorted(a.items(), key=lambda a: a[1], reverse = descend)
        return a

    @classmethod
    def get_random(cls, minNum, maxNum):
        res = random.randint(minNum, maxNum)
        return res

    @classmethod
    def get_random_list(cls, minNum, maxNum, cnt):
        list = []
        for i in range(cnt):
            num = ProcessTool.get_random(minNum, maxNum)
            list.append(num)
        return list

    @classmethod
    def get_list_str_sub_n(cls, list, N=-1):
        res = []
        i=0
        for line in list:
            res.append(line)
            i += 1
            if(N >= 0 and i >= N):
                break
        return res

    @classmethod
    def get_list_most_common(cls, list):
        c = Counter(list)
        res = c.most_common(1)[0][0]
        return res

    @classmethod
    def dictStrSetstr_add_str_str(cls, dict, key, str):
        if(key not in dict):
            dict[key] = set()
        dict[key].add(str)

    @classmethod
    def dictStrListStr_add_str_str(cls, dict, key, str):
        if(key not in dict):
            dict[key] = list()
        dict[key].append(str)



    @classmethod
    def dictStrInt_add_key(cls, dict, key):
        if(key not in dict):
            dict[key] = 0
        dict[key] += 1

    @classmethod
    def dictStrDictStrValue_add_str_str_str(cls, dict, key1, key2, str):
        if(key1 not in dict):
            dict[key1]={}
        dict[key1][key2] = str

    @classmethod
    def dictStrStr_to_listStr(cls, dict):
        strList = []
        for key in dict:
            value = dict[key]
            line = str(key) + "\t" + str(value)
            strList.append(line)
        return strList


    @classmethod
    def splitListByRatio(self, l, ratio):
        l1 = []
        l2 = []

        for item in l:
            n = random.random()
            if( n <= ratio):
                l1.append(item)
            else:
                l2.append(item)
        return (l1, l2)

    @classmethod
    def sampleListByRatio(cls, l, ratio):
        N = len(l)
        k=int(N*ratio)
        index = random.sample(range(0,N), k)

        res = []
        for i in index:
            res.append(l[i])
        return res

    @classmethod
    def list_to_set(cls, l):
        return set(l)

    @classmethod
    def filt_liststr_by_set(cls, l, s):
        res= []
        if(len(l) == 0):
            return res
        for item in l:
            if(item in s):
                res.append(item)
        return res


    @classmethod
    def sigmoid(cls, x):
        res = 1 / (1+math.exp(-x))
        return res



    @classmethod
    def get_count_asc_list_l_value(cls, l, v):
        count = 0
        for i in l:
            if(i <= v):
                count += 1
            else:
                break
        return count

    @classmethod
    def list_div_value(cls, l, N):
        res = [i/float(N) for i in l]
        return res
