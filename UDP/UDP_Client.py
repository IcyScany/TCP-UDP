from socket import *
import time

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

k = 0   # 计算丢包数
stime = 0
maxtime = 0
mintime = 1000
for i in range(10):
    try:
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # 开始时间
        start_time = time.perf_counter()
        # 请求最大时间
        clientSocket.settimeout(1)
        message = ('Ping %d %s' % (i+1, time_str))
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        # 结束时间
        end_time = time.perf_counter()
        RTT = (end_time - start_time)*1000
        if maxtime < RTT:
            maxtime = RTT
        if mintime > RTT:
            mintime = RTT
        stime = stime + RTT
        print(modifiedMessage.decode(), 'RTT:%0.5fms' % RTT)
    except timeout:
        print('请求超时')
        k += 1
clientSocket.close()

print('最大RTT:%0.5fms,最小RTT:%0.5fms' % (maxtime, mintime))
print('丢包率：%d%%, 平均请求时间:%0.5fms' % (k*10, stime/(10-k)))
