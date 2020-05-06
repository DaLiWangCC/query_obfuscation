import math
import time
import hashlib
def f(n,x):

    #n为待转换的大数，全部是整数，并且用字符串保存，x为进制，取值为2-16
    a=[0,1,2,3,4,5,6,7,8,9,'A','b','C','D','E','F']
    b=[]
    while True:
        jinwei=0
        shang=''
        for i in n:
            beichushu=int(i)+jinwei*10

            s=beichushu//x
            y=beichushu%x
            shang=shang+str(s)
            jinwei=int(y)
        b=b+[jinwei]

        if int(shang)==0:
            break
        n=shang
    b.reverse()
    for i in b:
        print(a[i],end='')
    print('('+str(x)+'x)')

f = f('10241111111111111111111111111111111111',16)

print(f)





str =  "00000f96a08c30a579c823bd3e253ad0f21dc30039866e6501b3150bcd25ec83"

a = hex(1111111111111111111111111111111111111111111111111111111111111111)

b = hex(12322323)

a = int(a, 16)
b = int(b, 16)
c = int(a/b)

print(hex(c))

difficulty = 1492634.8754
ff = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
fs = "b3d70a3d87d7f800000000000000000000000000000000000000000"
ff_int = int(ff, 16)
target = hex(int(ff_int / difficulty))

print(target)


a = time.time()
print(a)


def NewMerkleNode(leftNode, rightNode, data):
    newNode = {}
    if leftNode == None and rightNode == None:
#        hash = hashlib.sha256(data).hexdigest()
        s1 = hashlib.md5()
        s1.update(data.encode("utf8"))  # 指定编码格式，否则会报错
        hash = s1.hexdigest()

        newNode['Data'] = hash[:]
    else:
        prevHashes = leftNode['Data'] + rightNode['Data']
        hashlib.md5().update(prevHashes.encode("utf8"))
        # hash = hashlib.sha256(prevHashes).hexdigest()
        s1 = hashlib.md5()
        s1.update(prevHashes.encode("utf8"))  # 指定编码格式，否则会报错
        hash = s1.hexdigest()
        newNode['Data'] = hash[:]

    newNode['leftNode'] = leftNode
    newNode['rightNode'] = rightNode

    return newNode


def NewMerkleTree(dataList):
    nodes = []
    if len(dataList) % 2 != 0:
        dataList.append(dataList[len(dataList) - 1])

    for singleData in dataList:
        node = NewMerkleNode(None, None, singleData)
        nodes.append(node)


    for i in range(0,int(len(dataList)/2)):
        newNodes = []

        for j in range(len(nodes)-1):
            node = NewMerkleNode(nodes[j], nodes[j + 1], None)
            newNodes.append(node)

        nodes = newNodes

    mTreeRoot = nodes[0]

    return mTreeRoot


root= NewMerkleTree(["ddd","sss"])
print(root)