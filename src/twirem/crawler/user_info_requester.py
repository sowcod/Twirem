#-*- coding: utf-8 -*-

from pagelistingapis import FriendIds, FollowerIds

class UserInfoRequester(object):
	def __init__(self, api):
		self.api = api
	
	def lookup(self, ids):
		u"""
		id: ユーザID(string)の配列
		ユーザ情報をlookupして結果を返す。
		ユーザIDが100件以上の場合は、
		内部的に分割してリクエストする。
		"""
		users = []
		i = 0
		idslen = len(ids)
		if idslen == 0 : return
		for i in range(int(idslen/100) + 1):
			begin = i * 100
			end = min(begin + 100, idslen) 
			users += self.api.user_lookup(user_id = ids[begin:end])
		
		return users

	def request_friend_ids(self, user_id):
		u"""
		user_id : int
		ユーザの最新のフレンドIDを取得し、返す。
		ユーザ情報が無い分リクエスト数が少ない。
		"""
		friends = [o for o in FriendIds(self.api, user_id = user_id)]
		friends.sort()

		return friends

	def request_follower_ids(self, user_id):
		u"""
		user_id : int
		ユーザの最新のフォロワーIDを取得し、返す。
		ユーザ情報が無い分リクエスト数が少ない。
		"""
		followers = [o for o in FollowerIds(self.api, user_id = user_id)]
		followers.sort()

		return followers

