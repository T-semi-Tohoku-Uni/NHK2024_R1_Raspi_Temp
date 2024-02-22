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

この設定は起動時に毎回しないといけないので面倒だから, canの設定を記載したシェルスクリプト`can_init.sh`を起動時に実行するようにする. 
`/usr/local/bin`ディレクトリに設定ファイルをコピー
```
sudo cp can_init.sh /usr/local/bin/
```
実行権限の変更
```
sudo chmod 700 /usr/local/bin/can_init.sh
```
`/etc/rc.local`を開らく
```
sudo vim /etc/rc.local
```
`exit 0`の直前に追加
```
/usr/local/bin/can_init.sh &
```
再起動する
```
sudo reboot
```

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

## 起動時の設定
```
cd /etc/systemd/system/
sudo vim r1.service
```

以下の記述を`r1.serice`に書き込む
```
[Unit]
Description=仮想環境の起動とコマンドの実行

[Service]
# ディレクトリへ移動してから環境を有効にし、コマンドを実行
ExecStart=/bin/bash -c 'cd /home/pi/Devlopment/NHK2024_R1_Raspi; source ./env/bin/activate; python3 your_script.py'

[Install]
WantedBy=multi-user.target
```

起動させて動作チェック（`active`になってればOK）
```
sudo systemctl start r1.service
sudo systemctl status r1.service
```

プロセスの停止は
```
sudo systemctl stop r1.service
```

起動時実行を有効化
```
sudo systemctl enable r1.service
```

起動時実行を停止するには
```
sudo systemctl disable r1.service
```