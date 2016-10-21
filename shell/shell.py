# encoding=utf-8

import os
import sys
import shlex
import getpass
import socket
import signal
import subprocess
import platform
from func import *


built_in_cmds = {}

def regist_command(cmd, func):
	built_in_cmds[cmd] = func


def shell_loop():
	status = SHELL_STATUS_RUN
	while status == SHELL_STATUS_RUN:
		display_cmd_prompt()

		ignore_signal()

		try:
			cmd = sys.stdin.readline()

			cmd_tokens = tokenize(cmd)	# parser cmd into a token list

			cmd_tokens = preprocess(cmd_tokens)
			
			status = execute(cmd_tokens)
		except:
			_, err, _ = sys.exc_info()
			print(err)


def display_cmd_prompt():

	user = getpass.getuser()	# get user of current system

	hostname = socket.gethostname()	# get hostname of current system

	pwd = os.getcwd()	# current pwd

	base_dir = os.path.basename(pwd)	# get bottom dirname of pwd

	home_dir = os.path.expanduser('~')

	if pwd == home_dir:
		basedir = '~'

	# 输出命令提示符
	if platform.system() != 'Windows':
		sys.stdout.write("[\033[1;33m%s\033[0;0m@%s \033[1;36m%s\033[0;0m] $ " % (user, hostname, base_dir))
	else:
		sys.stdout.write("[%s@%s %s]$ " % (user, hostname, base_dir))
	sys.stdout.flush()


def ignore_signal():
	if platform.system() != 'Windows':
		# ignore ctrl + z
		signal.signal(signal.SIGTSTP, signal.SIG_IGN)
	signal.signal(signal.SIGINT, signal.SIG_IGN)

def tokenize(string):
	# split string by blank
	return shlex.split(string)


def preprocess(tokens):
    # 用于存储处理之后的 tokeen
    processed_token = []
    for token in tokens:
        if token.startswith('$'):
            # os.getenv() 用于获取环境变量的值，比如 'HOME'
            # 变量不存在则返回空
            processed_token.append(os.getenv(token[1:]))
        else:
            processed_token.append(token)
    return processed_token

def handler_kill(signum, frame):
    raise OSError("Killed!")

def execute(cmd_tokens):
	# 'a' 模式表示以添加的方式打开指定文件
	# 这个模式下文件对象的 write 操作不会覆盖文件原有的信息，而是添加到文件原有信息之后
	
	history_file = open(HISTORY_PATH, 'a')
	
	history_file.write(' '.join(cmd_tokens) + os.linesep)

	if cmd_tokens:
		# 获取命令
		cmd_name = cmd_tokens[0]
		# 获取命令参数
		cmd_args = cmd_tokens[1:]

		# 如果当前命令在命令表中
		# 则传入参数，调用相应的函数进行执行
		if cmd_name in built_in_cmds:
			return built_in_cmds[cmd_name](cmd_args)

		# 监听 Ctrl-C 信号
		signal.signal(signal.SIGINT, handler_kill)

		if platform.system() != "Windows":
        	# call subprocess to execute cmd
			p = subprocess.Popen(cmd_tokens)
			# parent porcess read data from subprocess, until read EOF

			p.communicate()
		else:
			# windows platform
			command = ""
			command = ' '.join(cmd_tokens)
			os.system(command)
	return SHELL_STATUS_RUN

def init():
	regist_command('cd', cd)
	regist_command('exit', exit)
	regist_command('getenv', getenv)
	regist_command('history', history)

def main():
	init()
	shell_loop()

if __name__ == '__main__':
	main()	



