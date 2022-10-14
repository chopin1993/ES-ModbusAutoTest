# encoding:utf-8
from src.engine import TestEngine


def start(config):
    """
    开始测试
    :param config:字典，配置信息
    """
    return TestEngine.instance().start(config)


def close():
    """
    关闭测试
    """
    TestEngine.instance().close()


# 通用TCP接口
def tcpCommunication(msg, aswMsg, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
    """
    通用TCP通信测试
    :param msg: modbus报文
    :param aswMsg: modbus应答报文
    :param json: 发送的json报文
    :param aswJson: json应答报文
    :param packet: 发送的7E报文
    :param aswPacket: 7E应答报文
    """
    TestEngine.instance().tcpCommunication(msg, aswMsg, sendJson, aswJson, send7ePacket, asw7ePacket)


# Modbus接口
def readCoils(name, start, num, aswValue, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
    """
    01 读线圈
    :param name: 测试内容
    :param start: 起始寄存器地址
    :param num: 寄存器个数
    :param aswValue: 寄存器的值
    :param sendJson: 发送的Json报文
    :param aswJson: json应答报文
    :param send7ePacket: 发送的7E报文
    :param asw7ePacket: 7E应答报文
    """
    TestEngine.instance().readCoils(name, start, num, aswValue, sendJson, aswJson, send7ePacket, asw7ePacket)


def readDiscreteInputs(name, start, num, aswValue, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
    """
    02 读离散输入
    :param name: 测试内容
    :param start: 起始寄存器地址
    :param num: 寄存器个数
    :param aswValue: 寄存器的值
    :param sendJson: 发送的Json报文
    :param aswJson: json应答报文
    :param send7ePacket: 发送的7E报文
    :param asw7ePacket: 7E应答报文
    """
    TestEngine.instance().readDiscreteInputs(name, start, num, aswValue, sendJson, aswJson, send7ePacket, asw7ePacket)


def readHoldingRegisters(name, start, num, aswValue, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
    """
    03 读保持寄存器
    :param name: 测试内容
    :param start: 起始寄存器地址
    :param num: 寄存器个数
    :param aswValue: 寄存器的值
    :param sendJson: 发送的Json报文
    :param aswJson: json应答报文
    :param send7ePacket: 发送的7E报文
    :param asw7ePacket: 7E应答报文
    """
    TestEngine.instance().readHoldingRegisters(name, start, num, aswValue, sendJson, aswJson, send7ePacket, asw7ePacket)


def readInputRegisters(name, start, num, aswValue, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
    """
    04 读输入寄存器
    :param name: 测试内容
    :param start: 起始寄存器地址
    :param num: 寄存器个数
    :param aswValue: 寄存器的值
    :param sendJson: 发送的Json报文
    :param aswJson: json应答报文
    :param send7ePacket: 发送的7E报文
    :param asw7ePacket: 7E应答报文
    """
    TestEngine.instance().readInputRegisters(start, num, aswValue, sendJson, aswJson, send7ePacket, asw7ePacket)


def writeSingleCoil(name, start, value, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
    """
    05 写单线圈
    :param name: 测试内容
    :param start: 寄存器地址
    :param value: 寄存器的值
    :param sendJson: 发送的Json报文
    :param aswJson: json应答报文
    :param send7ePacket: 发送的7E报文
    :param asw7ePacket: 7E应答报文
    """
    TestEngine.instance().writeSingleCoil(name, start, value, sendJson, aswJson, send7ePacket, asw7ePacket)


def writeSingleRegister(name, start, value, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
    """
    06 写单寄存器
    :param name: 测试内容
    :param start: 寄存器地址
    :param value: 寄存器的值
    :param sendJson: 发送的Json报文
    :param aswJson: json应答报文
    :param send7ePacket: 发送的7E报文
    :param asw7ePacket: 7E应答报文
    """
    TestEngine.instance().writeSingleRegister(name, start, value, sendJson, aswJson, send7ePacket, asw7ePacket)


def writeMultipleCoils(name, start, num, value, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
    """
    0F 写多线圈
    :param name: 测试内容
    :param start: 起始寄存器地址
    :param num: 寄存器个数
    :param value: 寄存器的值
    :param sendJson: 发送的Json报文
    :param aswJson: json应答报文
    :param send7ePacket: 发送的7E报文
    :param asw7ePacket: 7E应答报文
    """
    TestEngine.instance().writeMultipleCoils(name, start, num, value, sendJson, aswJson, send7ePacket, asw7ePacket)


# 10 写多线寄存器
def writeMultipleRegister(name, start, num, value, sendJson=None, aswJson=None, send7ePacket=None, asw7ePacket=None):
    """
    0F 写多线圈
    :param name: 测试内容
    :param start: 起始寄存器地址
    :param num: 寄存器个数
    :param value: 寄存器的值
    :param sendJson: 发送的Json报文
    :param aswJson: json应答报文
    :param send7ePacket: 发送的7E报文
    :param asw7ePacket: 7E应答报文
    """
    TestEngine.instance().writeMultipleRegister(name, start, num, value, sendJson, aswJson, send7ePacket, asw7ePacket)
