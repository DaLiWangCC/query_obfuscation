'''计算四叉树，每个区域有多少查询'''

import gensim
import numpy as np
import PCA2d
import TSNE_DR
import sys
import os
import matplotlib.pyplot as plt
import handleQuerySentence
import random
import compareTest
import FileTool
import json

class cal4Tree:

    # 全局变量
    top = 0
    bottom = 0
    right = 0
    left = 0
    celllineNum = 0  # 一条边有多少单元格
    cellLength = 0  # 一个单元多宽
    words = None  # 存储每个查询的查询语句
    vector = None  # 存储每个查询的向量
    qTree = None  # 划分后的查询树
    level_k = 0  # 匿名层次
    global_k = 0  # k匿名
    totalQuery = 0  # 查询总数
    resultStrList = []  # 输出内容存入txt

    def __init__(self):
        pass

    # 初始化
    def init(self, arrayFilePath, labelFilePath, level, k):
        global right
        global left
        global top
        global bottom
        global celllineNum
        global cellLength
        global words
        global vector
        global totalQuery

        self.global_k = k
        self.level_k = level
        vector = np.loadtxt(arrayFilePath, dtype=np.float32)
        words = open(labelFilePath).read().splitlines()
        totalQuery = len(words)
        celllineNum = pow(2, self.level_k)

        # 获取查询边界
        right = int(vector[:, 0].max()) + 1
        left = int(vector[:, 0].min()) - 1
        top = int(vector[:, 1].max()) + 1
        bottom = int(vector[:, 1].min()) - 1

        # 计算边长，取一个正方形范围
        cellLength = max(right - left, top - bottom) / celllineNum

        self.buildQtree()


    # 输入 input: 用户查询，k，Qtree
    # 输出，匿名区域，查询集合
    def findFakeQueries(self, userQuery):
        # 输出的匿名查询集合

        # 找到userQuery在2维空间中的位置
        # 直接通过字典去找，认为它已经在我们要建词库的集合里
        # 目前只能从字典表中取找
        # 找到该查询词的位置
        i = words.index(userQuery)
        x = vector[i][0]
        y = vector[i][1]

        resultStrList = self.calEntropy(x,y)

        return resultStrList


    # 计算附近k个匿名区域的熵值
    def calEntropy(self, x,y):
        x_index, y_index = self.calIndex(x, y)

        # 从 x_index - k
        # 根据k 选择附近的k个区域
        # 从当前节点向左向右分别k个
        print(sys._getframe().f_lineno, x_index, y_index, self.global_k)
        rectangleList = []
        for i in range(x_index - self.global_k + 1, x_index+1): # 满足条件的左边界
            if self.global_k%(x_index - i + 1) != 0: # i 为宽度 必须能够整除i
                continue

            width_min = x_index-i+1  # 满足条件的宽度 width_min 到 global_k

            for width in range(width_min, self.global_k+1):

                if self.global_k%width != 0:
                    continue
                height = self.global_k//width # 宽度定死后 可得而出高度

                for j in range(y_index - height+1, y_index+1):
                    # 此时 左上角为 i,j
                    # 遍历满足条件的宽度, (1, j - y_index)
                    resultRectangele = self.getRectangleList(i,j,width,height)
                    if len(resultRectangele):
                        rectangleList.append(resultRectangele)

        # 计算每个集合的熵
        entropyList = []

        # 存储访问概率到数组
        probabilityList = []
        for cellList in rectangleList: # 矩形区域
            dicSet = {} # 此匿名区域的熵，查询
            dicSet["query"] = []
            sumEntropy = 0

            # 计算cellList中k个区域的查询总数
            cellListSumQuery = 0
            for cell in cellList:  # 矩形区域所有的单元格
                i = cell[0]
                j = cell[1]
                dic = qTree[i][j]
                cellListSumQuery += dic["count"]

            for cell in cellList: #矩形区域所有的单元格

                i = cell[0]
                j = cell[1]
                dic = qTree[i][j]
                # probability = dic["count"] / totalQuery
                probability = dic["count"] / cellListSumQuery # 概率为此单元格中的查询数量/k个单元格内的查询数量

                # 计算熵 概率乘以log(概率)
                if probability > 0:
                    sumEntropy += probability * np.log2(probability)

                    # 从该区域随机选取一个查询，作为对照组
                    oneQuery = random.choice(dic["query"])
                    dicSet["query"].append(oneQuery)

                probabilityList.append(probability)

            dicSet["entropy"] = -sumEntropy # 加个负号取正

            entropyList.append(dicSet.copy())
            dicSet = {}

        # 取出熵最大的集合
        maxSet = max(entropyList,key=lambda a:a["entropy"])
        print(sys._getframe().f_lineno, maxSet["query"])
        print(str(sys._getframe().f_lineno), maxSet["entropy"])


        # 得到熵值和查询集合
        sumEntropy,Qf = compareTest.findFakeQueries(self.global_k, qTree)

        self.resultStrList.append("entropy1," + str(maxSet["entropy"])+ ",entropy2," + str(sumEntropy))


        return  self.resultStrList


    # 根据左上角坐标和宽度，返回长方形的单元格的list
    def getRectangleList(self, x,y,width,height):
        res = []
        for i in range(x,x+width):
            for j in range(y,y+height):
                # i,j不能超出范围，弹出
                if i<0 or i >= celllineNum or j < 0 or j >= celllineNum:
                    return []
                else:
                    res.append([i,j])
        return res


    # 一个查询属于哪个单元格
    def calIndex(self, x,y):
        x_index = min(int((x - left) // cellLength), celllineNum - 1)
        y_index = min(int((top - y) // cellLength), celllineNum - 1)  # 原点在左上
        return x_index,y_index

    # 构建四叉树
    # 输入 查询的向量文件地址， 查询的label文件地址  level
    def buildQtree(self):

        # 对每个区域计算查询数量
        # 遍历所有查询，对固定区域进行计数，每个区域标记count，并存储该区域内的query名称
        # 以多维数组存字典的形式存储，[dic,dic]
        global qTree
        qTree = [[{'count':0,'query':[]} for j in range(celllineNum)] for _ in range(celllineNum)]

        row_num = np.size(vector, 0)  # 计算 vector 一列元素的个数


        for i in range(row_num):
            x = vector[i][0]
            y = vector[i][1]
            # 计算属于哪个坐标
            x_index, y_index = self.calIndex(x,y)

            # 存入对应区域的dic
            dic = qTree[x_index][y_index]
            dic["count"] = dic["count"] + 1
            tmpList = dic["query"]
            tmpList.append(words[i].strip())
            dic["query"] = tmpList

            qTree[x_index][y_index] = dic
        countList = []
        for i in range(celllineNum):
            for j in range(celllineNum):
                dic = qTree[j][i]
                countList.append(dic["count"])

        self.drawPlot(vector, words,countList, left, top ,cellLength, celllineNum)


    def drawPlot(self, vector, words, countList,left, top ,cellLength, celllineNum):
        # 可视化
        plt.figure(figsize=(14, 10))
        plt.scatter(vector[:, 0], vector[:, 1])

        # 只标记部分数据
        wordSubset = words[:100]
        for i, word in enumerate(wordSubset):
            # plt.annotate(word, xy=(vector[i, 0], vector[i, 1]))
            pass



        # 划线
        # xAxis = [left + cellLength*i for i in range(celllineNum)]
        # yAxis = [top - cellLength*i for i in range(celllineNum)]
        #
        # plt.grid()
        # plt.xticks(xAxis)
        # plt.yticks(yAxis)

        # 添加计数文字
        # for i in range(celllineNum):
        #     for j in range(celllineNum):
        #         # 找到单元格的中心
        #         x_c = (j+0.5)*cellLength + left
        #         y_c = top - (i+0.5)*cellLength
        #         plt.text(x_c,y_c,countList[j*celllineNum + i],fontsize = 30,color='r')


        # 标记某一特定用户点为红色
        userFilePath = "data/User_queries_2018.12.all.txt"


        cleanedSentence,newSentence = self.readUserQueryFile(userFilePath)


        sum = 0
        for i, word in enumerate(words):
            sum += 1
            if word.strip() in newSentence[0:200]:
            # if sum < 100:
                plt.scatter(vector[i, 0], vector[i, 1], s=np.pi * 4**2, c='r')


        # 标记锚点为橘黄色

        jsonData = []
        dmozPath = "data/dmoz.json"
        with open(dmozPath, 'r') as f:
            jsonData = json.load(f)

        for i, word in enumerate(words):
            if word.strip() in jsonData:
                plt.scatter(vector[i, 0], vector[i, 1], s=np.pi * 4**2, c='y')


        plt.show()


    # 获得查询词汇
    def readUserQueryFile(self, filePath):
        h = handleQuerySentence.handleQuerySentence()
        h.init()

        cleanedSentence,newSentence = h.readFile(filePath, '\t')
        return cleanedSentence,newSentence







    # init(arrayFilePath, labelFilePath, 5,15)
    # findFakeQueries("u.s.china friction threatens undercut fight climate")
