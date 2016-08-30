# coding:utf8

import subprocess

def monitor(first_invoke=1):
    """
    查询机器运行了多久
    :param first_invoke:
    :return:
    """
    value_dic = {}
    shell_command = 'uptime'

    # 查询失败返回一个空的字符串
    result = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE).stdout.read()
    if result.__len__() < 1:
        value_dic = {
            'status': -1,
        }
    else:
        value_dic = {
            'uptime': result,
            'status': 0
        }

    return value_dic

if __name__ == "__main__":
    print(monitor())

