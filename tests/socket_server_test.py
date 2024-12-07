from threading import Thread
from time import sleep

from app.unity_conn import SocketServer
from app.logging_config import setup_logging

setup_logging()

server = SocketServer()
server_thread = Thread(target=server.start, daemon=True)
server_thread.start()

sleep(1)

try:
    while True:
        print("\n送信オプション: ")
        print("1: コマンドを送信")
        print("2: ファイルを送信")
        print("q: サーバーを停止")

        option = input("選択してください: ").strip()

        if option == "1":
            command = input("送信するコマンド: ").strip()
            server.send_command(command)
        elif option == "2":
            file_path = input("送信するファイルのパス: ").strip()
            server.send_file(file_path)
        elif option.lower() == "q":
            server.stop()
            break
        else:
            print("無効な選択です。もう一度試してください")
except FileNotFoundError as e:
    print(f"ファイルが見つかりません: {e}")
except KeyboardInterrupt:
    print("\nサーバーを停止します")
    server.stop()
