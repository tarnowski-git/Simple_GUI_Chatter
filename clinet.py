import socket

# Create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 444

# connecting with server
client_socket.connect((host, port))


full_massage = ""
while True:
    # Receiving a maximum of 8 bytes / buffer for chunks
    message = client_socket.recv(8)
    if len(message) <= 0:
        break
    full_massage += message.decode("utf-8")

print(full_massage)
