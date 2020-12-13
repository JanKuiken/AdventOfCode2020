import numpy as np
from collections import Counter

# read data and store in numpy matrix for convinient indexing
with open('input.txt') as f:
    blob = f.read()
seats  = blob[:-1].split('\n')
seats = [[c for c in s] for s in seats]
seats = np.asarray(seats)

# we will use r,c (row,column) as indices, and as limits: ROWS, COLS
ROWS, COLS = seats.shape

def adjacent_positions(r,c):
    return [ (nr,nc)
             for nr,nc in
                [ (r-1, c-1), (r-1, c  ), (r-1, c+1),
                  (r  , c-1),             (r  , c+1),
                  (r+1, c-1), (r+1, c  ), (r+1, c+1), ]
             if (     nr >= 0 
                  and nr < ROWS
                  and nc >= 0
                  and nc < COLS ) ] 

def apply_rules_to_a_seat(r, c, current_seats):

    adjacent_list = [ current_seats[r,c] 
                      for r,c in adjacent_positions(r,c)]
    count = Counter(adjacent_list)

    current = current_seats[r,c]
    if current == 'L' and count['#'] == 0:
        return '#'
    if current == '#' and count['#'] >= 4:
        return 'L'
    return current

def new_seats(old_seats):
    new_seats = np.zeros_like(seats)
    for r in range(ROWS):
        for c in range(COLS):
            new_seats[r,c] = apply_rules_to_a_seat(r,c,old_seats)
    return new_seats



# wait untill the chaos stabilizes...
while(True):
    print('.', end='', flush=True)
    next_seats = new_seats(seats)
    if np.array_equal(next_seats, seats):
        break
    seats = next_seats

# ok, we are stabilized, count occupied seats
occupied = np.sum(seats == '#')
print('\n\nanswer :',occupied)


