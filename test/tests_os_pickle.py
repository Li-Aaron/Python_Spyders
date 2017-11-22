# -*- coding: utf-8 -*-
'''
@Author: AC
2017-10-15
'''
__author__ = 'AC'

# normal IO operators
PATH = r'D:\Codes\Python\Python_Spyders'
try:
	f = open(PATH+r'\test.txt')
	print f.read()
finally:
	f.close()

# after Python 2.6
with open(PATH+r'\test.txt','r') as f:
	for line in f.readlines():
		print line.strip()

with open(PATH+r'\test.txt','w') as f:
	f.write("I'm very happy to be an Indian\n")

# OS operators
import os
print os.getcwd()
print os.listdir(PATH)
print os.listdir(os.getcwd())
print os.name
print os.linesep


# serial operators
try:
	import cPickle as pickle 
except ImportError:
	import pickle

d = dict(url = 'index.html', title = '首页', content = '首页')
pickle.dumps(d)

with open(PATH+r'\pickle.txt','w') as f:
	pickle.dump(d,f)
with open(PATH+r'\pickle.txt','r') as f:
	d1 = pickle.load(f)

#print d
#print d1



