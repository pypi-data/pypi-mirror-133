from os import error
import socket

SIZE = 1024
FORMAT = "utf-8"
SOCKET_TIMEOUT = 0.025

class InfoMark_Client:

    def __init__(self, serverIp, serverPort):
        self.serverIp = serverIp
        self.serverPort = serverPort

    def getData(self, dataName, amount):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(SOCKET_TIMEOUT)
        
        address = (self.serverIp, self.serverPort)
        client.connect(address)
        
        print(f"[CONNECTED] Client connected to server at {self.serverIp}:{self.serverPort}")

    
        msg = "get" + ',' + dataName + ',' + str(amount)
        client.send(msg.encode(FORMAT))

        #receive number of files that will be sent for the for cycle
        dataLimit = client.recv(SIZE).decode(FORMAT)
        
        for i in range(0, int(dataLimit)):
            
            #receive file name from server
            fileName = client.recv(SIZE).decode(FORMAT)
            print(fileName)
            
            with open(fileName, "wb") as file:
                try:
                    while True:
                        fileChunk = client.recv(SIZE)
                        if not fileChunk:
                            break
                        file.write(fileChunk)
                except socket.timeout:
                    file.close()
                    continue
        
        client.close()
