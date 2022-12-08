from socket import*
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('127.0.0.1', 12000))

# 访问文件报文
request = b'GET /1.html HTTP/1.1\
            Host: 127.0.0.1:12000\r\n\r\n'
clientSocket.send(request)
recv = b''
# 读取响应报文
while True:
    data = clientSocket.recv(1024)
    recv += data
    if len(data) < 1024:
        break
clientSocket.close()
print('From Server:', recv.decode())
# 将网页存入html文件
recv = recv.decode()
content = recv.split('\r\n\r\n')[1]
with open('recv.html', 'wb') as f:
    f.write(content.encode())
