'''' 文件读写工具 '''
import sys
resultPath = "data/result/"
# 将result 写入 文件
def writeResult(fileName, resultStrList):
    file = open(resultPath + fileName, 'w')
    for line in resultStrList:

        file.write(line)
        file.write('\n')


# 打印行号
def printLog(line):
    print(str(sys._getframe().f_lineno) + " :"+ line)
