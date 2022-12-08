from socket import*
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 12000))
serverSocket.listen(1)

f = open('test.jpg', 'rb')
pic_content = b'''
HTTP/1.x 200 OK
Content-Type: image/jpg
'''
pic_content = pic_content+f.read()
f.close()

while True:
    print('The server is ready to recieve')
    connectionSocket, addr = serverSocket.accept()
    request = connectionSocket.recv(1024).decode()
    # 获取用户请求的文件路径
    file = request.split(' ')[1]
    # 成功响应报文
    try:
        if file == '/test.jpg':
            response = pic_content
        else:
            # 请求文件内容
            with open('.' + file, 'rb') as f:
                data = f.read()
            response_line = 'HTTP/1.1 200 OK\r\n'
            response_header = 'Server:pwb\r\n\r\n'
            response_body = data
            response = (response_line + response_header + '\r\n').encode() + response_body
        connectionSocket.sendall(response)
        connectionSocket.close()
    # 未找到请求文件
    except IOError:
        response_line = 'HTTP/1.1 404 NOT FOUND\r\n'
        response_header = 'Server:pwb\r\n'
        response_body = '404 NOT FOUND!'
        response = (response_line + response_header + '\r\n').encode() + response_body.encode()
        connectionSocket.send(response)
        connectionSocket.close()
