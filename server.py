# Server for multithreaded (asynchronous) chat application.
import socket
import select
from threading import Thread


class Server:

    HOST = socket.gethostname()
    PORT = 33000
    BUFSIZ = 1024

    def __init__(self):
        # define dictionaries
        self.clients = {}
        self.addresses = {}
        # init server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server IP: {}".format(self.HOST))
        self.server.bind((self.HOST, self.PORT))
        self.server.listen(5)

    def run(self):
        print("Waiting for connection...")
        accept_thread = Thread(target=self.accept_incoming_connections)
        accept_thread.start()
        # the main script waits for it to complete and doesn’t
        # jump to the next line, which closes the server.
        accept_thread.join()
        self.server.close()

    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            client, client_address = self.server.accept()
            print("{} has connected.".format(client_address))
            client.send(
                bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
            # add address to the dictionary
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        """Handles a single client connection. Takes client socket as argument."""
        name = client.recv(self.BUFSIZ).decode("utf8")
        welcome = "Welcome {}! If you ever want to quit, type EXIT to exit.".format(
            name)
        client.send(bytes(welcome, "utf8"))
        msg = "{} has joined the chat!".format(name)
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name

        while True:
            msg = client.recv(self.BUFSIZ)
            if msg != bytes("EXIT", "utf8"):
                self.broadcast(msg, name+": ")
            else:
                client.send(bytes("EXIT", "utf8"))
                client.close()
                del self.clients[client]
                self.broadcast(
                    bytes("{} has left the chat.".format(name), "utf8"))
                break

    def broadcast(self, msg, prefix=""):
        """Broadcasts a message to all the clients.
        prefix is for name identification."""

        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)


# this means that if this script is executed, then
# main() will be executed
if __name__ == "__main__":
    server = Server()
    server.run()
