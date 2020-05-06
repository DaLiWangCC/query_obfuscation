
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


arr=np.random.rand(3,3)

data = [[0.1,0.2,0.9],[0.3,0.4,0.5],[0.5,0.6,0.7]]




data = np.mat(data)

bounds=[-1,1,1]
cmap = colors.ListedColormap(['none','red'])

norm = colors.BoundaryNorm(bounds, cmap.N)

plt.imshow(data,interpolation='nearest',cmap='bone',origin='lower')
#根据像素绘制图片 origin表示渐变程度
plt.colorbar()
#显示像素与数据对比
plt.xticks(())
plt.yticks(())
#不显示坐标轴刻度
data2 = [[1,0,0],[0,1,0],[0,0,1]]

plt.imshow(data2,interpolation='nearest',cmap=cmap,origin='lower',norm=norm)
plt.show()

