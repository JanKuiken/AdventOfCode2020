from collections import namedtuple
from itertools import product

test_data = """
.#.
..#
###
"""


data = """
#.......
.#..#..#
....#.#.
.##..#.#
#######.
#...####
###.##..
.##.#.#.
"""

data = data[1:-1] # strip leading/ending newline
lines = data.split('\n')

# we're gonna use a namedtuple for a point definition and
# sets as containers

point = namedtuple('point', ['x', 'y', 'z', 'w'])
active = set()

# fill active with input data
for x, line in enumerate(lines):
    for y, c in enumerate(line):
        if c == '#':
            z = 0
            w = 0
            active.add(point(x,y,z,w))

# utility functions
def neighours_of_point(p):
    neighours = set()
    for dx,dy,dz,dw in product([-1,0,+1], repeat=4):
        new_p = point(p.x + dx, p.y + dy, p.z + dz, p.w + dw)
        if (new_p != p):
            neighours.add(new_p)
    return neighours

def neighours_of_state(state):
    neighours = set()
    for p in state:
        neighours.update(neighours_of_point(p))
    return neighours

def number_of_active_neighbours(state, p):
    return len(state.intersection(neighours_of_point(p)))

# function to calculate the next state, according the rules
def next_state(state):   
    to_be_investigated = neighours_of_state(state)
    # also include state itself, these points might not be in neighbours
    to_be_investigated.update(state)
    new_state = set()
    for p in to_be_investigated:
        active_neighbors = number_of_active_neighbours(state, p)
        if p in state:
            if active_neighbors == 2 or active_neighbors == 3:
                new_state.add(p)        
        else:
            if active_neighbors == 3:
                new_state.add(p)        
    return new_state            

for _ in range(6):
    active = next_state(active)

print(len(active))

