#-*- coding: utf-8 -*-

class Marge(object):
	def __init__(self, listL, listR, comp_func):
		self.listL = listL
		self.listR = listR
		if comp_func is None:
			self.compf = lambda l, r : cmp(l, r)
		else:
			self.compf = comp_func
	
	def full(self, 
			match = lambda l,r: 0,
			left = lambda l,r: 0,
			right = lambda l,r: 0):
		u"""
		同一キー:  match(lo, ro)
		leftのみ:  left(lo)
		rightのみ: right(ro)
		"""
		indexL = 0
		indexR = 0
		lenL = len(self.listL)
		lenR = len(self.listR)
		while indexL < lenL and indexR < lenR:
			lo = self.listL[indexL]
			ro = self.listR[indexR]
			if self.compf(lo,ro) == 0 :
				match(lo, ro)
				indexL += 1
				indexR += 1
			elif self.compf(lo, ro) < 0 :
				left(lo)
				indexL += 1
			else:
				right(ro)
				indexR += 1
		else:
			while indexR < lenR:
				right(self.listR[indexR])
				indexR += 1
			while indexL < lenL:
				left(self.listL[indexL])
				indexL += 1

	
