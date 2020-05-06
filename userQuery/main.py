import handleQuerySentence
import cal4Tree
import json
import FileTool


dirPath = "/Users/rememberthelesson/paper/毕业论文/数据/Firefox/top100分离"


arrayFilePath = "data/result3.txt" # 60w
labelFilePath = "data/labels3.txt"

arrayFilePath = "data/result_2_DMOZ_60.txt"  # 5000
labelFilePath = "data/labels_2_DMOZ_60.txt"



# 将domz中的停用词 and 去除
# 如果有多个词汇，就分开
def handleDmoz():
    pass

def trainModel():
    hand = handleQuerySentence.handleQuerySentence()
    hand.init()

    # 训练Word2vec
    # cleanedSentence, sentences = hand.readFile("data/User_queries_2018.12.all.txt","\t\t")
    #cleanedSentence, sentences = hand.readAllFile(dirPath)
    cleanedSentence = []
    sentences =[]
    # 加入dmoz的词语进行训练
    # 读取json
    jsonData = []
    dmozPath = "data/dmoz.json"
    with open(dmozPath, 'r') as f:
        jsonData = json.load(f)

    # print(data)
    sentences.extend(jsonData)
    print(sentences[-10:-1])
    for word in jsonData:
        wordList = word.split(" ")
        # 只取第一个单词进行训练，省去处理停用词
        cleanedSentence.append(wordList[0:1])

    hand.trainModel(cleanedSentence, sentences)

    return


def findFQ():


    # 比较不同的k值和level值输出的结果
    cal = cal4Tree.cal4Tree()
    # for i in range(1):
    level = 5
    k = 5

    # 初始化
    cal.init(arrayFilePath, labelFilePath, level, k)


    # for j in range(6,24,2):
    cal.global_k = k
    # 查找虚假查询
    # resultStrList = cal.findFakeQueries("u.s.china friction threatens undercut fight climate")

    resultStrList = cal.findFakeQueries('meat lent patrick')
    resultfileName = "result_" + str(level) + '_' + str(k) #str(int(time.time()))
    FileTool.writeResult(resultfileName, resultStrList)
    resultStrList=[]

    cleanedSentence, sentences = handleQuerySentence.readAllFile(dirPath)
    handleQuerySentence.trainModel(cleanedSentence, sentences)


if __name__ == '__main__':
    trainModel()
    # findFQ()



