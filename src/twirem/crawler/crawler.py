#-*- coding: utf-8 -*-

from twirem.main.models import UserProfile
from twirem.main import auth_util
from twirem.crawler import UserInfoRequester
from twirem.crawler import db_update
import time

class Crawler(object):
	def __init__(self, sleep = 5):
		self.sleep = sleep

	def run(self):
		while True:
			self.crawl_users(limit = 1)
			time.sleep(self.sleep)
	
	def crawl_users(self, limit = 1):
		"""
		クロールすべきユーザを探してクロールする
		"""
		users = UserProfile.objects.filter(
				authorization__isnull = False,
				next_update_date__lt = time.time()
				).order_by('-next_update_date')[:limit]

		for user in users:
			self.crawl_user(user)

	def crawl_user(self, user):
		"""
		ユーザを中心とした各情報をクロールする
		"""
		auth = user.authorization
		api = auth_util.create_api(auth = auth)
		requester = UserInfoRequester(api)

		self.update_followers(user, requester)
		self.update_friends(user, requester)
		self.update_bios(user, requester)

		users = [str(user.user_id) for user 
				in users_noactivity(auth.user_id) if user.activity == 0]
		update_users = sorted(requester.lookup(users),
				cmp = lambda a,b:cmp(a['id'], b['id']))

	def update_followers(self, user, requester):
		activity = user.followers_activity
		if activity != 0 : return

		new_followers = requester.request_followers_ids(user.user_id)
		db_update.update_followers(user.user_id, new_followers)

		activity = user.followers_activity
		activity.update_date = time.time()
		activity.save()

	def update_friends(self, user, requester):
		activity = user.friends_activity
		if activity != 0 : return

		new_friends = requester.request_friend_ids(user.user_id)
		db_update.update_friends(user.user_id, new_friends)

		activity = user.followers_activity
		activity.update_date = time.time()
		activity.save()
	
	def update_bios(self, user, requester):
		pass


