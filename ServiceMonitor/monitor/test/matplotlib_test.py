# coding:utf8
import json

import matplotlib.pyplot as plt
from numpy import arange


class MatplotlibUtils(object):
    """
    matplotlib 是画图工具库，依赖于 numpy
    """
    def __init__(self):
        self.data = """
        {"swap_used": "0B", "swap_free": "2.0G", "mem_buffers": "106.7M","mem_used": "1.2G", "mem_total": "1.8G",
         "mem_used_rate": "65.17", "mem_free_rate": "34.83", "mem_cached":"505.7M", "swap_total": "2.0G",
         "mem_free": "652.6M", "swap_used_rate": "0.00", "swap_free_rate": "100.00"}
        """

    def parse(self):
        data = json.loads(self.data)
        left = []
        height = []
        lable = []
        i = 0
        for index in data:
            left.append(i)
            lable.append(index)
            i += 1
            if data[index][-1].lower() == 'g':
                height.append(float(('%0.2f' % (float(data[index][0:-1]) * 1024))))
            elif data[index][-1].lower() == 'm':
                height.append(float(('%0.2f' % (float(data[index][0:-1])))))
            elif data[index][-1].lower() == 'b':
                height.append(float(('%0.2f' % (float(data[index][0:-1]) / 1024))))
            else:
                height.append(float(('%0.2f' % (float(data[index])))))
        print('left====', left)
        print('height==', height)

        font = {'family': 'serif',
                'color': 'darkred',
                'weight': 'normal',
                'size': 10,
                }

        plt.bar(left, height, width=0.5)
        plt.xlabel('(index)')
        plt.ylabel('(MB)')
        plt.xticks(arange(len(lable)), lable)
        fig = plt.gcf()
        fig.set_size_inches(20.0, 10.5)

        ax = fig.gca()
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(10)

        fig.savefig('mem.png', dpi=100)


if __name__ == "__main__":
    plts = MatplotlibUtils()
    plts.parse()