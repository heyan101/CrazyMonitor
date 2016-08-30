# coding:utf8

"""
插件对外的同一名称
"""

from linux import sysinfo, cpu, memory, network, host_alive



def LinuxSysInfo():
    """
    系统信息收集
    :return:
        {
            'wake_up_type': 'Power Switch',
            'uuid': '564D8023-B2CD-9078-98AB-CE8088FA564D',
            'os_release': 'CentOS release 6.5 (Final)',
            'os_type': 'linux',
            'cpu_count': '1',
            'ram': [{
                'slot': 'RAM slot #0',
                'capacity': '2048',
                'manufactory': 'Not Specified',
                'asset_tag': 'Not Specified',
                'sn': 'Not Specified',
                'model': 'DRAM'
            }],
            'cpu_model': 'Intel(R) Core(TM) i3-4170 CPU @ 3.70GHz',
            'manufactory': 'VMware, Inc.',
            'physical_disk_driver': [],
            'sn': 'VMware-56 4d 80 23 b2 cd 90 78-98 ab ce 80 88 fa 56 4d',
            'cpu_core_count': '',
            'nic': [{
                'macaddress': '00:0C:29:FA:56:4D',
                'name': 'eth0',
                'netmask': '255.255.255.0',
                'bonding': 0,
                'model': 'unknown',
                'ipaddress': '192.168.1.120',
                'network': '192.168.1.255'
            }],
            'model': 'VMware Virtual Platform',
            'os_distribution': 'CentOS',
            'asset_type': 'server',
            'ram_size': 1862
        }
    """
    return sysinfo.monitor()


# def WindowsSysInfo():
#     from windows import sysinfo as win_sysinfo
#     return win_sysinfo.collect()

def get_linux_cpu():
    """
    获取 CPU 信息
    # yum -y install sysstat | apt-get install sysstat
    :return:
        {'status': 0, 'iowait': '0.00', 'system': '1.74', 'idle': '98.26',
        'user': '0.00', 'steal': '0.00', 'nice': '0.00'}
    """
    return cpu.monitor()

def host_alive_check():
    """
    查询机器运行了多久
    :return:
        # uptime
        17:06:46 up  3:29,  2 users,  load average: 0.00, 0.00, 0.00
        @'17:06:46'     ：当前系统时间
        @'up  3:29,'    ：系统已运行的时间，这里是3小时29分钟
        @'2 users,'     ：当前连接的用户数
        @'load average: 0.00, 0.00, 0.00'：平均负载量，我们这里把平均负载量放在一个另外的插件中获取
    """
    return host_alive.monitor()

# def GetMacCPU():
#     #return cpu.monitor()
#     return cpu_mac.monitor()

def get_network_info():
    """
    网卡信息，返回lo 和 ech0 两个网卡的输入输出百分比
    :param first_invoke:
    :return:
        {'status': 0, 'data':
            {'lo':  {'t_in': '0.00', 't_out': '0.00'},
            'eth0': {'t_in': '0.21', 't_out': '0.00'}
            }
        }
    """
    return network.monitor()

def get_memory_info():
    """
    内存
    :param first_invoke:
    :return:
        {'status': 0, 'MemTotal': '1907580', 'MemUsage': 413724, 'Cached': '533408', 'MemUsage_p': '21',
        'SwapFree': '4194296', 'SwapUsage': 0, 'SwapTotal': '4194296', 'MemFree': '920192',
        'SwapUsage_p': '0', 'Buffers': '40256'}
    """
    return memory.monitor()
