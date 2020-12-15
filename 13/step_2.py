import pprint

# testline
# line = "67,x,7,59,61"

# question line:
line = "13,x,x,41,x,x,x,x,x,x,x,x,x,569,x,29,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,19,x,x,x,23,x,x,x,x,x,x,x,937,x,x,x,x,x,37,x,x,x,x,x,x,x,x,x,x,17"

definition = []
for index, bus_id in enumerate(line.split(',')):
    if bus_id != 'x':
        definition.append({
            'delay'  : index,
            'bus_id' : int(bus_id),
            'found'  : False
        })
        
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(definition)


number = 0
while True:
    
    for item in definition:
        if (number + item['delay']) % item['bus_id'] == 0:
            item['found']  = True
            
    # step size if calculated way to often, but who cares...
    step = 1
    all_found = True
    for item in definition:
        if item['found']:
            step *= item['bus_id']
        else:
            all_found = False
    if all_found:
        print("\n\n answer :", number)
        break
    number += step


