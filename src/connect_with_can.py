import can
import time
from typing import List

class MessageListener(can.Listener):
    def on_message_received(self, msg):
        print(f"Received message: {msg}")
        
def receive_message(bus):
    listener = MessageListener()
    notifier = can.Notifier(bus, [listener])
    
    return notifier

"""
send message on can bus

Parameters
----------
    can_id: int
    data  : List[int]

Returns
-------
    None
"""
def send_message_on_can(can_id: int, data: List[int], bus):
    # CANインターフェースを設定
    # with can.interface.Bus(channel='can0', bustype='socketcan', bitrate=1000000) as bus: 
        # bus.flush_tx_buffer()

    # CANメッセージを作成
    msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)

    # メッセージを送信
    bus.send(msg, timeout=0.01)
    print("Message sent on {}".format(bus.channel_info))
    print("sent id is {}".format(msg.arbitration_id))
    print("sent message is {}".format(msg.data))
    time.sleep(0.01)

if __name__ == "__main__":
    with can.interface.Bus(channel='can0', bustype='socketcan', bitrate=5000000) as bus: 
    
        if bus is not None:
            notifier = receive_message(bus)
        
            try:
                # # while True:
                #     send_message_on_can(0x010, [0x00, 0x11, 0x22])
                #     time.sleep(1)
                #     # send_message_on_can(0x200, [0x11, 0x22, 0x33])
                #     # time.sleep(1)
                #     # send_message_on_can(0x300, [0x33, 0x44, 0x55])
                #     # time.sleep(1)
                # with can.interface.Bus(channel='can0', bustype='socketcan', bitrate=5000000) as bus: 
                    
                for i in range(100):
                    send_message_on_can(i + 3, [0x00, 0x11, 0x22], bus)
                    time.sleep(0.01)
            except KeyboardInterrupt:
                notifier.stop()
                pass
