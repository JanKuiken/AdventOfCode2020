from collections import Counter

with open('input.txt') as f:
    alles = f.read()

numbers  = alles[:-1].split('\n')
numbers = [int(n) for n in numbers]

# add outlet and device joltage
numbers.append(0)
numbers.append(max(numbers)+3)

numbers.sort()

n = len(numbers)
steps = [numbers[i+1] - numbers[i] for i in range(n-1)]

# Can we find a pattern....?
#
# - we only have steps of 1 and 3 jolts
# - a 3 jolts step cannot be removed
#
# - one 1 jolt step cannot be changed
#
# - two 1 jolt steps can be changed, example:
#     3  1  1  3        
#    7-10-11-12-15 =>  7-10-  -12-15
#     (i.e. original + 1 change)
#
# - three 1 jolt steps can be changed, example:
#     3  1  1  1  3
#    7-10-11-12-13-16 =>  7-10-  -12-13-16
#                     =>  7-10-11-  -13-16
#                     =>  7-10-     -13-16
#     (i.e. original + 3 changes)
#
# hmmm, lets do a damage assesment
# first check what our biggest series of 1 jolt steps is....
#

steps_str = ''.join(str(s) for s in steps)

for i in range(100):
    test_str = '1' * i
    print(i, test_str)
    if not test_str in steps_str:
        break

# oke five 1 jolt steps is the biggest series, we might
# proceed a bit further with previous analysis
#
# - four 1 jolt steps
#   3  1  1  1  1  1
#  7-10-11-12-13-14-17  => 7-10-  -12-13-14-17
#                       => 7-10-11-  -13-14-17
#                       => 7-10-11-12-  -14-17
#                       => 7-10-  -  -13-14-17
#                       => 7-10-11-  -  -14-17
#                       => 7-10-  -12-  -14-17
#     (i.e. original + 6 changes)
#
# - five 1 jolt steps
#   3  1  1  1  1  1  3
#  7-10-11-12-13-14-15-18  => 7-10-  -12-13-14-15-18
#                          => 7-10-11-  -13-14-15-18
#                          => 7-10-11-12-  -14-15-18
#                          => 7-10-11-12-13-  -15-18
#                          => 7-10-  -  -13-14-15-18
#                          => 7-10-  -12-  -14-15-18
#                          => 7-10-  -12-13-  -15-18
#                          => 7-10-11-  -  -14-15-18
#                          => 7-10-11-  -13-  -15-18
#                          => 7-10-11-12-  -  -15-18
#     (i.e. original + 10 changes)
#
#
#  Wow that was messy, lets summarize:
#
#  "11"      => 2  possibilities
#  "111"     => 4  possibilities
#  "1111"    => 7  possibilities
#  "11111"   => 11 possibilities
#  (hope we did not make mistakes....)
#
# now we have to count how often the series occur, let
# use Capital Letters for series, and some string replacements

steps_str = steps_str.replace('11111', 'E')
steps_str = steps_str.replace('1111' , 'D')
steps_str = steps_str.replace('111'  , 'C')
steps_str = steps_str.replace('11'   , 'B')

count = Counter(steps_str)
print(count)

# shoot, '11111' did not occur i did too much analysis
# muliply all possible mutations of replacable series

total_possibilities = (    7 ** count['D'] 
                        *  4 ** count['C']
                        *  2 ** count['B']  )

print(total_possibilities)


