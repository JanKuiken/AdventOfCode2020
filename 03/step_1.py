

valid_lines = 0

with open("input.txt") as f:
    lines = f.readlines()
    
    width = 31
    hpos = 0
    tree_count = 0
    for line in lines:
        print(line, hpos)
        if line[hpos] == "#":
            tree_count += 1
        hpos = (hpos + 3) % width

print(tree_count)


