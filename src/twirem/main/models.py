#-*- coding: utf-8 -*-

import time
from django.db import models
from datetime import datetime
from django.db.models import Q

_maxtime = time.mktime(datetime.max.timetuple())

def q_inner(tick = None, key = ''):
	if tick is None: tick = time.time()
	if key != '' : key += '__'
	kargs = {}
	kargs[key + 'start_date__lte'] = tick
	kargs[key + 'end_date__gt'] = tick
	return Q(**kargs)

class Authorization(models.Model):
	user_id = models.IntegerField(primary_key = True)
	screen_name = models.CharField(max_length = 20)
	token = models.CharField(max_length = 100, blank = True)
	token_secret = models.CharField(max_length = 100, blank = True)
	def __init__(self, *args, **kwargs):
		super(Authorization, self).__init__(*args, **kwargs)
		self.user_profile = UserProfile.objects.get_or_create(user_id = self.user_id)[0]
		self.user_profile.authorization = self
		self.user_profile.save()

class UserProfile(models.Model):
	"""
	next_update_date : 次回このユーザ回りの更新をする日時
	"""
	user_id = models.IntegerField(primary_key = True, db_index = True)
	authorization = models.OneToOneField('Authorization', related_name = 'user_profile', null = True)
	update_date = models.FloatField(default = 0)

	def __init__(self, *args, **kwargs):
		super(UserProfile, self).__init__(*args, **kwargs)
		self.friends_activity = UserFriendsActivity.objects.get_or_create(
				user = self)[0]
		self.followers_activity = UserFollowersActivity.objects.get_or_create(
				user = self)[0]
		self.bios_activity = UserBiosActivity.objects.get_or_create(
				user = self)[0]

	@property
	def screen_name_now(self):
		return self.screen_names.get(q_inner()).screen_name
	@property
	def icons_now(self):
		return self.icons.get(q_inner())
	@property
	def screen_names_now(self):
		return self.screen_names.get(q_inner())
	@property
	def friends_now(self):
		return self.friends.filter(q_inner())
	@property
	def followers_now(self):
		return self.followers.filter(q_inner())

class UserFriendsActivity(models.Model):
	"""
	フレンドの更新がされたかどうか
	"""
	user = models.OneToOneField('UserProfile', related_name = 'friends_activity')
	update_date = models.FloatField(default = 0)

class UserFollowersActivity(models.Model):
	"""
	フォロワーの更新がされたかどうか
	"""
	user = models.OneToOneField('UserProfile', related_name = 'followers_activity')
	update_date = models.FloatField(default = 0)

class UserBiosActivity(models.Model):
	"""
	Bioの更新がされたかどうか
	"""
	user = models.OneToOneField('UserProfile', related_name = 'bios_activity')
	update_date = models.FloatField(default = 0)

class UserBio(models.Model):
	user = models.OneToOneField('UserProfile', related_name = 'latest_bio')
	screen_name = models.CharField(max_length = 20)
	icon_url = models.CharField(max_length = 500)
	update_date = models.FloatField(default = 0)

class SpanModel(models.Model):
	start_date = models.FloatField(default = -1)
	end_date = models.FloatField(default = _maxtime)

	def __init__(self, *args, **kwargs):
		super(SpanModel, self).__init__(*args, **kwargs)
		if self.start_date == -1:
			self.start_date = time.time()

	@property
	def start_date_datetime(self):
		return datetime.fromtimestamp(self.start_date)
	@property
	def end_date_datetime(self):
		return datetime.fromtimestamp(self.end_date)

	class Meta:
		abstract = True


class UserFriend(SpanModel):
	user = models.ForeignKey('UserProfile',
			related_name = 'friends', db_index = True)
	friend = models.ForeignKey('UserProfile',
			related_name = 'followers', db_index = True)
	unfollow = models.BooleanField()

class UserScreenName(SpanModel):
	user = models.ForeignKey('UserProfile',
			related_name = 'screen_names', db_index = True)
	screen_name = models.CharField(max_length = 20)

class UserIcon(SpanModel):
	"""
	small(), normal(), bigger(), original()関数で、
	画像のファイルパスを取得できる。
	403で画像が取得できなかった時などは、digestには何もセットしない。
	"""
	user = models.ForeignKey('UserProfile',
			related_name = 'icons', db_index = True)
	url = models.CharField(max_length = 500)
	digest = models.CharField(max_length = 40, null = True)
	def small(self):
		pass
	def normal(self):
		pass
	def bigger(self):
		pass
	def original(self):
		pass
