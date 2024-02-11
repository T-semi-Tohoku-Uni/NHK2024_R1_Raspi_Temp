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
def send_message_on_can(can_id: int, data: List[int]):
    # CANインターフェースを設定
    with can.interface.Bus(channel='can0', bustype='socketcan') as bus: 

        # CANメッセージを作成
        msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)

        # メッセージを送信
        bus.send(msg)
        print("Message sent on {}".format(bus.channel_info))

if __name__ == "__main__":
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    
    if bus is not None:
        notifier = receive_message(bus)
    
        try:
            while True:
                #send_message_on_can(0x123, [0x11, 0x22, 0x33])
                time.sleep(0.1)
        except KeyboardInterrupt:
            notifier.stop()
            pass
