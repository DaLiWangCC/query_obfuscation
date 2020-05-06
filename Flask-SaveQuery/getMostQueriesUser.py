#-*- coding:utf-8 -*-

import copy

# 将十个用户搜索写入文件
def writeTxt(most10User,index):
    path = "/Users/rememberthelesson/wanghao/Firefox/AOL-user-ct-collection/"

    for i in range(0,len(most10User)-1):

        userDic = most10User[i]
        userQueries = userDic["userQueries"]

        writePath = path + "out-tpo10-" + str(index).zfill(2) + "_"+str(i)+".txt"
        fout = open(writePath, 'w')  # 返回一个文件对象

        print(userDic["queryCount"])
        for userQuery in userQueries:
            string = userQuery["anonID"] +"\t"+ userQuery["query"] +"\t"+ userQuery["queryTime"] +"\t" +userQuery["itemRank"] + "\t" +userQuery["clickURL"]
            # print("每行数据")
            # print(string)
            fout.write(string)

    fout.close()



def getMostQueriesUser(index,most_num=1):

    path = "/Users/rememberthelesson/wanghao/Firefox/AOL-user-ct-collection/"

    filename = "user-ct-test-collection-"

    if index == None: index = 1
    filename = filename + str(index).zfill(2) +".txt"

    readPath = path + filename
    f = open(readPath, 'r')  # 返回一个文件对象

    #每个用户的搜索次数
    queryCount = 1
    line = f.readline()
    #越过标题行
    line = f.readline()
    lastAnonID = None
    userDic = {"anonID": "", "queryCount": 0, "userQueries": []}
    most10User = []
    while line:

        strArray = line.split("\t")
        anonID = strArray[0]
        query = strArray[1]
        queryTime = strArray[2]
        itemRank = strArray[3]
        clickURL = strArray[4]


        if anonID == lastAnonID:
            queryCount += 1

        # 如果到了下一个用户，存老的，开一个新的userDic
        elif lastAnonID != None and lastAnonID != anonID:
            # print(queryCount)

            #把上一个用户存进来
            tempDic = userDic.copy()
            userDic = {"anonID": "",  "queryCount": 0, "userQueries": []}

            most10User.append(tempDic)
            most10User = sorted(most10User, key=lambda x: x['queryCount'], reverse=True)

            # 根据queryCount数量排序，换出最小的
            if len(most10User) > most_num:
                most10User.pop(-1)

            queryCount = 0

        lastAnonID = anonID
        userQuery = {}
        userQuery["anonID"] = anonID
        userQuery["query"] = query
        userQuery["queryTime"] = queryTime
        userQuery["itemRank"] = itemRank
        userQuery["clickURL"] = clickURL

        # 收集一个用户的queries
        userDic["queryCount"] = queryCount
        userDic["anonID"] = anonID
        userDic["userQueries"].append(userQuery.copy())

        line = f.readline()

    writeTxt(most10User,index)




def getTop10User(index):

    path = "/Users/rememberthelesson/wanghao/Firefox/AOL-user-ct-collection/"

    filename = "out-top10-"

    if index == None: index = "01_1"
    filename = filename + str(index).zfill(2) +".txt"

    readPath = path + filename
    f = open(readPath, 'r')  # 返回一个文件对象


    line = f.readline()
    allUserDic = []
    while line:

        strArray = line.split("\t")
        anonID = strArray[0]
        query = strArray[1]
        queryTime = strArray[2]
        itemRank = strArray[3]
        clickURL = strArray[4]
        userQuery = {}
        userQuery["anonID"] = anonID
        userQuery["query"] = query
        userQuery["queryTime"] = queryTime
        userQuery["itemRank"] = itemRank
        userQuery["clickURL"] = clickURL

        allUserDic.append(userQuery)
        print(userQuery)
        line = f.readline()
    f.close()
    return allUserDic

# getTop10User(1)


#将10个文件里面查询数量前n多的user存起来
# for i in range(0,10):
#     print(i+1)
#     getMostQueriesUser(i + 1,11)