import modbus_tk.defines as md
import modbus_tk.modbus_tcp as mt
from cffi.backend_ctypes import xrange

from src.logUtil import LogUtil

# self.master.execute(35, md.READ_COILS, 0, 10))
# self.master.execute(35, md.READ_DISCRETE_INPUTS, 0, 8))
# self.master.execute(35, md.READ_INPUT_REGISTERS, 100, 3))
# self.master.execute(35, md.READ_HOLDING_REGISTERS, 100, 12))
# self.master.execute(35, md.WRITE_SINGLE_COIL, 7, output_value=1))
# self.master.execute(35, md.WRITE_SINGLE_REGISTER, 100, output_value=54))
# self.master.execute(35, md.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
# self.master.execute(35, md.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))

class ModbusTK:

    def __init__(self):
        LogUtil.instance().print("ModbusTK __init__")

    def connect(self, ip, port):
        try:
            # 远程连接到服务器端
            self.master = mt.TcpMaster(ip, port)
            self.master.set_timeout(3.0)
            LogUtil.instance().print("ModbusTK connect success")
            return True
        except Exception as e:
            LogUtil.instance().print("ModbusTK connect exception: " + str(e.args))
            return False

    def close(self):
        self.master.close()
        LogUtil.instance().print("ModbusTK 已关闭")

    # @slave=1 : identifier of the slave. from 1 to 247.  0为广播所有的slave
    # @function_code=READ_HOLDING_REGISTERS：功能码
    # @starting_address=1：开始地址
    # @quantity_of_x=3：寄存器/线圈的数量
    # @output_value：一个整数或可迭代的值：1/[1,1,1,0,0,1]/xrange(12)
    # @data_format
    # @expected_length

    # 01 读线圈
    def readCoils(self, slave, start, num):
        return self.master.execute(slave=slave, function_code=md.READ_COILS, starting_address=start, quantity_of_x=num)

    # 02 读离散输入
    def readDiscreteInputs(self, slave, start, num):
        return self.master.execute(slave=slave, function_code=md.READ_DISCRETE_INPUTS, starting_address=start,
                                   quantity_of_x=num)

    # 03 读保持寄存器
    def readHoldingRegisters(self, slave, start, num):
        return self.master.execute(slave=slave, function_code=md.READ_HOLDING_REGISTERS, starting_address=start,
                                   quantity_of_x=num)

    # 04 读输入寄存器
    def readInputRegisters(self, slave, start, num):
        return self.master.execute(slave=slave, function_code=md.READ_INPUT_REGISTERS, starting_address=start,
                                   quantity_of_x=num)

    # 05 写单线圈
    def writeSingleCoil(self, slave, start, value):
        return self.master.execute(slave=slave, function_code=md.WRITE_SINGLE_COIL, starting_address=start,
                                   quantity_of_x=1, output_value=value)

    # 06 写单寄存器
    def writeSingleRegister(self, slave, start, value):
        return self.master.execute(slave=slave, function_code=md.WRITE_SINGLE_REGISTER, starting_address=start,
                                   quantity_of_x=1, output_value=value)

    # 0F 写多线圈
    def writeMultipleCoils(self, slave, start, num, value):
        return self.master.execute(slave=slave, function_code=md.WRITE_MULTIPLE_COILS, starting_address=start,
                                   quantity_of_x=num, output_value=value)

    # 10 写多线寄存器
    def writeMultipleRegister(self, slave, start, num, value):
        return self.master.execute(slave=slave, function_code=md.WRITE_MULTIPLE_REGISTERS, starting_address=start,
                                   quantity_of_x=num, output_value=value)


if __name__ == '__main__':
    tk = ModbusTK()
    tk.connect('192.168.1.103', 502)
    addr = 16
    print(tk.readCoils(addr, 1, 1))
    print(tk.writeSingleCoil(addr, 1, 1))
    print(tk.readCoils(addr, 1, 4))
    print(tk.writeMultipleCoils(addr, 1, 4, [1,1,1,1]))
    print(tk.readCoils(addr, 1, 4))
    tk.close()