# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import copy
import calculatePercent
import os


def mydraw(fileName):
    readFile = open(fileName)
    line = readFile.readline()
    dicOneLineArray = []
    oldList = []
    dataArray = []# 把文档读取为二维数组

    while (line):
        values = line.split('\t\t')
        number = int(values[0])  # 原先所在的index
        type = values[2]
        dicOneLine = {}
        dicOneLine["type"] = type
        dicOneLine["cluster"] = values[1]
        dicOneLine["query"] = values[3]
        dicOneLineArray.append(dicOneLine)

        #
        oldList.append(number)
        sim = values[4].strip().split(',')
        simArray = map(float, sim)
        dataArray.append(simArray)
        line = readFile.readline()
        # 这里做了一个替换，聚类之前的对应关系

    for sim in dataArray:
        tempSim = copy.copy(sim)
        for i in range(0, len(sim) - 1):
            sim[i] = tempSim[oldList[i]]

    # 为了画出tmn和用户的不同
    dataArrayTmnUser = copy.deepcopy(dataArray)
    for i in range(0, len(dataArrayTmnUser) - 1):
        dic = dicOneLineArray[i]
        if dic["type"] == "tmn":
            dataArrayTmnUser[i][i] = 2;
        elif dic["type"] == "user":
            dataArrayTmnUser[i][i] = 1.5;

    # 为了画出不同的聚类分割的不同
    dataArrayCluster = copy.deepcopy(dataArray)

    startCluster = 0
    endCluster = 0
    lastCluster = 0
    for i in range(0, len(dataArrayCluster)):
        dic = dicOneLineArray[i]
        if lastCluster != dic["cluster"] or i == len(dataArrayCluster) - 1:
            endCluster = i
            lastCluster = dic["cluster"]
            # 画框框
            for j in range(startCluster, endCluster):
                dataArrayCluster[startCluster][j] = 3.5;
                dataArrayCluster[endCluster][j] = 3.5;
                dataArrayCluster[j][startCluster] = 3.5;
                dataArrayCluster[j][endCluster] = 3.5;
            startCluster = i

    # data = np.mat(data)

    # WeightMesh=np.array(AyMesh*AxMesh, dtype=float)

    plt.imshow(dataArray, interpolation='nearest', cmap='bone', origin='upper')
    # 根据像素绘制图片 origin表示渐变程度
    plt.colorbar()
    # 显示像素与数据对比
    plt.xticks(())
    plt.yticks(())
    # 不显示坐标轴刻度

    # 画第二个覆盖的图，对角线
    # data2 = [[1,0,0],[0,1,0],[0,0,1]]
    bounds = [-1, 1.1, 1.6, 2.5, 3.5]
    cmap = colors.ListedColormap(['none', 'blue', 'red', 'yellow'])

    norm = colors.BoundaryNorm(bounds, cmap.N)
    plt.imshow(dataArrayTmnUser, interpolation='nearest', cmap=cmap, origin='upper', norm=norm)
    plt.imshow(dataArrayCluster, interpolation='nearest', cmap=cmap, origin='upper', norm=norm)

    plt.show()

    # 最大类中的计算精确率
    print("precision: ", calculatePercent.calculate(fileName))



def str2float(s):
    # 把小数点后面的数字转化成 0.xxx 的值，t 为小数的位数
    def decimalize(n, t):
        while t > 0:
            n = n / 10
            t = t - 1
        return n
    # 获得小数点的位置
    pos = s.find('.')
    if pos == -1:
        return s
    else:
        return int(s[:pos]) + decimalize(int(s[pos + 1:]), len(s[pos + 1:]))


# fileName = 'user_02_100_sim_ready_cluster.txt'
fileName = 'TMN_queries_01_0_2018.12.21_mix100_clusterData.txt'
fileName = '/Users/rememberthelesson/wanghao/Firefox/clusterData/origin_15_1/TMN_queries_01_6_2018.12.16_mix200_clusterData.txt'

mydraw(fileName)

dirPath = "/Users/rememberthelesson/wanghao/Firefox/clusterData/origin_15_1/"
fileNameList = os.listdir(dirPath)
for fileName in fileNameList:
    fileNamePath = dirPath + fileName
    # mydraw(fileNamePath)

