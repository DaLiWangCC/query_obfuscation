import numpy as np





p = 1/64

h = - p * np.log(p)

print(h)


dic = {"a":2}

for key, value in dic.items():
    print(key)
    print(value)


array = [2,4,1,2,3]
array.sort()
print(array)


your_list = ["","ads","Asd",""]
your_list = [x for x in your_list if x != '']

print(your_list)


s = '\xef\xbc\x8c2'
ss = s.encode('raw_unicode_escape')
print(ss) #结果：b'\xe9\x9d\x92\xe8\x9b\x99\xe7\x8e\x8b\xe5\xad\x90'
sss = ss.decode()
print(sss)
