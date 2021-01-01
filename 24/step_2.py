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

print('\n\n answer "Part One": ', len(flipped_tiles))


#  Part Two:  Conway game of live revisited...
# eerst een paar functies tiepen...

def neigbours(tile):
    retval = set()
    for neighbour in map_nesw_to_xy.values():
        retval.add((tile[0] + neighbour[0], tile[1] + neighbour[1]))
    return retval

def to_be_investigated_tiles(tiles):
    """
    given a set of tiles return a set of tiles, being either
    part ot the input (tiles) or a neighbour of any of the input tiles
    """
    retval = set()
    for tile in tiles:
        retval.add(tile)
        for neighbour in neigbours(tile):
            retval.add(neighbour)
    return retval

def todays_tiles(yesterday_tiles):
    """
    Rules:
        - Any black tile with zero or more than 2 black tiles immediately 
          adjacent to it is flipped to white.
        - Any white tile with exactly 2 black tiles immediately adjacent 
          to it is flipped to black.    
    """
    to_be_investigated = to_be_investigated_tiles(yesterday_tiles)
    retval = set()
    for tile in to_be_investigated:
        neigbour_tiles = neigbours(tile)
        n_black_neigbour_tiles = len(neigbour_tiles.intersection(yesterday_tiles))
        if tile in yesterday_tiles:
            # this tile was black, stays black if 1 or 2 black neighbours
            if n_black_neigbour_tiles in [1,2]:
                retval.add(tile)      
        else:
            # this tile was white, turns black with 2 black neighbours
            if n_black_neigbour_tiles in [2]:
                retval.add(tile)      
    return retval

# we werken vanaf nu met sets ipv. lists
flipped_tiles = set(flipped_tiles)

for day in range(100):
    flipped_tiles = todays_tiles(flipped_tiles)

print('\n\n  answer : ', len(flipped_tiles))

