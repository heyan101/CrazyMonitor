# coding:utf8

import os
import sys
# 这里将当前 Client添加到 PATH 中
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import main

# 程序入口
if __name__ == "__main__":
    client = main.command_handler(sys.argv)
