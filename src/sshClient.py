import paramiko

from src.logUtil import LogUtil


class SshClient:
    def __init__(self):
        LogUtil.instance().print("SshClient __init__")
        self.connection = None

    def connect(self, ip, port, username, password):
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if password != '':
                self.connection.connect(ip, port, username, (str(password)), timeout=5.0)
                LogUtil.instance().print("SshClient connect success")
                return True
            else:
                try:
                    self.connection.connect(ip, port, username, look_for_keys=False,
                                            allow_agent=False, timeout=5.0)
                    LogUtil.instance().print("SshClient connect success")
                except paramiko.ssh_exception.SSHException as e:
                    try:
                        LogUtil.instance().print("SshClient connect exception: " + str(e.args))
                        return False
                        # self.connection.get_transport().auth_none(username)
                        # self.connection.exec_command('uname -a')
                    finally:
                        e = None
                        del e
                self.connection.sftp = paramiko.SFTPClient.from_transport(self.connection.get_transport())
                return True
        except Exception as e:
            try:
                LogUtil.instance().print("SshClient connect exception: " + str(e.args))
                self.connection = None
                return False
            finally:
                e = None
                del e

    def getGatewayLog(self, path):
        stdin, stdout, stderr = self.connection.exec_command('tail -n 50 ' + path)  # 查看最新的20行日志
        # stdin为输入的命令 stdout为命令返回的结果 stderr为命令错误时返回的结果
        log = stdout.read().decode().replace(" ", "").replace("\n", "")
        return log

    def close(self):
        self.connection = None
        LogUtil.instance().print("SshClient 已关闭")


if __name__ == '__main__':
    test = SshClient()
    test.connect('192.168.37.143', 22, 'root', 'ihome_309')
    # 执行命令并获取命令结果
    print(test.getGatewayLog("/home/rolling.log"))
    test.close()
