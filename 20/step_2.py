"""
 a tile is defined by four 10 binary digits numbers (decimal 0-1023), for
 example the first tile in the inputfile:

  Tile 2131:

            ---> 
         1110010001
        
      1  ###..#...#  1
      1  ##..#.##.#  1        top    : 0b1110010001   ~ 913  (decimal)
      0  ..###...#.  0        right  : 0b1101110011   ~ 883
   ^  0  ......#..#  1 |      bottom : 0b1101001101   ~ 845
   |  1  ##.#.....#  1 |      left   : 0b1000010011   ~ 531
   |  0  ..#..#...#  1 |
   |  0  ......#...  0 v       
      0  ......#...  0
      0  .........#  1
      1  #.##..#.##  1
        
         1011001011    
            <---

 - a rotation of a tile is cycling values of (top, right, bottom, left)
 - a horizontal flip is swapping left and right and binary reverse all
 - a vertical flip is swapping top and bottom and binary reverse all
 
 we have 144 tiles, i.e. a 12x12 matrix
            
"""
from collections import namedtuple, Counter
from functools import reduce
from operator import mul
import numpy as np
import matplotlib.pyplot as plt

Tile = namedtuple('Tile', ['top', 'right', 'bottom', 'left', 'inner_tile'])

# read data and trans form it
with open('input.txt') as f:
    blob = f.read()[:-1]
    
tiles_txt = blob.split('\n\n')

tiles = {}
for tile_txt in tiles_txt:

    # split tiles, extract tile number and tile content
    header, body = tile_txt.split(':\n')
    tile_number = int(header.replace('Tile ',''))

    # clean up body, join lines, change to 0's and 1's
    body = body.replace('\n','')
    body = body.replace('#','1')
    body = body.replace('.','0')
    
    # find top, right, bottom, left with some fancy indexing
    top    = int( body[0:10]     ,2)
    right  = int( body[9:100:10] ,2)
    bottom = int( body[99:89:-1] ,2)
    left   = int( body[90::-10]  ,2)
    
    # add inner 8x8 tile for step 2 as a numpy array
    inner_tile = np.zeros((8,8), dtype=np.int8)
    for row in range(8):
        inner_tile[row,:] = [int(c) for c in body[11+10*row : 19+10*row]]
    
    # for manual check, print it
    print(tile_number, top, right, bottom, left)
    
    # add it to our data store
    tiles[tile_number] = Tile(top, right, bottom, left, inner_tile)

# copy for debugging 
tiles_orig = tiles.copy()

# oke, lets write that 'binary reverse' function 

def binary_reverse(i, n=10):
    """
    reverse the bits of a 10(default) bit number
    """
    s = bin(i)                      # change it to a binary string
    s = s[2:]                       # remove leading '0b'
    s = '0' * n + s                 # add enough leading zeros in front
    s = s[-n:]                      # take last (right) 10 most characters
    l = list(s)                     # make a list of the characters
    l.reverse()                     # reverse it (inplace)
    s = ''.join(l)                  # make it a string again
    return int(s, 2)                # return it as an int with base 2

# first damage assesment: 'what amount sides can connect to other sides?'

sides = []
for t in tiles.values():
    sides.append(t.top)
    sides.append(t.right)
    sides.append(t.bottom)
    sides.append(t.left)
    sides.append(binary_reverse(t.top))
    sides.append(binary_reverse(t.right))
    sides.append(binary_reverse(t.bottom))
    sides.append(binary_reverse(t.left))

count = Counter(sides)
print(count.values())
print(set(count.values()))

# result {1,2}, so we are lucky:
#  - each side fits to only one other side of another piece
#  - we have sides, that dont fit to other pieces, i.e. side or corner pieces

# lets run the count results again through a count:
count_2 = Counter(count.values())
print(count_2)
print(set(count_2.values()))

# ok, this looks solid we have:
print(12 * 4 * 2)       # external sides  (sides * 2 for reversed numbers) 
print(12 * 11 * 2 * 2)  # internal sides  (horizontal + vertical * 2 )

sides_with_no_neightbours = [key for key,values in count.items() if values == 1]

# find tiles with 4 (2* 2 for reversed numbers) sides without neighbours
# that must be corners
corners = []
for tile_number, tile in tiles.items():
    n = 0
    if tile.top                    in sides_with_no_neightbours  : n += 1
    if tile.right                  in sides_with_no_neightbours  : n += 1
    if tile.bottom                 in sides_with_no_neightbours  : n += 1
    if tile.left                   in sides_with_no_neightbours  : n += 1
    if binary_reverse(tile.top)    in sides_with_no_neightbours  : n += 1
    if binary_reverse(tile.right)  in sides_with_no_neightbours  : n += 1
    if binary_reverse(tile.bottom) in sides_with_no_neightbours  : n += 1
    if binary_reverse(tile.left)   in sides_with_no_neightbours  : n += 1
    if n == 4:
        print(tile_number)
        corners.append(tile_number)

