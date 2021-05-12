# import requests
# import base64
# import urllib

# username = 'natas28'
# password = 'JWwR438wkgTsNKBbcJoowyysdM82YjeF'
# url = f'http://{username}.natas.labs.overthewire.org/'

# s = requests.Session()
# s.auth = (username, password)

# for i in range(50):
#     data = {'query': 'a'*i}
#     r = s.post(url, data=data)
#     query = r.url.split('=')[1]

#     url_decoded = urllib.parse.unquote(query)
#     b64_decoded = base64.b64decode(url_decoded)
#     print(i, len(b64_decoded))


# didn't finish it
