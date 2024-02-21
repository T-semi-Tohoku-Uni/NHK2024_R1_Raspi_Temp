import socket
import json
from typing import Dict
from connect_with_can import send_message_on_can, receive_message
import sys
import can
import multiprocessing
from can_list import CANList
from enum import Enum

ARM_EXPANDER = 0x103
HAND1 = 0x105
HAND2 = 0X106
ARM_ELEVATOR = 0x104
ARM1 = 0x108
SHOOT = 0x101
BALL_HAND = 0x102
ROBOT_VEL = 0x10B

# ハンドの状態を表す列挙型
class HAND_STATE(Enum):
    OPEN_WAIT = 0
    OPEN_FINISH = 1
    CLOSE_WAIT = 2
    CLOSE_FINISH = 3
    
class BALL_STATE(Enum):
    WAIT = 0
    FINISH = 1
    
class HAND_POS(Enum):
    POS1_WAIT = 0
    POS1_FINISH = 1
    POS2_WAIT = 2
    POS2_FINISH = 3
    POS3_WAIT = 4
    POS3_FINISH = 5
    
# HAND1_State = HAND_STATE.OPEN_WAIT

# ハンドの状態を格納するクラス
class HandStates:
    def __init__(self):
        self.pos = HAND_STATE.OPEN_WAIT
        self.hand_pos = HAND_POS.POS1_WAIT
        self.hand1_state = HAND_STATE.OPEN_WAIT
        self.hand2_state = HAND_STATE.OPEN_WAIT
        self.ball_in_state = BALL_STATE.WAIT
        self.ball_shoot_state = BALL_STATE.WAIT
 

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
            self.btn_lb = data["btn_lb"]
            self.btn_rb = data["btn_rb"]
            self.start_btn = data["start_btn"]
        except Exception as e:
            print("err at ControllerData::__init__  {e}")
            sys.exit(1)
    
    def __repr__(self):
        return str(self.__dict__)

