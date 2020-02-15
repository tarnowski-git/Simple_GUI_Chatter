import socket
import time

HEADER_SIZE = 10

# creating the socket object - ipv4, tcp ip
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# store the host IP address
host = socket.gethostname()
port = 999

# binding host & port with socket
server_socket.bind((host, port))

# statring TCP listener of three contections
server_socket.listen(5)


while True:
    # starting the  from clinet
    client_socket, address = server_socket.accept()
    print(f"receved connection from {address} has been established!")

    message = "Welcome to the Server!"
    # fixed lenth to the left for 10 characters
    message = f"{len(message):<{HEADER_SIZE}}" + message
    print(message)

    # sending information to the client socket
    client_socket.send(bytes(message, "utf-8"))

    while True:
        time.sleep(3)
        message = f"The time is! {time.time()}"
        message = f"{len(message):<{HEADER_SIZE}}" + message
        print(message)
        client_socket.send(bytes(message, "utf-8"))
