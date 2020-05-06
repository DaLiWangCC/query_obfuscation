'''随机选取k-1个虚假查询，计算熵值，作为对照组'''

import random
import numpy as np
# 输入 k
# 所有区域的probability
def findFakeQueries(k,qTree):

    Qf = []
    Hf = 0
    totalQueryCount = 0
    kList = []
    i = 0
    while i < k:
        ii = random.randint(0,len(qTree)-1)
        jj = random.randint(0,len(qTree)-1)
        dic = qTree[ii][jj]
        if dic["count"] > 0 :
            print(dic["count"])
            totalQueryCount += dic["count"]
            kList.append(dic["count"])
            i += 1


    # 随机选取
    # randomList = random.sample(probability,k)

    # 求熵和
    sumEntropy = 0
    for count in kList:
        p = count/totalQueryCount
        if p > 0 :
            print(p)
            sumEntropy +=  - p * np.log2(p)
        else:
            pass
    return sumEntropy,Qf