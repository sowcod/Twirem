#-*- coding: utf-8 -*-

import os
import os.path
import urllib2
import hashlib
import re

_path = None

class PathNotExists(Exception):
	def __init__(self, path):
		self.path = path
	
	def __str__(self):
		return '\"%s\" is not exists' % self.path

def set_base_path(path):
	global _path
	if not os.path.exists(path):
		raise PathNotExists(path)
	_path = path

def convert_iconurl(url):
	"""
	http://~~~/~~~_normal.xxx
	を、
	http://~~~/~~~.xxx
	http://~~~/~~~_bigger.xxx
	http://~~~/~~~_normal.xxx
	http://~~~/~~~_mini.xxx
	に変換
	"""
	m = re.match(r'^(.*)_normal(\.\w*)?$', url)
	pre = m.group(1)
	suf = m.group(2) if m.group(2) is not None else ''

	newurl = lambda n: pre + n + suf

	return {
			'original': newurl(''),
			'bigger': newurl('_bigger'),
			'normal': newurl('_normal'),
			'mini' : newurl('_mini'),
			}

def icon_pre_dir(digest):
	return os.path.abspath(os.path.join(_path, digest[:2]))

def icon_digest_dir(digest):
	return os.path.join(icon_pre_dir(digest), digest)

def icon_paths(digest):
	digest_dir = icon_digest_dir(digest)
	return {
			'original': os.path.join(digest_dir, 'original'),
			'bigger': os.path.join(digest_dir, 'bigger'),
			'normal': os.path.join(digest_dir, 'normal'),
			'mini': os.path.join(digest_dir, 'mini'),
			}
			

class ManagedIcon(object):
	def __init__(self, url = None, digest = None):
		"""
		url : _normal url
		"""
		if url is not None:
			self.urls = convert_iconurl(url)
			self.load('normal', digest_target = True)
		if digest is not None:
			self.digest = digest
	
	def load_all(self):
		self.load('bigger')
		self.load('mini')
		try:
			self.load('original')
		except urllib2.HTTPError:
			pass

	def load(self, name, digest_target = False):
		"""
		raise : IOError, urllib2.HTTPError
		"""
		response = urllib2.urlopen(self.urls[name])
		buf = response.read()
		if digest_target :
			self.digest = hashlib.sha1(buf).hexdigest()
		self.save(buf, name)
	
	def save(self, buf, name):
		"""
		raise : ManagedIcon.IconNotLoaded
		return : filepath
		"""
		if buf is None:
			raise ManagedIcon.IconNotLoaded()

		predir = icon_pre_dir(self.digest)
		if not os.path.exists(predir):
			os.mkdir(predir)

		digestdir = icon_digest_dir(self.digest)
		if not os.path.exists(digestdir):
			os.mkdir(digestdir)

		writepath = icon_paths(self.digest)[name]
		if not os.path.exists(writepath):
			with open(writepath, 'w') as f:
				f.write(buf)

		return writepath
	
	class IconNotLoaded(Exception):
		def __init__(self):
			self.message = 'Call \'load()\' method.'

		def __str__(self):
			return self.message
	
