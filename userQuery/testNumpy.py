import numpy as  np


def change(x):
    return x+1

arr1 = np.array((60, -4, 10, 10))
arr2 = np.array((14, 3, 110, 10))
arr3 = np.array((6, 1, 120, 10))

merge_arr = np.concatenate([arr1, arr2, arr3], axis=0)

print(merge_arr)  # (80, 4, 10, 10)


m2 = np.vstack([arr1, arr2, arr3])

print(m2)


print(m2[1][0])
print(m2.max(axis=0))
print(m2[2].max())
print(m2[1])
print(m2[1].min())


m3 = change(m2)
print(m3)


