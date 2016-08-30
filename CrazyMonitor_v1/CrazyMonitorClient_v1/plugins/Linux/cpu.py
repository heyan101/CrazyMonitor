# coding:utf8

# yum -y install sysstat

import commands
import subprocess


def monitor(frist_invoke=1):
    """
    获取 CPU 信息
    # yum -y install sysstat | apt-get install sysstat
    :param frist_invoke:
    :return:
    """
    shell_command_en = 'sar 1 3 | grep "^Average"'
    shell_command_zh = 'sar 1 3 | grep "^平均时间"'
    value_dic = {}

    status, result = commands.getstatusoutput(shell_command_en)
    if status != 0:  # 命令执行错误
        status, result = commands.getstatusoutput(shell_command_zh)

    if status != 0:
        value_dic = {'status': status}
    else:
        user, nice, system, iowait, steal, idle = result.split()[2:]
        value_dic = {
            'user': user,
            'nice': nice,
            'system': system,
            'iowait': iowait,
            'steal': steal,
            'idle': idle,
            'status': status,
        }
    return value_dic

if __name__ == "__main__":
    print(monitor())

