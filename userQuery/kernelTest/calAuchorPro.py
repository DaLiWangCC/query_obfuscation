import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.neighbors import KernelDensity
import json
import gensim
import os
import random

maxValue = 0
minValue = 0
dirPath = "/Users/rememberthelesson/paper/毕业论文/数据/Firefox/top100分离"
# 读取模型
word2vec_save = '../data/model_60w_1.txt'
# model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_save,binary=True)
model = gensim.models.Word2Vec.load(word2vec_save)


# 获取dmoz词汇
def getDmoz():
    DmozList = []
    dmozPath = "../data/dmoz.json"
    with open(dmozPath, 'r') as f:
        DmozList = json.load(f)

    return DmozList


def getWordVector(word):
    # 读取label 得到index
    # 再从result中读到向量
    # 应该考虑更便利的存储方式，如字典，然后存成json形式
    jsonPath = "../data/label_vector.json"

    # 读取json获得数据
    with open(jsonPath, 'r') as f:
        data = json.load(f)
        return data[word]



# 根据一个用户的个性化查询，进行核密度估计
def getWordPro(dmoz_word,kde,userJson):

    # wordVector = getWordVector(dmoz_word)
    # arrayFilePath = "../data/test2.txt"
    # vector = np.loadtxt(arrayFilePath, dtype=np.float32)

    # X_row = np.size(vector, 0)  # 计算 X 一行元素的个数
    # X_col = np.size(vector, 1)  # 计算 X 一列元素的个数

    # 获取模型
    # kde = getKDE()

    # 计算word到用户每个词的距离 di  similar
    words = userJson["words"][0:100]
    similarValueList = []
    for index in range(len(words)):
        pair = words[index]

        for key, value in pair.items():
            sentence =  key  # 整句
            wordList1 = value # 每个词一个格子的list

        similar_K = []
        k = len(wordList1)

        # 复杂度可能太高
        for word1 in wordList1:
            curSimilar = model.wv.similarity(word1, dmoz_word)
            similar_K.append(curSimilar)

        similar_K.sort()
        similar_K.reverse()
        similarValue = sum(similar_K[0:k]) / k

        similarValueList.append(similarValue)

    # dis = []
    # for i in range(X_row):
    #     vec = vector[i]
    #     # 计算距离，一种是欧拉距离，一种是根据训练的模型得到相似度
    #     di = np.sqrt(np.sum(np.square(vec - wordVector)))
    #     # 对di进行归一化
    #     di = MaxMinNormalization(di,maxValue,minValue)
    #     dis.append([di])

    sumPro = 0

    # 将所有的距离的概率加和
    for di in similarValueList:
        density = np.exp(kde.score([[di]]))
        # 个性化访问概率
        # p = 1/N  * 求和（kde.score）
        # 密度xbandwidth 计算出概率，这里有一定疑问
        probability = density * kde.bandwidth
        sumPro += probability
        # print("di",di)
    averPro = sumPro/len(similarValueList)

    return averPro

# 归一化 0~1的范围
def MaxMinNormalization(x,Max,Min):
    x = (x - Min) / (Max - Min)
    return x


