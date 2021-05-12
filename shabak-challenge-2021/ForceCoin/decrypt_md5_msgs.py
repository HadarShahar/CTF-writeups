from hashlib import md5
import string
import re


def decrypt_msg(msg: str) -> str:
    hashes = [h.strip() for h in msg.split(',')]
    result = ''

    for h in hashes:
        cache = {}
        for ch in string.printable:
            hashed = md5((result+ch).encode()).hexdigest()
            cache[hashed] = ch
        result += cache[h]

    return result


with open('db.txt', 'r') as file:
    content = file.read()
    # great website: https://pythex.org/
    msgs = re.findall('\[(.*?)\]', content)
    for msg in msgs:
        print(decrypt_msg(msg))
