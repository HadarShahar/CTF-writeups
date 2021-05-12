from hashlib import md5
import itertools
import string

hashed_pincode = '2D3114BCC2E5C58BBAC77F04237723D9'

# for i in range(10000):
#     text = str(i).zfill(4)
#     hashed = text
#     for j in range(20):
#         hashed = md5(hashed.encode()).hexdigest().upper()
#     if hashed == hashed_pincode:
#         print(text, hashed)

for chars in itertools.product(string.digits + string.ascii_letters, repeat=4):
    text = ''.join(chars)
    hashed = text
    for j in range(20):
        hashed = md5(hashed.encode()).hexdigest().upper()

    print(text, hashed)
    if hashed == hashed_pincode:
        print('found!!!')
        break

# 5cRt 2D3114BCC2E5C58BBAC77F04237723D9
# found!!!
