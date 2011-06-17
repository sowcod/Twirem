#-*- coding: utf-8 -*-

from twirem.main.models import UserProfile, UserScreenName, UserBio
from twirem.arrayutil import Marge, IteratorProxy
import time

def users_related(user_id, contains_unfollow = False):
	u"""
	user_id の自分自身・フレンド・フォロワーの
	UserProfileを返す。
	contains_unfollowがTrueの時、
		過去にフレンド/フォロワーだったものも対象にする。
	"""
	user = UserProfile.objects.get_or_create(user_id = user_id)[0]
	friend_friends   = user.friends_now.order_by('friend')
	friend_followers = user.followers_now.order_by('user')

	if not contains_unfollow:
		# unfolowを除外
		friend_friends   = friend_friends.exclude(unfollow = True)
		friend_followers = friend_followers.exclude(unfollow = True)

	friends   = IteratorProxy(friend_friends, lambda o: o.friend)
	followers = IteratorProxy(friend_followers, lambda o: o.user)

	users = []
	m = Marge(friends, followers, 
			comp_func = lambda l,r: cmp(l.user_id, r.user_id))
	m.full(match = lambda l, r: users.append(l),
			left = lambda o: users.append(o),
			right = lambda o: users.append(o))

	return users

def update_followers(user_id, followers):
	u"""
	user_id のフォロワーを、
	followers(intの配列) のユーザで更新する。
	"""
	new_followers = followers[:]
	new_followers.sort()
	user = UserProfile.objects.get_or_create(user_id = user_id)[0]
	db_followers = user.followers_now.order_by('user')

	def removed(o):
		friend_rem = user.followers.create(user = o.user, unfollow = True)
		o.end_date = friend_rem.start_date
		o.save()
	def followed(uid):
		user.followers.create(
				user = UserProfile.objects.get_or_create(user_id = uid)[0])
	def refollowed(o, uid):
		if not o.unfollow : return
		# refollow
		friend_rem = user.followers.create(user = o.user)
		o.end_date = friend_rem.start_date
		o.save()

	m = Marge(db_followers, new_followers,
			comp_func = lambda l, r: cmp(l.user.pk, r))
	m.full(match = refollowed, left = removed, right = followed)

def update_friends(user_id, friends):
	u"""
	user_id のフレンドを、
	friends(intの配列) のユーザで更新する。
	"""
	new_friends = friends[:]
	new_friends.sort()
	user = UserProfile.objects.get_or_create(user_id = user_id)[0]
	db_friends = user.friends_now.order_by('friend')

	def removed(o):
		friend_rem = user.friends.create(friend = o.friend, unfollow = True)
		o.end_date = friend_rem.start_date
		o.save()
		pass
	def followed(uid):
		user.friends.create(
				friend = UserProfile.objects.get_or_create(user_id = uid)[0])
		pass
	def refollowed(o, uid):
		if not o.unfollow : return
		#refollow
		friend_rem = user.friends.create(friend = o.friend)
		o.end_date = friend_rem.start_date
		o.save()
		pass

	m = Marge(db_friends, new_friends,
			comp_func = lambda l, r: cmp(l.friend.pk, r))
	m.full(match = refollowed, left = removed, right = followed)

def update_bios(bios, target_date = None):
	u"""
	APIから得られたユーザ情報のリストから、
	UserBioテーブルを更新する。
	"""
	if target_date is None: target_date = time.time() - 60*60*24

	for bio_data in bios:
		user = UserProfile.objects.get_or_create(user_id = bio_data['id'])[0]
		bio = UserBio.objects.get_or_create(user = user)[0]
		if bio.update_date <= target_date:
			bio.screen_name = bio_data['screen_name']
			bio.icon_url = bio_data['profile_image_url']
			bio.update_date = time.time()
			bio.save()

def update_screen_names(users):
	u"""
	APIから得られたuser情報のリストから、
	UserScreenNameテーブルを更新する
	{ 'id' : id, 'screen_name' : 'name' }
	"""
	for user_data in users:
		user_id = user_data['id']
		screen_name = user_data['screen_name']
		user = UserProfile.objects.get_or_create(user_id = user_id)[0]
		
		user_screen_name = None
		try:
			user_screen_name = user.screen_names_now
		except UserScreenName.DoesNotExist: pass

		if user_screen_name is None or user_screen_name.screen_name != screen_name:
			user_screen_name_new = user.screen_names.create(screen_name = screen_name)
			if user_screen_name is not None :
				# screen_nameの変更された時
				user_screen_name.end_date = user_screen_name_new.start_date
				user_screen_name.save()

