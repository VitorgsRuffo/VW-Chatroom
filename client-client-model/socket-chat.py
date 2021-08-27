import socket
import select
import sys
from _thread import *


class SocketChat:
    def __init__(self, ip: str, port: int):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ip, port))
        self.server_socket.listen(100)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __menu(self):
        print("---------------------------")
        print("         VW chat\n")
        print("1 - Connect.")
        print("2 - Wait for connection.")
        print("3 - Exit.")
        print("---------------------------")

    def __connect_on_server(self):

        ip = input("Enter the IP you want to connect with:")
        port = int(input("Enter the port you want to connect with:"))

        self.client_socket.connect((ip, port))

        while True:
            sockets = [sys.stdin, self.client_socket]

            read_sockets, write_socket, error_socket = select.select(sockets, [], [])

            for socket in read_sockets:
                if socket == self.client_socket:
                    message = socket.recv(2048).decode("ascii")
                    print(message)
                else:
                    message = sys.stdin.readline()
                    if message == "exit":
                        print("Exiting chat...")
                        return

                    ip = self.server_socket.getsockname()[0]
                    formated_message = "<" + ip + "> " + message
                    bytes_sent = self.client_socket.send(formated_message.encode("ascii"))
                    if bytes_sent == 0:
                        print("Connection closed...")
                        return

                    sys.stdout.write("<You>")
                    sys.stdout.write(message)
                    sys.stdout.flush()

    def __wait_for_client(self):

        print("Waiting for a connection...")
        while True:
            connection, addr = self.server_socket.accept()

            print("{}:{} wants to connect.".format(addr[0], addr[1]))
            print("Do you accept ? (y/n)")
            allow = input()

            if (allow == "n") | (allow == "N"):
                connection.shutdown(socket.SHUT_RD)
                connection.close()
            else:
                break

        print("{}:{} just to connected!".format(addr[0], addr[1]))
        print("(Type \"exit\" to exit the chat)")

        ip = self.server_socket.getsockname()[0]

        connection.send(str("You connected to {}.\n(Type \"exit\" to exit the chat)".format(ip)).encode('ascii'))

        while True:
            sockets = [sys.stdin, connection]

            read_sockets, write_socket, error_socket = select.select(sockets, [], [])

            for socket in read_sockets:
                if socket == connection:
                    message = socket.recv(2048).decode('ascii')
                    print(message)
                else:
                    message = sys.stdin.readline()
                    if message == "exit":
                        print("Exiting chat...")
                        return

                    formated_message = "<" + ip + "> " + message

                    bytes_sent = self.client_socket.send(formated_message.encode('ascii'))
                    if bytes_sent == 0:
                        print("Connection closed...")
                        return

                    sys.stdout.write("<You>")
                    sys.stdout.write(message)
                    sys.stdout.flush()

    def run(self):
        while True:
            self.__menu()
            option = int(input())

            if option == 1:
                self.__connect_on_server()
            elif option == 2:
                self.__wait_for_client()
            elif option == 3:
                print("Exiting chat...")
                return
            else:
                print("Invalid option. Please try again.")


print("\n\nWelcome to your VW chat!\n")
ip = input("Enter you computer's IP address:")
port = int(input("Enter the port in which the application will run:"))
chat = SocketChat(ip, port)
chat.run()
