# coding:utf8
import client


class command_handler(object):
    """
    开始启动客户端
    """
    def __init__(self, sys_args):
        self.sys_args = sys_args
        if len(self.sys_args) < 2:
            self.help_msg()

        self.command_allowcator()

    def command_allowcator(self):
        '''分拣用户输入的不同指令'''

        # 这里利用反射获取要指定的函数
        if hasattr(self, self.sys_args[1]):
            func = getattr(self, self.sys_args[1])
            return func()
        else:
            print('command does not exist!')

    def start(self):
        print('going to start the monitor client...')

        Client = client.ClientHandle()
        Client.forever_run()

    # 目前没有用到这个功能
    # def stop(self):
    #     print('stopping the monitor client')

    @staticmethod
    def help_msg():
        valid_commands = '''
        start       start monitor client
        stop        stop monitor client
        '''
        exit(valid_commands)

