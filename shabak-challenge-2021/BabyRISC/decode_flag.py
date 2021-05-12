"""
To generate 'output.bin': 
cat payload_builder/payload.bin | nc babyrisc.shieldchallenges.com 9070 > output.bin
"""
import struct

content = b''
with open('output.bin', 'rb') as file:
	content = file.read()
lines = content.split(b'\n')
e_flag = lines[10]

flag = b''
for i in range(0, len(e_flag), 4):
	dword = struct.unpack('I', e_flag[i: i+4])[0]  # unpack always returns a tuple
	# ASM_REGISTER_ZERO is added to each four bytes, and it's equal to -41 because of the solution, thus add 41
	flag += struct.pack('I', dword+41)
print(flag)