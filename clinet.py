import socket
import select
import errno
import sys

HEADER_LENGTH = 10

my_username = input("Username: ")

# Create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 999

# connecting with server
client_socket.connect((host, port))
client_socket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")

    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

    # receive things
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_lenght = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_lenght).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue

    except Exception as e:
        print("General error", str(e))
        sys.exit()

# while True:
#     full_massage = ""
#     new_massege = True
#     while True:
#         # Receiving a maximum of 16 bytes / buffer for chunks
#         message = client_socket.recv(16)
#         if new_massege:
#             print(f"new message lenght: {message[:HEADER_SIZE]}")
#             message_lenght = len(message[: HEADER_SIZE])
#             new_massege = False

#         full_massage += message.decode("utf-8")

#         if len(full_massage) - HEADER_SIZE == message_lenght:
#             print("full message recvd")
#             print(full_massage[10:])
#             new_massege = True
#             full_massage = ""

#     print(full_massage)
