# NHK2024_R1_Raspi
ロボット1のラズパイのプログラム

## 実行方法
R1_Controllerと同じ


## CANの設定
CANFDが乗ってる`MCP2517FD`とラズパイでSPI通信してデータの送受信をするらしい.
設定などなどのまとめ
### `/boot/config.txt`
`/boot/config.txt`に以下の行を追加して(一番最後の行に追加), SPIの有効化, SPIのCSピンの割り当てとINTピンの割り当てを行う.
ピンの割り当ては
- `CE` : 27 (=> `SPI0_CE_0`に対応)
- `INT` : 24（GPIOの番号）

```
dtparam=spi=on
dtoverlay=mcp251xfd,spi0-0,interrupt=24
```

`spi0-0`は, SPI0（`MOSI` : 19, `MISO` : 21, `CLK` : 23のピン配置）の`CE_0`をチップセレクトピンとして使用するという意味. 
`interrupt`には`INT`のGPIOの番号を入れる（ピンの番号ではないので注意）

設定を有効化するために再起動する. コマンドラインに戻って次のコードを実行. 
```
sudo reboot 
```

### インターフェースの追加
LinuxにCAN通信用のデバイスファイル？を追加する.
```
sudo ip link set can0 up type can bitrate 1000000 dbitrate 1000000 fd on
```
- `bitrate`: 通常のCAN通信の速度（1MHz）
- `dbitrate` : FDCANの一部速度をはやくできる部分の速度（1MHz） => もう少しあげても耐える？

### `python`で書く
`python-can`ライブラリを使って簡単にできるらしい
```
$ sudo pip3 install --upgrade pip
$ pip install python-can
```

ChatGPT様のサンプルコード（まだ動作確認してない）
```
import can

def send_message():
    # CANインターフェースを設定
    bus = can.interface.Bus(channel='can0', bustype='socketcan')

    # CANメッセージを作成
    msg = can.Message(arbitration_id=0x123, data=[0x11, 0x22, 0x33], is_extended_id=False)

    # メッセージを送信
    bus.send(msg)
    print("Message sent on {}".format(bus.channel_info))

if __name__ == "__main__":
    send_message()

```