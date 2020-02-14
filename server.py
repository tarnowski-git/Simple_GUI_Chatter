import socket

# creating the socket object - ipv4, tcp ip
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# store the host IP address
host = socket.gethostname()
port = 444

# binding host & port with socket
server_socket.bind((host, port))

# statring TCP listener of three contections
server_socket.listen(3)


while True:
    # starting the  from clinet
    client_socket, address = server_socket.accept()

    print(f"receved connection from {address} has been established!")

    message = "Thank you for connecting to the server" + "\r\n"

    # sending information to the client socket
    client_socket.send(bytes("Welcome to the server!", "utf-8"))

    client_socket.close()
