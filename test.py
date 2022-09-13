import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 1])

for i in range(10):
    y = np.random.random()
    plt.xlim([0,10])
    plt.ylim([0,10])
    plt.scatter(i, y)
    plt.pause(0.05)
    plt.clf()

plt.show()