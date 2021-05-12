"""
useful caclulator: https://hub.zhovner.com/tools/nfc/

flag{G0_M1n1on$}
"""
import socket
from threading import Thread
import time

REMOTE_ADDRESS = ('nfc.shieldchallenges.com', 80)
AUTH_MSG = b'\x1B\x24\x68\xBE\xAF\x49\x30'


class VerboseTcpSocket(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, data: bytes) -> int:
        n = super().send(data)
        print('sent:', data)
        return n

    def recv(self, bufsize: int) -> bytes:
        data = super().recv(bufsize)
        print('received:', data)
        return data


sock = VerboseTcpSocket()
sock.connect(REMOTE_ADDRESS)

sock.send(AUTH_MSG)
data = sock.recv(1024)

# sock.send(b'\x66\xCE\x57')
# data = sock.recv(1024)

print('\nFAST_READ:')
sock.send(b'\x3A\x00\x2C\xAE\xBB')
data = sock.recv(1024)

sock.close()
