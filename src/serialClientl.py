import threading

import serial

from src.logUtil import LogUtil


class SerialClient:

    def __init__(self):
        LogUtil.instance().print("SerialClient __init__")
        self.recvMsg = ''

    def connect(self, port, rate, timeout=0.5):
        self.serial = serial.Serial(port, rate, timeout)
        if self.serial.isOpen():
            LogUtil.instance().print("SerialClient connect success")
            return True
        else:
            LogUtil.instance().print("SerialClient connect failed")
            return False

    def recv(self):
        while True:
            data = self.serial.read_all()
            if data == '':
                continue
            else:
                break
        return data

    def getMessageThread(self):
        while True:
            data = self.recv()
            if data != b'':
                print("receive : ", data)
                self.recvMsg += str(data)

    def getMessage(self):
        return self.recvMsg

    def sendMessage(self, message):
        self.serial.write(self, message.encode(encoding='utf-8'))

    def closeClient(self):
        self.serial.close()
        LogUtil.instance().print("SerialClient 已关闭")


if __name__ == '__main__':
    T = SerialClient()
    T.connect('COM1', 115200, 0.5)
    thread_getMessage = threading.Thread(target=T.getMessage)
    thread_getMessage.setDaemon(True)
    thread_getMessage.start()
    T.sendMessage('')
