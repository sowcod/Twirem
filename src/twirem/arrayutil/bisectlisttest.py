from bisectlist import BisectListProxy
import unittest

class _T:
	"""
	_T has 'prop'
	"""
	def __init__(self, val):
		self.prop = val

class BisectListProxyTest(unittest.TestCase):

	def setUp(self):
		self.olist = [_T(1), _T(3), _T(7), _T(9), _T(5)]
		self.blist = BisectListProxy(
				self.olist,
				value_func = lambda o : o.prop,
				do_sort = True)
		self.olist2 = [1,3,7,9,5]
		self.blist2 = BisectListProxy(self.olist2, do_sort = True)

	def test_add_default(self):
		answer = [1,2,3,3,5,7,9]
		self.blist2.add(2)
		self.blist2.add(3)
		for i, v in enumerate(self.blist2):
			self.assertEqual(v, answer[i])

	def test_do_sort(self):
		self.assertEqual(self.blist[0], 1)
		self.assertEqual(self.blist[1], 3)
		self.assertEqual(self.blist[2], 5)
		self.assertEqual(self.blist[3], 7)
		self.assertEqual(self.blist[4], 9)

	def test_objAt(self):
		self.assertEquals(self.blist.objAt(2).prop, 5)

	def test_add(self):
		self.blist.add(_T(2))
		self.blist.add(_T(3))
		self.assertEqual(self.blist[0], 1)
		self.assertEqual(self.blist[1], 2)
		self.assertEqual(self.blist[2], 3)
		self.assertEqual(self.blist[3], 3)
		self.assertEqual(self.blist[4], 5)
	
	'''
	def test_delete(self):
		self.blist.add(_T(3))
		self.blist.delete(_T(3))
		self.assertEquals(self.blist[0], 1)
		self.assertEquals(self.blist[1], 5)
		self.assertEquals(self.blist[2], 7)
	'''
	
	def test_delete_value(self):
		self.blist.add(_T(3))
		self.blist.delete_value(3)
		self.assertEquals(self.blist[0], 1)
		self.assertEquals(self.blist[1], 5)
		self.assertEquals(self.blist[2], 7)
	
	def test_value_list(self):
		answer = [1, 3, 5, 7, 9]
		for i, v in enumerate(self.blist.value_list):
			self.assertEquals(v, answer[i])

if __name__ == '__main__':
	unittest.main()
