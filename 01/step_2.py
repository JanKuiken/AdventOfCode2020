import numpy as np

data = np.loadtxt("input.txt", dtype=int)

for first in data:
    for second in data:
        for third in data:
            if first + second + third == 2020:
                print(first, second, third, first*second*third)

