# encoding=utf-8
from PIL import Image
import argparse
'''
灰度值：指黑白图像中点的颜色深度，范围一般从0到255，白色为255，黑色为0，故黑白图片也称灰度图像
灰度值公式将像素的 RGB 值映射到灰度值：
gray ＝ 0.2126 * r + 0.7152 * g + 0.0722 * b

'''
# handle the agrs from the command line
parser = argparse.ArgumentParser()

parser.add_argument('file') # input file
parser.add_argument('-o', '--output') # output file
parser.add_argument('--width', type = int, default = 80) # width of ascii pic
parser.add_argument('--height', type = int, default = 80) # height of ascii pic

# get args:
args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# characters transform oof RGB values
def get_char(r,g,b,alpha = 256):
	if alpha == 0:
		return ' '
	length = len(ascii_char)
	gray = int (0.2126 * r + 0.7152 * g + 0.0722 * b)

	unit = (256.0 + 1)/length
	return ascii_char[int(gray/unit)]

if __name__ == '__main__':

	img = Image.open(IMG)
	img = img.resize((WIDTH,HEIGHT), Image.NEAREST)

	txt = ""

	for i in range(HEIGHT):
		for j in range(WIDTH):
			txt += get_char(*img.getpixel((j,i)))
	txt += '\n'

	print (txt)

	# output charactor pic into file
	if OUTPUT:
		with open(OUTPUT,'w') as f:
			f.write(txt)
	else:
		with open("dora.txt", 'w') as f:
			f.write(txt)



