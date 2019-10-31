__author__ = 'guyulong'

from os.path import join
from Config import *

from Tool import FileTool
from Tool.FileTool import *
from Tool.InOut import *

class Edge():
    edgeColCnt = 2

    def __init__(self, start="", end=""):
        self.start = start
        self.end = end

    @classmethod
    def read_edge_from_list(cls, list):
        edge = None
        if(len(list) == Edge.edgeColCnt):
            start = list[0]
            end = list[1]
            edge = Edge(start, end)
        return edge

    @classmethod
    def read_edge_asc_from_list(cls, list):
        edge = None
        if(len(list) == Edge.edgeColCnt):
            l1 = list[0]
            l2 = list[1]
            (start, end) = Edge.get_asc(l1, l2)
            edge = Edge(start, end)
        return edge

    @classmethod
    def get_asc(cls, l1, l2):
        il1 = int(l1)
        il2 = int(l2)
        if(il1 > il2):
            tmp = l1
            l1 = l2
            l2 = tmp
        return (l1, l2)

    @classmethod
    def loadDictEdgeFromFile_remove_duplicate(cls, file):
        dict = Edge.loadDictEdgeFromFile(file)
        dict = Edge.dictEdge_undirected_remove_duplicate(dict)
        return dict

    @classmethod
    def loadDictEdgeFromFile(cls, file, flagAsc=False):
        dict = {}
        listLineList = FileTool.ReadListLineListFromFile(file)
        for listLine in listLineList:
            if(flagAsc == False):
                edge = Edge.read_edge_from_list(listLine)
            else:
                edge = Edge.read_edge_asc_from_list(listLine)
            if(edge == None):
                continue
            ProcessTool.dictStrSetstr_add_str_str(dict, edge.start, edge.end)
        return dict

    @classmethod
    def dictEdge_undirected_remove_duplicate(cls, dictEdge):
        dict = {}
        for start in dictEdge:
            for end in dictEdge[start]:
                if(end in dict and start in dict[end]):
                    continue
                ProcessTool.dictStrSetstr_add_str_str(dict, start, end)
        return dict

