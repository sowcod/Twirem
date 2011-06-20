#-*- coding: utf-8 -*-

"""
iconsフォルダ内容を見て足りないファイル等を調査する
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

def checkicons(digest, icondir):
	files = os.listdir(icondir)
	if 'full' not in files: print('%s / missing: full' % digest)
	if 'mini' not in files: print('%s / missing: mini' % digest)
	if 'normal' not in files: print('%s / missing: normal' % digest)
	if 'bigger' not in files: print('%s / missing: bigger' % digest)

checkdir('./icons')
