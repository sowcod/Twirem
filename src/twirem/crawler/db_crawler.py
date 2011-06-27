#-*- coding: utf-8 -*-

from twirem.main.models import UserProfile, UserBio
from twirem.main.models import UserScreenName, UserIcon
from iconmanager import ManagedIcon
import logging
import time
import threading

class DatabaseCrawler(threading.Thread):
	def __init__(self, sleep):
		super(DatabaseCrawler, self).__init__(target = self)
		self.sleep = sleep
		self.setDaemon(True)
	
	def run(self):
		logging.debug('start crawling database')
		while True:
			start_time = time.time()
			self.crawl_bios(limit = 50)
			timediff = time.time() - start_time
			if timediff > 60 : logging.debug('crawl_bios() time %d' % timediff)
			time.sleep(self.sleep)
	
	def crawl_bios(self, limit = 50):
		all_bios = UserBio.objects.all()
		bios = all_bios.order_by('update_date')[:limit]
		#ids = [bio.user_id for bio in bios]
		#user_dict = UserProfile.objects.select_related(
		#		'screen_names', 'icons').filter(
		#		q_inner(key='screen_names'), q_inner(key='icons')
		#		).in_bulk(ids)
		logging.debug('DatabaseCrawler time : %d / remaining %d users' % (time.time(), all_bios.count()))

		for bio in bios:
			#user = user_dict[bio.user_id] if bio.user_id in user_dict else None
			#logging.debug('crawl bio %s' % bio.user_id)

			try:
				user = UserProfile.objects.get_or_create(user_id = bio.user_id)[0]
				self.update_screen_name(bio, user)
				self.update_icon(bio, user)
				bio.delete()
			except Exception, ex:
				logging.debug('Exception \'crawl_bio()\' user : %d / %s / %s' % (bio.user_id, ex.__class__, ex))
	
	def update_screen_name(self, bio, user):
		"""
		bioでUserScreenNameを更新する
		"""
		try:
			old_sn = user.screen_names_now # sn : screen_name
		except UserScreenName.DoesNotExist:
			old_sn = None

		if old_sn is None or old_sn.screen_name != bio.screen_name:
			if old_sn is not None:
				new_sn = user.screen_names.create(screen_name = bio.screen_name)
				old_sn.end_date = new_sn.start_date
				old_sn.save()
			else:
				new_sn = user.screen_names.create(screen_name = bio.screen_name,
						start_date = 0)


	def update_icon(self, bio, user):
		"""
		bioでUserIconを更新する
		"""
		try:
			old_icon = user.icons_now # sn : screen_name
		except UserIcon.DoesNotExist:
			old_icon = None

		# normalアイコン画像を取得してdigestを計算する
		icon = ManagedIcon(bio.icon_url)

		if old_icon is None \
				or old_icon.url.encode('utf-8') != icon.urls['normal'] \
				or old_icon.digest != icon.digest:
			icon.load_all()
			if old_icon is not None:
				new_icon = user.icons.create(digest = icon.digest, url = icon.urls['normal'])
				old_icon.end_date = new_icon.start_date
				old_icon.save()
			else:
				new_icon = user.icons.create(digest = icon.digest, url = icon.urls['normal'],
						start_date = 0)

