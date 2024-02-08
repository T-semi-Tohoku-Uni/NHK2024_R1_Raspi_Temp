import socket

def start_udp_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    print(f"UDP server listening on {ip}:{port}")

    while True:
        data, addr = sock.recvfrom(1024)  # バッファサイズは1024バイト
        print(f"Received message: {data} from {addr}")

        # 応答を送る場合は以下のコメントを外す
        # sock.sendto(b"Received your message", addr)

if __name__ == "__main__":
    start_udp_server("raspberrypi.local", 12345)

