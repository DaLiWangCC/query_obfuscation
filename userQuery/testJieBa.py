# encoding=utf-8
import jieba

seg_list = jieba.cut("上海篮球场在哪", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

seg_list = jieba.cut("上海篮球场在哪", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))

import jieba.posseg as pseg
#查看词性
words = pseg.cut("我爱北京天安门")
for word, flag in words:
    print('%s %s' % (word, flag))