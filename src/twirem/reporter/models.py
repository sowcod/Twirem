#-*- coding: utf-8 -*-

from django.db import models

DIFF_TYPE = (
		('E', 'Equal'),
		('C', 'Change'),
		('N', 'None'),
		)

class Report(models.Model):
	"""
	followers
	friends
	screen_names
	icons
	"""
	user = models.ForeignKey('main.UserProfile')
	start_date = models.FloatField(default = 0)
	end_date = models.FloatField(default = 0)

class DiffFollower(models.Model):
	"""
	remove : Trueなら、リムーブされた。Falseなら、フォローされた。
	"""
	report = models.ForeignKey('Report', related_name = 'followers')
	user = models.ForeignKey('main.UserProfile')
	remove = models.BooleanField()

class DiffFriend(models.Model):
	"""
	remove : Trueなら、リムーブした。Falseなら、フォローした。　
	"""
	report = models.ForeignKey('Report', related_name = 'friends')
	user = models.ForeignKey('main.UserProfile')
	remove = models.BooleanField()

class DiffScreenName(models.Model):
	report = models.ForeignKey('Report', related_name = 'screen_name')
	old = models.ForeignKey('main.UserScreenName', related_name = 'diff_old', null = True)
	new = models.ForeignKey('main.UserScreenName', related_name = 'diff_new', null = True)
	diff_type = models.CharField(max_length = 1, choices = DIFF_TYPE)

class DiffIcon(models.Model):
	report = models.ForeignKey('Report', related_name = 'icon')
	old = models.ForeignKey('main.UserIcon', related_name = 'diff_old', null = True)
	new = models.ForeignKey('main.UserIcon', related_name = 'diff_new', null = True)
	diff_type = models.CharField(max_length = 1, choices = DIFF_TYPE)
