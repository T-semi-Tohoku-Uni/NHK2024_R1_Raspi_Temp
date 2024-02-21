import socket
import json
from typing import Dict
from connect_with_can import send_message_on_can, receive_message
import sys
import can
import multiprocessing

class ControllerData:
    """
    コントローラーのデータを格納するクラス
    
    Attributes
    ------------
    v_x : int
        x方向の速度
    v_y : int
        y方向の速度
    omega: 
        角速度
    btn_a : int
        Aボタンの状態
    btn_b : int
        Bボタンの状態
    btn_x : int
        Xボタンの状態
    btn_y : int
        Yボタンの状態
        
    Methods
    ------------
    __init__(data: Dict)
        コンストラクタ
    __repr__()
        オブジェクトの文字列表現を返す
    """
    def __init__(self, data: Dict):
        """
        初期化メソッド
        
        Parameters
        ------------
        data : Dict
            コントローラーのデータ（Dict形式）
        """
        try:
            self.v_x = data["v_x"]
            self.v_y = data["v_y"]
            self.omega = data["omega"]
            self.btn_a = data["btn_a"]
            self.btn_b = data["btn_b"]
            self.btn_x = data["btn_x"]
            self.btn_y = data["btn_y"]
        except Exception as e:
            print("err at ControllerData::__init__  {e}")
            sys.exit(1)
    
    def __repr__(self):
        return str(self.__dict__)

def parse_message(data: ControllerData, bus):
    if data.btn_a == 1:
        print("btn_a is pushed")
        
    send_message_on_can(0x106, bytearray([data.v_x, data.v_y, data.omega]), bus)

def start_udp_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    print(f"UDP server listening on {ip}:{port}")

    try:
        with can.interface.Bus(channel='can0', bustype='socketcan', bitrate=5000000) as bus:
            while True:
                data, addr = sock.recvfrom(1024)  # バッファサイズは1024バイト
                try:
                    message: Dict = json.loads(data.decode())
                    ctr_data = ControllerData(message)
                    print(f"v_x is {ctr_data.v_x} and v_y is {ctr_data.v_y}")
                    # p = multiprocessing.Process(target=parse_message, args=(ctr_data,))
                    # p.start()
                    # print(f"Data received: {ctr_data}")
                    parse_message(ctr_data, bus)
                except json.JSONDecodeError:
                    print("Invalid JSON format")
                    continue
            
    except KeyboardInterrupt:
        print("Server stopped")

if __name__ == "__main__":
    # server settings
    host_name = "R2.local"
    port = 12345
    
    # with can.interface.Bus(channel='can0', bustype='socketcan') as bus: 
        # notifier = receive_message(bus)
        
        # try:
    start_udp_server(host_name, port)
        # except KeyboardInterrupt:
            # notifier.stop()
            # pass

