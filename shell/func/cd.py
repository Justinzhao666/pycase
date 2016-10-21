# encoding=utf-8
from .constants import *
import os
def cd(args):
	if len(args)>0:
		os.chdir(args[0])
	else:
		os.chdir(os.getenv('HOME'))

	return SHELL_STATUS_RUN
