import threading
from socket import*


# 处理用户请求报文函数
def deal_request(clientSocket):
    request = clientSocket.recv(1024).decode()
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
        clientSocket.sendall(response)
        clientSocket.close()
    # 请求失败报文
    except IOError:
        response_line = 'HTTP/1.1 404 NOT FOUND\r\n'
        response_header = 'Server:pwb\r\n'
        response_body = '404 NOT FOUND!'
        response = (response_line + response_header + '\r\n').encode() + response_body.encode()
        clientSocket.send(response)
        clientSocket.close()


f = open('test.jpg', 'rb')
pic_content = b'''
HTTP/1.x 200 OK
Content-Type: image/jpg

'''
pic_content = pic_content+f.read()
f.close()

if __name__ == '__main__':
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', 12000))
    serverSocket.listen(100)
    while True:
        print('The server is ready to recieve')
        clientSocket, addr = serverSocket.accept()
        # 创建子进程
        sub_thread = threading.Thread(target=deal_request, args=(clientSocket,))
        sub_thread.start()