print('\n\n answer:', reduce(mul, corners))

print('\n\n step 2, now it\'s gonna get thougher\n\n')

# first write some rotate and flip functions for tiles
# (functions take a tile and return one)

def rotate_tile_ccw(in_tile):
    top        = in_tile.right
    right      = in_tile.bottom
    bottom     = in_tile.left
    left       = in_tile.top
    inner_tile = np.rot90(in_tile.inner_tile.copy())  # take copy first, rot90 is inplace
    return Tile(top, right, bottom, left, inner_tile)

def rotate_tile_180(in_tile):
    return rotate_tile_ccw(
               rotate_tile_ccw(in_tile))
    
def rotate_tile_cw(in_tile):
    return rotate_tile_ccw(rotate_tile_180(in_tile))

def flip_tile_lr(in_tile):
    top        = binary_reverse(in_tile.top)
    right      = binary_reverse(in_tile.left)
    bottom     = binary_reverse(in_tile.bottom)
    left       = binary_reverse(in_tile.right)
    inner_tile = np.fliplr(in_tile.inner_tile.copy())  # take copy first, fliplr is inplace
    return Tile(top, right, bottom, left, inner_tile)

def flip_tile_ud(in_tile):
    return flip_tile_lr(rotate_tile_180(in_tile))


# create a map from sidenumbers to tile numbers:
side_tile_map = {}
for side_number in set(sides):
    side_tile_map[side_number] = []
    for tile_number, tile in tiles.items():
        if side_number in (tile.top,
                           tile.right,
                           tile.bottom,
                           tile.left,
                           binary_reverse(tile.top),
                           binary_reverse(tile.right),
                           binary_reverse(tile.bottom),
                           binary_reverse(tile.left)     ):
                           
            side_tile_map[side_number].append(tile_number)

print(side_tile_map)

# oke now the (jigsaw) puzzling starts, this is the plan:
#
# - create a 12x12 grid for the tiles (content will be tile numbers)
# - start with a previously found corner tile (let's use 3061, the first found)
# - flip/rotate it such it will fill the upper left corner
#     (the rotated/flipped state will be stored in our tiles dictionary)
# - find tiles that fit to the right (subsequently), to complete the top row
#     (tiles most likely need to be rotated/flipped)
# - find tiles that fit to the bottom of the top row (subsequently)
#     (tiles most likely need to be rotated/flipped again)

# function for manual debugging
def print_tile(tile_number):
    tile = tiles[tile_number]
    print("Number :", tile_number)
    print("Top    :", tile.top   , binary_reverse(tile.top)   , side_tile_map[tile.top   ])  
    print("Right  :", tile.right , binary_reverse(tile.right) , side_tile_map[tile.right ])
    print("Bottom :", tile.bottom, binary_reverse(tile.bottom), side_tile_map[tile.bottom])
    print("Left   :", tile.left  , binary_reverse(tile.left)  , side_tile_map[tile.left  ])


board = np.zeros((12,12), dtype=np.int16)

# we start with the first previous found corner in the upper left 
our_lu_corner = corners[0]

# oke, find out if/how we must rotate our corner tile
has_no_neighbours_top    = count[tiles[our_lu_corner].top]    == 1
has_no_neighbours_right  = count[tiles[our_lu_corner].right]  == 1
has_no_neighbours_bottom = count[tiles[our_lu_corner].bottom] == 1
has_no_neighbours_left   = count[tiles[our_lu_corner].left]   == 1
print(has_no_neighbours_top, 
      has_no_neighbours_right, 
      has_no_neighbours_bottom, 
      has_no_neighbours_left)
tmp = ( has_no_neighbours_top, 
        has_no_neighbours_right, 
        has_no_neighbours_bottom, 
        has_no_neighbours_left   )
if   tmp == (True,True,False,False) : tiles[our_lu_corner] = rotate_tile_ccw(tiles[our_lu_corner])
elif tmp == (False,True,True,False) : tiles[our_lu_corner] = rotate_tile_180(tiles[our_lu_corner])
elif tmp == (False,False,True,True) : tiles[our_lu_corner] = rotate_tile_cw(tiles[our_lu_corner])
elif tmp == (True,False,False,True) : pass
else                                : raise ValueError('Should not happen in orienting first corner')

# set our nicely oriented tile to the upper left corner of the board
board[0,0] = our_lu_corner
        
# oke, that looks good, 

# now find the tiles of the top row

