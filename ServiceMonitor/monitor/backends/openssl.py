# coding:utf8
import commands
import os


class Openssl(object):
    """
    openssl 解密
    """
    file_name = 'log.des'

    def __init__(self):
        pass

    def decryptData(self, data):
        """
        openssl 解密
        :param data:
        :return: 解密后的数据，报错返回 ''
        """
        print('go to decryptData')
        file_path = os.path.dirname(os.path.abspath(__file__)) + '/' + self.file_name
        self.saveTempFile(file_path, data)
        status, result = self.execute(file_path)
        return status, result

    @staticmethod
    def saveTempFile(file_path, data):
        with open(file_path, 'w') as f:
            f.truncate()
            f.write(data)

    @staticmethod
    def cleanTempFile(file_name):
        """
        clean file content
        :param file_name:
        :return:
        """
        with open(file_name, 'w') as f:
            f.truncate()

    @staticmethod
    def execute(file_path):
        shell_command = 'openssl enc -des -d -a -in %s -pass pass:itnihao' % file_path
        print(shell_command)
        status, result = commands.getstatusoutput(shell_command)
        return status, result
