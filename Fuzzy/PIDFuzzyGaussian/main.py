import sys
import math
import numpy as np
import matplotlib.pyplot as plt

file1 = open('data.txt', 'r')
Lines = file1.readlines()

t = []
data = []

for line in Lines:
    value = line.replace('\n', '').split(' ')
    print(value)
    t.append(float(value[0]))
    data.append(float(value[1]))

plt.plot(t, data)
plt.show()