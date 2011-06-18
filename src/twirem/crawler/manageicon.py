#-*- coding: utf-8 -*-

import os

class PathNotExists(Exception):
	def __init__(self, path):
		self.path = path
	
	def __str__(self):
		return '\"%s\" is not exists' % self.path

def set_base_path(path):
	global _path
	if not os.exists(path):
		raise PathNotExists(path)
	_path = path

class ManageIcon(object):
	def __init__(self):
		pass
