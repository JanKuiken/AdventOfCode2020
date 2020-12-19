
#starting_numbers = [3,1,2]
starting_numbers = [14,8,16,0,1,17]

current = starting_numbers.copy()

def reversed_find_except_last(l, value):
    N = len(l)
    for i in range(-2, -(N+1), -1):
        if l[i] == value:
            return -i-1
    return None # should not happen

while(True):   # again we use a 'break' when finished
    last_spoken = current[-1]
    if not last_spoken in current[:-1]:
        current.append(0)
    elif True:
        turns = reversed_find_except_last(current, last_spoken)
        if turns:
            current.append(turns)
        else:
            print('Whoops, should not happen')
    if len(current) == 2020:
        break

print('\n\n answer:', current[-1])

