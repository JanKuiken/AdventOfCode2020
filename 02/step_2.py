
# regex would be better, but i hate regex's...
# my cool split_n_clean function workst as well... (for this case)

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
        minc = int(minc)
        maxc = int(maxc)

        if minc > len(password) or maxc > len(password):
            continue
        
        if (( password[minc-1] == character and
              password[maxc-1] != character      )
            or
            ( password[minc-1] != character and
              password[maxc-1] == character      )) :

            print(line)
            valid_lines += 1 

print(valid_lines)

