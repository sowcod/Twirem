#-*- coding: utf-8 -*-

from twirem.main.models import UserProfile, UserScreenName
from twirem.arrayutil import Marge

class IteratorProxy(object):
	def __init__(self, iteratableList, vfunc):
		self.iteratableList = iteratableList
		self.vfunc = vfunc
	def __iter__(self):
		for o in self.iteratableList: 
			yield self.vfunc(o)
	def __getitem__(self, index):
		return self.vfunc(self.iteratableList[index])
	def __len__(self):
		return self.iteratableList.__len__()

def users_noactivity(user_id):
	u"""
	user_id の自分自身・フレンド・フォロワーのうち、
	activityの低い順にユーザIDを返す。
	"""
	user = UserProfile.objects.get(user_id = user_id)
	friends = IteratorProxy(user.friends_now.order_by('friend'), lambda o: o.friend)
	followers = IteratorProxy(user.followers_now.order_by('user'), lambda o: o.user)

	users = []
	m = Marge(friends, followers, 
			comp_func = lambda l,r: cmp(l.user_id, r.user_id))
	m.full(match = lambda l, r: users.append(l),
			left = lambda o: users.append(o),
			right = lambda o: users.append(o))

	users.sort(cmp = lambda a, b: cmp(a.activity, b.activity))

	return users

def update_followers(user_id, followers):
	u"""
	user_id のフォロワーを、
	followers(intの配列) のユーザで更新する。
	"""
	new_followers = followers[:]
	new_followers.sort()
	user = UserProfile.get_or_create(user_id = user_id)
	db_followers = user.followers_now.order_by('user')

	def removed(o):
		friend_rem = user.followers.create(user = o.user, unfollow = True)
		o.end_date = friend_rem.start_date
		o.save()
	def followed(uid):
		user.followers.create(user = UserProfile.get_or_create(user_id = uid))
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
	user = UserProfile.get_or_create(user_id = user_id)
	db_friends = user.friends_now.order_by('friend')

	def removed(o):
		friend_rem = user.friends.create(friend = o.friend, unfollow = True)
		o.end_date = friend_rem.start_date
		o.save()
		pass
	def followed(uid):
		user.friends.create(friend = UserProfile.get_or_create(user_id = uid))
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

def update_screen_names(users):
	u"""
	APIから得られたuser情報のリストから、
	UserScreenNameテーブルを更新する
	{ 'id' : id, 'screen_name' : 'name' }
	"""
	for user_data in users:
		user_id = user_data['id']
		screen_name = user_data['screen_name']
		user = UserProfile.get_or_create(user_id = user_id)
		
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

