
# regex would be better, but i hate regex's...
# my cool split_n_clean function workst as well... (for this case)

from collections import Counter

def split_n_clean(s, sep):
    first, second = s.split(sep)
    return first.strip(), second.strip()

valid_lines = 0

with open("input.txt") as f:
    lines = f.readlines()
    for line in lines:
        rules, password    = split_n_clean(line, ":")
        numbers, character = split_n_clean(rules, " ")
        minc, maxc         = split_n_clean(numbers, "-")
        
        # apply some collections.Counter fun
        counter = Counter(password)
        if character in counter:
            num_of_char = counter[character]
            if num_of_char >= int(minc) and num_of_char <= int(maxc):
                print(line)
                valid_lines += 1 

print(valid_lines)