def parse_message(data: ControllerData, hand_states: HandStates, bus):
    # if data.btn_a == 1:
    #     send_message_on_can(HAND1, bytearray([1]), bus)
    #     HAND1_State = 1
    
    # ボタンA関連(HAND1)
    if data.btn_a == 1 and hand_states.hand1_state == HAND_STATE.OPEN_WAIT:
        send_message_on_can(HAND1, bytearray([1]), bus)
        print("open")
        hand_states.hand1_state = HAND_STATE.OPEN_FINISH
    
    if data.btn_a == 0 and hand_states.hand1_state == HAND_STATE.OPEN_FINISH:
        hand_states.hand1_state = HAND_STATE.CLOSE_WAIT
    
    if data.btn_a == 1 and hand_states.hand1_state == HAND_STATE.CLOSE_WAIT:
        send_message_on_can(HAND1, bytearray([0]), bus)
        print("close")
        hand_states.hand1_state = HAND_STATE.CLOSE_FINISH
    
    if data.btn_a == 0 and hand_states.hand1_state == HAND_STATE.CLOSE_FINISH:
        hand_states.hand1_state = HAND_STATE.OPEN_WAIT
        
    # ボタンB関連(HAND2)
    if data.btn_b == 1 and hand_states.hand2_state == HAND_STATE.OPEN_WAIT:
        send_message_on_can(HAND2, bytearray([1]), bus)
        hand_states.hand2_state = HAND_STATE.OPEN_FINISH
    
    if data.btn_b == 0 and hand_states.hand2_state == HAND_STATE.OPEN_FINISH:
        hand_states.hand2_state = HAND_STATE.CLOSE_WAIT
    
    if data.btn_b == 1 and hand_states.hand2_state == HAND_STATE.CLOSE_WAIT:
        send_message_on_can(HAND2, bytearray([0]), bus)
        hand_states.hand2_state = HAND_STATE.CLOSE_FINISH
    
    if data.btn_b == 0 and hand_states.hand2_state == HAND_STATE.CLOSE_FINISH:
        hand_states.hand2_state = HAND_STATE.OPEN_WAIT
        
    # ボタンY関連(ARM_EXPANDER)
    if data.btn_y == 1 and hand_states.pos == HAND_STATE.OPEN_WAIT:
        send_message_on_can(ARM_ELEVATOR, bytearray([1]), bus)
        hand_states.pos = HAND_STATE.OPEN_FINISH
    
    if data.btn_y == 0 and hand_states.pos == HAND_STATE.OPEN_FINISH:
        hand_states.pos = HAND_STATE.CLOSE_WAIT
    
    if data.btn_y == 1 and hand_states.pos == HAND_STATE.CLOSE_WAIT:
        send_message_on_can(ARM_ELEVATOR, bytearray([0]), bus)
        hand_states.pos = HAND_STATE.CLOSE_FINISH
    
    if data.btn_y == 0 and hand_states.pos == HAND_STATE.CLOSE_FINISH:
        hand_states.pos = HAND_STATE.OPEN_WAIT
        
    if data.start_btn == 1:
        send_message_on_can(ARM_EXPANDER, bytearray([1]), bus)
    
    # ボタンX関連
    if data.btn_x == 1 and hand_states.hand_pos == HAND_POS.POS1_WAIT:
        send_message_on_can(ARM1, bytearray([1]), bus)
        hand_states.hand_pos = HAND_POS.POS1_FINISH
    
    if data.btn_x == 0 and hand_states.hand_pos == HAND_POS.POS1_FINISH:
        hand_states.hand_pos = HAND_POS.POS2_WAIT
    
    if data.btn_x == 1 and hand_states.hand_pos == HAND_POS.POS2_WAIT:
        send_message_on_can(ARM1, bytearray([2]), bus)
        hand_states.hand_pos = HAND_POS.POS2_FINISH
    
    if data.btn_x == 0 and hand_states.hand_pos == HAND_POS.POS2_FINISH:
        hand_states.hand_pos = HAND_POS.POS3_WAIT
        
    if data.btn_x == 1 and hand_states.hand_pos == HAND_POS.POS3_WAIT:
        send_message_on_can(ARM1, bytearray([3]), bus)
        hand_states.hand_pos = HAND_POS.POS3_FINISH
    
    if data.btn_x == 0 and hand_states.hand_pos == HAND_POS.POS3_FINISH:
        hand_states.hand_pos = HAND_POS.POS1_WAIT
        
    # ボールの争点
    if data.btn_lb == 1 and hand_states.ball_in_state == BALL_STATE.WAIT:
        send_message_on_can(BALL_HAND, bytearray([0]), bus)
        hand_states.ball_in_state = BALL_STATE.FINISH
    
    if data.btn_lb == 0 and hand_states.ball_in_state == BALL_STATE.FINISH:
        hand_states.ball_in_state = BALL_STATE.WAIT
        
    # 発射
    if data.btn_rb == 1 and hand_states.ball_shoot_state == BALL_STATE.WAIT:
        send_message_on_can(SHOOT, bytearray([0]), bus)
        hand_states.ball_shoot_state = BALL_STATE.FINISH
        
    if data.btn_rb == 0 and hand_states.ball_shoot_state == BALL_STATE.FINISH:
        hand_states.ball_shoot_state = BALL_STATE.WAIT
    
    send_message_on_can(ROBOT_VEL, bytearray([data.v_x, data.v_y, data.omega]), bus)
    # send_message_on_can(CANList.ARM_ELEVATOR, bytearray([data.v_x, data.v_y, data.omega]), bus)

def start_udp_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    print(f"UDP server listening on {ip}:{port}")
    
    hand_stetes = HandStates()

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
                    parse_message(ctr_data, hand_stetes, bus)
                except json.JSONDecodeError:
                    print("Invalid JSON format")
                    continue
            
    except KeyboardInterrupt:
        print("Server stopped")

if __name__ == "__main__":
    # server settings
    host_name = "raspberrypi.local"
    port = 12345
    
    # with can.interface.Bus(channel='can0', bustype='socketcan') as bus: 
        # notifier = receive_message(bus)
        
        # try:
    start_udp_server(host_name, port)
        # except KeyboardInterrupt:
            # notifier.stop()
            # pass

