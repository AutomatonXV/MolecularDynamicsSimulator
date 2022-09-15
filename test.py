import numpy as np
import matplotlib.pyplot as plt

# plt.axis([0, 10, 0, 1])

# for i in range(10):
#     y = np.random.random()
#     plt.xlim([0,10])
#     plt.ylim([0,10])
#     plt.scatter(i, y)
#     plt.pause(0.05)
#     plt.clf()

# plt.show()

# def angle_dot(a, b):
#     dot_product = round(np.dot(a, b),7)
#     prod_of_norms = round(np.linalg.norm(a) * np.linalg.norm(b),5)
#     print(dot_product)
#     print(prod_of_norms)
#     print(dot_product/prod_of_norms)
#     print(np.arccos(dot_product / prod_of_norms))
#     angle = round(np.degrees(np.arccos(dot_product / prod_of_norms)), 1)
#     return round(dot_product, 1), angle

# r = np.array([2,1])
# v = np.array([0.60034159, 0.79974369])
# p1 = r-np.array([5.,         4.99644325])
# p2 = r-np.array([1.24933251, 5.        ])

# target = p1
# print(angle_dot(target,v))

A = None
if not A: print("nice")