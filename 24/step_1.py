"""

AdventOfCode2020 day 24 (https://adventofcode.com/2020/day/24)

oke, first step is defining coordinate system for hexagonal tiles:
let's try some ASCII art:
                   /\     /\
                  /  \   /  \
               \ /    \ /    \ /
                | (0,  | (1,  |
                |    1)|   1) |
                /\     /\    /\
           \   /  \   /  \  /  \
            \ /    \ /    \/    \/
             |(-1,  | (0, | (1, |
             |   0) |   0)|   0 |
            / \    / \    /\    / \
           /   \  /   \  /  \  /
                \/     \/    \/      
                |(-1,  | (0, |  
                |  -1) |  -1)|      ,etc, etc....

i.e.:  x-direction: east-west, east is positive
       y-direction: northwest-southeast, northwest is positive          
"""

# read input
with open('input.txt') as f:
    blob = f.read()[:-1]
raw_instructions = blob.split('\n')

map_nesw_to_xy = { 'e'  : ( 1, 0),
                   'se' : ( 0,-1),
                   'sw' : (-1,-1),
                   'w'  : (-1, 0),
                   'nw' : ( 0, 1),
                   'ne' : ( 1, 1),  }

def translate_raw_instructions(raw_instructions):
    instructions = []
    while len(raw_instructions):
        for k,v in map_nesw_to_xy.items():
            if raw_instructions.startswith(k):
                instructions.append(v)
                raw_instructions = raw_instructions[len(k):]
                break # (out of the for loop, continue with while loop)
    return instructions

def end_tile_xy(instruction):
    xy = (0,0) # start tile
    for move in instruction:
        xy = (xy[0] + move[0], xy[1] + move[1])
    return xy

instructions = [translate_raw_instructions(i) for i in raw_instructions]

end_tiles = [end_tile_xy(i) for i in instructions]

flipped_tiles = []
for tile in end_tiles:
    if tile in flipped_tiles:
        flipped_tiles.remove(tile)
    else:
        flipped_tiles.append(tile)

print('\n\n answer : ', len(flipped_tiles))


