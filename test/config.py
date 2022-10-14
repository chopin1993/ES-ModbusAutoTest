class Config(object):
    def __init__(self):
        self.config = dict()
        # 配置网关
        self.config["网关ip"] = r"192.168.1.103"
        self.config["网关类型"] = True # True 单相网关， False 三相网关
        self.config["日志路径(单相网关)"] = r"/tmp/rolling.log"
        self.config["日志路径(三相网关)"] = r"/home/rolling.log"

        # 配置Modbus
        self.config["Modbus地址"] = self.config["网关ip"]
        self.config["Modbus端口"] = 502

        # 配置ssh
        self.config["ssh地址"] = self.config["网关ip"]
        self.config["ssh端口"] = 22
        self.config["ssh用户名"] = "root"
        self.config["ssh密码(单相网关)"] = "eastsoft"
        self.config["ssh密码(三相网关)"] = "ihome_309"

        # 配置串口
        self.config["串口号"] = "COM1"
        self.config["波特率"] = 115200

        # 其他
        self.config["验证Json报文"] = True
        self.config["验证7E报文"] = True
        self.config["通过网关日志验证7E报文"] = True # True通过网关日志验证， False通过电力线监控器验证


