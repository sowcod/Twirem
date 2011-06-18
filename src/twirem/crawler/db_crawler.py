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
			self.crawl_bios(limit = 10)
			time.sleep(self.sleep)
	
	def crawl_bios(self, limit = 50):
		bios = UserBio.objects.all().order_by('update_date')[:limit]
		#ids = [bio.user_id for bio in bios]
		#user_dict = UserProfile.objects.select_related(
		#		'screen_names', 'icons').filter(
		#		q_inner(key='screen_names'), q_inner(key='icons')
		#		).in_bulk(ids)

		for bio in bios:
			#user = user_dict[bio.user_id] if bio.user_id in user_dict else None
			logging.debug('crawl bio %s' % bio.user_id)
			user = UserProfile.objects.get_or_create(user_id = bio.user_id)[0]
			self.update_screen_name(bio, user)
			self.update_icon(bio, user)
			bio.delete()
	
	def update_screen_name(self, bio, user):
		"""
		bioでUserScreenNameを更新する
		"""
		try:
			old_sn = user.screen_names_now # sn : screen_name
		except UserScreenName.DoesNotExist:
			old_sn = None

		if old_sn is None or old_sn.screen_name != bio.screen_name:
			new_sn = user.screen_names.create(screen_name = bio.screen_name)
			if old_sn is not None:
				old_sn.end_date = new_sn.start_date
				old_sn.save()

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
				or old_icon.url != icon.urls['normal'] \
				or old_icon.digest != icon.digest:
			icon.load_all()
			new_icon = user.icons.create(digest = icon.digest, url = icon.urls['normal'])
			if old_icon is not None:
				old_icon.end_date = new_icon.start_date
				old_icon.save()
