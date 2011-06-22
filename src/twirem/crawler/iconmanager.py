#-*- coding: utf-8 -*-

import os
import os.path
import urllib2
import urllib
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
	http://~~~/~~~_reasonably_small.xxx
	http://~~~/~~~_bigger.xxx
	http://~~~/~~~_normal.xxx
	http://~~~/~~~_mini.xxx
	に変換
	"""
	m = re.match(r'^(.*/)([^/]+)_normal(\.\w*)?$', url.encode('utf-8'))
	
	pre = m.group(1)
	mid = urllib.quote(m.group(2))
	suf = m.group(3) if m.group(3) is not None else ''

	newurl = lambda n: pre + mid + n + suf

	return {
			'full': newurl('_reasonably_small'),
			'full2': newurl(''),
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
			'full': os.path.join(digest_dir, 'full'),
			'bigger': os.path.join(digest_dir, 'bigger'),
			'normal': os.path.join(digest_dir, 'normal'),
			'mini': os.path.join(digest_dir, 'mini'),
			'mimetype': os.path.join(digest_dir, 'mimetype'),
			}

class ManagedIcon(object):
	def __init__(self, url = None, digest = None):
		"""
		url : _normal url
		"""
		if url is not None:
			self.urls = convert_iconurl(url)
			self.digest = None
			try:
				self.load('normal', [self.urls['normal']], digest_target = True)
			except ManagedIcon.CannotLoad:
				pass
		if digest is not None:
			self.digest = digest
	
	def load_all(self):
		if self.digest is None: return
		self.save_mimetype()
		#self.load('bigger')
		#self.load('mini')
		self.load('full', [
			self.urls['full'],
			self.urls['full2'],
			self.urls['normal']
			])
	
	def save_mimetype(self):
		self.save(self.mimetype, 'mimetype')

	def load(self, name, urls, digest_target = False):
		"""
		raise : IOError, urllib2.HTTPError, ManagedIcon.ForbiddenLoading
		"""
		response = None
		buf = None
		mimetype = None

		for url in urls:
			try:
				response = urllib2.urlopen(url)
				buf = response.read()
				if len(buf) < 50: continue

				mimetype = response.headers.type
				break
			except urllib2.HTTPError, er:
				if er.code == 403: continue
				raise

		if mimetype == None:
			raise ManagedIcon.CannotLoad()

		if digest_target :
			self.digest = hashlib.sha1(buf).hexdigest()
			self.mimetype = mimetype
		self.save(buf, name)
	
	def save(self, buf, name):
		"""
		raise : ManagedIcon.DigestIsNotSet
		return : filepath
		"""
		if self.digest is None:
			raise ManagedIcon.DigestIsNotSet()

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
	
	class DigestIsNotSet(Exception):
		def __init__(self):
			self.message = 'digest is not set.'

		def __str__(self):
			return self.message

	class CannotLoad(Exception):
		def __init__(self):
			self.message = 'image cannot load.'

		def __str__(self):
			return self.message
	
