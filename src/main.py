import socket
import json
from typing import Dict
import connect_with_can

class ControllerData:
    """
    コントローラーのデータを格納するクラス
    
    Attributes
    ------------
    joy_lx : int
        左スティックのx軸の値
    joy_ly : int
        左スティックのy軸の値
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
        for key, value in data.items():
            # 念の為型チェック
            if key == "joy_lx":
                if not isinstance(value, int):
                    raise ValueError("joy_lx must be int")
                else:
                    setattr(self, key, value)
                    continue
            elif key == "joy_ly":
                if not isinstance(value, int):
                    raise ValueError("joy_ly must be int")
                else:
                    setattr(self, key, value)
                    continue
            elif key == "btn_a":
                if not isinstance(value, int):
                    raise ValueError("btn_a must be int")
                else:
                    setattr(self, key, value)
                    continue
            elif key == "btn_b":
                if not isinstance(value, int):
                    raise ValueError("btn_b must be int")
                else:
                    setattr(self, key, value)
                    continue
            elif key == "btn_x":
                if not isinstance(value, int):
                    raise ValueError("btn_x must be int")
                else:
                    setattr(self, key, value)
                    continue
            elif key == "btn_y": 
                if not isinstance(value, int):
                    raise ValueError("btn_y must be int")
                else:
                    setattr(self, key, value)
                    continue
            else:
                raise ValueError(f"Invalid key: {key}")
    
    def __repr__(self):
        return str(self.__dict__)

def start_udp_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    print(f"UDP server listening on {ip}:{port}")

    try:
        while True:
            data, addr = sock.recvfrom(1024)  # バッファサイズは1024バイト
            try:
                message: Dict = json.loads(data.decode())
                ctr_data = ControllerData(message)
                print(f"Data received: {ctr_data}")
            except json.JSONDecodeError:
                print("Invalid JSON format")
                continue
            
    except KeyboardInterrupt:
        print("Server stopped")

if __name__ == "__main__":
    # server settings
    host_name = "raspberrypi.local"
    port = 12345
    
    start_udp_server("raspberrypi.local", port)