for col in range(11):
    the_tile = board[0,col]
    the_right_side = tiles[the_tile].right
    # find the tile that fits here
    the_candidates = side_tile_map[the_right_side].copy()
    the_candidates.remove(the_tile)
    if len(the_candidates) != 1:
        raise ValueError('Did not find a single candidate for top row tile')
    the_candidate = the_candidates[0]
    # now rotate/flip the one and only candidate to fit to 'the tile'
    # note: we need to fit the right side with a 'reversed' left side
    if                  tiles[the_candidate].top     == the_right_side : tiles[the_candidate] = flip_tile_ud(rotate_tile_ccw(tiles[the_candidate]))
    elif                tiles[the_candidate].right   == the_right_side : tiles[the_candidate] = flip_tile_ud(rotate_tile_180(tiles[the_candidate]))
    elif                tiles[the_candidate].bottom  == the_right_side : tiles[the_candidate] = flip_tile_ud(rotate_tile_cw(tiles[the_candidate]))
    elif                tiles[the_candidate].left    == the_right_side : tiles[the_candidate] = flip_tile_ud(tiles[the_candidate])
    elif binary_reverse(tiles[the_candidate].top)    == the_right_side : tiles[the_candidate] = rotate_tile_ccw(tiles[the_candidate])
    elif binary_reverse(tiles[the_candidate].right)  == the_right_side : tiles[the_candidate] = rotate_tile_180(tiles[the_candidate])
    elif binary_reverse(tiles[the_candidate].bottom) == the_right_side : tiles[the_candidate] = rotate_tile_cw(tiles[the_candidate])
    elif binary_reverse(tiles[the_candidate].left)   == the_right_side : pass
    else:
        raise ValueError('Could not flip/rotate the candidate')
    # add it to the broard:
    board[0,col+1] = the_candidate

print(tiles[1783])

# now find the tiles below the top row
for col in range(12):
    for row in range(0,11):
        the_tile = board[row,col]
        the_bottom_side = tiles[the_tile].bottom
        # find the tile that fits here
        the_candidates = side_tile_map[the_bottom_side].copy()
        the_candidates.remove(the_tile)
        if len(the_candidates) != 1:
            raise ValueError('Did not find a single candidate for a tile below')
        the_candidate = the_candidates[0]
        # now rotate/flip the one and only candidate to fit to 'the tile'
        if                  tiles[the_candidate].top     == the_bottom_side : tiles[the_candidate] = flip_tile_lr(tiles[the_candidate])
        elif                tiles[the_candidate].right   == the_bottom_side : tiles[the_candidate] = flip_tile_lr(rotate_tile_ccw(tiles[the_candidate]))
        elif                tiles[the_candidate].bottom  == the_bottom_side : tiles[the_candidate] = flip_tile_lr(rotate_tile_180(tiles[the_candidate]))
        elif                tiles[the_candidate].left    == the_bottom_side : tiles[the_candidate] = flip_tile_lr(rotate_tile_cw(tiles[the_candidate]))
        elif binary_reverse(tiles[the_candidate].top)    == the_bottom_side : pass
        elif binary_reverse(tiles[the_candidate].right)  == the_bottom_side : tiles[the_candidate] = rotate_tile_ccw(tiles[the_candidate])
        elif binary_reverse(tiles[the_candidate].bottom) == the_bottom_side : tiles[the_candidate] = rotate_tile_180(tiles[the_candidate])
        elif binary_reverse(tiles[the_candidate].left)   == the_bottom_side : tiles[the_candidate] = rotate_tile_cw(tiles[the_candidate])
        else:
            raise ValueError('Could not flip/rotate the candidate')
        # add it to the broard:
        board[row+1,col] = the_candidate

print(board)

# oke, that went well, let's hope the inner tiles rotated/flipped along correctly

big_board = np.zeros((12*8,12*8), dtype=np.int8)
for row in range(12):
    for col in range(0,12):
        big_board[col*8:(col+1)*8, row*8:(row+1)*8] = tiles[board[col,row]].inner_tile

monster = np.asarray([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                      [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1],
                      [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0],], dtype=np.int8)

monster_pixels = np.sum(monster)
monster_height, monster_width = monster.shape


def find_monsters():
    monster_max = 0
    no_monsters = 0
    sum_big_board = np.sum(big_board)
    print("----------------------")
    for h in range(96 - monster_height):
        for w in range(96 - monster_width):
            tst = monster * big_board[h:h + monster_height,
                                      w:w + monster_width]
            if np.sum(tst) == monster_pixels:
                no_monsters += 1
                print("Found it!", h,w, no_monsters, sum_big_board - no_monsters * monster_pixels) 
            if np.sum(tst) > monster_max:
                monster_max = np.sum(tst)
                print('monster_max', h,w,monster_max)
                if monster_max == 15:
                    plt.figure()
                    plt.imshow(big_board)
                    plt.show()


find_monsters()
big_board = np.rot90(big_board)
find_monsters()
big_board = np.rot90(big_board)
find_monsters()
big_board = np.rot90(big_board)
find_monsters()

big_board = np.flipud(big_board)

find_monsters()
big_board = np.rot90(big_board)
find_monsters()
big_board = np.rot90(big_board)
find_monsters()
big_board = np.rot90(big_board)
find_monsters()

