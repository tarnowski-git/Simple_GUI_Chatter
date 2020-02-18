import socket
import select
import time

HEADER_LENGHT = 10

# creating the socket object - ipv4, tcp ip
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# allow to reconnet
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# store the host IP address
host = socket.gethostname()
port = 999

# binding host & port with socket
server_socket.bind((host, port))

# statring TCP listener of three contections
server_socket.listen(5)

socket_list = [server_socket]

# while True:
#     # starting the  from clinet
#     client_socket, address = server_socket.accept()
#     print(f"receved connection from {address} has been established!")

#     message = "Welcome to the Server!"
#     # fixed lenth to the left for 10 characters
#     message = f"{len(message):<{HEADER_SIZE}}" + message
#     print(message)

#     # sending information to the client socket
#     client_socket.send(bytes(message, "utf-8"))

#     while True:
#         time.sleep(3)
#         message = f"The time is! {time.time()}"
#         message = f"{len(message):<{HEADER_SIZE}}" + message
#         print(message)
#         client_socket.send(bytes(message, "utf-8"))


clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGHT)
        if not len(message_header):
            return False
        message_lenght = int(message_header.decode("utf-8").strip())
        # return a dictionary type
        return {"header": message_header, "data": client_socket.recv(message_lenght)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(
        socket_list, [], socket_list)

    for notified_sockets in read_sockets:
        if notified_sockets == server_socket:
            client_socket, client_address = server_socket.accept()
            # get the dictionary
            user = receive_message(client_socket)
            if user is False:
                continue

            socket_list.append(client_socket)
            clients[client_socket] = user
            print(
                f"Accepyer new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
        else:
            message = receive_message(notified_sockets)

            if message is False:
                print(
                    f"Close connection from {clients[notified_sockets]['data'].decode('utf-8')}")
                socket_list.remove(notified_sockets)
                del clients[notified_sockets]
                continue
            user = clients[notified_sockets]
            print(f"Received message")

            for client_socket in clients:
                if client_socket != notified_sockets:
                    client_socket.send(
                        user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]
