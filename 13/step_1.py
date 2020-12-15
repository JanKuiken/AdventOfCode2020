import numpy as np

with open('input.txt') as f:
    blob = f.read()
lines = blob[:-1].split('\n')

start_time = int(lines[0])
bus_ids    = [ int(s) for s in lines[1].split(',') if s != 'x' ]

bus_time_after_our_start_time = []
for bus_id in bus_ids:
    dus  = start_time // bus_id
    rest = start_time % bus_id
    if rest != 0:
        dus += 1
    bus_time_after_our_start_time.append(dus * bus_id)

# efkens numpy array's der fan meitsje
bus_ids = np.asarray(bus_ids)
bus_time_after_our_start_time = np.asarray(bus_time_after_our_start_time)
wait_time = bus_time_after_our_start_time - start_time

earliest_bus_index = np.argmin(wait_time)

print(bus_ids)
print(bus_time_after_our_start_time)
print(wait_time)
print(earliest_bus_index)

print('\n answer :',   bus_ids[earliest_bus_index] 
                     * wait_time[earliest_bus_index] )

