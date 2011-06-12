#-*- coding: utf-8 -*-

import bisect

class _T:
	def __init__(self, v):
		self.prop = v

class BisectListProxy(object):
	"""
	オブジェクトの配列を、bisectモジュールを利用して効率よく
	追加・削除を行う。
	"""
	def __init__(self, olist, value_func = None, do_sort = True):
		self.olist = olist
		if value_func is None:
			self.vfunc = lambda o: o
		else:
			self.vfunc = value_func

		if do_sort:
			self.olist.sort(lambda a, b: cmp(self.vfunc(a),self.vfunc(b)))
	
	def __getitem__(self, index):
		"""
		indexの位置の要素のプロパティ値を返す。
		"""
		return self.vfunc(self.olist[index])

	def __len__(self):
		return self.olist.__len__()

	def __repr__(self):
		return self.olist.__repr__()

	def __str__(self):
		return self.olist.__str__()

	def __iter__(self):
		return self.olist.__iter__()

	@property
	def value_list(self):
		"""
		プロパティ値のリストを返す
		"""
		return [self.vfunc(v) for v in self.olist]

	def objAt(self, index):
		"""
		indexの位置の要素を返す。
		"""
		return self.olist[index]

	def add(self, obj):
		"""
		objを昇順になるようにリストに追加する。
		"""
		index = bisect.bisect_left(self, self.vfunc(obj))
		self.olist.insert(index, obj)
	
	'''
	def delete(self, obj):
		"""
		プロパティ値が、objのプロパティ値と同じ要素を
		リストから全て削除する。
		"""
		indexl = bisect.bisect_left(self, self.vfunc(obj))
		indexr = bisect.bisect_right(self, self.vfunc(obj))
		del self.olist[indexl:indexr]
	'''
	
	def delete_value(self, value):
		"""
		プロパティ値がvalueの要素をリストから全て削除する。
		"""
		indexl = bisect.bisect_left(self, value)
		indexr = bisect.bisect_right(self, value)
		del self.olist[indexl:indexr]
	
	def pop_value(self, value):
		"""
		プロパティ値がvalueの要素を1つリストから削除し、そのオブジェクト返す。
		"""
		index = bisect.bisect_left(self, value)
		return self.olist.pop(index)

