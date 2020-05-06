# 计算模型

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.neighbors import KernelDensity

arrayFilePath = "../data/test3.txt"
vector = np.loadtxt(arrayFilePath, dtype=np.float32)

print(vector)

# 归一化sigmod
def sigmoid(X,useStatus):
    if useStatus:
        return 1.0 / (1 + np.exp(-float(X)))
    else:
        return float(X)

# 归一化 0~1的范围

def MaxMinNormalization(x,Max,Min):
    x = (x - Min) / (Max - Min)
    return x


X_row=np.size(vector,0)  #计算 X 一行元素的个数
X_col=np.size(vector,1)  #计算 X 一列元素的个数


# 计算出每两个高维向量之间的距离
dis = []
dis2 = []
for i in range(X_row):
    vec1 = vector[i]
    for j in range(i+1,X_row):
        vec2 = vector[j]
        dis_c = np.sqrt(np.sum(np.square(vec1 - vec2)))
        dis_cs = sigmoid(dis_c,1)
        dis.append([dis_c])
        dis2.append(dis_cs)

maxValue = np.max(dis)
minValue = np.min(dis)

# dis3 = map(MaxMinNormalization(),dis,maxValue,minValue)
dis3 = MaxMinNormalization(dis,maxValue,minValue)
# print(dis)
print(dis3)
print(len(dis))
# 标准差
stdValue = np.std(dis3)

print(stdValue)


# Plot all available kernels
X_plot = np.linspace(-6, 6, 1000)[:, None]
X_src = np.zeros((1, 1))

fig, ax = plt.subplots(2, 3, sharex=True, sharey=True)
fig.subplots_adjust(left=0.05, right=0.95, hspace=0.05, wspace=0.05)


def format_func(x, loc):
    if x == 0:
        return '0'
    elif x == 1:
        return 'h'
    elif x == -1:
        return '-h'
    else:
        return '%ih' % x

for i, kernel in enumerate(['gaussian', 'tophat', 'epanechnikov',
                            'exponential', 'linear', 'cosine']):
    axi = ax.ravel()[i]
    log_dens = KernelDensity(kernel=kernel).fit(X_src).score_samples(X_plot)
    axi.fill(X_plot[:, 0], np.exp(log_dens), '-k', fc='#AAAAFF')
    axi.text(-2.6, 0.95, kernel)

    axi.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    axi.xaxis.set_major_locator(plt.MultipleLocator(1))
    axi.yaxis.set_major_locator(plt.NullLocator())

    axi.set_ylim(0, 1.05)
    axi.set_xlim(-2.9, 2.9)

ax[0, 1].set_title('Available Kernels')

#----------------------------------------------------------------------
# Plot a 1D density example
N = 100
np.random.seed(1)
X = np.concatenate((np.random.normal(0, 1, 30),
                    np.random.normal(5, 1, 70)))[:, np.newaxis]

X = np.array(dis)
N = len(dis)

X = dis3
maxValue3 = np.max(dis3)
minValue3 = np.min(dis3)

# 创建等差数列 -5 到 10， 1000个数
X_plot = np.linspace(minValue3-1, maxValue3+1, N)[:, np.newaxis]


# 真实密度
true_dens = (0.3 * norm(0, 1).pdf(X_plot[:, 0])
             + 0.7 * norm(5, 1).pdf(X_plot[:, 0]))

fig, ax = plt.subplots()
ax.fill(X_plot[:, 0], true_dens, fc='black', alpha=0.2, label='input distribution')



# 这里需要计算出一个合理的bandwidth
# bandwidth约等于 1/N^(0.2) * stdValue
bandwidth = 1/pow(N,0.2) * stdValue

print("bandwidth")
print(bandwidth,N)
# for kernel in ['gaussian', 'tophat', 'epanechnikov']:
for kernel in ['gaussian']:

    kde = KernelDensity(kernel=kernel, bandwidth=bandwidth).fit(X)  # bandwidth=0.008
    log_dens = kde.score_samples(X_plot)
    exp_dens = np.exp(log_dens)
    ax.plot(X_plot[:, 0], np.exp(log_dens), '-',
            label="kernel = '{0}'".format(kernel))

ax.text(6, 0.38, "N={0} points".format(N))

ax.legend(loc='upper left')

ax.plot(X[:, 0], -0.005 - 0.01 * np.random.random(X.shape[0]), '+k')

ax.set_xlim(minValue3, maxValue3)
ax.set_ylim(-0.02, 10)

plt.show()

density = np.exp(kde.score([[0.5]]))
# 个性化访问概率
# p = 1/N  * 求和（kde.score）
# 密度xbandwidth 计算出概率，这里有一定疑问
probability = density*bandwidth
print(probability)
