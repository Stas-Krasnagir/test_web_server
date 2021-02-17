import socket


client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 53210))
send_string = "123 fe egg?, 234345"
client_sock.send(send_string.encode())
data = client_sock.recv(1024).decode()
client_sock.close()
print('Received', repr(data))
