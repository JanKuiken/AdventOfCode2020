from string import digits, ascii_lowercase

required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid',]
optional = ['cid']

required.sort()

with open("input.txt") as f:
    alles = f.read()


# create passports from lines
passports = alles.split('\n\n')

valid_passports = 0
for p in passports:
    pairs = p.split()
    data = {p.split(':')[0]:p.split(':')[1] for p in pairs}
    keys = list(data.keys())
    #print(keys)
    
    # we ignore (remove) 'cid'
    if 'cid' in keys:
        keys.remove('cid')
    # als we een fout hebben gaan we door, op het laatst 
    # verhogen we de valid count
    
    # dit geld vast ook nog
    keys.sort()
    if keys != required:
        continue
    
    byr = data['byr']
    if len(byr) != 4 : continue
    byr = int(byr)
    if byr < 1920 or byr > 2002 : continue
    
    iyr = data['iyr']
    if len(iyr) != 4 : continue
    iyr = int(iyr)
    if iyr < 2010 or iyr > 2020 : continue
    
    eyr = data['eyr']
    if len(eyr) != 4 : continue
    eyr = int(eyr)
    if eyr < 2020 or eyr > 2030 : continue
    
    hgt = data['hgt']
    #print(hgt)
    hgt2 = int(hgt[:-2]) 
    if hgt[-2:] == 'cm':
        if hgt2 < 150 or hgt2 > 193 : continue
    elif hgt[-2:] == 'in': 
        if hgt2 < 59 or hgt2 > 79 : continue
    else:
        continue 
    
    hcl = data['hcl']
    print(hcl)
    if hcl == 'z': print(data)
    if len(hcl) != 7 : continue
    if hcl[0] != '#' : continue
    if not hcl[1] in '0123456789abcdef' : continue
    if not hcl[2] in '0123456789abcdef' : continue
    if not hcl[3] in '0123456789abcdef' : continue
    if not hcl[4] in '0123456789abcdef' : continue
    if not hcl[5] in '0123456789abcdef' : continue
    if not hcl[6] in '0123456789abcdef' : continue
     
    ecl = data['ecl']
    if not ecl in ['amb','blu','brn','gry','grn','hzl','oth'] : continue 
    
    pid = data['pid']
    if len(pid) != 9 : continue
    if not pid[0] in digits : continue
    if not pid[1] in digits : continue
    if not pid[2] in digits : continue
    if not pid[3] in digits : continue
    if not pid[4] in digits : continue
    if not pid[5] in digits : continue
    if not pid[6] in digits : continue
    if not pid[7] in digits : continue
    if not pid[8] in digits : continue
    
    # jaah, een geldig paspoort
    valid_passports += 1
        
        
        

print(valid_passports)

