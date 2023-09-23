import socket

import websocket
from websocket import ABNF
import json
import _thread
import time

url = "ws://system.stead:2346/"  # 接口地址
wav_path = "D:/audio_file/001/001M26_01_01_0001.pcm"  # 音频文件地址


def on_message(ws,message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("close connection")


def on_open(ws):
    def run(*args):
        content = {
            "mid": "1508232047195",
            "version": "1.0",
            "request": {
                "timestamp": 1508232047195,
                "sessionId": "aaaadsfasdfkop"
            },
            "params": {
                "audio": {
                    "audioType": "wav",
                    "sampleRate": 16000,
                    "channel": 1,
                    "sampleBytes": 2
                }
            }
        }
        ws.send(json.dumps(content))
        while True:
            pc_name = socket.getfqdn(socket.gethostname())
            pc_ip = socket.gethostbyname(pc_name)
            ws.send(json.dumps({"pc_ip": pc_ip, 'time': time.time()}))
            time.sleep(3.5)

    _thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
