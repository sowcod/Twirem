#-*- coding: utf-8 -*-

from twirem.main.models import UserProfile
from twirem.main import auth_util
from twirem.crawler.user_info_requester import UserInfoRequester
from twirem.crawler import db_update
from twirem.arrayutil import IteratorProxy, CrusterList
import logging
import time
import threading

class ApiCrawler(threading.Thread):
	def __init__(self, sleep = 5):
		super(ApiCrawler, self).__init__(target = self)
		self.sleep = sleep
		self.expire_time = 60 * 60 * 1
		self.setDaemon(True)

	def run(self):
		logging.debug('start crawling api')
		while True:
			self.crawl_users(limit = 10)
			time.sleep(self.sleep)
	
	def crawl_users(self, limit = 1):
		"""
		クロールすべきユーザを探してクロールする
		"""
		users = UserProfile.objects.filter(
				authorization__isnull = False,
				update_date__lt = time.time() - self.expire_time
				).order_by('update_date')[:limit]
		logging.debug('ApiCrawler time : %d' % (time.time() - self.expire_time))

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

		user.update_date = time.time()
		user.save()
		user.followers_activity.update_date = 0
		user.friends_activity.update_date = 0
		user.bios_activity.update_date = 0

		user.followers_activity.save()
		user.friends_activity.save()
		user.bios_activity.save()

	def update_followers(self, user, requester):
		"""
		ユーザのフォロワー状況を更新
		"""
		activity = user.followers_activity
		if activity.update_date != 0 : return

		new_followers = requester.request_follower_ids(user.user_id)
		db_update.update_followers(user.user_id, new_followers)

		activity.update_date = time.time()
		activity.save()

	def update_friends(self, user, requester):
		"""
		ユーザのフレンド状況を更新
		"""
		activity = user.friends_activity
		if activity.update_date != 0 : return

		new_friends = requester.request_friend_ids(user.user_id)
		db_update.update_friends(user.user_id, new_friends)

		activity.update_date = time.time()
		activity.save()
	
	def update_bios(self, user, requester):
		"""
		ユーザに関連するユーザのBioを更新
		"""
		activity = user.bios_activity
		if activity.update_date != 0 : return

		target_users = db_update.users_related(user.user_id)
		users_list = CrusterList(target_users, 99)
		for users in users_list:
			bios = requester.lookup(IteratorProxy(users, lambda o: str(o.user_id)))
			db_update.update_bios(bios, time.time() - self.expire_time)

		activity.update_date = time.time()
		activity.save()

