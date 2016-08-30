# coding:utf8

import commands


def monitor(first_invoke=1):
    """
    内存
    :param first_invoke:
    :return:
    """
    monitor_dic = {
        'SwapUsage': 'percentage',
        'MemUsage': 'percentage',
    }
    shell_command = "grep 'MemTotal\|MemFree\|Buffers\|^Cached\|SwapTotal\|SwapFree' /proc/meminfo"
    status, result = commands.getstatusoutput(shell_command)
    if status != 0:  # cmd exec error
        value_dic = {'status': status}
    else:
        value_dic = {'status': status}
        for i in result.split('kB\n'):
            key = i.split()[0].strip(':')  # factor name
            value = i.split()[1]  # factor value
            value_dic[key] = value

        if monitor_dic['SwapUsage'] == 'percentage':
            value_dic['SwapUsage_p'] = str(100 - int(value_dic['SwapFree']) * 100 / int(value_dic['SwapTotal']))
        # real SwapUsage value
        value_dic['SwapUsage'] = int(value_dic['SwapTotal']) - int(value_dic['SwapFree'])

        MemUsage = int(value_dic['MemTotal']) - (int(value_dic['MemFree']) + int(value_dic['Buffers'])
                                                 + int(value_dic['Cached']))
        if monitor_dic['MemUsage'] == 'percentage':
            value_dic['MemUsage_p'] = str(int(MemUsage) * 100 / int(value_dic['MemTotal']))
        # real MemUsage value
        value_dic['MemUsage'] = MemUsage

    return value_dic

if __name__ == "__main__":
    print(monitor())

"""
    # grep 'MemTotal\|MemFree\|Buffers\|^Cached\|SwapTotal\|SwapFree' /proc/meminfo
    @memtotal       ：总的物理内存， total = free + used
    @memfree        ：剩余使用量
    @buffers        ：缓存区，主要用于目录方面,inode值等（ls大目录可看到这个值增加）
    @cached         ：缓存区，用于已打开的文件
    @swaptotal      ：交换页总的大小
    @swapfree       ：交换页剩余大小
    @used           ：用户已使用量,  used = buffers + cached
    @free           ：完全未被使用的内存
"""