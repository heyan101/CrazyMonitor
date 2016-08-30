# coding:utf8

import subprocess

def monitor(first_invoke=1):
    """
    查询机器运行了多久
    :param first_invoke:
    :return:
        # uptime
        17:06:46 up  3:29,  2 users,  load average: 0.00, 0.00, 0.00
        @'17:06:46'     ：当前系统时间
        @'up  3:29,'    ：系统已运行的时间，这里是3小时29分钟
        @'2 users,'     ：当前连接的用户数
        @'load average: 0.00, 0.00, 0.00'：平均负载量，我们这里把平均负载量放在一个另外的插件中获取
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

"""

"""
