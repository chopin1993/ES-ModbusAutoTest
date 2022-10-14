# ModbusTcp协议客户端模块

import random
import socket
import struct
import time

from src.logUtil import LogUtil


class ModbusClient:

    def __init__(self):
        LogUtil.instance().print("ModbusClient __init__")

    def connect(self, ip, port):
        try:
            self.mysocket = socket.socket()
            self.mysocket.settimeout(1)
            ret = self.mysocket.connect((ip, port))
            if ret == socket.error:
                LogUtil.instance().print("ModbusClient connect failed")
                return False
            else:
                LogUtil.instance().print("ModbusClient connect success")
                return True
        except Exception as e:
            LogUtil.instance().print("ModbusClient connect exception: " + str(e.args))
            return False

    def closeClient(self):
        self.mysocket.close()
        LogUtil.instance().print("ModbusClient 已关闭")

    # Modbus-RTU协议的03或04读取保存或输入寄存器功能主-》从命令帧
    def modbus03or04s(self, add, startregadd, regnum, funcode=3):
        if add < 0 or add > 0xFF or startregadd < 0 or startregadd > 0xFFFF or regnum < 1 or regnum > 0x7D:
            print("Error: parameter error")
            return
        if funcode != 3 and funcode != 4:
            print("Error: parameter error")
            return
        # MBAP的实现
        ranvalue = random.randint(0, 0xFFFF)
        sendbytes = ranvalue.to_bytes(2, byteorder="big", signed=False)
        sendbytes = sendbytes + b"\x00\x00\x00\x06"
        sendbytes = sendbytes + add.to_bytes(1, byteorder="big", signed=False)
        # PDU实现
        sendbytes = sendbytes + funcode.to_bytes(1, byteorder="big", signed=False) + startregadd.to_bytes(2,
                                                                                                          byteorder="big",
                                                                                                          signed=False) + \
                    regnum.to_bytes(2, byteorder="big", signed=False)
        # for b in list(sendbytes):
        #     print(f"{b:02x}")
        return sendbytes

    # Modbus协议的03或04读取保持或输入寄存器功能从-》主的数据帧解析（浮点数2,1,4,3格式，16位短整形（定义正负数））
    def modbus03or04p(self, recvdata, valueformat=1, intsigned=False):
        if not recvdata:
            print("Error: data error")
            return
        datalist = list(recvdata)
        if datalist[7] != 0x3 and datalist[7] != 0x4:
            print("Error: recv data funcode error")
            return
        bytenums = datalist[8]
        if bytenums % 2 != 0:
            print("Error: recv data reg data error")
            return
        retdata = []
        if valueformat == 0:
            floatnums = bytenums / 4
            # print("float nums: ", str(floatnums))
            floatlist = [0, 0, 0, 0]
            for i in range(int(floatnums)):
                floatlist[1] = datalist[9 + i * 4]
                floatlist[0] = datalist[10 + i * 4]
                floatlist[3] = datalist[11 + i * 4]
                floatlist[2] = datalist[12 + i * 4]
                bfloatdata = bytes(floatlist)
                [fvalue] = struct.unpack('f', bfloatdata)
                retdata.append(fvalue)
                # print(f'Data{i+1}: {fvalue:.3f}')
        elif valueformat == 1:
            shortintnums = bytenums / 2
            # print("short int nums: ", str(shortintnums))
            for i in range(int(shortintnums)):
                btemp = recvdata[9 + i * 2:11 + i * 2]
                print("btemp: " + str(btemp))
                shortvalue = int.from_bytes(btemp, byteorder="big", signed=intsigned)
                retdata.append(shortvalue)
                # print(f"Data{i+1}: {shortvalue}")
        return retdata

    # modbus的01或02功能号命令打包函数
    def modbus01or02s(self, add, startregadd, regnum, funcode=2):
        if add < 0 or add > 0xFF or startregadd < 0 or startregadd > 0xFFFF or regnum < 1 or regnum > 0x7D0:
            print("Error: parameter error")
            return
        if funcode != 1 and funcode != 2:
            print("Error: parameter error")
            return
        # MBAP实现
        ranvalue = random.randint(0, 0xFFFF)
        sendbytes = ranvalue.to_bytes(2, byteorder="big", signed=False)
        sendbytes = sendbytes + b"\x00\x00\x00\x06"
        sendbytes = sendbytes + add.to_bytes(1, byteorder="big", signed=False)
        # PDU实现
        sendbytes = sendbytes + funcode.to_bytes(1, byteorder="big", signed=False) + startregadd.to_bytes(2,
                                                                                                          byteorder="big",
                                                                                                          signed=False) + \
                    regnum.to_bytes(2, byteorder="big", signed=False)
        # for b in list(sendbytes):
        #     print(f"{b:02x}")
        return sendbytes

    # modbus的01或02功能号的返回包解析函数
    def modbus01or02p(self, recvdata):
        if not recvdata:
            print("Error: data error")
            return
        datalist = list(recvdata)
        if datalist[7] != 0x1 and datalist[7] != 0x2:
            print("Error: recv data funcode error")
            return
        bytenums = datalist[8]
        ret_data = []
        for i in range(bytenums):
            intvalue = int(recvdata[9 + i])
            for bit in range(8):
                nowvalue = intvalue & 0x01
                intvalue = intvalue >> 1
                ret_data.append(nowvalue)
        return ret_data

    # 读取仪表数据并解析返回
    def readmeterdata(self, meter_add, start_reg, reg_num):
        try:
            send_data = self.modbus03or04s(meter_add, start_reg, reg_num)
            print("send: " + str(send_data))
            if not send_data:
                print("读取命令处理错误！")
                return
            starttime = time.time()
            self.mysocket.send(send_data)
            recv_data = self.mysocket.recv(1024)  # (reg_num*2+9)
            print("recv: " + str(recv_data))
            if recv_data and len(recv_data) > 0:
                retdata = self.modbus03or04p(recv_data)
                print("retdata: " + str(retdata))
                if retdata:
                    return retdata
                else:
                    return
            else:
                return
        except Exception as e:
            print(f"Exception : {e}")
            endtime = time.time()
            print(f"读取超时时间: {endtime - starttime:.3f}")
            return

    # 读取仪表数据并解析返回
    def readmeterdata2(self, meter_add, start_reg, reg_num):
        try:
            send_data = self.modbus01or02s(meter_add, start_reg, reg_num)
            if not send_data:
                print("读取命令处理错误！")
                return
            starttime = time.time()
            self.mysocket.send(send_data)
            recv_data = self.mysocket.recv(1024)  # (reg_num*2+9)
            endtime = time.time()
            # print(f"Used time is {endtime-starttime:.3f}")
            if recv_data and len(recv_data) > 0:
                retdata = self.modbus01or02p(recv_data)
                if retdata:
                    return retdata
                else:
                    return
            else:
                return
        except Exception as e:
            print(f"Exception : {e}")
            endtime = time.time()
            print(f"读取超时时间: {endtime - starttime:.3f}")
            return


if __name__ == "__main__":

    funcode = 3
    slaveadd = 1
    startreg = 0
    regnums = 10
    regStartName = 40001
    print("Modbus/Tcp Start!")

    c = ModbusClient()
    conn = c.connect("192.168.1.100", 502)
    if not conn:
        print("Connect ModbusTcp Server Fail!")
    else:
        # 读取寄存器数据值，用rich模块的表格实时显示数据，没有数据则模拟随机数据
        if funcode == 3 or funcode == 4:
            now_data = c.readmeterdata(slaveadd, startreg, regnums)
            print("now_data: " + str(now_data))
        if funcode == 1 or funcode == 2:
            now_data = c.readmeterdata2(slaveadd, startreg, regnums)
            print("now_data: " + str(now_data))
        c.closeClient()
