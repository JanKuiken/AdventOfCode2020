

required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid',]
optional = ['cid']

required.sort()

with open("input.txt") as f:
    all = f.read()


# create passports from lines
passports = all.split('\n\n')

valid_passports = 0
for p in passports:
    pairs = p.split()
    keys = [p.split(':')[0] for p in pairs]
    print(keys)
    
    # we ignore (remove) 'cid'
    if 'cid' in keys:
        keys.remove('cid')
    keys.sort()
    if keys == required:
        valid_passports += 1

print(valid_passports)

