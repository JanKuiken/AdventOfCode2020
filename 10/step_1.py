from collections import Counter

with open('input.txt') as f:
    alles = f.read()

numbers  = alles[:-1].split('\n')
numbers = [int(n) for n in numbers]

numbers.sort()

n = len(numbers)
steps = [numbers[i+1] - numbers[i] for i in range(n-1)]

count = Counter(steps)

# added +1 for the 3 joltage jump between last adapter and my device
# added +1 for the 1 joltage jump between outlet and first adapter
print((count[1]+1) * (count[3]+1))


