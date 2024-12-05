import os
import socket


class SocketServer:
    """
    Socketサーバーを管理するクラス
    """
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        self.running = False

    def start(self) -> None:
        """
        サーバを起動
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"サーバーが起動しました: {self.host}:{self.port}")
        self.running = True

        try:
            while self.running:
                print("クライアントの接続を待機中...")
                self.client_socket, self.client_address = self.server_socket.accept()
                print(f"クライアントが接続しました: {self.client_address}")
                self.handle_client(self.client_socket)
        except KeyboardInterrupt:
            print("サーバーを停止します")
        except Exception as e:
            print(f"サーバーでエラーが発生しました {e}")
        finally:
            self.stop()

    def stop(self) -> None:
        """
        サーバーを停止
        """
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        print("サーバーを完全に停止しました")

    def handle_client(self, client_socket: socket.socket) -> None:
        """
        クライアントとの通信を処理するスレッドを管理

        Args:
            client_socket (socket.socket): クライアントとの通信用ソケット
        """
        try:
            # クライアントからのデータを受け取る処理（必要なら実装）
            while self.running:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"クライアントからのデータ: {data}")
        except Exception as e:
            print(f"クライアント処理中にエラーが発生しました: {e}")
        finally:
            self.stop()
            print("クライアントとの接続を終了しました")

    def send_command(self, command: str) -> None:
        """
        クライアントにコマンドを送信

        Args:
            command (str): 送信するコマンド
        """
        if self.client_socket:
            try:
                message = f"COMMAND:{command}\n"
                self.client_socket.sendall(message.encode('utf-8'))
                print(f"コマンドを送信しました: {command}")
            except Exception as e:
                print(f"コマンド送信中にエラーが発生しました: {e}")

    def send_file(self, file_path: str) -> None:
        """
        クライアントにファイルを送信

        Args:
            file_path (str): 送信するファイルのパス

        Raises:
            FileNotFoundError: ファイルが見つからない場合
            e: その他のエラー
        """
        if self.client_socket:
            try:
                if not os.path.isfile(file_path):
                    raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

                # ファイル情報を送信
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                file_header = f"FILE:{file_name}:{file_size}\n"
                self.client_socket.sendall(file_header.encode('utf-8'))

                # ファイル内容を送信
                with open(file_path, "rb") as f:
                    while chunk := f.read(1024):
                        self.client_socket.sendall(chunk)

                print(f"ファイルを送信しました: {file_path}")
            except Exception as e:
                raise e
