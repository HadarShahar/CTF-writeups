import string
e_flag = 'VMY{vtxltkvbiaxkbltlnulmbmnmbhgvbiaxk}'
flag = ''
for ch in e_flag:
    if ch in '{}':
        flag += ch
        continue 
    charset = string.ascii_uppercase
    if ch.islower():
        charset = string.ascii_lowercase
    flag += charset[charset.find(ch)-19]
print(flag)
