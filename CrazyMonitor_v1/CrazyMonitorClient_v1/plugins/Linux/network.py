# coding:utf8

import subprocess

def monitor(first_invoke=1):
    """
    网卡信息，返回lo 和 ech0 两个网卡的输入输出百分比
    :param first_invoke:
    :return:
    """
    shell_command = 'sar -n DEV 1 5 |grep -v IFACE |grep Average'
    shell_command2 = 'sar -n DEV 1 5 |grep -v IFACE |grep 平均时间'
    value_dic = {}

    result = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE).stdout.readlines()
    if result.__len__() < 1:
        result = subprocess.Popen(shell_command2, shell=True, stdout=subprocess.PIPE).stdout.readlines()
        if result.__len__() < 1:
            value_dic = {'status': -1, 'data': {}}

    value_dic = {'status': 0, 'data': {}}
    for line in result:
        line = line.split()
        nic_name, t_in, t_out = line[1], line[4], line[5]
        value_dic['data'][nic_name] = {'t_in': t_in, 't_out': t_out}

    return value_dic

if __name__ == "__main__":
    print(monitor())