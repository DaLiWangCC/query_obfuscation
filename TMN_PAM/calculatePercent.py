# coding=utf-8

# 计算最大子集的真实查询的百分比
import os

def calculate(filename):
    # filename = "/Users/rememberthelesson/wanghao/Firefox/clusterData/TMN_queries_01_0_2018.12.21_mix100_clusterData.txt"
    file = open(filename)

    max = 0 # 最大的簇
    lastnum = -1
    clusterCount = 0
    tmpUserCount = 0
    userCount = 0 # 全部中有多少是用户的
    allUserCount = 0 # 全部中有多少是用户的

    lineCount = 0

    with file as fh:
        for line in fh:
            lineArr = line.split("\t\t")
            num = lineArr[1]

            if num == lastnum:
                clusterCount += 1
                if lineArr[2] == "user":
                    tmpUserCount += 1
            else:
                if clusterCount > max:
                    # print(lineArr[1], clusterCount, max, tmpUserCount)
                    max = clusterCount
                    userCount = tmpUserCount
                    clusterCount = 1

                if lineArr[2] == "user":
                    tmpUserCount = 1
                else:
                    tmpUserCount = 0
                lastnum = num

            lineCount += 1
            if lineArr[2] == "user":
                allUserCount += 1
    #处理最后一行的问题
    if clusterCount > max:
        # print(lineArr[1], clusterCount, max, tmpUserCount)
        max = clusterCount
        userCount = tmpUserCount


    filename = filename.replace(path,"")

    # 文件名，最大类中user数目，最大类数目，行数，精确率，召回率
    resultStr = "{},{},{},{},{:.3f},{:.3f}".format(filename, tmpUserCount, max, lineCount, tmpUserCount*1.0/max,tmpUserCount*1.0/allUserCount)
    # print(userCount,tmpUserCount,max,lineCount,tmpUserCount*1.0/max)
    print(resultStr)
    file.close()
    # 数据写入文本
    fileStatisticsPath = "/Users/rememberthelesson/wanghao/Firefox/dataforRunning/mywork11.txt"
    fileStatistics = open(fileStatisticsPath,'a')
    fileStatistics.write(resultStr)
    fileStatistics.write('\n')
    # fileStatistics.close()

    return tmpUserCount*1.0/max,tmpUserCount*1.0/allUserCount



path = "/Users/rememberthelesson/wanghao/Firefox/clusterData/mywork_1000/"

# 遍历所有文件
fileCount = 0
sum1 = 0
sum2 = 0
for filename in os.listdir(path):
    if '.txt' in filename:
        # print(filename)
        a,b = calculate(path + filename)
        sum1 += a
        sum2 += b

        fileCount += 1

print("average pre:", sum1*1.0/fileCount,sum2*1.0/fileCount)