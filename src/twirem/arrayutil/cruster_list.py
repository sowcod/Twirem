#-*- coding: utf-8 -*-
import math

class CrusterList(object):
	def __init__(self, iteratableList, cruster = 100):
		self.iteratableList = iteratableList
		self.cruster = cruster
	
	def __iter__(self):
		count = 0
		newList = []
		it = iter(self.iteratableList)
		try:
			while True :
				if count < self.cruster:
					newList.append(it.next())
					count += 1
				else:
					yield newList
					count = 0
					newList = []
		except StopIteration:
			if count > 0 : yield newList
	
	def __len__(self):
		return int(math.ceil(self.iteratableList.__len__() / float(self.cruster)))

	def __getitem__(self, index):
		maxlen = len(self.iteratableList)
		if index * self.cruster >= maxlen : raise IndexError()
		
		begin = index * self.cruster
		end = min((index + 1) * self.cruster, maxlen)
		return self.iteratableList[begin:end]

