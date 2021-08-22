
# Python program to implement client side of chat room.
import socket
import select
import sys

class ChatClient:
    def __init__(self, ip: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def connect(self):
        self.socket.connect((self.ip, self.port))
        
        while True:
            sockets_list = [sys.stdin, self.socket]

            read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

            for socks in read_sockets:
                if socks == self.socket:
                    message = socks.recv(2048).decode('ascii')
                    print(message)
                else:
                    message = sys.stdin.readline()
                    self.socket.send(message.encode('ascii'))
                    sys.stdout.write("<You>")
                    sys.stdout.write(message)
                    sys.stdout.flush()
        
        socket.close()



if len(sys.argv) != 3:
    print ("Por favor, forneça o ip e a porta do servidor do chat.\nExemplo: python3 chat_client.py <ip> <porta>\n")
    exit()
 

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

chat_client = ChatClient(IP_address, Port)
chat_client.connect()