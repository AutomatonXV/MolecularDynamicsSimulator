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

#A = None
#if not A: print("nice")

#print(2.)

# 0 -0.05, 0.05 - 0.1
# if my particle is moving at 0.055, then it is on bracket 2

#print((0.055%0.05)/(0.05))

# def findBracket(x):
#     i = 0 #my bracket slot
#     for i in range(0, 100):
#         StartRange = 0.05*i
#         EndRange = 0.05*(i+1)
#         if StartRange <= x and x < EndRange:
#             return i
# A = 0
# if A == None: print("what")


def partition(array, low, high):

  # choose the rightmost element as pivot
  pivot = array[high]

  # pointer for greater element
  i = low - 1

  # traverse through all elements
  # compare each element with pivot
  for j in range(low, high):
    if array[j] <= pivot:
      # if element smaller than pivot is found
      # swap it with the greater element pointed by i
      i = i + 1

      # swapping element at i with element at j
      (array[i], array[j]) = (array[j], array[i])

  # swap the pivot element with the greater element specified by i
  (array[i + 1], array[high]) = (array[high], array[i + 1])

  # return the position from where partition is done
  return i + 1

# function to perform quicksort
def quickSort(array, low, high):
  if low < high:

    # find pivot element such that
    # element smaller than pivot are on the left
    # element greater than pivot are on the right
    pi = partition(array, low, high)

    # recursive call on the left of pivot
    quickSort(array, low, pi - 1)

    # recursive call on the right of pivot
    quickSort(array, pi + 1, high)


data = [10000000000, 10000000000, 10000000000, 10000000000, 10000000000, 10000000000, 1.214391490829783, 1.5947679651209368, 1.9055553608495275, 1.014792312112908]
print("Unsorted Array")
print(data)

size = len(data)

quickSort(data, 0, size - 1)

print('Sorted Array in Ascending Order:')
print(data)
