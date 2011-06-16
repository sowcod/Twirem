#-*- coding: utf-8 -*-

import time
from django.db import models
from datetime import datetime
from django.db.models import Q

_maxtime = time.mktime(datetime.max.timetuple())

def q_inner(tick = None):
	if tick is None: tick = time.time()
	return Q(start_date__lte = tick, end_date__gt = tick)

def get_or_create(model, **args):
	try:
		obj = models.objects.get(**args)
	except model.DoesNotExist:
		obj = model(**args)
	return obj

class Authorization(models.Model):
	user_id = models.IntegerField(primary_key = True)
	screen_name = models.CharField(max_length = 20)
	token = models.CharField(max_length = 100, blank = True)
	token_secret = models.CharField(max_length = 100, blank = True)

class UserProfile(models.Model):
	"""
	next_update_date : 次回このユーザ回りの更新をする日時
	"""
	user_id = models.IntegerField(primary_key = True, db_index = True)
	activity = models.IntegerField(default = 0)
	authorization = models.OneToOneField('Authorization', related_name = 'user_profile', null = True)
	next_update_date = models.FloatField(default = 0)

	def __init__(self, *args, **kwargs):
		super(UserProfile, self).__init__(*args, **kwargs)
		self.friends_activity = UserFriendsActivity()
		self.followers_activity = UserFollowersActivity()
		self.bio_activity = UserBioActivity()
		self.save()

	@classmethod
	def get_or_create(cls, user_id, **args):
		try:
			user = cls.objects.get(user_id = user_id)
			return user
		except UserProfile.DoesNotExist:
			user = cls(user_id = user_id, **args)
			user.save()
			return user
	
	@property
	def screen_name_now(self):
		return self.screen_names.get(q_inner()).screen_name
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

class UserBioActivity(models.Model):
	"""
	Bioの更新がされたかどうか
	"""
	user = models.OneToOneField('UserProfile', related_name = 'bio_activity')
	update_date = models.FloatField(default = 0)

class UserBio(models.Model):
	user = models.OneToOneField('UserProfile', related_name = 'latest_bio')
	screen_name = models.CharField(max_length = 20)
	icon_url = models.CharField(max_length = 500)
	expiration_date = models.FloatField(default = 0)

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
	user = models.ForeignKey('UserProfile',
			related_name = 'icons', db_index = True)
	url = models.CharField(max_length = 500)
	digest = models.CharField(max_length = 40)
