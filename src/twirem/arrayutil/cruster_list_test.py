#-*- coding: utf-8 -*-

import unittest
from cruster_list import CrusterList

class CrusterListTest(unittest.TestCase):
	def setUp(self):
		pass
	
	def test_cruster10(self):
		list10 = [1,2,3,4,5,6,7,8,9,10]
		cruster = CrusterList(list10, 10)
		self.assertEquals(len(cruster), 1)
		self.assertEquals(cruster[0], list10[:])
		self.assertRaises(IndexError, cruster.__getitem__,1)
	
	def test_cruster11(self):
		list10 = [1,2,3,4,5,6,7,8,9,10]
		cruster = CrusterList(list10, 11)
		self.assertEquals(len(cruster), 1)
		self.assertEquals(cruster[0], list10[:])
		self.assertRaises(IndexError, cruster.__getitem__,1)

	def test_cruster9(self):
		list10 = [1,2,3,4,5,6,7,8,9,10]
		cruster = CrusterList(list10, 9)
		self.assertEquals(len(cruster), 2)
		self.assertEquals(cruster[0], list10[:9])
		self.assertEquals(cruster[1], list10[9:10])
		self.assertRaises(IndexError, cruster.__getitem__,2)

		it = iter(cruster)
		self.assertEquals(it.next(), list10[:9])
		self.assertEquals(it.next(), list10[9:10])
		self.assertRaises(StopIteration, it.next)
	
if __name__ == '__main__':
	unittest.main()
