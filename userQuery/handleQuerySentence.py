'''
处理查询短句
训练出全局word2vec
求词语的向量
求短句向量
将短句向量降维
输出
'''
import gensim
import numpy as np
import PCA2d
import TSNE_DR
import nltk
import os
import json


class handleQuerySentence:
    stopwords = []
    lemmatizer = None
    stemmer = None

    def init(self):

        # 去停用词
        stopwordsFile = "data/stopwords.txt"
        self.stopwords = [line.strip() for line in
                     open(stopwordsFile, encoding='utf-8').readlines()]
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.stemmer = nltk.stem.SnowballStemmer('english')

    # 读取文件夹下所有的用户查询
    def readAllFile(self, path):
        filePaths = os.listdir(path)
        allcleanedSentence = []
        allnewSentence = []
        for filePath in filePaths:
            # f = open(path + "/" + filePath);  # 打开文件
            cleanedSentence,newSentence = self.readFile(path + "/" + filePath, '\t')
            allcleanedSentence.extend(cleanedSentence)
            allnewSentence.extend(newSentence)

        return allcleanedSentence, allnewSentence


    # 读取所有查询短句到一个数组
    # 读取原文件，分理出查询词汇
    def readFile(self, filePath, splitWord):
        file = open(filePath)
        lines = file.readlines()
        userDic = {}
        userDic["words"] = []

        # tmn		the heisman vote filled with 		20:04:26   12/7/2018
        # 分离出查询
        sentences = []
        for line in lines:
            querySentence = line.split(splitWord)[1] # 原始词汇
            userId = line.split(splitWord)[0] # 用户id
            userDic["userId"] = userId
            sentences.append(querySentence)

        cleanedSentence = [] # 存放每个短句分离的数组，数组不为空
        newSentence = [] # 存放每个短句空格链接的数组
        for sentence in sentences:
            # 去除 前后空格使用空格分词
            wordsList = sentence.strip().split(' ')

            wordsListFilted = []
            # 去除停用词 word不为空
            for word in wordsList:
                if word not in self.stopwords and len(word):
                    # 词形还原
                    wordsListFilted.append(word)

            if len(wordsListFilted):
                wordsListFilted = self.word_reduction(wordsListFilted)
                # wordsListFilted = word_stemming(wordsListFilted)
                cleanedSentence.append(wordsListFilted)
                newSentence.append(' '.join(wordsListFilted))

                oneItem = {sentence:wordsListFilted}
                userDic["words"].append(oneItem) # dic["what is our ip address"] = [what,is,our,ip,address]
        # json存储用户id，原查询词，处理后的查询词

        jsonPath = "data/userJson/" +filePath.split("/")[-1].replace(".txt",".json")
        with open(jsonPath, 'w') as f:
            json.dump(userDic, f)
        return cleanedSentence,newSentence

    # 保存结果到文本
    def saveFile(self, array, labels):
        # H代表高维 100维度  2代表2维
        np.savetxt("data/result_2_DMOZ_60.txt", array)
        # np.savetxt("data/labels.txt",np.array(labels))
        with open('data/labels_2_DMOZ_60.txt', 'w', encoding='utf-8') as w:
            for line in labels:
                w.write( line +'\n' )
            w.close()

        # 存成json格式
        jsondic = {}
        jsonPath = "data/label_vector_2_60.json"
        for index in range(len(labels)):
            label = labels[index]
            vector = array[index].tolist()
            jsondic[label] = vector

        with open(jsonPath, 'w') as f:
            json.dump(jsondic, f)

    # 训练全局模型
    # sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
    #                  ['this', 'is', 'the', 'second', 'sentence'],
    #                  ['yet', 'another', 'sentence'],
    #                  ['one', 'more', 'sentence'],
    #                  ['and', 'the', 'final', 'sentence']]
    def trainModel(self, cleanedSentence, sentences):
        # 模型训练
        model = gensim.models.Word2Vec(cleanedSentence, window=3, min_count=1)
        # 存储模型
        model.save("data/model_60w_1.txt")
        # 获取所有词语
        words = list(model.wv.vocab)
        # 获取向量
        vector = model[words]

        absMaxList = []
        # 对每个短句，两种方法选其一组成句向量
        # 1.将词向量求和平均
        # 2.取每个维度绝对值最大的值
        for word in cleanedSentence:

            # 求和取平均
            print(word)
            print("@")
            senArray = model[word]
            # 1.取每列的平均值
            meanArray = np.mean(senArray, axis=0)
            # 2.使用每列的绝对值最大值 作为句子向量该列的值
            absMax = self.maxabs(senArray, axis=0) # 每列绝对值最大

            # 3.加和所有词向量
            # sumArray = np.add(senArray, axis=0)

            # newModel[sentence] = absMax

            # 选择使用3种模式之一
            absMaxList.append(absMax)


        mergedArray = np.vstack(absMaxList)
        words = sentences

        # PCA降维
        pca2d = PCA2d.word2vecPCA(mergedArray,words)
        # 降维
        result = TSNE_DR.transE2D(mergedArray, words)

        # 存储降维后的向量
        self.saveFile(result, words)
        # 存储高维向量
        # self.saveFile(absMaxList, words)

        return


    # 合并两个矩阵 取绝对值最大
    def maxabs(self, a, axis=None):
        """Return slice of a, keeping only those values that are furthest away
        from 0 along axis"""
        maxa = a.max(axis=axis)
        mina = a.min(axis=axis)
        p = abs(maxa) >= abs(mina) # bool, or indices where +ve values win
        n = abs(mina) > abs(maxa) # bool, or indices where -ve values win
        if axis == None:
            if p: return maxa
            else: return mina
        shape = list(a.shape)
        shape.pop(axis)
        out = np.zeros(shape, dtype=a.dtype)
        out[p] = maxa[p]
        out[n] = mina[n]
        return out

    # 计算短句的高维向量
    # 1.求和平均   2.取每个维度词向量最大的值


    # 词形还原
    def word_reduction(self,word_list):
        words = [self.lemmatizer.lemmatize(word) for word in word_list]
        return words

    # 词干化
    def word_stemming(self, word_list):
        words = [self.stemmer.stem(word) for word in word_list]
        return words


# cleanedSentence,sentences = readFile("data/User_queries_2018.12.all.txt")
#
# trainModel(cleanedSentence,sentences)


