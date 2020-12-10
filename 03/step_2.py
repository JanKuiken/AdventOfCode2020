

valid_lines = 0

with open("input.txt") as f:
    lines = f.readlines()
    
    lines = lines[::2]
    
    width = 31
    hpos = 0
    tree_count = 0
    for line in lines:
        print(line, hpos)
        if line[hpos] == "#":
            tree_count += 1
        hpos = (hpos + 1) % width

print(tree_count)

# Right 1, down 1.
# Right 3, down 1. (This is the slope you already checked.)
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.

# 1 - 57
# 3 - 252
# 5 - 64
# 7 - 66
# ..- 43

print(57*252*64*66*43)


