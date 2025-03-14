import socket
import json
import datetime

# 设置 OpenBCI 服务器的地址和端口
server_ip = "127.0.0.1"  # 替换为实际的 OpenBCI 服务器 IP 地址
local_port = 12345       # 替换为实际的 OpenBCI 服务器端口

# 创建 UDP 客户端套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # 绑定客户端套接字到本地端口（如果需要的话）
    client_socket.bind(("0.0.0.0", local_port))

    # 创建文件对象并打开文件以进行写入
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"data_{current_time}.txt"
    file = open(filename, "w")

    # 接收数据并打印
    while True:
        # time.sleep(1)
        data, server_address = client_socket.recvfrom(1024)
        data = data.decode('utf-8')
        data = json.loads(data)
        print(data['data'])

        # 将数据转换为JSON格式并写入文件
        json_data = json.dumps(data['data'])
        file.write(json_data + "\n")

except KeyboardInterrupt:
    print("Client stopped.")

finally:
    # 关闭套接字
    client_socket.close()

    # 关闭文件对象
    file.close()