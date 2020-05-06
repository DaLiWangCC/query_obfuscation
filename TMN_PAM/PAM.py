# coding=utf-8
import random
from numpy import *


def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split()
        fltLine = map(float, curLine)  # transfer to float
        dataMat.append(fltLine)
    return dataMat

#
def pearson_distance(vector1, vector2):
    from scipy.spatial.distance import pdist
    X = vstack([vector1, vector2])
    d2 = pdist(X)
    return d2


distances_cache = {}


def totalcost(blogwords, costf, medoids_idx):
    size = len(blogwords)
    total_cost = 0.0
    medoids = {}
    for idx in medoids_idx:
        medoids[idx] = []
    for i in range(size):
        choice = None
        min_cost = inf
        for m in medoids:
            tmp = distances_cache.get((m, i), None)
            if tmp == None:
                tmp = pearson_distance(blogwords[m], blogwords[i])
                distances_cache[(m, i)] = tmp
            if tmp < min_cost:
                choice = m
                min_cost = tmp
        medoids[choice].append(i)
        total_cost += min_cost
    return total_cost, medoids


def kmedoids(blogwords, k):
    import random
    size = len(blogwords)
    # 随机选择k个点为中心
    medoids_idx = random.sample([i for i in range(size)], k)
    # 计算SDA
    pre_cost, medoids = totalcost(blogwords, pearson_distance, medoids_idx)
    print(pre_cost)
    current_cost = inf  # maxmum of pearson_distances is 2.
    best_choice = []
    best_res = {}
    iter_count = 0
    while 1:
        for m in medoids:
            for item in medoids[m]:
                if item != m:
                    idx = medoids_idx.index(m)
                    swap_temp = medoids_idx[idx]
                    medoids_idx[idx] = item
                    tmp, medoids_ = totalcost(blogwords, pearson_distance, medoids_idx)
                    # print tmp,'-------->',medoids_.keys()
                    if tmp < current_cost:
                        best_choice = list(medoids_idx)
                        best_res = dict(medoids_)
                        current_cost = tmp
                    medoids_idx[idx] = swap_temp
        iter_count += 1
        print(current_cost, iter_count)
        if best_choice == medoids_idx: break
        if current_cost <= pre_cost:
            pre_cost = current_cost
            medoids = best_res
            medoids_idx = best_choice

    return current_cost, best_choice, best_res


# 画图工具
def show(dataSet, k, centroids, clusterAssment):
    from matplotlib import pyplot as plt
    numSamples, dim = dataSet.shape
    mark =  ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr', 'xr', 'sb', 'sg', 'sk', '2r', '<b', '<g', '+b', '+g', 'pb']
    for i in range(numSamples):
        # markIndex = int(clusterAssment[i, 0])
        for j in range(len(clusterAssment)):
            if i in clusterAssment[clusterAssment.keys()[j]]:
                plt.plot(dataSet[i, 0], dataSet[i, 1], mark[j])
    #mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb', 'or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    #for i in range(k):
        #plt.plot(centroids[i][0, 0], centroids[i][0, 1], mark[i], markersize=12)
    plt.show()


def getDataset(filename, k_sample):
    import linecache
    import random
    dataMat = []
    myfile = open(filename)
    lines = len(myfile.readlines())

    #从序列i到lines中选择k_sample个随机且独立的元素；
    SampleLine = random.sample([i for i in range(lines)], k_sample)
    for i in SampleLine:
        # 读取特定一行
        theline = linecache.getline(filename, i)
        # 删除开头结尾的空白符（包括'\n', '\r',  '\t',  ' ')，再返回数组
        curLine = theline.strip().split()
        # transfer to float
        fltLine = map(float, curLine)
        dataMat.append(fltLine)
    return dataMat

if __name__ == '__main__':
    dataMat = getDataset('R15.txt',150)
    best_cost, best_choice, best_medoids = kmedoids(dataMat, 15)

    #转化为矩阵
    dataMat = mat(dataMat)
    listone = []
    for i in range(len(best_choice)):
        listone.append(dataMat[best_choice[i]])
    show(dataMat, 15, listone, best_medoids)
