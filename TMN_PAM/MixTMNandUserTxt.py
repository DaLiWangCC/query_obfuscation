# coding=utf-8

import os

#
# print('参数个数为:', len(sys.argv), '个参数。')
# print('参数列表:', str(sys.argv))

#计算重复率
def calculateRepitition(filename):

    userFile = open(filename, 'r')

    userArray = [] #辅助数组
    txtCount = 0
    line = userFile.readline()
    while(line):

        lineArr = line.split('\t\t')
        query = lineArr[1]
        if query not in userArray:
            userArray.append(query)

        line = userFile.readline()
        txtCount += 1

    # print(len(userArray))
    # print(txtCount)
    return len(userArray),txtCount,len(userArray)*1.0/txtCount



# filename = str(sys.argv[0])
filePath = "/Users/rememberthelesson/wanghao/Firefox/saveData/similar/"
fileMixPath = "/Users/rememberthelesson/wanghao/Firefox/saveData/similar/mix/"
fileStatisticsPath = "/Users/rememberthelesson/wanghao/Firefox/dataforRunning/statisticMix.txt"

tmnFileName = filePath+".txt"
userFileName = filePath.replace("TMN","User")+".txt"


# 遍历文件夹中所有
statisticFile = open(fileStatisticsPath, 'w')
for filename in os.listdir(filePath):
    if '.txt' in filename and 'TMN' in filename:
        # 统计结果写入统计文件
        tmnFileName = filePath + filename
        userFileName = tmnFileName.replace("TMN", "User")

        userArrayLen,userTxtCount,userRRate = calculateRepitition(userFileName)
        tmnArrayLen,tmnTxtCount,tmnRRate = calculateRepitition(tmnFileName)

        print(filename,userArrayLen,userRRate)

        strLine = filename + ',' + str(userArrayLen) + ',' + str(userTxtCount) + ',' + str(round(userRRate,3)) + ',' + str(tmnArrayLen) + ',' + str(tmnTxtCount) + ',' + str(round(tmnRRate,3))
        statisticFile.write(strLine)
        statisticFile.write('\n')

statisticFile.close()


# 把每两个tmn和user 合并成100 200 300 500 1000

for filename in os.listdir(filePath):
    if '.txt' in filename and 'TMN' in filename:
        tmnFileName = filePath + filename
        userFileName = tmnFileName.replace("TMN", "User")
        # mixFileName = fileMixPath + filename

        print(filename)

        tmnFile = open(tmnFileName, 'r')
        userFile = open(userFileName, 'r')

        # 分到不同文件夹
        # filename100 = (filePath+"mix100/"+filename).replace('.txt','_mix100.txt')
        # filename200 = (filePath+"mix200/"+filename).replace('.txt','_mix200.txt')
        # filename300 = (filePath+"mix300/"+filename).replace('.txt','_mix300.txt')
        # filename500 = (filePath+"mix500/"+filename).replace('.txt','_mix500.txt')
        # filename1000 = (filePath+"mix1000/"+filename).replace('.txt','_mix1000.txt')

        filename100 = (fileMixPath  + filename).replace('.txt', '_mix100.txt')
        filename200 = (fileMixPath  + filename).replace('.txt', '_mix200.txt')
        filename300 = (fileMixPath  + filename).replace('.txt', '_mix300.txt')
        filename500 = (fileMixPath  + filename).replace('.txt', '_mix500.txt')
        filename1000 = (fileMixPath  + filename).replace('.txt', '_mix1000.txt')


        file100 = open(filename100, 'w')
        file200 = open(filename200, 'w')
        file300 = open(filename300, 'w')
        file500 = open(filename500, 'w')
        file1000 = open(filename1000, 'w')

        for i in range(0, 1000):
            tmnLine = tmnFile.readline()
            userLine = userFile.readline()

            if i < 50:
                file100.write(tmnLine)
                file100.write(userLine)
            if i < 100:
                file200.write(tmnLine)
                file200.write(userLine)
            if i < 150:
                file300.write(tmnLine)
                file300.write(userLine)
            if i < 250:
                file500.write(tmnLine)
                file500.write(userLine)
            if i < 500:
                file1000.write(tmnLine)
                file1000.write(userLine)
