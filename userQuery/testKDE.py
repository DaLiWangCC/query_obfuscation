from sklearn.neighbors import kde
import numpy as np
import matplotlib.pyplot as plt

X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
X = np.random.normal(0, 3, 30)[:, np.newaxis]
X = np.concatenate((np.random.normal(0, 1, 30),
                     np.random.normal(5, 1, 70)))[:, np.newaxis]

kde = kde.KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)

log_dens = kde.score_samples(X)
print(log_dens)
print(np.exp(kde.score_samples(X)))


score = kde.score([[5]])
print(score)
print(np.exp(score))



fig, ax = plt.subplots()
ax.plot(X[:, 0], np.exp(log_dens), '*', label="kernel = '{0}'".format('gaussian'))


ax.set_xlim(-4, 10)
ax.set_ylim(-0.02, 1)

plt.show()
