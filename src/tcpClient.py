import socket
import threading

from src.logUtil import LogUtil


class TcpClient:

    def __init__(self):
        LogUtil.instance().print("TcpClient __init__")

    def connect(self, ip, port):
        try:
            self.ip = ip
            self.port = port
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.tcp_client.settimeout(1)
            self.tcp_client.connect((self.ip, self.port))
            self.recv = ''
            LogUtil.instance().print("TcpClient connect success")
            return True
        except Exception as e:
            try:
                LogUtil.instance().print("TcpClient connect exception: " + str(e.args))
                return False
            finally:
                e = None
                del e

    def getMessageThread(self):
        while True:
            try:
                data, addr = self.tcp_client.recvfrom(1024)
                self.recv = data.decode()
            except socket.timeout:
                LogUtil.instance().print("socket timeout")
                break

    def getMessage(self):
        return self.recv

    def sendMessage(self, message):
        self.tcp_client.send(message.encode(encoding='utf-8'))

    def close(self):
        self.tcp_client.close()
        LogUtil.instance().print("TcpClient 已关闭")


if __name__ == '__main__':
    T = TcpClient()
    T.connect('127.0.0.1', 502)
    thread_getMessage = threading.Thread(target=T.getMessage)
    thread_getMessage.setDaemon(True)
    thread_getMessage.start()
    T.sendMessage("hello")
    T.close()
