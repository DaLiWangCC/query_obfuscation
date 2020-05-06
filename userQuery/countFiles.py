
import os

userIDDic = {} # 统计搜狗中有多少不重复的userid，将同一用户的查询单独生成一个文件

# 读取所有的用户查询
def readAllFile(path):
    filePaths = os.listdir(path)
    allcleanedSentence = []
    allnewSentence = []
    sumCount = 0
    qCount = 0
    for filePath in filePaths:
        # f = open(path + "/" + filePath);  # 打开文件
        # cleanedSentence,newSentence = readFile(path + "/" + filePath)
        # allcleanedSentence.extend(cleanedSentence)
        # allnewSentence.extend(newSentence)

        lineCount = readFile(path + "/" + filePath)
        # 记录总查询数量
        qCount += lineCount
    # 记录用户数量
    sumCount+=len(userIDDic.keys())
    print(sumCount, qCount)
    writeFile()
    return allcleanedSentence, allnewSentence


def readFile(filePath):
    global userIDDic
    file = open(filePath,'rb')
    print(filePath)
    lines = file.readlines()
    # AOL：tmn		the heisman vote filled with 		20:04:26   12/7/2018
    # 搜狗：062050989872388496	[好男儿]	1 1	ent.sina.com.cn/f/v/myhero/index.shtml
    # 用户ID\t[查询词]\t该URL在返回结果中的排名\t用户点击的顺序号\t用户点击的URL
    # 分离出查询
    sentences = []
    for line in lines:
        print(line)
        try:
            lineDe = line.decode('GB18030') # GB18030解决繁体字问题
            lineArray = lineDe.split('\t')
            querySentence = lineArray[1][1:-1]
            # sentences.append(querySentence)
            print(querySentence)
            userid = lineArray[0]
            dic= {}
            if userid in userIDDic.keys():
                dic = userIDDic[userid]
                dic["count"] += 1
                dic["query"].append(querySentence)
            else:
                dic["count"] = 1
                dic["query"] = [querySentence]
            userIDDic[userid] = dic
        except Exception as e:
            print(filePath)
            print(line)
            print('Error:', e)

    return len(lines)

# 将字典写入文件
def writeFile():
    for key in userIDDic.keys():
        file = open("/Users/rememberthelesson/paper/毕业论文/数据/SogouQS/" + key+".txt",'w')
        for query in userIDDic[key]["query"]:
            file.write(query)
            file.write('\n')
        file.close()


readAllFile("/Users/rememberthelesson/paper/毕业论文/数据/SogouQ2")