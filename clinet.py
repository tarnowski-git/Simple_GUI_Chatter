import socket

HEADER_SIZE = 10

# Create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 999

# connecting with server
client_socket.connect((host, port))

while True:
    full_massage = ""
    new_massege = True
    while True:
        # Receiving a maximum of 16 bytes / buffer for chunks
        message = client_socket.recv(16)
        if new_massege:
            print(f"new message lenght: {message[:HEADER_SIZE]}")
            message_lenght = len(message[: HEADER_SIZE])
            new_massege = False

        full_massage += message.decode("utf-8")

        if len(full_massage) - HEADER_SIZE == message_lenght:
            print("full message recvd")
            print(full_massage[10:])
            new_massege = True
            full_massage = ""

    print(full_massage)
