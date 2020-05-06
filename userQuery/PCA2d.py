import gensim
from gensim.models import word2vec

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
# 读取模型
word2vec_save = '/Users/rememberthelesson/paper/毕业论文/数据/GoogleNews-vectors-negative300.bin'

# model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_save,binary=True)

# 最相似的2个词语
# print(model.most_similar(positive=['like'], topn=2))




def test():
    # 训练的语料
    sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
                 ['this', 'is', 'the', 'second', 'sentence'],
                 ['yet', 'another', 'sentence'],
                 ['one', 'more', 'sentence'],
                 ['and', 'the', 'final', 'sentence']]

    # 利用语料训练模型
    # sg默认等于0，为CBOW算法，设置为1是Skip-gram算法
    #
    # size是输出词向量的维数，默认100，值太小会导致词映射因为冲突而影响结果，值太大会耗内存并使算法计算变慢，一般取100到200之间
    #
    # window=n是句子中当前词与目标词之间的最大距离，n表示在目标词前看n-b个词，后看b个词（b在0~n直接随机），默认3

    # sample表示更高频率的词被随机下采样到所设置的阈值，默认为1e-3
    #
    # hs默认为0，即negative Sampling，是1的话并且负采样（negative）个数大于0，则是Hierarchical Softmax。
    #
    # negative即使用negaative sampling时负采样的个数，默认是5。推荐在[3，10]之间
    #
    # cbow_mean 仅用于CBOW在做投影的时候，为0，为1（默认）则为上下文的词向量的平均值。不推荐修改。
    #
    # min_count 需要计算词向量的最小词频，默认是5，小语料可调低这个值。
    #
    # iter 随机梯度下降法中迭代的最大次数，默认是5，大语料可增大这个值
    #
    # alpha 在随机梯度下降法中迭代的初始步长，默认是0.025
    #
    # min_alpha 由于算法支持在迭代的过程中逐渐减小步长，min_alpha给出了最小的迭代步长值。随机梯度下降中每轮的迭代步长可以由iter，alpha， min_alpha一起得出。对于大语料，需要对alpha, min_alpha,iter一起调参，来选择合适的三个值。

    model = gensim.models.Word2Vec(sentences, window=5, min_count=1)

    # 基于2d PCA拟合数据
    Xndarray = model[model.wv.vocab]
    words = list(model.wv.vocab)


    word2vecPCA(Xndarray, words)



# 输入模型，输出PCA主成分分析降维
def word2vecPCA(Xndarray, words):

    # 降维
    pca = PCA(n_components=2)
    result = pca.fit_transform(Xndarray)
    # 可视化展示
    plt.scatter(result[:, 0], result[:, 1])
    # for i, word in enumerate(words):
    #     pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
    plt.show()

    return result

# test()