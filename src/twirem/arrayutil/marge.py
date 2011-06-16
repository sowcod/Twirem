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
		iterL = iter(self.listL)
		iterR = iter(self.listR)
		endL = False
		endR = False

		def nextL():
			try: return iterL.next(), False
			except StopIteration: return None, True
		def nextR():
			try: return iterR.next(), False
			except StopIteration: return None, True

		(lo, endL) = nextL()
		(ro, endR) = nextR()

		while endL == False and endR == False:
			if self.compf(lo,ro) == 0 :
				match(lo, ro)
				(lo, endL) = nextL()
				(ro, endR) = nextR()
			elif self.compf(lo, ro) < 0 :
				left(lo)
				(lo, endL) = nextL()
			else:
				right(ro)
				(ro, endR) = nextR()
		else:
			while endR == False:
				right(ro)
				(ro, endR) = nextR()
			while endL == False:
				left(lo)
				(lo, endL) = nextL()
