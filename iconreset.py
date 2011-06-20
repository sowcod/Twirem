#-*- coding: utf-8 -*-

"""
キャッシュしたアイコンを全て削除する
"""

import os
import os.path

def checkdir(basepath):
	dirs1 = os.listdir(basepath)
	for dir1 in dirs1:
		if dir1 == 'z_empty' or dir1[0] == '.': continue
		cdir = os.path.join(basepath, dir1)
		dirs2 = os.listdir(cdir)
		for dir2 in dirs2:
			if dir1[0] == '.': continue
			checkicons(dir2, os.path.join(cdir, dir2))
			os.rmdir(os.path.join(cdir, dir2))
		os.rmdir(cdir)

def checkicons(digest, icondir):
	files = os.listdir(icondir)
	for f in files:
		os.unlink(os.path.join(icondir, f))

checkdir('./icons')
