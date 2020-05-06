'''transe 降维'''
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt
import random
import gensim

# 因为词向量文件比较大，全部可视化就什么都看不见了，所以随机抽取一些词可视化

sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
			['this', 'is', 'the', 'second', 'sentence'],
			['yet', 'another', 'sentence'],
			['one', 'more', 'sentence'],
			['and', 'the', 'final', 'sentence']]



def transE2D(Xndarray, words):
    #

    tsne = TSNE(n_components=2, init='pca', verbose=1)
    result = tsne.fit_transform(Xndarray)

    # 可视化
    plt.figure(figsize=(14, 10))
    plt.scatter(result[:, 0], result[:, 1])

    # 只标记部分数据
    wordSubset = words[:100]
    for i, word in enumerate(wordSubset):
        plt.annotate(word, xy=(result[i, 0], result[i, 1]))
    plt.show()

    return result


def test():
    # 训练的语料
    sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
                 ['this', 'is', 'the', 'second', 'sentence'],
                 ['yet', 'another', 'sentence'],
                 ['one', 'more', 'sentence'],
                 ['and', 'the', 'final', 'sentence']]

    # 利用语料训练模型

    model = gensim.models.Word2Vec(sentences, window=5, min_count=1)

    # 基于2d PCA拟合数据
    Xndarray = model[model.wv.vocab]
    words = list(model.wv.vocab)
    transE2D(Xndarray, words)
# test()