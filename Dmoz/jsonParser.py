import json

jsonPath = 'items2.json'

data = None
# 读取json
with open(jsonPath,'r') as f:
    data=json.load(f)

# print(data)

dataList = []
for item in data:
    oneName = item['link'][1].strip()
    oneName = oneName.replace('\u00ad','')
    dataList.append(oneName)
print(dataList)

# 写入json

with open('dataList.json', 'w') as f:
    json.dump(dataList, f)