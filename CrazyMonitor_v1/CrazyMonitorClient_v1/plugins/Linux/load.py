# coding:utf8

import commands

def monitor():
    """
    平均负载量
    load average: 0.00, 0.00, 0.00
    分别表示 1分钟，5分钟，15分钟的负载量，这里显示的是百分比，值越低说明系统性能越好
    :return: {'load1': ' 0.00', 'load15': ' 0.00', 'status': 0, 'load5': ' 0.00'}
    """
    shell_command = 'uptime'
    value_dic = {}

    status, result = commands.getstatusoutput(shell_command)
    if status != 0:  # cmd exec error
        value_dic = {'status': status}
    else:
        #uptime = result.split(',')[:1][0]
        load1, load5, load15 = result.split('load average:')[1].split(',')
        value_dic = {
            # 'uptime': uptime,
            'load1': load1,
            'load5': load5,
            'load15': load15,
            'status': status
        }
    return value_dic

if __name__ == "__main__":
    print(monitor())