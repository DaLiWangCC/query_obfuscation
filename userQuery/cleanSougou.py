# 处理搜狗数据集的数据
# 存储为json格式
import os
import json
import re
import jieba

def readAllfile(dirPath):
        filePaths = os.listdir(dirPath)
        allqueryList = []
        for filePath in filePaths:
            # f = open(path + "/" + filePath)  # 打开文件
            if filePath == '.DS_Store':
                continue

            queryList = readFile(dirPath + "/" + filePath)
            allqueryList.extend(queryList)

        saveToJson(allqueryList)

# 读取单个文件
def readFile(filePath):
    print(filePath)
    f = open(filePath,encoding="gb18030")  # 打开文件
    # lines = f.readlines()
    countLine = 1
    line = f.readline()
    lines = []
    while line:
        countLine += 1
        try:
            line = f.readline()
            lines.append(line)
        except:
            print(countLine)
        # print(countLine)
        # print(line)

    queryList = []
    for line in lines:
        lineArray = line.split('\t')
        userID = lineArray[0]
        # print(lineArray)
        if len(lineArray) <= 2:
            continue
        word = lineArray[1]
        word = word[1:-1]  # 去除查询前后的[]
        queryList.append(userID + "\t" + word) # 用户id \t 查询词

    return queryList


# 把所有用户保持到json里面
def saveToJson(allqueryList):
    dic = {}
    for item in allqueryList:
        userID = item.split("\t")[0]
        word = item.split("\t")[1]
        word_cl = cleantxt(word) # 只保留中文的词汇
        if len(word_cl.strip()) == 0 :
            continue

        if userID not in dic.keys():
            dic[userID] = [word_cl]
        else:
            wordList = dic[userID]
            wordList.append(word_cl)
            dic[userID] = wordList


    with open('data/sogou/sogou_cl_all.json','w') as f :
        json.dump(dic,f)

def firstStep():
    sogouPath = "/Users/rememberthelesson/paper/毕业论文/数据/SogouQ"
    readAllfile(sogouPath)


# 筛选大于1的查询数的用户
def readJson(jsonPath):
    # 计算总查询数
    countAll = 0
    f = open(jsonPath)
    dic = json.load(f)
    dic2 = {}
    for userID in dic.keys():
        countAll += len(dic[userID])
        # print(len(dic[userID]))
        # 将查询数量大于一定数量的用户取出来,重新存一个json
        if len(dic[userID]) > 0:
            dic2[userID] = dic[userID]

    print("user num1", len(dic.keys()))

    with open('data/sogou/sogou_all.json','w') as f :
        json.dump(dic2,f)

    print("user num2 ", len(dic2.keys()))

    print("query num ", countAll)


def secondStep():
    readJson("data/sogou/sogou_cl_all.json")



# 只保留中英文
def cleantxt(raw):

	# fil = re.compile(u'[^0-9a-zA-Z\u4e00-\u9fa5]+', re.UNICODE) # 找出非中英文的词


    fil = re.compile(u'[^\u4e00-\u9fa5]+', re.UNICODE)  # 找出非中文的词 英文，数字 都不要

    return fil.sub(' ', raw) # 用空格替代



# 读取json 数据，清洗查询文本，分词处理
def thirdStep():

    jsonPath = "data/sogou/sogou_all.json"
    f = open(jsonPath)
    dic = json.load(f)
    newDic = {}

    for userID in dic.keys():
        wordList = dic[userID]
        newWordList = []
        for word in wordList:


            seg_list = jieba.cut(word, cut_all=False)
            newWord = " ".join(seg_list)

            newWordList.append(newWord.split(" "))

        newDic[userID] = newWordList

    with open('data/sogou/sogouCL_split_all.json', 'w') as f:
        json.dump(newDic, f)

def fourthStep(jsonPath):

    file = open("data/sogou/stopWord.txt")
    lines = file.readlines()

    stopList = [x.strip() for x in lines]

    f = open(jsonPath)
    dic = json.load(f)
    print(dic)
    newDic = {}
    for userID in dic.keys():
        queryList = dic[userID]
        newqueryList = []
        for query in queryList:
            newquery = [x for x in query if x.strip() != '' and x.strip() not in stopList]
            newqueryList.append(newquery)  # 去除数组中空字符
        newDic[userID] = newqueryList

    with open('data/sogou/sogouCL_split_all_2.json', 'w') as f:
        json.dump(newDic, f) # 最终洗好的数据 json结构  useid:[[query,query],[query]]


jsonPath = 'data/sogou/sogouCL_split_all.json'

# firstStep()
# secondStep()
thirdStep()

fourthStep(jsonPath)

f = open("data/sogou/sogouCL_split_all_2.json")
dic = json.load(f)
print(dic)