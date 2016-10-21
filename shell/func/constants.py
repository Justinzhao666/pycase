# encoding=utf-8
import os

SHELL_STATUS_STOP = 0
SHELL_STATUS_RUN = 1
CONFIG_PATH = '.config/pycases/'
# 使用 os.path.expanduser('~') 获取当前操作系统平台的当前用户根目录
HISTORY_PATH = os.path.expanduser('~') + os.sep +CONFIG_PATH +  '.py_shell_history'
