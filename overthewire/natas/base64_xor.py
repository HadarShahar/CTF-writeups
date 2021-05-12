import base64


def xor(bytes1: bytes, bytes2: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(bytes1, bytes2))


text = '{"showpassword":"no","bgcolor":"#ffffff"}'
given_cookie = 'ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw='
decoded = base64.b64decode(given_cookie)
key = xor(decoded, text.encode())
print(key)  # b'qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jq'


key = b'qw8J'
text = '{"showpassword":"yes","bgcolor":"#ffffff"}'
result = bytes(key[i % len(key)] ^ ch for i, ch in enumerate(text.encode()))
new_cookie = base64.b64encode(result)
print(new_cookie)
