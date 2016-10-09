# coding:utf8
import json

import matplotlib.pyplot as plt
from numpy import arange


class MatplotlibUtils(object):
    """
    matplotlib 是画图工具库，依赖于 numpy
    """
    def __init__(self):
        pass

    @staticmethod
    def parse(data, fname='temp.png'):
        print(type(data))
        left = []
        height = []
        lable = []
        i = 0
        for (key, value) in data.items():
            left.append(i)
            lable.append(key)
            i += 1
            if value[-1].lower() == 'g':
                height.append(float(('%0.2f' % (float(value[0:-1]) * 1024))))
            elif value[-1].lower() == 'm':
                height.append(float(('%0.2f' % (float(value[0:-1])))))
            elif value[-1].lower() == 'b':
                height.append(float(('%0.2f' % (float(value[0:-1]) / 1024))))
            else:
                height.append(float(('%0.2f' % (float(value)))))

        plt.bar(left, height, width=0.5)
        plt.xlabel('(index)')
        plt.ylabel('(MB)')
        plt.xticks(arange(len(lable)), lable)
        fig = plt.gcf()
        fig.set_size_inches(20.0, 10.5)

        ax = fig.gca()
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(10)

        fig.savefig(fname, dpi=100)


if __name__ == "__main__":
    plts = MatplotlibUtils()
    plts.parse()
