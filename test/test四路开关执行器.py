from src.interface import *
from test.config import Config


class TestAct(Config):
    def __init__(self):
        super(TestAct, self).__init__()
        self.config["设备名称"] = '4路开关执行器';
        self.config["设备ID"] = 16;


# 寄存器地址 对应功能
# coil:
# 1 第 1 路通道开关
# 2 第 2 路通道开关
# 3 第 3 路通道开关
# 4 第 4 路通道开关

if __name__ == '__main__':

    # 配置
    test = TestAct()
    conn = start(test.config)

    if conn:
        # 开始测试
        writeMultipleCoils("关闭四个通道", 1, 4, [0, 0, 0, 0], r'"function":{"channel_collection":[{"channel":1,"switch":false},{"channel":2,"switch":false},{"channel":3,"switch":false},{"channel":4,"switch":false}]}', r'"errorCode":0,"function":{"channel_collection":[{"channel":1,"switch":false},{"channel":2,"switch":false},{"channel":3,"switch":false},{"channel":4,"switch":false}]', '*7E*050712C0010F*', '*7E*050712C00100*')
        readCoils("读取第一通道(缓存)", 1, 1, [0])
        readCoils("读取第一通道(直读)", 1000+1, 1, [0], r'"function":{"channel_collection":[{"channel":1,"switch":true}]}', r'"errorCode":0,"function":{"channel_collection":[{"channel":1,"switch":false},{"channel":2,"switch":false},{"channel":3,"switch":false},{"channel":4,"switch":false}]', '*7E*040212C000*', '*7E*050212C00100*')
        writeSingleCoil("打开第一通道", 1, 1, r'"function":{"channel_collection":[{"channel":1,"switch":true}]}', r'"errorCode":0,"function":{"channel_collection":[{"channel":1,"switch":true},{"channel":2,"switch":false},{"channel":3,"switch":false},{"channel":4,"switch":false}]', '*7E*050712C00181*', '*7E*050712C00101*')
        readCoils("读取第一通道(直读)", 1000+1, 1, [1], r'"function":{"channel_collection":[{"channel":1,"switch":true}]}', r'"errorCode":0,"function":{"channel_collection":[{"channel":1,"switch":true},{"channel":2,"switch":false},{"channel":3,"switch":false},{"channel":4,"switch":false}]', '*7E*040212C000*', '*7E*050212C00101*')
        readCoils("读取四个通道(缓存)", 1, 4, [1,0,0,0])
        writeMultipleCoils("打开四个通道", 1, 4, [1, 1, 1, 1], r'"function":{"channel_collection":[{"channel":1,"switch":true},{"channel":2,"switch":true},{"channel":3,"switch":true},{"channel":4,"switch":true}]}', r'"errorCode":0,"function":{"channel_collection":[{"channel":1,"switch":true},{"channel":2,"switch":true},{"channel":3,"switch":true},{"channel":4,"switch":true}]', '*7E*050712C0018F*', '*7E*050712C0010F*')
        readCoils("读取四个通道(直读)", 1000+1, 4, [1, 1, 1, 1], r'"function":{"channel_collection":[{"channel":1,"switch":true},{"channel":2,"switch":true},{"channel":3,"switch":true},{"channel":4,"switch":true}]}', r'"errorCode":0,"function":{"channel_collection":[{"channel":1,"switch":true},{"channel":2,"switch":true},{"channel":3,"switch":true},{"channel":4,"switch":true}]', '*7E*040212C000*', '*7E*050212C0010F*')
        writeMultipleCoils("关闭四个通道", 1, 4, [0, 0, 0, 0], r'"function":{"channel_collection":[{"channel":1,"switch":false},{"channel":2,"switch":false},{"channel":3,"switch":false},{"channel":4,"switch":false}]}', r'"errorCode":0,"function":{"channel_collection":[{"channel":1,"switch":false},{"channel":2,"switch":false},{"channel":3,"switch":false},{"channel":4,"switch":false}]', '*7E*050712C0010F*', '*7E*050712C00100*')

    # 结束
    close()
