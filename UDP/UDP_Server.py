from socket import *
import random

# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))
print('The server is ready to receive')
while True:
    rand = random.randint(0, 10)    # 模拟丢包
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    print(modifiedMessage)
    if rand < 3:    # 丢包率30%
        continue
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