# 获取KDE模型
def getKDE(userJson):
    # arrayFilePath = "../data/test2.txt"
    # vector = np.loadtxt(arrayFilePath, dtype=np.float32)
    #
    # X_row = np.size(vector, 0)  # 计算 X 一行元素的个数
    # X_col = np.size(vector, 1)  # 计算 X 一列元素的个数
    #
    # # 计算出每两个高维向量之间的距离
    # dis = []
    # for i in range(X_row):
    #     vec1 = vector[i]
    #     for j in range(i + 1, X_row):
    #         vec2 = vector[j]
    #         dis_c = np.sqrt(np.sum(np.square(vec1 - vec2)))
    #         dis.append([dis_c])
    words = userJson["words"][0:100]#只选取用户100个查询
    similarValueList = []
    for index in range(len(words)):
        pair = words[index]
        for key, value in pair.items():
            sentence =  key  # 整句
            wordList1 = value # 每个词一个格子的list

        # 两两比较所有words
        for index in range(index+1, len(words)):
            pair2 = words[index]

            for key, value in pair2.items():

                sentence2 = key
                wordList2 = value

            # 比较两个短句的相似度，分拆后两两比较，
            # similarValue = model.similarity(sentence, sentence2)

            # 两两比较两个句子的每个词语之间的相似度，选出 最相似的k个值加权平均，

            similar_K = []
            minlen = min(len(wordList1),len(wordList2)) # 选择小的长度

            # 复杂度可能太高
            for word1 in wordList1:
                for word2 in wordList2:
                    curSimilar = model.wv.similarity(word1,word2)
                    similar_K.append(curSimilar)

            # 选取相似最大的minlen个，求和平均
            similar_K.sort()
            similar_K.reverse()
            similarValue = sum(similar_K[0:minlen])/minlen #

            similarValueList.append(similarValue)


    global maxValue
    global minValue
    maxValue = np.max(similarValueList)
    minValue = np.min(similarValueList)

    # 归一化到 0-1
    # dis3 = MaxMinNormalization(similarValueList, maxValue, minValue)
    dis3 = similarValueList
    # print(dis)
    print(dis3)
    print(len(similarValueList))
    # 标准差
    stdValue = np.std(dis3)

   # -----------------------------------------------------------

    X = [] # 1维变2维
    for item in dis3:
        X.append([item])
    N = len(dis3)
    maxValue3 = np.max(dis3)
    minValue3 = np.min(dis3)

    # 创建等差数列 -5 到 10， N个数 ，作为x坐标轴
    X_plot = np.linspace(minValue3 - 1, maxValue3 + 1, N)[:, np.newaxis]

    # 真实密度

    fig, ax = plt.subplots()

    # 这里需要计算出一个合理的bandwidth
    # bandwidth约等于 1/N^(0.2) * stdValue
    bandwidth = 1 / pow(N, 0.2) * stdValue

    print("bandwidth,N",bandwidth, N)
    # for kernel in ['gaussian', 'tophat', 'epanechnikov']:
    for kernel in ['gaussian']:
        kde = KernelDensity(kernel=kernel, bandwidth=bandwidth).fit(X)  # bandwidth=0.008
        log_dens = kde.score_samples(X_plot)
        exp_dens = np.exp(log_dens)
        ax.plot(X_plot[:, 0], np.exp(log_dens), '-',
                label="kernel = '{0}'".format(kernel))

    ax.text(6, 0.38, "N={0} points".format(N))

    ax.legend(loc='upper left')

    # ax.plot(X[:, 0], -0.005 - 0.01 * np.random.random(X.shape[0]), '+k')

    ax.set_xlim(minValue3, maxValue3)
    ax.set_ylim(-0.02, 10)

    plt.show()

    density = np.exp(kde.score([[0.5]]))
    # 个性化访问概率
    # p = 1/N  * 求和（kde.score）
    # 密度*bandwidth 计算出概率，这里有一定问题  应该是积分
    probability = density * bandwidth
    print(probability)

    return kde


def readUserFile(self, filePath, splitWord):
        file = open(filePath)
        lines = file.readlines()
        # tmn		the heisman vote filled with 		20:04:26   12/7/2018
        # 分离出查询
        sentences = []
        for line in lines:
            querySentence = line.split(splitWord)[1]
            sentences.append(querySentence)
        return sentences
def start():
    # 计算一个用户的kde 熵值
    userJson = {}
    userFileName = "out-top10-01_0.json"
    with open("../data/userJson/" + userFileName, 'r') as f:
        userJson = json.load(f)
    kde = getKDE(userJson)

    calEntropy(kde, userJson)
    return


    # 遍历所有用户
    filePaths = os.listdir("../data/userJson")
    for jsonPath in filePaths:
        userJson = {}
        with open("../data/userJson/" + jsonPath, 'r') as f:
            userJson = json.load(f)

        print(jsonPath)
        kde = getKDE(userJson)

        break         # 计算一个用户的kde


    return





def calEntropy(kde, userJson):
    # 计算每个domz词汇到用户词汇的距离，用kde模型计算概率
    domzList = getDmoz()
    proList = []
    for domzword in domzList:
        domzword = domzword.split(" ")[0]
        pro = getWordPro(domzword, kde, userJson)
        proList.append(pro)
        # print("pro:", pro)

    # 选择概率最高的k个锚点词汇
    proList.sort()
    proList.reverse()

    for k in range(2, 30, 2):
        # k = 2 # 2~30
        proList_k = proList[0:k]

        # 计算k个锚点的熵值
        sumPro = sum(proList_k) # 概率和
        sumEntropy = 0
        for pro in proList_k:
            pro_n = pro / sumPro
            sumEntropy += pro_n * np.log2(pro_n)

        print("entropy",-sumEntropy)

        # 随机选k个锚点的熵值
    for k in range(2, 30, 2):
        randomK = random.sample(proList, k)

        # 计算k个锚点的熵值
        sumPro = sum(randomK)  # 概率和
        sumEntropy = 0
        for pro in randomK:
            pro_n = pro / sumPro
            sumEntropy += pro_n * np.log2(pro_n)

        print("entropy2", -sumEntropy)

start()