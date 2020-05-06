# 计算一个txt查询的重复率
# 100个词里面除去重复有多少种
import os

# 全句重复即认为重复
def calculate_1(filename):
    # filename = "/Users/rememberthelesson/wanghao/Firefox/saveData/nothing/User_queries_03_6_2018.12.23"
    # tmnFileName = filename + ".txt"
    # userFileName = filename.replace("TMN", "User") + ".txt"

    userFile = open(filename, 'r')

    userArray = [] #辅助数组
    txtCount = 0
    line = userFile.readline()
    while(line):

        lineArr = line.split('\t\t')
        query = lineArr[1]
        if query not in userArray:
            userArray.append(query)
        else:
            print("重复",query)

        line = userFile.readline()
        txtCount += 1

    # print(len(userArray))
    # print(txtCount)
    return len(userArray),txtCount,len(userArray)*1.0/txtCount



# 两个查询有一个重复词就认为重复
def calculate_2(filename,lineNumber):
    # filename = "/Users/rememberthelesson/wanghao/Firefox/saveData/nothing/User_queries_03_6_2018.12.23"
    # tmnFileName = filename + ".txt"
    # userFileName = filename.replace("TMN", "User") + ".txt"

    userFile = open(filename, 'r')

    userArray = [] #辅助数组
    txtCount = 0
    line = userFile.readline()
    while(line and txtCount < lineNumber):

        lineArr = line.split('\t\t')
        query = lineArr[1]#取出查询

        if len(userArray)<1:
            userArray.append(query)
        else:
            list_c = []
            for fullQuery in userArray:
                queryArr = query.split(' ')#将查询分割为多个关键词
                fullQueryArr = fullQuery.split(' ')
                if len(list_c) <= 0:
                    list_c = [a for a in queryArr if a in fullQueryArr] # 将queryArr 中的每个单词 fullQueryArr中比对，看有没有

            if len(list_c) > 0: # 说明fullQuery和query里面有重复的关键词
                # print(fullQuery,"|", query,"有重复")
                i=0
            else:
                print(fullQuery,"|", query,"没重复")
                userArray.append(query)


        line = userFile.readline()
        txtCount += 1

    # print(len(userArray))
    # print(txtCount)
    return len(userArray),txtCount,len(userArray)*1.0/txtCount


def executeAll(lineNumber):
    # 遍历文件夹中所有

    fileStatisticsPath = "/Users/rememberthelesson/wanghao/Firefox/dataforRunning/statisticRepition_" + str(lineNumber)+".txt"
    fileStatisticsTMNPath = "/Users/rememberthelesson/wanghao/Firefox/dataforRunning/statisticRepitionTMN_" + str(lineNumber)+".txt"

    filePath = "/Users/rememberthelesson/wanghao/Firefox/saveData/nothing/"

    statisticFile = open(fileStatisticsPath, 'w')
    statisticTMNFile = open(fileStatisticsTMNPath, 'w')

    for filename in os.listdir(filePath):
        if '.txt' in filename and 'TMN' in filename:
            # 统计结果写入统计文件
            tmnFileName = filePath + filename
            userFileName = tmnFileName.replace("TMN", "User")


            userArrayLen,userTxtCount,userRRate = calculate_2(userFileName,lineNumber)
            tmnArrayLen,tmnTxtCount,tmnRRate = calculate_2(tmnFileName,lineNumber)

            print(filename,userArrayLen,userTxtCount,userRRate)
            # 文件名，没重复的数组长度，总共多少行，不重复率，重复率
            strLine = 'user ' + filename + ',' + str(userArrayLen) + ',' + str(userTxtCount) + ',' + str(round(userRRate,3)) +","+ str(round(1- userRRate,3))
            statisticFile.write(strLine)
            statisticFile.write('\n')
            strLine = 'tmn ' + filename + ',' + str(tmnArrayLen) + ',' + str(tmnTxtCount) + ',' + str(round(tmnRRate,3))+","+ str(round(1- tmnRRate,3))
            statisticTMNFile.write(strLine)
            statisticTMNFile.write('\n')

    statisticFile.close()
    statisticTMNFile.close()
#
# userArrayLen, userTxtCount, userRRate = calculate_2("/Users/rememberthelesson/wanghao/Firefox/saveData/nothing/User_queries_01_0_2018.12.21.txt")
# print(userArrayLen,userTxtCount,userRRate)

executeAll(50)
executeAll(100)
executeAll(150)
executeAll(250)
executeAll(500)