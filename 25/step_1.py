"""
AdventOfCode2020 day 25 (https://adventofcode.com/2020/day/25)


"""

# puzzle input:
#  1614360
#  7734663

# bij het lezen van de omschrijving voor het begrip het volgende
# getiept (ik lees beter code dan tekst). Maar voorlopig hebben we
# h.e.e.a. in aangepaste vorm nodig (daarom even in een 'if False' block

if True:
    def transform_subject_number(value, subject_number, loopsize):
        divider = 20201227  # from description
        for _ in range(loopsize):
            value = (value * subject_number) % divider
        return value    

    def public_key(subject_number, loopsize):
        return transform_subject_number(1, subject_number, loopsize)

    def encryption_key(start_value, subject_number, loopsize):
        return transform_subject_number(start_value, subject_number, loopsize)

    subject_number = 7

    door_loop_size = None  # dunno (yet)
    card_loop_size = None  # dunno (yet)

    door_public_key = None  # puzzle input, maar welke is welke...
    card_public_key = None  # 

# ja duh, nu even eerst 'Part One' oplossen

puzzle_input = [1614360, 7734663]

divider        = 20201227  # from description
subject_number = 7         # from description
value          = 1         # from description
loop_counter   = 0
loop_sizes     = []
public_keys    = []

while len(puzzle_input):
    value = (value * subject_number) % divider
    loop_counter += 1
    if value in puzzle_input:
        print(loop_counter, value)
        puzzle_input.remove(value)        
        loop_sizes.append(loop_counter)
        public_keys.append(value)

value = 1
subject_number = public_keys[1]
for i in range(loop_sizes[0]):
    value = (value * subject_number) % divider
print('\n\n  answer : ', value)

# check for door/card switched
value = 1
subject_number = public_keys[1]
for i in range(loop_sizes[0]):
    value = (value * subject_number) % divider
print('\n\n  answer : ', value)


