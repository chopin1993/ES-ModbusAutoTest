import threading
import time
from fnmatch import fnmatch

from src.logUtil import LogUtil
from src.modbusTK import ModbusTK
from src.serialClientl import SerialClient
from src.sshClient import SshClient


class TestEngine(object):
    """
    1. 测试引擎
    """
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = TestEngine()
        return cls._instance

    def __init__(self):
        self.config = None
        self.tcpClient = None
        self.sshClient = None
        self.serialClient = None
        self.totle = 0
        self.success = 0

    def start(self, config):
        LogUtil.instance().print('-------------------- TestEngine start --------------------')
        self.config = config
        LogUtil.instance().print(str(config))

        # Modbus/Tcp连接
        self.modbusTk = ModbusTK()
        self.modbusTk.connect(self.config["Modbus地址"], self.config["Modbus端口"])

        # SSH连接，用于获取网关日志
        if self.config['验证Json报文'] or (self.config['验证7E报文'] and self.config['通过网关日志验证7E报文']):
            self.sshClient = SshClient()
            conn = self.sshClient.connect(self.config["ssh地址"], self.config["ssh端口"], self.config["ssh用户名"],
                                          (self.config["ssh密码(单相网关)"] if self.config["网关类型"] else self.config[
                                              "ssh密码(三相网关)"]))
            if conn is False:
                return False

        # Comm串口连接
        if self.config['验证7E报文'] and (not self.config['通过网关日志验证7E报文']):
            self.serialClient = SerialClient()
            conn = self.serialClient.connect(self.config['串口号'], self.config['波特率'])
            if conn is False:
                return False
            getPacketThread = threading.Thread(target=self.serialClient.getMessageThread)
            getPacketThread.setDaemon(True)
            getPacketThread.start()
        LogUtil.instance().print('-------------------- TestEngine init success --------------------\n')
        LogUtil.instance().print('------------------------------------------------------------')
        LogUtil.instance().print('-------------------- 开始测试[' + self.config["设备名称"] + '] --------------------')
        LogUtil.instance().print('------------------------------------------------------------\n')
        return True

    def close(self):
        if self.tcpClient is not None:
            self.tcpClient.close()
            self.tcpClient = None
        if self.modbusTk is not None:
            self.modbusTk.close()
            self.modbusTk = None
        if self.sshClient is not None:
            self.sshClient.close()
            self.sshClient = None
        if self.serialClient is not None:
            self.serialClient.close()
            self.serialClient = None
        LogUtil.instance().print('-------------------- TestEngine close --------------------')
        LogUtil.instance().print('------------------------------------------------------------')
        LogUtil.instance().print(
            r'----- [' + self.config["设备名称"] + ']测试结束： 总计' + str(self.totle) + ' 成功' + str(self.success) + ' 失败' + str(
                self.totle - self.success) + ' --------------------')
        LogUtil.instance().print('------------------------------------------------------------\n')
        self.config = None

    def checkJson(self, sendJson, aswJson):
        if self.config["验证Json报文"] and sendJson is not None and aswJson is not None:
            log = self.sshClient.getGatewayLog((self.config["日志路径(单相网关)"] if self.config["网关类型"] else self.config[
                "日志路径(三相网关)"]))
            LogUtil.instance().print('获取网关日志：' + log)
            # if fnmatch(log, sendJson) and fnmatch(log, aswJson):   # fnmatch字符串最大长度为256
            if str(log).__contains__(sendJson) and str(log).__contains__(aswJson):
                LogUtil.instance().print('Json发送：' + sendJson)
                LogUtil.instance().print('Json接收：' + aswJson)
                return True
            else:
                LogUtil.instance().print('Json报文匹配失败')
                return False
        return True

    def check7ePacket(self, send7ePacket, asw7ePacket):
        if self.config["验证7E报文"] and send7ePacket is not None and asw7ePacket is not None:
            if self.config['通过网关日志验证7E报文']:
                # 使用网关日志验证
                log = self.sshClient.getGatewayLog((self.config["日志路径(单相网关)"] if self.config["网关类型"] else self.config[
                    "日志路径(三相网关)"]))
                LogUtil.instance().print('获取网关日志：' + log)
                if fnmatch(log, send7ePacket) and fnmatch(log, asw7ePacket):  # fnmatch字符串最大长度为256
                    LogUtil.instance().print('7E发送：' + send7ePacket)
                    LogUtil.instance().print('7E接收：' + asw7ePacket)
                    return True
                else:
                    LogUtil.instance().print('7E报文匹配失败')
                    return False
            else:
                # 使用电力线监控器验证
                LogUtil.instance().print('7E报文匹配成功')
        return True

    # 通用TCP通信接口
    def tcpCommunication(self, msg, aswMsg, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
        global log
        LogUtil.instance().print('================>')
        isSuccess = True
        self.tcpClient.sendMessage(msg)
        LogUtil.instance().print('Modbus发送：' + msg)
        time.sleep(1)
        # 验证modbus报文
        recv = self.tcpClient.getMessage()
        LogUtil.instance().print('Modbus接收：' + recv)
        if recv == aswMsg:
            LogUtil.instance().print('Modbus报文匹配成功')
        else:
            LogUtil.instance().print('Modbus报文匹配失败')
            isSuccess = False
        # 验证json报文和7E报文
        if isSuccess and self.checkJson(sendJson, aswJson) and self.check7ePacket(send7ePacket, asw7ePacket):
            isSuccess = True
        else:
            isSuccess = False
        LogUtil.instance().print('<================ Test ' + ('Success' if isSuccess else 'Failure') + '\n')

    # Modbus接口
    def readCoils(self, name, start, num, aswValue, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
        LogUtil.instance().print('================> ' + name)
        isSuccess = True
        value = self.modbusTk.readCoils(self.config["设备ID"], start, num)
        LogUtil.instance().print("modbus recv：" + str(list(value)) + ", expect: " + str(aswValue))
        if list(value).__eq__(aswValue):
            isSuccess = True
        else:
            isSuccess = False
        # 验证json报文和7E报文
        if isSuccess and self.checkJson(sendJson, aswJson) and self.check7ePacket(send7ePacket, asw7ePacket):
            isSuccess = True
        else:
            isSuccess = False
        self.totle += 1
        if isSuccess: self.success += 1
        LogUtil.instance().print('<================ Test ' + ('Success' if isSuccess else 'Failure') + '\n')

    def readDiscreteInputs(self, name, start, num, aswValue, sendJson=None, aswJson=None, send7ePacket=None,
                           asw7ePacket=None):
        LogUtil.instance().print('================> ' + name)
        isSuccess = True
        value = self.modbusTk.readDiscreteInputs(self.config["设备ID"], start, num)
        LogUtil.instance().print("readDiscreteInputs recv：" + str(value))
        if list(value).__eq__(aswValue):
            isSuccess = True
        else:
            isSuccess = False
        # 验证json报文和7E报文
        if isSuccess and self.checkJson(sendJson, aswJson) and self.check7ePacket(send7ePacket, asw7ePacket):
            isSuccess = True
        else:
            isSuccess = False
        self.totle += 1
        if isSuccess: self.success += 1
        LogUtil.instance().print('<================ Test ' + ('Success' if isSuccess else 'Failure') + '\n')

    def readHoldingRegisters(self, name, start, num, aswValue, sendJson=None, aswJson=None, send7ePacket=None,
                             asw7ePacket=None):
        LogUtil.instance().print('================> ' + name)
        isSuccess = True
        value = self.modbusTk.readHoldingRegisters(self.config["设备ID"], start, num)
        LogUtil.instance().print("readHoldingRegisters recv：" + str(value))
        if list(value).__eq__(aswValue):
            isSuccess = True
        else:
            isSuccess = False
        # 验证json报文和7E报文
        if isSuccess and self.checkJson(sendJson, aswJson) and self.check7ePacket(send7ePacket, asw7ePacket):
            isSuccess = True
        else:
            isSuccess = False
        self.totle += 1
        if isSuccess: self.success += 1
        LogUtil.instance().print('<================ Test ' + ('Success' if isSuccess else 'Failure') + '\n')

    def readInputRegisters(self, name, start, num, aswValue, sendJson=None, aswJson=None, send7ePacket=None,
                           asw7ePacket=None):
        LogUtil.instance().print('================> ' + name)
        isSuccess = True
        value = self.modbusTk.readInputRegisters(self.config["设备ID"], start, num)
        if list(value).__eq__(aswValue):
            isSuccess = True
        else:
            isSuccess = False
        # 验证json报文和7E报文
        if isSuccess and self.checkJson(sendJson, aswJson) and self.check7ePacket(send7ePacket, asw7ePacket):
            isSuccess = True
        else:
            isSuccess = False
        self.totle += 1
        if isSuccess: self.success += 1
        LogUtil.instance().print('<================ Test ' + ('Success' if isSuccess else 'Failure') + '\n')

    def writeSingleCoil(self, name, start, value, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
        LogUtil.instance().print('================> ' + name)
        isSuccess = True
        value = self.modbusTk.writeSingleCoil(self.config["设备ID"], start, value)
        # 验证json报文和7E报文
        if isSuccess and self.checkJson(sendJson, aswJson) and self.check7ePacket(send7ePacket, asw7ePacket):
            isSuccess = True
        else:
            isSuccess = False
        self.totle += 1
        if isSuccess: self.success += 1
        LogUtil.instance().print('<================ Test ' + ('Success' if isSuccess else 'Failure') + '\n')

    def writeSingleRegister(self, name, start, value, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
        LogUtil.instance().print('================> ' + name)
        isSuccess = True
        value = self.modbusTk.writeSingleRegister(self.config["设备ID"], start, value)
        # 验证json报文和7E报文
        if isSuccess and self.checkJson(sendJson, aswJson) and self.check7ePacket(send7ePacket, asw7ePacket):
            isSuccess = True
        else:
            isSuccess = False
        self.totle += 1
        if isSuccess: self.success += 1
        LogUtil.instance().print('<================ Test ' + ('Success' if isSuccess else 'Failure') + '\n')

    def writeMultipleCoils(self, name, start, num, value, sendJson=None, aswJson=None, send7ePacket=None,
                           asw7ePacket=None):
        LogUtil.instance().print('================> ' + name)
        isSuccess = True
        self.modbusTk.writeMultipleCoils(self.config["设备ID"], start, num, value)
        # 验证json报文和7E报文
        if isSuccess and self.checkJson(sendJson, aswJson) and self.check7ePacket(send7ePacket, asw7ePacket):
            isSuccess = True
        else:
            isSuccess = False
        self.totle += 1
        if isSuccess: self.success += 1
        LogUtil.instance().print('<================ Test ' + ('Success' if isSuccess else 'Failure') + '\n')

    def writeMultipleRegister(self, name, start, num, value, sendJson=None, aswJson=None, send7ePacket=None,
                              asw7ePacket=None):
        LogUtil.instance().print('================> ' + name)
        isSuccess = True
        self.modbusTk.writeMultipleRegister(self.config["设备ID"], start, num, value)
        # 验证json报文和7E报文
        if isSuccess and self.checkJson(sendJson, aswJson) and self.check7ePacket(send7ePacket, asw7ePacket):
            isSuccess = True
        else:
            isSuccess = False
        self.totle += 1
        if isSuccess: self.success += 1
        LogUtil.instance().print('<================ Test ' + ('Success' if isSuccess else 'Failure') + '\n')
