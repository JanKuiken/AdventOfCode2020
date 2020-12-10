import numpy as np

data = np.loadtxt("input.txt", dtype=int)

for first in data:
    for second in data:
        if first + second == 2020:
            print(first, second, first+second, first*second)

