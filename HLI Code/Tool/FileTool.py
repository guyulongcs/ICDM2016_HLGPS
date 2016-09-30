#-*- encoding:utf-8 -*-_

from os import listdir
from ProcessTool import *
from InOut import *


from TypeTool import *

class FileTool():
    def __init__(self):
        pass

    @classmethod
    def ReadFolderFileList(cls, path):
        return listdir(path)

    @classmethod
    def ReplaceLineListSplit(cls, lineList, splitOld, splitNew):
        lineListNew=[]
        for line in lineList:
            lineNew = line.replace(splitOld, splitNew)
            lineListNew.append(lineNew)
        return lineListNew

    @classmethod
    def ReplaceLineListSplitNorm(cls, lineList, splitOld, splitNew):
        lineListNew=[]
        for line in lineList:
            list = line.split(splitOld)
            listNorm = []
            for item in list:
                itemNorm = item.strip()
                listNorm.append(itemNorm)
            lineNew = splitNew.join(listNorm)
            lineListNew.append(lineNew)
        return lineListNew

    @classmethod
    def WriteStrListToFile(cls, strList, file):
        with open(file, 'w') as fout:
            fout.writelines(strList);
        fout.close();
    
    @classmethod
    def WriteStrListToFileWithNewLine(cls, strList, file):
        with open(file, 'w') as fout:
            for line in strList:
                line = "%s\n" % line;
                fout.write(line);
        fout.close();

    @classmethod
    def WriteListLineListToFileWithNewLine(cls, listLineList, file, connStr="\t"):
        lineList = TypeTool.listLineList_to_linelist(listLineList, connStr)
        FileTool.WriteStrListToFileWithNewLine(lineList, file)

    @classmethod
    def ReadLineListFromFile(cls, file, skipLineCnt=0):
        lines = [];
        with open(file, 'r') as fin:
            lines = fin.readlines();

        i=0;
        lineRes = [];
        for line in lines:
            i=i+1;
            if(skipLineCnt > 0 and i <= skipLineCnt):
                continue;
            lineNew = line.strip('\n');
            lineRes.append(lineNew);

        return lineRes;

    @classmethod
    def ReadListLineListFromFile(cls, file, skipLineCnt=0, splitCh='\t'):
        lines = [];
        with open(file, 'r') as fin:
            lines = fin.readlines();

        i=0;
        lineRes = [];
        for line in lines:
            i=i+1;
            if(skipLineCnt > 0 and i <= skipLineCnt):
                continue;
            lineNew = line.strip('\n');
            list = lineNew.split(splitCh)
            lineRes.append(list);

        return lineRes;
    
    @classmethod
    def SplitFileByColLimit(cls, file, fileLess, fileMore, splitChar, colIndex, upperLimit):
        lineList = FileTool.ReadLineListFromFile(file);
        
        lineLessList = [];
        lineMoreList = [];
        for line in lineList:
            arr = line.split(splitChar);
            if(len(arr) < colIndex):
                continue;
            if(arr[colIndex] < upperLimit):
                lineLessList.append(line);
            else:
                lineMoreList.append(line);
                
        FileTool.WriteStrListToFileWithNewLine(lineLessList, fileLess);
        FileTool.WriteStrListToFileWithNewLine(lineMoreList, fileMore);

    @classmethod
    def ReadFileDictStrStr(cls, file, colKeyIndex, colValueIndex, skipLine = 0, splitCh='\t'):
        d = {}
        listLineList = FileTool.ReadListLineListFromFile(file, skipLine, splitCh)
        for listLine in listLineList:
            key = listLine[colKeyIndex]
            value = listLine[colValueIndex]
            d[key] = value
        return d

    @classmethod
    def ReadFileDictIntInt(cls, file, colKeyIndex, colValueIndex, skipLine = 0, splitCh='\t'):
        d = FileTool.ReadFileDictStrStr(file, colKeyIndex, colValueIndex, skipLine, splitCh)
        res = {}
        for key in d:
            value = d[key]
            ikey = TypeTool.str_to_int(key)
            ivalue = TypeTool.str_to_int(value)
            res[ikey] = ivalue

        return res


    @classmethod 
    def GetFileColumnDict(cls, file, splitChar, colIndex, dictCol):
        list = FileTool.GetFileColumnList(file, splitChar, colIndex)
        
        #dictCol = {};
        index = 0;
        for item in list:
            if(dictCol.has_key(item) == False):
                index = index + 1;
                dictCol[item] = index;
    
        pass;
    
    @classmethod
    def GetFileBinaryMatrix(cls, file, fileRes, mRowIndex, mColIndex, dictRowKeyId, dictColKeyId):
                
        rowCnt = len(dictRowKeyId.keys());
        colCnt = len(dictColKeyId.keys());
        dictMatrix = FileTool.genMatrix(rowCnt, colCnt);
        pass;
                
    @classmethod
    def genMatrix(cls, rows,cols):  
        matrix = [[0 for col in range(cols)] for row in range(rows)]  
        for i in range(rows):  
            for j in range(cols):  
                print matrix[i][j],  
                print '\n'  
                
        return matrix;


    @classmethod
    def ReadFileColumnList(cls, file, splitChar='\t', colIndex=0):
        lines = FileTool.ReadLineListFromFile(file);
        list = [];
        for line in lines:
            line = line.strip('\n');
            arr = line.split(splitChar);
            if(len(arr) < colIndex+1):
                continue;
            list.append(arr[colIndex]);
        return list;

    @classmethod
    def ReadFileColumnSet(cls, file, splitChar='\t', colIndex=0):
        list = FileTool.ReadFileColumnList(file, splitChar, colIndex)
        res = set(list)
        return res

    @classmethod
    def ReadFileColumnSetInt(cls, file, splitChar='\t', colIndex=0):
        list = FileTool.ReadFileColumnList(file, splitChar, colIndex)
        res = set(list)
        res = TypeTool.setstr_to_setint(res)
        return res

    @classmethod
    def printDictIntInt(cls, dictIntInt):
        for (key,value) in dictIntInt.items():
            line = "%s\t%s" % (key,value);
            print line;

    @classmethod
    def FiltFileByColInSet(cls, srcFile, dstFile, colIndex, filtSet, skipLineCnt=0, splitChar='\t'):
        InOut.console_func_begin("FiltFileByColInSet")
        listLineList = FileTool.ReadListLineListFromFile(srcFile, skipLineCnt, splitChar)
        listRes = []
        for listLine in listLineList:
            if(listLine[colIndex] in filtSet):
                listRes.append(listLine)
        print "src:", len(listLineList)
        print "res:", len(listRes)
        FileTool.WriteListLineListToFileWithNewLine(listRes, dstFile)

    @classmethod
    def FiltFileByTwoColAtleastOneInSet(cls, srcFile, dstFile, colIndex1, colIndex2, filtSet, skipLineCnt=0, splitChar='\t'):
        listLineList = FileTool.ReadListLineListFromFile(srcFile, skipLineCnt, splitChar)
        listRes = []
        for listLine in listLineList:
            if(listLine[colIndex1] in filtSet or listLine[colIndex2] in filtSet):
                listRes.append(listLine)
        FileTool.WriteListLineListToFileWithNewLine(listRes, dstFile)

    @classmethod
    def FiltFileByTwoColAllInSet(cls, srcFile, dstFile, colIndex1, colIndex2, filtSet, skipLineCnt=0, splitChar='\t'):
        listLineList = FileTool.ReadListLineListFromFile(srcFile, skipLineCnt, splitChar)
        listRes = []
        for listLine in listLineList:
            if(listLine[colIndex1] in filtSet and listLine[colIndex2] in filtSet):
                listRes.append(listLine)
        FileTool.WriteListLineListToFileWithNewLine(listRes, dstFile)

    @classmethod
    def CopyFile(cls, srcFile, dstFile):
        lineList = FileTool.ReadLineListFromFile(srcFile)
        FileTool.WriteStrListToFileWithNewLine(lineList, dstFile)

