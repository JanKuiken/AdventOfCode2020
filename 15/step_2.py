
#starting_numbers = [3,1,2]
starting_numbers = [14,8,16,0,1,17]

# Ok, first i simply changed 2020 to 30000000 in step_1.py and 
# added a line in the while loop to print the length of current.
# The program grinded to a halt....
# ( Python is not very efficient with list indexing, but the fun
#   of this puzzle is probably that it 'doesn't work' with
#   indexing and looping over the list/array anyway in any language)

# lets change the used data structure to a a dictionary(map)
# with as key the called_value, and as value the last index as
# it would have if we used a list/array

# (we've checked that the input has no duplicates)

# snapshot contains relevant upto but not including the last
# called number...
snapshot = {} 
for i,value in enumerate(starting_numbers[:-1]):
    snapshot[value] = i + 1 # lets start with 1 as normal people do

last_number_called = starting_numbers[-1] # but not yet 'indexed'...
index_to_be_added  = len(starting_numbers)

print(snapshot)
print(last_number_called)
print(index_to_be_added)

while(True):

    if last_number_called in snapshot.keys():

        delay = index_to_be_added - snapshot[last_number_called]
        snapshot[last_number_called] = index_to_be_added
        last_number_called = delay

    else:
    
        snapshot[last_number_called] = index_to_be_added
        last_number_called = 0
    
    index_to_be_added += 1
    # print progress
    if index_to_be_added % 1000000 == 0:
        print(index_to_be_added)

    if index_to_be_added == 30_000_000:
        print('\n\n answer:', last_number_called)
        break

