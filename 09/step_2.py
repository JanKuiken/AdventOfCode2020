with open('input.txt') as f:
    alles = f.read()

numbers  = alles[:-1].split('\n')
numbers = [int(n) for n in numbers]

def sums_of_two(l):
    retval = []
    n = len(l)
    for i in range(n-1):
        for j in range(i+1,n):
            retval.append(l[i]+l[j])
    return retval

N = 25
for i in range(N, len(numbers)):
    if not numbers[i] in sums_of_two(numbers[i-N:i]):
        answer = numbers[i]

for i in range(len(numbers)):
    for j in range(i+1, len(numbers)):
        contiguous_range = numbers[i:j+1]
        if sum(contiguous_range) == answer:
            print(max(contiguous_range) + min(contiguous_range))

