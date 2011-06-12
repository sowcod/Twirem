import unittest
from marge import Marge

class _T:
	"""
	_T has 'prop'
	"""
	def __init__(self, val):
		self.prop = val

class MargeTest(unittest.TestCase):
	def setUp(self):
		self.list1 = [_T(1),_T(2),_T(3),_T(4)]
		self.list2 = [_T(2),_T(3),_T(4),_T(5)]
		self.list3 = [_T(2),_T(4),_T(5),_T(6)]
		self.list4 = [_T(5),_T(6),_T(7),_T(8)]

	def marge_templ(self, listl, listr):
		m = Marge(listl, listr,
				comp_func = lambda l, r: cmp(l.prop,r.prop))

		matchList = []
		leftList = []
		rightList = []

		def matchf(lo, ro):
			matchList.append(lo.prop)
		def leftf(lo):
			leftList.append(lo.prop)
		def rightf(ro):
			rightList.append(ro.prop)

		m.full(matchf, leftf, rightf)

		return matchList, leftList, rightList

	def test_full_equal(self):
		(matchList, leftList, rightList) = self.marge_templ(
				self.list1, self.list1)

		self.assertEquals(len(matchList), 4)
		self.assertEquals(matchList[0], 1)
		self.assertEquals(matchList[1], 2)
		self.assertEquals(matchList[2], 3)
		self.assertEquals(matchList[3], 4)
		self.assertEquals(len(leftList), 0)
		self.assertEquals(len(rightList), 0)

	def test_full_left(self):
		(matchList, leftList, rightList) = self.marge_templ(
				self.list2, self.list1)

		self.assertEquals(len(matchList), 3)
		self.assertEquals(matchList[0], 2)
		self.assertEquals(matchList[1], 3)
		self.assertEquals(matchList[2], 4)
		self.assertEquals(len(leftList), 1)
		self.assertEquals(leftList[0], 5)
		self.assertEquals(len(rightList), 1)
		self.assertEquals(rightList[0], 1)

	def test_full_right(self):
		(matchList, leftList, rightList) = self.marge_templ(
				self.list1, self.list2)

		self.assertEquals(len(matchList), 3)
		self.assertEquals(matchList[0], 2)
		self.assertEquals(matchList[1], 3)
		self.assertEquals(matchList[2], 4)
		self.assertEquals(len(leftList), 1)
		self.assertEquals(leftList[0], 1)
		self.assertEquals(len(rightList), 1)
		self.assertEquals(rightList[0], 5)

	def test_full_all(self):
		(matchList, leftList, rightList) = self.marge_templ(
				self.list3, self.list4)

		self.assertEquals(len(matchList), 2)
		self.assertEquals(matchList[0], 5)
		self.assertEquals(matchList[1], 6)
		self.assertEquals(len(leftList), 2)
		self.assertEquals(leftList[0], 2)
		self.assertEquals(leftList[1], 4)
		self.assertEquals(len(rightList), 2)
		self.assertEquals(rightList[0], 7)
		self.assertEquals(rightList[1], 8)

if __name__ == '__main__':
	unittest.main()
