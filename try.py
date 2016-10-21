# encoding=utf-8


a = [1,2,3]
b = [4,5,6]
c = zip(a,b)
d = zip(*c)
print (list(d))
print ("你好")