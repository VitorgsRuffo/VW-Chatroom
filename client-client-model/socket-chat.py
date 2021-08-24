
import socket
import select
import sys
from _thread import *








class SocketChat:
    def __init__(self, ip: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)       #Entender essa linha
        self.socket.bind((ip, port))
        self.socket.listen(100)


    def __menu(self):
        pas
        # print (1 - Se conectar a um server)
        # print (2 - Esperar conexão)
        #limpar tela

        #if(1):
            #infore ip e port
            #connect(ip, port, nickname)

        #if(2):
            #print(aguardando conexao...)
            #accept
            #aceita ou nao 
            #print(pessoa conectou)


    def run(self):
        pass











print("\n\nWelcome to your VW chat!\n")
ip = input("Enter you computer's IP address:")
port = input("Enter the port in which the application will run:")
chat = SocketChat(ip, port)
chat.run()
