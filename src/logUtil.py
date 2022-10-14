import os
import sys
import time


class LogUtil:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = LogUtil()
        return cls._instance

    def __init__(self):
        # 获取当前文件绝对路径
        self.path = os.path.abspath(os.path.dirname(sys.argv[0]))
        now = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))

        # logging会打印系统的一些日志
        # LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        #  filename = self.path + '/' + str(now) + '.txt';
        # logging.basicConfig(filename=filename, level=logging.DEBUG, format=LOG_FORMAT, encoding='utf-8')

        # sys.stdout = open(self.path + '/' + str(now) + '.txt', mode='a+', encoding='utf-8')

    def print(self, content):
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        log = now + " | " + content;
        # logging.debug(log)
        print(log)

if __name__ == '__main__':
    LogUtil.instance().print('这是日志！')
