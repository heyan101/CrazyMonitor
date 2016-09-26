# coding:utf8
import commands

from docx import Document


class DocUtils(object):
    """
    DOC 数据解析
    """
    def __init__(self):
        pass

    def parseDataProduceDoc(self, data=None):
        """
        解析数据，并生成 DOC 格式的文件
        :param data:
        :return:
        """
        if data is None:
            return None

        data = self.execute()


        return True

    def saveTempFile(self, data):
        with open('log.des', 'w') as f:
            f.write(data)

    def execute(self):
        shell_command = 'openssl enc -des -d -a -in log.des -pass pass:itnihao'
        status, result = commands.getstatusoutput(shell_command)
        return status, result

