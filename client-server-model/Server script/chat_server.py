# to do list:
#  - format chat strings.
#  - connect without hamachi.
#

from os import remove
import socket
import select
import sys
from _thread import *


class ChatServer:
    def __init__(self, ip: str, port: int, listen: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((ip, port))
        self.socket.listen(listen)
        self.clients = []

            
    def __remove_connection(self, connection):
        if connection in self.clients:
            self.clients.remove(connection)


    def __broadcast(self, message, connection):
        for client in self.clients:
            if client != connection:
                try:
                    client.send(message.encode('ascii'))
                
                except:
                    client.close()
                    self.__remove_connection(client)

    def __client_thread(self, conn, addr):
        conn.send(str("Welcome to <vw> chatroom!").encode('ascii'))
        while True:
            try:
                message = conn.recv(2048).decode("ascii")
                if message:
                    print("<" + addr[0] + "> " + message)
                    message_to_send = "<" + addr[0] + "> " + message
                    self.__broadcast(message_to_send, conn)
 
                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    self.__remove_connection(conn)
 
            except:
                continue


    def run(self):
        while True:
            conn, addr = self.socket.accept()

            self.clients.append(conn)
            print(addr[0] + " connected")
            start_new_thread(self.__client_thread,(conn, addr))
        self.socket.close()
    

if len(sys.argv) != 3:
    print ("Por favor, forneça o ip e a porta do servidor.\nExemplo: python3 char_server.py <ip> <porta>\n")
    exit()
 

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

chat_server = ChatServer(IP_address, Port, 100)
chat_server.run()
