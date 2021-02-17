import socket
import json

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 53210))

send_string = "123 fe egg?, 234345"

sending_data = {
    "name": "Viktor",
    "age": 30,
    "city": "Minsk"
}
send_string = json.dumps(sending_data)

# dict, list, tuple, string, int, float, True, False, None

client_sock.sendall(send_string.encode())
data = client_sock.recv(1024).decode()
client_sock.close()
print('Received', repr(data))

res = json.loads(data)
print(res["age"])
