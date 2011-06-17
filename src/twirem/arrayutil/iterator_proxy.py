#-*- coding: utf-8 -*-

class IteratorProxy(object):
	"""
	>> array = [1,2,3]
	>> proxy = IteratorProxy(array, lambda o: 'num%d' % o)
	>> it = iter(proxy)
	>> it.next()
	'num1'
	>> it.next()
	'num2'
	>> it.next()
	'num3'
	>> proxy[1]
	'num2'
	>> len(proxy)
	3
	"""

	def __init__(self, iteratableList, vfunc):
		self.iteratableList = iteratableList
		self.vfunc = vfunc

	def __iter__(self):
		for o in self.iteratableList: 
			yield self.vfunc(o)

	def __getitem__(self, index):
		if isinstance(index, slice):
			return [self.vfunc(o) for o in self.iteratableList[index]]
		else:
			return self.vfunc(self.iteratableList[index])

	def __len__(self):
		return self.iteratableList.__len__()

