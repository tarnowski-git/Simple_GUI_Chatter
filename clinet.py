import tkinter as tk
import socket
from threading import Thread


class Main_Application(tk.Frame):
    """Main class of application"""

    PORT = 33000
    BUFSIZ = 1024

    def __init__(self, master, host):
        super().__init__(master)
        self.master = master
        # init network
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, self.PORT))
        # init gui
        self.configure_gui()
        self.create_widgets()
        self.setup_layout()
        # create a communication thread
        receive_thread = Thread(target=self.receive)
        receive_thread.start()

    def configure_gui(self):
        """Setting general configurations of the application"""
        self.master.title("Chatter")
        self.master.resizable(0, 0)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """Creating the widgets of the application"""
        # create a subframe for new buttons
        self.messages_frame = tk.Frame(
            self.master, bg="white", borderwidth=1, relief="raised")
        # For the messages to be sent.
        self.my_msg = tk.StringVar()
        # Following will contain the messages.
        self.msg_list = tk.Listbox(self.messages_frame, height=15, width=100)
        # To navigate through past messages.
        self.scrollbar = tk.Scrollbar(self.messages_frame)
        self.scrollbar.configure(command=self.msg_list.yview)
        self.msg_list.configure(yscrollcommand=self.scrollbar.set)

        self.entry_field = tk.Entry(
            self.messages_frame, textvariable=self.my_msg, width=40)
        # bind Enter key with textbox
        self.entry_field.bind("<Return>", self.send)
        self.send_button = tk.Button(
            self.messages_frame, text="Send", command=self.send)

    def setup_layout(self):
        """Setup grid system"""
        # subframs for relative griding
        self.messages_frame.grid(row=0, sticky=tk.W+tk.E, pady=0)
        # ChatField
        self.msg_list.grid(row=0, column=0, columnspan=10,
                           rowspan=6, pady=20, padx=20)
        self.scrollbar.grid(row=0, column=10, rowspan=6, sticky=tk.N+tk.S)
        # TextFieldToSend
        self.entry_field.grid(row=7, column=0, columnspan=10, pady=10)
        # SendMessageButton
        self.send_button.grid(row=7, column=7, columnspan=2)

    # ======== Buttons function ========
    def send(self, event=None):
        """Handles sending of messages."""
        msg = self.my_msg.get()
        # reset textbox
        self.my_msg.set("")
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "EXIT":
            self.client_socket.close()
            self.exit()

    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.msg_list.insert(tk.END, msg)
            except OSError as e:  # Possibly client has left the chat.
                print("Connection problem:", str(e))
                break

    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self.my_msg.set("EXIT")
        self.send()

    def exit(self):
        """Closing the program"""
        # stops mainloop
        self.master.quit()
        # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        self.master.destroy()


# this means that if this script is executed, then
# main() will be executed
if __name__ == "__main__":
    host = input('Enter host: ')
    root = tk.Tk()
    application = Main_Application(master=root, host=host)
    application.mainloop()
