from django.test import TestCase


class Decorator(object):
	def __init__(self,func):
		print 'init decorator'
		self.func = func
	def __call__(self):
		print 'call func'
		self.func()

@Decorator
def foo():
	print 'i am foo'


def gift_deco(gift):
	print 'gift_deco'
	def outer_wrapper(func):
		print '....outer_wrapper'
		def innter_wrapper(*args, **kwags):
			print '........innter_wrapper %s' % gift
			func(*args, **kwags)
		return innter_wrapper
	return outer_wrapper

@gift_deco('test gift')
def foo(*args, **kwags):
	print '............foo'
	print args
