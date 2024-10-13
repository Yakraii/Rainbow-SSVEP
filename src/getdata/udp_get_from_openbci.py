import socket
import time
import json
# 设置 OpenBCI 服务器的地址和端口
server_ip = "127.0.0.1"  # 替换为实际的 OpenBCI 服务器 IP 地址
local_port = 12345       # 替换为实际的 OpenBCI 服务器端口

# 创建 UDP 客户端套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # 绑定客户端套接字到本地端口（如果需要的话）
    client_socket.bind(("0.0.0.0", local_port))

    # 接收数据并打印
    while True:
        # time.sleep(1)
        data, server_address = client_socket.recvfrom(1024)
        data = data.decode('utf-8')
        data = json.loads(data)
        print(data['data'])
        print("Received data:", data)

except KeyboardInterrupt:
    print("Client stopped.")

finally:
    # 关闭套接字
    client_socket.close()