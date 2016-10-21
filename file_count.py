#! /usr/bin/python
# encoding=utf-8

import os
import optparse
import time

file_list = []
type_list = []
def get_file(path):

	if os.path.isdir(path):	
		for parent, dirNames, fileNames in os.walk(path,topdown=True):
			for fileName in fileNames:
				sufix = fileName.split('.')[-1]
				if sufix in type_list:
					file_list.append(os.path.join(parent, fileName))
	elif os.path.isfile(path):
		file_list.append(path)



def count_line(file):
	count = 0
	for file_line in open(file).xreadlines():
		if file_line != '' and file_line != '\n':
			count += 1

	print file, count
	return count


def main():
	parser = optparse.OptionParser("-p project_path -t file_type1 file_type2...")
	parser.add_option('-p', '--path', dest='path', type='string', help='project path')
	parser.add_option('-t', '--type', dest='type', type='string', help='file type')
	(options, args) = parser.parse_args()
	path = options.path
	file_type = options.type
	args.append(file_type)
	if (path == None) | (file_type == None):
		print('[-] You must specify a project path and serveral file types.')
		return

	for fileType in args:
		type_list.append(fileType)

	start_time = time.clock() 

	total_count = 0
	get_file(path)
	for file in file_list:
		total_count += count_line(file)

	print('=== total line count:%s ===' % total_count)
	print('time:%0.2f second.' % (time.clock() - start_time))

if __name__ == '__main__':
	main()
